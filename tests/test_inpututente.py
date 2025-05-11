from unittest.mock import patch

from scacchi.Boundary.InputUtente import InputUtente


def test_leggi():
    """Test che leggi() ritorni l'input utente simulato."""
    with patch("builtins.input", return_value="ciao"):
        iu = InputUtente()
        risultato = iu.leggi("Scrivi qualcosa: ")
        assert risultato == "ciao"


def test_leggi_mossa_valida():
    """Test leggi_mossa con input valido, usando un parser mockato."""
    with patch("builtins.input", return_value="e4"), \
         patch("scacchi.Boundary.InputUtente.Parser") as MockParser:
        mock_parser_instance = MockParser.return_value
        mock_parser_instance.parse_mossa.return_value = "coordinata_mock"

        iu = InputUtente()
        risultato = iu.leggi_mossa()
        assert risultato == "coordinata_mock"
        mock_parser_instance.parse_mossa.assert_called_once_with("e4")


def test_leggi_mossa_non_valida_riprova_due_volte():
    """Test che leggi_mossa ripeta l'input se la mossa non è valida."""
    input_sequence = ["xxx", "e2"]  # Prima input non valido, poi valido
    with patch("builtins.input", side_effect=input_sequence), \
         patch("scacchi.Boundary.InputUtente.Parser") as MockParser:
        mock_parser_instance = MockParser.return_value
        # Prima chiamata: ValueError, seconda: ritorna coordinata
        mock_parser_instance.parse_mossa.side_effect = [ValueError("Errore fittizio"), "coordinata_valida"]

        iu = InputUtente()
        risultato = iu.leggi_mossa()
        assert risultato == "coordinata_valida"
        assert mock_parser_instance.parse_mossa.call_count == 2
