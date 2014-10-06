#!/usr/bin/env python

import re
import sys
import json
import requests
import xml.etree.ElementTree as etree

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

    j = _extract(xml)
    if not j:
        return None
    j['@id'] = 'http://catalog.hathitrust.org/Record/%s' % record_id
    j['@context'] = {'@vocab': 'http://purl.org/dc/terms/'}

    return j

def main():
    """
    Read a list of HathiTrust URLs in a file and print out the JSON-LD
    for them on stdout. Or if a single URL is passed in that record
    will be retrieved and printed on stdout.
    """
    filename = sys.argv[1]
    if filename.startswith('http://'):
        print json.dumps(get(filename), indent=2)
    else:
        print "["
        first = True
        for url in open(filename):
            url = url.strip()
            if not first:
                print ","
            first = False
            item = get(url)
            item.pop('@context')
            print json.dumps(item, indent=2),
        print "]"


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
    i['spatial'] = _spatial(doc)
    i['description'] = _description(doc)
    i['issuance'] = _issuance(doc)
    i['publisher'] = _publisher(doc)

    # remove empty values
    for k, v in i.items():
        if v == [] or v is None or v == '':
            i.pop(k)

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
    main()
