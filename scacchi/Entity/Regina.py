from .Coordinata import Coordinata
from .Pezzo import Pezzo


class Regina(Pezzo):
    """CLASSE ENTITY."""
    
    """Rappresenta la Regina, uno dei pezzi fondamentali negli scacchi."""

    def __init__(self, simbolo: str, coord: Coordinata, colore: bool):
        """Crea una Regina derivante dalla classe Pezzo.
        
        Args:
            simbolo (str): Simbolo da mostrare per il Regina.
            coord: (Coordinata): Posizione iniziale del Regina sulla scacchiera.
            colore (bool): Colore del pedReginaone (True = bianco, False = nero)

        """
        super().__init__(simbolo, coord, colore)

    def check_move(self, final: Coordinata) -> bool:
        """Verifica se la mossa verso la coordinata specificata è valida per la Regina.
        
        Args:
            final (Coordinata): Coordinata finale della Regina verso cui si deve muovere

        """
        pass