from . model import Model


class UserFriend(Model):
    __timestamps__ = False
    __fillable__ = ['user_1', 'user_2', 'started_at']
