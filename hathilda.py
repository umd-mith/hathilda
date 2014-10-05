#!/usr/bin/env python

import re
import sys
import requests
import xml.etree.ElementTree as etree

def main():
    """
    Read a list of HathiTrust URLs in a file and print out the JSON-LD
    for them on stdout.
    """
    filename = sys.argv[1]
    for url in open(filename):
        item = get(url)
        print item

def get(record_url):
    """
    Get a HathiTrust record and return it as JSON-LD
    """
    record_id = record_url.split('/')[-1]
    response = _get_hathi_record(record_id)
    # hopefully just need the first record since we are looking up
    # with the hathi record id?
    first_id = response['records'].keys()[0]
    xml = response['records'][first_id]['marc-xml']
    return _extract(xml)


def _extract(xml):
    """
    Parse MARC XML and return JSON-LD.
    """
    doc = etree.fromstring(xml.encode('utf8'))
    i = {}
    i['title'] = _title(doc)
    i['creator'] = _creator(doc)
    i['contributor'] = _contributor(doc)
    i['subject'] = _subject(doc)
    #i['datePublished'] = _datePublished(doc)

    return i

def _get_hathi_record(record_id):
    url = 'http://catalog.hathitrust.org/api/volumes/full/recordnumber/%s.json' % record_id
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

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
    return s

def _first(doc, path):
    e = doc.find(path)
    if e != None:
        return e.text
    else:
        return ''

def _list(doc, path):
    return [e.text for e in doc.findall(path)]

def _stripl(l):
    """
    Strips AACR2 punctuation from strings in a list.
    """
    return [_strip(s) for s in l]

def _strip(s):
    """
    Strips AACR3 punctuation from a string.
    """
    s = s.strip()
    return re.sub(r' ?[.,/]$', '', s)

if __name__ == "__main__":
    main()
