#import time
import telepot.telepot as tp
#from telepot.telepot.loop import MessageLoop
import os

import socket

from flask import Flask, request
from telepot.telepot.loop import OrderedWebhook

#Fake token, change to valid one
TOKEN='463574165:AAEqgwRAsHT9rv484DlCJ7BbXlVNN79LNf8'
bot = tp.Bot(TOKEN)

PORT=os.environ['PORT']
#PORT=80
print(os.environ['PORT'])
#sock=socket.socket()
#sock.bind(('',int(os.environ['PORT'])))
#sock.listen(1)



import ai
AI = ai.AI()

def on_chat_message(msg):
    content_type, chat_type, chat_id = tp.glance(msg)
    print('Chat Message:', content_type, chat_type, chat_id)

def handle(msg):
    content_type, chat_type, chat_id = tp.glance(msg)
    #print(content_type, chat_type, chat_id)
    #bot.sendMessage(chat_id,"LOL")
    if content_type == 'text':
        answer=AI.answer(msg['text'])
        #answer=msg['text']
        bot.sendMessage(chat_id, answer)

app = Flask(__name__)

webhook = OrderedWebhook(bot, {'chat': handle})

@app.route('/bot'+TOKEN, methods=[ 'GET','POST'])
def pass_update():
    #print("Data:")
    #print(request.data)
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


