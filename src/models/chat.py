from . model import Model
from orator.orm import scope


class Chat(Model):
    __timestamps__ = False
    __fillable__ = ['user_1', 'user_2', 'started_at']

    @scope
    def idle(self, query):
        return query.where_raw('started_at < now() - interval 3 minute')

    def disable_auto_close(self):
        if self.started_at:
            self.update({'started_at': None})

        return self
