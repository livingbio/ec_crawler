import fileinput
import csv
import multiprocessing
import re
import os
import urllib

URL_PATTERN = re.compile(r"([\w-]+).shop.rakuten.tw")
URL_POSTFIX = "owner/"
OUTPUT_DIR = "output"


def get_info(input_iterator):
    """
    Returns:
    (url, name)
    """
    result = []
    for line in input_iterator:
        url = line.strip() + URL_POSTFIX
        print url
        resultItem = (url, URL_PATTERN.search(url).group(1))
        result.append(resultItem)
    return result

def fetch_page(info):
    try:
        url = info[0]
        name = info[1]
        
        print "fetching %s..." % name
        content = urllib.urlopen(url).read()

        with open("%s/%s.html" % (OUTPUT_DIR, name), 'w') as fp:
            fp.write(content)
    except:
        print "failed: %s" % name
        return False
    else:
        print "succeed"
        return True


if __name__ == '__main__':
    infos = get_info(fileinput.input())

    pool = multiprocessing.Pool(processes=30)
    result = pool.map(fetch_page, infos)

    print "total: %s" % len(result)
    print "fetched: %s" % len(filter(lambda x:x, result))

