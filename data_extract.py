from bs4 import BeautifulSoup
import requests

"""
Collecting all posts from https://www.reddit.com/r/emotionalabuse/

"""
# Create an output file for appending documents
f = open('raw_data.txt', 'a')

#headers with the user agent to avoid error 429
headers = {
    'User-Agent': 'Svetlana Krasikova',
    'From': 'svetakrasikova@me.com'
}

#A very ad-hoc method for collecting all urls from 'https://www.reddit.com/r/emotionalabuse/'

#list of urls
urls = []
top_url = 'https://www.reddit.com/r/emotionalabuse/'
top_url_content = requests.get(top_url, headers = headers).content
soup = BeautifulSoup(top_url_content, 'html.parser')
#they all have the class attribute "_3jOxDPIQ0KaOWpzvSQo-1s"
links = soup.find_all('a', attrs={"class":"_3jOxDPIQ0KaOWpzvSQo-1s"})
for link in links:
	urls.append(link['href'])

# Extract the post content from each of the resulting urls, again using an ad-hoc heuristics

for url in urls: 
	url_content = requests.get(url, headers = headers).content
	soup = BeautifulSoup(url_content, 'html.parser')	
	post_content = soup.find_all('div', attrs={"data-test-id":"post-content"})
	#if there is a post text on this url
	if len(post_content) > 0:
		#pick only the top post because this is the actual post, the following ones are comments
		for tag in post_content[0]:
			if 's1t8cjpc-0' in tag['class'] or 's1t8cjpc-4' in tag['class']:
				for word in tag.get_text().split():
					f.write(word.encode("utf8") + ', ')



#TODO 1 COLLECT ALL URLS
# Not all urls are captured currently, not sure how to capture all in a general way


#TODO 2
# Generalise the method for finding the post content, use more general heuristics

#TODO 3 CORRECT DOC REPRESENTATION
#Currently using mab of words for all docs, find out how to reprenset each doc for SCIKIT-LEARN
