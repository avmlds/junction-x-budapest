import datetime
from typing import Set

from constants import (
    MACHINE_TB1,
    CRAINOSPINAL,
    BREAST,
    BREAST_SPECIAL,
    HEAD_NECK,
    ABDOMEN,
    PELVIS,
    CRANE,
    LUNG,
    LUNG_SPECIAL,
    MACHINE_TB2,
    MACHINE_VB1,
    WHOLE_BRAIN,
    MACHINE_VB2,
    MACHINE_U,
)
from scheduling.base import AllocatableEntity


class AlreadyAllocated(Exception):
    def __init__(self):
        super().__init__("Already allocated")


class AlreadyDeallocated(Exception):
    def __init__(self):
        super().__init__("Already deallocated")


class InvalidCancerType(Exception):
    def __init__(self):
        super().__init__("Invalid cancer type")


class BaseMachine(AllocatableEntity):
    _name: str
    _available_treatments: Set[str]

    def name(self):
        return self._name

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name()})"

    def __repr__(self):
        return self.__str__()

    def __init__(self):
        self._on_maintenance = False
        self._allocated = False

    @property
    def is_allocated(self):
        return self._allocated

    def allocate(self, cancer_type: str):
        if self._allocated:
            raise AlreadyAllocated
        if self.can_treat(cancer_type):
            self._allocated = True
        else:
            raise
        return self

    def deallocate(self):
        if not self._allocated:
            raise AlreadyDeallocated
        self._allocated = False
        return self

    @property
    def available_treatments(self):
        return self._available_treatments

    def can_treat(self, cancer_type: str) -> bool:
        return cancer_type in self._available_treatments

    def on_maintenance(self) -> bool:
        return self._on_maintenance

    def set_maintenance(self):
        self._on_maintenance = True
        return self._on_maintenance

    def unset_maintenance(self):
        self._on_maintenance = False
        return self._on_maintenance

    def machine_gen(self, cancer_type: str):
        yield self


class TB1Machine(BaseMachine):
    _name = MACHINE_TB1
    _available_treatments = (
        CRAINOSPINAL,
        BREAST,
        BREAST_SPECIAL,
        HEAD_NECK,
        ABDOMEN,
        PELVIS,
        CRANE,
        LUNG,
        LUNG_SPECIAL,
    )


class TB2Machine(TB1Machine):
    _name = MACHINE_TB2


class VB1Machine(BaseMachine):
    _name = MACHINE_VB1
    _available_treatments = {
        BREAST,
        HEAD_NECK,
        ABDOMEN,
        PELVIS,
        CRANE,
        LUNG,
        LUNG_SPECIAL,
        WHOLE_BRAIN,
    }


class VB2Machine(VB1Machine):
    _name = MACHINE_VB2


class UMachine(BaseMachine):
    _name = MACHINE_U
    _available_treatments = {BREAST, WHOLE_BRAIN}
