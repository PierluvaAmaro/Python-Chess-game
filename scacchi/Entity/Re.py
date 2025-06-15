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
        """Verifica se il percorso verso la coordinata finale è libero.

        Args:
            finale (Coordinata): Coordinata verso cui il re si deve muovere.
            scacchiera: Scacchiera su cui verificare le posizioni dei pezzi.

        Returns:
            bool: True se il percorso è libero, False altrimenti.
        
        """
        return (not scacchiera.occupata(finale)) or scacchiera.occupata_da_nemico(self, finale)

    def controlla_mossa(self, finale: Coordinata, scacchiera=None) -> bool:
        """Verifica se la mossa verso la coordinata specificata è valida per il re.
        
        Args:
            finale (Coordinata): Coordinata finale del re verso cui deve muoversi.
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.

        Raise:
            ValueError: Se la coordinata finale non è valida o il percorso è occupato.

        """
        if finale is None:
            raise ValueError("Coordinata non valida")
        
        if not self.percorso_libero(finale, scacchiera):
            return False

        dx = abs(finale.x - self.iniziale.x)
        dy = abs(finale.y - self.iniziale.y)
            
        return (dx <= 1 and dy <= 1) and (dx != 0 or dy != 0)
    
    def mosse_possibili(self, scacchiera):
        return super().mosse_possibili(scacchiera)
