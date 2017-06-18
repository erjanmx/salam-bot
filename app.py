import json
import logging as log
from src.bot import Bot
from config.app import *
from flask import Flask, request, abort, jsonify

app = Flask(__name__)

log.basicConfig(filename='salam-bot.log')


@app.route('/', methods=['POST'])
def entry():
    try:
        if request.args.get(SALAM_BOT_TOKEN_KEY) != SALAM_BOT_TOKEN_VALUE:
            raise Exception('BAD_TOKEN')

        bot = Bot(
            json.loads(
                request.get_data()
            )
        )

        bot.run()

        return jsonify({
            'success': 'true'
        })
    except Exception as e:
        log.error(e)
        abort(404)


if __name__ == '__main__':
    app.run()
