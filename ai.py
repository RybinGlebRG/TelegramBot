import psycopg2
import dbInteraction
import string
import random
import action
import utility
import genMod as gm

class AI():
    DB = dbInteraction.DBInteraction()
    EVO=gm.Evolution()
    UC=utility.UtilityCalc(EVO)


    isGameStarted=False

    def startGame(self):
        self.isGameStarted=True
        self.DB.deleteUsedWords()

    def closeGame(self,res):
        self.isGameStarted=False
        self.EVO.setFitness(res)

    def __init__(self):
        self.DB.deleteUsedWords()

    def tupleToString(self,tup):
        used = ""
        for elem in tup:
            if elem is None:
                break
            else:
                used += "'" + elem[0] + "', "
        return used[:-2]

    def IsUsed(self,wrd):
        tup=self.DB.getUsedWords()
        for elem in tup:
            if elem[0]==wrd.upper():
                return True
        return False

    def getWordList(self,theme):
        used = self.tupleToString(self.DB.getUsedWords()).upper()
        res = self.DB.query("select" + theme[:-1] +"from" +theme+ "where upper(substr("+theme[:-1]+",1,1))='" + str[-1:].upper() + "' and upper("+theme[:-1]+") not in (" + used + ")")
        if res[0][0] is None:
            return None
        else:
            return res

    def answer(self, str):
        if (str=="/startGame"):
            #self.status=True
            self.startGame()
            return "It's your move"
        if self.isGameStarted:
            return self.gameProcess(str)
        else:
            return self.idleChat(str)

    def idleChat(self,str):
        return "Game isn't started"

    def gameProcess(self,str):
        if self.IsUsed(str):
            answer = "That word have already been used"
            return answer
        self.DB.addUsedWord(str)
        answer=self.makeDecision(str)
        if answer is None:
            answer = "Have lost"
            self.closeGame(0)
        else:
            self.DB.addUsedWord(answer)
        return answer

    def makeDecision(self,word):
        self.UC.actions.clear()
        #Possible answers
        have=self.DB.query("select distinct upper(color) from colors,used where upper(color) not in (select upper(word) from used) and substr(upper(color),1,1)='"+word[-1].upper()+"'")
        self.UC.addActions(have)
        res=self.UC.getFittest()
        return res

    def __exit__(self, exception_type, exception_value, traceback):
        pass
