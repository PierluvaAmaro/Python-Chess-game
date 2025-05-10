from Core.Coordinata import Coordinata
from Pezzi.Pezzo import Pezzo


class Pedone(Pezzo):
    """Classe che rappresenta il pezzo base degli scacchi: il Pedone."""

    def __init__(self, simbolo: str, coord: Coordinata, colore: bool = True):
        super().__init__(simbolo, coord, colore)

    def check_move(self, final: Coordinata) -> bool:
        if final is None:
            raise ValueError("Coordinata non valida.")
        if self.init.x == final.x and self.init.y == final.y:
            raise ValueError("Coordinata non valida.")

        dx = final.x - self.init.x
        dy = final.y - self.init.y

        # Il pedone può muoversi solo in verticale (dx deve essere 0)
        if dx != 0:
            return False

        # Il pedone si sposta di una casella in avanti
        if dy == 1 or dy == -1:
            self.primo = False
            return True

        # Il pedone può spostarsi di due caselle solo al primo movimento
        if dy == 2 or dy == -2 and self.primo:
            self.primo = False
            return True

        return False
