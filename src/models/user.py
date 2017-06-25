import logging
from . chat import Chat
from orator.orm import scope
from . model import db, Model

logging.getLogger("salam-bot.log")


class User(Model):
    __incrementing__ = False
    __fillable__ = ['id', 'chat_id', 'name', 'lang', 'gender', 'status']

    statuses = {
        'idle': 1,
        'active': 2,
        'not_active': 0,
    }

    def set_status(self, status):
        if status not in self.statuses:
            return False

        return self.update({'status': self.statuses[status]})

    def friend(self):
        u_chat = Chat.where('user_1', self.id).or_where('user_2', self.id).first()

        if u_chat:
            if u_chat.user_2 == self.id:
                friend_id = u_chat.user_1
                u_chat.disable_auto_close()
            else:
                friend_id = u_chat.user_2
        else:
            friend_id = 0

        return User.find(friend_id)

    def del_friend(self):
        return Chat.where('user_1', self.id).or_where('user_2', self.id).delete()

    def add_friend(self):
        added = False
        gender_order = 'asc' if self.gender == 'M' else 'desc'

        friend = User.free() \
                     .active() \
                     .where('id', '<>', self.id) \
                     .order_by('status', 'desc') \
                     .order_by('gender', gender_order) \
                     .order_by(db.raw('RAND()')) \
                     .first()

        if friend:
            try:
                Chat.create(user_1=self.id, user_2=friend.id, started_at=db.raw('now()'))
                added = True
            except:
                logging.error('Failed to add friend {} for user: {}'.format(friend.id, self.id), exc_info=True)

        return added            

    @scope
    def active(self, query):
        return query.where('status', '<>', User.statuses['not_active']) \
                    .where_raw('updated_at > now() - interval 5 day')

    @scope
    def free(self, query):
        users_list = Chat.select_raw('group_concat(user_1, ",", user_2) as ids').first()

        ids = []
        if users_list and users_list.ids:
            ids = [int(u_id) for u_id in str(users_list.ids).split(',') if u_id.isdigit()]

        return query.where_not_in('id', ids)
