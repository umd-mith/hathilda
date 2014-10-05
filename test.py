import pytest
import hathilda

def test_get_volume():
    r = hathilda.get('009649975')
    assert r['title'] == 'Canon medicinae (latine), a Gerardo Cremonensi translatus ; De viribus cordis (latine), ab Arnaldo de Villa Nova translatum'
    assert r['creator'] == 'Avicena'
    assert r['contributor'] == [
        'Herbort, Johannes',
        'Arnau de Vilanova',
        'Gerardus Cremonensis',
    ]
    assert r['subject'] == ['Medicina -- Obras anteriores a 1800']
