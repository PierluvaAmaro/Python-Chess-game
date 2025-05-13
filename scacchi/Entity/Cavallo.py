from .Coordinata import Coordinata
from .Pezzo import Pezzo


class Cavallo(Pezzo):
    """Rappresenta il Cavallo, uno dei pezzi fondamentali negli scacchi."""

    def __init__(self, simbolo: str, coord: Coordinata, colore: bool):
        """Crea un Cavallo derivante dalla classe Pezzo.
        
        Args:
            simbolo (str): simbolo che rappresenta il Cavallo sulla scacchiera.
            coord (Coordinata): coordinata iniziale del pezzo sulla scacchiera.
            colore (bool): Colore del Cavallo (True = bianco, False = nero)
        
        """
        super().__init__(simbolo, coord, colore)

    
    def check_move(self, final: Coordinata) -> bool:
        """Verifica se la mossa verso la coordinata specificata è valida per il Cavallo.
        
        Args:
            final (Coordinata): Coordinata finale del Cavallo verso cui si deve muovere.

        """
        pass