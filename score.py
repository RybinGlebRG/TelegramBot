import random


class Score:
    def letter_dict(self):
        answer = [chr(i) for i in range(ord('a'), ord('z') + 1)]  # latinic letters
        answer.extend([chr(i) for i in range(ord('а'), ord('я') + 1)])  # cyrillic letter
        answer.extend([str(i) for i in range(10)])  # numbers
        answer.extend(['-', ' ', '(', ')', ])  # spec chars
        return dict((i, 0) for i in answer)

    alphabet = 0

    score_limit = 0
    moves_limit = 0

    def __init__(self, score_limit, moves_limit):
        self.alphabet = self.letter_dict()
        self.createValues()
        self.score_limit = int(score_limit)
        self.moves_limit = int(moves_limit)

    def createValues(self):
        for key in self.alphabet.keys():
            self.alphabet[key] = random.randint(1, 5)

    def isOver(self, ai_score, user_score, moves):
        if ai_score >= self.score_limit or user_score >= self.score_limit or moves >= self.moves_limit:
            return True
        else:
            return False
