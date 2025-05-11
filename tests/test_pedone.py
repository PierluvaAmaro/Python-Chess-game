import pytest

from scacchi.Entity.Coordinata import Coordinata
from scacchi.Entity.Pedone import Pedone


@pytest.fixture
def pedone_nero():
    """Fixture che crea un pedone nero in posizione (1, 7)."""
    return Pedone("♟", Coordinata(1, 7), False)


@pytest.fixture
def pedone_bianco():
    """Fixture che crea un pedone bianco in posizione (1, 2)."""
    return Pedone("♙", Coordinata(1, 2), True)


def test_check_move_2caselle_in_avanti(pedone_nero):
    """Testa il movimento valido del pedone nero di due caselle al primo movimento."""
    final_coord = Coordinata(1, 5)  # Mossa valida: il pedone nero può spostarsi di 2 caselle in avanti
    assert pedone_nero.check_move(final_coord) == True  # La mossa è valida se è il primo movimento


def test_check_move_1casella_in_avanti(pedone_nero):
    """Testa il movimento valido del pedone nero di una casella in avanti."""
    pedone_nero.primo = False  # Il pedone ha già mosso
    final_coord = Coordinata(1, 6)  # Mossa valida: il pedone nero può spostarsi di 1 casella in avanti
    assert pedone_nero.check_move(final_coord) == True  # La mossa è valida se è una casella in avanti


def test_check_move_negativo(pedone_nero):
    """Testa il movimento non valido del pedone nero (due caselle indietro)."""
    final_coord = Coordinata(1, 8)  # Mossa non valida: il pedone nero non può andare indietro
    assert pedone_nero.check_move(final_coord) == False  # Il pedone non può muoversi indietro


def test_check_move_non_valido(pedone_nero):
    """Testa il movimento non valido del pedone nero (mossa orizzontale)."""
    final_coord = Coordinata(2, 7)  # Mossa non valida: il pedone può muoversi solo verticalmente
    assert pedone_nero.check_move(final_coord) == False  # Il pedone non può muoversi orizzontalmente


def test_check_move_bianco(pedone_bianco):
    """Testa il movimento valido del pedone bianco di una casella in avanti."""
    final_coord = Coordinata(1, 3)  # Mossa valida: il pedone bianco può spostarsi di una casella in avanti
    assert pedone_bianco.check_move(final_coord) == True


def test_check_move_bianco_2caselle(pedone_bianco):
    """Testa il movimento valido del pedone bianco di due caselle al primo movimento."""
    pedone_bianco.primo = True  # Impostiamo che il pedone non ha ancora mosso
    final_coord = Coordinata(1, 4)  # Mossa valida: il pedone bianco può spostarsi di 2 caselle in avanti
    assert pedone_bianco.check_move(final_coord) == True


def test_check_move_bianco_non_valido(pedone_bianco):
    """Testa il movimento non valido del pedone bianco (mossa orizzontale)."""
    final_coord = Coordinata(2, 2)  # Mossa non valida: il pedone può muoversi solo verticalmente
    assert pedone_bianco.check_move(final_coord) == False  # Il pedone non può muoversi orizzontalmente
