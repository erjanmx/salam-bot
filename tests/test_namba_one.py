import mock
import unittest
from src.namba_one import NambaOne


class TestNambaOne(unittest.TestCase):
    test_token = 'test_token'

    def setUp(self):
        self.namba_one = NambaOne(self.test_token)

    def test_header(self):
        expected_headers = {
            'X-Namba-Auth-Token': 'test_token'
        }

        self.assertEqual(self.namba_one.headers, expected_headers)

    @mock.patch('src.namba_one.requests.post')
    def test_create_chat(self, post_mock):
        user_id = 1
        name = 'test_name'
        image = 'test_image'

        result = self.namba_one.create_chat(user_id, name, image)
        
        post_mock.assert_called_once_with(
            'https://api.namba1.co/chats/create', 
            data = {
                'name': name, 
                'image': image, 
                'members[]': user_id
            }, 
            headers = {
                'X-Namba-Auth-Token': self.test_token
            }
        )

    @mock.patch('src.namba_one.requests.post')
    def test_send_message(self, post_mock):
        self.namba_one.send_message(1, 'Hi There!', 'text/plain')
        
        post_mock.assert_called_once_with(
            'https://api.namba1.co/chats/1/write', 
            data = {
                'content': 'Hi There!', 
                'type': 'text/plain', 
            }, 
            headers = {
                'X-Namba-Auth-Token': self.test_token
            }
        )


if __name__ == '__main__':
    unittest.main()
