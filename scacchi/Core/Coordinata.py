class Coordinata:
    """Rappresenta le coordinate x e y sulla scacchiera."""

    def __init__(self, x: int, y: int):
        """Inizializza le coordinate con i valori forniti."""
        self.change(x, y)

    def change(self, x: int = None, y: int = None):
        """Modifica la posizione del pezzo sulla scacchiera.

        Args:
            x (int, optional): Nuova coordinata x.
            y (int, optional): Nuova coordinata y.

        """
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

    def __eq__(self, other):
        """Controlla se due coordinate sono uguali."""
        return isinstance(other, Coordinata) and self.x == other.x and self.y == other.y

    def __hash__(self):
        """Restituisce l'hash della coordinata."""
        return hash((self.x, self.y))

    def to_string(self) -> str:
        """Restituisce la coordinata in formato stringa.

        Returns:
            str: La coordinata in notazione scacchistica, es. 'e4'.

        """
        return f"{chr(ord('a') + self.x - 1)}{self.y}"

    def to_notazione(self) -> str:
        """Restituisce la coordinata in notazione algebrica.

        Returns:
            str: Notazione scacchistica classica, ad esempio 'e4'.

        """
        colonna = chr(ord('a') + self.x - 1)
        riga = str(self.y)
        return f"{colonna}{riga}"