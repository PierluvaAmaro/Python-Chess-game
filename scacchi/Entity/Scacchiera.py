from Entity.Coordinata import Coordinata
from Entity.Pezzo import Pezzo


class Scacchiera:
    """Rappresenta lo stato della scacchiera e gestisce le operazioni sui Pezzi."""

    def __init__(self, pezzi_vivi: dict[Coordinata, Pezzo]):
        """Inizializza la scacchiera con i pezzi forniti.
        
        Args:
            pezzi_vivi (dict[Coordinata, Pezzo]): Dizionario contenente i pezzi attivi.

        """
        self.pezzi_vivi = pezzi_vivi

    def is_occupied(self, final: Coordinata) -> bool:
        """Verifica se una casella e' occupata da un pezzo.

        Args:
            final (Coordinata): Coordinata da controllare.

        Returns:
            bool: True se la casella e' occupata, False altrimenti.

        """ 
        if final in self.pezzi_vivi:
            print("Posizione occupata.")
            return True
        return False