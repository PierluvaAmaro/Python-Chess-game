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

    def percorso_libero(self, finale: Coordinata, scacchiera) -> bool:
        return True
    
    def controlla_mossa(self, finale: Coordinata, scacchiera=None) -> bool:
        """Verifica se la mossa verso la coordinata specificata è valida per il Cavallo.
        
        Arg:
            finale (Coordinata): Coordinata finale del Cavallo verso cui deve muoversi.
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.
            
        Raise: 
            ValueError se la coordinata finale non e' valida.
        """
        if finale is None:
            raise ValueError("Coordinata non valida")
        
        dx = abs(finale.x - self.iniziale.x)
        dy = abs(finale.y - self.iniziale.y)
        
        if (dx == 2 and dy == 1) or (dx == 1 and dy == 2):
            return not (
                scacchiera is not None and scacchiera.occupata_da_alleato(self, finale)
            )
        return False
    
    def mosse_possibili(self, scacchiera):
        return super().mosse_possibili(scacchiera)