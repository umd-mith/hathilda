# hathilda

[![Build Status](https://travis-ci.org/umd-mith/hathilda.svg)](http://travis-ci.org/umd-mith/hathilda)

hathilda helps you get [HathiTrust](http://www.hathitrust.org/home) volume
metadata records as JSON-LD. At the moment only simple Dublin Core is 
emitted. If you have suggestions on additional vocabularies to use, or 
other improvements please file an issue ticket!

## Example

Here's how you can use hathilda:

```python

import json
import hathilda

v = hathilda.get_volume('mdp.39015001539116')
print json.dumps(v, indent=2)
```

Which will output:

```javascript
{
  "@context": {
    "@vocab": "http://purl.org/dc/terms/",
    "ore": "http://www.openarchives.org/ore/terms/"
  },
  "@id": "http://hdl.handle.net/2027/mdp.39015001539116",
  "title": "Tractatus logico-philosophicus",
  "creator": "Wittgenstein, Ludwig",
  "publisher": "Harcourt, Brace",
  "issuance": "1922",
  "subject": [
    "Language and languages -- Philosophy",
    "Logic, Symbolic and mathematical"
  ],
  "description": [
    "German and English on opposite pages.",
    "Includes index.",
    "Originally published in German in Annalen der Naturphilosophie, 1921 under title: Logisch-Philosophische Abhandlung.",
    "Mode of access: Internet."
  ],
  "identifier": "http://catalog.hathitrust.org/Record/001387595",
  "provenance": "University of Michigan",
  "rights": "pdus",
  "ore:aggregates": {
    "@id": "http://babel.hathitrust.org/cgi/imgsrv/download/pdf?id=mdp.39015001539116;orient=0;size=100",
    "format": "application/pdf"
  }
}
```

When you install hathilda you should also get a command line program 
`hathilda.py` which you can pass a HathiTrust volume id, and which will
print the JSON-LD to stdout:

    % hathilda.py mdp.39015001539116 > mdp.39015001539116.json
