"""Tests for the InterfacciaUtente class."""

import os
import sys

import pytest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scacchi.Boundary.InterfacciaUtente import InterfacciaUtente


def test_ui_set_valid_accent_color():
    """Test setting a valid accent color."""
    ui = InterfacciaUtente()
    ui.set_accent("blue")
    assert ui.get_accent() == "blue"

    # Test another valid color
    ui.set_accent("bright_green")
    assert ui.get_accent() == "bright_green"


def test_ui_set_invalid_accent_color():
    """Test that setting an invalid accent color raises a ValueError."""
    ui = InterfacciaUtente()
    with pytest.raises(ValueError):
        ui.set_accent("invalid_color")


def test_ui_get_accent_color():
    """Test that get_accent returns the current accent color."""
    ui = InterfacciaUtente()
    ui.set_accent("cyan")
    assert ui.get_accent() == "cyan"
