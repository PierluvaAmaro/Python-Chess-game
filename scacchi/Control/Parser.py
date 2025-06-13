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
        """Converti una mossa scacchistica in un oggetto di tipo Coordinata.
        
        Args:
            notazione(str): Notazione scacchistica della mossa.
            colore(bool): Colore del pezzo che sta effettuando la mossa.
            
        """
        # controllo se e' stato dichiarato lo scacco
        scacco = '+' in notazione
        if scacco:
            notazione = notazione.replace('+', '')
        
        # controllo se il pezzo deve catturare
        cattura = 'x' in notazione
        if cattura:
            notazione = notazione.replace('x', '')
        
        matto = '#' in notazione
        if matto:
            notazione = notazione.replace('#', '')
            
        notazione = notazione.strip()
        
        # controllo se il pezzo è stato specificato
        # almeno 3 caratteri, di cui i primi due sono lettere
        lettera_pezzo = 'P'
        if len(notazione) >= 3 and notazione[0].isalpha() and notazione[1].isalpha():
            lettera_pezzo = notazione[0]
            colonna = notazione[1].lower()
            riga = notazione[2:]
        else:
            colonna = notazione[0].lower()
            riga = notazione[1:]
        
        if colonna < 'a' or colonna > 'h':
            raise ValueError("Colonna non valida. Deve essere tra 'a' e 'h'.")

        x = ord(colonna) - ord('a') + 1
        y = int(riga)
        
        if y < 1 or y > 8:
            raise ValueError("Riga non valida. Deve essere tra 1 e 8.")
        
        simbolo = self.mappa_simboli.get(lettera_pezzo, {}).get(colore)
        if simbolo is None:
            raise ValueError(f"Simbolo non valido per il pezzo: {lettera_pezzo}")
        
        return {
            "tipo": "mossa",
            "cattura": cattura,
            "simbolo": simbolo,
            "finale": Coordinata(x, y),
            # TODO: gestire promozione e en_passant
            "promozione": None,
            "en_passant": None,
            "scacco": scacco,
            "matto": matto
        }
    