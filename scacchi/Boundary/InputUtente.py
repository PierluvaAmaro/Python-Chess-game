from ..Control.Parser import Parser
from .CommandListener import CommandListener


class InputUtente:
    """CLASSE BOUNDARY."""
    
    """Gestisce l'input dell'utente."""

    def __init__(self):
        """Inizializza un nuovo oggetto InputUtente."""
        self.parser = Parser()

    def leggi_mossa(self, prompt: str = "Inserisci mossa (es. 'e4'): "):
        """Legge una mossa dell'utente da input e la converte in una Coordinata.
        
        Mostra un prompt all'utente e attende un input di mossa (es. 'e4').
        Se l'input non e' valido, mostra un messaggio di errore e ripete la richiesta.
        
        Args:
            prompt: Il messaggio da mostrare (default: "Inserisci mossa (es. 'e4')
        
        Returns:
            Coordinata: L'oggetto Coordianta risultante dal parsing dell'input.

        """
        while True:
            try:
                mossa = input(prompt).strip()
                
                return self.parser.parse_mossa(mossa)
                    
            except ValueError as e:
                print(f"Errore: {e}. Riprova.")

    def leggi(self, prompt: str = "") -> str:
        """Prende in input una stringa dall'utente."""
        return input(prompt)
    
    def listen(self, stringa: str):
        """Verifica se e' stato inserito un comando.
        
        Args:
            stringa (str): stringa da verificare

        """
        try:
            if stringa.startswith("/"):
                commandListener = CommandListener()
                return commandListener.run_command(stringa)
            return None
        except NotImplementedError as e:
            print(f"Errore: {e}. Riprova")