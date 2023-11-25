import random

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
)
from scheduling.patients import Patient


class DataGeneration:

    cancers = [
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
    ]

    def __init__(self):
        distribution_size = 10_000

    def get_patient(self):
        cancer = random.choices(self.cancers, weights=[cancer.probability for cancer in self.cancers])
        patient = Patient()
