from Logic import game
from TelegramInterface import fsm
from ThreadSpread import message as m


######## DO I EVEN NEED THIS CLASS????????????????

class Chat:
    chat_id = None
    game = None
    bot = None
    db = None
    category = None
    score_limit = None
    moves_limit = None
    menu = None
    FSM = None
    # answers=[]
    messages = []

    def __init__(self, chat_id, bot, db, evo):
        self.chat_id = chat_id
        self.bot = bot
        self.db = db
        self.evo = evo
        self.game = game.Game(self.chat_id, self.db, self.evo)
        self.FSM = fsm.FSM(self.bot.sendMessage, self.chat_id, self.game, self.bot)

    def differentiate(self,message):
        if message.subtype is None:
            self.analyzeNew(message.text)
        if message.subtype=="callback":
            self.on_callback_query(message.text)
        if message.subtype=="command":
            self.commandExecutor(message.text)
        pass

    def analyzeNew(self, word):
        if word == "Начать новую игру":
            text=self.FSM.handler(word)
            subtype="command"
            type="transmit"
            self.messages.append(m.Message(self.chat_id,text,type,subtype))
        elif word == "Закончить текущую игру":
            # self.FSM.handler(word)
            text=self.FSM.handler(word)
            subtype="command"
            type="transmit"
            self.messages.append(m.Message(self.chat_id,text,type,subtype))
        elif (word == "/start"):
            #self.FSM.handler(word)
            text=self.FSM.handler(word)
            subtype="command"
            type="transmit"
            self.messages.append(m.Message(self.chat_id,text,type,subtype))
        elif word == "Текущий счет":
            if self.game.isRunning:
                self.messages.append(m.Message(self.chat_id,
                                               text='Счет: Я: ' + str(self.game.ai_score) + ", Вы: " + str(
                                                   self.game.user_score)))
            else:
                self.messages.append(m.Message(self.chat_id, text="Игра не начата"))
        elif word == "Авторы":
            self.messages.append(m.Message(self.chat_id, "Самые крутые разработчики, Люба и Глеб"))
            self.messages.append(m.Message(self.chat_id, "Продолжим?"))
        else:

            reply=self.game.routine(word)
            self.messages.append(m.Message(self.chat_id,reply))

    def commandExecutor(self,command):
        if command=="current_count":
            if self.game.isRunning:
                self.messages.append(m.Message(self.chat_id,
                                               text='Счет: Я: ' + str(self.game.ai_score) + ", Вы: " + str(
                                                   self.game.user_score)))
            else:
                self.messages.append(m.Message(self.chat_id, text="Игра не начата"))
        if command=="start_new_game":
            self.start(self.category,self.score_limit,self.moves_limit)


    def start(self, category, score_limit, moves_limit):

        self.game.startGame(category, score_limit, moves_limit)
        self.messages.append(m.Message(self.chat_id, "Стоимость букв:\n" + self.game.Score.getValuedAlphabet()))
        self.messages.append(m.Message(self.chat_id, "Ваш ход"))

    def on_callback_query(self, query_data):
        if self.getKey(query_data) == 'main':
            if self.getValue(query_data) == "Quick Game":
                self.category = "Star"
                self.score_limit = 500
                self.moves_limit = 15
                self.bot.editMessageText(self.FSM.menu,
                                         text="Тема: " + self.category + ", очки: " + str(
                                             self.score_limit) + ", ходы: " + str(
                                             self.moves_limit) + "\n Подождите пожалуйста, пока я не выведу таблицу счета очков",
                                         reply_markup=None)
                self.FSM.handler("Быстря игра")

                self.start(self.category, self.score_limit, self.moves_limit)
            elif self.getValue(query_data) == 'Own Game':
                self.FSM.handler("Своя игра")
        elif self.getKey(query_data) == 'category':
            self.category = self.getValue(query_data)
            self.FSM.handler("Категория")
        elif self.getKey(query_data) == 'scoreLimit':
            self.score_limit = self.getValue(query_data)
            self.FSM.handler("Очки")
        elif self.getKey(query_data) == 'movesLimit':
            self.moves_limit = self.getValue(query_data)
            self.bot.editMessageText(self.FSM.menu, text="Тема: " + self.category + ", очки: " + str(
                self.score_limit) + ", ходы: " + str(
                self.moves_limit) + "\n Пожалуйста, подождите хочу посчитать сколько очков будет за каждую букву.",
                                     reply_markup=None)
            self.FSM.handler("Ходы")
            self.start(self.category, self.score_limit, self.moves_limit)
        elif self.getKey(query_data) == "confirm":
            if self.getValue(query_data) == "Yes":
                self.FSM.handler("yes")
            else:
                self.FSM.handler("no")
        elif self.getKey(query_data) == "confirmNG":
            if self.getValue(query_data) == "Yes":

                self.FSM.handler("yes")

            else:
                self.FSM.handler("no")

    def getKey(self, query_data):
        key = query_data[:query_data.find('~')]
        return key

    def getValue(self, query_data):
        value = query_data[query_data.find('~') + 1:]
        return value
