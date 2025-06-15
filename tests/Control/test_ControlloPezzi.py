import pytest

from scacchi.Control.ControlloPezzi import ControlloPezzi
from scacchi.Entity.Coordinata import Coordinata
from scacchi.Entity.Pedone import Pedone
from scacchi.Entity.Re import Re
from scacchi.Entity.Torre import Torre
from scacchi.Entity.Scacchiera import Scacchiera

def setup_scacchiera(*pezzi):
    return Scacchiera({p.iniziale: p for p in pezzi})

def test_muovi_valido():
    pedone = Pedone("♙", Coordinata(1, 2), True)
    scacchiera = setup_scacchiera(pedone)
    controllo = ControlloPezzi()
    finale = Coordinata(1, 3)
    assert controllo.muovi(False, scacchiera, pedone, finale) is True
    assert pedone.iniziale == finale
    assert scacchiera.pezzi_vivi[finale] == pedone

def test_muovi_non_valido():
    pedone = Pedone("♙", Coordinata(1, 2), True)
    scacchiera = setup_scacchiera(pedone)
    controllo = ControlloPezzi()
    finale = Coordinata(1, 5)  # mossa non valida per pedone bianco
    with pytest.raises(ValueError):
        controllo.muovi(False, scacchiera, pedone, finale)

def test_muovi_cattura_valida():
    pedone = Pedone("♙", Coordinata(2, 2), True)
    nemico = Pedone("♟", Coordinata(3, 3), False)
    scacchiera = setup_scacchiera(pedone, nemico)
    controllo = ControlloPezzi()
    assert controllo.muovi(True, scacchiera, pedone, Coordinata(3, 3)) is True
    assert pedone.iniziale == Coordinata(3, 3)
    assert Coordinata(3, 3) in scacchiera.pezzi_vivi
    assert nemico not in scacchiera.pezzi_vivi.values()

def test_muovi_cattura_senza_nemico():
    pedone = Pedone("♙", Coordinata(2, 2), True)
    scacchiera = setup_scacchiera(pedone)
    controllo = ControlloPezzi()
    with pytest.raises(ValueError):
        controllo.muovi(True, scacchiera, pedone, Coordinata(3, 3))

def test_muovi_su_alleato():
    pedone = Pedone("♙", Coordinata(2, 2), True)
    alleato = Pedone("♙", Coordinata(2, 3), True)
    scacchiera = setup_scacchiera(pedone, alleato)
    controllo = ControlloPezzi()
    with pytest.raises(ValueError):
        controllo.muovi(False, scacchiera, pedone, Coordinata(2, 3))

def test_muovi_normale_su_nemico():
    pedone = Pedone("♙", Coordinata(2, 2), True)
    nemico = Pedone("♟", Coordinata(2, 3), False)
    scacchiera = setup_scacchiera(pedone, nemico)
    controllo = ControlloPezzi()
    with pytest.raises(ValueError):
        controllo.muovi(False, scacchiera, pedone, Coordinata(2, 3))

def test_muovi_re_in_casa_minacciata():
    re = Re("♔", Coordinata(4, 1), True)
    torre = Torre("♜", Coordinata(4, 8), False)
    scacchiera = setup_scacchiera(re, torre)
    controllo = ControlloPezzi()
    # Torre nera minaccia la colonna 4, quindi il re non può andare in 4,2
    with pytest.raises(ValueError, match="minacciata da nemico"):
        controllo.muovi(False, scacchiera, re, Coordinata(4, 2))

def test_minacciato_da_nemico_true():
    re = Re("♔", Coordinata(4, 1), True)
    torre = Torre("♜", Coordinata(4, 8), False)
    scacchiera = setup_scacchiera(re, torre)
    controllo = ControlloPezzi()
    assert controllo.minacciato_da_nemico(True, scacchiera, Coordinata(4, 2))

def test_minacciato_da_nemico_false():
    re = Re("♔", Coordinata(4, 1), True)
    torre = Torre("♜", Coordinata(5, 8), False)
    scacchiera = setup_scacchiera(re, torre)
    controllo = ControlloPezzi()
    assert not controllo.minacciato_da_nemico(True, scacchiera, Coordinata(4, 2))

def test_simula_mossa_valida():
    pedone = Pedone("♙", Coordinata(1, 2), True)
    scacchiera = setup_scacchiera(pedone)
    controllo = ControlloPezzi()
    nuova = controllo.simula(scacchiera, pedone, Coordinata(1, 3))
    assert nuova is not None
    assert Coordinata(1, 3) in nuova.pezzi_vivi

def test_muovi_non_valido():
    pedone = Pedone("P", Coordinata(1, 2), True)
    scacchiera = setup_scacchiera(pedone)
    controllo = ControlloPezzi()
    finale = Coordinata(1, 5)  # mossa non valida
    
    assert controllo.muovi(False, scacchiera, pedone, finale, False)
def test_trova_pezzo():
    pedone = Pedone("♙", Coordinata(2, 2), True)
    scacchiera = setup_scacchiera(pedone)
    controllo = ControlloPezzi()
    candidati = controllo.trova_pezzo(scacchiera, None, Coordinata(2, 3), True, "♙")
    assert pedone in candidati

def test_esegui_promozione_valida():
    pedone = Pedone("♙", Coordinata(1, 8), True)
    scacchiera = setup_scacchiera(pedone)
    controllo = ControlloPezzi()
    controllo.esegui_promozione(scacchiera, pedone, "D")
    from scacchi.Entity.Regina import Regina
    assert isinstance(scacchiera.pezzi_vivi[Coordinata(1, 8)], Regina)

def test_esegui_promozione_non_valida():
    pedone = Pedone("♙", Coordinata(1, 7), True)
    scacchiera = setup_scacchiera(pedone)
    controllo = ControlloPezzi()
    with pytest.raises(ValueError):
        controllo.esegui_promozione(scacchiera, pedone, "D")

def test_esegui_promozione_simbolo_non_valido():
    pedone = Pedone("♙", Coordinata(1, 8), True)
    scacchiera = setup_scacchiera(pedone)
    controllo = ControlloPezzi()
    with pytest.raises(ValueError):
        controllo.esegui_promozione(scacchiera, pedone, "Z")