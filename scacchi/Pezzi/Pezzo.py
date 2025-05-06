from abc import ABC, abstractmethod

from Core.Coordinata import Coordinata


class Pezzo(ABC):
    """Classe astratta che definisce un pezzo generico degli scacchi.
    
    Permette di controllare la mossa effettuata dal giocatore
    e di disegnare il pezzo sulla scacchiera.
    """

    def __init__(self, init: Coordinata, colore: str, id: str,  
                 primo: bool
    ):
        """Costruttore che inizializza il pezzo."""
        self.init = init
        self.colore = colore
        self.id = id
        self.primo = primo
        self.final = init

    @abstractmethod
    def check_move(self, move: Coordinata) -> bool:
        """Metodo astratto che permette di controllare il movimento del pezzo."""
        if(True):
            pass
    
    def draw(self):
        """Metodo che permette di disegnare il pezzo singolo sulla tastiera."""
        print(self.id)