import vkapi
import vkbot
from vk_api.longpoll import VkEventType
import models
from models import Session, engine

# create a Session
session = Session()
connection = engine.connect()


def main():
    vk_bot = vkbot.VKBot()
    vk_api = vkapi.VkApi()
    stack = []
    flag_wish = False
    flag_black = False

    def get_user_for_bot(user_id):
        city_search, sex_search, bdate_search = vk_api.get_user_info(user_id)
        user_for_bot = vk_api.search_user(city_search, sex_search, bdate_search)
        # Проверяем, если пользователь есть в базе данных
        if models.check_if_bot_user_exists(user_id) is None:
            # Добавляем пользователя бота в базу данных
            models.add_bot_user(user_id)
        return user_for_bot

    def add_user_to_db(bot_user_id, flag=None):
        nonlocal flag_wish
        nonlocal flag_black
        if len(stack) == 0 or (flag and not flag_wish):
            vk_bot.send_msg(event.user_id, "Добавлять некого")
            return False
        elif len(stack) == 0 or (not flag is None and not flag_black):
            vk_bot.send_msg(event.user_id, "Добавлять некого")
            return False
        data = stack.pop()
        first_name, last_name, url = data[0], data[1], data[2]
        vk_user_id, user_attachment = int(data[2].split('id')[1]), data[3]
        models.add_photo_of_the_match(user_attachment, vk_user_id)
        if flag:
            flag_wish = True
            models.add_new_match_to_favorites(vk_user_id, bot_user_id, first_name, last_name, url)
        else:
            flag_black = True
            models.add_new_match_to_black_list(vk_user_id, bot_user_id, first_name, last_name, url)

    for event in vk_bot.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                message = event.text.lower()
                if message == "привет":
                    vk_bot.send_msg(event.user_id, 'Привет, для начала работы нажми кнопку "Показать"')
                elif message == "список избранных":
                    for user in models.show_all_favorites(event.user_id):
                        msg = f'{user[0]} {user[1]}\n{user[2]}'
                        vk_bot.send_msg(event.user_id, message=msg, attachment=user[3])
                elif message == "черный список":
                    for user in models.show_all_blacklisted(event.user_id):
                        msg = f'{user[0]} {user[1]}\n{user[2]}'
                        vk_bot.send_msg(event.user_id, message=msg, attachment=user[3])
                elif message == "добавить в избранное":
                    add_user_to_db(event.user_id, True)
                    vk_bot.send_msg(event.user_id, message='Добавил в избранное')
                elif message == "не нравится":
                    add_user_to_db(event.user_id, False)
                    vk_bot.send_msg(event.user_id, message='Добавил в черный список')
                elif message == "показать":
                    data = get_user_for_bot(event.user_id)
                    msg = f'{data[0]} {data[1]}\n{data[2]}'
                    stack.append(data)
                    vk_bot.send_msg(event.user_id, message=msg, attachment=data[3])
                    flag_wish, flag_black = True, True
                else:
                    vk_bot.send_msg(event.user_id, "К сожалению, такой команды я не знаю")

if __name__ == '__main__':
    main()
