from ..Entity.Coordinata import Coordinata


class Parser:
    """CLASSE CONTROL."""
    
    """Classe per la lettura e la conversione di mosse in notazione scacchistica."""

    def __init__(self):
        """Inizializza un nuovo parser."""
        pass

    def parse_mossa(self, notazione: str):
        """Converti una stringa di notazione scacchistica in una coordinata.
        
        Args:
            notazione (str): Stringa in notazione algebrica abbreviata (es. "e4").
        
        Raises:
            ValueError: Se la notazione non e' valida o fuori dall'intervallo consentito
        
        """
        if len(notazione) != 2:
            raise ValueError("Notazione non valida.")
        
        col = notazione[0].lower()
        row = notazione[1]

        if(col < 'a' or col > 'h' or not row.isdigit()):
            raise ValueError(f"Notazione non valida: {notazione}")
            
        x = ord(col) - ord('a') + 1
        y = int(row)

        if y < 1 or y > 8:
            raise ValueError(f"Riga fuori intervallo: {notazione}")

        return Coordinata(x, y)