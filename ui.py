import telepot.telepot as tp
from telepot.telepot.loop import OrderedWebhook
import botAuthorization as ba
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
import transmitter
import receiver
import threading as th
import fsm



class UI(th.Thread):
    TOKEN=None
    bot=None
    webhook=None
    buffer=None
    lock=None
    fsm=None

    def __init__(self,shared,lock):
        self.TOKEN = ba.getToken()
        self.bot=tp.Bot(self.TOKEN)
        self.buffer=shared
        self.lock=lock
        #self.fsm=fsm.FSM()
        th.Thread.__init__(self)

    def run(self):
        while True:
            self.main()

    def main(self):
        t1=receiver.Receiver(self.buffer,self.TOKEN,self.bot)
        t2=transmitter.Transmitter(self.buffer,self.bot)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

