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
                        se la posizione e' occupata da un pezzo dello stesso colore,
                        o se la mossa non elimina lo scacco.

        Returns:
            bool: True se la mossa e' stata eseguita con successo, False altrimenti.
        
        """
        if (self.minacciato_da_nemico(pezzo.colore, scacchiera, finale)
        and isinstance(pezzo, Re)):
            raise ValueError("Posizione minacciata da nemico")

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

    def scacco(self, pezzo: Pezzo, mossa: Coordinata, scacchiera: Scacchiera) -> bool:
        """Controlla se il re avversario e' in scacco dopo una mossa.
        
        Args:
            pezzo (Pezzo): Il pezzo che sta effettuando la mossa.
            mossa (Coordinata): La coordinata di destinazione del pezzo.
            scacchiera (Scacchiera): La scacchiera di gioco contenente i pezzi.
            
        Raises:
            ValueError: Se il pezzo non e' un Re o se la mossa non e' valida.
        
        Returns:
            bool: True se il re e' in scacco dopo la mossa, False altrimenti.
    
        """
        copia = self.simula(scacchiera, pezzo, mossa)
        if copia is None:
            return False

        colore = not pezzo.colore
        re = next((p for p in copia.pezzi_vivi.values()
                if isinstance(p, Re) and p.colore == colore), None)
        if re is None:
            return False

        for _, altro_pezzo in copia.pezzi_vivi.items():
            if altro_pezzo.colore != re.colore and altro_pezzo.controlla_mossa(re.iniziale, copia):
                return True
        return False
    
    def mossa_elimina_scacco(self, scacchiera: Scacchiera, pezzo: Pezzo, 
    finale: Coordinata) -> bool:
        """Controlla dopo la mossa, il re e' ancora in scacco.
        
        Args:
            scacchiera (Scacchiera): La scacchiera di gioco contenente i pezzi.
            pezzo (Pezzo): Il pezzo che sta effettuando la mossa.
            finale (Coordinata): La coordinata di destinazione del pezzo.
            
        Raises:
            ValueError: Se il pezzo non e' un Re o se la mossa non e' valida.
            
        Returns:
            bool: True se la mossa elimina lo scacco del re, False altrimenti.
        
        """
        copia = self.simula(scacchiera, pezzo, finale)

        re = next((p for p in copia.pezzi_vivi.values()
        if isinstance(p, Re) and p.colore == pezzo.colore), None)
        if re is None:
            return False

        for _, altro_pezzo in copia.pezzi_vivi.items():
            if (altro_pezzo.colore != pezzo.colore
            and altro_pezzo.controlla_mossa(re.iniziale, copia)):
                return False
        return True
    
    def simula(self, scacchiera: Scacchiera, pezzo: Pezzo, 
    finale: Coordinata) -> Scacchiera:
        """Simula una determinata mossa su una scacchiera di copia.
        
        Args:
            scacchiera (Scacchiera): La scacchiera di gioco contenente i pezzi.
            pezzo (Pezzo): Il pezzo da muovere.
            finale (Coordinata): La coordinata di destinazione del pezzo.
        
        Raises:
            Exception: Se la mossa non e' valida o se il pezzo non puo' essere spostato.
            
        Returns:
            Scacchiera: Una copia della scacchiera dopo la mossa, se valida.

        """
        copia = deepcopy(scacchiera)
        
        try:
            pezzo_copia = copia.pezzi_vivi.pop(pezzo.iniziale)
            pezzo_copia.iniziale = finale
            copia.pezzi_vivi[finale] = pezzo_copia
            
            return copia
        except Exception as e:
            print(f"Errore: {e} Riprova.")
                
    def in_scacco_matto(self, scacchiera: Scacchiera, colore_re: bool) -> bool:
        """Controlla se il re del colore specificato e' in scacco matto.
        
        Args:
            scacchiera (Scacchiera): La scacchiera di gioco contenente i pezzi.
            colore_re (bool): Colore del re da controllare.
            
        Returns:
            bool: True se il re e' in scacco matto, False altrimenti.
            
        Raises:
            ValueError: Se il re del colore specificato non esiste sulla scacchiera.
            
        """
        res = True
        re = next((p for p in scacchiera.pezzi_vivi.values() if isinstance(p, Re) 
        and p.colore == colore_re), None)
        if re is None:
            return False
        
        # se non c'e' scacco, non e' scacco matto
        if not self.scacco(re, re.iniziale, scacchiera):
            return False
        
        # per ogni pezzo del colore sotto scacco, provo tutte le mosse possibili
        for _, pezzo in scacchiera.pezzi_vivi.items():
            if pezzo.colore == colore_re:
                for x in range(1, 9):
                    for y in range(1, 9):
                        finale = Coordinata(x, y)
                        if (pezzo.controlla_mossa(finale, scacchiera)):
                            copia = self.simula(scacchiera, pezzo, finale)
                            res = bool(self.scacco(re, finale, copia))
        
        return res
    
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
        