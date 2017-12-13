from telepot.telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
from telepot.telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
import dbInteraction

max_score1 = 1000
max_score2 = 2000


kbMain = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Быстрая игра', callback_data='main~Quick Game')],
    [InlineKeyboardButton(text='Своя игра', callback_data='main~Own Game')]
])


kbCategories = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Птицы', callback_data='category~Bird')],
[InlineKeyboardButton(text='Животные', callback_data='category~Animal')],
[InlineKeyboardButton(text='Города', callback_data='category~City')],
[InlineKeyboardButton(text='Книги', callback_data='category~Book')],
[InlineKeyboardButton(text='Пьесы', callback_data='category~Play')],
[InlineKeyboardButton(text='Еда', callback_data='category~Food')],
[InlineKeyboardButton(text='Звезды', callback_data='category~Star')],
[InlineKeyboardButton(text='Видеоигры', callback_data='category~VideoGame')],
[InlineKeyboardButton(text='Лекарственные препараты', callback_data='category~Drug')],
[InlineKeyboardButton(text='Фильмы', callback_data='category~Film')]
])



kbScores = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=max_score1, callback_data='scoreLimit~'+str(max_score1))]
    , [InlineKeyboardButton(text=max_score2, callback_data='scoreLimit~'+str(max_score2))]
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
[KeyboardButton(text='Текущий счет')],
[KeyboardButton(text='Авторы')]
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
