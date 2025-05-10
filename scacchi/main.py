from UI import UI
from Utility.Utils import leggi_scacchiera

from Boundary.InputUtente import InputUtente
from Boundary.InterfacciaUtente import InterfacciaUtente
from Control.PieceControl import PieceControl
from Entity.Scacchiera import Scacchiera


def main():
    """Run the Scacchi game and activate the GH workflows."""
    """ ui = UI()
    ui.set_accent_color("blue")

    name = input("Benvenuto in Scacchi! Inserisci il tuo nome: ")
    print(
        f"Ciao [bold {ui.get_accent_color()}]{name}[/bold {ui.get_accent_color()}]! "
        "Iniziamo a giocare a [bold]scacchi[/bold]!"
    ) """
    scacchiera = Scacchiera(leggi_scacchiera())
    interfaccia = InterfacciaUtente()
    pieces = PieceControl(scacchiera)

    inputt = InputUtente()

    colore = 1

    while True:
        interfaccia.display_scacchiera(scacchiera)
        mossa = inputt.leggi_mossa()
        pezzo = pieces.find_piece(mossa, colore)

        if pezzo is not None and pieces.muovi(pezzo, mossa):
            colore = not colore
    
if __name__ == "__main__":
    main()