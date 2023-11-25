import random
import uuid
from typing import Generator

from scheduling.diseases import Cancer
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


class Patient:
    def __init__(self, name: str, cancer: Cancer):
        super().__init__()
        self.name = name or str(uuid.uuid4())
        self.cancer = cancer
        self.fraction_time_days = None

    def assign_fraction_time(self):
        self.fraction_time_days = random.choice(self.cancer.fraction_time())
        return self.fraction_time_days


class PatientGen:

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

    def get_patient(self) -> Generator[Patient, None, None]:
        while True:
            cancer = random.choices(
                self.cancers, weights=[cancer.probability() for cancer in self.cancers]
            )[0]
            yield Patient(name=str(uuid.uuid4()), cancer=cancer())
