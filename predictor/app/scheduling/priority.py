from typing import List

from scheduling.calendar import MachineCalendar, Period
from scheduling.machines import BaseMachine


class MachinePriority:
    """Priority allocator.

    Order machines according to their capabilities.
    Less capable machines will go first.
    """

    @classmethod
    def prioritize(cls, machines: List[BaseMachine]):
        return sorted(machines, key=lambda machine: machine.probability_to_treat())

    @classmethod
    def get_balanced(
        cls, machine_calendar: MachineCalendar, machines: List[BaseMachine]
    ) -> List[BaseMachine]:

        return sorted(
            cls.prioritize(machines),
            key=lambda machine: machine_calendar[machine].load_level(),
            reverse=True,
        )
