import json
from bot.bot import Bot
from bot.config import (
    BOT_CONFIG, TEST_DATA_FILE, URL_ENDPOINTS,
    ALL_POSTS_RDS, ALL_USERS_RDS, DETAILED_POSTS_RDS, DETAILED_USERS_RDS
)


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def get_dict_from_json(config_file):
        with open(config_file, 'r') as fp:
            config = json.load(fp)
        return config

    @staticmethod
    def dump_result_to_file(config_file, data):
        with open(config_file, 'w') as fp:
            json.dump(data, fp)


if __name__ == "__main__":
    bot_config = Utils.get_dict_from_json(BOT_CONFIG)
    url_endpoints = Utils.get_dict_from_json(URL_ENDPOINTS)
    test_data = Utils.get_dict_from_json(TEST_DATA_FILE)
    bot = Bot(bot_config, url_endpoints, test_data)

    print('\n\n==========================================================================================')
    print('Bot will start loading the data using the API endpoints')
    print('==========================================================================================\n')

    # Signup
    bot.signup_users()
    print("Sign-up phase was a success!")
    print('\n==========================================================================================\n')

    bot.login_users()
    print("All the users were able to login ! And have received JWT tokens")
    print('\n==========================================================================================\n')

    bot.make_users_create_posts()
    print("All the users have created new posts randomly !")

    bot.make_users_like_post_of_other_users()
    print("Bots have liked/disliked each others posts according to rules mentioned in 'Readme.md'")

    print('\n\n==========================================================================================')
    print('Bot will start collecting the data stored previously using API endpoints')
    print('==========================================================================================\n')
    all_posts = bot.get_all_posts()
    Utils.dump_result_to_file(ALL_POSTS_RDS, all_posts)
    print('Successfully gathered all posts randomly created by users. Stored at - {}'.format(ALL_POSTS_RDS))
    print('\n==========================================================================================\n')

    all_detailed_posts = bot.get_all_posts_in_detail()
    Utils.dump_result_to_file(DETAILED_POSTS_RDS, all_detailed_posts)
    print('Successfully gathered all posts in detail (contains info of users who liked/disliked it). Stored at - {}'.format(DETAILED_POSTS_RDS))
    print('\n==========================================================================================\n')

    all_users = bot.get_all_users()
    Utils.dump_result_to_file(ALL_USERS_RDS, all_users)
    print('Successfully gathered all user data. Stored at - {}'.format(ALL_USERS_RDS))
    print('\n==========================================================================================\n')

    all_detailed_users = bot.get_all_users_in_detail()
    Utils.dump_result_to_file(DETAILED_USERS_RDS, all_detailed_users)
    print('Successfully gathered all user data in detail (Also contain data gathered from clearbit). Stored at - {}'.format(DETAILED_USERS_RDS))
    print('\n==========================================================================================\n')

    print("Done !")