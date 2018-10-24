import urllib3
from bs4 import BeautifulSoup
import re

# finds news articles that are about refugees detained on Nauru from the Guardian's website. Each news articles' URL stored as an element in a 1-dimensional list.
searchURL = "https://news.google.com/news/rss/search/section/q/nauru+refugee+guardian/nauru+refugee+guardian?hl=en-AU&gl=AU&ned=au"
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

# find all 'directly relevant' sentences from within all news articles found. Each sentence stored as an element in a 2-dimensional list.
http = urllib3.PoolManager()
validSentencesAll = []
for url in urls:
    # get all text from news article
    page = http.request('GET', url)
    page = page.data.decode("utf-8")
    soup = BeautifulSoup(page, 'html.parser')
    textRaw = str(soup.find_all('p'))
    # clean gotten text
    text = re.sub('<.*?>', '', textRaw) # remove all HTML markup
    text = re.sub('(?<=\.),', '', text) # remove comma directly after full-stop
    text = re.sub('(?<=\.\u201d),', '', text) # remove comma after closing quotation mark that's directly proceeded by a full-stop
    n = text.rfind('\n') # remove everything before last '\n' character
    if n != -1:
        text = text[(n+3):]
    # find relevant sentences from within text
    sentencesRaw = re.split('(?<=.\.|.\?|\.\u201d) ', text) # get each sentence as its own element in a list
    validSentences = []
    for sentence in sentencesRaw:
        validSentence = re.search('refugee', sentence) # definition of 'directly relevant'
        if validSentence:
            validSentences.append(sentence)
    validSentencesAll.append(validSentences)
validSentencesAll.remove([]) # remove all empty elements

# TODO: combine all sentences randomly into a single paragraph. DEV: combine into single 1-dimensional list then random.shuffle(list) twice

# TODO: add news article hyperlinks to each sentence within paragraph

# TODO: display paragraph on a single page within web browser
#def application(environ, start_response):
    # status = '200 OK'
    # output = b'output.'

    # response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
    # start_response(status, response_headers)

    # return [output]