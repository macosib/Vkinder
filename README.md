<img  src="https://cdn.glitch.global/5045ed4d-89cd-4f64-80ba-25a2c76b94b7/bot.png?v=1651674003202"  alt="logo">

# [VKinder](https://vk.com/public213024441 "Сообщество VKinder")  чат-бот ВКонтакте

### Цель проекта

Цель командного проекта - разработать программу-бота для взаимодействия с базами данных социальной сети. Бот будет предлагать различные варианты людей для знакомств в социальной сети Вконтакте в виде диалога с пользователем.

### Инструкция к работе над проектом

Необходимо разработать программу-бота, которая должна выполнять следующие действия:
1. Используя информацию (возраст, пол, город) о пользователе, который общается с пользователем в ВК, сделать поиск других людей (других пользователей ВК) для знакомств.
2. У тех людей, которые подошли под критерии поиска, получить три самые популярные фотографии в профиле. Популярность определяется по количеству лайков.
3. Выводить в чат с ботом информацию о пользователе в формате:

```
 Имя Фамилия
 ссылка на профиль
 три фотографии в виде attachment(https://dev.vk.com/method/messages.send)
```

4. Должна быть возможность перейти к следующему человеку с помощью команды или кнопки.
5. Сохранить пользователя в список избранных.
6. Вывести список избранных людей.

 ### Настройка бота

1. Установить зависимости из файла `requirements.txt`. С помощью команды `pip install -r requirements.txt`.
2. Перейдите в main.py, основная для работы с ботом.  Запустите бота.
3. В modules.py необходимо изменить пароль, вместо YOURPASSWORD должен быть Ваш пароль для создания базы данных. Для данного бота использовался PosеgreSQL и PgAdmin. После чего необходимо запустить скрипт module.py, база данных будет создана.
4. Чтобы перейти к диалогу с ботом, необходимо перейти по ссылке [VKinder](https://vk.com/im?media=&sel=-213024441&v=)
5. Для активации бота написать сообщение "привет".
6. При нажатии кнопки "Показать" будут выданы результаты, которые соответсвуют прописанному, согласно инструкциям, алгоритму.
Бот выбирает анкеты людей противоположного Вам пола, из Вашего города, одного и того же с Вами возраста. В случае, если у пользователя бота отсутствует информация о городе, по умолчанию используется город Москва.
7. При нажатии кнопки "Добавить в избранное" анкета записывается в базу данных, в список избранных. Просмотреть все избранные анкеты можно при нажатии кнопки "Список избранных".
8. При нажатии кнопки "Не нравится" анкета записывается в базу данных, в черный список. Просмотреть все анкеты из черного списка можно при нажатии кнопки "Черный список".


### Дополнительные требования к проекту (необязательные для получения зачёта)

1. Получать токен от пользователя с нужными правами.
2. Добавлять человека в чёрный список, чтобы он больше не попадался при поиске, используя БД.
3. Создать кнопки в чате для взаимодействия с ботом.
4. Добавить возможность ставить/убирать лайк выбранной фотографии.
5. К списку фотографий из аватарок добавлять список фотографий, где отмечен пользователь.
6. В ВК максимальная выдача при поиске - 1000 человек. Подумать, как это ограничение можно обойти.
7. Можно усложнить поиск, добавив поиск по интересам. Разбор похожих интересов (группы, книги, музыка, интересы) нужно будет провести с помощью анализа текста.
8. У каждого критерия поиска должны быть свои веса, то есть совпадение по возрасту должно быть важнее общих групп, интересы по музыке - важнее книг, наличие общих друзей - важнее возраста и т.д.
