from ..Entity.Coordinata import Coordinata


class Parser:
    """Classe control per la conversione di notazioni scacchistiche in mosse."""
    
    def __init__(self):
        """Inizializza il parser con la mappa dei simboli Unicode per i pezzi."""
        self.mappa_simboli = {
            'P': {True: '♙', False: '♟'},     # Pedone
            'T': {True: '♖', False: '♜'},     # Torre
            'C': {True: '♘', False: '♞'},     # Cavallo
            'A': {True: '♗', False: '♝'},     # Alfiere
            'D': {True: '♕', False: '♛'},     # Regine
            'K': {True: '♔', False: '♚'},     # Re
        }

    def parse_mossa(self, notazione: str, colore):
        """Converti una notazione scacchistica in una mossa strutturata.
        
        Args:
            notazione: Stringa nella notazione scacchistica (es. 'e4', 'Nxf6+').
            colore: Colore del pezzo che muove (True = bianco, False = nero).

        Returns:
            Dizionario con la struttura:
            {
                "tipo": str ("mossa"|"arrocco"),
                "cattura": bool,
                "simbolo": str (simbolo Unicode),
                "finale": Coordinata,
                "promozione": str | None,
                "en_passant": bool | None,
                "scacco": bool,
                "matto": bool,
                "lato": str | None (solo per arrocco)
            }

        Raises:
            ValueError: Se la notazione è malformata o contiene valori non validi.
        
        """
        notazione = notazione.strip()

        if notazione in ("0-0", "O-O"):
            return {"tipo": "arrocco", "lato": "corto", "cattura": False}
        if notazione in ("0-0-0", "O-O-O"):
            return {"tipo": "arrocco", "lato": "lungo", "cattura": False}
        
        # modificatori
        modificatori = {
            'scacco': '+' in notazione,
            'matto': '#' in notazione,
            'cattura': 'x' in notazione
        }
        notazione = notazione.replace('+', '').replace('#', '').replace('x', '').strip()
        
        # estrazione informazioni pezzo
        lettera_pezzo = 'P'
        if len(notazione) >= 3 and notazione[0].isalpha() and notazione[1].isalpha():
            lettera_pezzo, colonna = notazione[0].upper(), notazione[1].lower()
            riga = notazione[2:]
        else:
            colonna = notazione[0].lower()
            riga = notazione[1:]
        
        if not ('a' <= colonna <= 'h'):
            raise ValueError(f"Colonna '{colonna}' non valida. Usa lettere a-h.")
        
        try:
            y = int(riga)
            if not (1 <= y <= 8):
                raise ValueError
        except ValueError as err:
            raise ValueError(f"Riga '{riga} non valida. Usa numeri 1-8") from err
        
        x = ord(colonna) - ord('a') + 1
        simbolo = self.mappa_simboli.get(lettera_pezzo, {}).get(colore)
        if simbolo is None:
            raise ValueError(f"Pezzo '{lettera_pezzo}' non riconosciuto o colore"\
                " non valido")
        
        return {
            "tipo": "mossa",
            "cattura": modificatori['cattura'],
            "simbolo": simbolo,
            "finale": Coordinata(x, y),
            "promozione": self._parse_promozione(notazione),
            "en_passant": self._parse_en_passant(notazione, lettera_pezzo),
            "scacco": modificatori['scacco'],
            "matto": modificatori['matto']
        }
        
    def _parse_promozione(self, notazione: str) -> str | None:
        """Estrae l'informazione di promozione dalla notazione.
        
        Args:
            notazione (str): notazione da cui estrarre le informazioni sulla promozione.
        
        Returns:
            str: Se il pezzo in promozione e' accettato, None altrimenti.
            
        """
        if "=" in notazione:
            pezzo = notazione.split('=')[1][0].upper()
            if pezzo in ('D','T','A','C'):
                return self.mappa_simboli.get(pezzo, {}).get(True)

        return None
    
    def _parse_en_passant(self, notazione: str, lettera: str) -> bool:
        """Determina se la mossa e' un en passant.
        
        Args:
            notazione (str): notazione da cui estrarre l'informazione sull'en-passant.
            lettera (str): lettera del pezzo.
        
        Returns:
            bool: True se e' stato specificato l'en-passant, False altrimenti.    
        
        """
        return lettera == 'P' and 'e.p.' in notazione