from Core.Coordinata import Coordinata
from Pezzi.Pezzo import Pezzo


class Pedone(Pezzo):
    """Classe che definisce il pezzo basico degli scacchi: il pedone."""

    def __init__(self, init: Coordinata, colore: str, id: str):
        """Costruttore che richiama il costruttore della classe madre."""
        super().__init__(init, colore, id, True)
    
    def check_move(self, move: Coordinata) -> bool:
        """Metodo che verifica se la posizione inserita dal giocatore e' corretta."""
        if self.primo and self.init.y + 2 == move.y or self.init.y + 1 == move.y:
            # mossa possibile
            self.init = move
            self.primo = False
            return True

        else:
            # mossa non valida.
            print("Mossa non valida.")
            return False