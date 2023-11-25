from typing import Optional, List

from matplotlib import pyplot as plt
import matplotlib

matplotlib.use("TkAgg")

from scheduling.diseases import Cancer
from scheduling.machines import BaseMachine
from scheduling.patients import PatientGen
from scheduling.calendar import Period, MachineCalendar
from scheduling.machine_pool import MachinePool


class Scheduler:
    DRAW_SLEEP = 0.01

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
            self.process_patient(patient)

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
        period: Period = None,
        to_deallocate: List[BaseMachine] = None,
        shift: int = 0,
    ) -> Optional[BaseMachine]:

        try:
            machine = self.machine_pool.select_machine(cancer)
        except StopIteration as e:
            print(f"Can't allocate machine for {days} with shift.")
            return None

        if period is None:
            period = self.calendar[machine]

        allocated = self.allocate_segment(period, cancer, days, shift)
        if allocated:
            self.deallocate_machines(to_deallocate)
            return machine

        machine.allocate(cancer)
        if to_deallocate is None:
            to_deallocate = [machine]
        else:
            to_deallocate.append(machine)

        return self.get_machine(cancer, days, None, to_deallocate, shift)

    def process_patient(self, patient):
        days = patient.assign_fraction_time()  # length of the sliding window
        cancer = patient.cancer

        machine = None
        for shift in range(self.period_length_days - days):
            machine = self.get_machine(cancer, days, None, [], shift)
            if machine:
                print(
                    f"Machine:        {machine.name()}\n"
                    f"Allocated for:  {days} days\n"
                    f"Day shift:      {shift} days\n"
                    f"Cancer:         '{cancer.name()}'\n"
                    f"Treatment time:  {cancer.treatment_time_minutes()}\n"
                )
                break
            else:
                print("No suitable machine")
        if not machine:
            raise Exception("We need to extend schedule!")
