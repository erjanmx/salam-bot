import json
from src.bot import Bot
from config.app import *
from flask import Flask, request, abort, jsonify

app = Flask(__name__)


@app.route('/', methods=['POST'])
def entry():
    try:
        if request.args.get('_token') != SALAM_BOT_TOKEN:
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
        if DEBUG:
            print(e)
        abort(404)


if __name__ == '__main__':
    app.run()
