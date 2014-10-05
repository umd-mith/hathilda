# hathilda

[![Build Status](https://travis-ci.org/umd-mith/hathilda.svg)](http://travis-ci.org/umd-mith/hathilda)

hathilda helps you get [HathiTrust](http://www.hathitrust.org/home) metadata records as JSON-LD. The JSON-LD is not intended to be comprehesive at this time. hathilda is largely a proof of concept that's used for getting HathiTrust metadata into OpenRefine, where records can be edited, and those edits can be serialized using [OpenAnnotation](http://www.openannotation.org/spec/core/).

If you want to learn more please visit the MITH/HTRC [project page](http://mith.umd.edu/mith-awarded-hathitrust-research-center-grant/).

## Example

Most of the time you'll probably want to use hathilda in your own program:

```python

import hathilda

o = hathilda.get('http://catalog.hathitrust.org/Record/001387595')
print o['title']
```

You can use hathilda.py from the command line, for example:

```
./hathilda.py http://catalog.hathitrust.org/Record/001387595
```

```javascript
{
  "@id": "http://catalog.hathitrust.org/Record/001387595",
  "@context": {
    "@vocab": "http://purl.org/dc/terms/"
  },
  "title": "Tractatus logico-philosophicus",
  "creator": "Wittgenstein, Ludwig",
  "publisher": "Harcourt, Brace",
  "issuance": "1922",
  "subject": [
    "Language and languages -- Philosophy",
    "Logic, Symbolic and mathematical"
  ],
  "description": [
    "Geman and English on opposite pages.",
    "Includes index.",
    "Originally published in German in Annalen der Naturphilosophie, 1921 under title: Logisch-Philosophische Abhandlung.",
    "Mode of access: Internet."
  ]
}
```

