from abc import ABC, abstractmethod

from ..Entity.Coordinata import Coordinata


class Pezzo(ABC):
    """CLASSE ENTITY."""
    
    """Rappresenta un pezzo generico degli scacchi.
    
    Questa e' una classe astratta che funge da base per tutti i pezzi
    specifici (Pedone, Torre, Cavallo, ecc.).
    """

    def __init__(self, simbolo: str, init: Coordinata, colore: bool):
        """Inizializza un nuovo pezzo generico.

        Args:
            simbolo (str): Il simbolo grafico che rappresenta il Pezzo.
            init (Coordinata): La coordinata iniziale del pezzo sulla scacchiera.
            colore (bool): Il colore del pezzo (True = bianco, False = nero)
        
        """
        self.init = init
        self.primo = True # indica se e' il primo movimento del pezzo.
        self.simbolo = simbolo
        self.colore = colore

    @abstractmethod
    def check_move(self, init: Coordinata, final: Coordinata) -> bool:
        """Verifica se una mossa verso una nuova coordinata e' valida per il pezzo.
        
        Deve essere implementata da tutte le sottoclassi.

        Args:
            init (Coordinata): La coordinata di partenza del Pezzo.
            final (Coordinata): La coordinata di destinazione della mossa.

        Returns:
            bool: True se la mossa e' valida, False altrimenti.

        """
        pass