from Entity.Coordinata import Coordinata
from Entity.Pezzo import Pezzo
from Entity.Scacchiera import Scacchiera
from rich import print
from rich.console import Console


class InterfacciaUtente:
    """Gestisce l'interfaccia utente per il gioco degli scacchi."""

    def __init__(self):
        """Crea una nuova interfaccia utente."""
        self.valid_colors = {
            "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
            "bright_black", "bright_red", "bright_green", "bright_yellow",
            "bright_blue", "bright_magenta", "bright_cyan", "bright_white"
        }
    
    def set_accent(self, accent: str):
        """Imposta un colore d'accento all'interfaccia.
        
        Args:
            accent (str): colore d'accento da impostare.

        """
        if accent is None:
            raise ValueError(f"'{accent}' non è un colore valido.")
        
        if accent in self.valid_colors:
            self._accent_color = accent
        else:
            raise ValueError(f"'{accent}' non è un colore valido.")
    
    def get_accent(self) -> str:
        """Restitusce il colore di accento corrente."""
        return self._accent_color
    
    def stampa(self, prompt: str = "", accent: str = None):
        """Mostra una stringa a schermo con un colore d'accento.
        
        Args:
            prompt (str): Stringa da mostrare.
            accent (str): Colore da impostare al prompt

        """
        console = Console()
        if accent is not None:
            self.set_accent(accent)
            
        console.print(f"[bold {self._accent_color}]{prompt}[/]")
              
    def display_coordinata(self, coord: Coordinata):
        """Mostra una coordinata in formato leggibile.

        Args:
            coord (Coordinata): Coordinata da mostrare a schermo.

        """
        console = Console()
        console.print(f"[bold {self._accent_color}][x:{coord.x}, y:{coord.y}]")

    def display_pezzo(self, pezzo: Pezzo):
        """Mostra le informazioni di un pezzo.
        
        Args:
            pezzo (Pezzo): Pezzo di cui stampare le informazioni.

        """
        print(f"x: {pezzo.init.x}, y: {pezzo.init.y}")
        print(
            f"Movimento: {pezzo.primo}\n"
            f"Colore: {'Bianco' if pezzo.colore else 'Nero'}"  
            )
    
    def display_scacchiera(self, scacchiera: Scacchiera):
        """Disegna la scacchiera con i pezzi presenti.
        
        Args:
            scacchiera (Scacchiera): Scacchiera da disegnare.

        """
        griglia = [[" . " for _ in range(8)] for _ in range(8)]

        for coord, pezzo in scacchiera.pezzi_vivi.items():
            if pezzo:
                x = coord.x - 1
                y = 8 - coord.y
                griglia[y][x] = f" {pezzo.simbolo} "

        print()
        print("   +" + "---+" * 8)

        for i, riga in enumerate(griglia):
            print(f" {8 - i} |" + "|".join(riga) + "|")
            print("   +" + "---+" * 8)
        
        self.stampa("   " + "".join(f"  {chr(97 + i)} " for i in range(8)), "cyan")