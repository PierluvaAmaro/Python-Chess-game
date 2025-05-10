from Core.Coordinata import Coordinata


class Parser:
    """Classe per la lettura e la conversione di mosse in notazione scacchistica."""

    def __init__(self):
        """Inizializza un nuovo parser."""
        pass

    def leggi_mossa(self, prompt="Inserisci mossa (es. e4): ") -> Coordinata:
        """Legge una mossa dell'utente e la converte in una Coordinata.
        
        Continua a chiedere l'input finche' l'utente non inserisce una mossa valida. 
        
        Args:
            prompt (str): Messaggio da mostrare all'utente
        
        Returns:
            Coordinata: L'oggetto coordinata corrispondente alla mossa inserita.

        """
        while True:
            try:
                mossa = input(prompt).strip()
                return self.parse_mossa(mossa)

            except ValueError as e:
                print(f"Errore: {e}. Riprova.")

    def parse_mossa(self, notazione: str) -> Coordinata:
        """Converti una stringa di notazione scacchistica in una coordinata.
        
        Args:
            notazione (str): Stringa in notazione algebrica abbreviata (es. "e4").
        
        Returns:
            Coordinata: La coordinata corrispondente sulla scacchiera.
        
        Raises:
            ValueError: Se la notazione non e' valida o fuori dall'intervallo consentito
        
        """
        if len(notazione) != 2:
            raise ValueError("Notazione non valida.")
        
        col = notazione[0].lower()
        row = notazione[1]

        if(col < 'a' or col > 'h' or not row.isdigit()):
            raise ValueError(f"Notazione non valida: {notazione}")
            
        x = ord(col) - ord('a') + 1
        y = int(row)

        if y < 1 or y > 8:
            raise ValueError(f"Riga fuori intervallo: {notazione}")

        return Coordinata(x, y)