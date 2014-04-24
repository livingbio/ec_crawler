#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyquery import PyQuery
import HTMLParser
import os
import re
import csv
import sys

colon_unicode = u'\uff1a'
title_pattern = re.compile(u'.*\uff1a')

def getFiles(path='output_profiles'):
    """
    Get input files list
    """
    all_files = []
    for path, dirs, files in os.walk(path):
        all_files += map(lambda s: os.path.join(path, s), files)

    return all_files


def parsePage(filename):
    """
    Parse info in a given page
    input: filename
    output: tuple
    """
    def replaceTitle(i):
        return title_pattern.sub('', i)

    pq = PyQuery(filename=filename)
    lis = pq("#ypsinfo li")

    return tuple([ replaceTitle(li.text) for li in lis ])


def writeCSV(tuples):
    csvwriter = csv.writer(sys.stdout)
    for t in tuples:
        row = [ s.encode('utf-8') for s in t ]
        csvwriter.writerow(row)


if __name__ == '__main__':
    files = getFiles()
    results = map(parsePage, files)

    writeCSV(results)

