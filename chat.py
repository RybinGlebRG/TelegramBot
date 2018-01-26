import game
import telepot.telepot as tp
import keyboards as kb
import fsm
import message as m


class Chat:
    chat_id = None
    game = None
    bot = None
    db = None
    category = None
    score_limit = None
    moves_limit = None
    menu = None
    Keyboards = None
    FSM = None
    # answers=[]
    messages = []

    def __init__(self, chat_id, bot, db, evo):
        self.chat_id = chat_id
        self.bot = bot
        self.db = db
        self.evo = evo
        self.game = game.Game(self.chat_id, self.db, self.evo)
        self.Keyboards = kb.Keyboards(self.db)
        self.FSM = fsm.FSM(self.bot.sendMessage, self.chat_id, self.game, self.bot)

    def differentiate(self,message):
        if message.subtype is None:
            self.analyzeNew(message.text)
        if message.subtype=="callback":
            self.on_callback_query(message.text)
        pass

    def analyzeNew(self, word):
        if word == "Начать новую игру":
            # TODO Stopped here
            text=self.FSM.handler(word)
            subtype="command"
            type="transmit"
        elif word == "Закончить текущую игру":
            self.FSM.handler(word)
        elif (word == "/start"):
            self.FSM.handler(word)
        elif word == "Текущий счет":
            if self.game.isRunning:
                # self.bot.sendMessage(self.chat_id, 'Счет: Я: '+str(self.game.ai_score)+", Вы: "+str(self.game.user_score))
                self.messages.append(m.Message(self.chat_id,
                                               text='Счет: Я: ' + str(self.game.ai_score) + ", Вы: " + str(
                                                   self.game.user_score)))
            else:
                # self.bot.sendMessage(self.chat_id, "Игра не начата")
                self.messages.append(m.Message(self.chat_id, text="Игра не начата"))
        elif word == "Авторы":
            self.messages.append(m.Message(self.chat_id, "Самые крутые разработчики, Люба и Глеб"))
            self.messages.append(m.Message(self.chat_id, "Продолжим?"))
            # self.bot.sendMessage(self.chat_id, "Самые крутые разработчики, Люба и Глеб")
            # self.bot.sendMessage(self.chat_id, "Продолжим?")
        else:
            if self.game.isRunning:
                if not self.game.registerQuestion(word):
                    self.messages.append(m.Message(self.chat_id, self.game.curComment))
                    # self.bot.sendMessage(self.chat_id, self.game.curComment)
                else:
                    if not self.game.checkUser():
                        self.messages.append(m.Message(self.chat_id, "Вы выиграли"))
                        self.messages.append(
                            m.Message(self.chat_id, "Счет: Я: " + str(self.game.ai_score) + ", Вы: " + str(
                                self.game.user_score)))
                        # self.bot.sendMessage(self.chat_id, "Вы выиграли")
                        # self.bot.sendMessage(self.chat_id,
                        #                     "Счет: Я: " + str(self.game.ai_score) + ", Вы: " + str(
                        #                         self.game.user_score))
                        self.game.closeGame(0)
                        return

                    if not self.game.getAnswer():
                        self.messages.append(m.Message(self.chat_id, "Не могу найти слово.. Вы выиграли"))
                        self.messages.append(
                            m.Message(self.chat_id, "Счет: Я: " + str(self.game.ai_score) + ", Вы: " + str(
                                self.game.user_score)))
                        # self.bot.sendMessage(self.chat_id, "Не могу найти слово.. Вы выиграли")
                        # self.bot.sendMessage(self.chat_id,
                        #                     "Счет: Я: " + str(self.game.ai_score) + ", Вы: " + str(
                        #                         self.game.user_score))
                        self.game.closeGame(0)
                        return
                    else:
                        answer = self.game.curAnswer
                        self.messages.append(m.Message(self.chat_id, answer.title()))
                        # self.bot.sendMessage(self.chat_id, answer.title())
                        if not self.game.checkAI():
                            self.messages.append(m.Message(self.chat_id, "Вы проиграли"))
                            self.messages.append(
                                m.Message(self.chat_id, "Счет: Я: " + str(self.game.ai_score) + ", Вы: " + str(
                                    self.game.user_score)))
                            # self.bot.sendMessage(self.chat_id, "Вы проиграли")
                            # self.bot.sendMessage(self.chat_id,
                            #                     "Счет: Я: " + str(self.game.ai_score) + ", Вы: " + str(
                            #                         self.game.user_score))
                            self.game.closeGame(1)
                            return

            else:
                self.messages.append(m.Message(self.chat_id, "Игра не начата"))
                # self.bot.sendMessage(self.chat_id, "Игра не начата")

    def start(self, category, score_limit, moves_limit):

        self.game.startGame(category, score_limit, moves_limit)
        self.messages.append(m.Message(self.chat_id, "Стоимость букв:\n" + self.game.Score.getValuedAlphabet()))
        self.messages.append(m.Message(self.chat_id, "Ваш ход"))
        # self.bot.sendMessage(self.chat_id,
        #                     "Стоимость букв:\n" + self.game.Score.getValuedAlphabet())
        # self.bot.sendMessage(self.chat_id, "Ваш ход")

    # def idleChat(self):
    #    return "Игра не начата"

    '''
    def checkUserWord(self, word):
        if self.game.curAnswer is not None:
            if word[0].upper() == self.game.curAnswer[-1].upper():
                return True
            else:
                return False
        else:
            return True
    '''

    def on_callback_query(self, query_data):
        #query_id, from_id, query_data = tp.glance(msg, flavor='callback_query')
        #print('Callback Query:', query_id, from_id, query_data)
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
