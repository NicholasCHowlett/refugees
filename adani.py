import urllib3
import re
from bs4 import BeautifulSoup

## find The Guardian news articles that are about Adani
searchURL = "https://news.google.com/news/rss/search/section/q/adani+guardian/adani+guardian?hl=en-AU&gl=AU&ned=au"
http = urllib3.PoolManager()
searchResults = http.request('GET', searchURL)
searchResults = searchResults.data.decode("utf-8") # transform to regular string
searchResultsList = re.split('\http+', searchResults) # split XML file into list with each element starting with a URL address
searchResultsListTrim = []
searchResultsListTrim = searchResultsList[3:] # remove irrelevant data at start of list
urls = []
for searchResult in searchResultsListTrim:
	searchResultSplit= re.split('\/', searchResult) # get domain name
	searchResultURL = re.split('\"', searchResult) # get full URL
	matchNews = re.search('news', searchResultSplit[2])
	matchEncrypted = re.search('encrypted', searchResultURL[0])
	matchDouble = re.search('\<\/link>', searchResultURL[0])
	if not matchNews and not matchEncrypted and not matchDouble:
		searchResultURL = "http" + searchResultURL[0]
		urls.append(searchResultURL)

## get all quotes from all The Guardian news articles found
http = urllib3.PoolManager()
quotesAll = []
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
	quotesAll.append(quotes) #quotesAll is a list of list of quotes

# get only the quotes that have 'Adani'/'project'/'it' as part of that quote

# combine quotes into single quote string

# send quote string to web browser (single page)
#def application(environ, start_response):
    # status = '200 OK'
    # output = b'output.'

    # response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
    # start_response(status, response_headers)

    # return [output]