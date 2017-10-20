import psycopg2

class AI():
    conn = psycopg2.connect(
        database="WORDS",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    def __init__(self):
        cursor=self.conn.cursor()
        cursor.execute("delete from used")
        self.conn.commit()



    def getUsedWords(self):
        used = ""
        cursor = self.conn.cursor()
        cursor.execute("select word from used")
        while (1):
            res = cursor.fetchone()
            if (res == None):
                break
            else:
                used += res[0] + ", "
        return used[:-2]


    def addUsedWord(self,wrd):
        cursor = self.conn.cursor()
        cursor.execute("insert into used(word) values('" + wrd + "')")
        self.conn.commit()

    def answer(self, str):
            answer=""

            cursor = self.conn.cursor()
            cursor.execute("select max(color) from colors where upper(substr(color,1,1))='"+str[-1:].upper()+"' and upper(color) not in ('"+ AI.getUsedWords(self).upper()+"')")
            res = cursor.fetchone()
            if (res[0]==None):
                answer="Have Losed"
            else:
                answer=res[0]
                AI.addUsedWord(self,answer)
            return answer

    def close(self):
        self.conn.close();

    def __exit__(self, exception_type, exception_value, traceback):
        self.conn.close();
