from copy import deepcopy

from ..Entity.Coordinata import Coordinata
from ..Entity.Pezzo import Pezzo
from ..Entity.Re import Re
from ..Entity.Scacchiera import Scacchiera
from ..Entity.Torre import Torre


class PieceControl:
    """CLASSE CONTROL."""
    
    """Controlla le operazioni sui pezzi durante il gioco degli scacchi."""

    def __init__(self):
        """Inizializza un oggetto PieceControl."""
        pass

    def find_piece(self, scacchiera: Scacchiera, final: Coordinata, colore: bool,
                   simbolo) -> Pezzo:
        """Trova il pezzo del colore specificato che puo' muoversi alla coordinata.
        
        Args:
            scacchiera (Scacchiera): La scacchiera di gioco contenente i pezzi
            final (Coordinata): Coordinata di destinazione del pezzo.
            colore (bool): Colore del pezzo da cercare.
            simbolo: Carattere simbolico del pezzo da cercare.
            
        Returns:
            Pezzo: Il primo pezzo valido che puo' effettuare la mossa, se trovato.
        
        """
        for _, piece in scacchiera.pezzi_vivi.items():            
            if (piece is not None and piece.colore == colore 
                and piece.simbolo == simbolo and piece.check_move(final, scacchiera)):
                return piece
        print(f"Nessun pezzo trovato per la mossa {final} con colore {colore}"
              "e simbolo {simbolo}")
      
    def muovi(
        self,
        da_mangiare: bool,
        scacchiera: Scacchiera,
        colore: bool,
        pezzo: Pezzo,
        final: Coordinata
    ) -> bool:
        """Esegue lo spostamento di un pezzo se la destinazione è valida."""
        if pezzo.simbolo == "♔" or pezzo.simbolo == "♚":  # noqa: SIM102
            if self.is_threatened_by_enemy(colore, scacchiera, final):
                raise ValueError("Posizione minacciata da nemico")

        if scacchiera.is_occupied_by_alliance(pezzo, final):
            raise ValueError("Mossa illegale")

        if da_mangiare:
            if not scacchiera.is_occupied_by_enemy(pezzo, final):
                raise ValueError("Mossa illegale")
            # Cattura il pezzo nemico
            scacchiera.pezzi_vivi.pop(final)
        else:
            if scacchiera.is_occupied_by_enemy(pezzo, final):
                raise ValueError("Mossa illegale")

        if not self.mossa_elimina_scacco(scacchiera, pezzo, final):
            raise ValueError("Mossa non valida: il re sarebbe in scacco dopo la mossa")
            
        scacchiera.pezzi_vivi.pop(pezzo.init)
        pezzo.init = final
        scacchiera.pezzi_vivi[final] = pezzo
        return True

    def is_threatened_by_enemy(self, colore: bool,  scacchiera: Scacchiera, final: Coordinata) -> bool:  # noqa: E501
        minacciato = False
        for _, pezzo in scacchiera.pezzi_vivi.items():
            if pezzo.colore != colore and pezzo.check_move(final, scacchiera):
                minacciato = True
        
        return minacciato

    def scacco(self, pezzo: Pezzo, mossa: Coordinata, scacchiera: Scacchiera) -> bool:
        copia = deepcopy(scacchiera)
        
        pezzo_copia = copia.pezzi_vivi.pop(pezzo.init)
        pezzo_copia.init = mossa
        
        copia.pezzi_vivi[mossa] = pezzo_copia
        
        colore = not pezzo.colore
        re = next(
            (
                p for p in copia.pezzi_vivi.values()
                if isinstance(p, Re) and p.colore == colore
            ),
            None
        )
        if re is None:
            return False
        
        for _, altro_pezzo in copia.pezzi_vivi.items():
            if (altro_pezzo.colore == pezzo.colore 
                and altro_pezzo.check_move(re.init, copia)):
                return True
        return False
    
    def mossa_elimina_scacco(self, scacchiera: Scacchiera, pezzo: Pezzo, 
                             final: Coordinata) -> bool:
        copia = deepcopy(scacchiera)
        # Muovi il pezzo sulla copia
        pezzo_copia = copia.pezzi_vivi.pop(pezzo.init)
        pezzo_copia.init = final
        copia.pezzi_vivi[final] = pezzo_copia

        # Trova il re del colore che ha mosso
        re = next((p for p in copia.pezzi_vivi.values() if isinstance(p, Re) and 
                   p.colore == pezzo.colore), None)
        if re is None:
            return False

        # Controlla se il re è minacciato da un pezzo avversario
        for _, altro_pezzo in copia.pezzi_vivi.items():
            if (altro_pezzo.colore != pezzo.colore
                and altro_pezzo.check_move(re.init, copia)):
                    return False
        return True
    
    def simulate(self, scacchiera: Scacchiera, pezzo: Pezzo, final: Coordinata) -> bool:
        """Simula una mossa e verifica se il re è ancora in scacco."""
        copia = deepcopy(scacchiera)
        try:
            pezzo_copia = copia.pezzi_vivi.pop(pezzo.init)
            pezzo_copia.init = final
            copia.pezzi_vivi[final] = pezzo_copia

            re = next((p for p in copia.pezzi_vivi.values() if isinstance(p, Re) 
                       and p.colore == pezzo.colore), None)
            if re is None:
                return False

            # Se il re NON è sotto scacco dopo la mossa, la mossa è valida per uscire
            # dallo scacco
            for _, altro_pezzo in copia.pezzi_vivi.items():
                if (altro_pezzo.colore != pezzo.colore 
                    and altro_pezzo.check_move(re.init, copia)):
                        return False
            return True
        except Exception as e:
            print(f"Errore durante la simulazione della mossa: {e}")
            return False
        
    def is_scacco_matto(self, scacchiera: Scacchiera, colore_re: bool) -> bool:
        """Controlla se il re del colore specificato è in scacco matto."""
        re = next((p for p in scacchiera.pezzi_vivi.values() if isinstance(p, Re) 
                   and p.colore == colore_re), None)
        if re is None:
            return False
        
        # se non c'e' scacco, non e' scacco matto
        if not self.scacco(re, re.init, scacchiera):
            return False
        
        # per ogni pezzo del colore sotto scacco, provo tutte le mosse possibili
        for _, pezzo in scacchiera.pezzi_vivi.items():
            if pezzo.colore == colore_re:
                for x in range(1, 9):
                    for y in range(1, 9):
                        final = Coordinata(x, y)
                        if (pezzo.check_move(final, scacchiera) 
                            and self.simulate(scacchiera, pezzo, final)):
                                return False
        return True
    
    def is_stallo(self, scacchiera: Scacchiera, colore_re: bool) -> bool:
        """Controlla se il re del colore specificato è in stallo."""
        re = next((p for p in scacchiera.pezzi_vivi.values() if isinstance(p, Re) 
                   and p.colore == colore_re), None)
        if re is None:
            return False
        
        if self.scacco(re, re.init, scacchiera):
            return False
        
        # se esiste almeno una mossa legale, NON e' stallo
        for _, pezzo in scacchiera.pezzi_vivi.items():
            if pezzo.colore == colore_re:
                for x in range(1, 9):
                    for y in range(1, 9):
                        final = Coordinata(x, y)
                        
                        if (pezzo.check_move(final, scacchiera) 
                            and self.simulate(scacchiera, pezzo, final)):
                                return False
        return True

    def esegui_arrocco(self, scacchiera: Scacchiera, colore: bool, lato: str) -> bool:
        """Esegue l'arrocco se le condizioni sono valide."""
        re = next((p for p in scacchiera.pezzi_vivi.values() if isinstance(p, Re) and p.colore == colore), None)

        if re is None or not re.primo:
            raise ValueError("L'arrocco non è possibile: il re ha già mosso.")

        if self.is_threatened_by_enemy(colore, scacchiera, re.init):
            raise ValueError("L'arrocco non è possibile mentre il re è sotto scacco.")

        riga = 1 if colore else 8
        if lato == "corto":
            torre_coord_iniziale = Coordinata(8, riga)
            caselle_intermedie = [Coordinata(6, riga), Coordinata(7, riga)]
            caselle_passaggio_re = [Coordinata(6, riga), Coordinata(7, riga)]
            coord_finale_re = Coordinata(7, riga)
            coord_finale_torre = Coordinata(6, riga)
        elif lato == "lungo":
            torre_coord_iniziale = Coordinata(1, riga)
            caselle_intermedie = [Coordinata(2, riga), Coordinata(3, riga), Coordinata(4, riga)]
            caselle_passaggio_re = [Coordinata(3, riga), Coordinata(4, riga)]
            coord_finale_re = Coordinata(3, riga)
            coord_finale_torre = Coordinata(4, riga)
        else:
            raise ValueError("Lato dell'arrocco non valido.")

        torre = scacchiera.pezzi_vivi.get(torre_coord_iniziale)
        if not isinstance(torre, Torre) or not torre.primo:
            raise ValueError("L'arrocco non è possibile con questa torre.")

        for coord in caselle_intermedie:
            if scacchiera.is_occupied(coord):
                raise ValueError("L'arrocco non è possibile: il percorso non è libero.")

        for coord in caselle_passaggio_re:
            if self.is_threatened_by_enemy(colore, scacchiera, coord):
                raise ValueError("L'arrocco non è possibile: il re non può passare su una casa minacciata.")

        scacchiera.pezzi_vivi.pop(re.init)
        scacchiera.pezzi_vivi.pop(torre_coord_iniziale)

        re.init = coord_finale_re
        re.primo = False
        re.arrocco = True
        torre.init = coord_finale_torre
        torre.primo = False

        scacchiera.pezzi_vivi[coord_finale_re] = re
        scacchiera.pezzi_vivi[coord_finale_torre] = torre

        return True