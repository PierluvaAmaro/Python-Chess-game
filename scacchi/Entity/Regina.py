from .Coordinata import Coordinata
from .Pezzo import Pezzo


class Regina(Pezzo):
    """CLASSE ENTITY."""
    
    """Rappresenta la regina, il pezzo più potente negli scacchi."""

    def __init__(self, simbolo: str, coord: Coordinata, colore: bool):
        """Crea una Regina derivante dalla classe Pezzo.
        
        Args:
            simbolo (str): simbolo che rappresenta la regina sulla scacchiera.
            coord (Coordinata): coordinata iniziale del pezzo sulla scacchiera.
            colore (bool): Colore della Regina (True = bianco, False = nero)

        """
        super().__init__(simbolo, coord, colore)


    def percorso_libero(self, finale: Coordinata, scacchiera) -> bool:
        """Verifica se il percorso verso la coordinata finale è libero.

        Args:
            final (Coordinata): Coordinata finale della Regina verso cui si deve muovere
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.

        Returns:
            bool: True se il percorso è libero, False altrimenti.
            
        """
        dx = finale.x - self.iniziale.x
        dy = finale.y - self.iniziale.y

        if dx == 0:  # Movimento verticale
            y_step = 1 if dy > 0 else -1
            for y in range(self.iniziale.y + y_step, finale.y, y_step):
                coord = Coordinata(self.iniziale.x, y)
                if scacchiera.occupata(coord):
                    return False
            return True
        elif dy == 0:  # Movimento orizzontale
            x_step = 1 if dx > 0 else -1
            for x in range(self.iniziale.x + x_step, finale.x, x_step):
                coord = Coordinata(x, self.iniziale.y)
                if scacchiera.occupata(coord):
                    return False
            return True
        elif abs(dx) == abs(dy):  # Movimento diagonale
            x_step = 1 if dx > 0 else -1
            y_step = 1 if dy > 0 else -1
            x = self.iniziale.x + x_step
            y = self.iniziale.y + y_step
            while x != finale.x and y != finale.y:
                coord = Coordinata(x, y)
                if scacchiera.occupata(coord):
                    return False
                x += x_step
                y += y_step
            return True
        else:
            return False

    def controlla_mossa(self, finale: Coordinata, scacchiera=None) -> bool:

        """Verifica se la mossa verso la coordinata specificata è valida per la donna.
        
        Args:
            finale (Coordinata): Coordinata finale della donna verso cui deve muoversi.
            scacchiera: Scacchiera per verificare le posizioni dei pezzi (opzionale).
            
        Raise:
            ValueError: Se la coordinata finale non è valida o il percorso è occupato.

        """
        if finale is None:
            raise ValueError("Coordinata non valida.")
        
        dx = abs(finale.x - self.iniziale.x)
        dy = abs(finale.y - self.iniziale.y)

        # Movimento diagonale, orizzontale o verticale
        movimento_valido = (
            (dx == dy and dx != 0)  # Diagonale
            or (dx == 0 and dy != 0)  # Verticale
            or (dy == 0 and dx != 0)  # Orizzontale
        )

        if not movimento_valido:
            return False

        if not self.percorso_libero(finale, scacchiera):
            return False

        return not scacchiera.occupata_da_alleato(self, finale) 

    def mosse_possibili(self, scacchiera):
        return super().mosse_possibili(scacchiera)