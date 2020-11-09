import random
from LAC import LAC
from pathlib import PurePath
import json
# import utils
from .utils import word2py, lazy_pinyin

# from .utils import word2py, lazy_pinyin

class Str2Emoji:
    def __init__(self):
        self.lac = LAC(mode='seg')
        path = PurePath(__file__).parent
        with open(path/'word2emoji.json', 'r') as f:
            self.w2e = json.load(f)
        with open(path/'py2emoji.json', 'r') as f:
            self.p2e = json.load(f)
        with open(path/'lpy2emoji.json', 'r') as f:
            self.lp2e = json.load(f)

    def word2emoji(self, word) -> str:
        if word in self.w2e:
            return random.choice(self.w2e[word])
        emoji_list = list()
        for w in word:
            if w in self.w2e:
                emoji_list.append(random.choice(self.w2e[w]))
            else:
                py = word2py(w)
                if py in self.p2e:
                    emoji_list.append(random.choice(self.p2e[py]))
                else:
                    lpy = ''.join(lazy_pinyin(w))
                    if lpy in self.lp2e:
                        emoji_list.append(random.choice(self.lp2e[lpy]))
                    else:
                        emoji_list.append(w)
        return ''.join(emoji_list)


    def sent2emoji(self, sent: str) -> str:
        sent = sent.lower()
        words = self.lac.run(sent)
        emoji = [self.word2emoji(word) for word in words]
        return ''.join(emoji)



