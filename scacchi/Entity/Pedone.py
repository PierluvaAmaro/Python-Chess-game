from .Coordinata import Coordinata
from .Pezzo import Pezzo


class Pedone(Pezzo):
    """CLASSE ENTITY."""
    
    """Rappresenta il pedone, uno dei pezzi fondamentali negli scacchi."""

    def __init__(self, simbolo: str, coord: Coordinata, colore: bool):
        """Crea un pedone derivante dall classe pezzo.
        
        Args:
            simbolo (str): Simbolo da mostrare per il pedone.
            coord: (Coordinata): Posizione iniziale del pedone sulla scacchiera.
            colore (bool): Colore del Pedone (True = bianco, False = nero)

        """
        super().__init__(simbolo, coord, colore)
        self.en_passant = False

    def percorso_libero(self, finale, scacchiera):
        """Verifica se il percorso verso la coordinata finale è libero.

        Args:
            finale (Coordinata): Coordinata verso cui il pedone si deve muovere.
            scacchiera: Scacchiera su cui verificare le posizioni dei pezzi.

        Returns:
            bool: True se il percorso è libero, False altrimenti.
        
        """
        if (self.primo and self.iniziale.x == finale.x 
            and abs(self.iniziale.y - finale.y) == 2):
            dir = 1 if self.colore else -1
            y = self.iniziale.y + dir
            
            middle = Coordinata(self.iniziale.x, y)
            
            return not (scacchiera.occupata(middle) or scacchiera.occupata(finale))

        elif self.iniziale.x == finale.x and abs(self.iniziale.y - finale.y) == 1:
            return not scacchiera.occupata(finale)
        return True

    def controlla_mossa(
        self,
        finale: Coordinata,
        scacchiera=None,
        en_passant=False
    ) -> bool:
        # ...existing code...
        dx = finale.x - self.iniziale.x
        dy = finale.y - self.iniziale.y
        direzione = 1 if self.colore else -1  # Bianco: su, Nero: giù

        # Movimento in avanti di una casella
        if dx == 0 and dy == direzione and not scacchiera.occupata(finale):
            self.en_passant = False
            return True

        # Movimento in avanti di due caselle solo al primo movimento
        if dx == 0 and dy == 2 * direzione and self.primo:
            middle = Coordinata(self.iniziale.x, self.iniziale.y + direzione)
            if not scacchiera.occupata(middle) and not scacchiera.occupata(finale):
                self.en_passant = True
                return True
            

        # Cattura in diagonale normale
        if abs(dx) == 1 and dy == direzione and scacchiera.occupata_da_nemico(
            self, finale
            ):
            return True

        # --- EN PASSANT ---
        # Verifica se la cattura en passant è possibile
        if abs(dx) == 1 and dy == direzione and not scacchiera.occupata(finale):
            # La casa finale è vuota, ma potrebbe essere en passant
            pedone_vicino = scacchiera.pezzi_vivi.get(
                Coordinata(finale.x, self.iniziale.y)
            )

            if (
                pedone_vicino is not None
                and pedone_vicino.simbolo in ("♙", "♟")
                and pedone_vicino.colore != self.colore
                and getattr(pedone_vicino, "en_passant", False)
            ):
                return True

        return False