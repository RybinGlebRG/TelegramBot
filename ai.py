import psycopg2

class AI():
    conn = psycopg2.connect(
        database="WORDS",
        #Change to something more secure
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    status=False

    def IsGameStarted(self):
        return  self.status

    def startGame(self):
        self.status=True
        self.deleteUsedWords()

    def closeGame(self):
        self.status=False

    def __init__(self):
        self.deleteUsedWords()

    def deleteUsedWords(self):
        with self.conn.cursor() as cursor:
            cursor.execute("delete from used")
            self.conn.commit()

    def getUsedWords(self):
        with self.conn.cursor() as cursor:
            cursor.execute("select word from used")
            res=cursor.fetchall()
            return res

    def tupleToString(self,tup):
        used = ""
        print(tup)
        for elem in tup:
            if (elem == None):
                break
            else:
                used +="'"+ elem[0] + "', "
        return used[:-2]

    def IsUsed(self,wrd):
        tup=self.getUsedWords()
        for elem in tup:
            if elem[0]==wrd:
                return True
        return False


    def addUsedWord(self,wrd):
        with self.conn.cursor() as cursor:
            cursor.execute("insert into used(word) values('" + wrd + "')")
            self.conn.commit()

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
        res = []
        self.addUsedWord(str)
        cursor = self.conn.cursor()
        used = self.tupleToString(self.getUsedWords()).upper()
        with self.conn.cursor() as cursor:
            cursor.execute("select max(color) from colors where upper(substr(color,1,1))='" + str[-1:].upper() + "' and upper(color) not in (" + used + ")")
            res = cursor.fetchone()
        if (res[0] == None):
            answer = "Have Losed"
            self.closeGame()
        else:
            answer = res[0]
            self.addUsedWord(answer)
        return answer

    def close(self):
        self.conn.close();

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()
