from ..Control.Parser import Parser
from ..Entity.Coordinata import Coordinata


class InputUtente:
    """Gestisce l'input dell'utente."""

    def __init__(self):
        """Inizializza un nuovo oggetto InputUtente."""
        pass

    def leggi_mossa(self, prompt: str = "Inserisci mossa (es. 'e4'): ") -> Coordinata:
        """Legge una mossa dell'utente da input e la converte in una Coordinata.
        
        Mostra un prompt all'utente e attende un input di mossa (es. 'e4').
        Se l'input non e' valido, mostra un messaggio di errore e ripete la richiesta.
        
        Args:
            prompt: Il messaggio da mostrare (default: "Inserisci mossa (es. 'e4')
        
        Returns:
            Coordinata: L'oggetto Coordianta risultante dal parsing dell'input.

        """
        parser = Parser()

        while True:
            try:
                mossa = input(prompt).strip()
                return parser.parse_mossa(mossa)
            except ValueError as e:
                print(f"Errore: {e}. Riprova.")

    def leggi(self, prompt: str = "") -> str:
        """Prende in input una stringa dall'utente."""
        return input(prompt)