from copy import deepcopy

from ..Entity.Coordinata import Coordinata
from ..Entity.Pezzo import Pezzo
from ..Entity.Re import Re
from ..Entity.Scacchiera import Scacchiera


class ControlloPezzi:
    """CLASSE CONTROL."""
    
    """Controlla le operazioni sui pezzi durante il gioco degli scacchi."""

    def __init__(self):
        """Inizializza un oggetto ControlloPezzi."""
        pass

    def trova_pezzo(self, scacchiera: Scacchiera, finale: Coordinata, colore: bool,
    simbolo) -> Pezzo:
        """Trova il pezzo del colore specificato che puo' muoversi alla coordinata.
        
        Args:
            scacchiera (Scacchiera): La scacchiera di gioco contenente i pezzi
            finale (Coordinata): Coordinata di destinazione del pezzo.
            colore (bool): Colore del pezzo da cercare.
            simbolo: Carattere simbolico del pezzo da cercare.
            
        Returns:
            Pezzo: Il primo pezzo valido che puo' effettuare la mossa, se trovato.
        
        """
        for _, piece in scacchiera.pezzi_vivi.items():            
            if (piece is not None and piece.colore == colore 
                and piece.simbolo == simbolo and 
                piece.controlla_mossa(finale, scacchiera)):
                return piece
      
    def muovi(self, da_mangiare: bool, scacchiera: Scacchiera, pezzo: Pezzo,
    finale: Coordinata) -> bool:
        """Esegue lo spostamento di un pezzo sulla scacchiera.
        
        Args:
            da_mangiare (bool): Indica se il pezzo deve mangiare un altro pezzo.
            scacchiera (Scacchiera): La scacchiera di gioco contenente i pezzi.
            pezzo (Pezzo): Il pezzo da muovere.
            finale (Coordinata): La coordinata di destinazione del pezzo.
        
        Raises:
            ValueError: Se la mossa non e' valida, se il pezzo e' minacciato, 
                        se la iniziale e' occupata da un pezzo dello stesso colore,
                        o se la mossa non elimina lo scacco.

        Returns:
            bool: True se la mossa e' stata eseguita con successo, False altrimenti.
        
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

        if not self.mossa_elimina_scacco(scacchiera, pezzo, finale):
            raise ValueError("Mossa illegale: il re sarebbe in scacco dopo la mossa")
        
        scacchiera.pezzi_vivi.pop(pezzo.iniziale)
        pezzo.iniziale = finale
        scacchiera.pezzi_vivi[finale] = pezzo
        
        return True

    def minacciato_da_nemico(self, colore: bool,  scacchiera: Scacchiera,
    finale: Coordinata) -> bool:
        """Controlla se la coordinata finale e' minacciata da un pezzo nemico.
        
        Args:
            colore: Colore del pezzo che sta effettuando la mossa.
            scacchiera (Scacchiera): La scacchiera di gioco contenente i pezzi.
            finale (Coordinata): La coordinata di destinazione del pezzo.
        
        Returns:
            bool: True se la coordinata finale e' minacciata da un pezzo nemico, 
                  False altrimenti.
                  
        """
        minacciato = False
        for _, pezzo in scacchiera.pezzi_vivi.items():
            if pezzo.colore != colore and pezzo.controlla_mossa(finale, scacchiera):
                minacciato = True
        
        return minacciato

    def scacco(self, scacchiera: Scacchiera, pezzo: Pezzo) -> bool:

        colore_re_avversario = not pezzo.colore
        re_avversario = next((p for p in scacchiera.pezzi_vivi.values()
                              if isinstance(p, Re) and p.colore == colore_re_avversario)
                            ,None)
        if re_avversario is None:
            raise ValueError("Re avversario non trovato")
        coordinata_re_avversario = re_avversario.iniziale
        
        for p in scacchiera.pezzi_vivi.values():
            if p.colore == pezzo.colore:
                mosse = p.mosse_possibili(scacchiera)
                if coordinata_re_avversario in mosse:
                    return True
        return False
    
    def re_in_scacco(self, scacchiera: Scacchiera, colore_re: bool) -> bool:
        re = next((p for p in scacchiera.pezzi_vivi.values()
                if isinstance(p, Re) and p.colore == colore_re), None)
        if re is None:
            raise ValueError("Re non trovato")

        for p in scacchiera.pezzi_vivi.values():
            if p.colore != colore_re and p.controlla_mossa(re.iniziale, scacchiera):
                return True
        return False

    
    def scacco_matto(self, scacchiera: Scacchiera, pezzo: Pezzo, finale: Coordinata) -> bool:
        scacchiera_sim = self.simula(scacchiera, pezzo, finale)
        if scacchiera_sim is None:
            return False

        colore_re_avversario = not pezzo.colore
        re_avversario = next((p for p in scacchiera_sim.pezzi_vivi.values()
                            if isinstance(p, Re) and p.colore == colore_re_avversario), None)
        if re_avversario is None:
            raise ValueError("Re avversario non trovato")

        if not self.re_in_scacco(scacchiera_sim, colore_re_avversario):
            return False

        for p in scacchiera_sim.pezzi_vivi.values():
            if p.colore == colore_re_avversario:
                mosse = p.mosse_possibili(scacchiera_sim)
                for mossa in mosse:
                    copia = self.simula(scacchiera_sim, p, mossa)
                    if copia is None:
                        continue
                    if not self.re_in_scacco(copia, colore_re_avversario):
                        return False
        return True

    def mossa_elimina_scacco(self, scacchiera: Scacchiera, pezzo: Pezzo, finale: Coordinata) -> bool:
        """Verifica se la mossa indicata elimina (o non causa) lo scacco al proprio re.
           
        Simula la mossa e controlla se il re dello stesso colore è sotto scacco.
        """
        copia = self.simula(scacchiera, pezzo, finale)
        if copia is None:
            return False

        # Trova il re del colore del pezzo che muove
        colore_re = pezzo.colore
        re = next((p for p in copia.pezzi_vivi.values() if isinstance(p, Re) and p.colore == colore_re), None)
        if re is None:
            return False

        # Se il re è sotto scacco dopo la mossa, la mossa non elimina lo scacco
        for avv in copia.pezzi_vivi.values():
            if avv.colore != colore_re and avv.controlla_mossa(re.iniziale, copia):
                return False
        return True
        
    def simula(self, scacchiera: Scacchiera, pezzo: Pezzo, finale: Coordinata) -> Scacchiera:
        """Simula una mossa su una copia della scacchiera.
        
        Args:
            scacchiera (Scacchiera): scacchiera corrente.
            pezzo (Pezzo): pezzo da muovere.
            finale (Coordinata): La destinazione della mossa.
        
        Returns:
            Scacchiera: nuova scacchiera dopo la mossa simulata se valida.
            None: se la mossa non e' valida.
            
        """
        copia = deepcopy(scacchiera)
        if not pezzo.controlla_mossa(finale, copia):
            return None
        pezzo_copia = copia.pezzi_vivi.get(pezzo.iniziale)
        if pezzo_copia is None:
            return None
        
        if finale in copia.pezzi_vivi:
            copia.pezzi_vivi.pop(finale)

        copia.pezzi_vivi.pop(pezzo_copia.iniziale)
        pezzo_copia.iniziale = finale
        copia.pezzi_vivi[finale] = pezzo_copia
        
        return copia
        
    def in_stallo(self, scacchiera: Scacchiera, colore_re: bool) -> bool:
        """Controlla se il re del colore specificato è in stallo.
        
        Args:
            scacchiera (Scacchiera): La scacchiera di gioco contenente i pezzi.
            colore_re (bool): Colore del re da controllare.
            
        Returns:
            bool: True se il re è in stallo, False altrimenti.
        
        Raises:
            ValueError: Se il re del colore specificato non esiste sulla scacchiera.
            
        """
        re = next((p for p in scacchiera.pezzi_vivi.values() if isinstance(p, Re) 
        and p.colore == colore_re), None)
        if re is None:
            return False
        
        if self.scacco(re, re.iniziale, scacchiera):
            return False
        
        # se esiste almeno una mossa legale, NON e' stallo
        for _, pezzo in scacchiera.pezzi_vivi.items():
            if pezzo.colore == colore_re:
                for x in range(1, 9):
                    for y in range(1, 9):
                        finale = Coordinata(x, y)
                        
                        if (pezzo.controlla_mossa(finale, scacchiera) 
                            and self.simula(scacchiera, pezzo, finale)):
                                return False
        return True
        