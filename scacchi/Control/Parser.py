import re

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
        
        self.espressione = re.compile(r"""^(?:O-O(-O)?|0-0(-0)?)$|^(?P<pezzo>[RDTAC])?(?P<origine>[a-h]?[1-8]?)[x:]?(?P<colonna>[a-h])(?P<riga>[1-8])(?:=(?P<promo>[RDTAC]))?(?P<scacco>[+#]?)(?:\s*(?:ep|e\.p\.))?$""")

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
            return {"tipo": "arrocco", "lato": "corto", "cattura": False, "iniziale": None, "finale": None, "simbolo": None, "promozione": None, "en_passant": False, "scacco": False, "matto": False   }
    
        if notazione in ("0-0-0", "O-O-O"):
            return {"tipo": "arrocco", "lato": "lungo", "cattura": False, "iniziale": None, "finale": None, "simbolo": None, "promozione": None, "en_passant": False, "scacco": False, "matto": False   }
        
        
        match = self.espressione.match(notazione)
        if not match:
            raise ValueError(f"Notazione '{notazione}' non valida.")
        
        pezzo = match.group('pezzo') or 'P'
        origine = match.group('origine') or '' 
        
        colonna = match.group('colonna')
        riga = match.group('riga')
        
        promozione = match.group('promo')
        scacco_matto = match.group('scacco') or ''

        
        cattura = 'x' in notazione
        finale = Coordinata(ord(colonna) - ord('a') + 1, int(riga))
        
        if origine:
            if len(origine) == 2:
                x = ord(origine[0]) - ord('a') + 1
                y = int(origine[1])
                iniziale = Coordinata(x, y)
            elif origine and origine[0].isalpha():
                x = ord(origine[0]) - ord('a') + 1
                iniziale = Coordinata(x, None)
            elif origine and origine[0].isdigit():
                y = int(origine[0])
                iniziale = Coordinata(None, y)
            else:
                iniziale = None
        else:
            iniziale = None
        
        simbolo = self.mappa_simboli.get(pezzo.upper(), {}).get(colore)
        if not simbolo:
            raise ValueError(f"Pezzo non riconosciuto o colore non valido: {pezzo}")
        
        return {
            "tipo": "mossa",
            "cattura": cattura,
            "simbolo": simbolo,
            "iniziale": iniziale,
            "finale": finale,
            "promozione": self._parse_promozione(promozione, colore),
            "en_passant": self._parse_en_passant(notazione, pezzo),
            "scacco": scacco_matto == '+',
            "matto": scacco_matto == '#'
        }

    def _parse_promozione(self, promo: str | None, colore: bool) -> str | None:
        """Ritorna la lettera del pezzo in promozione se valido."""
        if promo and promo.upper() in self.mappa_simboli:
            return promo.upper()
        return None

    def _parse_en_passant(self, notazione: str, pezzo: str) -> bool:
        """Determina se si tratta di un en passant (solo per pedoni)."""
        return pezzo.upper() == 'P' and (
            'ep' in notazione.lower() or 'e.p.' in notazione.lower()
        )