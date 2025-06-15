import pytest

from scacchi.Entity.Coordinata import Coordinata
from scacchi.Entity.Re import Re


class DummyScacchiera:
    """Classe di test per simulare una scacchiera degli scacchi."""

    def __init__(self, occupate=None, nemici=None):
        """Inizializza una scacchiera di test con pezzi occupati e nemici.

        Args:
            occupate (set): Set di coordinate occupate da pezzi.
            nemici (set): Set di coordinate occupate da nemici.

        """
        self._occupate = occupate or set()
        self._nemici = nemici or set()
    def occupata(self, coord):
        """Controlla se una coordinata è occupata da un pezzo.

        Args:
            coord (Coordinata): La coordinata da controllare.

        Returns:
            bool: True se la coordinata è occupata, False altrimenti.

        """
        return coord in self._occupate
    def occupata_da_nemico(self, pezzo, coord):
        """Controlla se la coordinata è occupata da un nemico.

        Args:
            pezzo: Il pezzo che sta controllando la coordinata.
            coord (Coordinata): La coordinata da controllare.

        Returns:
            bool: True se la coordinata è occupata da un nemico, False altrimenti.

        """
        return coord in self._nemici

def test_re_mossa_valida_libera():
    """Testa una mossa valida del Re su una casella libera."""
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
    """Testa una mossa non valida del Re, troppo lontana."""
    re = Re("♔", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    # Il Re non può muoversi a più di una casella di distanza
    assert re.controlla_mossa(Coordinata(6, 4), scacchiera) is False
    assert re.controlla_mossa(Coordinata(4, 6), scacchiera) is False
    assert re.controlla_mossa(Coordinata(2, 2), scacchiera) is False

def test_re_mossa_su_casella_occupata_da_alleato():
    """Testa la mossa del Re su una casella occupata da un alleato."""
    re = Re("♔", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera(occupate={Coordinata(5, 5)})
    # Non è nemico, quindi percorso_libero deve restituire False
    assert re.controlla_mossa(Coordinata(5, 5), scacchiera) is False

def test_re_mossa_su_casella_occupata_da_nemico():
    """Testa la mossa del Re su una casella occupata da un nemico."""
    re = Re("♔", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera(nemici={Coordinata(5, 5)})
    # Può catturare il nemico
    assert re.controlla_mossa(Coordinata(5, 5), scacchiera) is True

def test_re_mossa_su_stessa_casella():
    """Testa la gestione di una mossa su una casella già occupata."""
    re = Re("♔", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    # Non può restare fermo
    assert re.controlla_mossa(Coordinata(4, 4), scacchiera) is False

def test_re_mossa_finale_none():
    """Testa la gestione di una mossa finale None."""
    re = Re("♔", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    with pytest.raises(ValueError):
        re.controlla_mossa(None, scacchiera)

def test_re_mosse_possibili():
    """Testa le mosse possibili del Re."""
    # Il Re può muoversi in tutte le 8 caselle adiacenti
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