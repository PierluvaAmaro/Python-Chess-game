from sys import argv

from ..Boundary.InputUtente import InputUtente
from ..Boundary.InterfacciaUtente import UI
from ..Control.PieceControl import PieceControl
from ..Control.Utils import leggi_scacchiera
from .Scacchiera import Scacchiera


class Partita:
    """Gestisce la logica principale della partita a scacchi."""

    def __init__(self):
        """Inizializza la schacchiera, l'input utente, il controllo pezzi, l'UI e viene indicato che la partita è in corso con in.gioco.
        
        """
        self.scacchiera = Scacchiera(leggi_scacchiera("scacchiera.txt"))
        self.inputUtente = InputUtente()
        self.pieceControl = PieceControl()
        self.ui = UI()
        self.in_gioco = False
        
    def run(self):
        """Inizia una nuova partita.

        """
        if self.in_gioco:
            self.ui.stampa("Una partita è già in corso.", accent="yellow")
            return

        self.in_gioco = True

        nome1 = ""
        nome2 = ""

        while not nome1 or not nome2:
            nome1 = input("Inserisci nome giocatore bianco: ")
            nome2 = input("Inserisci nome giocatore nero: ")

        turno_bianco = True
        while True:
            nome = nome1 if turno_bianco else nome2
            colore = "white" if nome == nome1 else "black"

            self.ui.set_style('accent', f"{colore}")
            messaggio = f"{self.ui.format_text(nome)} - Inserisci mossa (es. e4):"
            self.ui.console.print(messaggio)

            stringa = self.inputUtente.leggi()
            if stringa.startswith("/"):
                risultato = self.inputUtente.listen(stringa)
                if risultato in [5, 6]:
                    self.process(risultato)
                    break
                else:
                    self.process(risultato)
                    continue
            else:
                coord = self.inputUtente.parser.parse_mossa(stringa)
                pezzo = self.pieceControl.find_piece(self.scacchiera, coord, colore == "white")
                if pezzo:
                    self.pieceControl.muovi(self.scacchiera, pezzo, coord)
                    turno_bianco = not turno_bianco

        self.in_gioco = False

    def check(self):
        """Controlla i comandi inseriti.
        
        """
        # Processa l'input da linea di comando solo una volta
        if len(argv) > 1 and argv[1] in ("--help", "-h"):
            self.ui.display_help("help.txt")

        while True:
            risultato = self.inputUtente.listen(
                self.inputUtente.leggi("Inserisci: ")
            )
            self.process(risultato)

    def process(self, risultato):
        """Esegue il comando inserito
            
            Args:
            risultato (int): indica il comando da eseguire.
        
        """
        match risultato:
            case 1: # gioca
                self.run()
            case 2: # mostra scacchiera
                self.ui.display_scacchiera(self.scacchiera)
            case 3: # mostra help
                print("help")
                pass
            case 4:
                print("mosse")
            case 5:
                print("patta")
            case 6:
                print("abbandona")
            case 7:
                print("esci")
                exit(0)

            case None:
                print("Input non riconosciuto.")
            case _:
                raise NotImplementedError("Stato sconosciuto.")
