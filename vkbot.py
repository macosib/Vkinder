from random import randrange
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
import config
from vk_api.utils import get_random_id



class VKBot:

    def __init__(self):
        self.token = config.token_vkinder
        self.vk_session = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(self.vk_session)
        self.keyboard = self.current_keyboard()

    def send_msg(self, user_id, message):
        self.vk_session.method('messages.send',
                               {'user_id': user_id,
                                'message': message,
                                'random_id': get_random_id(),
                                'keyboard': self.keyboard})

    @staticmethod
    def current_keyboard():
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Показать далее', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Добавить в избранное', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Не нравится', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button('Показать список избранных', color=VkKeyboardColor.SECONDARY)
        return keyboard.get_keyboard()


def main():
    vk_bot = VKBot()

    for event in vk_bot.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                message = event.text.lower()
                if message == "привет":
                    vk_bot.send_msg(event.user_id, f"Привет, {event.user_id}")
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


if __name__ == '__main__':
    main()
