from . models.user import User
from config.i18n import locales
from . namba_one import NambaOne
from . bot_commands import BotCommands
from config.app import NAMBA_ONE_API_TOKEN


class Bot:

    events = {
        'new/chat': 'event_user_follow',
        'message/new': 'event_new_message',
        'user/follow': 'event_user_follow',
        'user/unfollow': 'event_user_unfollow',
        'message/update': 'event_message_update',
    }

    def __init__(self, request_body):
        self.user = None
        self.event = request_body['event']
        self.request = request_body['data']
        self.api_client = NambaOne(NAMBA_ONE_API_TOKEN)

    def run(self):
        getattr(self, self.events[self.event])()

    def event_user_follow(self):
        self.user = User.update_or_create({'id': self.request['id']}, {
            'lang': '-',
            'name': self.request['name'],
            'gender': self.request['gender'],
            'status': User.statuses['active'],

            'chat_id': self.api_client.create_chat(self.request['id'])['id']
        })

        self.api_client.send_message(self.user, 'message_choose_language')

    def event_user_unfollow(self):
        user = User.find_or_fail(self.request['id'])
        if user.friend():
            user.del_friend()
            self.api_client.send_message(user.friend(), 'message_friend_gone')
        user.set_status('not_active')

    def event_new_message(self):
        user = User.find_or_fail(self.request['sender_id'])
        content = self.request['content'].strip()

        if user.lang == '-':
            if content.isnumeric() and len(locales) > int(content):
                user.update({'lang': list(locales.keys())[int(content)]})
                self.api_client.send_message(user, 'message_help')
            else:
                self.api_client.send_message(user, 'message_choose_language')
            return

        if getattr(BotCommands(user, self.api_client), 'run')(content.lower()):
            return

        if not user.friend():
            user.set_status('active')
            self.api_client.send_message(user, 'message_no_friend')
            return

        if self.request['type'] == 'text/plain':
            content = '{}: {}'.format(locales[user.lang]['text_friend'], content)

        self.api_client.send_message(user.friend(), content, self.request['type'])

