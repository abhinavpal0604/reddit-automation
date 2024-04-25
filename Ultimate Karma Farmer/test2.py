

import os
import praw

# Set the HTTPS_PROXY environment variable to your proxy URL
#os.environ['HTTPS_PROXY'] = 'http://dc.smartproxy.com:10002'


from requests import Session

session = Session()
session.proxies['https'] = 'http://dc.smartproxy.com:10002'
reddit = praw.Reddit(client_id='GFttyEkfEBG5DPTe2BsHIg',
                     client_secret='GY6jUgPwg5KQBbZbJ5ZNTnXxDKuKcQ',
                     username='OkActuary8437',
                     password='5QQAApbl2b',
                     user_agent='user_agent',
                     requestor_kwargs={'session': session},  # pass Session
)



# Use the Reddit API via PRAW as usual
subreddit = reddit.subreddit('learnpython')
for submission in subreddit.hot(limit=5):
    print(submission.title)
