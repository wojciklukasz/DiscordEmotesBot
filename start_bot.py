import os
from dotenv import load_dotenv
from src.bot import start


if os.path.isfile('.env'):
    load_dotenv()

try:
    start(os.getenv('TOKEN'))
except TypeError:
    print('Could not find the token! Either set the environmental variable TOKEN or add it to .env file!')