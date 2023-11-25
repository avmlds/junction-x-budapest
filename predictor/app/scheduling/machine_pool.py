from typing import List, Union

from scheduling.base import AllocatableEntity
from scheduling.diseases import Cancer
from scheduling.machines import BaseMachine


class MachinePool(AllocatableEntity):
    def __init__(self, name: str, machines: List[Union[BaseMachine, "MachinePool"]]):
        self._name = name
        self.machines = machines

    def name(self):
        return self._name

    def get_all_machines(self) -> List[BaseMachine]:
        machines = []
        for machine in self.machines:
            machines.extend(machine.get_all_machines())
        return machines

    def deallocate(self):
        raise NotImplementedError

    def probability_to_treat(self):
        unique_machines = set(self.machines)
        return sum(m.probability_to_treat() for m in unique_machines)

    @property
    def total_quantity(self):
        return sum(machine.total_quantity for machine in self.machines)

    @property
    def is_allocated(self):
        return all(machine.is_allocated for machine in self.machines)

    def allocate(self, cancer: Cancer):
        machine = self.select_machines(cancer)
        machine.allocate(cancer)
        return machine

    @property
    def available_treatments(self):
        treatments = set()
        for machine in self.machines:
            treatments.update(machine.available_treatments)
        return treatments

    def select_machines(self, cancer: Cancer):
        return self.machine_gen(cancer)

    def can_treat(self, cancer: Cancer):
        return cancer.__class__ in self.available_treatments

    def machine_gen(self, cancer: Cancer):

        machines = []
        for m in self.machines:
            if m.can_treat(cancer) and not m.is_allocated:
                machines.extend(m.machine_gen(cancer))

        return sorted(machines, key=lambda machine: machine.name())
