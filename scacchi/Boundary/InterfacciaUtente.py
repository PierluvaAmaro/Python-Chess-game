from Entity.Coordinata import Coordinata
from Entity.Pezzo import Pezzo
from Entity.Scacchiera import Scacchiera


class InterfacciaUtente:
    """."""

    def __init__(self):
        pass

    def display_coordinata(self, coord: Coordinata):
        """Stampa le coordinate in formato leggibile."""
        print(f"[x: {coord.x}, y: {coord.y}]\n")


    def display_pezzo(self, pezzo: Pezzo):
        """Stampa le informazioni sul pezzo."""
        print(f"\nCoordinata: {pezzo.init.x}, {pezzo.init.y}\n"
              f"movimento: {pezzo.primo}\n"
              f"simbolo: {'Bianco' if pezzo.colore else 'Nero'}\n"
            )
    
    def display_scacchiera(self, scacchiera: Scacchiera):
        """Disegna la scacchiera con i pezzi attualmente presenti."""
        griglia = [[" . " for _ in range(8)] for _ in range(8)]

        for coord, pezzo in scacchiera.pezzi_vivi.items():
            if pezzo is not None:
                x = coord.x - 1  # colonne da 0 a 7
                y = 8 - coord.y  # righe da 0 a 7 (inverso)
                griglia[y][x] = f" {pezzo.simbolo} "

        header = "   " + "".join(f" {chr(97 + i)}  " for i in range(8))
        print()
        print("  +" + "---+" * 8)

        for i, riga in enumerate(griglia):
            numero_riga = 8 - i
            print(f"{numero_riga} |" + "|".join(riga) + "|")
            print("  +" + "---+" * 8)

        print(header)
