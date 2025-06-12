from .Coordinata import Coordinata
from .Pezzo import Pezzo


class Pedone(Pezzo):
    """CLASSE ENTITY."""
    
    """Rappresenta il pedone, uno dei pezzi fondamentali negli scacchi."""

    def __init__(self, simbolo: str, coord: Coordinata, colore: bool):
        """Inizializza un nuovo pedone.
        
        Args:
            simbolo (str): Simbolo da mostrare per il pedone.
            coord: (Coordinata): Posizione iniziale del pedone sulla scacchiera.
            colore (bool): Colore del Pedone (True = bianco, False = nero)

        """
        super().__init__(simbolo, coord, colore)

    def percorso_libero(self, finale, scacchiera):
        if (self.primo and self.iniziale.x == finale.x 
            and abs(self.iniziale.y - finale.y) == 2):
            dir = 1 if self.colore else -1
            y = self.iniziale.y + dir
            
            middle = Coordinata(self.iniziale.x, y)
            
            return not (scacchiera.occupata(middle) or scacchiera.occupata(finale))

        elif self.iniziale.x == finale.x and abs(self.iniziale.y - finale.y) == 1:
            return not scacchiera.occupata(finale)
        return True

    def controlla_mossa(self, finale: Coordinata, scacchiera=None) -> bool:
        """Verifica se la mossa verso la coordinata specificata è valida per il pedone.
        
        Args:
            finale (Coordinata): Coordinata finale del Pedone verso cui si deve muovere
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.

        """
        if finale is None:
            raise ValueError("Coordinata non valida.")
        
        if self.iniziale.x == finale.x and self.iniziale.y == finale.y:
            return False

        dx = finale.x - self.iniziale.x
        dy = finale.y - self.iniziale.y

        # Il pedone può muoversi solo in verticale (dx deve essere 0)
        if dx != 0:
            return False

        direzione = 1 if self.colore else -1  # Bianco: su, Nero: giù

        # Il pedone si sposta di una casella in avanti
        if dy == direzione:
            return True

        # Il pedone può spostarsi di due caselle solo al primo movimento
        if dy == 2 * direzione and self.primo:
            return True

        if (not self.colore and dy < 0):
            return False

        return False
    
    