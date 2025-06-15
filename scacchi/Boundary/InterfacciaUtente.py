import os

from rich.console import Console

from ..Entity.Scacchiera import Scacchiera
from ..Utility.Utils import leggi_file


class InterfacciaUtente:
    """Classe boundary per la gestione dell'interfaccia utente degli scacchi."""
    
    def __init__(self):
        """Inizializza una nuova interfaccia utente con stili predefiniti."""
        self.console = Console()
        self.colori_validi = {
            "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
            "bright_black", "bright_red", "bright_green", "bright_yellow",
            "bright_blue", "bright_magenta", "bright_cyan", "bright_white"
        }
        self.default = {
            "accent": "cyan",
            "bold": True,
            "underline": False,
            "italic": True,
        }

    def imposta_stile(self, chiave: str, valore) -> bool:
        """Modifica uno stile dell'interfaccia.
        
        Args:
            chiave: Nome dello stile da modificare (es. "accent").
            valore: Nuovo valore dello stile (deve essere un colore valido per 
                    gli stili accent).
            
        Returns:
            bool: True se la modifica è avvenuta con successo, False altrimenti.

        Raises:
            ValueError: Se la chiave non esiste o il valore non è valido.
        
        """
        if chiave not in self.default:
            raise ValueError(f"Chiave di stile inesistente: '{chiave}'")
        if chiave == "accent" and valore not in self.colori_validi:
            raise ValueError(f"Colore non valido: '{valore}'")

        self.default[chiave] = valore
        return True

    def get_stile(self, chiave: str = None):
        """Restituisce uno stile specifico o tutti gli stili.

        Args:
            chiave: Nome dello stile da ottenere. Se None, restituisce tutti gli stili.

        Returns:
            Il valore dello stile richiesto o il dizionario completo se chiave è None.

        Raises:
            ValueError: Se la chiave non esiste.

        """
        if chiave is None:
            return self.default.copy()
        if chiave not in self.default:
            raise ValueError(f"Chiave di stile inesistente: '{chiave}'")
        
        return self.default[chiave]

    def formatta_testo(self, testo: str):
        """Applica gli stili correnti al testo.

        Args:
            testo (str): Testo da formattare.
        
        Returns:
            str: Stringa formattata con i tag Rich

        """
        style = ""
        if self.default["bold"]:
            style += "bold "
        if self.default["underline"]:
            style += "underline "
        if self.default["italic"]:
            style += "italic "

        style += self.default["accent"]

        return f"[{style}]{testo}[/]"

    def stampa(self, messaggio: str = "default", stile: str = None):
        """Stampa un messaggio formattato.
        
        Args:
            messaggio: Testo da stampare.
            stile: Colore temporaneo da applicare (opzionale).
            
        """
        if stile is not None:
            stile_originale = self.default["accent"]
            self.imposta_stile("accent", stile)
            self.console.print(self.formatta_testo(messaggio))
            self.imposta_stile("accent", stile_originale)
        else:
            self.console.print(self.formatta_testo(messaggio))
        
    def stampa_scacchiera(self, scacchiera: Scacchiera):
        """Stampa una rappresentazione grafica della scacchiera.
        
        Args:
            scacchiera: Oggetto Scacchiera da visualizzare.
            
        """
        os.system('cls' if os.name == 'nt' else 'clear')

        # Offset per spostare la scacchiera
        offset_x = "      "  # 6 spazi a sinistra
        offset_y = 2         # 2 righe vuote sopra

        # Riga vuota per spostare in basso
        for _ in range(offset_y):
            self.console.print()

        # Creo una matrice 8x8 di stringhe vuote
        griglia = [["   " for _ in range(8)] for _ in range(8)]

        # Inserisco i simboli dei pezzi nella griglia
        for coord, pezzo in scacchiera.pezzi_vivi.items():
            if pezzo is not None:
                x = coord.x - 1
                y = 8 - coord.y
                griglia[y][x] = f" {pezzo.simbolo} "

        lettere_colonne = offset_x + "   " + "  ".join(f" {chr(97 + i)}"
                                                       for i in range(8))
        self.imposta_stile("accent", "cyan")
        self.stampa(lettere_colonne)

        self.imposta_stile("accent", "white")
        self.console.print(offset_x + "  " + "┌" + "───┬" * 7 + "───┐")

        for i, riga in enumerate(griglia):
            numero_riga = 8 - i
            riga_str = "│".join(riga)
            self.console.print(f"{offset_x}{numero_riga} │{riga_str}│ {numero_riga}")
            if i < 7:
                self.console.print(offset_x + "  " + "├" + "───┼" * 7 + "───┤")
            else:
                self.console.print(offset_x + "  " + "└" + "───┴" * 7 + "───┘")

        self.imposta_stile("accent", "cyan")
        self.stampa(lettere_colonne)
    
    def stampa_file(self, filename: str, colore: str = None):
        """Stampa il contenuto di un file con formattazione.
        
        Args:
            filename: Percorso del file da stampare.
            colore: Colore del testo (opzionale).
            
        """
        if colore is None:
            self.imposta_stile("accent", "white")
        else:
            self.imposta_stile("accent", colore)
            
        self.stampa(leggi_file(filename))
