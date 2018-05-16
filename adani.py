import urllib3
from bs4 import BeautifulSoup
import re

# finds news articles that are about Adani from the Guardian's website
searchURL = "https://news.google.com/news/rss/search/section/q/adani+guardian/adani+guardian?hl=en-AU&gl=AU&ned=au"
http = urllib3.PoolManager()
searchResults = http.request('GET', searchURL)
searchResults = searchResults.data.decode("utf-8") # transform to regular string
soup = BeautifulSoup(searchResults, "xml")
links = soup.find_all('link')
urls = []
for link in links:
    url = link.get_text()
    # only retrieve articles from Guardian website
    validUrl = re.search('www.theguardian.com', url)
    if validUrl:
        urls.append(url)

# gets all quotes from all news articles found
http = urllib3.PoolManager()
quotesAllRaw = []
for url in urls:
    # get text from news website
    page = http.request('GET', url)
    page = page.data.decode("utf-8") 
    soup = BeautifulSoup(page, 'html.parser')
    text = str(soup.find_all('p'))
    # find all quotes in text
    quotesRaw = []
    textSplitList = re.split('\u201c', text)
    for textSplit in textSplitList:
        quoteList = re.split('\u201d', textSplit)
        quotesRaw.append(quoteList[0])
    quotes = quotesRaw[1:]
    quotesAllRaw.append(quotes) # 2-D list of list of quotes

# cleans quotes data by removing empty quotes, HTML markup from within quote, then whitespace/comma/full-stop from only end of quote
quotesAll = []   
for elementRaw in quotesAllRaw:
    element = []
    if elementRaw:
        for j in range(len(elementRaw)):
            elementRaw[j] = re.sub('<.*?>', '', elementRaw[j])
            elementRaw[j] = elementRaw[j].rstrip()
            elementRaw[j] = re.sub('[.,]$', '', elementRaw[j])
            element.append(re.sub('[.,]$', '', elementRaw[j]))
        quotesAll.append(element)

# TODO: get only the quotes that have 'Adani'/'project'/'it' as part of that quote. NOTE: this may induce empty list elements in quotesAll

# TODO: randomise quotes order then combine into single quote string. DEV: combine into single 1-D list then random.shuffle(list) twice

# TODO: add news article hyperlinks to each quote within single quote string

# TODO: send quote string as a single page to web browser
#def application(environ, start_response):
    # status = '200 OK'
    # output = b'output.'

    # response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
    # start_response(status, response_headers)

    # return [output]