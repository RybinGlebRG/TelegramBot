import game
import telepot.telepot as tp
import keyboards as kb
import fsm

class Chat:
    chat_id = None
    game = None
    bot=None
    db=None
    category=None
    score_limit=None
    moves_limit=None
    menu=None
    Keyboards=None
    FSM=None

    def __init__(self,chat_id,bot,db,evo):
        self.chat_id=chat_id
        self.bot=bot
        self.db=db
        self.evo=evo
        self.game=game.Game(self.chat_id,self.db,self.evo)
        self.Keyboards=kb.Keyboards(self.db)
        self.FSM=fsm.FSM(self.bot.sendMessage,self.chat_id,self.game,self.bot)

    def analyzeNew(self,word):
        if word=="Начать новую игру":
            self.FSM.handler(word)
        elif word == "Закончить текущую игру":
            self.FSM.handler(word)
        elif (word=="/start"):
            self.FSM.handler(word)
        elif word == "Текущий счет":
            if self.game.isRunning:
                self.bot.sendMessage(self.chat_id, 'Счет: Я: '+str(self.game.ai_score)+", Вы: "+str(self.game.user_score))
            else:
                self.bot.sendMessage(self.chat_id, "Игра не начата")
        else:
            if self.game.isRunning:
                try:
                    if not self.game.registerQuestion(word):
                        self.bot.sendMessage(self.chat_id, self.game.curComment)
                    else:
                        if not self.game.checkUser():
                            self.bot.sendMessage(self.chat_id, "Вы выиграли")
                            self.bot.sendMessage(self.chat_id,
                                                 "Счет: Я: " + str(self.game.ai_score) + ", Вы: " + str(
                                                     self.game.user_score))
                            self.game.closeGame(0)
                            return

                        if not self.game.getAnswer():
                            self.bot.sendMessage(self.chat_id, "Не могу найти слово.. Вы выиграли")
                            self.bot.sendMessage(self.chat_id,
                                                 "Счет: Я: " + str(self.game.ai_score) + ", Вы: " + str(
                                                     self.game.user_score))
                            self.game.closeGame(0)
                            return
                        else:
                            answer = self.game.curAnswer
                            self.bot.sendMessage(self.chat_id, answer.title())
                            if not self.game.checkAI():
                                self.bot.sendMessage(self.chat_id, "Вы проиграли")
                                self.bot.sendMessage(self.chat_id,
                                                     "Счет: Я: " + str(self.game.ai_score) + ", Вы: " + str(
                                                         self.game.user_score))
                                self.game.closeGame(1)
                                return
                except KeyError:
                    self.bot.sendMessage(self.chat_id, "Встретился некорректный символ")

            else:
                self.bot.sendMessage(self.chat_id, "Игра не начата")

    def start(self,category,score_limit,moves_limit):

        self.game.startGame(category, score_limit, moves_limit)
        self.bot.sendMessage(self.chat_id, "Стоимость букв:\n"+str(self.game.Score.alphabet).replace("'","").strip("{}"))
        self.bot.sendMessage(self.chat_id, "Ваш ход")

    def idleChat(self):
        return "Игра не начата"

    def checkUserWord(self,word):
        if self.game.curAnswer is not None:
            if word[0].upper()==self.game.curAnswer[-1].upper():
                return True
            else:
                return False
        else:
            return True

    def on_callback_query(self, msg):
        query_id, from_id, query_data = tp.glance(msg, flavor='callback_query')
        print('Callback Query:', query_id, from_id, query_data)
        if query_data[:query_data.find('~')] == 'main':
            if query_data[query_data.find('~') + 1:]=="Quick Game":
                self.category="Города"
                self.score_limit=2000
                self.moves_limit=15
                self.bot.editMessageText(self.FSM.menu,
                                         text="Тема: " + self.category + ", очки: " + str(self.score_limit) + ", ходы: " + str(self.moves_limit) + "\n Подождите пожалуйста, пока я не выведу таблицу счета очков",
                                         reply_markup=None)
                self.FSM.handler("Быстря игра")

                self.start(self.category, self.score_limit, self.moves_limit)
            elif query_data[query_data.find('~') + 1:] == 'Own Game':
                self.FSM.handler("Своя игра")
        elif query_data[:query_data.find('~')] == 'category':
            self.category = query_data[query_data.find('~') + 1:]
            self.FSM.handler("Категория")
        elif query_data[:query_data.find('~')] == 'scoreLimit':
            self.score_limit = query_data[query_data.find('~') + 1:]
            self.FSM.handler("Очки")
        elif query_data[:query_data.find('~')] == 'movesLimit':
            self.moves_limit = query_data[query_data.find('~') + 1:]
            self.bot.editMessageText(self.FSM.menu, text="Тема: "+self.category+", очки: "+str(self.score_limit)+", ходы: "+str(self.moves_limit) + "\n Пожалуйста, подождите хочу посчитать сколько очков будет за каждую букву.", reply_markup=None)
            self.FSM.handler("Ходы")
            self.start(self.category, self.score_limit, self.moves_limit)
        elif query_data[:query_data.find('~')]=="confirm":
            if query_data[query_data.find('~') + 1:]=="Yes":
                self.game.closeGame(0)
                self.FSM.handler("yes")
            else:
                self.FSM.handler("no")
        elif query_data[:query_data.find('~')]=="confirmNG":
            if query_data[query_data.find('~') + 1:]=="Yes":
                self.game.closeGame(0)
                self.FSM.handler("yes")

            else:
                self.FSM.handler("no")


