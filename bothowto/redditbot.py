#!/usr/bin/python3

import praw
import random

# Replace these with your actual credentials
username = "YOUR_USERNAME"
password = "YOUR_PASSWORD"
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
user_agent = "YOUR_USER_AGENT"

# Create a Reddit instance
reddit = praw.Reddit(username=username,
  password=password,
  client_id=client_id,
  client_secret=client_secret,
  user_agent=user_agent)

# List of sad quotes
sad_quotes = [
    "Lost in pain",
    "Tears fall silently",
    "Broken heart whispers",
    "Lonely soul weeps",
    "Shattered dreams echo",
    "Love fades away",
    "Hope drifts aimlessly",
    "Silent cries within",
    "Darkness consumes all",
    "Alone in shadows"
]

# Choose a subreddit to monitor
subreddit = reddit.subreddit("testingground4bots")

# For submissions
for submission in subreddit.hot(limit=10):
    # For comments in submissions
    for comment in submission.comments.list():
        if hasattr(comment, "body"):
            comment_lower = comment.body.lower()
            if "!bot" in comment_lower:
                print("-------")
                print(comment.body)
                random_index = random.randint(0, len(sad_quotes) - 1)
                comment.reply(sad_quotes[random_index])

# Stream your inbox messages
messages = reddit.inbox.stream()

for message in messages:
    try:
        # Check if the message is a mention and unread
        if message in reddit.inbox.mentions() and message in reddit.inbox.unread():
            # Reply with "hello"
            message.reply("hello")
            # Mark the message as read
            message.mark_read()

    except praw.exceptions.APIException:
        print("Probably a rate limit....")

