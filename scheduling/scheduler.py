import sys
from typing import Optional, List

from matplotlib import pyplot as plt
from prettytable import PrettyTable

from scheduling.priority import MachinePriority

from scheduling.diseases import Cancer
from scheduling.machines import BaseMachine
from scheduling.patients import PatientGen
from scheduling.calendar import Period, MachineCalendar
from scheduling.machine_pool import MachinePool


class ExtendScheduleError(Exception):
    def __init__(self):
        super().__init__("We need to extend schedule!")


class Scheduler:
    DRAW_SLEEP = 0.00001

    def __init__(
        self,
        period_length_days: int,
        machine_pool: MachinePool,
        patient_generator: PatientGen,
    ):
        self.machine_pool = machine_pool
        self.period_length_days = period_length_days
        self.calendar = MachineCalendar(self.machine_pool, period_length_days)
        self.patient_generator = patient_generator

    def schedule(self):
        """Schedule appointments."""
        plt.ion()
        fig, ax = plt.subplots()

        for patient in self.patient_generator.get_patient():
            ax.clear()

            try:
                self.process_patient(patient)
            except ExtendScheduleError:
                self.calendar.get_report_data()
                return

            self.calendar.visualize(ax)
            plt.pause(self.DRAW_SLEEP)
            plt.draw()

    @staticmethod
    def allocate_segment(period: Period, cancer: Cancer, days: int, shift: int) -> bool:
        if period.can_allocate(days, cancer.treatment_time_minutes(), shift):
            period.allocate(days, cancer.treatment_time_minutes(), shift)
            return True
        return False

    def deallocate_machines(self, machines_to_deallocate: List[BaseMachine]):
        if machines_to_deallocate:
            machine = machines_to_deallocate.pop(0)
            while machine:
                machine.deallocate()
                try:
                    machine = machines_to_deallocate.pop(0)
                except IndexError:
                    machine = None

    def get_machine(
        self,
        cancer: Cancer,
        days: int,
        shift: int = 0,
    ) -> Optional[BaseMachine]:

        machines = self.machine_pool.select_machines(cancer)
        balancer = MachinePriority()
        balanced_machines = balancer.get_balanced(self.calendar, machines)

        for machine in balanced_machines:
            period = self.calendar[machine]
            allocated = self.allocate_segment(period, cancer, days, shift)
            if allocated:
                return machine
        return None

    def process_patient(self, patient):
        days = patient.assign_fraction_time()  # length of the sliding window
        cancer = patient.cancer

        machine = None
        for shift in range(self.period_length_days - days):
            machine = self.get_machine(cancer, days, shift)
            if machine:
                table = PrettyTable(field_names=["Field", "Value"], align="r")
                table.add_rows(
                    [
                        ["Machine", machine.name()],
                        ["Allocated for", days],
                        ["Day shift", shift],
                        ["Cancer", cancer.name()],
                        ["Treatment time, minutes", cancer.treatment_time_minutes()],
                    ]
                )
                print(table)
                break
            else:
                print(f"No suitable machine for shift {shift}")

        if not machine:
            raise ExtendScheduleError
