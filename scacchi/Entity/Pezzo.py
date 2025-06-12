from abc import ABC, abstractmethod

from ..Entity.Coordinata import Coordinata


class Pezzo(ABC):
    """CLASSE ENTITY."""
    
    """Rappresenta un pezzo generico degli scacchi.
    
    Questa e' una classe astratta che funge da base per tutti i pezzi
    specifici (Pedone, Torre, Cavallo, ecc.).
    """

    def __init__(self, simbolo: str, iniziale: Coordinata, colore: bool):
        """Inizializza un nuovo pezzo generico.

        Args:
            simbolo (str): Il simbolo grafico che rappresenta il Pezzo.
            iniziale (Coordinata): La coordinata iniziale del pezzo sulla scacchiera.
            colore (bool): Il colore del pezzo (True = bianco, False = nero)
        
        """
        self.iniziale = iniziale
        self.primo = 1
        self.simbolo = simbolo
        self.colore = colore

    @abstractmethod
    def controlla_mossa(self, finale: Coordinata, scacchiera=None) -> bool:  # noqa: E501
        """Verifica se una mossa verso una nuova coordinata e' valida per il pezzo.
        
        Args:
            iniziale (Coordinata): La coordinata di partenza del Pezzo.
            finale (Coordinata): La coordinata di destinazione della mossa.
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.

        Returns:
            bool: True se la mossa e' valida, False altrimenti.
            
        """
        pass
    
    @abstractmethod
    def percorso_libero(self, finale: Coordinata, scacchiera) -> bool:
        """Verifica che il percorso tra due coordinate sia libero.
        
        Args:
            iniziale (Coordinata): La coordinata di partenza del Pezzo.
            finale (Coordinata): La coordinata di destinazione della mossa.
            scacchiera: Scacchiera per verificare le posizioni dei pezzi.
            
        Returns:
            bool: True se il percorso e' libero, False altrimenti.
            
        """
        pass
        