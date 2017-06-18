import requests
from config.i18n import locales


def translate(func):
    def wrapper(self, user, content, content_type='text/plain'):
        if content in locales[user.lang]:
            content = locales[user.lang][content]
        func(self, user.chat_id, content, content_type)

    return wrapper


class NambaOne:
    base_url = 'https://api.namba1.co/'

    def __init__(self, token):
        self.headers = {
            'X-Namba-Auth-Token': token
        }

    def post(self, url, params):
        response = requests.post(self.base_url + url, data=params, headers=self.headers).json()
        if not response['success']:
            raise Exception('API_CALL_ERROR')
        
        return response['data']
        
    def create_chat(self, user_id, name='', image=''):
        params = {
            'name': name,
            'image': image,
            'members[]': user_id,
        }

        return self.post('chats/create', params)

    @translate
    def send_message(self, chat_id, content='', content_type='text/plain'):
        params = {
            'type': content_type,
            'content': content,
        }
        return self.post('chats/{}/write'.format(chat_id), params)
