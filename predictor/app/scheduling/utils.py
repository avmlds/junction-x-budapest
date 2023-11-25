from scheduling.calendar import MachineCalendar
from scheduling.machine_pool import MachinePool
from scheduling.machines import TB2Machine, VB2Machine, VB1Machine, TB1Machine, UMachine

_CACHE = {}


def get_machine_pool():
    if not _CACHE.get("pool"):
        _CACHE["pool"] = MachinePool(
            "MachinePool",
            [
                MachinePool("TBPool", [TB1Machine(), TB2Machine()]),
                MachinePool("VBPool", [VB1Machine(), VB2Machine()]),
                MachinePool("UPool", [UMachine()]),
            ],
        )
    return _CACHE["pool"]


def get_machine_calendar(machine_pool, period_length_days) -> MachineCalendar:
    if not _CACHE.get("machine_calendar"):
        _CACHE["machine_calendar"] = MachineCalendar(machine_pool, period_length_days)
    return _CACHE["machine_calendar"]
