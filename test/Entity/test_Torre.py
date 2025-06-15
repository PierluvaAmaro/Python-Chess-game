import pytest
from scacchi.Entity.Torre import Torre
from scacchi.Entity.Coordinata import Coordinata

class DummyScacchiera:
    def __init__(self, occupate=None, alleati=None, nemici=None):
        self._occupate = occupate or set()
        self._alleati = alleati or set()
        self._nemici = nemici or set()
    def occupata(self, coord):
        return coord in self._occupate
    def occupata_da_alleato(self, pezzo, coord):
        return coord in self._alleati
    def occupata_da_nemico(self, pezzo, coord):
        return coord in self._nemici

def test_torre_mossa_orizzontale_libera():
    torre = Torre("♖", Coordinata(1, 1), True)
    scacchiera = DummyScacchiera()
    assert torre.controlla_mossa(Coordinata(8, 1), scacchiera)[0] is True

def test_torre_mossa_verticale_libera():
    torre = Torre("♖", Coordinata(1, 1), True)
    scacchiera = DummyScacchiera()
    assert torre.controlla_mossa(Coordinata(1, 8), scacchiera)[0] is True

def test_torre_mossa_non_valida_diagonale():
    torre = Torre("♖", Coordinata(1, 1), True)
    scacchiera = DummyScacchiera()
    assert torre.controlla_mossa(Coordinata(3, 3), scacchiera) is False

def test_torre_mossa_ostruita_orizzontale():
    torre = Torre("♖", Coordinata(1, 1), True)
    scacchiera = DummyScacchiera(occupate={Coordinata(4, 1)})
    assert torre.controlla_mossa(Coordinata(8, 1), scacchiera) is False

def test_torre_mossa_ostruita_verticale():
    torre = Torre("♖", Coordinata(1, 1), True)
    scacchiera = DummyScacchiera(occupate={Coordinata(1, 5)})
    assert torre.controlla_mossa(Coordinata(1, 8), scacchiera) is False

def test_torre_mossa_su_alleato():
    torre = Torre("♖", Coordinata(1, 1), True)
    scacchiera = DummyScacchiera(alleati={Coordinata(1, 8)})
    # La logica di blocco su alleato è in ControlloPezzi, qui percorso libero è True
    assert torre.controlla_mossa(Coordinata(1, 8), scacchiera)[0] is True

def test_torre_mossa_su_nemico():
    torre = Torre("♖", Coordinata(1, 1), True)
    scacchiera = DummyScacchiera(nemici={Coordinata(1, 8)})
    assert torre.controlla_mossa(Coordinata(1, 8), scacchiera)[0] is True

def test_torre_mossa_finale_none():
    torre = Torre("♖", Coordinata(1, 1), True)
    scacchiera = DummyScacchiera()
    with pytest.raises(ValueError):
        torre.controlla_mossa(None, scacchiera)

def test_torre_mosse_possibili():
    torre = Torre("♖", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    mosse = torre.mosse_possibili(scacchiera)
    # Deve poter andare in tutte le caselle della riga e colonna (tranne la posizione iniziale)
    assert Coordinata(4, 1) in mosse
    assert Coordinata(4, 8) in mosse
    assert Coordinata(1, 4) in mosse
    assert Coordinata(8, 4) in mosse
    assert Coordinata(4, 4) not in mosse