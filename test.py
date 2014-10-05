import pytest
import hathilda

def test_get_volume():
    r = hathilda.get('http://catalog.hathitrust.org/Record/009649975')
    assert r['@id'] == 'http://catalog.hathitrust.org/Record/009649975'
    assert r['@context'] == {'@vocab': 'http://purl.org/dc/terms/'}
    assert r['title'] == 'Canon medicinae (latine), a Gerardo Cremonensi translatus ; De viribus cordis (latine), ab Arnaldo de Villa Nova translatum'
    assert r['creator'] == 'Avicena'
    assert r['contributor'] == [
        'Herbort, Johannes',
        'Arnau de Vilanova',
        'Gerardus Cremonensis',
    ]
    assert r['subject'] == ['Medicina -- Obras anteriores a 1800']
    assert r['issuance'] == '1479'
    assert r['publisher'] == '[Johannes Herbort]'
