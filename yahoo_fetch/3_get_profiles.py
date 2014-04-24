#!/usr/bin/env python
"""
Get all pages back
"""
import urllib
import multiprocessing
import fileinput
import re
import time
import random
import sys

N = 1
GETNAME = re.compile(r'sid=(.*)')


def getPage(url, output_folder="./output_profiles"):
    """
    url: url of the page to fetch
    """
    global N
    name = GETNAME.search(url).group(1)

    # random sleeping for avoiding spider detection
    timeToSleep = random.randint(1, 30)
    time.sleep(timeToSleep)
    
    print "%4d: fetching %s..." % (N, url.strip()), 

    # fetch the webpage
    try:
        content = urllib.urlopen(url).read()
    except Exception as e:
        print e, e.message
        return False

    # this is the crawler-blocking page, raise Exception, because this ip is banned
    if len(content) == 4068:
        # TODO: send message to hubot
        raise Exception("No.%s not fetched, encountered 999 error, our spider got blocked." % N)

    with open("%s/%04d_%s.html" % (output_folder, N, name), 'w') as fp:
        fp.write(content)

    N += 1
    print "fetched %s bits" % len(content)
    return True


if __name__ == '__main__':
    links = []

    for line in fileinput.input():
        links.append(line)

    startPage = 1

    links = links[startPage - 1:]
    links = links[:5]  # DEBUG: only 5 test cases

    N = startPage

    result = map(getPage, links)

    print "total: %s" % len(result)
    print "fetched: %s" % len(filter(lambda x: x, result))
