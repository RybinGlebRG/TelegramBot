import ai
import threading as th

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
            with self.lock:
                if not self.buffer.isReceiveEmpty():
                    message=self.buffer.readMessage()
                    answers=self.AI.answer(message["text"],message["chat_id"])
                    # TODO Изменить на список словарей: ответ, тип
                    self.buffer.alterChat(message["chat_id"],answers)

