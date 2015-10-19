from bs4 import BeautifulSoup
import re
import requests

def contains_url(message):
	"""Check if a message contains an URL.

	Keyword argument:
	message -- message received from a channel or from a user
	"""
	pattern = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
	match = re.search(pattern, message)
	if match:
		return True
	return False

def get_url(message):
	"""Extract URL from a message.

	Keyword argument:
	message -- message received from a channel or from a user
	"""
	pattern = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
	match = re.search(pattern, message)
	return match.group(0)

def get_title(url):
    """Get HTML title from a specified URL.

    Keyword argument:
    url -- the URL to get the title from
    """
    if url.startswith('www'):
        url = 'http://' + url
    r = requests.request('GET', url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        if None != soup.title:
            return soup.title.string.encode('utf-8')
