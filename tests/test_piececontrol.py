"""Tests for the PieceControl class."""  # noqa: D100

import pytest  # noqa: F401

from scacchi.Control.PieceControl import PieceControl
from scacchi.Entity.Coordinata import Coordinata
from scacchi.Entity.Scacchiera import Scacchiera
from scacchi.Entity.Pedone import Pedone


def test_find_piece_success():
    """Verifica che find_piece trovi il pezzo corretto che può muoversi verso la coordinata."""
    coord_start = Coordinata(2, 2)
    coord_dest = Coordinata(2, 4)
    pedone_bianco = Pedone("P", coord_start, True)
    scacchiera = Scacchiera({coord_start: pedone_bianco})

    control = PieceControl()
    pezzo = control.find_piece(scacchiera, coord_dest, True)

    assert pezzo == pedone_bianco


def test_find_piece_fail_wrong_color():
    """Verifica che find_piece non trovi pezzi del colore sbagliato."""
    coord_start = Coordinata(2, 2)
    coord_dest = Coordinata(2, 4)
    pedone_nero = Pedone("p", coord_start, False)
    scacchiera = Scacchiera({coord_start: pedone_nero})

    control = PieceControl()
    pezzo = control.find_piece(scacchiera, coord_dest, True)

    assert pezzo is None


def test_muovi_success():
    """Verifica che muovi sposti un pezzo su una casella libera."""
    coord_start = Coordinata(2, 2)
    coord_dest = Coordinata(2, 3)
    pedone = Pedone("P", coord_start, True)
    scacchiera = Scacchiera({coord_start: pedone})

    control = PieceControl()
    successo = control.muovi(scacchiera, pedone, coord_dest)

    assert successo is True
    assert pedone.init == coord_dest
    assert coord_start not in scacchiera.pezzi_vivi
    assert scacchiera.pezzi_vivi[coord_dest] == pedone


def test_muovi_fail_casella_occupata():
    """Verifica che muovi fallisca se la destinazione è occupata."""
    coord_start = Coordinata(2, 2)
    coord_dest = Coordinata(2, 3)
    pedone = Pedone("P", coord_start, True)
    altro_pedone = Pedone("P", coord_dest, False)
    scacchiera = Scacchiera({coord_start: pedone, coord_dest: altro_pedone})

    control = PieceControl()
    successo = control.muovi(scacchiera, pedone, coord_dest)

    assert successo is False
    assert pedone.init == coord_start
    assert scacchiera.pezzi_vivi[coord_start] == pedone
    assert scacchiera.pezzi_vivi[coord_dest] == altro_pedone
