from Core.Coordinata import Coordinata
from Core.Scacchiera import Scacchiera
from Pezzi.Pedone import Pedone
from rich import print
from UI.UI import UI


def main():
    """Run the Scacchi game and activate the GH workflows."""
    ui = UI()
    ui.set_accent_color("blue")

    name = input("Benvenuto in Scacchi! Inserisci il tuo nome: ")
    print(
        f"Ciao [bold {ui.get_accent_color()}]{name}[/bold {ui.get_accent_color()}]! "
        "Iniziamo a giocare a [bold]scacchi[/bold]!"
    )

    pedone = Pedone(Coordinata(1,1), "bianco", "♟")
    scacchiera = Scacchiera({pedone.init: pedone})
    scacchiera.check_position(pedone, Coordinata(1,2))
    
if __name__ == "__main__":
    main()