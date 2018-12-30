import urllib3
from bs4 import BeautifulSoup
import re

"""Find articles that are about refugees detained on Nauru from the Guardian's website.
"""

"""Retrieve articles that are 'directly about' refugees on Nauru. 'Directly about' is defined as a search query."""
searchURL = "https://news.google.com/news/rss/search/section/q/nauru+refugee+guardian/nauru+refugee+guardian?hl=en-AU&gl=AU&ned=au" # definition of 'directly about'
http = urllib3.PoolManager()
searchResults = http.request('GET', searchURL)
searchResults = searchResults.data.decode("utf-8")
soup = BeautifulSoup(searchResults, "xml")

"""Store all URL's of articles retrieved in a 1-dimensional list."""
links = soup.find_all('link')
urls = []
for link in links:
    url = link.get_text()
    validUrl = re.search('www.theguardian.com', url)
    if validUrl:
        urls.append(url)

"""Find all 'directly relevant' sentences from within all news articles found.
"""

http = urllib3.PoolManager()
validSentencesAll = []
for url in urls:

    """Get all text from news article."""
    page = http.request('GET', url)
    page = page.data.decode("utf-8")
    soup = BeautifulSoup(page, 'html.parser')
    textRaw = str(soup.find_all('p'))

    """Clean gotten text."""
    text = re.sub('<.*?>', '', textRaw) # remove all HTML markup
    text = re.sub('(?<=\.),', '', text) # remove comma directly after full-stop
    text = re.sub('(?<=\.\u201d),', '', text) # remove comma after closing quotation mark that's directly proceeded by a full-stop
    n = text.rfind('\n') # remove everything before last '\n' character
    if n != -1:
        text = text[(n+3):]

    """Store 'directly relevant' sentences from within text in a 2-dimensional list. 'Directly relevant' is defined as a search query."""
    sentencesRaw = re.split('(?<=.\.|.\?|\.\u201d) ', text) # get each sentence as its own element in a list
    validSentences = []
    for sentence in sentencesRaw:
        validSentence = re.search('refugee', sentence) # definition of 'directly relevant'
        if validSentence:
            validSentences.append(sentence)
    validSentencesAll.append(validSentences)

"""Clean list containing directly relevant sentences."""
validSentencesAll.remove([])

"""Combine directly relevant sentences randomly into a single paragraph."""
# TODO: combine into single 1-dimensional list then random.shuffle(list) twice

"""Add article hyperlinks to respective sentences within paragraph."""
# TODO: design algorithm

"""Display paragraph on a single page website."""
#def application(environ, start_response):
    # status = '200 OK'
    # output = b'output.'

    # response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
    # start_response(status, response_headers)

    # return [output]