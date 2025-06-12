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

    def percorso_libero(self, finale: Coordinata, scacchiera) -> bool:
        return True

    def controlla_mossa(self, finale: Coordinata, scacchiera=None) -> bool:
        """Verifica se la mossa verso la coordinata specificata è valida per il Re.

        Args:
            finale (Coordinata): Coordinata finale del Re verso cui si deve muovere.
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.

        """
        if finale is None:
            raise ValueError("Coordinata non valida")
        
        dx = abs(finale.x - self.iniziale.x)
        dy = abs(finale.y - self.iniziale.y)
        
        if dx <= 1 and dy <= 1 and (dx != 0 or dy != 0):
            self.primo = False
            return True
        else:
            return False
        
    