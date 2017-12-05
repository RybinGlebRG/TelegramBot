import dbInteraction
import utility
import genMod as gm
import game
import inputAnalyzer as ia
#import telebot
import chat

class AI():
    bot=None
    db = None
    evo=gm.Evolution()
    analyzer = None
    chats=[]

    def __init__(self,bot):
        self.bot=bot
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
        self.chats.append(chat.Chat(int(chat_id),self.bot,self.db,self.evo))
        cur_chat = self.findChat(chat_id)
        return cur_chat

    def startGame(self,chat_id,limits):
        cur_chat=self.findChat(chat_id)
        cur_chat.start(limits[0],limits[1],limits[2])

    def answer(self, str,chat_id):
        cur_chat=self.findOrCreateChat(chat_id)
        cur_chat.analyzeNew(str)

    def __exit__(self, exception_type, exception_value, traceback):
        pass
