from Obsolete import inputAnalyzer as ia
#import telebot
from Logic import chat, dbInteraction, genMod as gm
# import telebot
from Logic import chat, dbInteraction, genMod as gm
from Obsolete import inputAnalyzer as ia


class AI():
    db = None
    evo=gm.Evolution()
    analyzer = None
    chats=[]

    def __init__(self):
        self.db = dbInteraction.DBInteraction()
        self.db.deleteAllUsedWords()
        self.analyzer = ia.InputAnalyzer(self.answer,self.chats)


    def findOrCreateChat(self,chat_id):
        cur_chat=None
        cur_chat=self.findChat(chat_id)
        if cur_chat is None:
            cur_chat=self.createChat(chat_id)
        return cur_chat


    def findChat(self,chat_id):
        cur_chat = None
        for i in range(0,len(self.chats)):
            if self.chats[i].chat_id==chat_id:
                cur_chat=self.chats[i]
        return cur_chat

    def createChat(self,chat_id):
        self.chats.append(chat.Chat(int(chat_id), self.db, self.evo))
        cur_chat = self.findChat(chat_id)
        return cur_chat

    def startGame(self,chat_id,limits):
        cur_chat=self.findChat(chat_id)
        cur_chat.start(limits[0],limits[1],limits[2])

    def answer(self, message):
        cur_chat=self.findOrCreateChat(message.chat_id)
        cur_chat.differentiate(message)
        return cur_chat.messages

    def __exit__(self, exception_type, exception_value, traceback):
        pass
