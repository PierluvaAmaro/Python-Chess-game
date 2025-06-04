from ..Entity.Coordinata import Coordinata


class Parser:
    """CLASSE CONTROL."""
    
    """Classe per la lettura e la conversione di mosse in notazione scacchistica."""

    def __init__(self):
        """Inizializza un nuovo parser."""
        self.mappa_simboli = {
            'P': {True: '♙', False: '♟'},
            'T': {True: '♖', False: '♜'},
            'C': {True: '♘', False: '♞'},
            'A': {True: '♗', False: '♝'},
            'D': {True: '♕', False: '♛'},
            'K': {True: '♔', False: '♚'},
        }

    def parse_mossa(self, notazione: str, colore):
        """Converti una stringa di notazione scacchistica in una coordinata.
        
        Arg:
            notazione (str): Stringa in notazione algebrica abbreviata (es. "e4").
        
        Raise:
            ValueError: Se la notazione non e' valida o fuori dall'intervallo consentito
        """
        notazione = notazione.strip()
        da_mangiare = "x" in notazione
        notazione = notazione.replace("x", "")  # rimuove la 'x' per analisi

        
        if len(notazione) < 2 or len(notazione) > 4:
            raise ValueError("Notazione non valida.")
        
        # pezzo specificato
        if notazione[0].isalpha() and notazione[1].isalpha():
            lettera_pezzo = notazione[0]
            col = notazione[1].lower()
            row = notazione[2:]
            
        # pezzo non specificato
        else:
            lettera_pezzo = 'P'
            col = notazione[0].lower()
            row = notazione[1:]
            
        if col < 'a' or col > 'h' or not row.isdigit():
            raise ValueError(f"Notazione non valida: {notazione}.")
        
        x = ord(col) - ord('a') + 1
        y = int(row)
        
        if y < 1 or y > 8:
            raise ValueError(f"Riga fuori intervallo: {notazione}.")
        
        simbolo = self.mappa_simboli[lettera_pezzo][colore]
        print(simbolo)
        
        return da_mangiare, simbolo, Coordinata(x, y)