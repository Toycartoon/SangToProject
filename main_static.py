# 2번째 코드 / 이후 GUI와 상호작용을 위해 Backend.py, GUI.py로 분리됨

import chromedriver_autoinstaller as cd
import requests
import re
from bs4 import BeautifulSoup as bs
from random import choice
from jamo import h2j, j2hcj
from unicode import join_jamos  # https://github.com/kaniblu/hangul-utils

cd.install()

url = "https://wordrow.kr/시작하는-말/"
check = lambda w: re.search("^[가-힣]{2,}$", w)

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


def choose_word(user_w, used, user_turn):
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
            l = word.get_text().split(":")
            w = l[0].lstrip().rstrip()
            e = ":".join(l[1:]).lstrip().rstrip()

            if check(w):
                to_choice.append([w, e])

        except ValueError:
            d_w = j2hcj(h2j(user_w))
            if d_w[0] == "ㄴ" or d_w[0] == "ㄹ":
                d_w = "ㅇ" + d_w[1:] if d_w[0] == "ㄴ" else "ㄴ" + d_w[1:]
                new_w = join_jamos(d_w)
                r, w = choose_word(new_w, used, user_turn)
                if r:
                    return True, w
            return False, None

    try:
        select = choice(to_choice)
        print(f": {select[0]}")
        print(select[1])
        return True, select[0][len(select[0]) - 1]
    except IndexError:
        return False, None


used = []
s = choice(["가", "나", "다", "라", "마"])   # 배열 안에 넣고 싶은 단어를 넣어주세요
user_turn = True
while True:
    w = input(f"[System] : 다음 단어로 끝말잇기를 해주세요 \"{s}\" \n 단어가 더 이상 생각나지 않으신다면 Enter를 입력해주세요 : ")

    if w == "":
        print("[System] : 패배하셨습니다..")
        break
    if w[0] != s:
        d_w = j2hcj(h2j(s))
        if d_w[0] == "ㄴ" or d_w[0] == "ㄹ":
            d_w = "ㅇ" + d_w[1:] if d_w[0] == "ㄴ" else "ㄴ" + d_w[1:]
            to_compare = join_jamos(d_w)
            if w[0] != to_compare:
                print(f"[System] : \"{s}\"로 시작하는 단어를 입력해주세요")
                continue
        else:
            print(f"[System] : \"{s}\"로 시작하는 단어를 입력해주세요")
            continue
    elif len(w) == 1:
        print("[System] : 한 단어는 입력하실 수 없습니다.")
        continue
    elif re.search("[^가-힣]", w):
        print("[System] : 모든 단어는 가-힣 사이의 한글로만 이루어져야합니다.")
        continue
    r_w, r_e = word_check(w, used)

    if r_w != w:
        print(r_e)
        continue
    else:
        print(r_e)
        user_turn = False
        result, word = choose_word(w[len(w) - 1], used, user_turn)

        if result:
            user_turn = True
            s = word
        else:
            print("[System] : 승리하셨습니다!")
            break

print("Thank you for playing!")
