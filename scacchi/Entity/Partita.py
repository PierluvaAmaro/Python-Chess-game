from sys import argv

from scacchi.Entity.Re import Re

from ..Boundary.InputUtente import InputUtente
from ..Boundary.InterfacciaUtente import InterfacciaUtente
from ..Control.ControlloPezzi import ControlloPezzi
from ..Utils import leggi_file, leggi_scacchiera
from .Scacchiera import Scacchiera


def saluta(ui: InterfacciaUtente):
    """Saluta i giocatori con un messaggio di benvenuto.
    
    Args:
        ui (InterfacciaUtente): L'istanza dell'interfaccia per la visualizzazione.
    
    """
    lines = leggi_file("ui/welcome.txt").splitlines()
    half = len(lines) // 2

    # Prima metà in rosso
    ui.imposta_stile("accent", "bright_white")
    for line in lines[:half]:
        ui.stampa(line)

    # Seconda metà in bianco (o nessun colore)
    ui.imposta_stile("accent", "cyan")
    for line in lines[half:]:
        ui.stampa(line)

class Partita:
    """CLASSE ENTITY: Gestisce la logica principale della partita a scacchi."""

    def __init__(self):
        """Inizializza: scacchiera, input utente, controllo dei vari pezzi, UI."""
        """Indica che la partita è in corso."""

        # scacchiera di base
        self.scacchiera = Scacchiera(leggi_scacchiera("ui/scacchiera.txt"))
        
        # variabili utilizzate per l'interazione con l'utente
        self.inputUtente = InputUtente()
        self.ui = InterfacciaUtente()

        # il controllo_pezzi gestisce tutti i pezzi della scacchiera
        self.controllo_pezzi = ControlloPezzi()
        
        # specificano se la partita e' gia' iniziata e se e' il turno del bianco.
        self.in_gioco = False
        self.turno_bianco = True

        # variabile temporanee
        self.nome1 = ""
        self.nome2 = ""

        # array di mosse
        self.mosse_bianco = []
        self.mosse_nero = []

    def reset(self):
        """Reimposta tutti i dati della partita per una nuova sessione."""
        self.scacchiera = Scacchiera(leggi_scacchiera("ui/scacchiera.txt"))
        self.in_gioco = False
        self.turno_bianco = True
        self.nome1 = ""
        self.nome2 = ""
        self.mosse_bianco = []
        self.mosse_nero = []

    def avvia(self):
        if self.in_gioco:
            self.ui.imposta_stile('accent', 'yellow')
            self.ui.stampa(self.ui.formatta_testo("Una partita è già in corso."))

            return

        self.in_gioco = True # la partita inizia ufficialmente

        while not self.nome1 or not self.nome2:
            self.nome1 = self.inputUtente.leggi("Inserisci nome giocatore bianco")
            self.nome2 = self.inputUtente.leggi("Inserisci nome giocatore nero")
            self.ui.stampa_scacchiera(self.scacchiera)

        while True:
            nome = self.nome1 if self.turno_bianco else self.nome2
            colore = "white" if self.turno_bianco else "black"

            self.ui.imposta_stile('accent', colore)
            stringa = self.inputUtente.leggi(f"\n{self.ui.formatta_testo(nome)} - "\
                                             f"Inserisci mossa (es. 'e4')")

            if stringa.startswith("/"):
                risultato = self.inputUtente.in_ascolto(stringa)
                esito = self.processa(risultato)

                if esito == "fine":
                    break  # partita iniziale
                continue
            
            try:
                mossa = self.inputUtente.parser.parse_mossa(stringa, self.turno_bianco)
                pezzo = self.controllo_pezzi.trova_pezzo(self.scacchiera,
                    mossa["finale"], self.turno_bianco, mossa["simbolo"])

                # 1. Controlla se il proprio re è sotto scacco
                re = next((p for p in self.scacchiera.pezzi_vivi.values()
                        if isinstance(p, Re) and p.colore == self.turno_bianco), None)
                if (
                    re
                    and self.controllo_pezzi.scacco(re, re.iniziale, self.scacchiera)
                    and not self.controllo_pezzi.mossa_elimina_scacco(
                        self.scacchiera, pezzo, mossa["finale"]
                    )
                ):
                    raise ValueError(
                        "Il tuo re è sotto scacco: puoi solo fare una mossa che "
                        "elimina lo scacco!"
                    )

                # 3. Verifica se la mossa mette il re avversario sotto scacco
                scacco_avv = self.controllo_pezzi.scacco(pezzo, mossa["finale"],
                self.scacchiera)
                if not mossa.get("scacco") and scacco_avv:
                    raise ValueError("Hai messo il re avversario sotto scacco ma non"\
                    "hai dichiarato '+'. Devi specificare '+' nella"\
                    "notazione della mossa.")
                if mossa.get("scacco") and not scacco_avv:
                    raise ValueError("Hai dichiarato scacco (+) ma la mossa non mette"\
                    "il re avversario sotto scacco.")

                # movimento reale
                if self.controllo_pezzi.muovi(mossa["cattura"], self.scacchiera, pezzo,
                mossa["finale"]):
                    self.turno_bianco = not self.turno_bianco

                if pezzo.primo:
                    pezzo.primo = False

                self.ui.stampa_scacchiera(self.scacchiera)
            except Exception as e:
                print(e)
                    
        self.in_gioco = False

    def verifica(self):
        """Controlla se l'input inserito è un comando."""
        # Processa l'input da linea di comando
        if len(argv) > 1 and argv[1] in ("--help", "-h"):
            saluta(self.ui)
            self.ui.stampa_file("ui/help.txt")
        elif len(argv) > 1 and argv[1] not in ("--help", "-h"):
            self.ui.imposta_stile('accent', 'red')
            self.ui.stampa(self.ui.formatta_testo("Comando non valido."))
            exit()
        else:
            saluta(self.ui)
        
        while True:
            risultato = self.inputUtente.in_ascolto(self.inputUtente.leggi("Inserisci"))
            self.processa(risultato)

    def processa(self, risultato):
        """Esegue il comando in input.

        Args:
            risultato (int): Rappresenta il comando da eseguire.

        """
        match risultato:
            case 1:  # gioca
                self.avvia()
            case 2:
                if not self.in_gioco:
                    self.ui.imposta_stile('accent', 'red')
                    self.ui.stampa(self.ui.formatta_testo("Non è in corso nessuna "\
                                                       "partita."))
                        
                    self.ui.imposta_stile('accent', 'white')
                    self.ui.stampa(self.ui.formatta_testo("Inserisci comando /gioca"))
                        
                else:
                    self.ui.stampa_scacchiera(self.scacchiera)
                    return "continua"
                    
            case 3:
                self.ui.stampa_file("ui/help.txt")
                return None if not self.in_gioco else "continua"
            
            case 4:
                if self.in_gioco:
                    for i, mossa_b in enumerate(self.mosse_bianco):
                        mossa_n = self.mosse_nero[i] if i < len(self.mosse_nero) else ""
                        riga = f"{i+1}: {mossa_b}" if not mossa_n else f"{i+1}:"\
                               f"{mossa_b} {mossa_n}"
                        
                        self.ui.imposta_stile("accent", "white")
                        self.ui.stampa(self.ui.formatta_testo(riga))
                else:
                    self.ui.imposta_stile('accent', 'red')
                    self.ui.stampa(self.ui.formatta_testo("Non è in corso nessuna" \
                                                       "partita."))
                    
                    self.ui.imposta_stile('accent', 'white')
                    self.ui.stampa(self.ui.formatta_testo("Inserisci comando /gioca"))
            case 5:
                if self.in_gioco:
                        risposta = self.inputUtente.leggi("Accetti la patta (s/n)")
                        
                        if risposta.lower() == "s":
                            self.ui.imposta_stile('accent', 'green')
                            self.ui.stampa(self.ui.formatta_testo("Partita finita per "\
                                            "patta"))
                            self.reset()

                            return "fine"
                        
                        elif risposta.lower() == "n":
                            self.ui.imposta_stile('accent', 'yellow')
                            self.ui.stampa(self.ui.formatta_testo("Patta annullata."))
                            
                            return "continua"
                else:
                    self.ui.imposta_stile('accent', 'red')
                    self.ui.stampa(self.ui.formatta_testo("Non è in corso nessuna "\
                                                       "partita."))
            case 6:
                if self.in_gioco:
                    while True:
                        risposta = self.inputUtente.leggi("Vuoi davvero abbandonare?" \
                                                          "(s/n)")
                        if risposta.lower() == "s":
                            vincitore = self.nome2 if self.turno_bianco else self.nome1

                            self.ui.imposta_stile('accent', 'green')
                            self.ui.stampa(
                                self.ui.formatta_testo(f"{vincitore} ha vinto"\
                                                    "per abbandono."))
                            
                            self.reset()  # resetta la partita
                            return "fine"
                        
                        elif risposta.lower() == "n":
                            self.ui.imposta_stile('accent', 'red')
                            self.ui.stampa(
                                self.ui.formatta_testo("Abbandono annullato.")
                            )
                            
                            return "continua"
                        
                        else:
                            self.ui.imposta_stile('accent', 'white')
                            self.ui.imposta_stile('italic', True)
                            self.ui.stampa(
                                self.ui.formatta_testo("Inserisci una risposta"\
                                                               " valida (s/n).")
                            )
                else:
                    self.ui.imposta_stile('accent', 'red')
                    self.ui.stampa(
                        self.ui.formatta_testo("Non puoi abbandonare, non è in"\
                                                       " corso nessuna partita.")
                    )
                        
            case 7:
                while True:
                    risposta = self.inputUtente.leggi("Vuoi davvero uscire? (s/n)")
                    if risposta.lower() == "s":
                        self.ui.imposta_stile('accent', 'yellow')
                        self.ui.stampa(self.ui.formatta_testo("Uscita in corso..."))
                        exit(0)

                    elif risposta.lower() == "n":
                        self.ui.imposta_stile('accent', 'green')
                        self.ui.stampa(self.ui.formatta_testo("Uscita annullata."))
                        
                        return "continua"
                    else:
                        self.ui.imposta_stile('accent', 'white')
                        self.ui.imposta_stile('italic', True)
                        self.ui.stampa(self.ui.formatta_testo("Inserisci una risposta"\
                                                           "valida (s/n)."))