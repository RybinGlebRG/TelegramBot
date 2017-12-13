import score
import utility
import inputAnalyzer as ia
import telepot.telepot as tp


class Game:

    curQuestion=None
    curAnswer=None
    curComment=None
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
        num = self.db.getNumberOfCurrCatwords(category)
        db_num = self.db.countAllBase()
        if db_num > 8000:
            self.db.deleteLargestCat()
        if num < 300:
            self.db.updateCategoryWordsBase(category)
        self.db.showTabstrings()
        self.curQuestion=None
        self.curAnswer=None

    # TODO Implement this
    def fillDB(self,category):
        pass

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

    def gameProcessNew(self,word):
        if not self.registerQuestion(word):
            return False
        self.user_score = self.recalcScore(self.user_score, self.curQuestion)
        if not self.checkNew():
            return False
        if not self.getAnswer():
            return False
        self.ai_score = self.recalcScore(self.ai_score, self.curAnswer)
        if not self.checkNew():
            return False
        return True

    def determineWinner(self):
        if self.user_score > self.ai_score:
            return False
        else:
            return True

    def registerQuestion(self,word):
        self.curComment=None
        if self.curAnswer is not None:
            if word[0].upper()!=self.curAnswer[-1].upper():
                self.curComment="Некорректное слово"
                return False
        self.curAnswer=None
        if self.IsUsed(word):
            self.curComment="Это слово уже использовалось"
            return False
        self.curQuestion=word
        self.db.addUsedWord(self.curQuestion, self.chat_id)
        return True

    def getAnswer(self):
        answer = self.makeDecision()
        self.curQuestion = None

        if answer is None:
            return False
        else:
            self.db.addUsedWord(answer, self.chat_id)
            self.curAnswer = answer
            return True

    def checkAI(self):
        self.ai_score = self.recalcScore(self.ai_score, self.curAnswer)
        if self.Score.isOver(self.ai_score, self.user_score, self.moves):
            return False
        return True

    def checkUser(self):
        self.user_score = self.recalcScore(self.user_score, self.curQuestion)
        if self.Score.isOver(self.ai_score, self.user_score, self.moves):
            return False
        return True

    def checkNew(self):
        if self.Score.isOver(self.ai_score, self.user_score, self.moves):
            return False
        return True

    def makeDecision(self):
        self.uc.actions.clear()
        self.uc.addActions(self.chat_id, self.curQuestion,self.category)
        res=self.uc.getFittest()
        return res

    def recalcScore(self,who,word):
        sum=0
        for letter in word:
            sum+=self.Score.alphabet[letter.lower()]
        sum+=who
        return sum


