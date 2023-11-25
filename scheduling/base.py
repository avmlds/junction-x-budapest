from typing import Set, Generator, Any


class AllocatableEntity:

    def name(self):
        raise NotImplementedError

    def allocate(self, cancer_type: str):
        raise NotImplementedError

    def deallocate(self):
        raise NotImplementedError

    @property
    def is_allocated(self) -> bool:
        raise NotImplementedError

    @property
    def available_treatments(self) -> Set[str]:
        raise NotImplementedError

    def machine_gen(self, cancer_type: str) -> Generator["AllocatableEntity", Any, None]:
        raise NotImplementedError
