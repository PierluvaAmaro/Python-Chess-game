from .Coordinata import Coordinata
from .Pezzo import Pezzo


class Scacchiera:
    """CLASSE ENTITY."""
    
    """Rappresenta lo stato della scacchiera e gestisce le operazioni sui Pezzi."""

    def __init__(self, pezzi_vivi: dict[Coordinata, Pezzo]):
        """Inizializza la scacchiera con i pezzi forniti.
        
        Args:
            pezzi_vivi (dict[Coordinata, Pezzo]): Dizionario contenente i pezzi attivi.

        """
        self.pezzi_vivi = pezzi_vivi

    def occupata_da_alleato(self, mosso: Pezzo, finale: Coordinata) -> bool:
        for coord, pezzo in self.pezzi_vivi.items():
            if pezzo.colore == mosso.colore and coord == finale:
                return True
        return False
    
    def occupata_da_nemico(self, mosso: Pezzo, finale: Coordinata) -> bool:
        for coord, pezzo in self.pezzi_vivi.items():
            if pezzo.colore != mosso.colore and coord == finale:
                return True
        return False
    
    def occupata(self, finale: Coordinata) -> bool:
        """Verifica se la coordinata finale è occupata da un pezzo.
        
        Args:
            finale (Coordinata): Coordinata da verificare.
        
        Returns:
            bool: True se la coordinata è occupata, False altrimenti.
        
        """
        return finale in self.pezzi_vivi