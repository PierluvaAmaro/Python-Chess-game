from Core.Coordinata import Coordinata
from Pezzi.Pezzo import Pezzo


class Scacchiera:
    """Rappresenta lo stato della scacchiera e gestisce le operazioni sui Pezzi."""

    def __init__(self, pezzi_vivi: dict[Coordinata, Pezzo]):
        """Inizializza la scacchiera con i pezzi forniti.
        
        Args:
            pezzi_vivi (dict[Coordinata, Pezzo]): Dizionario contenente i pezzi attivi.

        """
        self.pezzi_vivi = pezzi_vivi

    def draw(self):
        """Disegna la scacchiera con i pezzi attualmente presenti."""
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
        """Trova il pezzo del colore specificato che puo' muoversi alla coordinata.
        
        Args:
            final (Coordinata): Coordinata di destinazione del pezzo.
            colore (bool): Colore del pezzo da cercare.

        Returns:
            Pezzo: Il primo pezzo valido che puo' effettuare la mossa, se trovato.
        
        """
        for _, piece in self.pezzi_vivi.items():
            if piece is not None and piece.colore == colore and piece.check_move(final):
                return piece
        
        print("Nessun tuo pezzo puo' effettuare quella mossa.")
        return None

    def muovi(self, pezzo: Pezzo, final: Coordinata) -> bool:
        """Esegue lo spostamento di un pezzo se la destinazione non e' occupata.
        
        Args:
            pezzo (Pezzo): Il pezzo da muovere.
            final (Coordinata): La destinazione del pezzo.

        Returns:
            bool: True se la mossa e' stata effettuata con successo, False altrimenti.
        
        """
        if not self.is_occupied(final):
            self.pezzi_vivi.pop(pezzo.init)
            pezzo.init = final
            self.pezzi_vivi[final] = pezzo
            return True
        
        return False

    def is_occupied(self, final: Coordinata) -> bool:
        """Verifica se una casella e' occupata da un pezzo.

        Args:
            final (Coordinata): Coordinata da controllare.

        Returns:
            bool: True se la casella e' occupata, False altrimenti.

        """ 
        if final in self.pezzi_vivi:
            print("Posizione occupata.")
            return True
        return False