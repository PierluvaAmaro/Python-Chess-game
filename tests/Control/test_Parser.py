import pytest

from scacchi.Control.Parser import Parser
from scacchi.Entity.Coordinata import Coordinata


@pytest.fixture
def parser():
    """Fixture per creare un'istanza del parser da utilizzare nei test."""
    return Parser()

def test_parse_mossa_pedone(parser):
    """Testa la notazione per un pedone bianco.

    Args:
        parser (Parser): L'istanza del parser da testare.

    """
    result = parser.parse_mossa("e4", True)
    assert result["tipo"] == "mossa"
    assert result["simbolo"] == "♙"
    assert result["finale"] == Coordinata(5, 4)
    assert not result["cattura"]
    assert not result["scacco"]
    assert not result["matto"]

def test_parse_mossa_pedone_nero(parser):
    """Testa la notazione per un pedone nero.

    Args:
        parser (Parser): L'istanza del parser da testare.

    """
    result = parser.parse_mossa("e5", False)
    assert result["simbolo"] == "♟"
    assert result["finale"] == Coordinata(5, 5)

def test_parse_mossa_cavallo(parser):
    """Testa la notazione per il cavallo.

    Args:
        parser (Parser): L'istanza del parser da testare.

    """
    result = parser.parse_mossa("Cxf3+", True)
    assert result["simbolo"] == "♘"
    assert result["cattura"]
    assert result["scacco"]
    assert not result["matto"]

def test_parse_mossa_promozione(parser):
    """Testa la notazione per la promozione di un pedone.

    Args:
        parser (Parser): L'istanza del parser da testare.

    """
    result = parser.parse_mossa("e8=D", True)
    assert result["promozione"] == "D"
    assert result["finale"] == Coordinata(5, 8)

def test_parse_mossa_en_passant(parser):
    """Testa la notazione per la cattura en passant.

    Args:
        parser (Parser): L'istanza del parser da testare.

    """
    result = parser.parse_mossa("exd6 ep", True)
    assert result["cattura"]
    assert result["en_passant"]

def test_parse_mossa_arrocco_corto(parser):
    """Testa la notazione per l'arrocco corto.

    Args:
        parser (Parser): L'istanza del parser da testare.

    """
    result = parser.parse_mossa("O-O", True)
    assert result["tipo"] == "arrocco"
    assert result["lato"] == "corto"

def test_parse_mossa_arrocco_lungo(parser):
    """Testa la notazione per l'arrocco lungo.

    Args:
        parser (Parser): L'istanza del parser da testare.

    """
    result = parser.parse_mossa("O-O-O", True)
    assert result["tipo"] == "arrocco"
    assert result["lato"] == "lungo"

def test_parse_mossa_matto(parser):
    """Testa la notazione per il matto.

    Args:
        parser (Parser): L'istanza del parser da testare.

    """
    result = parser.parse_mossa("Dxf7#", True)
    assert result["matto"]
    assert result["cattura"]

def test_parse_mossa_con_origine_colonna(parser):
    """Testa la notazione con origine sulla colonna per una torre.

    Args:
        parser (Parser): L'istanza del parser da testare.

    """
    result = parser.parse_mossa("Tae1", True)
    assert result["simbolo"] == "♖"
    assert result["finale"] == Coordinata(5, 1)
    assert result["iniziale"].x == 1  # colonna 'a'
    assert result["iniziale"].y is None

def test_parse_mossa_con_origine_riga(parser):
    """Testa la notazione con origine sulla riga per una torre.

    Args:
        parser (Parser): L'istanza del parser da testare.

    """
    result = parser.parse_mossa("T1e1", True)
    assert result["iniziale"].x is None
    assert result["iniziale"].y == 1

def test_parse_mossa_con_origine_completa(parser):
    """Testa la notazione con origine completa per una torre.
    
    Args:
        parser (Parser): L'istanza del parser da testare.

    """
    result = parser.parse_mossa("Tg1e1", True)
    assert result["iniziale"] == Coordinata(7, 1)

def test_parse_mossa_notazione_errata(parser):
    """Testa che venga sollevata un'eccezione per notazione errata.

    Args:
        parser (Parser): L'istanza del parser da testare.

    """
    with pytest.raises(ValueError):
        parser.parse_mossa("notazioneErrata", True)

def test_parse_mossa_simbolo_non_valido(parser):
    """Testa che venga sollevata un'eccezione per simboli non validi.
    
    Args:
        parser (Parser): L'istanza del parser da testare.

    """
    with pytest.raises(ValueError):
        parser.parse_mossa("Zxe4", True)