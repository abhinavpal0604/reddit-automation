import praw
import prawcore

reddit = praw.Reddit(
    client_id="",
    client_secret="",
    username="",
    password="",
    user_agent="your_user_agent",
)

# Retrieve usernames from usernames.txt file
with open('usernames.txt', 'r') as file:
    usernames = [line.strip() for line in file]

# Filter and keep only usernames with 5 characters
filtered_usernames = [username for username in usernames if len(username) == 6]

# Rewrite usernames.txt file with filtered usernames
with open('usernames.txt', 'w') as file:
    file.write('\n'.join(filtered_usernames))

print("Usernames rewritten successfully.")
