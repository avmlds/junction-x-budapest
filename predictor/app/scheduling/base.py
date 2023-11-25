from typing import Set, Generator, Any

from scheduling.diseases import Cancer


class AllocatableEntity:
    def name(self):
        raise NotImplementedError

    def allocate(self, cancer: Cancer):
        raise NotImplementedError

    def deallocate(self):
        raise NotImplementedError

    @property
    def total_quantity(self):
        raise NotImplementedError

    @property
    def is_allocated(self) -> bool:
        raise NotImplementedError

    @property
    def available_treatments(self) -> Set[str]:
        raise NotImplementedError

    def get_all_machines(self):
        raise NotImplementedError

    def machine_gen(self, cancer: Cancer) -> Any:
        raise NotImplementedError
