from typing import List, Union

from scheduling.base import AllocatableEntity
from scheduling.machines import BaseMachine


class MachinePool(AllocatableEntity):

    def __init__(self, name: str, machines: List[Union[BaseMachine, "MachinePool"]]):
        self._name = name
        self.machines = machines

    def name(self):
        return self._name

    def deallocate(self):
        raise NotImplementedError

    @property
    def is_allocated(self):
        return all(machine.is_allocated for machine in self.machines)

    def allocate(self, cancer_type: str):
        machine = self.select_machine(cancer_type)
        machine.allocate(cancer_type)
        return machine

    @property
    def available_treatments(self):
        treatments = set()
        for machine in self.machines:
            treatments.update(machine.available_treatments)
        return treatments

    def select_machine(self, cancer_type: str):
        return next(self.machine_gen(cancer_type))

    def can_treat(self, cancer_type: str):
        return cancer_type in self.available_treatments

    def machine_gen(self, cancer_type: str):
        machines = [m for m in self.machines if m.can_treat(cancer_type) and not m.is_allocated]
        for machine in machines:
            yield from machine.machine_gen(cancer_type)
