from Core.Parser import Parser
from Core.Scacchiera import Scacchiera, leggi_scacchiera
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

    parser = Parser()
    scacchiera = Scacchiera(leggi_scacchiera())
    colore = 1
    while True:
        print("Turno Bianco" if colore == 1 else "Turno nero")
        scacchiera.draw()

        mossa = parser.leggi_mossa()
        pezzo = scacchiera.find_piece(mossa, colore)

        if pezzo is not None and scacchiera.muovi(pezzo, mossa):
            colore = not colore
    
if __name__ == "__main__":
    main()