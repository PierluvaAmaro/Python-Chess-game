import pytest

from scacchi.Entity.Cavallo import Cavallo
from scacchi.Entity.Coordinata import Coordinata


class DummyScacchiera:
    """Classe di test per simulare una scacchiera con pezzi alleati."""

    def __init__(self, alleati=None):
        """Inizializza una scacchiera di prova con pezzi alleati.

        Args:
            alleati (set, opzionale): Set di coordinate occupate da pezzi alleati.

        """
        # Inizializza un set di coordinate occupate da pezzi alleati
        self._alleati = alleati or set()
    def occupata_da_alleato(self, pezzo, coord):
        """Controlla se una coordinata è occupata da un pezzo alleato.

        Args:
            pezzo (Pezzo): Il pezzo che sta controllando la mossa.
            coord (Coordinata): La coordinata da controllare.

        Returns:
            bool: True se la coordinata è occupata da un pezzo alleato, 
            False altrimenti.

        """
        return coord in self._alleati

def test_cavallo_mossa_valida():
    """Testa che il cavallo possa muoversi in posizioni valide."""
    cavallo = Cavallo("♘", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    # Tutte le 8 mosse possibili da centro
    possibili = [
        Coordinata(6, 5), Coordinata(6, 3), Coordinata(2, 5), Coordinata(2, 3),
        Coordinata(5, 6), Coordinata(5, 2), Coordinata(3, 6), Coordinata(3, 2)
    ]
    for finale in possibili:
        assert cavallo.controlla_mossa(finale, scacchiera) is True

def test_cavallo_mossa_non_valida():
    """Testa che il cavallo non possa muoversi in posizioni non valide."""
    cavallo = Cavallo("♘", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    # Mossa non a L
    assert cavallo.controlla_mossa(Coordinata(4, 5), scacchiera) is False
    assert cavallo.controlla_mossa(Coordinata(5, 5), scacchiera) is False
    assert cavallo.controlla_mossa(Coordinata(4, 4), scacchiera) is False

def test_cavallo_mossa_su_alleato():
    """Testa che il cavallo non possa muoversi su una casella occupata da un alleato."""
    cavallo = Cavallo("♘", Coordinata(4, 4), True)
    alleati = {Coordinata(6, 5)}
    scacchiera = DummyScacchiera(alleati=alleati)
    # Non può muovere su una casella occupata da alleato
    assert cavallo.controlla_mossa(Coordinata(6, 5), scacchiera) is False

def test_cavallo_mossa_finale_none():
    """Testa che la mossa non sia valida se la coordinata finale è None."""
    cavallo = Cavallo("♘", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    with pytest.raises(ValueError):
        cavallo.controlla_mossa(None, scacchiera)

def test_cavallo_mosse_possibili():
    """Testa le mosse possibili per un cavallo in una posizione centrale."""
    cavallo = Cavallo("♘", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    mosse = cavallo.mosse_possibili(scacchiera)
    attese = [
        Coordinata(6, 5), Coordinata(6, 3), Coordinata(2, 5), Coordinata(2, 3),
        Coordinata(5, 6), Coordinata(5, 2), Coordinata(3, 6), Coordinata(3, 2)
    ]
    for c in attese:
        assert c in mosse
    assert Coordinata(4, 4) not in mosse