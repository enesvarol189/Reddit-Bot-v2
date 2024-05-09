def bot_message():
    return "Please respond to this message and include as much of the following information as possible in your response:\n\n🪴 How long have you had the plant?\n\n❓ How long have you been experiencing this issue?\n\n🌞 How much light does the plant receive?\n\n💦 What are your watering habits (both frequency and amount), and does the pot have proper drainage?\n\nThe more details you provide, the better we can assist you!\n___\n_If you don't respond to this message within 10 minutes, we will have to remove your post._\n\n***Inappropriate and/or unhelpful responses will result in a ban.***"

def additional_information_message(op_response):
    return f"Additional information about the plant that has been provided by the OP:\n\n{_format_message(op_response)}\n\nIf this information meets your satisfaction, please upvote this comment. If not, you can downvote it."

def inactive_post_removal_message():
    return "Your post has been removed because you didn't provide the necessary information requested in our previous message. If you'd like to receive assistance, please feel free to make a new post including the details mentioned earlier. We're here to help, so don't hesitate to reach out with the required information. Thank you!"

def blacklisted_post_removal_message():
    return "Your post has been removed because our bot failed to send you a message to request additional details about your plant. To avoid automatic removals in the future, please check your Reddit settings and ensure that you've whitelisted this bot account. Once you've done that, feel free to repost your query, and the bot will be able to assist you."

def _format_message(message):
    lines = message.split("\n")
    formatted_lines = [f"> {line}" for line in lines]
    formatted_message = "\n".join(formatted_lines)
    return formatted_message