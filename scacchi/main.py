from .Boundary.InputUtente import InputUtente
from .Boundary.InterfacciaUtente import InterfacciaUtente
from .Control.PieceControl import PieceControl
from .Control.Utils import leggi_scacchiera
from .Entity.Scacchiera import Scacchiera


def main():
    """Avvia il gioco degli scacchi e attiva il workflow GH."""
    ui = InterfacciaUtente()
    inputt = InputUtente()

    ui.set_accent("blue")

    name = inputt.leggi("Benvenuto in Scacchi! Inserisci il tuo nome: ")
    ui.stampa(f"Ciao {name}! Iniziamo a giocare a scacchi!")

    scacchiera = Scacchiera(leggi_scacchiera())
    pieces = PieceControl()

    colore = 1
    while True:
        ui.display_scacchiera(scacchiera)
        mossa = inputt.leggi_mossa()
        pezzo = pieces.find_piece(scacchiera, mossa, colore)
        if pezzo is not None and pieces.muovi(scacchiera, pezzo, mossa):
            colore = not colore

if __name__ == "__main__":
    main()
