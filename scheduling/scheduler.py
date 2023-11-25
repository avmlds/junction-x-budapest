from typing import Type

from scheduling.patients import Patient, PatientGen
from scheduling.calendar import Period
from scheduling.machine_pool import MachinePool


class Scheduler:
    def __init__(
        self,
        period: Period,
        machine_pool: MachinePool,
        patient_generator: PatientGen,
    ):
        self.period = period
        self.machine_pool = machine_pool
        self.patient_generator = patient_generator

    def process_patient(self):
        pass
