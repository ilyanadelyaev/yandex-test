class Enum(object):
    class __Meta(type):
        def __call__(cls, wd):
            return cls._to_str(wd)

    __metaclass__ = __Meta

    @classmethod
    def _to_str(cls, wd):
        try:
            wd = int(wd)
        except (ValueError, TypeError):
            return None
        return cls._choices.get(wd, None)


class Weekday(Enum):
    monday = 0
    tuesday = 1
    wednesday = 2
    thursday = 3
    friday = 4
    saturday = 5
    sunday = 6

    choices = (
        (monday, 'Monday'),
        (tuesday, 'Tuesday'),
        (wednesday, 'Wednesday'),
        (thursday, 'Thursday'),
        (friday, 'Friday'),
        (saturday, 'Saturday'),
        (sunday, 'Sunday'),
    )

    _choices = dict(choices)


class TimeInterval(Enum):
    _all = 0
    _0_9 = 1
    _9_12 = 2
    _12_15 = 3
    _15_21 = 4
    _21_24 = 5

    choices = (
        (_all, None),
        (_0_9, (0, 9)),
        (_9_12, (9, 12)),
        (_12_15, (12, 15)),
        (_15_21, (15, 21)),
        (_21_24, (21, 24)),
    )

    _choices = dict(choices)
