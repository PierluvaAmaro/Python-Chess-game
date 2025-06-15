import pytest

from scacchi.Entity.Alfiere import Alfiere
from scacchi.Entity.Coordinata import Coordinata


class DummyScacchiera:
    """Classe di test per simulare scacchiera con pezzi occupati,alleati e nemici."""

    def __init__(self, occupate=None, alleati=None, nemici=None):
        """Inizializza una scacchiera di prova con pezzi occupati, alleati e nemici.

        Args:
            occupate (set, opzionale): Set di coordinate occupate da pezzi.
            alleati (set, opzionale): Set di coordinate occupate da pezzi alleati.
            nemici (set, opzionale): Set di coordinate occupate da pezzi nemici.

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
        """Controlla se la coordinata è occupata da un pezzo alleato.

        Args:
            pezzo (Pezzo): Il pezzo che sta controllando la mossa.
            coord (Coordinata): La coordinata da controllare.

        Returns:
            bool: True se la coordinata è occupata da un pezzo alleato, 
            False altrimenti.

        """
        return coord in self._alleati
    def occupata_da_nemico(self, pezzo, coord):
        """Controlla se la coordinata è occupata da un pezzo nemico.

        Args:
            pezzo (Pezzo): Il pezzo che sta controllando la mossa.
            coord (Coordinata): La coordinata da controllare.  

        Returns:
            bool: True se la coordinata è occupata da un pezzo nemico, 
            False altrimenti.

        """ 
        return coord in self._nemici

def test_alfiere_mossa_diagonale_libera():
    """Testa che l'alfiere possa muoversi in diagonale se il percorso è libero."""
    alfiere = Alfiere("♗", Coordinata(3, 3), True)
    scacchiera = DummyScacchiera()
    # percorso libero
    assert alfiere.controlla_mossa(Coordinata(6, 6), scacchiera) is True

def test_alfiere_mossa_diagonale_ostruita():
    """Testa che l'alfiere non possa muoversi se il percorso è ostruito."""
    alfiere = Alfiere("♗", Coordinata(3, 3), True)
    scacchiera = DummyScacchiera(occupate={Coordinata(4, 4)})
    # percorso non libero
    assert alfiere.controlla_mossa(Coordinata(6, 6), scacchiera) is False

def test_alfiere_mossa_non_diagonale():
    """Testa che l'alfiere non possa muoversi in una direzione non diagonale."""
    alfiere = Alfiere("♗", Coordinata(3, 3), True)
    scacchiera = DummyScacchiera()
    # Mossa orizzontale
    assert alfiere.controlla_mossa(Coordinata(3, 5), scacchiera) is False
    # Mossa verticale
    assert alfiere.controlla_mossa(Coordinata(5, 3), scacchiera) is False

def test_alfiere_mossa_su_alleato():
    """Testa che l'alfiere non possa muoversi su una casella occupata da alleato."""
    alfiere = Alfiere("♗", Coordinata(3, 3), True)
    scacchiera = DummyScacchiera(alleati={Coordinata(5, 5)})
    # percorso libero, ma casella finale occupata da alleato (simulato)
    # la logica di blocco è in ControlloPezzi
    assert alfiere.controlla_mossa(Coordinata(5, 5), scacchiera) is True 
def test_alfiere_mossa_su_nemico():
    """Testa che l'alfiere possa muoversi su una casella occupata da nemico."""
    alfiere = Alfiere("♗", Coordinata(3, 3), True)
    scacchiera = DummyScacchiera(nemici={Coordinata(5, 5)})
    # percorso libero, ma casella finale occupata da nemico
    assert alfiere.controlla_mossa(Coordinata(5, 5), scacchiera) is True

def test_alfiere_mossa_finale_none():
    """Testa che l'alfiere non accetti una mossa con finale None."""
    alfiere = Alfiere("♗", Coordinata(3, 3), True)
    scacchiera = DummyScacchiera()
    with pytest.raises(ValueError):
        alfiere.controlla_mossa(None, scacchiera)

def test_alfiere_mosse_possibili():
    """Testa le mosse possibili per un alfiere."""
    alfiere = Alfiere("♗", Coordinata(4, 4), True)
    scacchiera = DummyScacchiera()
    mosse = alfiere.mosse_possibili(scacchiera)
    # Deve poter andare in tutte le diagonali
    assert Coordinata(1, 1) in mosse
    assert Coordinata(7, 7) in mosse
    assert Coordinata(1, 7) in mosse
    assert Coordinata(7, 1) in mosse
    assert Coordinata(4, 4) not in mosse