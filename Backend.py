import requests
import re
from bs4 import BeautifulSoup as bs
from random import choice
from jamo import h2j, j2hcj
from unicode import join_jamos  # https://github.com/kaniblu/hangul-utils

url = "https://wordrow.kr/시작하는-말/"
check = lambda w: re.search("^[가-힣]{2,}$", w)

def check_dueum(user_w):
    d_w = j2hcj(h2j(user_w))
    if d_w[0] == "ㄴ" or d_w[0] == "ㄹ":
        d_w = "ㅇ" + d_w[1:]
        new_w = join_jamos(d_w)
        return new_w
    return None

def word_check(user_w, used):
    if " " in user_w:
        return "", "[System] : 단어에 띄어쓰기가 들어갈 수 없습니다."
    elif user_w in used:
        return "", "[System] : 이미 사용된 단어는 다시 사용할 수 없습니다."
    html = requests.get(url=url + user_w)
    soup = bs(html.text, "html.parser")
    ul = soup.select_one("div.larger > ul")

    try:
        word_list = list(ul.find('li').stripped_strings)

        w, e = word_list[0], word_list[1].split(":\n")[1]
        if check(w):
            used.append(w)
            return w, e
        return "", "[System] : 없는 단어입니다"
    except:
        return "", "[System] : 없는 단어입니다"


def choose_word(user_w, used):
    global html
    try:
        html = requests.get(url=url + user_w)
        soup = bs(html.text, "html.parser")
        ul = soup.select_one("div.larger > ul")
        word_list = ul.select("li")
    except Exception as e:
        print(e)
        print(html.text)
        return

    to_choice = []
    for word in word_list:
        try:
            l = word.get_text().split(":", 1)
            w = l[0].lstrip().rstrip()
            e = l[1]

            if check(w):
                to_choice.append([w, e])

        except ValueError:
            d_w = j2hcj(h2j(user_w))
            if d_w[0] == "ㄴ" or d_w[0] == "ㄹ":
                d_w = "ㅇ" + d_w[1:] if d_w[0] == "ㄴ" else "ㄴ" + d_w[1:]
                new_w = join_jamos(d_w)
                r, w = choose_word(new_w, used)
                if r:
                    return True, w
            return False, None

    try:
        select = choice(to_choice)
        return True, select
    except IndexError:
        return False, None
