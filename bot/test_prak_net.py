# import requests
# from os import path
import json
from bot.bot import Bot
from bot.config import (
    BOT_CONFIG, USERS_SIGNUP_CONFIG,
    URL_ENDPOINTS)






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
    bot = Bot(bot_config, url_endpoints)

    # Test 1: Let users signup
    users_signup_config = Utils.get_dict_from_json(USERS_SIGNUP_CONFIG)
    bot.signup_users(users_signup_config)


