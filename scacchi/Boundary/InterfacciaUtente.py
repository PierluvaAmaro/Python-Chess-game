import os

from rich.console import Console

from ..Entity.Scacchiera import Scacchiera
from ..Utility.Utils import leggi_file


class InterfacciaUtente:
    """CLASSE BOUNDARY."""

    """Gestisce l'interfaccia tra l'utente e il gioco degli scacchi."""

    def __init__(self):
        """Crea una nuova interfaccia utente."""
        self.console = Console()

        self.colori_validi = {
            "black",
            "red",
            "green",
            "yellow",
            "blue",
            "magenta",
            "cyan",
            "white",
            "bright_black",
            "bright_red",
            "bright_green",
            "bright_yellow",
            "bright_blue",
            "bright_magenta",
            "bright_cyan",
            "bright_white",
        }

        self.default = {
            "accent": "cyan",
            "bold": True,
            "underline": False,
            "italic": True,
        }

    def imposta_stile(self, chiave: str, valore) -> bool:
        """Imposta un particolare stile dell'interfaccia.

        Args:
            chiave (str): chiave (nome) dello stile da impostare (es. "accent")
            valore: nuovo valore da assegnare (es. "blue")

        Raises:
            ValueError: se la chiave non esiste

        Returns:
            bool: True se l'azione e' andata a buon fine, False altrimenti.

        """
        if chiave not in self.default:
            raise ValueError(f"Chiave inesistente: '{chiave}'")

        self.default[chiave] = valore

    def get_stile(self, key: str = None):
        """Restituisce il valore di uno stile specifico.

        Args:
            key (str): chiave dello stile da restituire.

        Raises:
            ValueError: se la chiave non esiste.

        """
        if key is not None:
            if key not in self.default:
                raise ValueError("Chiave inesistente.")
        else:
            return self.default[key]

    def formatta_testo(self, text: str):
        """Applica gli stili definizialei al testo.

        Args:
            text (str): testo a cui applicare gli stili specifici.

        """
        style = ""
        if self.default["bold"]:
            style += "bold "
        if self.default["underline"]:
            style += "underline "
        if self.default["italic"]:
            style += "italic "

        style += self.default["accent"]

        return f"[{style}]{text}[/]"

    def stampa(self, prompt: str = "default", stile: str = None):
        """Mostra una stringa con il colore e stile specificato.

        Args:
            prompt (str): stringa da mostrare a schermo.
            stile (str): colore da impostare al prompt.

        """
        if stile is not None:
            self.imposta_stile("accent", stile)

        self.console.print(self.formatta_testo(prompt))
        
    def stampa_scacchiera(self, scacchiera: Scacchiera):
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
    
    def stampa_file(self, filename: str):
        """Mostra il contenuto di un file di aiuto.
 
        Args:
            filename (str): Il percorso del file di aiuto.

        """
        self.imposta_stile("accent", "white")
        self.stampa(leggi_file(filename))
