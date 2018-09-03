# a simple test of parsing reddit documents with Python...

# first, some libraries:
from bs4 import BeautifulSoup
import requests

# then, what page are we getting?  Here's an arbitrary post, but this
# would probably be iterating over a list of links or something.
url = 'https://www.reddit.com/r/emotionalabuse/comments/9aua6c/my_mom_offered_me_money_to_help_me_move_but_when/'

# need user agent because otherwise we get a 429 error.
# See https://www.reddit.com/r/redditdev/comments/3qbll8/429_too_many_requests/
req = requests.get(url, headers = {'User-agent': 'Testing a thing'})

# req.content is the html content, and we now get a BeautifulSoup object parsing it:
soup = BeautifulSoup(req.content, 'html.parser')

# if we want, we could just print out the whole text of the page:
print soup.get_text()

# but more likely, we just want the appropriate div... which, by just
# looking at the "View Source" of the page and/or the "Inspector" in
# Chrome, for example, and comparing it to what was on the screen, we
# discovered that the wrapper divs that have the content (a post, though
# also a comment) we care about have a class on them called "gDUzzi" --
# presumably from minified (see
# https://en.wikipedia.org/wiki/Minification_(programming) ) whatever:
gduzzi = soup.find_all('div', 'gDUzzi')

# if we look at the length of that, we'll find that it has one entry for
# the main post, plus an entry for each comment (so for a post with 5
# comments, this will return 6)
len(gduzzi)

# so the actual post is this one:
post_div = gduzzi[0]

# and we can get it just as text:
text = post_div.get_text()

# we might also want to do something with the children:
children = post_div.children
# or even recursive children:
generator = post_div.recursiveChildGenerator()


for child in generator:
  print "CHILD:", child
  # this will fail because reasons, but we can talk about that sometime
  # if you like; there are ways to get the equivalent of it.:
  print "CHILD:", child.get_text()

# or just get the whole text, though there'll be weird merging of words
# across paragraph boundaries, etc.  That's what the above code is
# moving in the direction of solving (but doesn't quite, because we
# didn't finish it.)
text = post_div.get_text()

# one way or another, once we have the text, we can tokenize it.
# Perhaps as simply as this (though we might also want something more
# complex):
words = text.split()

# From there, we could come up with word counts:
counts = {}
for word in words:
  counts[word] = counts.get(word, 0) + 1

# or more probably you'll just feed the array to one of the other
# libraries for doing LDA or whatever.

# but if we did go with counts ourselves, we could then sort them, from
# least frequent to most:
sorted_word_and_counts = sorted(counts.items(), key = lambda x: x[1])

# and maybe print out just the 30 most common:
for pair in sorted_word_and_counts[-30:]:
  print pair[0], pair[1]

# or something like that.
