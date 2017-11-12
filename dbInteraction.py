import psycopg2
import urllib.parse as urlparse
import os
#tmp="postgres://dwwonxduejlzym:c179f509be3eca5de4a54fdb2bd6679b5f78d7c5fdc7a96ea2ce655c0494e6a0@ec2-50-19-89-124.compute-1.amazonaws.com:5432/d5ivqg5m5qbeir"
class DBInteraction():
    cur_env = os.environ['DATABASE_URL']
    #cur_env=tmp
    url = urlparse.urlparse(cur_env)
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    '''
    conn = psycopg2.connect(
        database="WORDS",
        #Change to something more secure
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    '''
    conn = psycopg2.connect(
        database=dbname,
        #Change to something more secure
        user=user,
        password=password,
        host=host,
        port=port
    )

    def checkConnection(self):
        if self.conn.closed!=0:
            self.cur_env=os.environ['DATABASE_URL']
            #self.cur_env=tmp;
            self.url = urlparse.urlparse(self.cur_env)
            self.dbname = self.url.path[1:]
            self.user = self.url.username
            self.password = self.url.password
            self.host = self.url.hostname
            self.port = self.url.port
            self.conn=psycopg2.connect(
                database=self.dbname,
                # Change to something more secure
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )

    def deleteUsedWords(self):
        self.checkConnection();
        with self.conn.cursor() as cursor:
            cursor.execute("delete from used")
            self.conn.commit()

    def getUsedWords(self):
        self.checkConnection();
        with self.conn.cursor() as cursor:
            cursor.execute("select word from used")
            res=cursor.fetchall()
            return res

    def addUsedWord(self,wrd):
        self.checkConnection();
        with self.conn.cursor() as cursor:
            cursor.execute("insert into used(word) values('" + wrd + "')")
            self.conn.commit()

    def query(self,str):
        self.checkConnection();
        with self.conn.cursor() as cursor:
            cursor.execute(str)
            res=cursor.fetchall()
            return res

    def __exit__(self, exception_type, exception_value, traceback):
        self.conn.close();
