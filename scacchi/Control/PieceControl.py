from Entity.Coordinata import Coordinata
from Entity.Pezzo import Pezzo
from Entity.Scacchiera import Scacchiera


class PieceControl:
    """."""

    def __init__(self, scacchiera: Scacchiera):
        self.scacchiera = scacchiera
      
    def find_piece(self, final: Coordinata, colore: bool) -> Pezzo:
        """Trova il pezzo del colore specificato che puo' muoversi alla coordinata.
        
        Args:
            final (Coordinata): Coordinata di destinazione del pezzo.
            colore (bool): Colore del pezzo da cercare.

        Returns:
            Pezzo: Il primo pezzo valido che puo' effettuare la mossa, se trovato.
        
        """
        for _, piece in self.scacchiera.pezzi_vivi.items():
            if piece is not None and piece.colore == colore and piece.check_move(final):
                return piece
        
        print("Nessun tuo pezzo puo' effettuare quella mossa.")
        return None

    def muovi(self, pezzo: Pezzo, final: Coordinata) -> bool:
        """Esegue lo spostamento di un pezzo se la destinazione non e' occupata.
        
        Args:
            pezzo (Pezzo): Il pezzo da muovere.
            final (Coordinata): La destinazione del pezzo.

        Returns:
            bool: True se la mossa e' stata effettuata con successo, False altrimenti.
        
        """
        if not self.scacchiera.is_occupied(final):
            self.scacchiera.pezzi_vivi.pop(pezzo.init)
            pezzo.init = final
            self.scacchiera.pezzi_vivi[final] = pezzo
            return True
        
        return False