#! /usr/bin/env python

import urllib
from xml.dom import minidom, Node
import json

#1)get daa from internet archive in json format 2)clean the json to get identifier, format, title, date, and description
ka_archive_json = 'http://www.archive.org/advancedsearch.php?q=collection%3A%22khanacademy%22&fl%5B%5D=collection&fl%5B%5D=date&fl%5B%5D=description&fl%5B%5D=format&fl%5B%5D=identifier&fl%5B%5D=publicdate&fl%5B%5D=title&sort%5B%5D=&sort%5B%5D=&sort%5B%5D=&rows=2735&page=1&output=json'

json_dictionary = json.load(urllib.urlopen(ka_archive_json))

docs = json_dictionary['response']['docs']

clean = {}

for doc in docs:
  identifier = doc['identifier']
  clean[identifier] = {}

  clean[identifier]['format'] = doc['format']

  clean[identifier]['title'] = doc['title']

  clean[identifier]['publicdate'] = doc['publicdate']
  
  if doc.has_key('description'):
    clean[identifier]['description'] = doc['description']
  else:
    clean[identifier]['description'] = "No decsription available"

print clean

print len(clean)

