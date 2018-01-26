import ai
import threading as th
import message as m

class Logic(th.Thread):
    AI=None
    buffer=None
    lock=None

    def __init__(self,buffer,lock):
        self.buffer=buffer
        self.lock=lock
        self.AI=ai.AI()
        th.Thread.__init__(self)

    def run(self):
        while True:
            self.main()

    def main(self):
        while True:
            message=None
            messages = []
            while message is None:
                message=self.buffer.getReadMessage()
            messages = self.AI.answer(m.Message(message.chat_id,message.text,message.type,message.subtype))
            # TODO Do not differentiate types (Does it need?)
            while len(messages)>0:
                self.buffer.enqueueMessage(messages.pop())
            message=None

