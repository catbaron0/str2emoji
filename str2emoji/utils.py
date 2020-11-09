from bs4 import BeautifulSoup as bs
import requests
import json
import time
import tqdm
import random
from pypinyin import lazy_pinyin, pinyin
from functools import reduce
from LAC import LAC
from pathlib import Path, PurePath

headers = {
    'Referer': 'https://www.emojiall.com/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}

def word2py(word: str):
    py = pinyin(word, heteronym=False, errors=lambda x: list(x))
    py = ''.join(reduce(lambda a,b: a+b, py))
    return py

def emoji2words(emoji: str):
    url = 'https://www.emojiall.com/zh-hans/emoji/' + emoji.strip()
    res = requests.get(url, headers=headers)
    soup = bs(res.text, features="lxml")
    tables = soup.find_all('table')
    table = None
    for t in tables:
        if t.td.text.strip() == 'Emoji:':
            table = t
            break
    tds = table.find_all('td')

    name = tds[3].text.strip()
    if name.startswith('旗: '):
        return (name.split(' ')[1], )
    alias = list()
    for td in tds:
        if td.text.strip() == '简短名称:':
            name = td.find_next_sibling().text.strip()
            if name.startswith('旗: '):
                return (name.split(' ')[1], )
        if td.text.strip() == '也称为:':
            alias = [a.strip() for a in td.find_next_sibling().text.split('|')]
    words =  (name, *alias)
    return words

def gen_emoji2words_data():
    data = dict()
    with open('emoji_list', 'r') as f:
        for emoji in tqdm.tqdm(list(f)):
            time.sleep(1)
            try:
                data[emoji] = emoji2words(emoji)
            except Exception as e:
                print(f"Failed on {emoji}: {e}")

    with open('emoji2words.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def gen_word2emoji_data():
    with open('word2emoji.json', 'r') as f:
        w2e = json.load(f)
    with open('emoji2words.json', 'r') as f:
        emoji2words = json.load(f)
    word2emoji = dict()
    for k in w2e:
        word = k.lower()
        if word in word2emoji:
            word2emoji[word].append(w2e[k])
        else:
            word2emoji[word] = [w2e[k]]
    for emoji, words in tqdm.tqdm(list(emoji2words.items())):
        for word in words:
            try:
                word2emoji[word.lower()].append(emoji)
            except KeyError:
                word2emoji[word.lower()] = [emoji]
    for k in word2emoji:
        word2emoji[k] = list(set(word2emoji[k]))
    with open('word2emoji.json', 'w') as f:
        json.dump(word2emoji, f, indent=4, ensure_ascii=False)

def gen_py2emoji_data(lazy: bool) -> dict:
    with open('word2emoji.json', 'r') as f:
        word2emoji = json.load(f)
    py2emoji = dict()
    for word, emojis in tqdm.tqdm(list(word2emoji.items())):
        if lazy:
            py = ''.join(lazy_pinyin(word))
        else:
            # import ipdb; ipdb.set_trace()
            # py = ''.join(pinyin(word))
            py = ''.join(word2py(word))
        try:
            py2emoji[py] += emojis
        except KeyError:
            py2emoji[py] = emojis
    with open('py2emoji.json', 'w') as f:
        json.dump(py2emoji, f, indent=4, ensure_ascii=False)



class Sent2Emoji:
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



if __name__ == '__main__':
    # print(emoji2words('🇿🇼'))
    # print(emoji2words('😇'))
    # print(emoji2words('😀'))
    # print(emoji2words('🥇'))
    # gen_emoji2words_data()
    # e2w = {
    #         '😇': ['天使'],
    #         '🥇': ['第一名','金牌','冠军']
    # }
    # s2e = Sent2Emoji(data)
    # print(s2e.sent2emoji('天使爱美丽获得了冠军'))
    # gen_word2emoji_data()
    # gen_py2emoji_data(lazy=False)
    # s2e = Sent2Emoji()
    print('test')


