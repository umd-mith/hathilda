#!/usr/bin/env python

from __future__ import print_function

import re
import sys
import json
import backoff
import logging
import requests
import xml.etree.ElementTree as etree

from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException

http = requests.Session()
http.headers.update({'user-agent': 'hathilda <http://github.com/umd-mith/hathilda'})
http.mount('http://catalog.hathitrust.org', HTTPAdapter(max_retries=10))

def get_volume(vol_id):
    """
    Get a HathiTrust volume as JSON-LD.
    """
    response = _get_catalog_record(vol_id)
    if not response:
        return None

    # get volume specific information from the API response
    vol = _extract_vol(response, vol_id)

    # get additional metadata from the marc record in the API response
    first_id = list(response['records'].keys())[0]
    xml = response['records'][first_id]['marc-xml']
    _extract_marc(vol, xml)

    # remove any keys that have no value
    return _remove_empty(vol)


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

@backoff.on_exception(backoff.expo, RequestException, max_tries=10)
def _get_catalog_record(vol_id):
    """
    Return JSON for catalog record from HathiTrust API.
    """
    logging.info("getting record from api: %s", vol_id)
    url = 'http://catalog.hathitrust.org/api/volumes/full/htid/%s.json' % vol_id
    resp = http.get(url)
    resp.raise_for_status()
    try:
        return resp.json()
    except ValueError:
        logging.error("unable to get json from %s", url)
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
    Strips AACR2 punctuation from a string.
    """
    if not s:
        return s
    # remove leading trailing whitespace
    s = s.strip()
    # the negative lookbehind (?<! [A-Z]) is to prevent removing trailing 
    # periods from initialized names, e.g. Zingerman, B. I.
    return re.sub(r'(?<! [A-Z]) ?[.;,/]$', '', s)

if __name__ == "__main__":
    logging.basicConfig(filename='hathilda.log', level=logging.INFO)
    vol_id = sys.argv[1]
    print(json.dumps(get_volume(vol_id), indent=2))

