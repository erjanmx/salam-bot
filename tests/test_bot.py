import mock
import unittest
from src.bot import Bot
from config.i18n import locales
from src.models.model import db
from src.models.user import User
from src.models.chat import Chat
from database.factories.model_factory import factory


class TestBot(unittest.TestCase):
    def setUp(self):
        db.begin_transaction()

    def tearDown(self):
        db.rollback()

    @mock.patch('src.namba_one.NambaOne.send_message')
    @mock.patch('src.namba_one.NambaOne.create_chat')
    def test_event_user_follow(self, n1_create_chat, n1_send_message):
        user_id = 1
        chat_id = 10
        lang = '-'

        n1_create_chat.return_value = {'id': chat_id}

        self.__run_bot('user/follow', {
            'id': user_id,
            'name': 'John',
            'gender': 'M',
            'lang': lang,
        })

        user = User.find_or_fail(user_id)
        self.assertEqual(user.name, 'John')
        self.assertEqual(user.gender, 'M')
        self.assertEqual(user.lang, lang)

        n1_create_chat.assert_called_once_with(user_id)
        n1_send_message.assert_called_once_with(chat_id, locales[lang]['message_choose_language'], mock.ANY)


    def test_event_user_unfollow(self):
        user = factory(User).create(status=User.statuses['active'])
        
        self.__run_bot('user/unfollow', {
            'id': user.id,
        })

        user_to_check = User.find(user.id)
        self.assertEqual(user_to_check.status, User.statuses['not_active'])

    @mock.patch('src.namba_one.NambaOne.send_message')
    def test_event_user_unfollow_with_friend(self, n1_send_message):
        user_1 = factory(User).create()
        user_2 = factory(User).create()
        
        factory(Chat).create(
            user_1=user_1.id,
            user_2=user_2.id
        )

        self.__run_bot('user/unfollow', {
            'id': user_1.id,
        })

        n1_send_message.assert_called_once_with(user_2.chat_id, 'message_friend_gone', mock.ANY)

    @mock.patch('src.namba_one.NambaOne.send_message')
    def test_event_new_message_with_no_language(self, n1_send_message):
        user_id = 1
        user_chat_id = 10
        user = factory(User).create(id=user_id, chat_id=user_chat_id)
        
        self.__run_bot('message/new', {
            'sender_id': user_id,
            'content': 'text',
        })

        n1_send_message.assert_called_once_with(user_chat_id, locales[user.lang]['message_choose_language'], mock.ANY)

    @mock.patch('src.namba_one.NambaOne.send_message')
    def test_event_new_message_set_ru_language(self, n1_send_message):
        user_id = 1
        user_chat_id = 10
        lang = 'ru'
        user = factory(User).create(id=user_id, chat_id=user_chat_id)
        
        self.__run_bot('message/new', {
            'sender_id': user_id,
            'content': '1',
        })

        n1_send_message.assert_called_once_with(user_chat_id, locales[lang]['message_help'], mock.ANY)

    @mock.patch('src.bot_commands.BotCommands.run')
    def test_event_new_message_call_command(self, mock_bc):
        user = factory(User).create(lang='ru')

        content = 'content'
        self.__run_bot('message/new', {
            'sender_id': user.id,
            'content': content,
        })

        mock_bc.assert_called_once_with(content)

    @mock.patch('src.namba_one.NambaOne.send_message')
    def test_event_new_message_with_no_friend(self, n1_send_message):
        user_chat_id = 10
        user = factory(User).create(chat_id=user_chat_id, lang='ru', status=User.statuses['idle'])

        self.__run_bot('message/new', {
            'sender_id': user.id,
            'content': '',
        })

        user_to_check = User.find_or_fail(user.id)
        self.assertEqual(user_to_check.status, User.statuses['active'])

        n1_send_message.assert_called_once_with(user_chat_id, locales[user.lang]['message_no_friend'], mock.ANY)

    @mock.patch('src.namba_one.NambaOne.send_message')
    def test_event_new_message_with_friend(self, n1_send_message):
        user_2_chat_id = 10
        
        user_1 = factory(User).create(lang='ru')
        user_2 = factory(User).create(chat_id=user_2_chat_id, lang='ru')
        factory(Chat).create(
            user_1=user_1.id,
            user_2=user_2.id
        )

        self.__run_bot('message/new', {
            'sender_id': user_1.id,
            'content': 'Hello',
            'type': 'text/plain',
        })

        check_content = locales[user_2.lang]['text_friend'] + ': ' + 'Hello'
        n1_send_message.assert_called_once_with(user_2_chat_id, check_content, 'text/plain')

    @mock.patch('src.namba_one.NambaOne.send_message')
    def test_event_close_idle_chats(self, n1_send_message):
        user_1_chat_id = 1
        user_2_chat_id = 2

        user_1 = factory(User).create(chat_id = user_1_chat_id)
        user_2 = factory(User).create(chat_id = user_2_chat_id)
        
        chat_1 = factory(Chat).create(
            user_1=user_1.id,
            user_2=user_2.id,
            started_at='2000-01-01 00:00:00'
        )

        self.__run_bot('cron/close_idle_chats')

        n1_send_message.assert_has_calls([
            mock.call(user_1_chat_id, 'message_chat_close_friend', mock.ANY), 
            mock.call(user_2_chat_id, 'message_chat_close_user', mock.ANY)
        ])

        self.assertEqual(Chat.find(chat_1.id), None)

    def __run_bot(self, event, data=()):
        bot = Bot({
            'event': event,
            'data': data,
        })
        bot.run()


if __name__ == '__main__':
    unittest.main()
