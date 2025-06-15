class GestioneComandi:
    """Classe boundary per la gestione dei comandi utente."""
    
    def __init__(self):
        """Inizializza un nuovo oggetto per la gestione dei comandi."""
        pass

    def esegui_comando(self, comando: str) -> int:
        """Rileva ed esegue un comando specificato.
        
        Args:
            comando (str): Comando da eseguire (es. "/gioca", "/help").
        
        Returns:
            int: Codice di stato che rappresenta il tipo di comando:
                - 1: /gioca
                - 2: /scacchiera
                - 3: /help
                - 4: /mosse
                - 5: /patta
                - 6: /abbandona
                - 7: /esci

        Raises:
            NotImplementedError: se il comando e' sconosciuto.

        """
        match comando:
            case "/gioca":
                return 1

            case "/scacchiera":
                return 2
            
            case "/help":
                return 3
            
            case "/mosse":
                return 4
                
            case "/patta":
                return 5
            
            case "/abbandona":
                return 6

            case "/esci":
                return 7

            case _:
                raise NotImplementedError("Comando inesistente.")