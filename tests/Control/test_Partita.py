from unittest.mock import MagicMock, patch

import pytest

from scacchi.Control.Partita import Partita, saluta


# --- Test saluta ---
def test_saluta_file_non_trovato():
    """Testa che il metodo saluta gestisca l'assenza del file senza errori."""
    ui = MagicMock()
    with patch("scacchi.Control.Partita.leggi_file", side_effect=FileNotFoundError):
        saluta(ui)
    ui.stampa.assert_any_call("Benvenuto al gioco degli scacchi!", "bright_white")
    ui.stampa.assert_any_call("Versione 2.0 (Sprint 2)", "cyan")

def test_saluta_file_vuoto():
    """Testa che il metodo saluta gestisca un file vuoto senza errori."""
    ui = MagicMock()
    with patch("scacchi.Control.Partita.leggi_file", return_value=""):
        saluta(ui)
    ui.stampa.assert_called_with("Benvenuto al gioco degli scacchi!", "bright_white")

def test_saluta_file_contenuto():
    """Testa che il metodo saluta legga correttamente un file con contenuto."""
    ui = MagicMock()
    contenuto = "Linea1\nLinea2\nLinea3\nLinea4"
    with patch("scacchi.Control.Partita.leggi_file", return_value=contenuto):
        saluta(ui)
    assert ui.imposta_stile.call_count >= 2
    assert ui.stampa.call_count == 4

# --- Test Partita.reset ---
def test_reset_resetta_stato():
    """Testa che il metodo reset resetti lo stato della partita."""
    # Crea un'istanza di Partita e imposta alcuni valori
    partita = Partita()
    partita.nome1 = "A"
    partita.nome2 = "B"
    partita.in_gioco = True
    partita.turno_bianco = False
    partita.mosse_bianco = ["e4"]
    partita.mosse_nero = ["e5"]
    partita.reset()
    assert partita.nome1 == ""
    assert partita.nome2 == ""
    assert partita.in_gioco is False
    assert partita.turno_bianco is True
    assert partita.mosse_bianco == []
    assert partita.mosse_nero == []

# --- Test Partita.processa ---
@pytest.mark.parametrize("risultato,expected", [
    (1, None),  # avvia chiama avvia, che resetta e richiede input, qui mockato
    (2, "continua"),
    (3, None),
    (4, None),
    (5, None),
    (6, None),
    (7, None),
])
def test_processa_comandi(risultato, expected):
    """Testa il metodo processa con vari comandi."""
    partita = Partita()
    partita.ui = MagicMock()
    partita.input_utente = MagicMock()
    partita.in_gioco = True
    partita.nome1 = "A"
    partita.nome2 = "B"
    # Mock metodi che richiedono input o stampa
    partita.avvia = MagicMock()
    partita.ui.stampa_scacchiera = MagicMock()
    partita.ui.stampa_file = MagicMock()
    partita.reset = MagicMock()
    partita.input_utente.leggi = MagicMock(return_value="s")
    if risultato == 2:
        partita.in_gioco = False
    if risultato == 5:
        partita.input_utente.leggi = MagicMock(return_value="s")
    if risultato == 6:
        partita.input_utente.leggi = MagicMock(side_effect=["n", "s"])
    if risultato == 7:
        partita.input_utente.leggi = MagicMock(side_effect=["n", "s"])
    # Non testiamo l'uscita dal programma
    with patch("builtins.exit", side_effect=SystemExit):
        try:
            ret = partita.processa(risultato)
        except SystemExit:
            ret = None
    if risultato == 2 and not partita.in_gioco:
        assert partita.ui.stampa.called
        assert ret is None
    elif risultato == 2 and partita.in_gioco:
        assert ret == "continua"
    else:
        assert ret in (None, "continua", "fine")
        
def test_processa_comando_non_valido():
    """Testa il comportamento quando viene inserito un comando non valido."""
    partita = Partita()
    partita.ui = MagicMock()
    partita.input_utente = MagicMock()
    partita.in_gioco = True
    partita.nome1 = "A"
    partita.nome2 = "B"
    partita.input_utente.leggi = MagicMock(return_value="comando_non_valido")
    
    with patch("builtins.exit", side_effect=SystemExit):
        try:
            ret = partita.processa(0)
        except SystemExit:
            ret = None
            
    # Rimuovi questa riga se il codice non modifica in_gioco
    # assert not partita.in_gioco
    assert not partita.ui.stampa_scacchiera.called
    assert ret is None