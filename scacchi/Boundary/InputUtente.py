from Control.Parser import Parser
from Entity.Coordinata import Coordinata


class InputUtente:
    """."""
    
    def __init__(self):
        pass

    def leggi_mossa(self, prompt: str = "Inserisci mossa (es. e4): ") -> Coordinata:
        parser = Parser()

        while True:
            try:
                mossa = input(prompt).strip()
                return parser.parse_mossa(mossa)
            except ValueError as e:
                print(f"Errore: {e}. Riprova.")