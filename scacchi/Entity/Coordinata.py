class Coordinata:
    """Classe che rappresenta una coordinata in un sistema cartesiano."""
    
    def __init__(self, x, y):
        """Inizializza una coordinata con le posizioni x e y.

        Args:
            x (int): Posizione orizzontale della coordinata.
            y (int): Posizione verticale della coordinata.

        """
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Confronta due coordinate per verificare se sono uguali.

        Args:
            other (Coordinata): Altra coordinata da confrontare.

        Returns:
            bool: True se le coordinate sono uguali, False altrimenti.

        """
        if not isinstance(other, Coordinata):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        """Restituisce un hash della coordinata basato su x e y."""
        return hash((self.x, self.y))