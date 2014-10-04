#!/usr/bin/env python

import requests
import xml.etree.ElementTree as etree


def get(ht_id):
    hr = _get_hathi_record(ht_id)
    # hopefully just need the first record since we are looking up 
    # with hathi id?
    first_id = hr['records'].keys()[0]
    marc_xml = hr['records'][first_id]['marc-xml']
    return _extract(marc_xml)

def _extract(s):
    doc = etree.fromstring(s.encode('utf8'))
    i = {}
    _get_title(doc)
    i['title'] = _get_title(doc)
    # titles
    # authors
    # publication_date
    # subjects

    return i

def _get_hathi_record(ht_id):
    url = 'http://catalog.hathitrust.org/api/volumes/full/htid/%s.json' % ht_id
    r = requests.get(url)
    return r.json()

def _get_title(doc):
    return _text(doc, ".//record/datafield[@tag='245']/subfield[@code='a']")

def _text(doc, path):
    return [e.text for e in doc.findall(path)]

