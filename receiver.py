import telepot.telepot as tp
from telepot.telepot.loop import OrderedWebhook
import botAuthorization as ba
import threading as th
import time
import ai
import state
import os
import time
import requests as rq
from telepot.telepot.loop import MessageLoop
import os
from flask import Flask, request
from telepot.telepot.loop import OrderedWebhook
import threading as th

class Receiver(th.Thread):
    TOKEN=None
    buffer=None
    lock=None
    webhook=None
    bot=None
    fsm=None

    def __init__(self,buffer,lock,TOKEN,bot,fsm):
        self.buffer=buffer
        self.lock=lock
        self.TOKEN=TOKEN
        self.bot=bot
        self.webhook= OrderedWebhook(self.bot, {'chat': self.chatEvent, 'callback_query': self.callbackEvent})
        self.fsm=fsm
        th.Thread.__init__(self)

    def run(self):
        while True:
            self.main()

    def chatEvent(self,msg):
        content_type, chat_type, chat_id = tp.glance(msg)
        print('Chat_id:', chat_id)
        if content_type == 'text':
            with self.lock:
                self.buffer.receiveMessage(chat_id, msg['text'])

    def callbackEvent(self):
        #TODO Implement this
        pass

    def main(self):
        if not state.local:
            app = Flask(__name__)
            @app.route('/bot' + self.TOKEN, methods=['GET', 'POST'])
            def pass_update():
                self.webhook.feed(request.data)
                return 'OK'
            PORT = os.environ['PORT']
            try:
                self.bot.setWebhook('sinmo.herokuapp.com/bot' + self.TOKEN)
            # Sometimes it would raise this error, but webhook still set successfully.
            except tp.exception.TooManyRequestsError:
                pass

            self.webhook.run_as_thread()
            app.run(host='0.0.0.0', port=int(PORT))
        else:
            response = rq.get("https://api.telegram.org/bot" + self.TOKEN + "/setWebhook")
            print(response.content)
            MessageLoop(self.bot,
                        {'chat': self.chatEvent, 'callback_query': self.callbackEvent}).run_as_thread()
            print('Listening ...')
            while (1):
                time.sleep(10)