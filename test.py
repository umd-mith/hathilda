import pytest
import logging
import hathilda

logging.basicConfig(filename='test.log', level=logging.DEBUG)

def test_get_volume():
    r = hathilda.get_volume('ucm.5305727634')
    assert r['@context'] == {
        '@vocab': 'http://purl.org/dc/terms/',
        'ore': 'http://www.openarchives.org/ore/terms/'
    }
    assert r['@id'] == 'http://hdl.handle.net/2027/ucm.5305727634'
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
    assert r['identifier'] == 'http://catalog.hathitrust.org/Record/009649975'
    assert r['provenance'] == 'Universidad Complutense de Madrid'
    assert r['rights'] == 'pd'
    assert r['ore:aggregates'] == {
        '@id': 'http://babel.hathitrust.org/cgi/imgsrv/download/pdf?id=ucm.5305727634;orient=0;size=100',
        'format': 'application/pdf'
    }

def test_error():
    # this one causes an error in the HathiTrust API, which causes a 
    # 200 OK to come back with HTML instead of JSON. get_volume should
    # return None on these sorts of errors
    r = hathilda.get_volume('mdp.39015062249209')
    assert r == None
