

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
                sendMessage(game.chat_id, "It's your move")
        elif game.isRunning:
            sendMessage(game.chat_id, play(game,wrd))
        else:
            sendMessage(game.chat_id, self.idleChat())
