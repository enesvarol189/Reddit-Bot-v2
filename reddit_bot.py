from auth import authenticate
from bot_logic import run_bot
from mongodb_management import env
from logger import LogLevel, log
import traceback

def main():
    exit(0) # remove this line to enable the bot

    try:

        if env["version"] != "2.0":
            raise Exception(f"Version mismatch: {env['version']}. Please upgrade to the latest version.")

        log("Bot is starting up...")

        reddit = authenticate()
        run_bot(reddit)

    except Exception as e:
        error_message = str(e)
        stack_trace = traceback.format_exc()
        log(f"An error occurred: {error_message}", LogLevel.ERROR)
        reddit.redditor(env["developer"]).message("Error in bot", f"An error occurred: {error_message}\n\n{stack_trace}")
        log("Program is closing...")