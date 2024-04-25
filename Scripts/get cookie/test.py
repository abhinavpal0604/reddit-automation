from selenium import webdriver
from tkinter import *
import json

# Define HTTP Proxy IP and Port
PROXY_HOST = ''
PROXY_PORT = ''

# Set up Proxy configuration using Chrome options
options = webdriver.ChromeOptions()


# Open browser with Proxy settings
driver = webdriver.Chrome(options=options)

# Open Reddit.com
driver.get('https://www.reddit.com')

# Function to save cookie
def save_cookie():
    with open('session.txt', 'w') as f:
        cookies = driver.get_cookies()
        # Update the cookie domain to match the domain of the website being accessed
        for cookie in cookies:
            cookie['domain'] = 'www.reddit.com'
        json.dump(cookies, f)

# Function to handle button click
def button_click():
    save_cookie()

# Create GUI option
root = Tk()
root.title('Save Cookie')
root.geometry('200x100')

# Create button
button = Button(root, text='SAVE COOKIE NOW', command=button_click)
button.pack(pady=20)

root.mainloop()
