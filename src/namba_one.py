import requests


class NambaOne:
    base_url = 'https://api.namba1.co/'

    def __init__(self, token):
        self.headers = {
            'X-Namba-Auth-Token': token
        }

    def post(self, url, params):
        response = requests.post(self.base_url + url, data=params, headers=self.headers).json()
        if not response['success']:
            raise ValueError(response['message'])
        
        return response['data']
        
    def create_chat(self, user_id, name='', image=''):
        params = {
            'name': name,
            'image': image,
            'members[]': user_id,
        }

        return self.post('chats/create', params)

    def send_message(self, chat_id, content='', content_type='text/plain'):
        params = {
            'type': content_type,
            'content': content,
        }
        return self.post('chats/{}/write'.format(chat_id), params)
