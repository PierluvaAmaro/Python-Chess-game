from Core.Coordinata import Coordinata
from Pezzi.Pezzo import Pezzo


class Scacchiera:
    """Rappresenta l'insieme dei pezzi vivi non catturati nella partita."""
    
    def __init__(self, pezzi_vivi: dict[Coordinata, Pezzo]):
        self.pezzi_vivi = pezzi_vivi

    def check_position(self, pezzo: Pezzo, final: Coordinata):
        if not pezzo.check_move(final):
            return False
        
        # verifica se il pezzo e' ancora in gioco
        if pezzo not in self.pezzi_vivi.values():
            return False

        # verifica se la posizione final e' la stessa di partenza
        if (pezzo.init.x == final.x and pezzo.init.y == final.y
            and pezzo.final.x == final.x and pezzo.final.y == final.y
        ):
            return False
        
        # verifica se la posizione e' occupata
        if final in self.pezzi_vivi:
            altro = self.pezzi_vivi[final]
            if altro.colore == pezzo.colore:
                return False
            else:
                self.pezzi_vivi.pop(final)

        old = pezzo.init
        pezzo.init = final

        self.pezzi_vivi[final] = pezzo
        self.pezzi_vivi.pop(old)

        print("Posizione finale del pezzo: " + str(pezzo.init.x) 
              + " : " + str(pezzo.init.y))
        return True
    
    def draw(self):
        # Pulisce lo schermo
        print("\033[2J", end="")

         # Crea matrice vuota
        griglia = [[" . " for _ in range(8)] for _ in range(8)]

        # Inserisce i pezzi nella matrice
        for coord, pezzo in self.pezzi_vivi.items():
            x = coord.x - 1  # colonna da 0 a 7
            y = 8 - coord.y  # riga da 0 (in alto) a 7 (in basso)
            griglia[y][x] = f" {pezzo.id} "

        # Stampa la griglia con le etichette
        for riga in range(8):
            print(f"{8 - riga} ", end="")  # numeri da 8 a 1
            for cella in griglia[riga]:
                print(cella, end="")
            print()

        # Colonne (a-h)
        print("  ", end="")
        for c in range(8):
            print(f" {chr(ord('a') + c)} ", end="")
        print()