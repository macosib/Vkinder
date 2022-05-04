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
        # Проверка
        city_search, sex_search, bdate_search = vk_api.get_user_info(user_id)
        user_for_bot = vk_api.search_user(city_search, sex_search, bdate_search)
        # Проверяем, если пользователь есть в базе данных
        if user_id == models.check_if_bot_user_exists(user_id) is False:
            # Добавляем пользователя бота в базу данных
            models.add_bot_user(user_id)
        return f'{user_for_bot[0]} {user_for_bot[1]}\n{user_for_bot[2]}', user_for_bot[3]

    for event in vk_bot.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                message = event.text.lower()
                if message == "привет":
                    vk_bot.send_msg(event.user_id, 'Привет, для начала работы нажми кнопку "Показать"')
                elif message == "список избранных":
                    for user in vk_api.wish_list:
                        vk_bot.send_msg(event.user_id, message=user[0], attachment=user[1])
                elif message == "черный список":
                    for user in vk_api.black_list:
                        vk_bot.send_msg(event.user_id, message=user[0], attachment=user[1])
                elif message == "добавить в избранное":
                    if len(stack) == 0 or not flag_wish:
                        vk_bot.send_msg(event.user_id, "Добавлять нечего")
                    else:
                        vk_api.wish_list.append(stack.pop())
                        flag_wish = True
                        vk_bot.send_msg(event.user_id, f"Добавил в список избранных")
                elif message == "не нравится":
                    if len(stack) == 0 or not flag_black:
                        vk_bot.send_msg(event.user_id, "Добавлять нечего")
                    else:
                        vk_api.black_list.append(stack.pop())
                        flag_black = True
                        vk_bot.send_msg(event.user_id, f"Добавил в черный список")
                elif message == "показать":
                    data = get_user_for_bot(event.user_id)
                    stack.append(data)
                    vk_bot.send_msg(event.user_id, message=data[0], attachment=data[1])
                    flag_wish, flag_black = True, True
                else:
                    vk_bot.send_msg(event.user_id, "К сожалению, такой команды я не знаю")


if __name__ == '__main__':
    main()
