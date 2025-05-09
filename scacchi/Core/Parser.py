from Core.Coordinata import Coordinata


class Parser:
    """CLasse che coonverte una mossa: NA -> Coordinata."""

    def __init__(self):
        self.da_controllare = Coordinata(None, None, None)

    def leggi_mossa(self, prompt="Inserisci mossa (es. e4): ") -> Coordinata:
        while True:
            try:
                mossa = input(prompt).strip()
                return self.parse_mossa(mossa)

            except ValueError as e:
                print(f"Errore: {e}. Riprova.")

    def parse_mossa(self, notazione: str) -> Coordinata:
        if len(notazione) != 2:
            raise ValueError(f"Notazione non valida: {notazione}")
        
        col = notazione[0].lower()
        row = notazione[1]

        if(col < 'a' or col > 'h' or not row.isdigit()):
            raise ValueError(f"Notazione non valida: {notazione}")
        
        x = ord(col) - ord('a') + 1
        y = int(row)

        if y < 1 or y > 8:
            raise ValueError(f"Riga fuori intervallo: {notazione}")

        return Coordinata(x, y, False)