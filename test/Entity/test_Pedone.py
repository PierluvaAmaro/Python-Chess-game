import pytest
from scacchi.Entity.Pedone import Pedone
from scacchi.Entity.Coordinata import Coordinata

class DummyScacchiera:
    def __init__(self, occupate=None, nemici=None, pezzi_vivi=None):
        self._occupate = occupate or set()
        self._nemici = nemici or set()
        self.pezzi_vivi = pezzi_vivi or {}

    def occupata(self, coord):
        return coord in self._occupate

    def occupata_da_nemico(self, pezzo, coord):
        return coord in self._nemici

def test_pedone_mossa_avanti_libera():
    pedone = Pedone("♙", Coordinata(2, 2), True)
    scacchiera = DummyScacchiera()
    finale = Coordinata(2, 3)
    assert pedone.controlla_mossa(finale, scacchiera) is True

def test_pedone_mossa_avanti_occupata():
    pedone = Pedone("♙", Coordinata(2, 2), True)
    scacchiera = DummyScacchiera(occupate={Coordinata(2, 3)})
    finale = Coordinata(2, 3)
    assert pedone.controlla_mossa(finale, scacchiera) is False

def test_pedone_mossa_due_caselle_primo_libera():
    pedone = Pedone("♙", Coordinata(2, 2), True)
    scacchiera = DummyScacchiera()
    finale = Coordinata(2, 4)
    assert pedone.controlla_mossa(finale, scacchiera) is True
    assert pedone.en_passant is True

def test_pedone_mossa_due_caselle_non_primo():
    pedone = Pedone("♙", Coordinata(2, 2), True)
    pedone.primo = 0
    scacchiera = DummyScacchiera()
    finale = Coordinata(2, 4)
    assert pedone.controlla_mossa(finale, scacchiera) is False

def test_pedone_mossa_due_caselle_ostruita():
    pedone = Pedone("♙", Coordinata(2, 2), True)
    scacchiera = DummyScacchiera(occupate={Coordinata(2, 3)})
    finale = Coordinata(2, 4)
    assert pedone.controlla_mossa(finale, scacchiera) is False

def test_pedone_cattura_diagonale():
    pedone = Pedone("♙", Coordinata(2, 2), True)
    scacchiera = DummyScacchiera(nemici={Coordinata(3, 3)})
    finale = Coordinata(3, 3)
    assert pedone.controlla_mossa(finale, scacchiera) is True

def test_pedone_cattura_diagonale_vuota():
    pedone = Pedone("♙", Coordinata(2, 2), True)
    scacchiera = DummyScacchiera()
    finale = Coordinata(3, 3)
    assert pedone.controlla_mossa(finale, scacchiera) is False

def test_pedone_en_passant():
    pedone = Pedone("♙", Coordinata(4, 5), True)
    pedone_nero = Pedone("♟", Coordinata(5, 5), False)
    pedone_nero.en_passant = True
    pezzi_vivi = {Coordinata(5, 5): pedone_nero}
    scacchiera = DummyScacchiera(pezzi_vivi=pezzi_vivi)
    finale = Coordinata(5, 6)
    assert pedone.controlla_mossa(finale, scacchiera) is True

def test_pedone_en_passant_non_valido():
    pedone = Pedone("♙", Coordinata(4, 5), True)
    pedone_nero = Pedone("♟", Coordinata(5, 5), False)
    pedone_nero.en_passant = False
    pezzi_vivi = {Coordinata(5, 5): pedone_nero}
    scacchiera = DummyScacchiera(pezzi_vivi=pezzi_vivi)
    finale = Coordinata(5, 6)
    assert pedone.controlla_mossa(finale, scacchiera) is False

def test_pedone_mossa_indietro():
    pedone = Pedone("♙", Coordinata(2, 2), True)
    scacchiera = DummyScacchiera()
    finale = Coordinata(2, 1)
    assert pedone.controlla_mossa(finale, scacchiera) is False

def test_pedone_nero_avanti():
    pedone = Pedone("♟", Coordinata(2, 7), False)
    scacchiera = DummyScacchiera()
    finale = Coordinata(2, 6)
    assert pedone.controlla_mossa(finale, scacchiera) is True

def test_pedone_nero_due_caselle():
    pedone = Pedone("♟", Coordinata(2, 7), False)
    scacchiera = DummyScacchiera()
    finale = Coordinata(2, 5)
    assert pedone.controlla_mossa(finale, scacchiera) is True
    assert pedone.en_passant is True

def test_pedone_nero_cattura_diagonale():
    pedone = Pedone("♟", Coordinata(2, 7), False)
    scacchiera = DummyScacchiera(nemici={Coordinata(1, 6)})
    finale = Coordinata(1, 6)
    assert pedone.controlla_mossa(finale, scacchiera) is True