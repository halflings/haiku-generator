import json

import lxml.html

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