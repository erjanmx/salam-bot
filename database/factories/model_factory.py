from orator.orm import Factory
from src.models.user import User
from src.models.chat import Chat

factory = Factory()


@factory.define(User)
def users_factory(fake):
    return {
        'id': fake.random_int(),
        'name': fake.name(),
        'chat_id': fake.random_int(),
        'lang': '-',
        'status': 1,
        'gender': 'M',
    }


@factory.define(Chat)
def chats_factory(fake):
    return {
        'started_at': None,
    }
