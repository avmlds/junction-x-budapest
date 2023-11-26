import datetime
from typing import Set

from scheduling.constants import (
    MACHINE_TB1,
    MACHINE_TB2,
    MACHINE_VB1,
    MACHINE_VB2,
    MACHINE_U,
)
from scheduling.base import AllocatableEntity
from scheduling.diseases import (
    Crainospinal,
    Breast,
    BreastSpecial,
    HeadNeck,
    Abdomen,
    Pelvis,
    Crane,
    Lung,
    LungSpecial,
    WholeBrain,
    Cancer,
)


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
    _available_treatments: Set[Cancer]
    _color: str

    @property
    def color(self):
        return self._color

    def name(self):
        return self._name

    @property
    def total_quantity(self):
        return 1

    def get_all_machines(self):
        return [self]

    @classmethod
    def probability_to_treat(cls):
        return sum(cancer.probability() for cancer in cls._available_treatments)

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

    def allocate(self, cancer: Cancer):
        if self._allocated:
            raise AlreadyAllocated
        if self.can_treat(cancer):
            self._allocated = True
        else:
            raise
        return self

    def deallocate(self):
        if not self._allocated:
            raise AlreadyDeallocated
        self._allocated = False
        return self

    def to_dict(self):
        return {
            "name": self.name(),
            "probability_to_treat": self.probability_to_treat(),
            "available_treatments": [
                cancer.to_dict() for cancer in self.available_treatments
            ],
        }

    @property
    def available_treatments(self):
        return self._available_treatments

    def can_treat(self, cancer: Cancer) -> bool:
        return cancer.__class__ in self.available_treatments

    def on_maintenance(self) -> bool:
        return self._on_maintenance

    def set_maintenance(self):
        self._on_maintenance = True
        return self._on_maintenance

    def unset_maintenance(self):
        self._on_maintenance = False
        return self._on_maintenance

    def machine_gen(self, cancer: Cancer):
        return [self]


class TB1Machine(BaseMachine):
    _color = "#7fc97f"
    _name = MACHINE_TB1
    _available_treatments = (
        Crainospinal,
        Breast,
        BreastSpecial,
        HeadNeck,
        Abdomen,
        Pelvis,
        Crane,
        Lung,
        LungSpecial,
    )


class TB2Machine(TB1Machine):
    _color = "#beaed4"
    _name = MACHINE_TB2


class VB1Machine(BaseMachine):
    _color = "#fdc086"
    _name = MACHINE_VB1
    _available_treatments = {
        Breast,
        HeadNeck,
        Abdomen,
        Pelvis,
        Crane,
        Lung,
        LungSpecial,
        WholeBrain,
    }


class VB2Machine(VB1Machine):
    _color = "#ffff99"
    _name = MACHINE_VB2


class UMachine(BaseMachine):
    _color = "#386cb0"
    _name = MACHINE_U
    _available_treatments = {Breast, WholeBrain}
