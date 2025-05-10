from Core.Coordinata import Coordinata
from Pezzi.Pedone import Pedone
from Pezzi.Pezzo import Pezzo


def crea_pezzo(simbolo: str, id: Coordinata, colore: int):
    """Funzione che permette di generare un pezzo.

    Il pezzo viene generato da simbolo e dalla sua Coordinata iniziale
    """
    match simbolo:
        case "♟":
            return Pedone("♟", id, colore)

        case _:
            raise ValueError(f"Pezzo non conosciuto: {simbolo}")

def leggi_scacchiera(file="scacchiera.txt"):
    """Funzione che restituisce un dizionario Coordinata->Pezzo."""
    scacchiera = {}

    with open(file) as f:
        righe = [line.strip() for line in f.readlines() if line.strip()]

    if len(righe) != 8:
        raise ValueError(f"File non valido: le righe devono essere 8 ma sono: "
                         f"{len.righe}"
                        )
    
    for y_riga, riga in enumerate(righe):
        y = 8 - y_riga

        if len(riga) != 8:
            raise ValueError(f"File non valido: le colonne devono essere 8 ma sono"
                             f"{len(riga)}"
                            )

        for x_col, simbolo in enumerate(riga):
            if simbolo != ".":
                x = x_col + 1

                coord = Coordinata(x, y)
                if y == 2 or y == 1:
                    colore = 1  # Pedoni bianchi (turno 1)
                elif y == 7 or y == 8:
                    colore = 0  # Pedoni neri (turno -1)

                pezzo = crea_pezzo(simbolo, coord, colore)
                scacchiera[coord] = pezzo

    return scacchiera

class Scacchiera:
    """CLasse che rappresenta un dizionari di pezzi.
    
    Rappresenta un dizionari con i pezzi non catturati come matrice 8x8 
    """

    def __init__(self, pezzi_vivi: dict[Coordinata, Pezzo]):
        self.pezzi_vivi = pezzi_vivi

    def draw(self):
        """Disegna la scacchiera con i pezzi vivi."""
        griglia = [[" . " for _ in range(8)] for _ in range(8)]

        for coord, pezzo in self.pezzi_vivi.items():
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

    def find_piece(self, final: Coordinata, colore: bool) -> Pezzo:
        # il primo pezzo che puo fare una determinata mossa la fa, per ora.
        for _, piece in self.pezzi_vivi.items():
            if piece is not None and piece.check_move(final) and piece.colore == colore:
                piece.print()
                return piece

    def muovi(self, pezzo: Pezzo, final: Coordinata) -> bool:
        if not self.is_occupied(final):
            self.pezzi_vivi.pop(pezzo.init)
            pezzo.init = final
            self.pezzi_vivi[final] = pezzo
            return True
        
        return False

    def is_occupied(self, final: Coordinata) -> bool:
        return final in self.pezzi_vivi