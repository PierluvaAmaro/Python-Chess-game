import pytest
from scacchi.Entity.Coordinata import Coordinata
from scacchi.Entity.Pedone import Pedone
from scacchi.Control.Utils import crea_pezzo, leggi_scacchiera


def test_crea_pezzo():
    """Testa la creazione di un pezzo."""
    # Test per creare un pedone bianco
    coord = Coordinata(1, 2)
    pedone_bianco = crea_pezzo("♟", coord, True)
    
    assert isinstance(pedone_bianco, Pedone)
    assert pedone_bianco.simbolo == "♟"
    assert pedone_bianco.colore == True
    assert pedone_bianco.init == coord

    # Test per creare un pedone nero
    pedone_nero = crea_pezzo("♟", coord, False)
    
    assert isinstance(pedone_nero, Pedone)
    assert pedone_nero.simbolo == "♟"
    assert pedone_nero.colore == False
    assert pedone_nero.init == coord


def test_crea_pezzo_invalid_symbol():
    """Testa la gestione di un simbolo non valido."""
    coord = Coordinata(1, 2)
    
    with pytest.raises(ValueError):
        crea_pezzo("o", coord, True)  # Il simbolo ♞ non è un pezzo valido


# Faccio un mock per leggere la scacchiera da un file
@pytest.fixture
def mock_file(tmp_path):
    scacchiera_test = """........
........
........
........
........
........
........
........"""
    file = tmp_path / "scacchiera.txt"
    file.write_text(scacchiera_test)
    return file


def test_leggi_scacchiera(mock_file):
    """Testa la lettura della scacchiera da un file."""
    scacchiera = leggi_scacchiera(mock_file)
    
    assert len(scacchiera) == 0  # Tutte le caselle sono vuote

    # Aggiungi un pezzo e verifica la coordinata
    scacchiera_test = """
    ........
    ........
    ........
    ........
    ........
    ........
    ........
    .......♟
    """
    file = mock_file.parent / "scacchiera_test.txt"
    file.write_text(scacchiera_test)
    scacchiera = leggi_scacchiera(file)

    # Verifica che la scacchiera contenga un pedone nella giusta posizione
    coord = Coordinata(8, 1)
    pezzo = scacchiera[coord]
    assert isinstance(pezzo, Pedone)
    assert pezzo.simbolo == "♟"
    assert pezzo.colore == True  # Il pedone in questa posizione è bianco


def test_leggi_scacchiera_invalid_rows(mock_file):
    """Testa la gestione di un file con righe non valide."""
    invalid_file = mock_file.parent / "invalid_scacchiera.txt"
    invalid_scacchiera = """........
    ........
    ........
    ........
    ........
    ........
    ........"""
    
    invalid_file.write_text(invalid_scacchiera)

    with pytest.raises(ValueError, match="File non valido: le righe devono essere 8 ma sono: 7"):
        leggi_scacchiera(invalid_file)


def test_leggi_scacchiera_invalid_columns(mock_file):
    """Testa la gestione di un file con colonne non valide."""
    invalid_file = mock_file.parent / "invalid_scacchiera.txt"
    invalid_scacchiera = """.......
♟♟♟♟♟♟♟
.......
.......
.......
.......
♟♟♟♟♟♟♟
......."""
    
    invalid_file.write_text(invalid_scacchiera)

    with pytest.raises(ValueError, match="File non valido: le colonne devono essere 8"):
        leggi_scacchiera(invalid_file)
