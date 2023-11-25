from typing import Type

from scheduling.patients import Patient
from scheduling.calendar import Day
from scheduling.machines import BaseMachine


class Appointment:
    def __init__(
        self,
        allocated_time_minutes: int,
        patient: Patient,
        machine: Type[BaseMachine],
        day: Day,
    ):
        self.patient = patient
        self.machine = machine
        self.allocated_time_minutes = allocated_time_minutes
        self.day = day
