#!/usr/bin/env python
from pyquery import PyQuery
import HTMLParser
import os
import multiprocessing
import csv
import re

NUM_FIELDS = 8
NAME_PATTERN = re.compile(r"/([-\w]+).html$")

def query_page(htmlFilePath):
    clean_name = lambda x: x.replace('\r\n', '').replace(' ', '').strip()
    
    pyQuery = PyQuery(filename=htmlFilePath)
    dds = pyQuery("#companyInfo dd")
    result = []

    try:
        result.append(NAME_PATTERN.search(htmlFilePath).group(1))
    except Exception as e:
        print e
        print htmlFilePath

    for dd in dds: 
        result.append(clean_name(dd.text))

    try:
        assert len(result) == NUM_FIELDS
    except:
        return None
    else:
        return tuple(result)

def get_files(path='output'):
    all_files = []
    for path, dirs, files in os.walk(path):
        all_files += map(lambda s: os.path.join(path, s), files)

    return all_files


files = get_files()
pool = multiprocessing.Pool(processes=20)
result = pool.map(query_page, files)
print "proceed: %s" % len(result)
result = filter(lambda x:x, result)
print "fetched: %s" % len(result)


with open('results.csv', 'wb') as csvfile:
    csvwriter = csv.writer(csvfile)

    for r in result:
        csvwriter.writerow([s.encode('utf-8') for s in r])


