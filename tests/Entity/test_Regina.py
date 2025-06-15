import pytest

from scacchi.Entity.Coordinata import Coordinata
from scacchi.Entity.Regina import Regina


class DummyScacchiera:
    """Classe di test per simulare una scacchiera degli scacchi."""

    # Questa classe simula una scacchiera per testare le mosse della regina.
    def __init__(self, occupate=None, alleati=None, nemici=None):
        """Inizializza una scacchiera di test con pezzi occupati, alleati e nemici.

        Args:
            occupate (set): Set di coordinate occupate da pezzi.
            alleati (set): Set di coordinate occupate da alleati.
            nemici (set): Set di coordinate occupate da nemici.

        """
        self._occupate = occupate or set()
        self._alleati = alleati or set()
        self._nemici = nemici or set()
    def occupata(self, coord):
        """Controlla se una coordinata è occupata da un pezzo.

        Args:
            coord (Coordinata): La coordinata da controllare.

        Returns:
            bool: True se la coordinata è occupata, False altrimenti.

        """
        return coord in self._occupate
    def occupata_da_alleato(self, pezzo, coord):
        """Controlla se la coordinata è occupata da un alleato.

        Args:
            pezzo: Il pezzo che sta controllando la coordinata.
            coord (Coordinata): La coordinata da controllare.

        Returns:
            bool: True se la coordinata è occupata da un alleato, False altrimenti.

        """
        return coord in self._alleati
    def occupata_da_nemico(self, pezzo, coord):
        """Controlla se la coordinata è occupata da un nemico.
        
        Args:
            pezzo: Il pezzo che sta controllando la coordinata.
            coord (Coordinata): La coordinata da controllare.

        Returns:
            bool: True se la coordinata è occupata da un nemico, False altrimenti.

        """
        return coord in self._nemici

def test_regina_mossa_orizzontale_libera():
    """Testa una mossa orizzontale libera della regina."""
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    assert regina.controlla_mossa(Coordinata(8, 4), scacchiera) is True

def test_regina_mossa_verticale_libera():
    """Testa una mossa verticale libera della regina."""
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    assert regina.controlla_mossa(Coordinata(4, 1), scacchiera) is True

def test_regina_mossa_diagonale_libera():
    """Testa una mossa diagonale libera della regina."""
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    assert regina.controlla_mossa(Coordinata(7, 7), scacchiera) is True

def test_regina_mossa_non_valida():
    """Testa una mossa non valida della regina."""
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    # Movimento a L non valido
    assert regina.controlla_mossa(Coordinata(5, 6), scacchiera) is False

def test_regina_mossa_ostruita_verticale():
    """Testa la mossa verticale della regina con un ostacolo."""
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera(occupate={Coordinata(4, 3)})
    assert regina.controlla_mossa(Coordinata(4, 1), scacchiera) is False

def test_regina_mossa_ostruita_orizzontale():
    """Testa la mossa orizzontale della regina con un ostacolo."""
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera(occupate={Coordinata(6, 4)})
    assert regina.controlla_mossa(Coordinata(8, 4), scacchiera) is False

def test_regina_mossa_ostruita_diagonale():
    """Testa la mossa della regina su una coordinata occupata."""
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera(occupate={Coordinata(5, 5)})
    assert regina.controlla_mossa(Coordinata(7, 7), scacchiera) is False

def test_regina_mossa_su_alleato():
    """Testa la gestione di una mossa su un alleato."""
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera(alleati={Coordinata(4, 7)})
    assert regina.controlla_mossa(Coordinata(4, 7), scacchiera) is False

def test_regina_mossa_su_nemico():
    """Testa la mossa della regina su una coordinata occupata da nemico."""
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera(nemici={Coordinata(4, 7)})
    assert regina.controlla_mossa(Coordinata(4, 7), scacchiera) is True

def test_regina_mossa_finale_none():
    """Testa la gestione di una mossa finale None."""
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    with pytest.raises(ValueError):
        regina.controlla_mossa(None, scacchiera)

def test_regina_mosse_possibili():
    """Testa le mosse possibili della regina."""
    regina = Regina("♕", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    mosse = regina.mosse_possibili(scacchiera)
    # Deve poter andare in tutte le direzioni (orizzontale, verticale, diagonale)
    assert Coordinata(4, 8) in mosse
    assert Coordinata(8, 4) in mosse
    assert Coordinata(1, 1) in mosse
    assert Coordinata(7, 7) in mosse
    assert Coordinata(4, 4) not in mosse