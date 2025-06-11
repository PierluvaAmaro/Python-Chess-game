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

    def is_path_clear(self, final: Coordinata, scacchiera) -> bool:
        """Verifica se il percorso verso la coordinata finale è libero.

        Args:
            final (Coordinata): Coordinata finale dell'Alfiere verso cui si deve muovere
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.

        Returns:
            bool: True se il percorso è libero, False altrimenti.
        
        """
        x_step = 1 if final.x > self.init.x else -1
        y_step = 1 if final.y > self.init.y else -1
        x, y = self.init.x + x_step, self.init.y + y_step

        while x != final.x and y != final.y:
            coord = Coordinata(x, y)
            if scacchiera.is_occupied_by_alliance(self, coord) or scacchiera.is_occupied_by_enemy(self, coord):  # noqa: E501
                return False
            x += x_step
            y += y_step
        return True

    def check_move(self, final: Coordinata, scacchiera) -> bool:
        """Verifica se la mossa verso la coordinata specificata è valida per l'Alfiere.
        
        Args:
            final (Coordinata): Coordinata finale dell'Alfiere verso cui si deve muovere
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.

        Raise:
            ValueError: Se la coordinata finale non è valida o il percorso è occupato.

        """
        if final is None:
            raise ValueError("Coordinata non valida.")
        
        dx = abs(final.x - self.init.x)
        dy = abs(final.y - self.init.y)

        if dx == dy and dx != 0:
            if not self.is_path_clear(final, scacchiera):
                return False
            self.primo = False
            return True
        else:
            return False 