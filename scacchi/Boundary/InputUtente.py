from rich.prompt import Prompt

from ..Control.Parser import Parser
from ..Entity.Coordinata import Coordinata
from .GestioneComandi import GestioneComandi


class InputUtente:
    """Classe boundary per la gestione dell'input da parte dell'utente."""    

    def __init__(self):
        """Inizializza un nuovo oggetto per la gestione dell'input utente."""
        self.parser = Parser()

    def leggi_mossa(self, prompt: str) -> Coordinata:
        """Legge e converte una mossa dell'utente in un oggetto Coordinata.
        
        Mostra un prompt e attende l'input. In caso di errore, richiede 
        nuovamente l'input dopo aver visualizzato un messaggio di errore.

        Args:
            prompt (str): Messaggio personalizzato.

        Returns:
            Coordinata: Oggetto risultante dal parsing dell'input.

        Raises:
            ValueError: Reiterato internamente finché l'input non è valido.
        
        """
        while True:
            try:
                mossa = input(prompt).strip()
                
                return self.parser.parse_mossa(mossa)
                    
            except ValueError as e:
                print(f"Errore: {e} Riprova.")

    def leggi(self, prompt: str = "") -> str:
        """Prende in input una stringa dall'utente.
        
        Args:
            prompt (str): stringa da stampare.
        
        """
        return Prompt.ask(prompt)
    
    def in_ascolto(self, stringa: str):
        """Verifica se l'input è un comando e lo esegue.
        
        Args:
            stringa (str): Input da verificare.

        Returns:
            int: Codice del comando se riconosciuto.

        Raises:
            NotImplementedError: Gestito internamente con stampa dell'errore.
        
        """
        try:
            if stringa.startswith("/"):
                comandi = GestioneComandi()
                return comandi.esegui_comando(stringa)
            return None
        except NotImplementedError as e:
            print(f"Errore: {e}. Riprova")