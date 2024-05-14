### Plant Clinic Reddit Bot

This is a Reddit bot written in Python. It uses the [PRAW](https://praw.readthedocs.io/en/latest/) library to interact with Reddit's API and [MongoDB Atlas](https://www.mongodb.com/atlas/database) for database services. The bot is designed to manage posts on a selected subreddit by sending automated messages to authors of new posts, tracking responses, and handling posts based on certain conditions.

##### Getting Started

These instructions will get you a copy of the project up and running on your local machine for deployment purposes.

##### Prerequisites:

* Python 3.7+
* PRAW library
* PyMongo

##### Installing:

1. Clone the repository
```bash
git clone https://github.com/enesvarol189/Reddit-Bot-v2
```

2. Install the dependencies
```bash
pip install -r requirements.txt
```

3. Run the bot  
```bash
python main.py start
```

> __Important:__ Ensure that the last 2 commands are executed from the application's root directory.

##### Built With:

* Python - The programming language used
* PRAW - The Python Reddit API Wrapper
* MongoDB Atlas - The online database service

##### Authors:

* Enes VAROL

> Note: This bot is currently under active development, and future updates will continue to enhance its functionality.
