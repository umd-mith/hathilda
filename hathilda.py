#!/usr/bin/env python

from __future__ import print_function

import re
import sys
import json
import requests
import xml.etree.ElementTree as etree

def get_volume(vol_id):
    """
    Get a HathiTrust volume as JSON-LD.
    """

    # determine catalog id for the volume and look it up in the HathiTrust API
    catalog_id = _get_catalog_id(vol_id)
    response = _get_catalog_record(catalog_id)

    # get volume specific information from the API response
    vol = _extract_vol(response, vol_id)

    # get additional metadata from the marc record in the API response
    first_id = list(response['records'].keys())[0]
    xml = response['records'][first_id]['marc-xml']
    _extract_marc(vol, xml)

    return _remove_empty(vol)

def _get_catalog_id(vol_id):
    """
    Get the HathiTrust catalog record id for a HathiTrust volume id.
    """
    resp = requests.get('http://babel.hathitrust.org/cgi/pt?id=' + vol_id)
    catalog_id = None
    if resp.status_code == 200:
        m = re.search(r'catalog.hathitrust.org/Record/(\d+)', resp.content.decode())
        if m:
            catalog_id = m.group(1)
    return catalog_id

def _extract_vol(response, vol_id):
    vol = {
        '@id': "http://hdl.handle.net/2027/%s" % vol_id,
        '@context': {
            '@vocab': 'http://purl.org/dc/terms/',
            'ore': 'http://www.openarchives.org/ore/terms/'
        }
    }
    for item in response['items']:
        if item['htid'] == vol_id:
            vol['provenance'] = item['orig']
            vol['rights'] = item['rightsCode']
    vol['ore:aggregates'] = {
        '@id': 'http://babel.hathitrust.org/cgi/imgsrv/download/pdf?id=%s;orient=0;size=100' % vol_id,
        'format': 'application/pdf'
    }
    return vol

def _extract_marc(vol, xml):
    """
    Parse MARC XML and return JSON-LD.
    """
    doc = etree.fromstring(xml.encode('utf8'))
    vol['title'] = _title(doc)
    vol['creator'] = _creator(doc)
    vol['contributor'] = _contributor(doc)
    vol['subject'] = _subject(doc)
    vol['spatial'] = _spatial(doc)
    vol['description'] = _description(doc)
    vol['issuance'] = _issuance(doc)
    vol['publisher'] = _publisher(doc)
    vol['identifier'] = _id(doc)

def _remove_empty(d):
    new_d = {}
    for k, v in d.items():
        if v is None or v == '' or len(v) == 0:
            continue
        else:
            new_d[k] = v

    return new_d

def _get_catalog_record(record_id):
    """
    Return JSON for catalog record from HathiTrust API.
    """
    url = 'http://catalog.hathitrust.org/api/volumes/full/recordnumber/%s.json' % record_id
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

def _id(doc):
    catalog_id = _first(doc, ".//record/controlfield[@tag='001']")
    return 'http://catalog.hathitrust.org/Record/' + catalog_id

def _title(doc):
    a = _first(doc, ".//record/datafield[@tag='245']/subfield[@code='a']")
    b = _first(doc, ".//record/datafield[@tag='245']/subfield[@code='b']")
    if b:
        t = a + ' ' + b 
    else:
        t = a
    return _strip(t)

def _creator(doc):
    return _strip(_first(doc, ".//record/datafield[@tag='100']/subfield[@code='a']"))

def _contributor(doc):
    return _stripl(_list(doc, ".//record/datafield[@tag='700']/subfield[@code='a']"))

def _subject(doc):
    s = []
    for e in doc.findall(".//record/datafield[@tag='650']"):
        s.append(' -- '.join(_list(e, 'subfield')))
    return _stripl(s)

def _spatial(doc):
    s = []
    for e in doc.findall(".//record/datafield[@tag='651']"):
        s.append(' -- '.join(_list(e, 'subfield')))
    return _stripl(s)

def _issuance(doc):
    f = _first(doc, ".//record/controlfield[@tag='008']")
    if f:
        return f[7:11]
    else: 
        return None

def _description(doc):
    d = []
    for e in doc.findall(".//record/datafield"):
        if 'tag' in e.attrib and e.attrib['tag'].startswith('5'):
            d.append(''.join(_list(e, 'subfield')))
    return d

def _publisher(doc):
    return _strip(_first(doc, ".//record/datafield[@tag='260']/subfield[@code='b']"))

def _first(doc, path):
    e = doc.find(path)
    if e != None:
        return e.text
    else:
        return ''

def _list(doc, path):
    l = [e.text for e in doc.findall(path)]
    return filter(lambda a: a is not None, l)

def _stripl(l):
    """
    Strips AACR2 punctuation from strings in a list.
    """
    return [_strip(s) for s in l]

def _strip(s):
    """
    Strips AACR3 punctuation from a string.
    """
    if not s:
        return s
    # remove leading trailing whitespace
    s = s.strip()
    # the negative lookbehind (?<! [A-Z]) is to prevent removing trailing 
    # periods from initialized names, e.g. Zingerman, B. I.
    return re.sub(r'(?<! [A-Z]) ?[.;,/]$', '', s)

if __name__ == "__main__":
    vol_id = sys.argv[1]
    print(json.dumps(get_volume(vol_id), indent=2))

