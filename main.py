import vkapi
import vkbot
from vk_api.longpoll import VkEventType

def main():

    vk_bot = vkbot.VKBot()
    vk_api = vkapi.VkApi()

    for event in vk_bot.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                message = event.text.lower()
                user_id = event.user_id
                user_info = vk_api.get_user_info(user_id)
                user_sex = vk_api.get_user_info(user_id).get('sex')
                user_city = vk_api.get_user_info(user_id).get('home_town', 1)
                user_bdate = vk_api.get_user_info(user_id).get('bdate')
                wish_list = vk_api.users_search(user_city, user_sex - 1)
                print(wish_list)
                #
                # print(user_info)
                # print(user_sex, user_city, user_bdate)


                if message == "привет":
                    vk_bot.send_msg(event.user_id, f"Привет, {user_id}")
                elif message == "показать список избранных":
                    vk_bot.send_msg(event.user_id, f"Показываю избранных")
                elif message == "добавить в избранное":
                    vk_bot.send_msg(event.user_id, f"Добавил в избраннное")
                elif message == "не нравится":
                    vk_bot.send_msg(event.user_id, "Ну и ладно, поищем других")
                elif message == "показать далее":
                    vk_bot.send_msg(event.user_id, "Как скажешь босс")
                else:
                    vk_bot.send_msg(event.user_id, "Такой команды я не знаю")

#
# user_id = 'yarowoe'
# # user_city = input('Введите город: ')
# # user_sex = int(input('Введите пол, 1 — Женщина; 2 — Мужчина; 0 — Любой: '))
# # age = int(input('Введите возраст: '))
# vk_1 = Vk_api.VkApi()
# # print(*vk_1.get_photos_from_profile(8487111), sep='\n')
# vk_1.users_search('Новосибирск', 1, 30, 10))
# # sleep(5)
# print()
# print()
# pprint.pprint(vk_1.get_users())
# sleep(5)
# print()
# print()
# pprint.pprint(vk_1.get_users())
# pprint.pprint(vk_1.get_user_info(user_id))


if __name__ == '__main__':
    main()
