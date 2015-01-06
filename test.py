import pytest
import hathilda

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
         

def test_catalog_id():
    assert hathilda._get_catalog_id('hvd.hb16pk') == '000358054'
