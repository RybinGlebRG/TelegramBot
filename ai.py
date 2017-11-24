import dbInteraction
import utility
import genMod as gm
import game
import inputAnalyzer as ia
#import telebot

class AI():
    db = dbInteraction.DBInteraction()
    evo=gm.Evolution()
    #uc=utility.UtilityCalc(evo)
    analyzer = ia.InputAnalyzer()
    games=[]

    def __init__(self):
        self.db.deleteUsedWords()

    def findOrCreateGame(self,chat_id):
        cur_game=None
        for i in range(0,len(self.games)):
            if self.games[i].chat_id==chat_id:
                cur_game=self.games[i]
        if cur_game is None:
            cur_game=self.createGame(chat_id)
        return cur_game

    def createGame(self,chat_id):
        # TODO Get limits from user
        score_limit=0
        moves_limit=0
        category="colors"
        self.games.append(game.Game(chat_id,score_limit,moves_limit,self.db,self.evo,category))
        cur_game = self.games[-1]
        return cur_game

    def checkGame(self,game):
        if not game.isRunning:
            self.games.remove(game)

    def play(self,game,word):
        res=game.gameProcess(word)
        self.checkGame(game)
        return res

    def answer(self, str,chat_id,sendMessage):
        cur_game=self.findOrCreateGame(chat_id)
        self.analyzer.analyze(str,cur_game,self.play,sendMessage)


    def __exit__(self, exception_type, exception_value, traceback):
        pass
