from .Coordinata import Coordinata
from .Pezzo import Pezzo


class Cavallo(Pezzo):
    """CLASSE ENTITY."""
    
    """Rappresenta il Cavallo, uno dei pezzi fondamentali negli scacchi."""

    def __init__(self, simbolo: str, coord: Coordinata, colore: bool):
        """Crea un Cavallo derivante dalla classe Pezzo.
        
        Args:
            simbolo (str): simbolo che rappresenta il Cavallo sulla scacchiera.
            coord (Coordinata): coordinata iniziale del pezzo sulla scacchiera.
            colore (bool): Colore del Cavallo (True = bianco, False = nero)
        
        """
        super().__init__(simbolo, coord, colore)

    
    def check_move(self, final: Coordinata, scacchiera=None) -> bool:
        """Verifica se la mossa verso la coordinata specificata è valida per il Cavallo.
        
        Arg:
            final (Coordinata): Coordinata finale del Cavallo verso cui si deve muovere.
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.
            
        Raise: 
            ValueError se la coordinata finale non e' valida.
        """
        if final is None:
            raise ValueError("Coordinata non valida.")
        
        print(f"X: {self.init.x} - {final.x}")
        print(f"Y: {self.init.y} - {final.y}")
        
        dx = abs(final.x - self.init.x)
        dy = abs(final.y - self.init.y)
        
        if (dx == 2 and dy == 1) or (dx == 1 and dy == 2):
            self.primo = False
            
            return True
        else:
            return False