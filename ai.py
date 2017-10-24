import psycopg2
import dbInteraction

class AI():
    DB = dbInteraction.DBInteraction()

    status=False

    def IsGameStarted(self):
        return self.status

    def startGame(self):
        self.status=True
        self.DB.deleteUsedWords()

    def closeGame(self):
        self.status=False

    def __init__(self):
        self.DB.deleteUsedWords()

    def tupleToString(self,tup):
        used = ""
        #print(tup)
        for elem in tup:
            if elem is None:
                break
            else:
                used += "'" + elem[0] + "', "
        return used[:-2]

    def IsUsed(self,wrd):
        tup=self.DB.getUsedWords()
        for elem in tup:
            if elem[0]==wrd:
                return True
        return False

    def answer(self, str):
        if (str=="/startGame"):
            self.status=True
            return "It's your move"
        if self.IsGameStarted():
            return self.gameProcess(str)
        else:
            return self.idleChat(str)

    def idleChat(self,str):
        return "Game isn't started"

    def gameProcess(self,str):
        answer = ""

        if self.IsUsed(str):
            answer = "That word have already been used"
            return answer
        self.DB.addUsedWord(str)
        answer=self.makeDecision(str)
        if answer is None:
            answer = "Have lost"
            self.closeGame()
        else:
            self.DB.addUsedWord(answer)
        return answer

    def makeDecision(self,str):
        used = self.tupleToString(self.DB.getUsedWords()).upper()
        res=self.DB.query("select max(color) from colors where upper(substr(color,1,1))='" + str[-1:].upper() + "' and upper(color) not in (" + used + ")")
        if res[0][0] is None:
            return None
        else:
            return res[0][0]

    def __exit__(self, exception_type, exception_value, traceback):
        pass
