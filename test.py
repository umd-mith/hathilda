import hathij
import pytest

def test_get_volume():
    r = hathij.get('ucm.5305727634')
    assert r['title'] == ['Canon medicinae (latine), a Gerardo Cremonensi translatus ;']

