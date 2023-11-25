from scheduling.calendar import Period
from scheduling.constants import CANCER_TYPES, CRAINOSPINAL, BREAST_SPECIAL, WHOLE_BRAIN, CRANE, BREAST
from scheduling.machine_pool import MachinePool
from scheduling.machines import TB1Machine, TB2Machine, VB1Machine, VB2Machine, UMachine
from scheduling.patients import PatientGen
from scheduling.scheduler import Scheduler

if __name__ == "__main__":

    t_pool = MachinePool("TBPool", [TB1Machine(), TB2Machine()])
    v_pool_v1 = MachinePool("VBPool", [VB1Machine(), VB2Machine()])
    u_pool = MachinePool("UPool", [UMachine()])

    super_pool = MachinePool("super", [
        t_pool,
        v_pool_v1,
        u_pool,
    ])

    patient_flow = PatientGen()

    scheduler = Scheduler(
        period=Period(5000),
        machine_pool=super_pool,
        patient_generator=patient_flow,
    )

    for patient in patient_flow.get_patient():

        days = patient.assign_fraction_time()
        cancer = patient.cancer_type

        machine = super_pool.select_machine(cancer.name())
        machine.allocate(cancer.name())
        print(
            f"Machine {machine.name()} was allocated for {days} days "
            f"to treat patient {patient.name} with {cancer.name()} cancer. "
            f"Treatment time will be {cancer.treatment_time_minutes()} minutes long"
        )
        machine.deallocate()
        print(f"Machine {machine.name()} was deallocated")
