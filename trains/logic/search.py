import datetime

import django.db

import trains.models
import trains.logic.errors


def __nodes():
    """
    fetch all route combinations from graph
    --
    only near nodes
    st_1 and st_2: (pos1 = pos2 - 1) or (pos1 = pos2 + 1)
    --
    node is tuple, len=3:
    0 - first_point (Station.ID)
    1 - direction (Direction_ID)
    2 - second_point (Station_ID)
    """
    cursor = django.db.connection.cursor()
    cursor.execute("""
        select ds1.station_id, ds1.direction_id, ds2.station_id
        from
        %s ds1 inner join %s ds2
        on
            ds1.station_id != ds2.station_id
            and
            ds1.direction_id = ds2.direction_id
            and
            abs(ds1.position - ds2.position) = 1
    """ % (
        trains.models.DirectionStation._meta.db_table,
        trains.models.DirectionStation._meta.db_table,
    ))
    return cursor.fetchall()


def __find_paths(start_point, end_point, nodes, path=None, points=None):
    """
    Find shortest path between start and end points via graph

    - nodes - all nodes from direction's table / see __nodes() for more info
    - start_point - lookup from this point
    - end_point - lookup till this point
    - path - current path
    - points - processed points
    """
    # init start conditions
    if path is None:
        path = []
    if points is None:
        points = set((start_point,))
    result = []

    # get nodes belongs to start_point
    nearest_nodes = filter(lambda x: x[0] == start_point, nodes)

    # recurcively search nearest nodes for end_point
    # node - see docstring
    for node in nearest_nodes:
        # node processed - remove to exclude repeated paths
        nodes.remove(node)

        # next point = node second point
        next_point = node[2]

        # already processed for current path
        if next_point in points:
            continue

        # path found. append to paths to return
        if next_point == end_point:
            # TODO: if len(path = [node]) == 1: return
            result.append(path + [node])

        # make search again for next point
        result.extend(
            __find_paths(
                next_point,  # next point as start point
                end_point,  # look up till end point
                nodes[:],  # copy nodes to make changes for current path
                path + [node],  # current path
                points | set((next_point,)),  # processed points
            )
        )

    return result


def __find_routes(start, end, weekday, timeinterval):
    """
    find route for selected stations
    --
    start station must be lt than end station
    """
    cursor = django.db.connection.cursor()
    cursor.execute("""
        select
            rrr.route_id, tt.time
        from
            {timetable} tt left join
            (
            -- intersect two RouteStation tables
            -- to find sutable route for start/end station pair
            -- add DirectionStation table for positions
            select
                r.id route_id
            from
                (
                select
                    distinct rds1.route_id route_id
                from
                    (
                    select
                        rs.route_id route_id,
                        ds.station_id station_id,
                        ds.position position
                    from
                        {directionstation} ds inner join {routestation} rs
                    on
                        ds.station_id = rs.station_id
                    ) rds1
                inner join
                    (
                    select
                        rs.route_id route_id,
                        ds.station_id station_id,
                        ds.position position
                    from
                        {directionstation} ds inner join {routestation} rs
                    on
                        ds.station_id = rs.station_id
                    ) rds2
                on
                    rds1.route_id = rds2.route_id
                    and
                    rds1.station_id != rds2.station_id
                where
                    rds1.station_id = {start}
                    and
                    rds2.station_id = {end}
                ) rr
            inner join
                {route} r
            on
                r.id = rr.route_id
            where
                -- fetch station positions
                -- for RouteStation from DirectionStation
                (
                    (
                        (select position from {directionstation}
                            where direction_id = r.direction_id
                            and
                            station_id = r.start_station_id)
                        >
                        (select position from {directionstation}
                            where direction_id = r.direction_id
                            and
                            station_id = r.end_station_id)
                    )
                    and
                    (
                        (select position from {directionstation}
                            where direction_id = r.direction_id
                            and
                            station_id = {start})
                        >
                        (select position from {directionstation}
                            where direction_id = r.direction_id
                            and
                            station_id = {end})
                    )
                )
                or
                (
                    (
                        (select position from {directionstation}
                            where direction_id = r.direction_id
                            and
                            station_id = r.start_station_id)
                        <
                        (select position from {directionstation}
                            where direction_id = r.direction_id
                            and
                            station_id = r.end_station_id)
                    )
                    and
                    (
                        (select position from {directionstation}
                            where direction_id = r.direction_id
                            and
                            station_id = {start})
                        <
                        (select position from {directionstation}
                            where direction_id = r.direction_id
                            and
                            station_id = {end})
                    )
                )
            ) rrr
        on
            rrr.route_id = tt.route_id
        where
            rrr.route_id is not null
            and
            tt.weekday = {weekday}
            and
            tt.time >= "{timeinterval_start}"
            and
            tt.time <= "{timeinterval_end}"
        order by
            tt.time
    """.format(
        directionstation=trains.models.DirectionStation._meta.db_table,
        routestation=trains.models.RouteStation._meta.db_table,
        route=trains.models.Route._meta.db_table,
        timetable=trains.models.Timetable._meta.db_table,
        start=start,
        end=end,
        weekday=weekday,
        timeinterval_start=timeinterval[0],
        timeinterval_end=timeinterval[1],
    ))
    return cursor.fetchall()


def __raw_routes_to_models(raw_routes):
    """
    Convert Station_ID, Direction_ID and Route_ID to models
    """
    ret = []
    for start_point, end_point, direction, routes_with_time in raw_routes:
        ret.append({
            'start_station': trains.models.Station.objects.get(pk=start_point),
            'end_station': trains.models.Station.objects.get(pk=end_point),
            'direction': trains.models.Direction.objects.get(pk=direction),
            # split routes with time
            'routes': [{
                'route': trains.models.Route.objects.get(pk=route),
                'time': time,
            } for route, time in routes_with_time],
        })
    return ret


def search_routes(start, end, date, timeinterval):
    """
    Search routes from start to end station
    for selected weekday and time interval

    Return dict with models
    """

    # convert start and end points to integer
    try:
        start = int(start)
    except (ValueError, TypeError):
        raise trains.logic.errors.InvalidSearchArguments(
            'Invalid: START argument must be INT value.'
            ' START = "{}"'.format(start))
    #
    try:
        end = int(end)
    except (ValueError, TypeError):
        raise trains.logic.errors.InvalidSearchArguments(
            'Invalid: END argument must be INT value. END = "{}"'.format(end))
    try:
        weekday = datetime.datetime.strptime(date, '%m/%d/%Y').date().weekday()
    except ValueError:
        raise trains.logic.errors.InvalidSearchArguments(
            'Invalid: DATE argument must be "MM/DD/YYYY".'
            ' DATE = "{}"'.format(date))
    #
    if start == end:
        raise trains.logic.errors.InvalidSearchArguments(
            'Invalid: START equal END : "{}" == "{}"'.format(start, end))

    # set time interval to whole day if not present
    if timeinterval is None:
        timeinterval = (0, 24)
    try:
        timeinterval = (
            datetime.time(timeinterval[0], 0),
            datetime.time(timeinterval[1] - 1, 59)
        )
    except ValueError:
        raise trains.logic.errors.InvalidSearchArguments(
            'Invalid: TIMEINTERVAL values must be [ (0..24), (0..24) ].'
            ' TIMEINTERVAL = "{}"'.format(timeinterval))

    # fetch all graph nodes from database
    nodes = __nodes()

    # find paths from start to end points using nodes
    paths = __find_paths(start, end, nodes[:])

    if not paths:
        raise trains.logic.errors.UnboundedStations(
            'Unbounded stations: "{}" and "{}"'.format(start, end))

    # TODO: give path size by time
    raw_path = min(paths, key=len)

    # clean raw path - keep only start and end point for direction
    path = []
    start_point, direction, end_point = (None,) * 3
    for node in raw_path:
        #
        s, d, e = node
        # next direction on route
        if direction is not None and direction != d:
            path.append((start_point, direction, end_point))
            start_point = s
            direction = d
        # init input
        if direction is None:
            direction = d
        if start_point is None:
            start_point = s
        #
        end_point = e
    # last point
    path.append((start_point, direction, end_point))

    # find raw routes for path
    # include all variants for all days and times
    # will splitted in next section
    raw_routes = [
        (
            start_point,
            end_point,
            direction,
            __find_routes(
                start_point,
                end_point,
                weekday,
                timeinterval
            )
        )
        for start_point, direction, end_point in path
    ]

    return __raw_routes_to_models(raw_routes)
