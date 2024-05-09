import praw
import time
from collections import deque
from json_handler import save_json, load_json, clean_json, dump_json
from post_management import ManagePosts
from mongodb_management import archive_document, get_env_variable, env
from logger import LogLevel, log

def run_bot(reddit):
    subreddit = reddit.subreddit(env["subreddit"])
    post_tracker = load_json('post_data.json')

    manage = ManagePosts(reddit, post_tracker)

    cashed_messages = deque(maxlen=env["post_limit"])
    _bootstrap_cache(reddit, cashed_messages)

    last_checked = 0

    while True:
        if time.time() - last_checked >= env["poll_interval"]:
            _check_permission(reddit, post_tracker)
            last_checked = time.time()

        for submission in subreddit.new(limit=env["post_limit"]):
            try:
                manage.send_messages(submission)

            except praw.exceptions.RedditAPIException as e:
                manage.process_blacklisted_posts(e, submission)

        save_json('post_data.json', post_tracker)

        for message in reddit.inbox.all(limit=env["post_limit"]):
            post_id = manage.find_post(message)
          
            if post_id is not None:
                manage.process_active_posts(post_id, message)

            elif message.id not in cashed_messages:
                log(f"Message {message.id} does not belong to any tracked post.", LogLevel.WARNING)

                cashed_messages.append(message.id)

                log(f"Cache: {cashed_messages}", LogLevel.DEBUG)

        save_json('post_data.json', post_tracker)
    
        archived_logs = []
      
        for post_id, post_data in post_tracker.items():
            manage.process_inactive_posts(post_id, post_data)

            archive_document(post_id, post_data, archived_logs)

            manage.process_submission_status(post_id, post_data, archived_logs)

        save_json('post_data.json', post_tracker)
      
        for archived_document in archived_logs:
            post_tracker.pop(archived_document["post_id"], None)
    
        save_json('post_data.json', post_tracker)

        if len(archived_logs) > 0:
            log(f"{len(archived_logs)} documents have been archived.")

        time.sleep(env["cycle_delay"])

def _check_permission(reddit, post_tracker):
    execution_permission = get_env_variable("permission")
    if not execution_permission:
        log("Execution permission has been denied.", LogLevel.ERROR)
        reddit.redditor(env["developer"]).message("Bot execution has been terminated", dump_json(post_tracker))
        clean_json('post_data.json')
        log("Program is closing...")
        exit()

def _bootstrap_cache(reddit, cashed_messages):
    for message in reddit.inbox.all(limit=env["post_limit"]):
        cashed_messages.append(message.id)

    log(f"Message cache: {cashed_messages}", LogLevel.DEBUG)