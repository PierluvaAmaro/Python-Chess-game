from Core.Coordinata import Coordinata
from Pezzi.Pezzo import Pezzo


class Pedone(Pezzo):
    """Classe che rappresenta il pezzo base degli scacchi: il Pedone."""
    
    def __init__(self, simbolo: str, coord: Coordinata, turno: int = 1):
        super().__init__(simbolo, coord, turno)

    def check_move(self, final: Coordinata) -> bool:
        if final is None:
            raise ValueError("Coordinata non valida.")
        if self.id.x == final.x and self.id.y == final.y:
            raise ValueError("Coordinata non valida.")

        dx = final.x - self.id.x
        dy = final.y - self.id.y

        print(f"{final.y} - {self.id.y} = ?")

        # Il pedone può muoversi solo in verticale (dx deve essere 0)
        if dx != 0:
            return False
        
        # Il pedone si sposta di una casella in avanti
        if dy == 1:
            self.primo = False
            return True
        
        # Il pedone può spostarsi di due caselle solo al primo movimento
        if dy == 2 and self.primo:
            self.primo = False
            return True

        return False