from scacchi.Entity.Coordinata import Coordinata
from scacchi.Entity.Scacchiera import Scacchiera


class DummyPezzo:
    """Classe di test per simulare un pezzo degli scacchi."""

    def __init__(self, colore):
        """Inizializza un pezzo con il suo colore.
        
        Args:
            colore (bool): True se il pezzo è bianco, False se è nero.

        """
        self.colore = colore

def test_occupata_da_alleato_true():
    """Testa se la coordinata è occupata da un alleato."""
    c1 = Coordinata(1, 1)
    c2 = Coordinata(2, 2)
    pezzo_bianco = DummyPezzo(True)
    pezzo_nero = DummyPezzo(False)
    scacchiera = Scacchiera({c1: pezzo_bianco, c2: pezzo_nero})
    assert scacchiera.occupata_da_alleato(pezzo_bianco, c1) is True

def test_occupata_da_alleato_false():
    """Testa se la coordinata è occupata da un alleato."""
    c1 = Coordinata(1, 1)
    c2 = Coordinata(2, 2)
    pezzo_bianco = DummyPezzo(True)
    pezzo_nero = DummyPezzo(False)
    scacchiera = Scacchiera({c1: pezzo_bianco, c2: pezzo_nero})
    assert scacchiera.occupata_da_alleato(pezzo_bianco, c2) is False

def test_occupata_da_nemico_true():
    """Testa se la coordinata è occupata da un nemico."""
    c1 = Coordinata(1, 1)
    c2 = Coordinata(2, 2)
    pezzo_bianco = DummyPezzo(True)
    pezzo_nero = DummyPezzo(False)
    scacchiera = Scacchiera({c1: pezzo_bianco, c2: pezzo_nero})
    assert scacchiera.occupata_da_nemico(pezzo_bianco, c2) is True

def test_occupata_da_nemico_false():
    """Testa se la coordinata non è occupata da un nemico."""
    c1 = Coordinata(1, 1)
    c2 = Coordinata(2, 2)
    pezzo_bianco = DummyPezzo(True)
    pezzo_nero = DummyPezzo(False)
    scacchiera = Scacchiera({c1: pezzo_bianco, c2: pezzo_nero})
    assert scacchiera.occupata_da_nemico(pezzo_bianco, c1) is False

def test_occupata_true():
    """Testa se una coordinata è occupata da un pezzo."""
    c1 = Coordinata(1, 1)
    pezzo_bianco = DummyPezzo(True)
    scacchiera = Scacchiera({c1: pezzo_bianco})
    assert scacchiera.occupata(c1) is True

def test_occupata_false():
    """Testa se una coordinata non è occupata da un pezzo."""
    c1 = Coordinata(1, 1)
    c2 = Coordinata(2, 2)
    pezzo_bianco = DummyPezzo(True)
    scacchiera = Scacchiera({c1: pezzo_bianco})
    assert scacchiera.occupata(c2) is False