from abc import ABC, abstractmethod

from Core.Coordinata import Coordinata


class Pezzo(ABC):
    """CLasse astratta che rappresenta un pezzo degli scacchi generico."""

    def __init__(self, simbolo: str, id: Coordinata, turno: int):
        self.id = id
        self.primo = True
        self.simbolo = simbolo
        self.turno = turno

    @abstractmethod
    def check_move(self, final: Coordinata) -> bool:
        pass