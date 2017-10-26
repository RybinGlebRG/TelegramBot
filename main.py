#import time
import telepot.telepot as tp
#from telepot.telepot.loop import MessageLoop
import os
import botAuthorization as ba
from flask import Flask, request
from telepot.telepot.loop import OrderedWebhook

#Fake token, change to valid one
TOKEN=ba.getToken()
bot = tp.Bot(TOKEN)

PORT=os.environ['PORT']
import ai
AI = ai.AI()

def handle(msg):
    content_type, chat_type, chat_id = tp.glance(msg)
    if content_type == 'text':
        answer=AI.answer(msg['text'])
        bot.sendMessage(chat_id, answer)

app = Flask(__name__)

webhook = OrderedWebhook(bot, {'chat': handle})

@app.route('/bot'+TOKEN, methods=[ 'GET','POST'])
def pass_update():
    webhook.feed(request.data)
    return 'OK'

if __name__ == '__main__':
    try:
        bot.setWebhook('sinmo.herokuapp.com/bot'+TOKEN)
    # Sometimes it would raise this error, but webhook still set successfully.
    except tp.exception.TooManyRequestsError:
        pass

    webhook.run_as_thread()
    app.run(host='0.0.0.0', port=int(PORT))


