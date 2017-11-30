from telepot.telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
from telepot.telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
import dbInteraction

kbMain = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Быстрая игра', callback_data='main~Quick Game')],
    [InlineKeyboardButton(text='Своя игра', callback_data='main~Own Game')]
])

# TODO Get values from database
#kbCategories = InlineKeyboardMarkup(inline_keyboard=[
#    [InlineKeyboardButton(text='Цвета', callback_data='category~Colors')]
#])

kbScores = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='10', callback_data='scoreLimit~10')]
    , [InlineKeyboardButton(text='20', callback_data='scoreLimit~20')]
])

kbMoves = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='5', callback_data='movesLimit~5')]
    , [InlineKeyboardButton(text='15', callback_data='movesLimit~15')]
])

kbConfirm = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='confirm~Yes'),
     InlineKeyboardButton(text='Нет', callback_data='confirm~No')]
])

kbConfirmNG = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='confirmNG~Yes'),
     InlineKeyboardButton(text='Нет', callback_data='confirmNG~No')]
])

kbNG = ReplyKeyboardMarkup(keyboard=
[[
    KeyboardButton(text='Начать новую игру'),
    KeyboardButton(text='Закончить текущую игру')
],
[KeyboardButton(text='Текущий счет')]
], resize_keyboard=True)


class Keyboards():
    db=None

    def __init__(self,db):
        self.db=db

    def getKeyboard(self,type):
        if type=="kbMain":
            return kbMain
        elif type=="kbScores":
            return kbScores
        elif type=="kbMoves":
            return kbMoves
        elif type=="kbConfirm":
            return kbConfirm
        elif type=="kbConfirmNG":
            return kbConfirm
        elif type=="kbNG":
            return kbNG
        elif type=="kbCategories":
            buttons=[]
            categories=[]
            res=self.db.getCategories()
            for tup in res:
                categories.append(tup[0].title())
            for cat in categories:
                buttons.append([InlineKeyboardButton(text=cat, callback_data='category~'+cat)])
            kbCategories=InlineKeyboardMarkup(inline_keyboard=buttons)
            return kbCategories
