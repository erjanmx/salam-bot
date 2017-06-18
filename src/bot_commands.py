from config.i18n import locales


def user_unfriend(func):
    def wrapper(self):
        friend = self.user.friend()
        if friend:
            self.api_client.send_message(friend, 'message_friend_gone')
            self.user.del_friend()

        func(self)

    return wrapper


class BotCommands:
    commands = (
        'help',
        'stop',
        'start',
        'search',
    )

    def __init__(self, user, api_client):
        self.user = user
        self.api_client = api_client

    def run(self, command):
        run = False

        commands = {cmd: locales[self.user.lang][cmd] for cmd in self.commands}
        for c_key, c_val in commands.items():
            if c_val == command:
                getattr(self, c_key)()
                run = True
                break

        return run

    def help(self):
        self.api_client.send_message(self.user, 'message_help')

    @user_unfriend
    def stop(self):
        self.user.set_status('not_active')
        self.api_client.send_message(self.user, 'message_inactive')

    @user_unfriend
    def start(self):
        self.user.set_status('active')
        self.api_client.send_message(self.user, 'message_active')

    @user_unfriend
    def search(self):
        self.user.set_status('active')
        self.api_client.send_message(self.user, 'message_friend_search')

        if not self.user.add_friend():
            self.api_client.send_message(self.user, 'message_friend_not_found')
        else:
            self.user.friend().set_status('idle')
            self.api_client.send_message(self.user, 'message_friend_found')
            self.api_client.send_message(self.user.friend(), 'message_friend_found_user')

