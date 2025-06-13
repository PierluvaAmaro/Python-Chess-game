from copy import deepcopy

from ..Entity.Coordinata import Coordinata
from ..Entity.Pezzo import Pezzo
from ..Entity.Re import Re
from ..Entity.Scacchiera import Scacchiera


class ControlloPezzi:
    """Classe control per la gestione delle operazioni sui pezzi degli scacchi."""
    
    def __init__(self):
        """Inizializza un nuovo controller per le operazioni sui pezzi."""
        pass

    def trova_pezzo(self, scacchiera: Scacchiera, finale: Coordinata, colore: bool,
    simbolo: str) -> Pezzo:
        """Cerca un pezzo che può muoversi alla coordinata specificata.
        
        Args:
            scacchiera (Scacchiera): Scacchiera di gioco contenente i pezzi.
            finale (Coordinata): Coordinata di destinazione del movimento.
            colore (bool): Colore del pezzo da cercare (True = bianco, False = nero).
            simbolo (str): Simbolo del pezzo da cercare.

        Returns:
            pezzo (Pezzo): Il primo pezzo valido trovato che può effettuare la mossa, 
            o None se nessun pezzo soddisfa i criteri.
        
        """
        for _, piece in scacchiera.pezzi_vivi.items():            
            if (piece is not None and piece.colore == colore 
                and piece.simbolo == simbolo and 
                piece.controlla_mossa(finale, scacchiera)):
                return piece
        return None
      
    def muovi(self, da_mangiare: bool, scacchiera: Scacchiera, pezzo: Pezzo,
    finale: Coordinata) -> bool:
        """Esegue lo spostamento di un pezzo sulla scacchiera.
        
        Args:
            da_mangiare (bool): Se True, indica che la mossa è una cattura.
            scacchiera (Scacchiera): Scacchiera di gioco.
            pezzo (Pezzo): Pezzo da muovere.
            finale (Coordinata): Coordinata di destinazione.

        Raises:
            ValueError: Se la mossa non è valida per uno dei seguenti motivi:
                - La casella di destinazione è minacciata (per il Re)
                - La casella è occupata da un alleato
                - Mossa di cattura senza pezzo nemico
                - Mossa normale con pezzo nemico presente

        Returns:
            bool: True se la mossa è stata eseguita con successo.
        
        """
        if (self.minacciato_da_nemico(pezzo.colore, scacchiera, finale)
        and isinstance(pezzo, Re)):
            raise ValueError("iniziale minacciata da nemico")

        if scacchiera.occupata_da_alleato(pezzo, finale):
            raise ValueError("Mossa illegale")

        if da_mangiare:
            if not scacchiera.occupata_da_nemico(pezzo, finale):
                raise ValueError("Mossa illegale")
            else:
                scacchiera.pezzi_vivi.pop(finale)
        else:
            if scacchiera.occupata_da_nemico(pezzo, finale):
                raise ValueError("Mossa illegale")
        
        scacchiera.pezzi_vivi.pop(pezzo.iniziale)
        pezzo.iniziale = finale
        scacchiera.pezzi_vivi[finale] = pezzo
        
        return True

    def minacciato_da_nemico(self, colore: bool, scacchiera: Scacchiera,
    finale: Coordinata) -> bool:
        """Verifica se una coordinata è minacciata da pezzi nemici.
        
        Args:
            colore (bool): Colore del giocatore che sta muovendo (True = bianco).
            scacchiera (Scacchiera): Scacchiera corrente di gioco.
            finale (Coordinata): Coordinata da verificare.

        Returns:
            bool: True se almeno un pezzo nemico può attaccare la coordinata.
        
        """
        return any(
            pezzo.controlla_mossa(finale, scacchiera)
            for _, pezzo in scacchiera.pezzi_vivi.items()
            if pezzo is not None and pezzo.colore != colore
        )

    def scacco(self, scacchiera: Scacchiera, pezzo: Pezzo) -> bool:
        """Verifica se il pezzo puo' mettere in scacco il re avversario.
        
        Args:
            scacchiera (Scacchiera): Scacchiera corrente di gioco.
            pezzo (Pezzo): Pezzo che potrebbe dare scacco.
        
        Returns:
            bool: True se il pezzo minaccia il re avversario, False altrimenti.
            
        Raises:
            ValueError: Se il re avversario non e' trovato sulla scacchiera.
        
        """
        colore_re_avversario = not pezzo.colore
        re_avversario = next((p for p in scacchiera.pezzi_vivi.values()
                              if isinstance(p, Re) and p.colore == colore_re_avversario)
                            ,None)
        if re_avversario is None:
            raise ValueError("Re avversario non trovato")
        
        return any(
            re_avversario.iniziale in p.mosse_possibili(scacchiera)
            for p in scacchiera.pezzi_vivi.values()
            if p is not None and p.colore == pezzo.colore
        )
    
    def re_in_scacco(self, scacchiera: Scacchiera, colore_re: bool) -> bool:
        """Determina se il re del colore specificato è in scacco.
        
        Args:
            scacchiera: Scacchiera corrente di gioco.
            colore_re: Colore del re da verificare (True = bianco).

        Returns:
            bool: True se il re è sotto scacco, False altrimenti.

        Raises:
            ValueError: Se il re del colore specificato non è trovato.
        
        """
        re = next((p for p in scacchiera.pezzi_vivi.values()
                if isinstance(p, Re) and p.colore == colore_re), None)
        if re is None:
            raise ValueError("Re non trovato")

        return self.minacciato_da_nemico(colore_re, scacchiera, re.iniziale)

    def scacco_matto(self, scacchiera: Scacchiera, pezzo: Pezzo,
                     finale: Coordinata) -> bool:
        """Verifica se una mossa provoca scacco matto all'avversario.
        
        Args:
            scacchiera (Scacchiera): Scacchiera corrente prima della mossa.
            pezzo (Pezzo): Pezzo che sta per essere mosso.
            finale (Coordinata): Coordinata di destinazione.

        Returns:
            bool: True se la mossa risulta in scacco matto.

        Raises:
            ValueError: Se il re avversario non è trovato dopo la mossa simulata.
        
        """
        scacchiera_sim = self.simula(scacchiera, pezzo, finale)
        if scacchiera_sim is None:
            return False

        colore_re_avversario = not pezzo.colore
        
        if not self.re_in_scacco(scacchiera_sim, colore_re_avversario):
            return False

        for p in scacchiera_sim.pezzi_vivi.values():
            if p is not None and p.colore == colore_re_avversario:
                for mossa in p.mosse_possibili(scacchiera_sim):
                    copia = self.simula(scacchiera_sim, p, mossa)
                    if copia is not None and not self.re_in_scacco(copia, 
                                                                   colore_re_avversario):
                        return False                
        return True

    def mossa_elimina_scacco(self, scacchiera: Scacchiera, pezzo: Pezzo, 
                            finale: Coordinata) -> bool:
        """Verifica se una mossa specifica rimuove lo scacco al proprio re.
        
        Args:
            scacchiera (Scacchiera): Scacchiera corrente prima della mossa.
            pezzo (Pezzo): Pezzo che si intende muovere.
            finale (Coordinata): Coordinata di destinazione del pezzo.
        
        Returns:
            bool: True se la mossa:
                    - È valida
                    - Non lascia il re sotto scacco
                    - Non espone il re a nuovo scacco.
                                      
        """
        copia = self.simula(scacchiera, pezzo, finale)
        if copia is None:
            return False
        
        # trovo il re dello stesso colore del pezzo mosso
        re = next(
            (p for p in copia.pezzi_vivi.values()
             if isinstance(p, Re) and p.colore == pezzo.colore),
            None
        )
        if re is None:
            return False
        
        # verifico se il re e' ancora sotto scacco dopo la mossa
        return not any(
            avv.controlla_mossa(re.iniziale, copia)
            for avv in copia.pezzi_vivi.values()
            if avv is not None and avv.colore != pezzo.colore
        )
        
    def simula(self, scacchiera: Scacchiera, pezzo: Pezzo, 
               finale: Coordinata) -> Scacchiera:
        """Crea una copia della scacchiera con la mossa simulata.
        
        Args:
            scacchiera (Scacchiera): Scacchiera corrente prima della mossa.
            pezzo (Pezzo): Pezzo da muovere (deve esistere sulla scacchiera).
            finale (Coordinata): Destinazione della mossa.

        Returns:
            Scacchiera: Nuova scacchiera con la mossa applicata se valida, 
            None altrimenti.
        
        """
        copia = deepcopy(scacchiera)
        
        # verifica preliminare della mossa
        if not pezzo.controlla_mossa(finale, copia):
            return None
        
        pezzo_copia = copia.pezzi_vivi.get(pezzo.iniziale)
        if pezzo_copia is None:
            return None
        
        copia.pezzi_vivi.pop(pezzo_copia.iniziale)
        if finale in copia.pezzi_vivi:
            copia.pezzi_vivi.pop(finale)

        pezzo_copia.iniziale = finale
        copia.pezzi_vivi[finale] = pezzo_copia
        
        return copia
        
    def in_stallo(self, scacchiera: Scacchiera, colore_re: bool) -> bool:
        """Determina se il giocatore specificato è in stallo.
        
        Args:
            scacchiera (Scacchiera): Scacchiera corrente.
            colore_re (bool): Colore del giocatore da verificare (True = bianco).

        Returns:
            bool: True se il re non è sotto scacco
            o se nessun pezzo può effettuare mosse valide. 

        Raises:
            ValueError: Se il re del colore specificato non esiste.
            
        """
        re = next(
            (p for p in scacchiera.pezzi_vivi.values()
             if isinstance(p, Re) and p.colore == colore_re),
            None
        )
        if re is None:
            raise ValueError(f"Re del colore {'bianco' if colore_re else 'nero'}"\
                "non trovato")
        
        # se il re e' sotto scacco, non e' stallo
        if self.re_in_scacco(scacchiera, colore_re):
            return False
        
        for pezzo in scacchiera.pezzi_vivi.values():
            if pezzo is not None and pezzo.colore == colore_re:
                for x in range(1, 9):
                    for y in range(1, 9):
                        finale = Coordinata(x, y)
                        if (pezzo.controlla_mossa(finale, scacchiera) and
                            self.simula(scacchiera, pezzo, finale) is not None):
                            return False
        return True