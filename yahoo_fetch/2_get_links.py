import re

SHOPURL_PATTERN = re.compile(r'https://tw.mall.yahoo.com/store/[^<\ ;>]*"')
SHOPNAME_PATTERN = re.compile(r'.*/([^/]+)"$')
SHOPPROFILE_URL = "https://tw.user.mall.yahoo.com/booth/view/stIntroMgt?sid={0}"
PAGE_NUM = 72

def getShopIdsInPage(page):
    toShopName = lambda url: SHOPNAME_PATTERN.sub(r'\1', url)
    with open('output/%s.html' % page) as fp:
        content = fp.read()
        result = SHOPURL_PATTERN.findall(content)
    return set(map(toShopName, result))


def main():
    pages = range(1, PAGE_NUM+1)

    result = reduce(lambda a,b: set(list(a) + list(b)), map(getShopIdsInPage, pages))

    links = map(lambda s: SHOPPROFILE_URL.format(s), result)

    for l in links:
        print l

if __name__ == '__main__':
    main()



