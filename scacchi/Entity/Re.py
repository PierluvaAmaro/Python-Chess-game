from .Coordinata import Coordinata
from .Pezzo import Pezzo


class Re(Pezzo):
    """CLASSE ENTITY."""
    
    """Rappresenta il Re, uno dei pezzi fondamentali negli scacchi."""

    def __init__(self, simbolo: str, coord: Coordinata, colore: bool):
        """Crea un Re derivante dalla classe Pezzo.
        
        Args:
            simbolo (str): Simbolo da mostrare per il Re.
            coord: (Coordinata): Posizione iniziale del Re sulla scacchiera.
            colore (bool): Colore del Re (True = bianco, False = nero)

        """
        super().__init__(simbolo, coord, colore)
        self.arrocco = False

    def check_move(self, final: Coordinata, scacchiera=None) -> bool:
        """Verifica se la mossa verso la coordinata specificata è valida per il Re.

        Args:
            final (Coordinata): Coordinata finale del Re verso cui si deve muovere.
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.

        """
        if final is None:
            raise ValueError("Coordinata non valida")
        
        dx = abs(final.x - self.init.x)
        dy = abs(final.y - self.init.y)
        
        if dx <= 1 and dy <= 1 and (dx != 0 or dy != 0):
            self.primo = False
            return True
        else:
            return False