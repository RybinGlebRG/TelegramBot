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



class UI:
    TOKEN=None
    bot=None
    webhook=None
    shared=None
    lock=None

    def __init__(self,shared,lock):
        self.TOKEN = ba.getToken()
        self.bot=tp.Bot(self.TOKEN)
        #self.webhook = OrderedWebhook(self.bot, {'chat': self.chatEvent, 'callback_query': self.callbackEvent})
        self.shared=shared
        self.lock=lock



    def chatEvent(self,msg):
        content_type, chat_type, chat_id = tp.glance(msg)
        print('Chat_id:', chat_id)
        if content_type == 'text':
            while True:
                if self.shared.get("chat") is None or self.shared["chat"].get("id") is None or self.shared["chat"].get("text") is None:
                    with self.lock:
                        if self.shared.get("chat") is None or self.shared["chat"].get("id") is None or self.shared["chat"].get("text") is None:
                            self.shared["chat"]["id"]=chat_id
                            self.shared["chat"]["text"]=msg['text']
                            break

    def callbackEvent(self):
        #TODO Implement this
        pass

    def main(self):
        response = rq.get("https://api.telegram.org/bot" + self.TOKEN + "/setWebhook")
        print(response.content)
        MessageLoop(self.bot,
                    {'chat': self.chatEvent, 'callback_query': self.callbackEvent}).run_as_thread()
        print('Listening ...')
        while (1):
            time.sleep(10)
