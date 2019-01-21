# import requests
# from os import path
import json
from bot.bot import Bot
from bot.config import (
    BOT_CONFIG, TEST_DATA_FILE,
    URL_ENDPOINTS)
from pprint import pprint

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def get_dict_from_json(config_file):
        with open(config_file, 'r') as fp:
            config = json.load(fp)
        return config


if __name__ == "__main__":
    bot_config = Utils.get_dict_from_json(BOT_CONFIG)
    url_endpoints = Utils.get_dict_from_json(URL_ENDPOINTS)
    test_data = Utils.get_dict_from_json(TEST_DATA_FILE)
    bot = Bot(bot_config, url_endpoints, test_data)

    bot.signup_users()
    bot.login_users()
    bot.create_posts()

    pprint(bot.user_to_num_of_post_mapping)
