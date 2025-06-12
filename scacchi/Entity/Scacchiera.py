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

    def is_occupied_by_alliance(self, mosso: Pezzo, final: Coordinata) -> bool:
        for coord, pezzo in self.pezzi_vivi.items():
            if pezzo.colore == mosso.colore and coord == final:
                return True
        return False
    
    def is_occupied_by_enemy(self, mosso: Pezzo, final: Coordinata) -> bool:
        for coord, pezzo in self.pezzi_vivi.items():
            if pezzo.colore != mosso.colore and coord == final:
                return True
        return False
    
    def is_occupied(self, final: Coordinata) -> bool:
        """Verifica se la coordinata finale è occupata da un pezzo.
        
        Args:
            final (Coordinata): Coordinata da verificare.
        
        Returns:
            bool: True se la coordinata è occupata, False altrimenti.
        
        """
        return final in self.pezzi_vivi
