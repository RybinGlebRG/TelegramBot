import psycopg2
import dbInteraction
import string

class AI():
    DB = dbInteraction.DBInteraction()
    alphabet=dict.fromkeys(string.ascii_uppercase,0)

    status=False
    qaunt = {}

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

    def getWordList(self,theme):
        used = self.tupleToString(self.DB.getUsedWords()).upper()
        res = self.DB.query("select" + theme[:-1] +"from" +theme+ "where upper(substr("+theme[:-1]+",1,1))='" + str[-1:].upper() + "' and upper("+theme[:-1]+") not in (" + used + ")")
        if res[0][0] is None:
            return None
        else:
            return res

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
        res=self.getWordList("colors")
        return  res[0][0]



    def calcAlphabetHave(self,word):
        #Possible answers
        have=self.DB.query("select distinct upper(color) from colors,used where color not in (select word from used) and substr(upper(color),1,1)='"+word[-1].upper()+"'")
        max=0;
        #Amounts of answers player can have, based on knonw words
        for el in have:
            res=self.DB.query("select distinct color from colors,used where upper(color) not in (select upper(word) from used) and upper(color) not in ('"+el[0].upper()+"') and substr(upper(color),1,1)='"+el[0][-1].upper()+"'")
            #print (res)
            if len(res)>max:
                max=len(res)

            self.qaunt[el[0]]=len(res)

        print(self.qaunt)
        #Normalize values
        for el in have:
            tmp=(max-self.qaunt[el[0]])/(max)
            self.qaunt[el[0]]= tmp
        print(self.qaunt)

    def __exit__(self, exception_type, exception_value, traceback):
        pass
