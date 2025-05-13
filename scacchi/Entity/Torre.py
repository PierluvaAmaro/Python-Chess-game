from .Coordinata import Coordinata
from .Pezzo import Pezzo


class Torre(Pezzo):
    """CLASSE ENTITY."""
    
    """Rappresenta la Torre, uno dei pezzi fondamentali negli scacchi."""

    def __init__(self, simbolo: str, coord: Coordinata, colore: bool):
        """Crea una Torre derivante dalla classe Pezzo.
        
        Args:
            simbolo (str): simbolo che rappresenta la torre sulla scacchiera.
            coord (Coordinata): coordinata iniziale del pezzo sulla scacchiera.
            colore (bool): Colore della Torre (True = bianco, False = nero)
        
        """
        super().__init__(simbolo, coord, colore)

    
    def check_move(self, final: Coordinata) -> bool:
        """Verifica se la mossa verso la coordinata specificata è valida per la Torre.
        
        Args:
            final (Coordinata): Coordinata finale della Torre verso cui si deve muovere 

        """
        pass