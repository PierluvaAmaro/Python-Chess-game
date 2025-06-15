from scacchi.Entity.Coordinata import Coordinata
from scacchi.Entity.Pezzo import Pezzo


class DummyPezzo(Pezzo):
    """Classe di test per simulare un pezzo degli scacchi che si muove in diagonale."""

    def controlla_mossa(self, finale, scacchiera=None):
        """Controlla se la mossa è valida per un pezzo che si muove solo in diagonale.

        Args:
            finale (Coordinata): La coordinata finale della mossa.
            scacchiera (Scacchiera, opzionale): La scacchiera su cui si sta muovendo 
            il pezzo.

        Returns:
            bool: True se la mossa è valida, False altrimenti.

        """
        # Controlla se la mossa è valida solo in diagonale
        return abs(self.iniziale.x - finale.x) == abs(self.iniziale.y - finale.y)
    def percorso_libero(self, finale, scacchiera):
        """Simula un percorso sempre libero.
        
        Args:
            finale (Coordinata): La coordinata finale della mossa.
            scacchiera (Scacchiera, opzionale): La scacchiera su cui si sta muovendo 
            il pezzo.

        Returns:
            bool: Sempre True per simulare un percorso libero.

        """
        return True

def test_init():
    """Testa l'inizializzazione di un pezzo."""
    coord = Coordinata(3, 3)
    pezzo = DummyPezzo("X", coord, True)
    assert pezzo.simbolo == "X"
    assert pezzo.iniziale == coord
    assert pezzo.colore is True
    assert pezzo.primo == 1

def test_controlla_mossa_diagonale():
    """Testa che controlla_mossa accetti solo mosse diagonali."""
    pezzo = DummyPezzo("X", Coordinata(4, 4), True)
    assert pezzo.controlla_mossa(Coordinata(6, 6)) is True
    assert pezzo.controlla_mossa(Coordinata(2, 2)) is True
    assert pezzo.controlla_mossa(Coordinata(4, 6)) is False

def test_percorso_libero():
    """Testa che il percorso sia libero per una mossa diagonale."""
    pezzo = DummyPezzo("X", Coordinata(1, 1), True)
    assert pezzo.percorso_libero(Coordinata(2, 2), None) is True

def test_mosse_possibili_diagonale():
    """Testa le mosse possibili in diagonale per un pezzo."""
    pezzo = DummyPezzo("X", Coordinata(4, 4), True)
    mosse = pezzo.mosse_possibili(None)
    # Tutte le diagonali da (4,4) su scacchiera 8x8
    for i in range(1, 9):
        for j in range(1, 9):
            if abs(4 - i) == abs(4 - j) and (i, j) != (4, 4):
                assert Coordinata(i, j) in mosse
    # (4,4) non deve essere tra le mosse possibili
    assert Coordinata(4, 4) not in mosse

def test_mosse_possibili_exception():
    """Verifica che mosse_possibili ritorni lista vuota se controlla_mossa fallisce."""

    class DummyPezzoExc(Pezzo):
        """Classe di test che solleva eccezioni in controlla_mossa."""

        def controlla_mossa(self, finale, scacchiera=None):
            """Solleva un'eccezione per simulare un errore.
            
            Args:
                finale (Coordinata): La coordinata finale della mossa.
                scacchiera (Scacchiera, opzionale): La scacchiera su cui si 
                sta muovendo il pezzo.

            Raises:
                Exception: Simula un errore durante il controllo della mossa.

            """
            raise Exception("Errore")
        def percorso_libero(self, finale, scacchiera):
            """Simula un percorso libero.
            
            Args:
                finale (Coordinata): La coordinata finale della mossa.
                scacchiera (Scacchiera, opzionale): La scacchiera su cui si
                sta muovendo il pezzo.

            Returns:
                    bool: Sempre True per simulare un percorso libero.

            """
            return True
    pezzo = DummyPezzoExc("Y", Coordinata(1, 1), True)
    # Deve restituire lista vuota perché tutte le chiamate sollevano eccezione
    assert pezzo.mosse_possibili(None) == []