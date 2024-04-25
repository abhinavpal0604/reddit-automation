import praw
import datetime

# Function to calculate the time difference between two dates in a human-readable format
def human_readable_time_difference(start_date, end_date):
    time_difference = end_date - start_date
    days = time_difference.days
    hours = time_difference.seconds // 3600

    if days > 0:
        return f"{days} day{'s' if days > 1 else ''}"
    else:
        return f"{hours} hour{'s' if hours > 1 else ''}"

# Get the current date and time
current_datetime = datetime.datetime.now()

# Initialize Reddit API credentials
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     username='',
                     password='',
                     user_agent='YOUR_USER_AGENT')

# Read usernames from file
with open('usernames.txt') as f:
    usernames = f.readlines()

# Remove whitespace and newlines from each username
usernames = [u.strip() for u in usernames]

# Loop through each username and get account creation date
print("Current date and time:", current_datetime.strftime("%Y-%m-%d %H:%M:%S"))
for username in usernames:
    shadowbanned = False
    try:
        user = reddit.redditor(username)
        created_datetime = datetime.datetime.fromtimestamp(user.created_utc)
        account_age = human_readable_time_difference(created_datetime, current_datetime)

        print(f"{username} Age: {account_age}")
        comment_count = 0
        for comment in reddit.redditor(username).comments.new(limit=None):
            comment_count += 1
            comment_age = human_readable_time_difference(datetime.datetime.fromtimestamp(comment.created_utc), current_datetime)
            print(f"Comment posted {comment_age} ago")

        print(f"Comment Count: {comment_count}")
    except:
        print(f"{username} is SHADOWBANNED/SUSPENDED")
        shadowbanned = True
