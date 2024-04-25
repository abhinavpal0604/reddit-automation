# Reddit Automation 🤖

~By Abhinav Pal
Uploaded from my PC to github for attaching to my CV on 26/04/24 

Greetings CrowdStrike 👋

## Introduction

This project is a Python-Selenium based automation for the social platform Reddit. It leverages OpenAI's GPT-3 to comment like a real user, aiming to boost a Reddit account's karma and make it appear more authentic to bypass bot detections and be treated as a human.

This automation tool utilizes Python-Selenium for Reddit interactions and OpenAI's GPT-3 for generating comments. While GPT-3 is crucial, the real mechanism lies in the automation of actions that mimic real user behavior.

### Project Insights

Last year, this project was successfully implemented, showcasing the complexity of combatting bots by large companies to protect their users. However, it's worth noting that algorithms used for this purpose may not always be foolproof.

## Project Structure

The project is organized into three main folders:

1. **Scripts Folder**
   - Contains essential scripts: (these contain some scripts from the complete project, rest of the scripts are embedded directly into the main program)
     - Get comments with specific karma and replies criteria.
     - Shadow ban checker.
     - Get cookie of a login session.

2. **Username Checker**
   - Checks the availability of usernames from a provided notepad.

3. **Ultimate Karma Farmer**
   - The core program aiming to boost karma:
     - Utilizes OpenAI's GPT-3 to generate comments resembling real user behavior.
     - Engages with different subreddits to gain likes and comments, mimicking real user actions like upvotes and comments on various posts.

