from config.i18n import locales


def user_unfriend(func):
    def wrapper(self):
        friend = self.user.friend()
        if friend:
            self.send_message(friend, 'message_friend_gone')
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

    def __init__(self, user, send_message):
        self.user = user
        self.send_message = send_message

    def run(self, command):
        run = False

        if self.user.lang == '-':
            if command.isdigit() and 0 < int(command) < len(locales):
                self.user.update({
                    'lang': list(locales.keys())[int(command)]
                })
                self.send_message(self.user, 'message_help')
            else:
                self.send_message(self.user, 'message_choose_language')
            return True

        commands = {cmd: locales[self.user.lang][cmd] for cmd in self.commands}
        for c_key, c_val in commands.items():
            if c_val == command or (isinstance(c_val, list) and command in c_val):
                getattr(self, c_key)()
                run = True
                break

        return run

    def help(self):
        self.send_message(self.user, 'message_help')

    @user_unfriend
    def stop(self):
        self.user.set_status('not_active')
        self.send_message(self.user, 'message_inactive')

    @user_unfriend
    def start(self):
        self.user.set_status('active')
        self.send_message(self.user, 'message_active')

    @user_unfriend
    def search(self):
        self.user.set_status('active')
        self.send_message(self.user, 'message_friend_search')

        if not self.user.add_friend():
            self.send_message(self.user, 'message_friend_not_found')
        else:
            self.user.friend().set_status('idle')
            self.send_message(self.user, 'message_friend_found')
            self.send_message(self.user.friend(), 'message_friend_found_user')
