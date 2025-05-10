from abc import ABC, abstractmethod

from Core.Coordinata import Coordinata


class Pezzo(ABC):
    """Classe astratta che rappresenta un pezzo degli scacchi generico."""

    def __init__(self, simbolo: str, init: Coordinata, colore: bool):
        self.init = init
        self.primo = True
        self.simbolo = simbolo
        self.colore = colore

    @abstractmethod
    def check_move(self, final: Coordinata) -> bool:
        pass

    def print(self):
        print(f"Coordinata: {self.init.x}, {self.init.y}\nmovimento: {self.primo}\n"
              f"simbolo: {self.simbolo}\ncolore: {self.colore}\n\n"
            )
    