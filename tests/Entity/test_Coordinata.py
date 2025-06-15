from scacchi.Entity.Coordinata import Coordinata


def test_uguale_true():
    """Testa che due Coordinata con le stesse coordinate siano uguali."""
    c1 = Coordinata(3, 5)
    c2 = Coordinata(3, 5)
    assert c1 == c2

def test_uguale_false_differente_x():
    """Testa che Coordinata non sia uguale se le coordinate x sono diverse."""
    c1 = Coordinata(3, 5)
    c2 = Coordinata(4, 5)
    assert c1 != c2

def test_uguale_false_differente_y():
    """Testa che Coordinata non sia uguale se le coordinate y sono diverse."""
    c1 = Coordinata(3, 5)
    c2 = Coordinata(3, 6)
    assert c1 != c2

def test_uguale_false_tipo_diverso():
    """Testa che Coordinata non sia uguale a un tuple."""
    c1 = Coordinata(3, 5)
    assert c1 != (3, 5)

def test_hash_uguale_per_coord_uguali():
    """Testa che due Coordinata con le stesse coordinate abbiano lo stesso hash."""
    c1 = Coordinata(2, 7)
    c2 = Coordinata(2, 7)
    assert hash(c1) == hash(c2)

def test_hash_funzionante_in_set():
    """Testa che Coordinata possa essere usata in un set."""
    c1 = Coordinata(1, 1)
    c2 = Coordinata(1, 1)
    s = {c1}
    assert c2 in s

def test_posso_usare_da_chiave_dizionario():
    """Testa che una Coordinata possa essere usata come chiave in un dizionario."""
    c1 = Coordinata(8, 8)
    d = {c1: "regina"}
    assert d[Coordinata(8, 8)] == "regina"
