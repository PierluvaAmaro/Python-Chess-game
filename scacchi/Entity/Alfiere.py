from .Coordinata import Coordinata
from .Pezzo import Pezzo


class Alfiere(Pezzo):
    """Rappresenta l'alfiere, uno dei pezzi fondamentali negli scacchi."""

    def __init__(self, simbolo: str, coord: Coordinata, colore: bool):
        """Crea un Alfiere derivante dalla classe Pezzo.
        
        Args:
            simbolo (str): simbolo che rappresenta l'alfiere sulla scacchiera.
            coord (Coordinata): coordinata iniziale del pezoz sulla scacchiera.
            colore (bool): Colore dell'Alfiere (True = bianco, False = nero)
        
        """
        super().__init__(simbolo, coord, colore)

    def check_move(self, final: Coordinata) -> bool:
        """Verifica se la mossa verso la coordinata specificata è valida per l'Alfiere.
        
        Args:
            final (Coordinata): Coordinata finale dell'Alfiere verso cui si deve muovere

        """
        pass