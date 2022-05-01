import sqlalchemy as sql
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from pprint import pprint

"""
Creating a database tables according to a flowchart
"""

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


# creating a table for a match user
class FavoriteUser(Base):
    __tablename__ = 'favorites_list'
    id_favorites = sql.Column(sql.Integer, primary_key=True, autoincrement=True, nullable=False)
    vk_user_id = sql.Column(sql.Integer, unique=True, nullable=False)
    vk_user_first_name = sql.Column(sql.String)
    vk_user_last_name = sql.Column(sql.String)
    vk_user_city = sql.Column(sql.String)
    vk_user_bdate = sql.Column(sql.String)
    vk_user_sex = sql.Column(sql.String)
    id_bot_user = sql.Column(sql.Integer, sql.ForeignKey('bot_user.id_bot_user', ondelete='CASCADE'))


# creating a table for a blacklisted accounts
class BlackList(Base):
    __tablename__ = 'black_list'
    id_black_list = sql.Column(sql.Integer, primary_key=True, autoincrement=True, nullable=False)
    vk_user_id = sql.Column(sql.Integer, unique=True, nullable=False)
    vk_user_first_name = sql.Column(sql.String)
    vk_user_last_name = sql.Column(sql.String)
    vk_user_city = sql.Column(sql.String)
    vk_user_bdate = sql.Column(sql.String)
    vk_user_sex = sql.Column(sql.String)
    id_bot_user = sql.Column(sql.Integer, sql.ForeignKey('bot_user.id_bot_user', ondelete='CASCADE'))


# creating a table for a photo information
class VkUserPhoto(Base):
    __tablename__ = 'vk_user_photo'
    id_photo = sql.Column(sql.Integer, primary_key=True, autoincrement=True, nullable=False)
    photo_likes_count = sql.Column(sql.Integer, unique=False)
    photo_URL = sql.Column(sql.Integer, unique=True, nullable=False)
    vk_user_id = sql.Column(sql.Integer, sql.ForeignKey('favorites_list.vk_user_id', ondelete='CASCADE'))


"""
Creating a functions to work with database
"""


# adds new bot user
def add_bot_user(id_vk):
    new_entry = BotUser(
        bot_user_vk_id=id_vk
    )
    session.add(new_entry)
    session.commit()
    return True


# checks if bot user already in database
def check_if_bot_user_exists(id_vk):
    new_entry = session.query(BotUser).filter_by(bot_user_vk_id=id_vk).first()
    return new_entry


# adds new match to favorites list
def add_new_match_to_favorites(vk_user_id, first_name, last_name, city, bdate, sex, id_bot_user):
    new_entry = FavoriteUser(
        vk_user_id=vk_user_id,
        vk_user_first_name=first_name,
        vk_user_last_name=last_name,
        vk_user_city=city,
        vk_user_bdate=bdate,
        vk_user_sex=sex,
        id_bot_user=id_bot_user
    )
    session.add(new_entry)
    session.commit()
    return True


# adds new match to black list
def add_new_match_to_black_list(vk_user_id, first_name, last_name, city, bdate, sex, id_bot_user):
    new_entry = FavoriteUser(
        vk_user_id=vk_user_id,
        vk_user_first_name=first_name,
        vk_user_last_name=last_name,
        vk_user_city=city,
        vk_user_bdate=bdate,
        vk_user_sex=sex,
        id_bot_user=id_bot_user
    )
    session.add(new_entry)
    session.commit()
    return True


# deletes match from black list
def delete_match_from_black_list(vk_id):
    new_entry = session.query(BlackList).filter_by(vk_user_id=vk_id).first()
    session.delete(new_entry)
    session.commit()


# deletes match from favorites list
def delete_match_from_favorites_list(vk_id):
    new_entry = session.query(FavoriteUser).filter_by(vk_user_id=vk_id).first()
    session.delete(new_entry)
    session.commit()


# checks if match already present in database (both black and favorites list)
def check_if_match_exists(id_vk):
    favorite_list = session.query(FavoriteUser).filter_by(vk_user_id=id_vk).first()
    black_list = session.query(BlackList).filter_by(vk_user_id=id_vk).first()
    return favorite_list, black_list


# adds photo of the match to photo table
def add_photo_of_the_match(photo_likes_count, photo_url, vk_user_id):
    new_entry = VkUserPhoto(
        photo_likes_count=photo_likes_count,
        photo_URL=photo_url,
        vk_user_id=vk_user_id,
    )
    session.add(new_entry)
    session.commit()
    return True


# shows all favorite users of current bot user
def show_all_favorites(id_):
    bot_user = session.query(BotUser).filter_by(bot_user_vk_id=id_).first()
    all_favorites = session.query(FavoriteUser).filter_by(id_bot_user=bot_user.id_bot_user).all()
    return all_favorites


# shows all blacklisted users of current bot user
def show_all_blacklisted(id_):
    bot_user = session.query(BotUser).filter_by(bot_user_vk_id=id_).first()
    all_blacklisted = session.query(BlackList).filter_by(id_bot_user=bot_user.id_bot_user).all()
    return all_blacklisted


if __name__ == '__main__':
    Base.metadata.create_all(engine)



