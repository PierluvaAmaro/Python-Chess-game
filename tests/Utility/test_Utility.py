import pytest
from unittest.mock import patch, mock_open

from scacchi.Utility.Utils import crea_pezzo, leggi_file, leggi_scacchiera
from scacchi.Entity.Coordinata import Coordinata
from scacchi.Entity.Pedone import Pedone
from scacchi.Entity.Torre import Torre
from scacchi.Entity.Cavallo import Cavallo
from scacchi.Entity.Re import Re
from scacchi.Entity.Regina import Regina
from scacchi.Entity.Alfiere import Alfiere

def test_crea_pezzo_pedone_bianco():
    coord = Coordinata(1, 2)
    pezzo = crea_pezzo("♙", coord, True)
    assert isinstance(pezzo, Pedone)
    assert pezzo.simbolo == "♙"
    assert pezzo.colore is True
    assert pezzo.iniziale == coord

def test_crea_pezzo_pedone_nero():
    coord = Coordinata(1, 7)
    pezzo = crea_pezzo("♟", coord, False)
    assert isinstance(pezzo, Pedone)
    assert pezzo.simbolo == "♟"
    assert pezzo.colore is False

def test_crea_pezzo_torre():
    coord = Coordinata(1, 1)
    pezzo = crea_pezzo("♖", coord, True)
    assert isinstance(pezzo, Torre)
    assert pezzo.simbolo == "♖"

def test_crea_pezzo_cavallo():
    coord = Coordinata(2, 1)
    pezzo = crea_pezzo("♘", coord, True)
    assert isinstance(pezzo, Cavallo)
    assert pezzo.simbolo == "♘"

def test_crea_pezzo_re():
    coord = Coordinata(5, 1)
    pezzo = crea_pezzo("♔", coord, True)
    assert isinstance(pezzo, Re)
    assert pezzo.simbolo == "♔"

def test_crea_pezzo_regina():
    coord = Coordinata(4, 1)
    pezzo = crea_pezzo("♕", coord, True)
    assert isinstance(pezzo, Regina)
    assert pezzo.simbolo == "♕"

def test_crea_pezzo_alfiere():
    coord = Coordinata(3, 1)
    pezzo = crea_pezzo("♗", coord, True)
    assert isinstance(pezzo, Alfiere)
    assert pezzo.simbolo == "♗"

def test_crea_pezzo_simbolo_non_valido():
    coord = Coordinata(1, 1)
    with pytest.raises(ValueError):
        crea_pezzo("Z", coord, True)

def test_leggi_file_valido(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("ciao\nmondo")
    assert leggi_file(str(file_path)) == "ciao\nmondo"

def test_leggi_file_nessun_percorso():
    with pytest.raises(ValueError):
        leggi_file("")

def test_leggi_file_non_esistente():
    with pytest.raises(FileNotFoundError):
        leggi_file("file_che_non_esiste.txt")

def test_leggi_file_permission_error(monkeypatch):
    def raise_perm(*args, **kwargs):
        raise PermissionError("Permesso negato")
    monkeypatch.setattr("builtins.open", raise_perm)
    with pytest.raises(PermissionError):
        leggi_file("qualcosa.txt")

def test_leggi_file_oserror(monkeypatch):
    def raise_os(*args, **kwargs):
        raise OSError("Errore generico")
    monkeypatch.setattr("builtins.open", raise_os)
    with pytest.raises(OSError):
        leggi_file("qualcosa.txt")

def test_leggi_scacchiera_valida(monkeypatch):
    contenuto = (
        "♜♞♝♛♚♝♞♜\n"
        "♟♟♟♟♟♟♟♟\n"
        "........\n"
        "........\n"
        "........\n"
        "........\n"
        "♙♙♙♙♙♙♙♙\n"
        "♖♘♗♕♔♗♘♖\n"
    )
    monkeypatch.setattr("scacchi.Utility.Utils.leggi_file", lambda _: contenuto)
    scacchiera = leggi_scacchiera("dummy.txt")
    assert len(scacchiera) == 32
    assert isinstance(scacchiera[Coordinata(1, 2)], Pedone)
    assert isinstance(scacchiera[Coordinata(1, 7)], Pedone)
    assert isinstance(scacchiera[Coordinata(1, 1)], Torre)
    assert isinstance(scacchiera[Coordinata(1, 8)], Torre)

def test_leggi_scacchiera_righe_errate(monkeypatch):
    contenuto = "♜♞♝♛♚♝♞♜\n" * 7  # solo 7 righe
    monkeypatch.setattr("scacchi.Utility.Utils.leggi_file", lambda _: contenuto)
    with pytest.raises(ValueError):
        leggi_scacchiera("dummy.txt")

def test_leggi_scacchiera_colonne_errate(monkeypatch):
    contenuto = (
        "♜♞♝♛♚♝♞\n"  # solo 7 colonne
        "♟♟♟♟♟♟♟♟\n"
        "........\n"
        "........\n"
        "........\n"
        "........\n"
        "♙♙♙♙♙♙♙♙\n"
        "♖♘♗♕♔♗♘♖\n"
    )
    monkeypatch.setattr("scacchi.Utility.Utils.leggi_file", lambda _: contenuto)
    with pytest.raises(ValueError):
        leggi_scacchiera("dummy.txt")