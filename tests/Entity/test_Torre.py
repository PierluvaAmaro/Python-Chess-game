import pytest

from scacchi.Entity.Coordinata import Coordinata
from scacchi.Entity.Torre import Torre


class DummyScacchiera:
    """Classe di test per simulare una scacchiera."""
    
    def __init__(self, occupate=None, alleati=None, nemici=None):
        """Inizializza la scacchiera con pezzi occupati, alleati e nemici."""
        self._occupate = occupate or set()
        self._alleati = alleati or set()
        self._nemici = nemici or set()
    def occupata(self, coord):
        """Controlla se una coordinata è occupata da un pezzo."""
        return coord in self._occupate
    def occupata_da_alleato(self, pezzo, coord):
        """Controlla se una coordinata è occupata da un alleato."""
        return coord in self._alleati
    def occupata_da_nemico(self, pezzo, coord):
        """Controlla se una coordinata è occupata da un nemico."""
        return coord in self._nemici

def test_torre_mossa_orizzontale_libera():
    """Testa la mossa della Torre in orizzontale quando il percorso è libero."""
    torre = Torre("♖", Coordinata(1, 1), True)
    scacchiera = DummyScacchiera()
    assert torre.controlla_mossa(Coordinata(8, 1), scacchiera)[0] is True

def test_torre_mossa_verticale_libera():
    """Testa la mossa della Torre in verticale, che è valida."""
     # Torre in posizione (1, 1) che tenta di muovere su una casella libera
     # La mossa dovrebbe essere valida se il percorso è libero
    torre = Torre("♖", Coordinata(1, 1), True)
    scacchiera = DummyScacchiera()
    assert torre.controlla_mossa(Coordinata(1, 8), scacchiera)[0] is True

def test_torre_mossa_non_valida_diagonale():
    """Testa la mossa della Torre in diagonale, che non è valida."""
    torre = Torre("♖", Coordinata(1, 1), True)
    scacchiera = DummyScacchiera()
    assert torre.controlla_mossa(Coordinata(3, 3), scacchiera) is False

def test_torre_mossa_ostruita_orizzontale():
    """Testa la mossa della Torre quando è ostacolata da un pezzo."""
     # Torre in posizione (1, 1) che tenta di muovere su una casella occupata
     # La mossa dovrebbe essere non valida se c'è un pezzo che blocca il percorso
    torre = Torre("♖", Coordinata(1, 1), True)
    scacchiera = DummyScacchiera(occupate={Coordinata(4, 1)})
    assert torre.controlla_mossa(Coordinata(8, 1), scacchiera) is False

def test_torre_mossa_ostruita_verticale():
    """Testa la mossa della Torre quando è ostacolata da un pezzo."""
     # Torre in posizione (1, 1) che tenta di muovere su una casella occupata
     # La mossa dovrebbe essere non valida se c'è un pezzo che blocca il percorso
    torre = Torre("♖", Coordinata(1, 1), True)
    scacchiera = DummyScacchiera(occupate={Coordinata(1, 5)})
    assert torre.controlla_mossa(Coordinata(1, 8), scacchiera) is False

def test_torre_mossa_su_alleato():
    """Testa la mossa della Torre su una casella occupata da alleato."""
     # Torre in posizione (1, 1) che tenta di muovere su una casella
     # occupata da un alleato
     # La mossa dovrebbe essere valida se l'alleato è presente
    torre = Torre("♖", Coordinata(1, 1), True)
    scacchiera = DummyScacchiera(alleati={Coordinata(1, 8)})
    # La logica di blocco su alleato è in ControlloPezzi, qui percorso
    # libero è True
    assert torre.controlla_mossa(Coordinata(1, 8), scacchiera)[0] is True

def test_torre_mossa_su_nemico():
    """Testa la mossa della Torre su una casella occupata da nemico."""
     # Torre in posizione (1, 1) che tenta di muovere su una casella 
     # occupata da un nemico
     # La mossa dovrebbe essere valida se il nemico è presente

    torre = Torre("♖", Coordinata(1, 1), True)
    scacchiera = DummyScacchiera(nemici={Coordinata(1, 8)})
    assert torre.controlla_mossa(Coordinata(1, 8), scacchiera)[0] is True

def test_torre_mossa_finale_none():
    """Testa la gestione di una mossa finale None."""
    torre = Torre("♖", Coordinata(1, 1), True)
    scacchiera = DummyScacchiera()
    with pytest.raises(ValueError):
        torre.controlla_mossa(None, scacchiera)

def test_torre_mosse_possibili():
    """Testa le mosse possibili della Torre."""
     # Torre in posizione centrale, dovrebbe poter muovere in 
     # tutte le direzioni
     # fino a raggiungere i bordi della scacchiera
    torre = Torre("♖", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    mosse = torre.mosse_possibili(scacchiera)
    # Deve poter andare in tutte le caselle della riga e colonna 
    # (tranne la posizione iniziale)
    assert Coordinata(4, 1) in mosse
    assert Coordinata(4, 8) in mosse
    assert Coordinata(1, 4) in mosse
    assert Coordinata(8, 4) in mosse
    assert Coordinata(4, 4) not in mosse