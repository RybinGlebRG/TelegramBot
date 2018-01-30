import threading as th

from TelegramInterface import botAuthorization as ba, receiver, transmitter
from TelegramInterface.telepot import telepot as tp


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
        t1= receiver.Receiver(self.buffer, self.TOKEN, self.bot)
        t2= transmitter.Transmitter(self.buffer, self.bot)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

