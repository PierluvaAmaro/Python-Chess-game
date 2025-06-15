from scacchi.Entity.Coordinata import Coordinata
from scacchi.Entity.Pedone import Pedone


class DummyScacchiera:
    """Classe di test per simulare una scacchiera con pezzi occupati e nemici."""

    def __init__(self, occupate=None, nemici=None, pezzi_vivi=None):
        """Inizializza una scacchiera di prova con pezzi occupati e nemici.

        Args:
            occupate (set, opzionale): Set di coordinate occupate da pezzi.
            nemici (set, opzionale): Set di coordinate occupate da pezzi nemici.
            pezzi_vivi (dict, opzionale): Dizionario di pezzi vivi sulla scacchiera.

        """
        self._occupate = occupate or set()
        self._nemici = nemici or set()
        self.pezzi_vivi = pezzi_vivi or {}

    def occupata(self, coord):
        """Controlla se una coordinata è occupata da un pezzo.

        Args:
            coord (Coordinata): La coordinata da controllare.

        Returns:
            bool: True se la coordinata è occupata, False altrimenti.

        """
        return coord in self._occupate

    def occupata_da_nemico(self, pezzo, coord):
        """Controlla se la coordinata è occupata da un pezzo nemico.

        Args:
            pezzo (Pezzo): Il pezzo che sta controllando la mossa.
            coord (Coordinata): La coordinata da controllare.

        Returns:
            bool: True se la coordinata è occupata da un pezzo nemico, False altrimenti.

        """
        return coord in self._nemici

def test_pedone_mossa_avanti_libera():
    """Testa che un pedone possa muoversi avanti se la casella finale è libera."""
    pedone = Pedone("♙", Coordinata(2, 2), True)
    scacchiera = DummyScacchiera()
    finale = Coordinata(2, 3)
    assert pedone.controlla_mossa(finale, scacchiera) is True

def test_pedone_mossa_avanti_occupata():
    """Testa che un pedone non possa muoversi avanti se la casella finale è occupata."""
    pedone = Pedone("♙", Coordinata(2, 2), True)
    scacchiera = DummyScacchiera(occupate={Coordinata(2, 3)})
    finale = Coordinata(2, 3)
    assert pedone.controlla_mossa(finale, scacchiera) is False

def test_pedone_mossa_due_caselle_primo_libera():
    """Testa che un pedone possa avanzare di due caselle se è la prima mossa."""
    pedone = Pedone("♙", Coordinata(2, 2), True)
    scacchiera = DummyScacchiera()
    finale = Coordinata(2, 4)
    assert pedone.controlla_mossa(finale, scacchiera) is True
    assert pedone.en_passant is True

def test_pedone_mossa_due_caselle_non_primo():
    """Testa che un pedone non possa avanzare di due caselle se non è la prima mossa."""
    pedone = Pedone("♙", Coordinata(2, 2), True)
    pedone.primo = 0
    scacchiera = DummyScacchiera()
    finale = Coordinata(2, 4)
    assert pedone.controlla_mossa(finale, scacchiera) is False

def test_pedone_mossa_due_caselle_ostruita():
    """Testa che il pedone non possa avanzare di due caselle se la finale è occupata."""
    pedone = Pedone("♙", Coordinata(2, 2), True)
    scacchiera = DummyScacchiera(occupate={Coordinata(2, 3)})
    finale = Coordinata(2, 4)
    assert pedone.controlla_mossa(finale, scacchiera) is False

def test_pedone_cattura_diagonale():
    """Testa che un pedone possa catturare un pezzo nemico in diagonale."""
    pedone = Pedone("♙", Coordinata(2, 2), True)
    scacchiera = DummyScacchiera(nemici={Coordinata(3, 3)})
    finale = Coordinata(3, 3)
    assert pedone.controlla_mossa(finale, scacchiera) is True

def test_pedone_cattura_diagonale_vuota():
    """Testa che un pedone non possa muoversi in diagonale su una casella vuota."""
    pedone = Pedone("♙", Coordinata(2, 2), True)
    scacchiera = DummyScacchiera()
    finale = Coordinata(3, 3)
    # Non dovrebbe essere possibile catturare su una casella vuota
    assert pedone.controlla_mossa(finale, scacchiera) is False

def test_pedone_en_passant():
    """Testa la mossa en passant di un pedone."""
    pedone = Pedone("♙", Coordinata(4, 5), True)
    pedone_nero = Pedone("♟", Coordinata(5, 5), False)
    pedone_nero.en_passant = True
    pezzi_vivi = {Coordinata(5, 5): pedone_nero}
    scacchiera = DummyScacchiera(pezzi_vivi=pezzi_vivi)
    finale = Coordinata(5, 6)
    # Il pedone bianco può catturare il pedone nero en passant
    assert pedone.controlla_mossa(finale, scacchiera) is True

def test_pedone_en_passant_non_valido():
    """Testa che un pedone non possa catturare en passant se non è abilitato."""
    pedone = Pedone("♙", Coordinata(4, 5), True)
    pedone_nero = Pedone("♟", Coordinata(5, 5), False)
    pedone_nero.en_passant = False
    pezzi_vivi = {Coordinata(5, 5): pedone_nero}
    scacchiera = DummyScacchiera(pezzi_vivi=pezzi_vivi)
    finale = Coordinata(5, 6)
    # Il pedone bianco non può catturare il pedone nero en passant
    assert pedone.controlla_mossa(finale, scacchiera) is False

def test_pedone_mossa_indietro():
    """Testa che un pedone non possa muoversi indietro."""
    pedone = Pedone("♙", Coordinata(2, 2), True)
    scacchiera = DummyScacchiera()
    finale = Coordinata(2, 1)
    # Un pedone non può muoversi indietro
    assert pedone.controlla_mossa(finale, scacchiera) is False

def test_pedone_nero_avanti():
    """Testa la mossa avanti di un pedone nero."""
    pedone = Pedone("♟", Coordinata(2, 7), False)
    scacchiera = DummyScacchiera()
    finale = Coordinata(2, 6)
    assert pedone.controlla_mossa(finale, scacchiera) is True

def test_pedone_nero_due_caselle():
    """Testa la mossa di un pedone nero che può muovere due caselle."""
    pedone = Pedone("♟", Coordinata(2, 7), False)
    scacchiera = DummyScacchiera()
    finale = Coordinata(2, 5)
    assert pedone.controlla_mossa(finale, scacchiera) is True
    assert pedone.en_passant is True

def test_pedone_nero_cattura_diagonale():
    """Testa la cattura diagonale di un pedone nero."""
    pedone = Pedone("♟", Coordinata(2, 7), False)
    scacchiera = DummyScacchiera(nemici={Coordinata(1, 6)})
    finale = Coordinata(1, 6)
    assert pedone.controlla_mossa(finale, scacchiera) is True