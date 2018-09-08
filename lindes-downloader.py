# doing a hack-ish test implementation of a fetcher, as example code for
# the basic process of how a downloader might look...  Not written to be
# clean, it was done fairly interactively while testing the 'praw'
# interface.  Cleanup (or re-write by Sveta ;)) desired.

import praw
import os
# from requests import Session
import auth # from local dir
import json

# session = Session()
reddit = praw.Reddit(client_id=auth.client_id, user_agent='domestic_violence_project',client_secret=auth.client_secret)
# TODO: figure out how to get the next batch:
submissions = reddit.subreddit('emotionalabuse').new(limit=100)

# during debugging, we were saving this as a list... could probably get
# rid of this:
sub_list = []
for sub in submissions:
    sub_list.append(sub)

first_sub = sub_list[0]

def save_sub(submission):
    """Function to (possibly) save JSON data for a Submission object."""

    # Note: may need to create these directories.
    path = "data/reddit/{}.json".format(submission.fullname)
    if os.path.isfile(path):
        print "Already have {}, skipping".format(path)
        return

    # get rid of and/or transmogrify some stuff into something we can
    # serialize as JSON:
    d = submission.__dict__.copy()
    d['subreddit'] = d['subreddit'].__dict__.copy()
    del(d['subreddit']['_reddit'])
    del(d['_reddit'])
    if d['author']:
        d['author'] = d['author'].__dict__.copy()
        del(d['author']['_reddit'])

    # In case more work is needed on the above, here's code for
    # debugging dumps errors:

    # for k,v in d.items():
      # print "k, v = {}, {}".format(k,v)
      # json.dumps({k:v})

    json_data = json.dumps(d)

    # saving as JSON.  Text conversion will be done later by a separate
    # process.
    print("Writing JSON data to to {}".format(path))
    with open(path, "w") as f:
        f.write(json_data)

# Now save the files:
for sub in sub_list:
    save_sub(sub)
