from TelegramInterface import keyboards as kb
from TelegramInterface.telepot import telepot as tp


class Chat:
    chat_id=None
    state=None
    menu=None

    def __init__(self,  chat_id ):
        self.chat_id=chat_id




class FSM:
    sendMessage=None
    chat_id=None
    state=None
    game=None
    menu=None
    bot=None
    chats=[]

    def __init__(self,sendMessage,chat_id,game,bot):
        self.sendMessage=sendMessage
        self.chat_id=chat_id
        self.game=game
        self.bot=bot

    def createChat(self,chat_id):
        self.chats.append(Chat(chat_id))

    def findChat(self,chat_id):
        cur_chat = None
        for i in range(0,len(self.chats)):
            if self.chats[i].chat_id==chat_id:
                cur_chat=self.chats[i]
        return cur_chat

    def findOrCreateChat(self,chat_id):
        cur_chat=None
        cur_chat=self.findChat(chat_id)
        if cur_chat is None:
            cur_chat=self.createChat(chat_id)
        return cur_chat

    def stateMain(self,chat):
        chat.menu=None
        chat.state="main"

    def stateConfirmClose(self,chat):
        chat.state="confirm_close"
        msg = self.sendMessage(chat.chat_id, "Вы уверены?", reply_markup=kb.kbConfirm)
        chat.menu = tp.message_identifier(msg)

    def stateConfirmNG(self,chat):
        chat.state = "confirm_ng"


    def stateGameType(self,chat):
        chat.state = "game_type"
        msg = self.bot.sendMessage(chat.chat_id, "Ну и как поступим?", reply_markup=kb.kbMain)
        chat.menu = tp.message_identifier(msg)


    def stateCategory(self,chat):
        chat.state = "category"
        self.bot.editMessageText(chat.menu, text="Выберите тему", reply_markup=kb.kbCategories)


    def stateScoreLimits(self,chat):
        chat.state = "score_limits"
        self.bot.editMessageText(chat.menu, text="Выберите количество очков", reply_markup=kb.kbScores)


    def stateMovesLimits(self,chat):
        chat.state = "moves_limits"
        self.bot.editMessageText(chat.menu, text="Выберите количество ходов", reply_markup=kb.kbMoves)


    def handler(self,chat_id, txt):
        chat=self.findOrCreateChat(chat_id)
        if txt== "/start":
            # Work
            if chat.state is None:
                self.sendMessage(chat.chat_id, 'Сыграем?', reply_markup=kb.kbNG)
                self.stateMain(chat)
        # TODO Stopped here
        elif txt== "Начать новую игру":
            # Do not work
            if self.game.isRunning:
                self.stateConfirmClose()
            else:
                self.stateGameType()

        elif txt == "Закончить текущую игру":
            # Do not work
            if self.game.isRunning:
                self.stateConfirmClose()
            else:
                self.bot.sendMessage(self.chat_id, "Игра не начата")

        elif  txt== "yes":
            # Do not work
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
            # Do not work
            if self.state=="confirm_close":
                self.bot.editMessageText(self.menu, "Тогда продолжаем", reply_markup=None)
                self.stateMain()
            if self.state=="confirm_ng":
                self.bot.editMessageText(self.menu, "Тогда продолжаем", reply_markup=None)
                self.stateMain()

        elif txt== "Быстря игра":
            # Do not work
            self.stateMain()

        elif txt== "Своя игра":
            # Do not work
            self.stateCategory()

        elif txt== "Категория":
            # Do not work
            self.stateScoreLimits()

        elif txt== "Очки":
            # Do not work
            self.stateMovesLimits()

        elif txt== "Ходы":
            # Do not work
            self.stateMain()