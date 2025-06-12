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

    def is_path_clear(self, final: Coordinata, scacchiera) -> bool:
        """Verifica se il percorso verso la coordinata finale è libero.

        Args:
            final (Coordinata): Coordinata finale della Regina verso cui si deve muovere
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.

        Returns:
            bool: True se il percorso è libero, False altrimenti.
        """
        dx = final.x - self.init.x
        dy = final.y - self.init.y

        if dx == 0 and dy != 0:  # Movimento verticale
            y_step = 1 if dy > 0 else -1
            for y in range(self.init.y + y_step, final.y, y_step):
                coord = Coordinata(self.init.x, y)
                if scacchiera.is_occupied_by_alliance(self, coord) or scacchiera.is_occupied_by_enemy(self, coord):
                    return False
            return True
        elif dy == 0 and dx != 0:  # Movimento orizzontale
            x_step = 1 if dx > 0 else -1
            for x in range(self.init.x + x_step, final.x, x_step):
                coord = Coordinata(x, self.init.y)
                if scacchiera.is_occupied_by_alliance(self, coord) or scacchiera.is_occupied_by_enemy(self, coord):
                    return False
            return True
        elif abs(dx) == abs(dy) and dx != 0:  # Movimento diagonale
            x_step = 1 if dx > 0 else -1
            y_step = 1 if dy > 0 else -1
            x, y = self.init.x + x_step, self.init.y + y_step
            while x != final.x and y != final.y:
                coord = Coordinata(x, y)
                if scacchiera.is_occupied_by_alliance(self, coord) or scacchiera.is_occupied_by_enemy(self, coord):
                    return False
                x += x_step
                y += y_step
            return True
        else:
            return False

    def check_move(self, final: Coordinata, scacchiera) -> bool:
        """Verifica se la mossa verso la coordinata specificata è valida per la Regina.
        
        Args:
            final (Coordinata): Coordinata finale della Regina verso cui si deve muovere
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.

        Raise:
            ValueError: Se la coordinata finale non è valida o il percorso è occupato.

        """
        if final is None:
            raise ValueError("Coordinata non valida.")
        
        dx = abs(final.x - self.init.x)
        dy = abs(final.y - self.init.y)

        # Movimento diagonale, orizzontale o verticale
        if (dx == dy and dx != 0) or (dx == 0 and dy != 0) or (dy == 0 and dx != 0):
            if not self.is_path_clear(final, scacchiera):
                return False
            if scacchiera.is_occupied_by_alliance(self, final):
                return False
            self.primo = False
            return True
        else:
            return False
