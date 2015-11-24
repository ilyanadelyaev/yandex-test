import datetime

import django.db

import trains.core.models
import trains.logic.errors


def __nodes():
    """
    fetch all route combinations from graph
    --
    only near nodes
    st_1 and st_2: (pos1 = pos2 - 1) or (pos1 = pos2 + 1)
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
        trains.core.models.DirectionStation._meta.db_table,
        trains.core.models.DirectionStation._meta.db_table,
    ))
    return cursor.fetchall()


def __find_routes(start, end, weekday):
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
            -- intersect two RouteStation tables to find sutable route for start/end station pair
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
                -- fetch station positions for RouteStation from DirectionStation
                (
                    (
                        (select position from {directionstation}
                            where direction_id = r.direction_id and station_id = r.start_station_id)
                        >
                        (select position from {directionstation}
                            where direction_id = r.direction_id and station_id = r.end_station_id)
                    )
                    and
                    (
                        (select position from {directionstation}
                            where direction_id = r.direction_id and station_id = {start})
                        >
                        (select position from {directionstation}
                            where direction_id = r.direction_id and station_id = {end})
                    )
                )
                or
                (
                    (
                        (select position from {directionstation}
                            where direction_id = r.direction_id and station_id = r.start_station_id)
                        <
                        (select position from {directionstation}
                            where direction_id = r.direction_id and station_id = r.end_station_id)
                    )
                    and
                    (
                        (select position from {directionstation}
                            where direction_id = r.direction_id and station_id = {start})
                        <
                        (select position from {directionstation}
                            where direction_id = r.direction_id and station_id = {end})
                    )
                )
            ) rrr
        on
            rrr.route_id = tt.route_id
        where
            rrr.route_id is not null
            and
            tt.weekday = {weekday}
        order by
            tt.time
    """.format(
        directionstation=trains.core.models.DirectionStation._meta.db_table,
        routestation=trains.core.models.RouteStation._meta.db_table,
        route=trains.core.models.Route._meta.db_table,
        timetable=trains.core.models.Timetable._meta.db_table,
        start=start,
        end=end,
        weekday=weekday,
    ))
    return cursor.fetchall()


def search_routes(start, end, date, timeinterval):
    try:
        start = int(start)
    except (ValueError, TypeError):
        raise trains.logic.errors.InvalidSearchArguments(
            'Invalid: START argument must be INT value. START = "{}"'.format(start))
    try:
        end = int(end)
    except (ValueError, TypeError):
        raise trains.logic.errors.InvalidSearchArguments(
            'Invalid: END argument must be INT value. END = "{}"'.format(end))
    try:
        weekday = datetime.datetime.strptime(date, '%m/%d/%Y').date().weekday()
    except ValueError:
        raise trains.logic.errors.InvalidSearchArguments(
            'Invalid: DATE argument must be "MM/DD/YYYY". DATE = "{}"'.format(date))

    if start == end:
        raise trains.logic.errors.InvalidSearchArguments(
            'Invalid: START equal END : "{}" == "{}"'.format(start, end))

    nodes = __nodes()

    paths = []

    def _process(p, nodes, path=None, points=None):
        if path is None:
            path = []
        if points is None:
            points = set((p,))
        pn = filter(lambda x: x[0] == p, nodes)
        append = False
        for n in pn:
            nodes.remove(n)
            pp = n[2]
            if pp in points:
                continue
            if pp == end:
                # TODO: if len(path = [n]) == 1: return
                paths.append(path + [n])
            _process(pp, nodes[:], path + [n], points | set((pp,)))

    _process(start, nodes[:])

    if not paths:
        raise trains.logic.errors.UnboundedStations('Unbounded stations: "{}" and "{}"'.format(start, end))

    # TODO: give path size by time
    path = min(paths, key=len)

    # remove middle nodes from path
    pp = []
    st, dr, ed = (None,) * 3
    for p in path:
        s, d, e = p
        if dr is not None and dr != d:
            pp.append((st, dr, ed))
            st = s
            dr = d
        if dr is None:
            dr = d
        if st is None:
            st = s
        ed = e
    pp.append((st, dr, ed))

    # find suitable routes
    routes = [(s, e, d, __find_routes(s, e, weekday)) for s, d, e in pp]

    def __routes_with_models(routes):
        ret = []
        for i in routes:
            s, e, d, rr = i
            ret.append((
                trains.core.models.Station.objects.get(pk=s),
                trains.core.models.Station.objects.get(pk=e),
                trains.core.models.Direction.objects.get(pk=d),
                [((trains.core.models.Route.objects.get(pk=r), t)) for r, t in rr],
            ))
        return ret

    return __routes_with_models(routes)


def check_consistency():
    pass
