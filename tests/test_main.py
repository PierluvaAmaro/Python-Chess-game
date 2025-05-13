import builtins
import unittest
from unittest.mock import MagicMock, patch

from scacchi.main import main


class TestMain(unittest.TestCase):

    @patch('scacchi.main.Partita')  # patcha il costruttore Partita
    def test_main_runs_check_once(self, MockPartita):
        # Crea un'istanza mock
        mock_partita_instance = MagicMock()
        MockPartita.return_value = mock_partita_instance

        # Simula un ciclo che termina subito sollevando SystemExit (come se si uscisse)
        mock_partita_instance.check.side_effect = [SystemExit]

        with self.assertRaises(SystemExit):
            main()  # Deve terminare il ciclo

        # Verifica che check sia stato chiamato una sola volta
        mock_partita_instance.check.assert_called_once()

    @patch('scacchi.main.Partita')
    def test_main_handles_exception(self, MockPartita):
        mock_partita_instance = MagicMock()
        MockPartita.return_value = mock_partita_instance

        # Simula un'eccezione generica
        mock_partita_instance.check.side_effect = [Exception("Errore simulato"), SystemExit]

        with patch.object(builtins, 'print') as mock_print:
            with self.assertRaises(SystemExit):
                main()

            # Verifica che l'errore sia stato stampato
            mock_print.assert_any_call("Errore: Errore simulato. Riprova.")
