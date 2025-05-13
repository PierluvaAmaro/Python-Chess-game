from sys import argv

from ..Boundary.InputUtente import InputUtente
from ..Boundary.InterfacciaUtente import UI
from ..Control.PieceControl import PieceControl
from ..Control.Utils import leggi_scacchiera
from .Scacchiera import Scacchiera


class Partita:
    """CLASSE ENTITY."""

    """Gestisce la logica principale della partita a scacchi."""

    def __init__(self):
        """Inizializza: scacchiera, input utente, controllo dei vari pezzi, UI."""
        """Indica che la partita è in corso."""
        self.scacchiera = Scacchiera(leggi_scacchiera("scacchiera.txt"))
        self.inputUtente = InputUtente()
        self.pieceControl = PieceControl()
        self.ui = UI()
        self.in_gioco = False
        self.turno_bianco = True
        self.nome1 = ""
        self.nome2 = ""

    def reset(self):
        """Reimposta tutti i dati della partita per una nuova sessione."""
        self.scacchiera = Scacchiera(leggi_scacchiera("scacchiera.txt"))
        self.in_gioco = False
        self.turno_bianco = True
        self.nome1 = ""
        self.nome2 = ""

        
    def run(self):
        if self.in_gioco:
            self.ui.stampa("Una partita è già in corso.", accent="yellow")
            return
    
        self.in_gioco = True

        while not self.nome1 or not self.nome2:
            self.nome1 = input("Inserisci nome giocatore bianco: ")
            self.nome2 = input("Inserisci nome giocatore nero: ")

        while True:
            nome = self.nome1 if self.turno_bianco else self.nome2
            colore = "white" if self.turno_bianco else "black"

            self.ui.set_style('accent', colore)
            messaggio = f"{self.ui.format_text(nome)} - Inserisci mossa (es. e4):"
            self.ui.console.print(messaggio)

            stringa = self.inputUtente.leggi()
            if stringa.startswith("/"):
                risultato = self.inputUtente.listen(stringa)
                esito = self.process(risultato)

                if esito == "fine":
                    break  # partita finita
                elif esito == "continua":
                    continue  # turno non cambiato, stesso giocatore riprova
                else:
                    continue  # altri comandi, si continua
            else:
                coord = self.inputUtente.parser.parse_mossa(stringa)
                pezzo = self.pieceControl.find_piece(self.scacchiera, coord, self.turno_bianco)  # noqa: E501
                if pezzo:
                    self.pieceControl.muovi(self.scacchiera, pezzo, coord)
                    self.turno_bianco = not self.turno_bianco

        self.in_gioco = False

    def check(self):
        """Controlla se l'input inserito è un comando."""
        # Processa l'input da linea di comando solo una volta
        if len(argv) > 1 and argv[1] in ("--help", "-h"):
            self.ui.display_help("help.txt")

        while True:
            risultato = self.inputUtente.listen(
                self.inputUtente.leggi("Inserisci: ")
            )
            self.process(risultato)

    def process(self, risultato):
        """Esegue il comando in input.

        Args:
        risultato (int): Rappresenta il comando da eseguire.

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
                while True:
                    if(self.in_gioco):
                        risposta = input("Vuoi davvero abbandonare? (s/n): ")
                        if risposta.lower() == "s":
                            vincitore = self.nome2 if self.turno_bianco else self.nome1
                            print(f"{vincitore} ha vinto per abbandono.")
                            self.reset()  # resetta la partita
                            return "fine"
                        elif risposta.lower() == "n":
                            print("Abbandono annullato.")
                            return "continua"
                        else:
                            print("Inserisci una risposta valida (s/n).")
                    else:
                        print("Non puoi abbandonare, non è in corso nessuna partita.")
                        break
            case 7:
                while True:
                    risposta = input("Vuoi davvero uscire? (s/n): ")
                    if risposta.lower() == "s":
                        print("Uscita in corso...")
                        exit(0)
                    elif risposta.lower() == "n":
                        print("Uscita annullata.")
                        return "continua"
                    else:
                        print("Inserisci una risposta valida (s/n).")
            case None:
                print("Input non riconosciuto.")
            case _:
                raise NotImplementedError("Stato sconosciuto.")
