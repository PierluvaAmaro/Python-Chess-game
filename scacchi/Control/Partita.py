from sys import argv

from scacchi.Entity.Coordinata import Coordinata
from scacchi.Entity.Pedone import Pedone
from scacchi.Entity.Re import Re

from ..Boundary.InputUtente import InputUtente
from ..Boundary.InterfacciaUtente import InterfacciaUtente
from ..Entity.Scacchiera import Scacchiera
from ..Utility.Utils import leggi_file, leggi_scacchiera
from .ControlloPezzi import ControlloPezzi


def saluta(ui: InterfacciaUtente):
    """Mostra il messaggio di benvenuto con formattazione a colori.
    
    Divide il messaggio di benvenuto in due parti, mostrandole con stili diversi
    per un effetto visivo accattivante.
    
    Args:
        ui (InterfacciaUtente): Interfaccia utente configurata per la visualizzazione.
    
    Example:
        >>> ui = InterfacciaUtente()
        >>> saluta(ui)
        [Mostra il messaggio di benvenuto formattato]

    """
    try:
        contenuto = leggi_file("ui/welcome.txt")
        if not contenuto:
            ui.stampa("Benvenuto al gioco degli scacchi!", "bright_white")
            return
        
        linee = contenuto.splitlines()
        meta = len(linee) // 2
        
        # prima meta'
        ui.imposta_stile("accent", "bright_white")
        for linea in linee[:meta]:
            ui.stampa(linea)
            
        # seconda meta'
        ui.imposta_stile("accent", "cyan")
        for linea in linee[meta:]:
            ui.stampa(linea)
            
    except FileNotFoundError:
        ui.stampa("Benvenuto al gioco degli scacchi!", "bright_white")
        ui.stampa("Versione 2.0 (Sprint 2)", "cyan")

class Partita:
    """Classe Control per gestire lo stato e la logica principale di una partita.
    
    Attributes:
        scacchiera (Scacchiera): Lo stato attuale della scacchiera.
        input_utente (InputUtente): Gestore dell'input dei giocatori.
        ui (InterfacciaUtente): Gestore dell'interfaccia grafica.
        controllo_pezzi (ControlloPezzi): Gestore delle regole dei pezzi.
        
        in_gioco (bool): Flag che indica se la partita e' attiva.
        turno_bianco (bool): Flag che indica il turno corrente (True = bianco)
        
        nome1 (str): Nome del giocatore bianco
        nome2 (str): Nome del giocatore nero
        
        mosse_bianco (list): Cronologia delle mosse del giocatore bianco
        mosse_nero (list): Cronologia delle mosse del giocatore nero
 
    """

    def __init__(self):
        """Inizializza una nuova partita con stato iniziale."""
        # scacchiera di base
        self.scacchiera = Scacchiera(leggi_scacchiera("ui/scacchiera.txt"))
        
        # variabili utilizzate per l'interazione con l'utente
        self.input_utente = InputUtente()
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
        """Reimposta la partita allo stato iniziale.
        
        Ricrea:
        - Una nuova scacchiera con pezzi nella posizione iniziale
        - Resetta lo stato del gioco
        - Pulisce la cronologia delle mosse
        - Cancella i nomi dei giocatori
        """
        self.scacchiera = Scacchiera(leggi_scacchiera("ui/scacchiera.txt"))
        self.in_gioco = False
        self.turno_bianco = True
        self.nome1 = ""
        self.nome2 = ""
        self.mosse_bianco = []
        self.mosse_nero = []

    def avvia(self):
        """Metodo principale che gestisce tutto il loop del gioco."""
        self.reset()
        if self.in_gioco:
            self.ui.imposta_stile("accent", "yellow")
            self.ui.stampa(self.ui.formatta_testo("Una partita e' gia' in corso!"))
            return

        self.in_gioco = True
        
        while not self.nome1 or not self.nome2:
            self.nome1 = self.input_utente.leggi("Inserisci nome giocatore bianco")
            self.nome2 = self.input_utente.leggi("Inserisci nome giocatore nero")
            self.ui.stampa_scacchiera(self.scacchiera)

        while self.in_gioco:
                       
            nome = self.nome1 if self.turno_bianco else self.nome2
            colore = "white" if self.turno_bianco else "black"

            self.ui.imposta_stile('accent', colore)
            stringa = self.input_utente.leggi(f"\n{self.ui.formatta_testo(nome)} - "\
                                             f"Inserisci mossa (es. 'e4')")

            if stringa.startswith("/"):
                risultato = self.input_utente.in_ascolto(stringa)
                esito = self.processa(risultato)

                if esito == "fine":
                    break  # partita iniziale
                continue
            
            try:
                pezzi = []
                mossa = self.input_utente.parser.parse_mossa(stringa, self.turno_bianco)

                if mossa.get("tipo") == "arrocco":
                    self.controllo_pezzi.esegui_arrocco(
                        self.scacchiera, self.turno_bianco, mossa["lato"]
                    )
                else:
                    while True:
                        pezzi = self.controllo_pezzi.trova_pezzo(
                            self.scacchiera,
                            mossa["iniziale"],
                            mossa["finale"],
                            self.turno_bianco,
                            mossa["simbolo"],
                            mossa.get("en_passant", False)
                        )
                        if not pezzi:
                            raise ValueError("Nessun pezzo valido per questa mossa")
                        if isinstance(pezzi, list):
                            if len(pezzi) > 1:
                                self.ui.stampa("Mossa ambigua: specifica anche la colonna di partenza (es: Cbe2 o exd5).")
                                break  # Esce dal ciclo simulando il comportamento do-while
                            pezzo = pezzi[0]
                            #Se il pedone arriva in promozione senza che sia 
                            #specicata la promozione
                            if(
                                isinstance(pezzo, Pedone)
                                and mossa["finale"].y in (1,8)
                                and not mossa.get("promozione")
                            ):
                                raise ValueError(
                                    "Devi specificare la promozione per il pedone"
                                    "(es: e8=D)"
                                )
                        else:
                            pezzo = pezzi
                        if self.controllo_pezzi.re_in_scacco(self.scacchiera, self.turno_bianco):
                            if not self.controllo_pezzi.mossa_elimina_scacco(
                                self.scacchiera, pezzo, mossa["finale"]
                            ):
                                raise ValueError(
                                    "Mossa non valida: il re sarebbe in scacco dopo la mossa!"
                                )
                        break
                
                    simulazione = self.controllo_pezzi.simula(
                        self.scacchiera, pezzo, mossa["finale"]
                    )
                    if simulazione is None:
                        raise ValueError("Mossa non valida")

                    pedone_sim = simulazione.pezzi_vivi.get(mossa["finale"])
                    if pedone_sim is None:
                        raise ValueError("Pedone non trovato nella simulazione")
                        
                    colore_re_avversario = not pezzo.colore
                    re_avversario = next(
                        (
                            p
                            for p in simulazione.pezzi_vivi.values()
                            if isinstance(p, Re) and p.colore == colore_re_avversario
                        ),
                        None,
                    )
                    if re_avversario is None:
                        raise ValueError("Re avversario non trovato")

                    is_scacco = self.controllo_pezzi.scacco(simulazione, pezzo)
                    is_matto = self.controllo_pezzi.scacco_matto(
                        self.scacchiera, pezzo, mossa["finale"]
                    )

                    if mossa.get("matto"):
                        if not is_matto:
                            raise ValueError(
                                "Hai dichiarato scacco matto (#), ma la mossa"
                                "non mette il re avversario sotto scacco matto."
                            )
                    else:
                        if is_matto:
                            raise ValueError(
                                "Hai messo il re avversario sotto scacco"
                                "matto ma non lo hai dichiarato."
                            )
                        if not mossa.get("scacco") and is_scacco:
                            raise ValueError(
                                "Hai messo il re avversario sotto scacco ma"
                                "non lo hai dichiarato (+)."
                            )
                        if mossa.get("scacco") and not is_scacco:
                            raise ValueError(
                                "Hai dichiarato scacco (+) ma la mossa non"
                                "mette il re avversario sotto scacco."
                            )

                    self.controllo_pezzi.muovi(
                        mossa["cattura"], self.scacchiera, pezzo, mossa["finale"], mossa.get("en_passant", False)
                    )
                    if pezzo.primo:
                        pezzo.primo = False

                    if mossa.get("en_passant"):
                        x_catturato = mossa["finale"].x
                        y_catturato = mossa["finale"].y
                        coord_catturato = Coordinata(x_catturato, y_catturato - 1 if self.turno_bianco else y_catturato + 1)
                        if coord_catturato in self.scacchiera.pezzi_vivi:
                            self.scacchiera.pezzi_vivi.pop(coord_catturato)
                            
                    if mossa.get("promozione"):
                        pedone = self.scacchiera.pezzi_vivi.get(mossa["finale"])
                        self.controllo_pezzi.esegui_promozione(
                            self.scacchiera, pedone, mossa["promozione"]
                        )
                    
                    if is_matto:
                        vincitore = self.nome1 if self.turno_bianco else self.nome2

                        self.ui.imposta_stile("accent", "bright_green")
                        self.ui.imposta_stile("bold", False)
                        self.ui.stampa(f"Scacco Matto! Ha vinto {vincitore}!")

                        self.in_gioco = False
                        break

                if self.turno_bianco:
                    self.mosse_bianco.append(stringa)
                else:
                    self.mosse_nero.append(stringa)

                for p in self.scacchiera.pezzi_vivi.values():
                    if hasattr(p, "en_passant") and isinstance(p, type(pezzo)) and p.colore != pezzo.colore:
                        p.en_passant = False
                        
                self.turno_bianco = not self.turno_bianco
                self.ui.stampa_scacchiera(self.scacchiera)

            except Exception as e:
                print(f"Errore: {e}. Riprova.")

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
            risultato = self.input_utente.in_ascolto(
                self.input_utente.leggi("Inserisci"))
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
                                                       " partita."))
                        
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
                                                       " partita."))
                    
                    self.ui.imposta_stile('accent', 'white')
                    self.ui.stampa(self.ui.formatta_testo("Inserisci comando /gioca"))
            case 5:
                if self.in_gioco:
                        risposta = self.input_utente.leggi("Accetti la patta (s/n)")
                        
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
                                                       " partita."))
            case 6:
                if self.in_gioco:
                    while True:
                        risposta = self.input_utente.leggi("Vuoi davvero abbandonare?" \
                                                          "(s/n)")
                        if risposta.lower() == "s":
                            vincitore = self.nome2 if self.turno_bianco else self.nome1

                            self.ui.imposta_stile('accent', 'green')
                            self.ui.stampa(
                                self.ui.formatta_testo(f"{vincitore} ha vinto"\
                                                    " per abbandono."))
                            
                            self.reset()
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
                    risposta = self.input_utente.leggi("Vuoi davvero uscire? (s/n)")
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
