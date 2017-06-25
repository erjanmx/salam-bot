import unittest
from src.models.model import db
from src.models.user import User
from src.models.chat import Chat
from database.factories.model_factory import factory


class TestUser(unittest.TestCase):
    def setUp(self):
        db.begin_transaction()

    def tearDown(self):
        db.rollback()

    def test_set_status_active(self):
        user = factory(User).create(status=User.statuses['idle'])
        user.set_status('active')

        self.assertEqual(user.status, User.statuses['active'])

    def test_set_status_wrong(self):
        user = factory(User).create(status=User.statuses['idle'])
        user.set_status('status_that_does_not_exist')

        self.assertEqual(user.status, User.statuses['idle'])

    def test_friend(self):
        user = factory(User).create()

        self.assertEqual(user.friend(), None)

    def test_add_friend_with_one_user(self):
        user_1 = factory(User).create()

        self.assertFalse(user_1.add_friend())

    def test_add_friend_with_two_users(self):
        user_1 = factory(User).create(lang='ru')
        user_2 = factory(User).create(lang='ru')

        user_1.add_friend()

        self.assertEqual(user_1.friend().id, user_2.id)
        self.assertEqual(user_2.friend().id, user_1.id)

    def test_add_friend_with_different_users(self):
        active_user_1 = factory(User).create(status=User.statuses['active'], lang='ru')
        active_user_2 = factory(User).create(status=User.statuses['active'], lang='ru')
        factory(User).make(status=User.statuses['idle'], lang='ru')
        factory(User).make(status=User.statuses['not_active'], lang='ru')

        active_user_1.add_friend()

        self.assertEqual(active_user_1.friend().id, active_user_2.id)

    def test_del_friend(self):
        user_1 = factory(User).create()
        user_2 = factory(User).create()

        self.__make_friends(user_1, user_2)

        user_1.del_friend()

        self.assertEqual(user_1.friend(), None)

    @staticmethod
    def __make_friends(user_1, user_2):
        factory(Chat).create(
            user_1=user_1.id,
            user_2=user_2.id
        )


if __name__ == '__main__':
    unittest.main()
