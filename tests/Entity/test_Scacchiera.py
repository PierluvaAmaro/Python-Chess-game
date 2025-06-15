from scacchi.Entity.Scacchiera import Scacchiera
from scacchi.Entity.Coordinata import Coordinata

class DummyPezzo:
    def __init__(self, colore):
        self.colore = colore

def test_occupata_da_alleato_true():
    c1 = Coordinata(1, 1)
    c2 = Coordinata(2, 2)
    pezzo_bianco = DummyPezzo(True)
    pezzo_nero = DummyPezzo(False)
    scacchiera = Scacchiera({c1: pezzo_bianco, c2: pezzo_nero})
    assert scacchiera.occupata_da_alleato(pezzo_bianco, c1) is True

def test_occupata_da_alleato_false():
    c1 = Coordinata(1, 1)
    c2 = Coordinata(2, 2)
    pezzo_bianco = DummyPezzo(True)
    pezzo_nero = DummyPezzo(False)
    scacchiera = Scacchiera({c1: pezzo_bianco, c2: pezzo_nero})
    assert scacchiera.occupata_da_alleato(pezzo_bianco, c2) is False

def test_occupata_da_nemico_true():
    c1 = Coordinata(1, 1)
    c2 = Coordinata(2, 2)
    pezzo_bianco = DummyPezzo(True)
    pezzo_nero = DummyPezzo(False)
    scacchiera = Scacchiera({c1: pezzo_bianco, c2: pezzo_nero})
    assert scacchiera.occupata_da_nemico(pezzo_bianco, c2) is True

def test_occupata_da_nemico_false():
    c1 = Coordinata(1, 1)
    c2 = Coordinata(2, 2)
    pezzo_bianco = DummyPezzo(True)
    pezzo_nero = DummyPezzo(False)
    scacchiera = Scacchiera({c1: pezzo_bianco, c2: pezzo_nero})
    assert scacchiera.occupata_da_nemico(pezzo_bianco, c1) is False

def test_occupata_true():
    c1 = Coordinata(1, 1)
    pezzo_bianco = DummyPezzo(True)
    scacchiera = Scacchiera({c1: pezzo_bianco})
    assert scacchiera.occupata(c1) is True

def test_occupata_false():
    c1 = Coordinata(1, 1)
    c2 = Coordinata(2, 2)
    pezzo_bianco = DummyPezzo(True)
    scacchiera = Scacchiera({c1: pezzo_bianco})
    assert scacchiera.occupata(c2) is False