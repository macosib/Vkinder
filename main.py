from time import sleep

import vkapi
import vkbot
from vk_api.longpoll import VkEventType


def main():

    vk_bot = vkbot.VKBot()
    vk_api = vkapi.VkApi()
    stack = []

    def get_user_for_bot(user_id):
        city_search, sex_search, bdate_search = vk_api.get_user_info(user_id)
        user_for_bot = vk_api.search_user(city_search, sex_search, bdate_search)
        return f'{user_for_bot[0]} {user_for_bot[1]}\n{user_for_bot[2]}', user_for_bot[3]


    for event in vk_bot.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                message = event.text.lower()
                if message == "привет":
                    vk_bot.send_msg(event.user_id, 'Привет, для начала работы нажми кнопку "Показать далее"')
                elif message == "показать список избранных":
                    for user in vk_api.wish_list:
                        vk_bot.send_msg(event.user_id, message=user[0], attachment=user[1])
                elif message == "добавить в избранное":
                    if len(stack) == 0:
                        print('Добавлять нечего')
                    else:
                        vk_api.wish_list.append(stack[-1])
                        vk_bot.send_msg(event.user_id, f"Добавил в список избранных")
                elif message == "не нравится":
                    vk_bot.send_msg(event.user_id, "Ну и ладно, поищем других")
                elif message == "показать далее":
                    data = get_user_for_bot(event.user_id)
                    stack.append(data)
                    vk_bot.send_msg(event.user_id, message=data[0], attachment=data[1])
                else:
                    vk_bot.send_msg(event.user_id, "Такой команды я не знаю")


if __name__ == '__main__':
    main()
