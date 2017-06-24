import logging
from . models.user import User
from config.i18n import locales
from . namba_one import NambaOne
from . bot_commands import BotCommands
from config.app import NAMBA_ONE_API_TOKEN
from . models.chat import Chat

logging.getLogger("salam-bot.log")


class Bot:

    events = {
        'new/chat': 'event_user_follow',
        'message/new': 'event_new_message',
        'user/follow': 'event_user_follow',
        'user/unfollow': 'event_user_unfollow',
        'message/update': 'event_message_update',

        'cron/close_idle_chats': 'event_close_idle_chats',
    }

    def __init__(self, request_body):
        self.user = None
        self.event = request_body['event']
        self.request = request_body['data']
        self.api_client = NambaOne(NAMBA_ONE_API_TOKEN)

    def run(self):
        logging.info(self.event)
        getattr(self, self.events[self.event])()

    def event_user_follow(self):
        self.user = User.update_or_create({'id': self.request['id']}, {
            'lang': '-',
            'name': self.request['name'],
            'gender': self.request['gender'],
            'status': User.statuses['active'],

            'chat_id': self.api_client.create_chat(self.request['id'])['id']
        })

        self.__send_message(self.user, 'message_choose_language')

    def event_user_unfollow(self):
        user = User.find_or_fail(self.request['id'])
        if user.friend():
            self.__send_message(user.friend(), 'message_friend_gone')
            user.del_friend()
        user.set_status('not_active')

    def event_new_message(self):
        user = User.find_or_fail(self.request['sender_id'])
        content = self.request['content'].strip()

        if getattr(BotCommands(user, self.__send_message), 'run')(content.lower()):
            return

        if not user.friend():
            user.set_status('active')
            self.__send_message(user, 'message_no_friend')
            return

        if self.request['type'] == 'text/plain':
            content = '{}: {}'.format(locales[user.friend().lang]['text_friend'], content)

        self.__send_message(user.friend(), content, self.request['type'])

    def event_message_update(self):
        pass

    def event_close_idle_chats(self):
        idle_chats = Chat.idle().get()
        for chat in idle_chats:
            user = User.find(chat.user_1)
            self.__send_message(user, 'message_chat_close_friend')
            user.set_status('active')
            self.__send_message(User.find(chat.user_2), 'message_chat_close_user')
            chat.delete()

    def __send_message(self, user, content, content_type = 'text/plain'):
        if content in locales[user.lang]:
            content = locales[user.lang][content]

        self.api_client.send_message(user.chat_id, content, content_type)
