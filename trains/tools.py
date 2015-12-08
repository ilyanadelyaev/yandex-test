class _EnumMeta(type):
    def __init__(cls, name, bases, dct):
        super(_EnumMeta, cls).__init__(name, bases, dct)
        cls._choices = dict(cls.__dict__['choices']) \
            if 'choices' in cls.__dict__ else dict()

    def __call__(cls, key):
        return cls._to_str(key)


class Enum(object):
    __metaclass__ = _EnumMeta

    @classmethod
    def _to_str(cls, key):
        try:
            key = int(key)
        except (ValueError, TypeError):
            return None
        return cls._choices.get(key, None)


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
