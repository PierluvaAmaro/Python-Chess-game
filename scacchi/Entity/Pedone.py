from Entity.Coordinata import Coordinata
from Entity.Pezzo import Pezzo


class Pedone(Pezzo):
    """Rappresenta il pedone, uno dei pezzi fondamentali negli scacchi."""

    def __init__(self, simbolo: str, coord: Coordinata, colore: bool):
        """Inizializza un nuovo pedone.
        
        Args:
            simbolo (str): Simbolo da mostrare per il pedone.
            coord: (Coordinata): Posizione iniziale del pedone sulla scacchiera.
            colore (bool): Colore del pedone (True = bianco, False = nero)

        """
        super().__init__(simbolo, coord, colore)

    def check_move(self, final: Coordinata) -> bool:
        """Verifica se la mossa verso la coordinata specificata e' valida per il pedone.
        
        Args:
            final (Coordinata): Coordinata di destinazione.

        Returns:
            bool: True se la mossa e' valida, False altrimenti.

        Raises:
            ValueError: Se la coordinata finale e' nulla.
        
        """
        if final is None:
            raise ValueError("Coordinata non valida.")
        if self.init.x == final.x and self.init.y == final.y:
            print("La coordinata finale deve essere diversa da quella di partenza.")
            return False

        dx = final.x - self.init.x
        dy = final.y - self.init.y

        
        # Il pedone può muoversi solo in verticale (dx deve essere 0)
        if dx != 0:
            return False
        
        direzione = 1 if self.colore else -1  # Bianco: su, Nero: giù

        # Il pedone si sposta di una casella in avanti
        if dy == direzione:
            self.primo = False
            return True

        # Il pedone può spostarsi di due caselle solo al primo movimento
        if dy == 2 * direzione and self.primo:
            self.primo = False
            return True

        return False
