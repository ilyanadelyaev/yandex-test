from django.db import connection

from .models import Station, Direction, DirectionStation


def __nodes():
    """
    only near nodes
    1 and 2: (pos1 = pos2 - 1) or (pos1 = pos2 + 1)
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
            abs(ds1.station_pos - ds2.station_pos) = 1
    """ % (
        DirectionStation._meta.db_table,
        DirectionStation._meta.db_table,
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
    return min(paths, key=len)
