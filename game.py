import score
import utility

class Game:

    isRunning=False
    ai_score=0
    user_score=0
    moves=0
    chat_id = ""
    Score=None
    db=None
    evo=None
    uc=utility.UtilityCalc(evo)

    def __init__(self,chat_id,score_limit,moves_limit,db,evo):
        self.chat_id=str(chat_id)
        self.Score=score.Score(score_limit,moves_limit)
        self.db=db
        self.evo=evo

    def startGame(self):
        self.isRunning = True
        self.db.deleteUsedWords()

    def closeGame(self,res):
        self.isRunning=False
        self.evo.setFitness(res)

    def checkStatus(self):
        if self.Score.isOver(self.ai_score,self.user_score,self.moves):
            # TODO implement this
            pass

    def IsUsed(self,wrd,chat_id):
        tup=self.db.getUsedWords(chat_id)
        for elem in tup:
            if elem[0]==wrd.upper():
                return True
        return False

    def gameProcess(self, word):
        # TODO How to win?
        if self.IsUsed(word, self.chat_id):
            answer = "That word have already been used"
            return answer
        self.db.addUsedWord(word, self.chat_id)
        answer=self.makeDecision(word, self.chat_id)
        if answer is None:
            answer = "Have lost"
            self.closeGame(0)
        else:
            self.db.addUsedWord(answer, self.chat_id)
        return answer

    def makeDecision(self,word,chat_id):
        self.uc.actions.clear()
        self.uc.addActions(chat_id, word)
        res=self.uc.getFittest()
        return res