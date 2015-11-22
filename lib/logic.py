from django.db import connection

from . import models


def __nodes():
    """
    fetch all route combinations from graph
    --
    only near nodes
    st_1 and st_2: (pos1 = pos2 - 1) or (pos1 = pos2 + 1)
    """
    cursor = connection.cursor()
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
        models.DirectionStation._meta.db_table,
        models.DirectionStation._meta.db_table,
    ))
    return cursor.fetchall()


def __find_routes(start, end, weekday):
    """
    find route for selected stations
    --
    start station must be lt than end station
    """
    cursor = connection.cursor()
    cursor.execute("""
        select rs.route_id, tt.time
        from %s tt left join
        (
            select rs1.route_id route_id
            from %s rs1 inner join %s rs2
            on
                rs1.route_id = rs2.route_id
                and
                rs1.station_id != rs2.station_id
                and
                rs1.position < rs2.position
            where
                rs1.station_id = %s
                and
                rs2.station_id = %s
        ) rs
        on
            rs.route_id = tt.route_id
        where
            rs.route_id is not null
            and
            tt.weekday = %s
        order by
            tt.time
    """ % (
        models.Timetable._meta.db_table,
        models.RouteStation._meta.db_table,
        models.RouteStation._meta.db_table,
        start,
        end,
        weekday,
    ))
    return cursor.fetchall()


def search_route(start, end):
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
                paths.append(path + [n])
            _process(pp, nodes[:], path + [n], points | set((pp,)))

    _process(start, nodes[:])

    # calculate chunk times here
    path = min(paths, key=len)

    # load objects
    pp = []
    for p in path:
        s, d, e = p
        pp.append((
            models.Station.objects.get(pk=s),
            models.Direction.objects.get(pk=d),
            models.Station.objects.get(pk=e),
        ))

    return pp
