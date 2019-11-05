from konlpy.tag import Komoran
# from konlpy.tag import Kkma, Twitter, Komoran, Hannanum


class Analyser:
    tagger = Komoran()

    def __init__(self):
        pass

    def get_noun_tokens(self, text):
        result = self.tagger.nouns(text)
        print("NOUNS", result)
        return result
