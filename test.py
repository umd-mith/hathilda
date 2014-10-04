import pytest
import hathilda

def test_get_volume():
    r = hathilda.get('ucm.5305727634')
    assert r['title'] == ['Canon medicinae (latine), a Gerardo Cremonensi translatus ;']

