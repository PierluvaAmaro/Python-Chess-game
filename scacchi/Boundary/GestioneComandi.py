class GestioneComandi:
    """CLASSE BOUNDARY."""
    
    """Gestisce l'input dei comandi dell'utente."""

    def __init__(self):
        """Inizializza un nuovo oggetto ComandoUtente."""
        pass

    def esegui_comando(self, comando: str) -> int:
        """Rileva ed esegue un comando.
        
        Args:
            comando (str): comando da eseguire.

        Returns:
            int: stato che rappresenta il tipo di comando inserito.

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