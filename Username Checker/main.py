import praw
import prawcore

reddit = praw.Reddit(
    client_id="",
    client_secret="",
    username="",
    password="",
user_agent="your_user_agent",
)


with open('usernames.txt', 'r') as file:
    usernames = [line.strip() for line in file]

print("List of available usernames:")
def check_account_status(username):
    try:
        reddit.redditor(username).id  # Check if the account exists by accessing its ID.
        return "Active"  # Account is active.
    except prawcore.exceptions.NotFound:
        return "Deleted"  # Account is deleted.
    except praw.exceptions.ClientException as e:
        return "Invalid"  # Invalid account name or other client-related error.
    except Exception as e:
        return "Unknown"  # An unknown error occurred.


for username in usernames:

    #Deleted = Available or Deleted

    status = check_account_status(username)
    if status == 'Deleted':

        print(username)
