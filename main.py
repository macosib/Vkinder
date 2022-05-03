from time import sleep

import vkapi
import vkbot
from vk_api.longpoll import VkEventType


def main():
    vk_bot = vkbot.VKBot()
    vk_api = vkapi.VkApi()

    # def get_user_for_bot(user_id):
    #     city_search, sex_search, bdate_search = vk_api.get_user_info(user_id)
    #     if sex_search == 2:
    #         sex_search = 1
    #     else:
    #         sex_search = 2
    #     user_for_bot = vk_api.search_user(city_search, sex_search, bdate_search)
    #     return f'{user_for_bot[0]} {user_for_bot[1]}\n{user_for_bot[2]}', user_for_bot[3]

    def get_user_for_bot(user_id, user_for_bot=None):
        city_search, sex_search, bdate_search = vk_api.get_user_info(user_id)
        if sex_search == 2:
            sex_search = 1
        else:
            sex_search = 2
        while not user_for_bot:
            user_for_bot = vk_api.search_user(city_search, sex_search, bdate_search)
        print(user_for_bot)
        return f'{user_for_bot[0][0]} {user_for_bot[0][1]}\n{user_for_bot[0][2]}', user_for_bot[0][3]



    for event in vk_bot.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                message = event.text.lower()
                if message == "привет":
                    vk_bot.send_msg(event.user_id, 'Привет, для начала работы нажми кнопку "Показать далее"')
                elif message == "показать список избранных":
                    msg = get_user_for_bot(event.user_id)
                    vk_bot.send_msg(event.user_id, msg)
                elif message == "добавить в избранное":
                    vk_bot.send_msg(event.user_id, f"Добавил в список избраннных")
                elif message == "не нравится":
                    vk_bot.send_msg(event.user_id, "Ну и ладно, поищем других")
                elif message == "показать далее":
                    data = get_user_for_bot(event.user_id)
                    msg, attach = data[0], data[1]
                    vk_bot.send_msg(event.user_id, msg, attachment=attach)
                else:
                    vk_bot.send_msg(event.user_id, "Такой команды я не знаю")


if __name__ == '__main__':
    main()
