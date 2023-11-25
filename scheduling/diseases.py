import random
from typing import List

from scheduling.constants import (
    CRAINOSPINAL_PROBABILITY,
    CRAINOSPINAL_FRACTION_NUMBER,
    BREAST_PROBABILITY,
    BREAST_FRACTION_NUMBER,
    BREAST_SPECIAL_PROBABILITY,
    BREAST_SPECIAL_FRACTION_NUMBER,
    HEAD_NECK_PROBABILITY,
    HEAD_NECK_FRACTION_NUMBER,
    ABDOMEN_PROBABILITY,
    ABDOMEN_FRACTION_NUMBER,
    PELVIS_PROBABILITY,
    PELVIS_FRACTION_NUMBER,
    CRANE_PROBABILITY,
    CRANE_FRACTION_NUMBER,
    LUNG_PROBABILITY,
    LUNG_FRACTION_NUMBER,
    LUNG_SPECIAL_PROBABILITY,
    LUNG_SPECIAL_FRACTION_NUMBER,
    WHOLE_BRAIN_PROBABILITY,
    WHOLE_BRAIN_FRACTION_NUMBER,
)


class Cancer:

    _probability: float
    _fraction_time: List[str]
    _treatment_time: int

    def name(self):
        return self.__class__.__name__.lower()

    @property
    def probability(self) -> float:
        return self._probability

    @property
    def fraction_time(self):
        return self._fraction_time

    @property
    def treatment_time(self):
        return self._treatment_time


class Crainospinal(Cancer):
    _probability = CRAINOSPINAL_PROBABILITY
    _fraction_time = CRAINOSPINAL_FRACTION_NUMBER
    _treatment_time = 30


class Breast(Cancer):
    _probability = BREAST_PROBABILITY
    _fraction_time = BREAST_FRACTION_NUMBER
    _treatment_time = 12


class BreastSpecial(Cancer):
    _probability = BREAST_SPECIAL_PROBABILITY
    _fraction_time = BREAST_SPECIAL_FRACTION_NUMBER
    _treatment_time = 20


class HeadNeck(Cancer):
    _probability = HEAD_NECK_PROBABILITY
    _fraction_time = HEAD_NECK_FRACTION_NUMBER
    _treatment_time = 12


class Abdomen(Cancer):
    _probability = ABDOMEN_PROBABILITY
    _fraction_time = ABDOMEN_FRACTION_NUMBER
    _treatment_time = 12


class Pelvis(Cancer):
    _probability = PELVIS_PROBABILITY
    _fraction_time = PELVIS_FRACTION_NUMBER
    _treatment_time = 12


class Crane(Cancer):
    _probability = CRANE_PROBABILITY
    _fraction_time = CRANE_FRACTION_NUMBER
    _treatment_time = 10


class Lung(Cancer):
    _probability = LUNG_PROBABILITY
    _fraction_time = LUNG_FRACTION_NUMBER
    _treatment_time = 12


class LungSpecial(Cancer):
    _probability = LUNG_SPECIAL_PROBABILITY
    _fraction_time = LUNG_SPECIAL_FRACTION_NUMBER
    _treatment_time = 15


class WholeBrain(Cancer):
    _probability = WHOLE_BRAIN_PROBABILITY
    _fraction_time = WHOLE_BRAIN_FRACTION_NUMBER
    _treatment_time = 10
