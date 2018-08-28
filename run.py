import os
from app import create_app
import database_setup
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

config_name = os.getenv("APP_SETTINGS") # config_name = "development"
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
