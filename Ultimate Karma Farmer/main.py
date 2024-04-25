import praw
import random
from datetime import datetime
import openai
import time
import os
import pandas as pd
import threading
import traceback
import requests
from requests import Session


openai.api_key = "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"


def thread_main(username, password, client_id, client_secret, http_proxy):
    while True:
        try:
            main(username, password, client_id, client_secret, http_proxy)
        except Exception as e:
            with open('error_log.txt', 'a') as f:
                            f.write(f"[{username}]: Thread failed with error: {e}. Restarting thread with same arguments.\n")
                            traceback.print_exc(file=f)
                            
            #print(f"[{username}]: Thread failed with error: {e}. Restarting thread with same arguments.")
            continue


def main(username,password,client_id,client_secret,http_proxy=None):

    # Set up a Reddit instance using PRAW
    if http_proxy:

        session = Session()
        session.proxies['https'] = f'http://{http_proxy}'
        
    else:
        session = Session()
    
    # Authenticate with the Reddit API using the session with the headers and proxy (if specified)
    reddit = praw.Reddit(client_id=client_id,
                        client_secret=client_secret,
                        username=username,
                        password=password,
                        user_agent="YOUR_USER_AGENT",
                        requestor_kwargs={'session': session},  # pass Session,
    )

    def get_info():
        
        # get the Reddit user
        user = reddit.redditor(username)

        # get the user's link karma
        link_karma = user.link_karma

        # get the user's comment karma
        comment_karma = user.comment_karma

        # get the user's award karma
        awardee_karma = user.awardee_karma
        awarder_karma = user.awarder_karma

        # calculate the user's total karma
        total_karma = link_karma + comment_karma + awardee_karma + awarder_karma

        # get the user's account creation time
        created_utc = user.created_utc
        created_datetime = datetime.utcfromtimestamp(created_utc)

        # calculate the number of days since the account was created
        days_since_creation = (datetime.utcnow() - created_datetime).days

        # calculate the number of months since the account was created
        months_since_creation = int(days_since_creation / 30.44)

        # print the results
        print(f"[{username}]: Link karma: {link_karma}")
        print(f"[{username}]: Comment karma: {comment_karma}")
        print(f"[{username}]: Awardee karma: {awardee_karma}")
        print(f"[{username}]: Awarder karma: {awarder_karma}")
        print(f"[{username}]: Total karma: {total_karma}")
        print(f"[{username}]: Account created: {created_datetime}")
        print(f"[{username}]: Days since creation: {days_since_creation}")
        print(f"[{username}]: Months since creation: {months_since_creation}")
    

    def random_post_upvote():
        # Get a list of the top popular 100 SFW subreddits
        subreddit_list = [subreddit.display_name for subreddit in reddit.subreddits.popular(limit=100) if subreddit.over18 == False]

        # Select a random subreddit from the list
        random_subreddit = reddit.subreddit(random.choice(subreddit_list))

        # Select a random post from the hot section of the subreddit
        hot_posts = random_subreddit.hot(limit=10)
        random_post = random.choice([post for post in hot_posts])

        # Upvote the post
        random_post.upvote()

        # Print confirmation message
        print(f'[{username}]: Upvoted post "{random_post.id}" in r/{random_subreddit.display_name}')


    def random_post_upvote_with_comment_upvote():
       # Get a list of the top popular 100 SFW subreddits
        subreddit_list = [subreddit.display_name for subreddit in reddit.subreddits.popular(limit=100) if subreddit.over18 == False]

        # Select a random subreddit from the list
        random_subreddit = reddit.subreddit(random.choice(subreddit_list))

        # Select a random post from the hot section of the subreddit
        hot_posts = random_subreddit.hot(limit=10)
        random_post = random.choice([post for post in hot_posts])

        # Upvote the post
        random_post.upvote()

        # Print confirmation message
        print(f'[{username}]: Upvoted post "{random_post.id}" in r/{random_subreddit.display_name}')

        # Select a random comment (if there are any comments)
        if random_post.num_comments > 0:
            random_comments = random_post.comments[:3] # Only fetch first 3 comments
            random_comment = random.choice(random_comments)
            random_comment.upvote()
            print(f'[{username}]: Upvoted comment "{random_comment.id}" in post "{random_post.id}" in r/{random_subreddit.display_name}')
        
    def random_comment_upvote():
        # Get a list of the top popular 100 SFW subreddits
        subreddit_list = [subreddit.display_name for subreddit in reddit.subreddits.popular(limit=100) if subreddit.over18 == False]

        # Select a random subreddit from the list
        random_subreddit = reddit.subreddit(random.choice(subreddit_list))

        # Select a random post from the hot section of the subreddit
        hot_posts = random_subreddit.hot(limit=10)
        random_post = random.choice([post for post in hot_posts])

        # Select a random comment (if there are any comments)
        if random_post.num_comments > 0:
            random_comments = random_post.comments[:3] # Only fetch first 3 comments
            random_comment = random.choice(random_comments)
            random_comment.upvote()
            print(f'[{username}]: Upvoted comment "{random_comment.id}" in post "{random_post.id}" in r/{random_subreddit.display_name}')
        
    def random_comment():
        
        if reddit.redditor(username).link_karma + reddit.redditor(username).comment_karma > 50:

            # Read the subreddit names from subreddits.txt file
            with open("subreddits.txt") as f:
                subreddit_list = [line.strip() for line in f]

            # Initialize the post variable to None
            post = None

            while post is None:
                # Select a random subreddit from the list
                random_subreddit = reddit.subreddit(random.choice(subreddit_list))

                # Loop through the posts in the subreddit
                for p in random_subreddit.new():
                    # Check if the post meets the criteria
                    if p.num_comments < 5 and p.num_comments > 2 and p.score >= 10 and time.time() - p.created_utc < 20*60:
                        # Check if the post ID is not in the posts.txt file
                        if str(p.id) not in open("posts.txt").read():
                            # Save the post to the variable
                            post = p
                            break  # Exit the loop once a matching post is found

                # If no matching post is found, select a new random subreddit and continue the loop
                else:
                    continue

            post_content = f"{post.title}\n\n{post.selftext}"

            # Get 10 comments and its 2 replies on post and stores it
            all_comments = []

            # If an AttributeError is encountered, the code will not crash and will instead pass the error and continue running.
            # Loop through the top 10 comments
            for comment in post.comments[:10]:
                comment_data = {}
                try:
                    comment_data['text'] = comment.body
                    comment_data['replies'] = []
                except AttributeError:
                    pass

                # Loop through the first 2 replies to the comment
                for reply in comment.replies[:2]:
                    reply_data = {}
                    try:
                        reply_data['text'] = reply.body
                        comment_data['replies'].append(reply_data)
                    except AttributeError:
                        pass

                all_comments.append(comment_data)


            davinci_reply = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f'Generate Reddit Comment to subreddit: {post.subreddit} Post: {post_content}, here is some comments made on post: {all_comments}, use this to only guide your comment, but make your own judgement, the comment should get many upvotes.Dont always start your comment with Wow. Do not write comment in quotes. The comment must not look like it was generated by a bot. Generated Comment:',
                max_tokens=200,
                n=1,
                stop=None,
                temperature=0.5,
            )
            davinci_reply = davinci_reply.choices[0].text

            post.reply(davinci_reply)
            print(f'[{username}]: Random Comment Sent to "{post.id}" in r/{post.subreddit}')

            with open("posts.txt", "a") as file:
                file.write(post.id + "\n")


        else:
            # Read the subreddit names from subreddits.txt file
            with open("lowkarma_subreddits.txt") as f:
                subreddit_list = [line.strip() for line in f]

            # Initialize the post variable to None
            post = None

            while post is None:
                # Select a random subreddit from the list
                random_subreddit = reddit.subreddit(random.choice(subreddit_list))

                # Loop through the posts in the subreddit
                for p in random_subreddit.new():
                    # Check if the post meets the criteria
                    if p.num_comments < 10 and p.num_comments > 2 and p.score >= 2 and time.time() - p.created_utc < 40*60:
                        # Check if the post ID is not in the posts.txt file
                        if str(p.id) not in open("posts.txt").read():
                            # Save the post to the variable
                            post = p
                            break  # Exit the loop once a matching post is found

                # If no matching post is found, select a new random subreddit and continue the loop
                else:
                    continue

            post_content = f"{post.title}\n\n{post.selftext}"

            # Get 10 comments and its 2 replies on post and stores it
            all_comments = []

            # If an AttributeError is encountered, the code will not crash and will instead pass the error and continue running.
            # Loop through the top 10 comments
            for comment in post.comments[:10]:
                comment_data = {}
                try:
                    comment_data['text'] = comment.body
                    comment_data['replies'] = []
                except AttributeError:
                    pass

                # Loop through the first 2 replies to the comment
                for reply in comment.replies[:2]:
                    reply_data = {}
                    try:
                        reply_data['text'] = reply.body
                        comment_data['replies'].append(reply_data)
                    except AttributeError:
                        pass

                all_comments.append(comment_data)


            davinci_reply = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f'Generate Reddit Comment to subreddit: {post.subreddit} Post: {post_content}, here is some comments made on post: {all_comments}, use this to only guide your comment, but make your own judgement, the comment should get many upvotes.Dont always start your comment with Wow. Do not write comment in quotes. The comment must not look like it was generated by a bot. Generated Comment:',
                max_tokens=200,
                n=1,
                stop=None,
                temperature=0.5,
            )
            davinci_reply = davinci_reply.choices[0].text

            post.reply(davinci_reply)
            print(f'[{username}]: Random Comment Sent to "{post.id}" in r/{post.subreddit}')

            with open("posts.txt", "a") as file:
                file.write(post.id + "\n")

        with open('test_logg.txt', 'a') as f:
                        f.write(f"[{username}]: Comment Sent\n")    

    def random_comment_topreply():
            
        if reddit.redditor(username).link_karma + reddit.redditor(username).comment_karma > 50:

            # Read the subreddit names from subreddits.txt file
            with open("subreddits.txt") as f:
                subreddit_list = [line.strip() for line in f]

            # Initialize the post variable to None
            post = None

            while post is None:
                # Select a random subreddit from the list
                random_subreddit = reddit.subreddit(random.choice(subreddit_list))

                # Loop through the posts in the subreddit
                for p in random_subreddit.new():
                    # Check if the post meets the criteria
                    if p.num_comments < 5 and p.num_comments > 2 and p.score >= 10 and time.time() - p.created_utc < 20*60:
                        # Check if the post ID is not in the posts.txt file
                        if str(p.id) not in open("posts.txt").read():
                            # Save the post to the variable
                            post = p
                            break  # Exit the loop once a matching post is found

                # If no matching post is found, select a new random subreddit and continue the loop
                else:
                    continue

            post_content = f"{post.title}\n\n{post.selftext}"


            # Get 10 comments and its 2 replies on post and stores it
            all_comments = []

            # If an AttributeError is encountered, the code will not crash and will instead pass the error and continue running.
            # Loop through the top 10 comments
            for comment in post.comments[:10]:
                comment_data = {}
                try:
                    comment_data['text'] = comment.body
                    comment_data['replies'] = []
                except AttributeError:
                    pass

                # Loop through the first 2 replies to the comment
                for reply in comment.replies[:2]:
                    reply_data = {}
                    try:
                        reply_data['text'] = reply.body
                        comment_data['replies'].append(reply_data)
                    except AttributeError:
                        pass

                all_comments.append(comment_data)

            # Get the top comment or the second top comment
            top_comment = None
            second_top_comment = None
            for i, comment in enumerate(post.comments[:2]):
                if comment.author and not comment.author.is_mod:
                    top_comment = comment
                    break
                elif i == 1:
                    second_top_comment = comment




            comment_text = top_comment.body if top_comment else second_top_comment.body
            comment_id = top_comment.id if top_comment else second_top_comment.id


            davinci_reply = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f'Generate Reddit Comment to subreddit: {post.subreddit} Post: {post_content}, here is some comments made on post: {all_comments}, use this to only guide your comment, but make your own judgement, the comment should get many upvotes.Dont always start your comment with Wow. Do not write comment in quotes. The comment must not look like it was generated by a bot. You are replying to this comment: {comment_text}, it doesnt have to specific reply to this, our goal is to just get the most amount of upvotes. Dont act as if youre talking to the post creator because you are replying to comment. Generated Comment:',
                max_tokens=200,
                n=1,
                stop=None,
                temperature=0.5,
            )
            davinci_reply = davinci_reply.choices[0].text

            
            if not top_comment and not second_top_comment:
                print(f'[{username}]: No eligible comments found in "{post.id}" in r/{post.subreddit}, comment send to post.')
                post.reply(davinci_reply)
            else:
                reddit.comment(comment_id).reply(davinci_reply)
                print(f'[{username}]: Random Comment replied to Comment {comment_id}, Sent to "{post.id}" in r/{post.subreddit}')


            with open("posts.txt", "a") as file:
                file.write(post.id + "\n")


        else:
            # Read the subreddit names from subreddits.txt file
            with open("lowkarma_subreddits.txt") as f:
                subreddit_list = [line.strip() for line in f]

            # Initialize the post variable to None
            post = None

            while post is None:
                # Select a random subreddit from the list
                random_subreddit = reddit.subreddit(random.choice(subreddit_list))

                # Loop through the posts in the subreddit
                for p in random_subreddit.new():
                    # Check if the post meets the criteria
                    if p.num_comments < 10 and p.num_comments > 2 and p.score >= 2 and time.time() - p.created_utc < 40*60:
                        # Check if the post ID is not in the posts.txt file
                        if str(p.id) not in open("posts.txt").read():
                            # Save the post to the variable
                            post = p
                            break  # Exit the loop once a matching post is found

                # If no matching post is found, select a new random subreddit and continue the loop
                else:
                    continue

            post_content = f"{post.title}\n\n{post.selftext}"


            # Get 10 comments and its 2 replies on post and stores it
            all_comments = []

            # If an AttributeError is encountered, the code will not crash and will instead pass the error and continue running.
            # Loop through the top 10 comments
            for comment in post.comments[:10]:
                comment_data = {}
                try:
                    comment_data['text'] = comment.body
                    comment_data['replies'] = []
                except AttributeError:
                    pass

                # Loop through the first 2 replies to the comment
                for reply in comment.replies[:2]:
                    reply_data = {}
                    try:
                        reply_data['text'] = reply.body
                        comment_data['replies'].append(reply_data)
                    except AttributeError:
                        pass

                all_comments.append(comment_data)

            # Get the top comment or the second top comment
            top_comment = None
            second_top_comment = None
            for i, comment in enumerate(post.comments[:2]):
                if comment.author and not comment.author.is_mod:
                    top_comment = comment
                    break
                elif i == 1:
                    second_top_comment = comment




            comment_text = top_comment.body if top_comment else second_top_comment.body
            comment_id = top_comment.id if top_comment else second_top_comment.id


            davinci_reply = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f'Generate Reddit Comment to subreddit: {post.subreddit} Post: {post_content}, here is some comments made on post: {all_comments}, use this to only guide your comment, but make your own judgement, the comment should get many upvotes.Dont always start your comment with Wow. Do not write comment in quotes. The comment must not look like it was generated by a bot. You are replying to this comment: {comment_text}, it doesnt have to specific reply to this, our goal is to just get the most amount of upvotes. Dont act as if youre talking to the post creator because you are replying to comment. Generated Comment:',
                max_tokens=200,
                n=1,
                stop=None,
                temperature=0.5,
            )
            davinci_reply = davinci_reply.choices[0].text

            
            if not top_comment and not second_top_comment:
                print(f'[{username}]: No eligible comments found in "{post.id}" in r/{post.subreddit}, comment send to post.')
                post.reply(davinci_reply)
            else:
                reddit.comment(comment_id).reply(davinci_reply)
                print(f'[{username}]: Random Comment replied to Comment {comment_id}, Sent to "{post.id}" in r/{post.subreddit}')


            with open("posts.txt", "a") as file:
                file.write(post.id + "\n")

        with open('test_logg.txt', 'a') as f:
                        f.write(f"[{username}]: Comment Sent\n")    
        
    def remove_negative_comments():
        # Get the newest 10 comments from your profile
        comments = reddit.redditor(username).comments.new(limit=50)

        # Loop through each comment
        for comment in comments:
            # Check if the comment's karma is less than 1
            if comment.score < 1:
                # Save the comment details to negativecomments.txt
                with open('negativecomments.txt', 'a') as f:
                    f.write(f'Comment URL: {comment.permalink}\n')
                    f.write(f'Comment Content: {comment.body}\n')
                    f.write(f'Comment Points: {comment.score}\n\n')
                # Delete the comment
                comment.delete()
                print(f'[{username}]: Removed Comment {comment.id} with {comment.score} points')

    def random_post_downvote():
         # Get a list of the top popular 100 SFW subreddits
        subreddit_list = [subreddit.display_name for subreddit in reddit.subreddits.popular(limit=100) if subreddit.over18 == False]

        # Select a random subreddit from the list
        random_subreddit = reddit.subreddit(random.choice(subreddit_list))

        # Select a random post from the hot section of the subreddit
        hot_posts = random_subreddit.hot(limit=10)
        random_post = random.choice([post for post in hot_posts])

        # Upvote the post
        random_post.downvote()

        # Print confirmation message
        print(f'[{username}]: Downvoted post "{random_post.id}" in r/{random_subreddit.display_name}')
    
    def random_comment_downvote():
        # Get a list of the top popular 100 SFW subreddits
        subreddit_list = [subreddit.display_name for subreddit in reddit.subreddits.popular(limit=100) if subreddit.over18 == False]

        # Select a random subreddit from the list
        random_subreddit = reddit.subreddit(random.choice(subreddit_list))

        # Select a random post from the hot section of the subreddit
        hot_posts = random_subreddit.hot(limit=10)
        random_post = random.choice([post for post in hot_posts])

        # Select a random comment (if there are any comments)
        if random_post.num_comments > 0:
            random_comments = random_post.comments[:3] # Only fetch first 3 comments
            random_comment = random.choice(random_comments)
            random_comment.downvote()
            print(f'[{username}]: Downvoted comment "{random_comment.id}" in post "{random_post.id}" in r/{random_subreddit.display_name}')



    def run():
        while True:
            time.sleep(10)
            try:
                #get_info()
                # Check if the current time is not between 11 pm and 6 am
                current_time = time.time()
                local_time = time.localtime(current_time)
                current_hour = local_time.tm_hour
                if not (23 <= current_hour or current_hour < 6):


                    # Check if time since last comment has been over 5 minutes
                    recent_comments = list(reddit.redditor(username).comments.new(limit=1))
                    if len(recent_comments) > 0:
                        comment_time = recent_comments[0].created_utc
                    else:
                        comment_time = 301 #If there is no comment or something.

                    if current_time - comment_time > 300:

            
                        if reddit.redditor(username).link_karma + reddit.redditor(username).comment_karma > 50:
                            sleep_time = random.randint(300, 1800)
                        else:
                            sleep_time = random.randint(600, 1800)

                        


                        #random_number = random.randint(0, 5)
                        random_number = 69
                        if random_number == 0:
                            random_comment_upvote()
                        elif random_number == 1:
                            random_comment_downvote()
                        elif random_number == 2:
                            random_post_downvote()
                        elif random_number == 3:
                            random_post_upvote_with_comment_upvote()
                        elif random_number == 4:
                            random_post_upvote()

                        if random.random() <= 0.5:
                            random_comment_topreply()
                        else:
                            random_comment()
                            
                        print(f"[{username}]: Sleeping for {sleep_time} Seconds")
                        time.sleep(sleep_time)
                    else:
                        time.sleep(300)
                else:
                    time.sleep(1800)

            except Exception as e:
                # if an exception occurs, restart the thread
                if 'RATELIMIT' in str(e):
                    #print(e)
                    with open('error_log.txt', 'a') as f:
                        f.write(f"[{username}]: Thread failed with error: {e}. Restarting thread with same arguments.\n")
                        traceback.print_exc(file=f)
                    time.sleep(1200)
                    run_thread = threading.Thread(target=run)
                    run_thread.daemon = True
                    run_thread.start()
                else:
                    #print(f"[{username}]: {e}")
                    with open('test_log.txt', 'a') as f:
                        f.write(f"[{username}]: {e}\n")
                    with open('error_log.txt', 'a') as f:
                        f.write(f"[{username}]: Thread failed with error: {e}. Restarting thread with same arguments.\n")
                        traceback.print_exc(file=f)
                    run_thread = threading.Thread(target=run)
                    run_thread.daemon = True
                    run_thread.start()

    # start a new thread to execute the run() function
    run_thread = threading.Thread(target=run)
    run_thread.daemon = True
    run_thread.start()

    while True:
        remove_negative_comments()
        time.sleep(30) #should be 30 seconds





def start_threads():
    # Read the CSV file into a pandas dataframe
    df = pd.read_csv("accounts.csv")

    # Start a thread for each row in the dataframe
    threads = []
    for _, account in df.iterrows():
        t = threading.Thread(target=thread_main,
                             args=(account["username"],
                                   account["password"],
                                   account["client_id"],
                                   account["client_secret"],
                                   "dc.smartproxy.com:10000"))
                                   #account["http_proxy"] if not pd.isna(account["http_proxy"]) else None))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

start_threads()
