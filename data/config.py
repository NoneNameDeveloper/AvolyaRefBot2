import os

from dotenv import load_dotenv


load_dotenv(dotenv_path="config.env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

ADMINS = 1888872438, 804830369,

