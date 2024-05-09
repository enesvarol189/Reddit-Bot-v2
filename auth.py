import praw
from mongodb_management import env

def authenticate():
    client_id = env["client_id"]
    client_secret = env["client_secret"]
    username = env["username"]
    password = env["password"]

    reddit = praw.Reddit(
        client_id = client_id,
        client_secret = client_secret,
        user_agent = f"botscript by u/{env['developer']}",
        check_for_updates = False,
        comment_kind = "t1",
        message_kind = "t4",
        redditor_kind = "t2",
        submission_kind = "t3",
        subreddit_kind = "t5",
        trophy_kind = "t6",
        oauth_url = "https://oauth.reddit.com",
        reddit_url = "https://www.reddit.com",
        short_url = "https://redd.it",
        ratelimit_seconds = 5,
        timeout = 16,
        username = username,
        password = password
    )

    return reddit