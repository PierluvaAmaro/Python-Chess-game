import pytest
from scacchi.Entity.Alfiere import Alfiere
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

def test_alfiere_mossa_diagonale_libera():
    alfiere = Alfiere("♗", Coordinata(3, 3), True)
    scacchiera = DummyScacchiera()
    assert alfiere.controlla_mossa(Coordinata(6, 6), scacchiera) is True

def test_alfiere_mossa_diagonale_ostruita():
    alfiere = Alfiere("♗", Coordinata(3, 3), True)
    scacchiera = DummyScacchiera(occupate={Coordinata(4, 4)})
    assert alfiere.controlla_mossa(Coordinata(6, 6), scacchiera) is False

def test_alfiere_mossa_non_diagonale():
    alfiere = Alfiere("♗", Coordinata(3, 3), True)
    scacchiera = DummyScacchiera()
    assert alfiere.controlla_mossa(Coordinata(3, 5), scacchiera) is False
    assert alfiere.controlla_mossa(Coordinata(5, 3), scacchiera) is False

def test_alfiere_mossa_su_alleato():
    alfiere = Alfiere("♗", Coordinata(3, 3), True)
    scacchiera = DummyScacchiera(alleati={Coordinata(5, 5)})
    # percorso libero, ma casella finale occupata da alleato (simulato)
    assert alfiere.controlla_mossa(Coordinata(5, 5), scacchiera) is True  # la logica di blocco è in ControlloPezzi

def test_alfiere_mossa_su_nemico():
    alfiere = Alfiere("♗", Coordinata(3, 3), True)
    scacchiera = DummyScacchiera(nemici={Coordinata(5, 5)})
    assert alfiere.controlla_mossa(Coordinata(5, 5), scacchiera) is True

def test_alfiere_mossa_finale_none():
    alfiere = Alfiere("♗", Coordinata(3, 3), True)
    scacchiera = DummyScacchiera()
    with pytest.raises(ValueError):
        alfiere.controlla_mossa(None, scacchiera)

def test_alfiere_mosse_possibili():
    alfiere = Alfiere("♗", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    mosse = alfiere.mosse_possibili(scacchiera)
    # Deve poter andare in tutte le diagonali
    assert Coordinata(1, 1) in mosse
    assert Coordinata(7, 7) in mosse
    assert Coordinata(1, 7) in mosse
    assert Coordinata(7, 1) in mosse
    assert Coordinata(4, 4) not in mosse