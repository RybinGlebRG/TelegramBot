
class Buffer:
    chats=[]
    transmit=[]
    receive=[]

    def __init__(self):
        pass

    def addChat(self,chat_id):
        self.chats.append(Chat(chat_id))
        i=self.findChat(chat_id)
        return i

    def findChat(self,chat_id):
        i=None
        for j in range(0,len(self.chats)):
            if self.chats[j].chat_id==chat_id:
                i=j
        return i

    def receiveMessage(self, chat_id, text):
        i=self.findChat(chat_id)
        if i is None:
            i=self.addChat(chat_id)
        self.chats[i].text=text
        self.receive.append(i)

    def readMessage(self):
        i=self.receive.pop(0)
        res={"chat_id":None, "text":None}
        res["chat_id"]=self.chats[i].chat_id
        res["text"]=self.chats[i].text
        return res

    def transmitMessage(self,chat_id):
        i = self.findChat(chat_id)
        self.transmit.append(i)

    def getNextTransmit(self):
        i=self.transmit.pop(0)
        res = {"chat_id": None, "text": None}
        res["chat_id"]=self.chats[i].chat_id
        res["text"]=self.chats[i].answer
        return res

    def alterChat(self,chat_id,answer):
        i = self.findChat(chat_id)
        self.chats[i].answer=answer
        self.transmit.append(i)

    def isReceiveEmpty(self):
        if len(self.receive)>0:
            return False
        else:
            return True

    def isTransmitEmpty(self):
        if len(self.transmit)>0:
            return False
        else:
            return True

    def deleteChat(self):
        # TODO Implement this
        # Если удалить чат из списка, съедут номера в других списках
        pass


class Chat:
    chat_id=""
    text=""
    # answer/command
    type=""
    answer=None

    def __init__(self,chat_id):
        self.chat_id=chat_id
