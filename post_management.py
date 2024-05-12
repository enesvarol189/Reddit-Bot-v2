import time
from collections import deque
from canned_messages import (
    bot_message,
    additional_information_message,
    inactive_post_removal_message,
    blacklisted_post_removal_message
)
from mongodb_management import env
from logger import LogLevel, log

class ManagePosts:
    def __init__(self, reddit, post_tracker):
        self.reddit = reddit
        self.post_tracker = post_tracker
        self.cashed_submissions = deque(maxlen=env["post_limit"])
        self._bootstrap_cache()

    def send_messages(self, submission):
        post_id = submission.id
        post_approved = submission.approved
        word_count = len(submission.selftext.split())
        post_age = int(time.time() - submission.created_utc)
        op = submission.author

        if op and post_id not in self.post_tracker and post_age <= env["post_age_threshold"] and \
            not post_approved and word_count < env["word_threshold"] and op.name not in env["moderators"]:
            op_message = bot_message()

            op.message("Request for Context", op_message)

            message = next(self.reddit.inbox.sent(limit=1))
            self.post_tracker[post_id] = {
                "message_id": message.id,
                "op_responded": False,
                "timestamp": time.time(),
                "post_removed": False
            }

            log(f"Message sent to {op} for submission {post_id}.", LogLevel.INFO)

        elif post_id not in self.cashed_submissions and not op:
            log(f"Author not found for submission {post_id}.", LogLevel.WARNING)
            self.cashed_submissions.append(post_id)
            log(f"Submission cache: {self.cashed_submissions}", LogLevel.DEBUG)

        elif post_id not in self.cashed_submissions and post_approved:
            log(f"Submission {post_id} by {op} is ignored as it has been approved by a moderator.", LogLevel.WARNING)
            self.cashed_submissions.append(post_id)
            log(f"Submission cache: {self.cashed_submissions}", LogLevel.DEBUG)

        elif post_id not in self.cashed_submissions and word_count >= env["word_threshold"]:
            log(f"Submission {post_id} by {op} is ignored as it has a sufficent self text length.", LogLevel.WARNING)
            self.cashed_submissions.append(post_id)
            log(f"Submission cache: {self.cashed_submissions}", LogLevel.DEBUG)
        
        elif post_id not in self.cashed_submissions and op.name in env["moderators"]:
            log(f"Submission {post_id} by {op} is ignored as they are a moderator.", LogLevel.WARNING)
            self.cashed_submissions.append(post_id)
            log(f"Submission cache: {self.cashed_submissions}", LogLevel.DEBUG)
    
    def process_blacklisted_posts(self, e, submission):
        if "NOT_WHITELISTED_BY_USER_MESSAGE" in str(e):
            comment = submission.reply(blacklisted_post_removal_message())
            comment.mod.distinguish(how='yes', sticky=True)
            comment.mod.lock()
    
            submission.mod.remove()
            submission.mod.lock()

            log(f"Submission by {submission.author} has been removed due to blacklisting.", LogLevel.WARNING)
    
    def find_post(self, message):
        for post_id, value in self.post_tracker.items():
            if value.get("message_id") == str(message.parent_id)[3:]:
                return post_id
        return None
    
    def process_active_posts(self, post_id, message):
        submission = self.reddit.submission(id=post_id)
      
        if submission and not self.post_tracker[post_id]["op_responded"]:
            comment = submission.reply(additional_information_message(message.body))
            comment.mod.distinguish(how='yes', sticky=True)
            comment.mod.lock()
    
            if self.post_tracker[post_id]["post_removed"]:
                submission.mod.approve()
                submission.mod.unlock()
    
                for comment in submission.comments:
                    if comment.author and comment.author.name == self.reddit.user.me().name and "Your post has been removed" in comment.body:
                        comment.delete()
    
                self.post_tracker[post_id]["post_removed"] = False

                log(f"Submission {post_id} by {submission.author} has been re-approved.", LogLevel.INFO)

            else:
                log(f"Submission {post_id} by {submission.author} has been approved.", LogLevel.INFO)

            self.post_tracker[post_id]["op_responded"] = True
        
        elif not submission:
            log(f"Submission {post_id} by {submission.author} no longer exists.", LogLevel.WARNING)
            del self.post_tracker[post_id]
    
    def process_inactive_posts(self, post_id, post_data):
        elapsed_time = int(time.time() - post_data["timestamp"])

        if not post_data["post_removed"] and elapsed_time >= env["inactivity_threshold"] and not post_data["op_responded"]:
            submission = self.reddit.submission(id=post_id)
    
            if post_id not in self.cashed_submissions and submission.approved:
                log(f"Submission {post_id} by {submission.author} has been approved by a moderator.", LogLevel.WARNING)
                self.cashed_submissions.append(post_id)
                log(f"Submission cache: {self.cashed_submissions}", LogLevel.DEBUG)
                return
            
            elif post_id not in self.cashed_submissions and len(submission.selftext.split()) >= env["word_threshold"]:
                log(f"Submission {post_id} by {submission.author} is ignored as it has a sufficent self text length.", LogLevel.WARNING)
                self.cashed_submissions.append(post_id)
                log(f"Submission cache: {self.cashed_submissions}", LogLevel.DEBUG)
                return
    
            submission.mod.remove()
            submission.mod.lock()
          
            comment = submission.reply(inactive_post_removal_message())
            comment.mod.distinguish(how='yes', sticky=True)
            comment.mod.lock()
    
            post_data["post_removed"] = True

            log(f"Submission {post_id} by {submission.author} has been removed due to inactivity.", LogLevel.INFO)

    def process_submission_status(self, post_id, post_data, archived_logs):
        submission = self.reddit.submission(id=post_id)

        if not submission:
            log(f"Submission {post_id} has been deleted by the author, or removed by a moderator.", LogLevel.WARNING)
            archived_logs.append({"post_id": post_id, **post_data})

        elif post_data["post_removed"] and submission.approved:
            log(f"Formerly removed submission {post_id} by {submission.author} has been re-approved by a moderator.", LogLevel.WARNING)
            archived_logs.append({"post_id": post_id, **post_data})

    def _bootstrap_cache(self):
        for submission in self.reddit.subreddit(env["subreddit"]).new(limit=env["post_limit"]):
            self.cashed_submissions.append(submission.id)

        log(f"Submission cache: {self.cashed_submissions}", LogLevel.DEBUG)
