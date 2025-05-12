import pytest

from scacchi.Entity.Coordinata import Coordinata
from scacchi.Entity.Pedone import Pedone
from scacchi.Entity.Pezzo import Pezzo
from scacchi.Entity.Scacchiera import Scacchiera


@pytest.fixture
def pezzi_vivi():
    """Fixture per creare pezzi e inizializzare la scacchiera."""
    # Creiamo un pedone bianco in (1, 2)
    pedone_bianco = Pedone("♙", Coordinata(1, 2), colore=True)
    # Creiamo un pedone nero in (1, 7)
    pedone_nero = Pedone("♟", Coordinata(1, 7), colore=False)
    # Aggiungiamo i pezzi alla scacchiera
    pezzi_vivi = {Coordinata(1, 2): pedone_bianco, Coordinata(1, 7): pedone_nero}
    return pezzi_vivi

@pytest.fixture
def scacchiera(pezzi_vivi):
    """Fixture per creare una scacchiera con i pezzi vivi."""
    return Scacchiera(pezzi_vivi)

def test_is_occupied_true(scacchiera):
    """Testa la funzione is_occupied quando la casella è occupata."""
    coord_occupata = Coordinata(1, 2)
    assert scacchiera.is_occupied(coord_occupata) == True  # La casella (1, 2) è occupata da un pedone bianco

def test_is_occupied_false(scacchiera):
    """Testa la funzione is_occupied quando la casella non è occupata."""
    coord_libera = Coordinata(2, 3)
    assert scacchiera.is_occupied(coord_libera) == False  # La casella (2, 3) è vuota

def test_is_occupied_multiple_pieces(scacchiera):
    """Testa la funzione is_occupied con più pezzi sulla scacchiera."""
    coord_occupata = Coordinata(1, 7)
    assert scacchiera.is_occupied(coord_occupata) == True  # La casella (1, 7) è occupata da un pedone nero
