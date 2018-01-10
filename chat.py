import game
import telepot.telepot as tp
import keyboards as kb
import fsm

class Chat:
    chat_id = None
    game = None
    db=None
    category=None
    score_limit=None
    moves_limit=None
    menu=None
    answers=[]

    def __init__(self,chat_id,db,evo):
        self.chat_id=chat_id
        self.db=db
        self.evo=evo
        self.game=game.Game(self.chat_id,self.db,self.evo)

    def analyzeNew(self,word):
        if word=="Начать новую игру":
            # TODO Implement this
            pass
        elif word == "Закончить текущую игру":
            # TODO Implement this
            pass
        elif word == "Текущий счет":
            self.answers.append('Счет: Я: '+str(self.game.ai_score)+", Вы: "+str(self.game.user_score))
        else:
            if not self.game.registerQuestion(word):
                self.answers.append(self.game.curComment)
            else:
                if not self.game.checkUser():
                    self.answers.append( "Вы выиграли")
                    self.answers.append("Счет: Я: " + str(self.game.ai_score) + ", Вы: " + str(
                                             self.game.user_score))
                    self.game.closeGame(0)
                    return

                if not self.game.getAnswer():
                    self.answers.append("Не могу найти слово.. Вы выиграли")
                    self.answers.append("Счет: Я: " + str(self.game.ai_score) + ", Вы: " + str(
                                             self.game.user_score))
                    self.game.closeGame(0)
                    return
                else:
                    answer = self.game.curAnswer
                    self.answers.append(answer.title())
                    if not self.game.checkAI():
                        self.answers.append( "Вы проиграли")
                        self.answers.append("Счет: Я: " + str(self.game.ai_score) + ", Вы: " + str(
                                                 self.game.user_score))
                        self.game.closeGame(1)
                        return


