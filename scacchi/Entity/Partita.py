from sys import argv

from ..Boundary.InputUtente import InputUtente
from ..Boundary.InterfacciaUtente import UI
from ..Control.PieceControl import PieceControl
from ..Control.Utils import leggi_scacchiera
from .Scacchiera import Scacchiera


def say_hello(ui: UI):
    """Saluta i giocatori."""
    ui.set_style("accent", "cyan")
    benvenuto = ui.format_text("Benvenuto")
    ui.set_style("accent", "magenta")
    
    gruppo = ui.format_text("gruppo Milner")
    ui.set_style("accent", "yellow")
    
    istruzioni = ui.format_text("Inserisci un comando tra quelli disponibili,")
    ui.set_style("accent", "green")
    
    help_hint = ui.format_text("/help")
    messaggio = (
            f"{benvenuto} nel gioco degli scacchi del {gruppo}!\n"
            f"{istruzioni} o usa {help_hint} per vedere la lista dei comandi."
    )
    
    ui.stampa(messaggio)

class Partita:
    """CLASSE ENTITY: Gestisce la logica principale della partita a scacchi."""

    def __init__(self):
        """Inizializza: scacchiera, input utente, controllo dei vari pezzi, UI."""
        """Indica che la partita è in corso."""

        # scacchiera di base
        self.scacchiera = Scacchiera(leggi_scacchiera("scacchiera.txt"))
        
        # variabili utilizzate per l'interazione con l'utente
        self.inputUtente = InputUtente()
        self.ui = UI()

        # il pieceControl gestisce tutti i pezzi della scacchiera
        self.pieceControl = PieceControl()
        
        # specificano se la partita e' gia' iniziata e se e' il turno del bianco.
        self.in_gioco = False
        self.turno_bianco = True

        # variabile temporanee
        self.nome1 = ""
        self.nome2 = ""

        # array di mosse
        self.mosse_bianco=[]
        self.mosse_nero=[]

    def reset(self):
        """Reimposta tutti i dati della partita per una nuova sessione."""
        self.scacchiera = Scacchiera(leggi_scacchiera("scacchiera.txt"))
        self.in_gioco = False
        self.turno_bianco = True
        self.nome1 = ""
        self.nome2 = ""
        self.mosse_bianco=[]
        self.mosse_nero=[]

    def run(self):
        if self.in_gioco:
            self.ui.set_style('accent', 'yellow')
            self.ui.stampa(self.ui.format_text("Una partita è già in corso."))

            return

        self.in_gioco = True # la partita inizia ufficialmente

        while not self.nome1 or not self.nome2:
            self.nome1 = self.inputUtente.leggi("Inserisci nome giocatore bianco")
            self.nome2 = self.inputUtente.leggi("Inserisci nome giocatore nero")
            self.ui.display_scacchiera(self.scacchiera)

        while True:
            nome = self.nome1 if self.turno_bianco else self.nome2
            colore = "white" if self.turno_bianco else "black"

            self.ui.set_style('accent', colore)
            stringa = self.inputUtente.leggi(f"\n{self.ui.format_text(nome)} - "\
                                             f"Inserisci mossa (es. 'e4')")

            if stringa.startswith("/"):
                risultato = self.inputUtente.listen(stringa)
                esito = self.process(risultato)

                if esito == "fine":
                    break  # partita finita
                continue

            try:
                simbolo, coord = self.inputUtente.parser.parse_mossa(
                    stringa, bool(not self.turno_bianco))
                pezzo = self.pieceControl.find_piece(
                    self.scacchiera, coord, self.turno_bianco, simbolo
                )
                
                # se il pezzo esiste e il movimento va a buon fine
                if pezzo:
                    if self.pieceControl.muovi(self.scacchiera, pezzo, coord):
                        # se e' il turno del bianco
                        if self.turno_bianco:
                            # inserisce l'ultima mossa del bianco nel suo array
                            self.mosse_bianco.append(stringa)
                        else: # altrimenti...
                            # ...
                            self.mosse_nero.append(stringa)

                        # cambio turno e stampa della scacchiera
                        self.turno_bianco = not self.turno_bianco
                    self.ui.display_scacchiera(self.scacchiera)
            except ValueError as e:
                self.ui.set_style("accent", "red")
                self.ui.stampa(self.ui.format_text(f"Errore: {e}. Riprova."))
                
        self.in_gioco = False

    def check(self):
        """Controlla se l'input inserito è un comando."""
        # Processa l'input da linea di comando
        if len(argv) > 1 and argv[1] in ("--help", "-h"):
            say_hello(self.ui)
            self.ui.display_help("help.txt")
        elif len(argv) > 1 and argv[1] not in ("--help", "-h"):
            self.ui.set_style('accent', 'red')
            self.ui.stampa(self.ui.format_text("Comando non valido."))
            exit()
        else:
            say_hello(self.ui)
        
        while True:
            risultato = self.inputUtente.listen(self.inputUtente.leggi("Inserisci"))
            self.process(risultato)

    def process(self, risultato):
        """Esegue il comando in input.

        Args:
            risultato (int): Rappresenta il comando da eseguire.

        """
        match risultato:
            case 1:  # gioca
                self.run()
            case 2:
                if not self.in_gioco:
                    self.ui.set_style('accent', 'red')
                    self.ui.stampa(self.ui.format_text("Non è in corso nessuna"\
                                                       "partita."))
                        
                    self.ui.set_style('accent', 'white')
                    self.ui.stampa(self.ui.format_text("Inserisci comando /gioca"))
                        
                else:
                    self.ui.display_scacchiera(self.scacchiera)
                    return "continua"
                    
            case 3:
                self.ui.display_help("help.txt")
                return None if not self.in_gioco else "continua"
            
            case 4:
                if self.in_gioco:
                    for i, mossa_b in enumerate(self.mosse_bianco):
                        mossa_n = self.mosse_nero[i] if i < len(self.mosse_nero) else ""
                        riga = f"{i+1}: {mossa_b}" if not mossa_n else f"{i+1}:"\
                               f"{mossa_b} {mossa_n}"
                        
                        self.ui.set_style("accent", "white")
                        self.ui.stampa(self.ui.format_text(riga))
                else:
                    self.ui.set_style('accent', 'red')
                    self.ui.stampa(self.ui.format_text("Non è in corso nessuna" \
                                                       "partita."))
                    
                    self.ui.set_style('accent', 'white')
                    self.ui.stampa(self.ui.format_text("Inserisci comando /gioca"))
            case 5:
                if self.in_gioco:
                        risposta = self.inputUtente.leggi("Accetti la patta (s/n)")
                        
                        if risposta.lower() == "s":
                            self.ui.set_style('accent', 'green')
                            self.ui.stampa(self.ui.format_text("Partita finita per " \
                                            "patta"))
                            self.reset()

                            return "fine"
                        
                        elif risposta.lower() == "n":
                            self.ui.set_style('accent', 'yellow')
                            self.ui.stampa(self.ui.format_text("Patta annullata."))
                            
                            return "continua"
                else:
                    self.ui.set_style('accent', 'red')
                    self.ui.stampa(self.ui.format_text("Non è in corso nessuna "\
                                                       "partita."))
            case 6:
                if self.in_gioco:
                    while True:
                        risposta = self.inputUtente.leggi("Vuoi davvero abbandonare?" \
                                                          "(s/n)")
                        if risposta.lower() == "s":
                            vincitore = self.nome2 if self.turno_bianco else self.nome1

                            self.ui.set_style('accent', 'green')
                            self.ui.stampa(self.ui.format_text(f"{vincitore} ha vinto "\
                                                               "per abbandono."))
                            
                            self.reset()  # resetta la partita
                            return "fine"
                        
                        elif risposta.lower() == "n":
                            self.ui.set_style('accent', 'red')
                            self.ui.stampa(self.ui.format_text("Abbandono annullato."))
                            
                            return "continua"
                        
                        else:
                            self.ui.set_style('accent', 'white')
                            self.ui.set_style('italic', True)
                            self.ui.stampa(self.ui.format_text("Inserisci una risposta"\
                                                               " valida (s/n)."))
                else:
                    self.ui.set_style('accent', 'red')
                    self.ui.stampa(self.ui.format_text("Non puoi abbandonare, non è in"\
                                                       "corso nessuna partita."))
                        
            case 7:
                while True:
                    risposta = self.inputUtente.leggi("Vuoi davvero uscire? (s/n)")
                    if risposta.lower() == "s":
                        self.ui.set_style('accent', 'yellow')
                        self.ui.stampa(self.ui.format_text("Uscita in corso..."))
                        exit(0)

                    elif risposta.lower() == "n":
                        self.ui.set_style('accent', 'green')
                        self.ui.stampa(self.ui.format_text("Uscita annullata."))
                        
                        return "continua"
                    else:
                        self.ui.set_style('accent', 'white')
                        self.ui.set_style('italic', True)
                        self.ui.stampa(self.ui.format_text("Inserisci una risposta"\
                                                           "valida (s/n)."))
            case _:
                raise NotImplementedError("Inputsconosciuto.")
