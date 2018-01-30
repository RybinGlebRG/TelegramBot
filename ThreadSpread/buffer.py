import threading as th

from ThreadSpread import message as m


class Buffer:
    messages=[]
    lock=th.Lock()

    def __init__(self):
        pass



    def enqueueMessage(self,message):
        with self.lock:

            self.messages.append(m.Message(message.chat_id,message.text,message.type,message.subtype))


    def getReadMessage(self):
        with self.lock:
            if len(self.messages)>0:
                if self.messages[0].type=="read":
                    message=self.messages.pop(0)
                    return m.Message(message.chat_id,message.text,message.type,message.subtype)
            return None


    def getTransmitMessage(self):
        with self.lock:
            if len(self.messages) > 0:
                if self.messages[0].type=="transmit":
                    message=self.messages.pop(0)
                    return m.Message(message.chat_id,message.text,message.type,message.subtype)
            return None
