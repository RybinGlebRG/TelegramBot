import telepot.telepot as tp
import ai
import state
import botAuthorization as ba
import os
import time
import requests as rq
from telepot.telepot.loop import MessageLoop
import os
from flask import Flask, request
from telepot.telepot.loop import OrderedWebhook
import ui
import threading as th

shared={"chat":None}
lock=th.Lock()

if state.owner == 'liuba':
    TOKEN = os.environ["TOKEN"]
else:
    TOKEN = ba.getToken()

bot = tp.Bot(TOKEN)
AI = ai.AI(bot)
app = Flask(__name__)
webhook = OrderedWebhook(bot, {'chat': AI.analyzer.handle, 'callback_query': AI.analyzer.on_callback_query})
UI=ui.UI(shared,lock)

@app.route('/bot' + TOKEN, methods=['GET', 'POST'])
def pass_update():
    webhook.feed(request.data)
    return 'OK'


if not state.local:
    PORT = os.environ['PORT']
    try:
        bot.setWebhook('sinmo.herokuapp.com/bot' + TOKEN)
    # Sometimes it would raise this error, but webhook still set successfully.
    except tp.exception.TooManyRequestsError:
        pass

    webhook.run_as_thread()
    app.run(host='0.0.0.0', port=int(PORT))

else:
    UI.main()

