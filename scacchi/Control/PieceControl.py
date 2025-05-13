from ..Entity.Coordinata import Coordinata
from ..Entity.Pezzo import Pezzo
from ..Entity.Scacchiera import Scacchiera


class PieceControl:
    """CLASSE CONTROL."""
    
    """Controlla le operazioni sui pezzi durante il gioco degli scacchi."""

    def __init__(self):
        """Inizializza un oggetto PieceControl."""
        pass

    def find_piece(self, scacchiera: Scacchiera, final: Coordinata, colore: bool
                   ) -> Pezzo:
        """Trova il pezzo del colore specificato che puo' muoversi alla coordinata.
        
        Args:
            scacchiera (Scacchiera): La scacchiera di gioco contenente i pezzi
            final (Coordinata): Coordinata di destinazione del pezzo.
            colore (bool): Colore del pezzo da cercare.

        Returns:
            Pezzo: Il primo pezzo valido che puo' effettuare la mossa, se trovato.
        
        """
        for _, piece in scacchiera.pezzi_vivi.items():
            if piece is not None and piece.colore == colore and piece.check_move(final):
                return piece
        
        print("Nessun tuo pezzo puo' effettuare quella mossa.")
        return None

    def muovi(self, scacchiera: Scacchiera, pezzo: Pezzo, final: Coordinata
              ) -> bool:
        """Esegue lo spostamento di un pezzo se la destinazione non e' occupata.
        
        Args:
            scacchiera (Scacchiera): La scacchiera su cui effettuare il movimento.
            pezzo (Pezzo): Il pezzo da muovere.
            final (Coordinata): La destinazione del pezzo.

        Returns:
            bool: True se la mossa e' stata effettuata con successo, False altrimenti.
        
        """
        if not scacchiera.is_occupied(final):
            scacchiera.pezzi_vivi.pop(pezzo.init)
            pezzo.init = final
            scacchiera.pezzi_vivi[final] = pezzo
            
            return True
        
        return False