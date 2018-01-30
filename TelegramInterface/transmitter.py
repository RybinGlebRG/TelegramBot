import threading as th


class Transmitter(th.Thread):
    buffer=None
    lock=None
    bot=None
    FSM=None

    def __init__(self,buffer,bot,lock=None,fsm=None):
        self.buffer=buffer
        #self.lock=lock
        self.bot=bot
        #self.FSM=fsm
        th.Thread.__init__(self)

    def run(self):
        while True:
            self.main()

    def formAnswer(self,message):
        pass

    def main(self):
        while True:
            message=None
            while message is None:
                message=self.buffer.getTransmitMessage()
            while len(message.text)>0:
                if message.subtype is not "command":
                    self.bot.sendMessage(message.chat_id,message.text.pop() )
                else:
                    self.formAnswer(message)
            message=None

