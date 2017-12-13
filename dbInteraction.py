import psycopg2
import urllib.parse as urlparse
import os
import state
import internetInteraction
from os import environ

class DBInteraction():

	cur_env=None
	url = None
	dbname = None
	user = None
	password = None
	host = None
	port = None

	conn = None

	def __init__(self):
		self.cur_env=self.getDatabaseURL()
		self.url = urlparse.urlparse(self.cur_env)
		self.dbname = self.url.path[1:]
		self.user = self.url.username
		self.password = self.url.password
		self.host = self.url.hostname
		self.port = self.url.port
		print(self.port)
		self.conn = psycopg2.connect(
			database=self.dbname,
			user=self.user,
			password=self.password,
			host=self.host,
			port=self.port
		)

	def getDatabaseURL(self):
		if state.local == False:
			cur_env = os.environ['DATABASE_URL']

		elif state.owner == 'liuba':
			cur_env = state.liubas_db
		else:
			cur_env = "postgres://postgres:postgres@127.0.0.1:5432/WRDS"

		return  cur_env


	def checkConnection(self):
		if self.conn.closed!=0:
			self.cur_env=self.getDatabaseURL()
			self.url = urlparse.urlparse(self.cur_env)
			self.dbname = self.url.path[1:]
			self.user = self.url.username
			self.password = self.url.password
			self.host = self.url.hostname
			self.port = self.url.port
			self.conn=psycopg2.connect(
				database=self.dbname,
				user=self.user,
				password=self.password,
				host=self.host,
				port=self.port
			)


	def deleteUsedWords(self,chat_id):
		self.checkConnection()
		with self.conn.cursor() as cursor:
			cursor.execute("delete from used where chat_id='"+chat_id+"'")
			self.conn.commit()

	def getNumberOfCurrCatwords(self, category):
		self.checkConnection()
		with self.conn.cursor() as cursor:
			s = "select count(*) from words where category='" + category +"';"
			res = 0
			try:
				cursor.execute(s)

				res = cursor.fetchall()
			except Exception as e:
				print(e)

			return res



	def updateCategoryWordsBase(self,category):
		words = []
		words = internetInteraction.getWords(100, category)
		s = ""
		self.checkConnection()
		with self.conn.cursor() as cursor:
			for i in range(len(words)):
				s = "insert into words(word,category) values('"
				s += words[i] + "', '" + category + "');"
				try:
					cursor.execute(s)
				except Exception as e:
					print(e)
			self.conn.commit()
		pass

	def showTabstrings(self):
		self.checkConnection()
		with self.conn.cursor() as cursor:
			cursor.execute("select word, category from words")
			res = cursor.fetchall()
		for i in res:
			print(i)


	def deleteAllUsedWords(self):
		self.checkConnection()
		with self.conn.cursor() as cursor:
			cursor.execute("delete from used ")
			self.conn.commit()


	def getUsedWords(self,chat_id):
		self.checkConnection()
		with self.conn.cursor() as cursor:
			cursor.execute("select upper(word) from used where chat_id='"+chat_id+"'")
			res=cursor.fetchall()
			return res

	def addUsedWord(self,wrd,chat_id):
		self.checkConnection()
		with self.conn.cursor() as cursor:
			cursor.execute("insert into used(word,chat_id) values('" + wrd + "', '"+chat_id+"')")
			self.conn.commit()

	def DML(self,str):
		self.checkConnection()
		with self.conn.cursor() as cursor:
			for el in str:
				cursor.execute(el)
			self.conn.commit()

	def query(self,str):
		self.checkConnection()
		with self.conn.cursor() as cursor:
			cursor.execute(str)
			res=cursor.fetchall()
			return res

	def getPossibleAnswers(self,chat_id,word,category):
		have = self.query(
			"select distinct upper(word) from words where upper(category)='"+category.upper()+"' and upper(word) not in (select upper(word) from used where chat_id='" + chat_id + "') and substr(upper(word),1,1)='" +
			word.upper() + "'")
		return have

	def getPossiblePlayerAnswers(self,chat_id,el,category):
		res = self.query(
			"select distinct upper(word) from words where upper(category)='"+category.upper()+"' and upper(word) not in (select upper(word) from used where chat_id='" + chat_id + "') and upper(word) not in ('" +
			el[0].upper() + "') and substr(upper(word),1,1)='" + el[0][-1].upper() + "'")
		return  res
	def getCategories(self):
		res=self.query("select distinct category from words")
		return res

	def __exit__(self, exception_type, exception_value, traceback):
		self.conn.close()
