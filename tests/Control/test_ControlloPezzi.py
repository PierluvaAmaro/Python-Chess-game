import pytest

from scacchi.Control.ControlloPezzi import ControlloPezzi
from scacchi.Entity.Coordinata import Coordinata
from scacchi.Entity.Pedone import Pedone
from scacchi.Entity.Re import Re
from scacchi.Entity.Scacchiera import Scacchiera
from scacchi.Entity.Torre import Torre


def setup_scacchiera(*pezzi):
    """Crea una scacchiera con i pezzi specificati.

    Args:
        pezzi (tuple): Una tupla di pezzi da aggiungere alla scacchiera.

    Returns:
        Scacchiera: Un'istanza di Scacchiera con i pezzi specificati.

    """
    return Scacchiera({p.iniziale: p for p in pezzi})

def test_muovi_valido():
    """Testa che un pedone possa muoversi in avanti di una casa."""
    pedone = Pedone("♙", Coordinata(1, 2), True)
    scacchiera = setup_scacchiera(pedone)
    controllo = ControlloPezzi()
    finale = Coordinata(1, 3)
    assert controllo.muovi(False, scacchiera, pedone, finale) is True
    assert pedone.iniziale == finale
    assert scacchiera.pezzi_vivi[finale] == pedone

def test_muovi_cattura_valida():
    """Testa che un pedone possa muoversi in diagonale per catturare un pezzo nemico."""
    pedone = Pedone("♙", Coordinata(2, 2), True)
    nemico = Pedone("♟", Coordinata(3, 3), False)
    scacchiera = setup_scacchiera(pedone, nemico)
    controllo = ControlloPezzi()
    assert controllo.muovi(True, scacchiera, pedone, Coordinata(3, 3)) is True
    assert pedone.iniziale == Coordinata(3, 3)
    assert Coordinata(3, 3) in scacchiera.pezzi_vivi
    assert nemico not in scacchiera.pezzi_vivi.values()

def test_muovi_cattura_senza_nemico():
    """Testa che un pedone non possa muoversi in diagonale senza un pezzo nemico."""
    pedone = Pedone("♙", Coordinata(2, 2), True)
    scacchiera = setup_scacchiera(pedone)
    controllo = ControlloPezzi()
    # Il pedone non può muoversi in diagonale senza un pezzo nemico
    with pytest.raises(ValueError):
        controllo.muovi(True, scacchiera, pedone, Coordinata(3, 3))

def test_muovi_su_alleato():
    """Testa che un pedone non possa muoversi su una casa occupata da alleato."""
    pedone = Pedone("♙", Coordinata(2, 2), True)
    alleato = Pedone("♙", Coordinata(2, 3), True)
    scacchiera = setup_scacchiera(pedone, alleato)
    controllo = ControlloPezzi()
    # Il pedone non può muoversi su una casa occupata da un pezzo alleato
    with pytest.raises(ValueError):
        controllo.muovi(False, scacchiera, pedone, Coordinata(2, 3))

def test_muovi_normale_su_nemico():
    """Testa che un pedone non possa muoversi su una casa occupata da nemico."""
    pedone = Pedone("♙", Coordinata(2, 2), True)
    nemico = Pedone("♟", Coordinata(2, 3), False)
    scacchiera = setup_scacchiera(pedone, nemico)
    controllo = ControlloPezzi()
    # Il pedone non può muoversi su una casa occupata da un pezzo nemico
    with pytest.raises(ValueError):
        controllo.muovi(False, scacchiera, pedone, Coordinata(2, 3))

def test_muovi_re_in_casa_minacciata():
    """Testa che il re non possa muoversi in una casa minacciata da un pezzo nemico."""
    re = Re("♔", Coordinata(4, 1), True)
    torre = Torre("♜", Coordinata(4, 8), False)
    scacchiera = setup_scacchiera(re, torre)
    controllo = ControlloPezzi()
    # Torre nera minaccia la colonna 4, quindi il re non può andare in 4,2
    with pytest.raises(ValueError, match="minacciata da nemico"):
        controllo.muovi(False, scacchiera, re, Coordinata(4, 2))

def test_minacciato_da_nemico_true():
    """Testa che minacciato_da_nemico ritorni True se la casella è minacciata."""
    re = Re("♔", Coordinata(4, 1), True)
    torre = Torre("♜", Coordinata(4, 8), False)
    scacchiera = setup_scacchiera(re, torre)
    controllo = ControlloPezzi()
    # Torre nera minaccia la colonna 4, quindi 4,2 è minacciata
    assert controllo.minacciato_da_nemico(True, scacchiera, Coordinata(4, 2))

def test_minacciato_da_nemico_false():
    """Testa che minacciato_da_nemico ritorni False se la casella non è minacciata."""
    re = Re("♔", Coordinata(4, 1), True)
    torre = Torre("♜", Coordinata(5, 8), False)
    scacchiera = setup_scacchiera(re, torre)
    controllo = ControlloPezzi()
    # Torre nera non minaccia la colonna 4, quindi 4,2 non è minacciata
    assert not controllo.minacciato_da_nemico(True, scacchiera, Coordinata(4, 2))

def test_simula_mossa_valida():
    """Testa che simula ritorni una nuova scacchiera con la mossa applicata."""
    pedone = Pedone("♙", Coordinata(1, 2), True)
    scacchiera = setup_scacchiera(pedone)
    controllo = ControlloPezzi()
    nuova = controllo.simula(scacchiera, pedone, Coordinata(1, 3))
    assert nuova is not None
    assert Coordinata(1, 3) in nuova.pezzi_vivi

def test_muovi_non_valido():
    """Testa che il metodo muovi sollevi un'eccezione per una mossa non valida."""
    pedone = Pedone("P", Coordinata(1, 2), True)
    scacchiera = setup_scacchiera(pedone)
    controllo = ControlloPezzi()
    finale = Coordinata(1, 5)  # mossa non valida
    assert controllo.muovi(False, scacchiera, pedone, finale, False)

def test_trova_pezzo():
    """Testa che il metodo trova_pezzo restituisca il pezzo corretto."""
    pedone = Pedone("♙", Coordinata(2, 2), True)
    scacchiera = setup_scacchiera(pedone)
    controllo = ControlloPezzi()
    candidati = controllo.trova_pezzo(scacchiera, None, Coordinata(2, 3), True, "♙")
    # Verifica che il pedone sia tra i candidati
    assert pedone in candidati

def test_esegui_promozione_valida():
    """Testa che un pedone venga promosso correttamente."""
    pedone = Pedone("♙", Coordinata(1, 8), True)
    scacchiera = setup_scacchiera(pedone)
    controllo = ControlloPezzi()
    controllo.esegui_promozione(scacchiera, pedone, "D")
    from scacchi.Entity.Regina import Regina
    # Verifica che il pedone sia stato promosso a Regina
    assert isinstance(scacchiera.pezzi_vivi[Coordinata(1, 8)], Regina)

def test_esegui_promozione_non_valida():
    """Testa che venga sollevata un'eccezione se il pedone non è in ultima riga."""
    pedone = Pedone("♙", Coordinata(1, 7), True)
    scacchiera = setup_scacchiera(pedone)
    controllo = ControlloPezzi()
    # Il pedone non è in ultima riga, quindi non può essere promosso
    with pytest.raises(ValueError):
        controllo.esegui_promozione(scacchiera, pedone, "D")

def test_esegui_promozione_simbolo_non_valido():
    """Testa che venga sollevata un'eccezione se il simbolo di promozione è invalido."""
    pedone = Pedone("♙", Coordinata(1, 8), True)
    scacchiera = setup_scacchiera(pedone)
    controllo = ControlloPezzi()
    # Simbolo non valido per promozione
    with pytest.raises(ValueError):
        controllo.esegui_promozione(scacchiera, pedone, "Z")