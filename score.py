import random

class Score:

    alphabet={'a': 0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0}
    score_limit=0
    moves_limit=0

    def __init__(self,score_limit,moves_limit):
        self.createValues()
        self.score_limit=int(score_limit)
        self.moves_limit=int(moves_limit)

    def createValues(self):
        for key in self.alphabet.keys():
            self.alphabet[key]=random.randint(0,5)

    def isOver(self,ai_score,user_score,moves):
        if ai_score>=self.score_limit or user_score>=self.score_limit or moves>=self.moves_limit:
            return True
        else:
            return False

