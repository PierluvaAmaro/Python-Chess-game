import pytest
from scacchi.Control.Parser import Parser
from scacchi.Entity.Coordinata import Coordinata


def test_parse_mossa_valida():
    """Test su una mossa valida."""
    parser = Parser()
    coord = parser.parse_mossa("e4")
    assert isinstance(coord, Coordinata)
    assert coord.x == 5  # 'e' -> 5
    assert coord.y == 4


# test per piu mosse diverse con lo stesso test
@pytest.mark.parametrize("input_str", ["e9", "j4", "4e", "ee", "a", "e", "z0", "", "E0"])
def test_parse_mossa_non_valida(input_str):
    """Test su input non validi che devono generare ValueError."""
    parser = Parser()
    with pytest.raises(ValueError):
        parser.parse_mossa(input_str)


def test_parse_mossa_case_insensitive():
    """Verifica che input maiuscoli vengano accettati."""
    parser = Parser()
    coord = parser.parse_mossa("D7")
    assert coord.x == 4
    assert coord.y == 7
