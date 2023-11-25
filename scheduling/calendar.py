import copy
from typing import List, Optional


class AllocationError(Exception):
    def __init__(self, time_to_allocate: int):
        super().__init__(f"Can't allocate {time_to_allocate} minutes.")


class NotEnoughDaysError(Exception):
    def __init__(self):
        super().__init__("Not enough days to allocate")


class Day:

    def __str__(self):
        return f"{self.__class__.__name__}(time_left={self.time_left()})"

    def __repr__(self):
        return self.__str__()

    def __init__(self):
        self._day_length_minutes = 8 * 60
        self._time_limit_minutes = copy.copy(self._day_length_minutes)

        self.appointments: List[str] = []

    def time_left(self):
        return self._time_limit_minutes

    def can_allocate(self, minutes_to_allocate: int):
        return self.time_left() >= minutes_to_allocate

    def allocate(self, minutes_to_allocate: int):
        if (self._time_limit_minutes - minutes_to_allocate) >= 0:
            self._time_limit_minutes -= minutes_to_allocate
        else:
            raise AllocationError(minutes_to_allocate)

        return self.time_left()

    def release(self, minutes_to_release: int):
        if (self._time_limit_minutes + minutes_to_release) >= self._day_length_minutes:
            self._time_limit_minutes = self._day_length_minutes
        else:
            self._time_limit_minutes += minutes_to_release
        return self.time_left()


class Period:

    def __str__(self):
        return f"{self.__class__.__name__}(period_length_days={self.period_length_days})"

    def __repr__(self):
        return self.__str__()

    def __init__(self, period_length_days: int = 365):
        self.period_length_days = period_length_days
        self.days = [Day() for _ in range(self.period_length_days)]

    def _can_allocate_row(self, minutes_to_allocate: int, days_to_allocate: int, shift: int = 0):
        return all(day.can_allocate(minutes_to_allocate) for day in self.days[shift:shift + days_to_allocate])

    def _allocate_row(self, minutes_to_allocate: int, days_to_allocate: int, shift: int = 0):
        for day in self.days[shift:shift + days_to_allocate]:
            day.allocate(minutes_to_allocate)
        return self

    def can_allocate(
        self,
        days_to_allocate: int,
        minutes_to_allocate: int,
        shift: Optional[int] = 0,
    ):

        if shift + days_to_allocate > self.period_length_days:
            raise NotEnoughDaysError

        return self._can_allocate_row(minutes_to_allocate, days_to_allocate, shift)

    def allocate(
        self,
        days_to_allocate: int,
        minutes_to_allocate: int,
        shift: Optional[int] = 0,
    ):
        if not self.can_allocate(days_to_allocate, minutes_to_allocate):
            raise AllocationError(minutes_to_allocate)

        return self._allocate_row(minutes_to_allocate, days_to_allocate, shift)
