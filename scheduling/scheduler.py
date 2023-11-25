from typing import Type

from scheduling.patients import Patient
from scheduling.calendar import Period
from scheduling.machine_pool import MachinePool


class Scheduler:

    def __init__(self, period: Period, machine_pool: MachinePool):
        self.period = period
        self.machine_pool = machine_pool

    def create_appointment(
        self,
        appointment_length: int,
        patient: Patient,
    ):
        pass
