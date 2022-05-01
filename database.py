import sqlalchemy as sql
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from pprint import pprint

# Connecting a db
Base = declarative_base()

# an Engine, which the Session will use for connection
engine = sql.create_engine('postgresql://postgres:Mimishka20@localhost:5432/vKinder_bot_db')

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()
connection = engine.connect()


# creating a table for a bot user
class BotUser(Base):
    __tablename__ = "bot_user"
    id_bot_user = sql.Column(sql.Integer, primary_key=True, autoincrement=True, nullable=False)
    bot_user_vk_id = sql.Column(sql.Integer, unique=True, nullable=False)
    bot_user_first_name = sql.Column(sql.String)
    bot_user_last_name = sql.Column(sql.String)
    bot_user_bdate = sql.Column(sql.String)
    bot_user_sex = sql.Column(sql.String)
    bot_user_hometown = sql.Column(sql.String)


# creating a table for a match
class VkUserMatch(Base):
    __tablename__ = 'vk_user_match'
    id_vk_user = sql.Column(sql.Integer, primary_key=True, autoincrement=True, nullable=False)
    vk_user_id = sql.Column(sql.Integer, unique=True, nullable=False)
    vk_user_first_name = sql.Column(sql.String)
    vk_user_last_name = sql.Column(sql.String)
    vk_user_bdate = sql.Column(sql.String)
    vk_user_sex = sql.Column(sql.String)
    vk_user_hometown = sql.Column(sql.String)
    id_bot_user = sql.Column(sql.Integer, sql.ForeignKey('bot_user.id_bot_user', ondelete='CASCADE'))


# creating a table for a favorite photos
class FavoritePhotosList(Base):
    __tablename__ = 'favorites_list'
    id_favorites = sql.Column(sql.Integer, primary_key=True, autoincrement=True, nullable=False)
    vk_user_id = sql.Column(sql.Integer, sql.ForeignKey('vk_user_match.id_vk_user', ondelete='CASCADE'))


# creating a table for a blacklisted accounts
class BlackList(Base):
    __tablename__ = 'black_list'
    id_black_list = sql.Column(sql.Integer, primary_key=True, autoincrement=True, nullable=False)
    vk_user_id = sql.Column(sql.Integer, sql.ForeignKey('vk_user_match.id_vk_user', ondelete='CASCADE'))


# creating a table for a photo information
class VkUserPhoto(Base):
    __tablename__ = 'vk_user_photo'
    id_photo = sql.Column(sql.Integer, primary_key=True, autoincrement=True, nullable=False)
    photo_likes_count = sql.Column(sql.Integer, unique=False)
    photo_URL = sql.Column(sql.Integer, unique=True, nullable=False)
    vk_user_id = sql.Column(sql.Integer, sql.ForeignKey('vk_user_match.id_vk_user', ondelete='CASCADE'))
    photo_id = sql.Column(sql.Integer, unique=True)


if __name__ == '__main__':
    Base.metadata.create_all(engine)



