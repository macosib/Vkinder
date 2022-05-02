from time import sleep

import vkapi
import vkbot
from vk_api.longpoll import VkEventType
from pprint import pprint

def main():

    vk_bot = vkbot.VKBot()
    vk_api = vkapi.VkApi()



    def get_user_for_bot(user_id):
        city_search, sex_search, bdate_search = vk_api.get_user_info(user_id)
        if sex_search == 2:
            sex_search = 1
        else:
            sex_search = 2
        user_for_bot = None
        while not user_for_bot:
            user_for_bot = vk_api.users_search(city_search, sex_search, bdate_search)
        last_name = user_for_bot[0]['last_name']
        first_name = user_for_bot[0]['first_name']
        link = f'https://vk.com/id{user_for_bot[0]["person_id"]}'
        attachment = []
        for photo in user_for_bot[0]['profile_foto']:
            attachment.append(f'photo{photo["owner_id"]}_{photo["foto_id"]}')
        print(attachment)
        return f'{first_name} {last_name}\n{link}', ','.join(attachment)


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
                    msg = data[0]
                    attach = data[1]
                    vk_bot.send_msg(event.user_id, msg, attachment=attach)
                else:
                    vk_bot.send_msg(event.user_id, "Такой команды я не знаю")

'''Имя Фамилия
ссылка на профиль
три фотографии в виде attachment(https://dev.vk.com/method/messages.send)'''

if __name__ == '__main__':
    main()
