import praw
import sys
import time

def main():
    # Read the subreddit name from the subreddit.txt file
    with open("subreddit.txt", "r") as file:
        subreddit_name = file.read().strip()

    # Initialize a Reddit instance and go to the specified subreddit
    reddit = praw.Reddit(client_id='',
                         client_secret='',
                         username='',
                         password='',
                         user_agent='newuseragent')
    subreddit = reddit.subreddit(subreddit_name)

    # Get the top 3 posts of the day that were posted within the last 3 hours
    current_time = int(time.time())
    three_hours_ago = current_time - 20800  # within last 3 hours

#three_hours_ago = 0  # Remove within last 3 hour.
#three_hours_ago = current_time - 10800  # 10800 seconds = 3 hours #within last hour limit

    top_posts = [post for post in subreddit.new(limit=100) if post.created_utc > three_hours_ago][:30]

    # Store the comment details in a list
    comment_details = []
    count = 0
    for post in top_posts:
        for comment in post.comments:
            if isinstance(comment, praw.models.Comment) and comment.score >= 20:
                if len(comment.replies) <= 2:
                    all_replies = comment.replies
                    reply_count = 0
                    for reply in all_replies:
                        if not isinstance(reply, praw.models.MoreComments):
                            if len(reply.replies) == 0:
                                reply_count += 1
                    if reply_count == len(all_replies):
                        comment_details.append("Comment link: https://www.reddit.com" + comment.permalink + 
                                                "\nScore: " + str(comment.score) + 
                                                "\nNumber of replies: " + str(len(all_replies)) +
                                                "\nReplies to replies count: " + str(reply_count))
                        count += 1
                        sys.stdout.write("\r" + "Matching comments found: " + str(count))
                        sys.stdout.flush()

    # Write the comment details to the comments.txt file
    with open("comments.txt", "w") as file:
        file.write("\n".join(comment_details))

if __name__ == "__main__":
    main()
