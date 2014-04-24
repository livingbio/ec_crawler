#!/usr/bin/env python
"""
Get all pages back
"""
import urllib
import multiprocessing

MENU_LINK = "https://tw.mall.yahoo.com/merchant_homepage?catid=0&searchby=sname&sort_by=&order_by=0&searchby=sname&apg={0}"
MENU_LAST_PAGE = 72

def getPage(page, output_folder="./output"):
    """
    url: url of the page to fetch
    page: page number
    """
    url = MENU_LINK.format(page)

    print "fetching %s..." % url, 
    try:
        content = urllib.urlopen(url).read()
        with open("%s/%s.html" % (output_folder, page), 'w') as fp:
            fp.write(content)
    except Exception as e:
        print e, e.message
        print False
        return False
    else:
        print True
        return True


if __name__ == '__main__':
    pageNums = range(1, MENU_LAST_PAGE + 1)

    pool = multiprocessing.Pool(processes=30)
    result = pool.map(getPage, pageNums)

    print "total: %s" % len(result)
    print "fetched: %s" % len(filter(lambda x:x, result))

        
        

