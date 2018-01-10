import threading as th
import fsm


class Transmitter(th.Thread):
    buffer=None
    lock=None
    bot=None
    FSM=None

    def __init__(self,buffer,lock,bot,fsm):
        self.buffer=buffer
        self.lock=lock
        self.bot=bot
        self.FSM=fsm
        th.Thread.__init__(self)

    def run(self):
        while True:
            self.main()

    def main(self):
        while True:
            with self.lock:
                if not self.buffer.isTransmitEmpty():
                    message=self.buffer.getNextTransmit()
                    self.bot.sendMessage(message["chat_id"],message["text"])