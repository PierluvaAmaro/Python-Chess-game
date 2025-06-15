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

    def percorso_libero(self, finale: Coordinata, scacchiera) -> bool:
        """Verifica se il percorso verso la coordinata finale è libero.

        Args:
            finale (Coordinata): Coordinata finale della Torre verso cui si deve muovere
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.

        Returns:
            bool: True se il percorso è libero, False altrimenti.
        
        """
        dx = finale.x - self.iniziale.x
        dy = finale.y - self.iniziale.y
        
        x_step = (dx > 0) - (dx < 0)
        y_step = (dy > 0) - (dy < 0)
        
        x, y = self.iniziale.x + x_step, self.iniziale.y + y_step
        lista = []
        while x != finale.x or y!= finale.y:
            coord = Coordinata(x, y)
            if (scacchiera.occupata(coord)):
                return False
            x += x_step
            y += y_step
            
            lista.append(coord)
        return True, lista
       
    def controlla_mossa(self, finale: Coordinata, scacchiera) -> bool:
        """Verifica se la mossa verso la coordinata specificata è valida per la Torre.
        
        Args:
            finale (Coordinata): Coordinata finale della Torre verso cui si deve muovere
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.

        Raise:
            ValueError: Se la coordinata finale non è valida o il percorso è occupato.

        """
        if finale is None:
            raise ValueError("Coordinata non valida.")

        dx = abs(finale.x - self.iniziale.x)
        dy = abs(finale.y - self.iniziale.y)

        if (dy == 0) != (dx == 0):
            return self.percorso_libero(finale, scacchiera)

        else:
            return False
        
    def mosse_possibili(self, scacchiera):
        return super().mosse_possibili(scacchiera)