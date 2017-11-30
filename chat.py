import game
from telepot.telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
import telepot.telepot as tp

class Chat:
    chat_id = None
    game = None
    bot=None
    db=None
    category=None
    score_limit=None
    moves_limit=None

    def __init__(self,chat_id,bot,db,evo):
        self.chat_id=chat_id
        self.bot=bot
        self.db=db
        self.evo=evo

    def analyze(self,word):
        if (word == "/startGame"):
            if self.game is not None:

                if self.game.isRunning:
                    self.bot.sendMessage(self.chat_id, "You have already started the game")
                else:
                    self.getLimits()

            else:
                self.game=game.Game(self.chat_id,self.db,self.evo)
                self.getLimits()

        elif self.game is not None:
            if self.game.isRunning:
                if self.checkUserWord(word):
                    self.game.curQuestion=word
                    self.bot.sendMessage(self.chat_id, self.game.gameProcess().title())
                else:
                    self.bot.sendMessage(self.chat_id, "Your word is incorrect")
            else:
                self.bot.sendMessage(self.chat_id, self.idleChat())
        else:
            self.bot.sendMessage(self.chat_id, self.idleChat())

    def start(self,category,score_limit,moves_limit):
        self.game.startGame(category, score_limit, moves_limit)
        self.bot.sendMessage(self.chat_id, "It is your move")

    def idleChat(self):
        return "Game isn't started"

    def checkUserWord(self,word):
        if self.game.curAnswer is not None:
            if word[0].upper()==self.game.curAnswer[-1].upper():
                return True
            else:
                return False
        else:
            return True


    def getLimits(self):
        kbCategories = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Colors', callback_data='category~Colors')]
        ])
        kbScoreLimit = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='10', callback_data='scoreLimit~10')]
            , [InlineKeyboardButton(text='20', callback_data='scoreLimit~20')]
        ])
        kbMovesLimit = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='5', callback_data='movesLimit~5')]
            , [InlineKeyboardButton(text='15', callback_data='movesLimit~15')]
        ])
        kbDecision = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Start', callback_data='decision~Start'),
             InlineKeyboardButton(text='Leave', callback_data='decision~Leave')]
        ])

        self.bot.sendMessage(self.chat_id, "Choose category:", reply_markup=kbCategories)
        self.bot.sendMessage(self.chat_id, "Choose score limit:", reply_markup=kbScoreLimit)
        self.bot.sendMessage(self.chat_id, "Choose moves limit:", reply_markup=kbMovesLimit)
        self.bot.sendMessage(self.chat_id, "What do we do now?", reply_markup=kbDecision)

    def on_callback_query(self, msg):
        query_id, from_id, query_data = tp.glance(msg, flavor='callback_query')
        print('Callback Query:', query_id, from_id, query_data)
        if query_data[:query_data.find('~')] == 'category':
            self.bot.answerCallbackQuery(query_id,
                                    text='Got it, your category is "' + query_data[query_data.find('~') + 1:] + '"')
            self.category=query_data[query_data.find('~') + 1:]
        elif query_data[:query_data.find('~')] == 'scoreLimit':
            self.bot.answerCallbackQuery(query_id,
                                    text='Got it, your score limit is "' + query_data[query_data.find('~') + 1:] + '"')
            self.score_limit=query_data[query_data.find('~') + 1:]
        elif query_data[:query_data.find('~')] == 'movesLimit':
            self.bot.answerCallbackQuery(query_id,
                                    text='Got it, your moves limit is "' + query_data[query_data.find('~') + 1:] + '"')
            self.moves_limit=query_data[query_data.find('~') + 1:]

        elif query_data[:query_data.find('~')] == 'decision':
            if query_data[query_data.find('~') + 1:]=='Start':
                self.start(self.category,self.score_limit,self.moves_limit)
            else:
                # TODO Implement this
                pass

