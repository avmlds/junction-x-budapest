from scheduling.patients import PatientGen
from scheduling.calendar import Period, MachineCalendar
from scheduling.machine_pool import MachinePool


class Scheduler:
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

        for patient in self.patient_generator.get_patient():
            self.process_patient(patient)

    def allocate_segment(self, period, cancer, days):
        for shift in range(self.period_length_days - days):
            if period.can_allocate(days, cancer.treatment_time_minutes(), shift):
                period.allocate(days, cancer.treatment_time_minutes(), shift)
                return True
        else:
            return False

    def process_patient(self, patient):
        days = patient.assign_fraction_time()  # length of the sliding window
        cancer = patient.cancer

        machine = self.machine_pool.select_machine(cancer)
        period = self.calendar[machine]

        allocated = False
        machines_to_deallocate = []

        while not allocated:
            allocated = self.allocate_segment(period, cancer, days)
            if not allocated:
                try:
                    machine.allocate(cancer)
                    machines_to_deallocate.append(machine)
                    machine = self.machine_pool.select_machine(cancer)
                except StopIteration:
                    print("We need to extend schedule!")
                    raise Exception("We need to extend schedule!")

        for machine_to_deallocate in machines_to_deallocate:
            machine_to_deallocate.deallocate()
