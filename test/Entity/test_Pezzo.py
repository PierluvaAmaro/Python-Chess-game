import pytest
from scacchi.Entity.Pezzo import Pezzo
from scacchi.Entity.Coordinata import Coordinata

class DummyPezzo(Pezzo):
    def controlla_mossa(self, finale, scacchiera=None):
        # Consente solo la mossa in diagonale
        return abs(self.iniziale.x - finale.x) == abs(self.iniziale.y - finale.y)
    def percorso_libero(self, finale, scacchiera):
        return True

def test_init():
    coord = Coordinata(3, 3)
    pezzo = DummyPezzo("X", coord, True)
    assert pezzo.simbolo == "X"
    assert pezzo.iniziale == coord
    assert pezzo.colore is True
    assert pezzo.primo == 1

def test_controlla_mossa_diagonale():
    pezzo = DummyPezzo("X", Coordinata(4, 4), True)
    assert pezzo.controlla_mossa(Coordinata(6, 6)) is True
    assert pezzo.controlla_mossa(Coordinata(2, 2)) is True
    assert pezzo.controlla_mossa(Coordinata(4, 6)) is False

def test_percorso_libero():
    pezzo = DummyPezzo("X", Coordinata(1, 1), True)
    assert pezzo.percorso_libero(Coordinata(2, 2), None) is True

def test_mosse_possibili_diagonale():
    pezzo = DummyPezzo("X", Coordinata(4, 4), True)
    mosse = pezzo.mosse_possibili(None)
    # Tutte le diagonali da (4,4) su scacchiera 8x8
    for i in range(1, 9):
        for j in range(1, 9):
            if abs(4 - i) == abs(4 - j) and (i, j) != (4, 4):
                assert Coordinata(i, j) in mosse
    # (4,4) non deve essere tra le mosse possibili
    assert Coordinata(4, 4) not in mosse

def test_mosse_possibili_exception():
    class DummyPezzoExc(Pezzo):
        def controlla_mossa(self, finale, scacchiera=None):
            raise Exception("Errore")
        def percorso_libero(self, finale, scacchiera):
            return True
    pezzo = DummyPezzoExc("Y", Coordinata(1, 1), True)
    # Deve restituire lista vuota perché tutte le chiamate sollevano eccezione
    assert pezzo.mosse_possibili(None) == []