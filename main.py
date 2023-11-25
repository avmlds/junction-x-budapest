from scheduling.machine_pool import MachinePool
from scheduling.machines import TB1Machine, TB2Machine, VB1Machine, VB2Machine, UMachine
from scheduling.patients import PatientGen
from scheduling.scheduler import Scheduler

if __name__ == "__main__":

    t_pool = MachinePool("TBPool", [TB1Machine(), TB2Machine()])
    v_pool_v1 = MachinePool("VBPool", [VB1Machine(), VB2Machine()])
    u_pool = MachinePool("UPool", [UMachine()])

    super_pool = MachinePool(
        "super",
        [
            t_pool,
            v_pool_v1,
            u_pool,
        ],
    )

    patient_flow = PatientGen()

    scheduler = Scheduler(
        period_length_days=50,
        machine_pool=super_pool,
        patient_generator=patient_flow,
    )
    scheduler.schedule()
