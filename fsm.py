import keyboards as kb
import telepot.telepot as tp

class FSM:
    sendMessage=None
    chat_id=None
    state=None
    game=None
    menu=None
    bot=None

    def __init__(self,sendMessage,chat_id,game,bot):
        self.sendMessage=sendMessage
        self.chat_id=chat_id
        self.game=game
        self.bot=bot


    def stateMain(self):
        self.menu=None
        self.state="main"

    def stateConfirmClose(self):
        self.state="confirm_close"
        msg = self.sendMessage(self.chat_id, "Вы уверены?", reply_markup=kb.kbConfirm)
        self.menu = tp.message_identifier(msg)

    def stateConfirmNG(self):
        self.state = "confirm_ng"


    def stateGameType(self):
        self.state = "game_type"
        msg = self.bot.sendMessage(self.chat_id, "Ну и как поступим?", reply_markup=kb.kbMain)
        self.menu = tp.message_identifier(msg)


    def stateCategory(self):
        self.state = "category"
        self.bot.editMessageText(self.menu, text="Выберите тему", reply_markup=kb.kbCategories)


    def stateScoreLimits(self):
        self.state = "score_limits"
        self.bot.editMessageText(self.menu, text="Выберите количество очков", reply_markup=kb.kbScores)


    def stateMovesLimits(self):
        self.state = "moves_limits"
        self.bot.editMessageText(self.menu, text="Выберите количество ходов", reply_markup=kb.kbMoves)


    def handler(self, txt):
        if txt== "/start":
            if self.state is None:
                self.sendMessage(self.chat_id, 'Сыграем?', reply_markup=kb.kbNG)
                self.stateMain()

        elif txt== "Начать новую игру":
            if self.game.isRunning:
                self.stateConfirmClose()
            else:
                self.stateGameType()

        elif txt == "Закончить текущую игру":
            if self.game.isRunning:
                self.stateConfirmClose()
            else:
                self.bot.sendMessage(self.chat_id, "Игра не начата")

        elif  txt== "yes":
            if self.state=="confirm_close":
                self.bot.editMessageText(self.menu, "Игра завершена", reply_markup=None)
                self.bot.sendMessage(self.chat_id,
                                     "Счет: Я: " + str(self.game.ai_score) + ", Вы: " + str(
                                         self.game.user_score))
                self.game.closeGame(1)
                self.stateMain()
            if self.state == "confirm_ng":
                self.bot.sendMessage(self.chat_id,
                                     "Счет: Я: " + str(self.game.ai_score) + ", Вы: " + str(
                                         self.game.user_score))
                self.game.closeGame(1)
                self.stateGameType()


        elif txt== "no":
            if self.state=="confirm_close":
                self.bot.editMessageText(self.menu, "Тогда продолжаем", reply_markup=None)
                self.stateMain()
            if self.state=="confirm_ng":
                self.bot.editMessageText(self.menu, "Тогда продолжаем", reply_markup=None)
                self.stateMain()

        elif txt== "Быстря игра":
            self.stateMain()

        elif txt== "Своя игра":
            self.stateCategory()

        elif txt== "Категория":
            self.stateScoreLimits()

        elif txt== "Очки":
            self.stateMovesLimits()

        elif txt== "Ходы":
            self.stateMain()