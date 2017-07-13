import os
import importlib


def __get_app_languages():
    return [lang.strip() for lang in str(os.getenv('APP_LANGS')).split(',')]


def __get_locales():
    locales = {'-': {'message_choose_language': ''}}

    languages = ''
    app_langs = __get_app_languages()

    for i in range(len(app_langs)):
        i18n = importlib.import_module('.locales.' + app_langs[i], 'config')

        locales[app_langs[i]] = i18n.locale

        languages += '\n {}️⃣ {}'.format(i + 1, i18n.locale['language'])
        locales['-']['message_choose_language'] += '{}. '.format(i18n.locale['choose_language'])

    locales['-']['message_choose_language'] += '\n{}'.format(languages)

    return locales


def __default_locale():
    default = '-'
    locales = __get_app_languages()
    if len(locales) == 1:
        default = locales[0]

    return default


locales = __get_locales()
default_locale = __default_locale()
