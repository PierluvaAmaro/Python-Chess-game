import pytest
from scacchi.Entity.Coordinata import Coordinata

def test_inizializzazione():
    """Testa l'inizializzazione di una Coordinata."""
    coord = Coordinata(3, 4)
    
    assert coord.x == 3
    assert coord.y == 4

def test_change():
    """Testa la modifica delle coordinate."""
    coord = Coordinata(3, 4)
    
    # Modifica delle coordinate
    coord.change(5, 6)
    
    assert coord.x == 5
    assert coord.y == 6

def test_change_invalid_x():
    """Testa la modifica della coordinata X con un valore None."""
    coord = Coordinata(3, 4)
    
    with pytest.raises(ValueError, match="Valore X non valido."):
        coord.change(None, 5)

def test_change_invalid_y():
    """Testa la modifica della coordinata Y con un valore None."""
    coord = Coordinata(3, 4)
    
    with pytest.raises(ValueError, match="Valore Y non valido."):
        coord.change(5, None)

def test_eq():
    """Testa l'uguaglianza tra due coordinate."""
    coord1 = Coordinata(3, 4)
    coord2 = Coordinata(3, 4)
    coord3 = Coordinata(5, 6)
    
    assert coord1 == coord2  # Dovrebbero essere uguali
    assert coord1 != coord3  # Dovrebbero essere diverse

def test_eq_invalid_comparison():
    """Testa il confronto di una Coordinata con un oggetto non Coordinata."""
    coord1 = Coordinata(3, 4)
    not_a_coord = (3, 4)  # Una tupla, non una Coordinata
    
    assert coord1 != not_a_coord  # Dovrebbero essere considerati diversi

def test_hash():
    """Testa la generazione dell'hash per la coordinata."""
    coord1 = Coordinata(3, 4)
    coord2 = Coordinata(3, 4)
    coord3 = Coordinata(5, 6)
    
    assert hash(coord1) == hash(coord2)  # Stesso hash per coordinate uguali
    assert hash(coord1) != hash(coord3)  # Hash diversi per coordinate diverse
