import json

import lxml.html

def crawl_haikus():
    ROOT_URL = 'http://www.ahapoetry.com/aadoh'
    SUMMARY_URL = 'http://www.ahapoetry.com/aadoh/h_dictionary.htm'
    OUTPUT_FILENAME = 'haikus.json'

    tree = lxml.html.parse(SUMMARY_URL)

    haikus_dataset = dict()
    for link in tree.xpath('//a'):
        url = link.attrib['href']
        if 'mailto' in url or 'intro.htm' in url or 'index.htm' in url:
            continue
        print "Parsing: '{}'".format(url)
        page = lxml.html.parse('{}/{}'.format(ROOT_URL, url))

        title_elements = page.xpath('//font[@face="Book Antiqua, Times New Roman, Times"]/p/b')
        if not title_elements:
            title_elements = page.xpath('//font[@face="Times New Roman"]/p')
        title = title_elements[0].text_content()
        print "  . Title: {}".format(title)

        haikus = list()
        for paragraph in page.xpath('//p[@align="center"]'):
            text = paragraph.text_content().encode('utf8').replace('\r\n  ', '\r\n').rstrip('\xc2\xa0 ')
            if not text:
                continue
            haikus.append(text)
        haikus_dataset[title] = haikus
        print "  . Found {} haikus!".format(len(haikus))

    with open(OUTPUT_FILENAME, 'w') as output_file:
        json.dump(haikus_dataset, output_file)

    print ''
    print "Saved to '{}'.".format(OUTPUT_FILENAME)

def crawl_seasonal_words():
    WORDS_URL = 'http://www.2hweb.net/haikai/renku/500ESWd.html'
    SEASONAL_FILENAME = 'seasonal.json'

    tree = lxml.html.parse(WORDS_URL)

    dataset = dict()
    last_title = None
    for paragraph in tree.xpath('//p'):
        bold_elements = paragraph.xpath('b')
        if bold_elements and '--' in bold_elements[0].text_content():
            if last_title is not None:
                print "    > {} words".format(len(dataset[last_title]))
            last_title = bold_elements[0].text_content()
            dataset[last_title] = list()
            print ". Parsing '{}'".format(last_title)

        if last_title is None:
            continue

        if paragraph.xpath('i') and paragraph.xpath('a'):
            text = paragraph.text_content()
            text = text.split('(')[0].replace('*', '').replace('[', '').replace(']', '')
            tokens = text.split('/')
            for token in tokens:
                dataset[last_title].append(token.strip())
    print "    > Parsed {} seasonal words".format(len(dataset[last_title]))

    with open(SEASONAL_FILENAME, 'w') as output_file:
        json.dump(dataset, output_file)

    print ''
    print "Saved to '{}'.".format(SEASONAL_FILENAME)

if __name__ == '__main__':
    crawl_haikus()
    crawl_seasonal_words()