import sqlite3


class AI():
    used_words=""
    def __init__(self):
        str="А"
        conn=sqlite3.connect('Words.db')
        cursor=conn.cursor()
        cursor.execute("select * from words")
        res=cursor.fetchall()
        print(res)
        conn.close()


    def answer(self, str):
        #Add Handler!!!!!!!!!!!!!!!!!!!
       try:
            conn = sqlite3.connect('Words.db')
            cursor = conn.cursor()

            print(AI.used_words)
            cursor.execute("select max(word) from words where f_char='"+str[0].upper()+"' and word not in ('"+AI.used_words+"')")
            res = cursor.fetchall()
            conn.close()
            print(res)
            if (res[0][0]==None):
                answer="Have Losed"
            else:
                answer=res[0][0]
                if (len(AI.used_words) > 0):
                    AI.used_words += "," + answer
                else:
                    AI.used_words += answer
            print (answer)
            return answer
       except sqlite3.OperationalError:
            print("Unresolved error")
            return "Ошибка"

