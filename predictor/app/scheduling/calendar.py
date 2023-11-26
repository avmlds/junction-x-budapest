import copy
from typing import List, Optional, TYPE_CHECKING

import numpy as np
from prettytable import PrettyTable

from scheduling.constants import YEAR_LEN_DAYS

if TYPE_CHECKING:
    from scheduling.machine_pool import MachinePool

from scheduling.machines import BaseMachine


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

    def is_busy(self):
        return self.time_left() < self._day_length_minutes // 2

    def load_level(self) -> float:
        return self.time_left() / self._day_length_minutes

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
        return (
            f"{self.__class__.__name__}(period_length_days={self.period_length_days})"
        )

    def __repr__(self):
        return self.__str__()

    def __init__(self, period_length_days: int = 365):
        self.period_length_days = period_length_days
        self.days = [Day() for _ in range(self.period_length_days)]

    def is_busy(self):
        return sum([day.is_busy() for day in self.days]) > self.period_length_days // 2

    def load_level(self):
        return sum([day.load_level() for day in self.days]) / self.period_length_days

    def _can_allocate_row(
        self, minutes_to_allocate: int, days_to_allocate: int, shift: int = 0
    ):
        return all(
            day.can_allocate(minutes_to_allocate)
            for day in self.days[shift : shift + days_to_allocate]
        )

    def _allocate_row(
        self, minutes_to_allocate: int, days_to_allocate: int, shift: int = 0
    ):
        for day in self.days[shift : shift + days_to_allocate]:
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
        if not self.can_allocate(days_to_allocate, minutes_to_allocate, shift):
            raise AllocationError(minutes_to_allocate)

        return self._allocate_row(minutes_to_allocate, days_to_allocate, shift)


class MachineUsage:
    def __init__(self, name: str, usage: float):
        self.name = name
        self.usage = usage


class CalendarRow(dict):
    def __init__(self, day, machine_usage: List[MachineUsage]):
        super().__init__()
        self["day"] = day
        for machine in machine_usage:
            if self[machine.name] is not None:
                raise Exception("Already exist")
            self[machine.name] = machine.usage


class MachineCalendar:
    def __str__(self):
        return f"{self.__class__.__name__}(calendar={self.calendar})"

    def __repr__(self):
        return self.__str__()

    def __init__(
        self, machine_pool: "MachinePool", calendar_length_days: int = YEAR_LEN_DAYS
    ):
        self.calendar_length_days = calendar_length_days
        self.calendar = {
            machine: Period(calendar_length_days)
            for machine in machine_pool.get_all_machines()
        }

    def __getitem__(self, item: BaseMachine):
        return self.calendar[item]

    def get_daily_load(self, shift: int):
        daily_load = {"items": [], "average_load": 0}

        if shift >= self.calendar_length_days:
            raise NotEnoughDaysError

        machines = sorted(
            [machine for machine in self.calendar.keys()],
            key=lambda machine: machine.name(),
        )
        sum_percentages = 0
        for machine in machines:

            load_level = self.calendar[machine].days[shift].load_level()
            utilization_percentage = round((1 - load_level) * 100, 2)
            daily_load["items"].append(
                {
                    "machine_name": machine.name(),
                    "load": utilization_percentage,
                }
            )

            sum_percentages += (1 - load_level) * 100

        daily_load["average_load"] = round(sum_percentages / len(machines), 2)
        return daily_load

    def get_report_data(
        self, days: int = YEAR_LEN_DAYS, start_day: int = 0
    ) -> PrettyTable:
        machines = sorted(
            [machine for machine in self.calendar.keys()],
            key=lambda machine: machine.name(),
        )

        table = PrettyTable()
        table.title = "Utilization report"
        table.field_names = (
            ["Day"] + [machine.name() for machine in machines] + ["Average"]
        )

        for day_pointer in range(start_day, min(days, self.calendar_length_days)):

            row = [day_pointer + 1]  # just for managers, they don't like leading zero

            sum_percentages = 0
            for machine in machines:
                load_level = self.calendar[machine].days[day_pointer].load_level()
                utilization_percentage = round((1 - load_level) * 100, 2)
                sum_percentages += (1 - load_level) * 100
                row.append(f"{utilization_percentage}%")

            row.append(f"{round(sum_percentages / len(machines), 2)}%")

            table.add_row(row)
            day_pointer += 1

        return table

    def visualize(self, ax):
        x = np.arange(self.calendar_length_days)

        num_bars_in_group = len(self.calendar.keys())
        gap_between_bargroups = 0.3
        gap_between_bars_in_group = 0.03

        bar_width = (
            (1.0 - gap_between_bargroups) + gap_between_bars_in_group
        ) / num_bars_in_group

        for num, (machine, period) in enumerate(self.calendar.items()):
            ys = [day.time_left() / 100 for day in period.days]
            ax.bar(
                x + num * bar_width,
                ys,
                color=machine.color,
                width=bar_width - gap_between_bars_in_group,
                align="center",
            )
