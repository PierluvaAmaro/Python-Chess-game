from .Coordinata import Coordinata
from .Pezzo import Pezzo


class Alfiere(Pezzo):
    """CLASSE ENTITY."""
    
    """Rappresenta l'alfiere, uno dei pezzi fondamentali negli scacchi."""

    def __init__(self, simbolo: str, coord: Coordinata, colore: bool):
        """Crea un Alfiere derivante dalla classe Pezzo.
        
        Args:
            simbolo (str): simbolo che rappresenta l'alfiere sulla scacchiera.
            coord (Coordinata): coordinata iniziale del pezoz sulla scacchiera.
            colore (bool): Colore dell'Alfiere (True = bianco, False = nero)
        
        """
        super().__init__(simbolo, coord, colore)

    def percorso_libero(self, finale: Coordinata, scacchiera) -> bool:
        """Verifica se il percorso verso la coordinata finale è libero.

        Args:
            finale (Coordinata): Coordinata verso cui l'Alfiere si deve muovere.
            scacchiera: Scacchiera su cui verificare le posizioni dei pezzi.

        Returns:
            bool: True se il percorso è libero, False altrimenti.
        
        """
        x_step = 1 if finale.x > self.iniziale.x else -1
        y_step = 1 if finale.y > self.iniziale.y else -1
        
        x = self.iniziale.x + x_step
        y = self.iniziale.y + y_step

        while x != finale.x and y != finale.y:
            coord = Coordinata(x, y)
            if scacchiera.occupata(coord):
                return False
            
            x += x_step
            y += y_step
        return True

    def controlla_mossa(self, finale: Coordinata, scacchiera=None) -> bool:
        """Verifica se la mossa verso la coordinata specificata è valida per l'Alfiere.
        
        Args:
            finale (Coordinata): Coordinata finale dell'Alfiere verso cui deve muoversi.
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.

        Raise:
            ValueError: Se la coordinata finale non è valida o il percorso è occupato.

        """
        if finale is None:
            raise ValueError("Coordinata non valida.")
        
        dx = abs(finale.x - self.iniziale.x)
        dy = abs(finale.y - self.iniziale.y)

        if dx == dy and dx != 0:
            return self.percorso_libero(finale, scacchiera)
        else:
            return False 
        
    def mosse_possibili(self, scacchiera):
        return super().mosse_possibili(scacchiera)