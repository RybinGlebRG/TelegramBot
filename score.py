import random


class Score:
    alphabet = {'а': 0, 'б': 0, 'в': 0, 'г': 0, 'д': 0, 'е': 0, 'ё': 0, 'ж': 0, 'з': 0, 'и': 0, 'й': 0, 'к': 0, 'л': 0,
                'м': 0, 'н': 0, 'о': 0, 'п': 0, 'р': 0, 'с': 0, 'т': 0, 'у': 0, 'ф': 0, 'х': 0, 'ц': 0, 'ч': 0, 'ш': 0, 'щ': 0,
                'ъ': 0, 'ы': 0, 'ь': 0, 'э': 0, 'ю': 0, 'я': 0, '-': 0, ' ': 0}
    score_limit = 0
    moves_limit = 0

    def __init__(self, score_limit, moves_limit):
        print(self.alphabet.__len__())
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
