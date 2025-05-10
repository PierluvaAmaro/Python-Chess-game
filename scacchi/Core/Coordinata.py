class Coordinata:
    """Rappresenta una coppia di coordinate cartesiane (x, y)."""

    def __init__(self, x: int, y: int):
        """Inizializza una nuova coordinata con i valori specificati.
        
        Args:
            x (int): La coordinata orizzontale.
            y (int): La coordinata verticale.

        Raises:
            ValueError: Se uno dei due valori e' None

        """
        self.change(x, y)

    def change(self, x: int, y: int):
        """Modifica i valori delle coordinate x e y.

        Args:
            x (int): Il nuovo valore per la coordinata x.
            y (int): Il nuovo valore per la coordinata y.

        Raises:
            ValueError: Se x o y sono None.

        """
        if x is not None:
            self.x = x
        else: 
            raise ValueError("Valore X non valido.")
        
        if y is not None:
            self.y = y
        else:
            raise ValueError("Valore Y non valido.")

    def display(self):
        """Stampa le coordinate in formato leggibile."""
        print(f"[x: {self.x}, y: {self.y}]\n")

    def __eq__(self, other):
        """Confronta due coordinate per uguaglianza.

        Args:
            other (Coordinata): L'altra coordinata da confrontare.

        Returns:
            bool: True se le coordinate sono uguali, False altrimenti.

        """
        if isinstance(other, Coordinata):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        """Restituisce un hash della coordinata.

        Returns:
            int: L'hash basato su x e y.
            
        """
        return hash((self.x, self.y))