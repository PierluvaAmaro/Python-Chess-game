from .Coordinata import Coordinata
from .Pezzo import Pezzo


class Regina(Pezzo):
    """CLASSE ENTITY."""
    
    """Rappresenta la Regina, uno dei pezzi fondamentali negli scacchi."""

    def __init__(self, simbolo: str, coord: Coordinata, colore: bool):
        """Crea una Regina derivante dalla classe Pezzo.
        
        Args:
            simbolo (str): Simbolo da mostrare per il Regina.
            coord (Coordinata): Posizione iniziale del Regina sulla scacchiera.
            colore (bool): Colore della Regina (True = bianco, False = nero)

        """
        super().__init__(simbolo, coord, colore)

    def percorso_libero(self, final: Coordinata, scacchiera) -> bool:
        """Verifica se il percorso verso la coordinata finale è libero.

        Args:
            final (Coordinata): Coordinata finale della Regina verso cui si deve muovere
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.

        Returns:
            bool: True se il percorso è libero, False altrimenti.

        """
        dx = final.x - self.iniziale.x
        dy = final.y - self.iniziale.y

        if dx == 0 and dy != 0:
            y_step = 1 if dy > 0 else -1
            for y in range(self.iniziale.y + y_step, final.y, y_step):
                coord = Coordinata(self.iniziale.x, y)
                if (
                    scacchiera.occupata_da_alleato(self, coord) 
                    or scacchiera.occupata_da_nemico(self, coord)
                ):
                    return False
            return True

        elif dy == 0 and dx != 0:
            x_step = 1 if dx > 0 else -1
            for x in range(self.iniziale.x + x_step, final.x, x_step):
                coord = Coordinata(x, self.iniziale.y)
                if (
                    scacchiera.occupata_da_alleato(self, coord) 
                    or scacchiera.occupata_da_nemico(self, coord)
                ):
                    return False
            return True

        elif abs(dx) == abs(dy) and dx != 0:
            x_step = 1 if dx > 0 else -1
            y_step = 1 if dy > 0 else -1
            x, y = self.iniziale.x + x_step, self.iniziale.y + y_step
            while x != final.x and y != final.y:
                coord = Coordinata(x, y)
                if (
                    scacchiera.occupata_da_alleato(self, coord) 
                    or scacchiera.occupata_da_nemico(self, coord)
                ):
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

        movimento_valido = (
            (dx == dy and dx != 0)
            or (dx == 0 and dy != 0)
            or (dy == 0 and dx != 0)
        )

        if not movimento_valido:
            return False

        if not self.percorso_libero(finale, scacchiera):
            return False

        return not scacchiera.occupata_da_alleato(self, finale) 

    def mosse_possibili(self, scacchiera):
        return super().mosse_possibili(scacchiera)