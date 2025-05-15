from rich.console import Console

from ..Entity.Coordinata import Coordinata
from ..Entity.Pezzo import Pezzo
from ..Entity.Scacchiera import Scacchiera


class UI:
    """CLASSE BOUNDARY."""

    """Gestisce l'interfaccia tra l'utente e il gioco degli scacchi."""

    def __init__(self):
        """Crea una nuova interfaccia utente."""
        self.console = Console()

        self.valid_colors = {
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

    def set_style(self, key: str, value) -> bool:
        """Imposta un particolare stile dell'interfaccia.

        Args:
            key (str): chiave (nome) dello stile da impostare (es. "accent")
            value: nuovo valore da assegnare (es. "blue")

        Raises:
            ValueError: se la chiave non esiste

        Returns:
            bool: True se l'azione e' andata a buon fine, False altrimenti.

        """
        if key not in self.default:
            raise ValueError(f"Chiave inesistente: '{key}'")

        self.default[key] = value

    def get_style(self, key: str = None):
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

    def format_text(self, text: str):
        """Applica gli stili definiti al testo.

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

    def stampa(self, prompt: str = "default", accent: str = None):
        """Mostra una stringa con il colore e stile specificato.

        Args:
            prompt (str): stringa da mostrare a schermo.
            accent (str): colore da impostare al prompt.

        """
        if accent is not None:
            self.set_style("accent", accent)

        self.console.print(self.format_text(prompt))

    def display_coordinata(self, coord: Coordinata):
        """Mostra una coordinata in formato leggibile.

        Args:
            coord (Coordinata): coordinata da mostrare a schermo

        """
        self.console.print(self.format_text(f"[x: {coord.x}, y: {coord.y}]"))

    def display_pezzo(self, pezzo: Pezzo):
        """Mostra tutte le informazioni riguardanti un pezzo specificato.

        Args:
            pezzo (Pezzo): Pezzo di cui mostare le informazioni.

        """
        self.display_coordinata(self.init)

        console = Console()
        console.print(
            self.format_text(
                f"Primo movimento: {pezzo.primo}"
                f"Colore: {'Bianco' if pezzo.colore else 'Nero'}"
            )
        )

    def display_scacchiera(self, scacchiera: Scacchiera):
        """Mostra a schermo la scacchiera 8x8 senza colori."""
        griglia = [[" . " for _ in range(8)] for _ in range(8)]

        for coord, pezzo in scacchiera.pezzi_vivi.items():
            if pezzo is not None:
                x = coord.x - 1
                y = 8 - coord.y
                griglia[y][x] = f" {pezzo.simbolo} "

        self.console.print()
        self.console.print("    +" + "---+" * 8)

        for i, riga in enumerate(griglia):
            numero_riga = f"{8 - i:>2}"
            print(f" {numero_riga} |" + "|".join(riga) + "|")
            self.console.print("    +" + "---+" * 8)

        lettere = "".join(f" {chr(97 + i)}  " for i in range(8))
        self.console.print(f"     {lettere}")

    def display_help(self, filename: str):
        """Mostra il contenuto di un file di aiuto.

        Args:
            filename (str): Il percorso del file di aiuto.

        """
        try:
            with open(filename, encoding="utf-8") as f:
                help_content = f.read()
            self.console.print(help_content)
        except FileNotFoundError:
            self.ui.stampa(
                f"Errore: File di aiuto '{filename}' non trovato.", accent="red"
            )
        except Exception as e:
            self.ui.stampa(
                f"Errore durante la lettura del file di aiuto: {e}", accent="red"
            )
