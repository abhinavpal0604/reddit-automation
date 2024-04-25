import praw
import random

reddit = praw.Reddit(
    client_id='GFttyEkfEBG5DPTe2BsHIg',
    client_secret='GY6jUgPwg5KQBbZbJ5ZNTnXxDKuKcQ',
    username='OkActuary8437',
    password='5QQAApbl2b',
    user_agent='your_user_agent_here'
)

subreddit = reddit.subreddit('test')
random_post = random.choice(list(subreddit.new(limit=10)))

comment_text = 'This is my comment!'
random_post.reply(comment_text)


