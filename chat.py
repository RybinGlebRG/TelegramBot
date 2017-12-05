import game
import telepot.telepot as tp
import keyboards as kb

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

    def __init__(self,chat_id,bot,db,evo):
        self.chat_id=chat_id
        self.bot=bot
        self.db=db
        self.evo=evo
        self.game=game.Game(self.chat_id,self.db,self.evo)
        self.Keyboards=kb.Keyboards(self.db)

    def analyze(self,word):
        if word=="Начать новую игру":
            self.startNewGame()
        elif word == "Закончить текущую игру":
            self.finishCurrentGame()
        elif (word=="/start"):
            self.bot.sendMessage(self.chat_id, 'Сыграем?', reply_markup=kb.kbNG)
        elif word == "Текущий счет":
            if self.game.isRunning:
                self.bot.sendMessage(self.chat_id, 'Счет: Я: '+str(self.game.ai_score)+", Вы: "+str(self.game.user_score))
            else:
                self.bot.sendMessage(self.chat_id, "Игра не начата")
        else:
            if self.game.isRunning:
                if self.checkUserWord(word):
                    self.game.curQuestion=word
                    answer=self.game.gameProcess()
                    # TODO Change
                    if self.game.checkStatus():
                        answer+=". Game is over."
                    self.bot.sendMessage(self.chat_id, answer.title())
                else:
                    self.bot.sendMessage(self.chat_id, "Это слово неправильное")
            else:
                self.bot.sendMessage(self.chat_id, self.idleChat())

    def analyzeNew(self,word):
        if word=="Начать новую игру":
            self.startNewGame()
        elif word == "Закончить текущую игру":
            self.finishCurrentGame()
            self.menu=None
        elif (word=="/start"):
            self.bot.sendMessage(self.chat_id, 'Сыграем?', reply_markup=kb.kbNG)
        elif word == "Текущий счет":
            if self.game.isRunning:
                self.bot.sendMessage(self.chat_id, 'Счет: Я: '+str(self.game.ai_score)+", Вы: "+str(self.game.user_score))
            else:
                self.bot.sendMessage(self.chat_id, "Игра не начата")
            self.menu = None
        else:
            if self.game.isRunning:
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
                        self.bot.sendMessage(self.chat_id, "Вы выиграли")
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
                '''
                if self.game.gameProcessNew(word):
                    answer=self.game.curAnswer
                    self.bot.sendMessage(self.chat_id, answer.title())
                    return
                else:
                    if self.game.curComment is None:
                        self.announceWinner()
                        return
                    else:
                        self.bot.sendMessage(self.chat_id,self.game.curComment)
                        return
                '''
            else:
                self.bot.sendMessage(self.chat_id, "Игра не начата")

    '''
    def announceWinner(self):
        winner = self.game.determineWinner()
        if winner:
            self.bot.sendMessage(self.chat_id, "Вы проиграли")
            self.bot.sendMessage(self.chat_id,
                                 "Счет: Я: " + str(self.game.ai_score) + ", Вы: " + str(self.game.user_score))
            self.game.closeGame(1)
            return
        else:
            self.bot.sendMessage(self.chat_id, "Вы выиграли")
            self.bot.sendMessage(self.chat_id,
                                 "Счет: Я: " + str(self.game.ai_score) + ", Вы: " + str(self.game.user_score))
            self.game.closeGame(0)
            return
    '''
    def start(self,category,score_limit,moves_limit):
        self.game.startGame(category, score_limit, moves_limit)
        self.bot.sendMessage(self.chat_id, "Ваш ход")

    def startNewGame(self):
        if self.game.isRunning:
            msg = self.bot.sendMessage(self.chat_id, "Вы уверены?", reply_markup=kb.kbConfirmNG)
            self.menu = tp.message_identifier(msg)
        else:
            self.getLimits()

    def finishCurrentGame(self):
        if self.game.isRunning:
            msg = self.bot.sendMessage(self.chat_id, "Вы уверены?", reply_markup=kb.kbConfirm)
            self.menu = tp.message_identifier(msg)
        else:
            self.bot.sendMessage(self.chat_id, "Игра не начата")

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


    def getLimits(self):
        if self.menu is None:
            msg=self.bot.sendMessage(self.chat_id, "Ну и как поступим?", reply_markup=kb.kbMain)
            self.menu = tp.message_identifier(msg)
        else:
            self.bot.editMessageText(self.menu, text="Ну и как поступим?", reply_markup=kb.kbMain)



    def on_callback_query(self, msg):
        query_id, from_id, query_data = tp.glance(msg, flavor='callback_query')
        print('Callback Query:', query_id, from_id, query_data)
        if query_data[:query_data.find('~')] == 'main':
            if query_data[query_data.find('~') + 1:]=="Quick Game":
                self.category="Colors"
                self.score_limit=10
                self.moves_limit=5
                self.bot.editMessageText(self.menu,
                                         text="Тема: " + self.category + ", очки: " + str(self.score_limit) + ", ходы: " + str(self.moves_limit),
                                         reply_markup=None)
                self.menu=None
                self.start(self.category, self.score_limit, self.moves_limit)
            elif query_data[query_data.find('~') + 1:] == 'Own Game':
                self.bot.editMessageText(self.menu, text="Выберите тему", reply_markup=self.Keyboards.getKeyboard("kbCategories"))
        elif query_data[:query_data.find('~')] == 'category':
            self.category = query_data[query_data.find('~') + 1:]
            self.bot.editMessageText(self.menu, text="Выберите количество очков", reply_markup=kb.kbScores)
        elif query_data[:query_data.find('~')] == 'scoreLimit':
            self.score_limit = query_data[query_data.find('~') + 1:]

            self.bot.editMessageText(self.menu, text="Выберите количество ходов", reply_markup=kb.kbMoves)
        elif query_data[:query_data.find('~')] == 'movesLimit':
            self.moves_limit = query_data[query_data.find('~') + 1:]
            self.bot.editMessageText(self.menu, text="Тема: "+self.category+", очки: "+str(self.score_limit)+", ходы: "+str(self.moves_limit), reply_markup=None)
            self.menu=None
            self.start(self.category, self.score_limit, self.moves_limit)
        elif query_data[:query_data.find('~')]=="confirm":
            if query_data[query_data.find('~') + 1:]=="Yes":
                self.game.closeGame(0)
                self.bot.editMessageText(self.menu,"Игра завершена", reply_markup=None)
                self.menu=None
            else:
                self.bot.editMessageText(self.menu,"Тогда продолжаем", reply_markup=None)
                self.menu=None
        elif query_data[:query_data.find('~')]=="confirmNG":
            if query_data[query_data.find('~') + 1:]=="Yes":
                self.game.closeGame(0)
                self.bot.editMessageText(self.menu,"Игра завершена", reply_markup=None)
                self.menu=None
                self.getLimits()
            else:
                self.bot.editMessageText(self.menu,"Тогда продолжаем", reply_markup=None)
                self.menu=None

