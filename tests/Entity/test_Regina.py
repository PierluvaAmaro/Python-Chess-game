import pytest
from scacchi.Entity.Regina import Regina
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

def test_regina_mossa_orizzontale_libera():
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    assert regina.controlla_mossa(Coordinata(8, 4), scacchiera) is True

def test_regina_mossa_verticale_libera():
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    assert regina.controlla_mossa(Coordinata(4, 1), scacchiera) is True

def test_regina_mossa_diagonale_libera():
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    assert regina.controlla_mossa(Coordinata(7, 7), scacchiera) is True

def test_regina_mossa_non_valida():
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    # Movimento a L non valido
    assert regina.controlla_mossa(Coordinata(5, 6), scacchiera) is False

def test_regina_mossa_ostruita_verticale():
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera(occupate={Coordinata(4, 3)})
    assert regina.controlla_mossa(Coordinata(4, 1), scacchiera) is False

def test_regina_mossa_ostruita_orizzontale():
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera(occupate={Coordinata(6, 4)})
    assert regina.controlla_mossa(Coordinata(8, 4), scacchiera) is False

def test_regina_mossa_ostruita_diagonale():
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera(occupate={Coordinata(5, 5)})
    assert regina.controlla_mossa(Coordinata(7, 7), scacchiera) is False

def test_regina_mossa_su_alleato():
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera(alleati={Coordinata(4, 7)})
    assert regina.controlla_mossa(Coordinata(4, 7), scacchiera) is False

def test_regina_mossa_su_nemico():
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera(nemici={Coordinata(4, 7)})
    assert regina.controlla_mossa(Coordinata(4, 7), scacchiera) is True

def test_regina_mossa_finale_none():
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    with pytest.raises(ValueError):
        regina.controlla_mossa(None, scacchiera)

def test_regina_mosse_possibili():
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    mosse = regina.mosse_possibili(scacchiera)
    # Deve poter andare in tutte le direzioni (orizzontale, verticale, diagonale)
    assert Coordinata(4, 8) in mosse
    assert Coordinata(8, 4) in mosse
    assert Coordinata(1, 1) in mosse
    assert Coordinata(7, 7) in mosse
    assert Coordinata(4, 4) not in mosse