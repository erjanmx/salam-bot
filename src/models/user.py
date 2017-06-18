from orator.orm import scope
from . model import db, Model
from . user_friend import UserFriend


class User(Model):
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
        uf = UserFriend.where('user_1', self.id).or_where('user_2', self.id).first()

        if uf:
            friend_id = uf.user_1 if uf.user_2 == self.id else uf.user_2
        else:
            friend_id = 0

        return User.find(friend_id)

    def del_friend(self):
        return UserFriend.where('user_1', self.id).or_where('user_2', self.id).delete()

    def add_friend(self):
        gender_order = 'asc' if self.gender == 'M' else 'desc'

        friend = User.free() \
                     .active() \
                     .where('id', '<>', self.id) \
                     .order_by('status', 'desc') \
                     .order_by('gender', gender_order) \
                     .order_by(db.raw('RAND()')) \
                     .first()

        if not friend:
            return False

        return UserFriend.create(user_1=self.id, user_2=friend.id)

    @scope
    def active(self, query):
        return query.where('status', '<>', User.statuses['not_active']) \
                    .where_raw('updated_at > now() - interval 5 day')

    @scope
    def free(self, query):
        users_list = UserFriend.select_raw('group_concat(user_1, ",", user_2) as ids').first()

        users = users_list.ids or []
        ids = [int(users[i]) for i in range(0, len(users), 2)]

        return query.where_not_in('id', ids)
