import mock
import unittest
from src.models.model import db
from src.models.user import User
from src.bot_commands import BotCommands
from database.factories.model_factory import factory


class TestBotCommands(unittest.TestCase):
    def setUp(self):
        db.begin_transaction()

        self.user = factory(User).create(lang='ru')
        self.send_message_mock = mock.Mock()

    def tearDown(self):
        db.rollback()

    def test_help(self):
        self.__run_command('помощь')
        
        self.send_message_mock.assert_called_once_with(mock.ANY, 'message_help')

    def test_stop(self):
        self.__run_command('стоп')

        self.send_message_mock.assert_called_once_with(mock.ANY, 'message_inactive')
        self.assertEqual(self.user.status, User.statuses['not_active'])

    def test_start(self):
        self.__run_command('старт')

        self.send_message_mock.assert_called_once_with(mock.ANY, 'message_active')
        self.assertEqual(self.user.status, User.statuses['active'])

    def test_search(self):
        factory(User).create(lang='ru')

        self.__run_command('поиск')

        self.send_message_mock.assert_has_calls([
            mock.call(mock.ANY, 'message_friend_search'), 
            mock.call(mock.ANY, 'message_friend_found'),
            mock.call(mock.ANY, 'message_friend_found_user'),
        ])

        self.assertEqual(self.user.status, User.statuses['active'])
        self.assertEqual(self.user.friend().status, User.statuses['idle'])

    @mock.patch('src.models.user.User.add_friend')
    def test_search_with_no_friend(self, add_friend_mock):
        add_friend_mock.return_value = False
        
        self.__run_command('поиск')

        self.send_message_mock.assert_has_calls([
            mock.call(mock.ANY, 'message_friend_search'), 
            mock.call(mock.ANY, 'message_friend_not_found')
        ])
        self.assertEqual(self.user.status, User.statuses['active'])

    def __run_command(self, command):
        bc = BotCommands(self.user, self.send_message_mock)
        return bc.run(command)


if __name__ == '__main__':
    unittest.main()
