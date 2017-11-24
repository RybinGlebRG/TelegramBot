
from telepot.telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

class InputAnalyzer:

    def idleChat(self):
        return "Game isn't started"

    def analyze(self,wrd,game,play,sendMessage):
        if (wrd=="/startGame"):
            if game.isRunning:
                sendMessage(game.chat_id, "You have already started the game")
            else:
                game.isRunning=True

                game.startGame()
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='theme1', callback_data='theme~theme1')],
                    [InlineKeyboardButton(text='theme2', callback_data='theme~theme2')]
                ])
                sendMessage(game.chat_id, "It's your move. Shoose theme:", reply_markup=keyboard)
                #return "It's your move"
        elif game.isRunning:
            sendMessage(game.chat_id, play(game,wrd))
        else:
            sendMessage(game.chat_id, self.idleChat())
