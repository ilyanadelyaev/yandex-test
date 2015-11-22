class Weekday(object):
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

    class __Meta(type):
        def __call__(cls, wd):
            return cls._to_str(wd)
    __metaclass__ = __Meta

    __choices = dict(choices)

    @classmethod
    def _to_str(cls, wd):
        return cls.__choices.get(wd, '')
