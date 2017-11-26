import score
import utility
import inputAnalyzer as ia
import telepot.telepot as tp


class Game:

    curQuestion=None
    isRunning=False
    ai_score=0
    user_score=0
    moves=0
    chat_id = None
    Score=None
    db=None
    evo=None
    uc=None
    category=None


    def __init__(self,chat_id,db,evo):
        self.chat_id=str(chat_id)
        self.db=db
        self.evo=evo
        self.uc = utility.UtilityCalc(evo)

    def startGame(self,category,score_limit,moves_limit):
        self.category = category
        self.Score = score.Score(score_limit, moves_limit)
        self.isRunning = True
        self.moves=0
        self.user_score=0
        self.ai_score=0
        self.db.deleteUsedWords(self.chat_id)

    def closeGame(self,res):
        self.isRunning=False
        self.evo.setFitness(res)

    def checkStatus(self):
        if self.Score.isOver(self.ai_score,self.user_score,self.moves):
            if self.user_score>self.ai_score:
                self.closeGame(0)
            else:
                self.closeGame(1)
            return True
        else:
            return False

    def IsUsed(self,wrd):
        tup=self.db.getUsedWords(self.chat_id)
        for elem in tup:
            if elem[0]==wrd.upper():
                return True
        return False

    def gameProcess(self):
        if self.IsUsed(self.curQuestion):
            answer = "That word have already been used"
            return answer
        self.db.addUsedWord(self.curQuestion, self.chat_id)
        if self.checkStatus():
            answer=None
        else:
            answer=self.makeDecision()
        self.curQuestion=None
        if answer is None:
            answer = "Have lost"
            self.closeGame(0)
        else:
            self.db.addUsedWord(answer, self.chat_id)
        self.checkStatus()
        return answer

    def makeDecision(self):
        self.uc.actions.clear()
        self.uc.addActions(self.chat_id, self.curQuestion,self.category)
        res=self.uc.getFittest()
        return res

