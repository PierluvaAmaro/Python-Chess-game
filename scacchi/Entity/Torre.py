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

    def is_path_clear(self, final: Coordinata, scacchiera) -> bool:
        """Verifica se il percorso verso la coordinata finale è libero.

        Args:
            final (Coordinata): Coordinata finale della Torre verso cui si deve muovere
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.

        Returns:
            bool: True se il percorso è libero, False altrimenti.
        
        """
        dx = final.x - self.init.x
        dy = final.y - self.init.y
        
        x_step = (dx > 0) - (dx < 0)
        y_step = (dy > 0) - (dy < 0)
        
        x, y = self.init.x + x_step, self.init.y + y_step

        while x != final.x or y!= final.y:
            coord = Coordinata(x, y)
            if (scacchiera.is_occupied_by_alliance(self, coord) 
                or scacchiera.is_occupied_by_enemy(self, coord)):
                return False
            x += x_step
            y += y_step
        return True
       
    def check_move(self, final: Coordinata, scacchiera) -> bool:
        """Verifica se la mossa verso la coordinata specificata è valida per la Torre.
        
        Args:
            final (Coordinata): Coordinata finale della Torre verso cui si deve muovere
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.

        Raise:
            ValueError: Se la coordinata finale non è valida o il percorso è occupato.

        """
        if final is None:
            raise ValueError("Coordinata non valida.")

        dx = abs(final.x - self.init.x)
        dy = abs(final.y - self.init.y)

        if (dy == 0) != (dx == 0):
            if not self.is_path_clear(final, scacchiera):
                return False
            self.primo = False
            return True
        else:
            return False 