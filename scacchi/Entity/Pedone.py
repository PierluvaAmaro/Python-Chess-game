from .Coordinata import Coordinata
from .Pezzo import Pezzo


class Pedone(Pezzo):
    """CLASSE ENTITY."""
    
    """Rappresenta il pedone, uno dei pezzi fondamentali negli scacchi."""

    def __init__(self, simbolo: str, coord: Coordinata, colore: bool):
        """Inizializza un nuovo pedone.
        
        Args:
            simbolo (str): Simbolo da mostrare per il pedone.
            coord: (Coordinata): Posizione iniziale del pedone sulla scacchiera.
            colore (bool): Colore del Pedone (True = bianco, False = nero)

        """
        super().__init__(simbolo, coord, colore)

    def check_move(self, final: Coordinata, scacchiera=None) -> bool:
        """Verifica se la mossa verso la coordinata specificata è valida per il pedone.
        
        Args:
            final (Coordinata): Coordinata finale del Pedone verso cui si deve muovere
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.

        """
        if final is None:
            raise ValueError("Coordinata non valida.")
        
        if self.init.x == final.x and self.init.y == final.y:
            return False

        dx = final.x - self.init.x
        dy = final.y - self.init.y

        # Il pedone può muoversi solo in verticale (dx deve essere 0)
        if dx != 0:
            return False

        direzione = 1 if self.colore else -1  # Bianco: su, Nero: giù

        # Il pedone si sposta di una casella in avanti
        if dy == direzione:
            return True

        # Il pedone può spostarsi di due caselle solo al primo movimento
        if dy == 2 * direzione and self.primo:
            return True

        if (not self.colore and dy < 0):
            return False

        return False
    
    def is_path_clear(self, init, final, scacchiera):
        if self.primo and init.x == final.x and abs(init.y - final.y) == 2:
            dir = 1 if self.colore else -1
            y = init.y + dir
            
            middle = Coordinata(init.x, y)
            middle.print()
            
            return not (scacchiera.is_occupied(middle) or scacchiera.is_occupied(final))

        elif init.x == final.x and abs(init.y - final.y) == 1:
            return not scacchiera.is_occupied(final)
        return True