import pytest
from scacchi.Entity.Re import Re
from scacchi.Entity.Coordinata import Coordinata

class DummyScacchiera:
    def __init__(self, occupate=None, nemici=None):
        self._occupate = occupate or set()
        self._nemici = nemici or set()
    def occupata(self, coord):
        return coord in self._occupate
    def occupata_da_nemico(self, pezzo, coord):
        return coord in self._nemici

def test_re_mossa_valida_libera():
    re = Re("♔", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    # Tutte le 8 caselle adiacenti sono mosse valide
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            finale = Coordinata(4 + dx, 4 + dy)
            assert re.controlla_mossa(finale, scacchiera) is True

def test_re_mossa_non_valida_lontana():
    re = Re("♔", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    assert re.controlla_mossa(Coordinata(6, 4), scacchiera) is False
    assert re.controlla_mossa(Coordinata(4, 6), scacchiera) is False
    assert re.controlla_mossa(Coordinata(2, 2), scacchiera) is False

def test_re_mossa_su_casella_occupata_da_alleato():
    re = Re("♔", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera(occupate={Coordinata(5, 5)})
    # Non è nemico, quindi percorso_libero deve restituire False
    assert re.controlla_mossa(Coordinata(5, 5), scacchiera) is False

def test_re_mossa_su_casella_occupata_da_nemico():
    re = Re("♔", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera(nemici={Coordinata(5, 5)})
    # Può catturare il nemico
    assert re.controlla_mossa(Coordinata(5, 5), scacchiera) is True

def test_re_mossa_su_stessa_casella():
    re = Re("♔", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    # Non può restare fermo
    assert re.controlla_mossa(Coordinata(4, 4), scacchiera) is False

def test_re_mossa_finale_none():
    re = Re("♔", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    with pytest.raises(ValueError):
        re.controlla_mossa(None, scacchiera)

def test_re_mosse_possibili():
    re = Re("♔", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    mosse = re.mosse_possibili(scacchiera)
    # Deve poter andare in tutte le 8 caselle adiacenti
    attese = [Coordinata(3,3), Coordinata(3,4), Coordinata(3,5),
              Coordinata(4,3),              Coordinata(4,5),
              Coordinata(5,3), Coordinata(5,4), Coordinata(5,5)]
    for c in attese:
        assert c in mosse
    assert Coordinata(4,4) not in mosse