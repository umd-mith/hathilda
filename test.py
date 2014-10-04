import pytest
import hathild

def test_get_volume():
    r = hathild.get('ucm.5305727634')
    assert r['title'] == ['Canon medicinae (latine), a Gerardo Cremonensi translatus ;']

