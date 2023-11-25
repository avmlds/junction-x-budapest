import random
import uuid
from typing import Type

from scheduling.diseases import Cancer


class Patient:
    def __init__(self, name: str, cancer_type: Cancer):
        super().__init__()
        self.name = name or str(uuid.uuid4())
        self.cancer_type = cancer_type
        self.treatment_time = random.choice(self.cancer_type.treatment_time)
