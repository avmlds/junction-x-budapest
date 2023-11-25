from scheduling.calendar import Period
from scheduling.constants import CANCER_TYPES, CRAINOSPINAL, BREAST_SPECIAL, WHOLE_BRAIN, CRANE, BREAST
from scheduling.machine_pool import MachinePool
from scheduling.machines import TB1Machine, TB2Machine, VB1Machine, VB2Machine, UMachine
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

    scheduler = Scheduler(
        period=Period(5000),
        machine_pool=super_pool,
    )



    for cancer_type in CANCER_TYPES:
        machine = super_pool.select_machine(cancer_type)
        machine.allocate(cancer_type)
        print(machine, machine.is_allocated)
        machine.deallocate()
        print(machine, machine.is_allocated)
