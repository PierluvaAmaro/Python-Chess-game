from ..Entity.Coordinata import Coordinata
from ..Entity.Pezzo import Pezzo
from ..Entity.Scacchiera import Scacchiera


class PieceControl:
    """CLASSE CONTROL."""
    
    """Controlla le operazioni sui pezzi durante il gioco degli scacchi."""

    def __init__(self):
        """Inizializza un oggetto PieceControl."""
        pass

    def find_piece(self, scacchiera: Scacchiera, final: Coordinata, colore: bool,
                   simbolo) -> Pezzo:
        """Trova il pezzo del colore specificato che puo' muoversi alla coordinata.
        
        Args:
            scacchiera (Scacchiera): La scacchiera di gioco contenente i pezzi
            final (Coordinata): Coordinata di destinazione del pezzo.
            colore (bool): Colore del pezzo da cercare.
            simbolo: Carattere simbolico del pezzo da cercare.
            
        Returns:
            Pezzo: Il primo pezzo valido che puo' effettuare la mossa, se trovato.
        
        """
        for _, piece in scacchiera.pezzi_vivi.items():
            if (piece is not None and piece.colore == colore and 
                piece.simbolo == simbolo and piece.check_move(final, scacchiera)):
                    return piece
        
        print("Nessun tuo pezzo puo' effettuare quella mossa.")
        return None

    def muovi(self, da_mangiare: bool, scacchiera: Scacchiera, colore : bool, pezzo: Pezzo, final: Coordinata) -> bool:
        """Esegue lo spostamento di un pezzo se la destinazione è valida."""
        if pezzo.simbolo == "♔" or pezzo.simbolo == "♚":
            if self.is_threatened_by_enemy(colore, scacchiera, final):
                raise ValueError("Posizione minacciata da nemico")

        if scacchiera.is_occupied_by_alliance(pezzo, final):
            raise ValueError("Mossa illegale")

        if da_mangiare:
            if not scacchiera.is_occupied_by_enemy(pezzo, final):
                raise ValueError("Mossa illegale")
            # Cattura il pezzo nemico
            scacchiera.pezzi_vivi.pop(final)
        else:
            if scacchiera.is_occupied_by_enemy(pezzo, final):
                raise ValueError("Mossa illegale")

        # Esegui il movimento
        scacchiera.pezzi_vivi.pop(pezzo.init)
        pezzo.init = final
        scacchiera.pezzi_vivi[final] = pezzo

        return True

    def is_threatened_by_enemy(self, colore: bool,  scacchiera: Scacchiera, final: Coordinata) -> bool:
        minacciato = False
        for _, pezzo in scacchiera.pezzi_vivi.items():
            if pezzo.colore != colore:
                if pezzo.check_move(final, scacchiera):
                    minacciato = True
        
        return minacciato