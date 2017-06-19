from orator.orm import Factory
from src.models.user import User
from src.models.user_friend import UserFriend
factory = Factory()


@factory.define(User)
def users_factory(fake):
    return {
        'id': fake.random_int(),
        'name': fake.name(),
        'chat_id': fake.random_int(),
        'lang': 'ru',
        'status': 1,
        'gender': 'M',
    }

@factory.define(UserFriend)
def userfriends_factory(fake):
    return {
        'started_at': None,
    }

