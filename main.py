# 최초 코드 / 동적 크롤링이라 속도면에서 떨어져 이후 정적 크롤링으로 변경

import chromedriver_autoinstaller as cd
from selenium import webdriver
from random import choice
from selenium.webdriver.common.by import By
from jamo import h2j, j2hcj
from unicode import join_jamos  # https://github.com/kaniblu/hangul-utils

cd.install()

options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_argument('disable-gpu')
options.add_argument('headless')

driver = webdriver.Chrome(options=options)

url = "https://wordrow.kr/시작하는-말/"


def check(user_w, used):
    if " " in user_w:
        return "[System] : 단어에 띄어쓰기가 들어갈 수 없습니다."
    elif user_w in used:
        return "[System] : 이미 사용된 단어는 다시 사용할 수 없습니다."
    driver.get(url=url + user_w)
    word_list = driver.find_element(By.XPATH, "/html/body/div[1]/section[1]/div[3]").text.split("\n")

    for i in word_list:
        try:
            w, e = i.split(" : ")

            if user_w == w:
                print(e)
                return w
        except ValueError:
            break

    return "[System] : 없는 단어입니다."


def choose_word(user_w, used, user_turn):
    driver.get(url=url + user_w)
    word_list = driver.find_element(By.XPATH, "/html/body/div[1]/section[1]/div[3]").text.split("\n")

    to_choice = []
    for i in word_list:
        try:
            if " : " not in i:
                continue

            w, e = i.split(" : ")

            if " " not in w and w not in used and len(w) != 1:
                to_choice.append([w, e])
        except ValueError:
            d_w = j2hcj(h2j(user_w))
            print(d_w, d_w[0])
            if d_w[0] == "ㄴ" or d_w[0] == "ㄹ":
                d_w = "ㅇ" + d_w[1:]
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
    w = input(f"[System] : 다음 단어로 끝말잇기를 해주세요 \"{s}\" \n 단어가 더 이상 생각나지 않으신다면 \"\"를 입력해주세요 : ")

    if w == "":
        print("[System] : 패배하셨습니다..")
        break
    if w[0] != s:
        d_w = j2hcj(h2j(s))
        if d_w[0] == "ㄴ" or d_w[0] == "ㄹ":
            d_w = "ㅇ" + d_w[1:]
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
    result = check(w, used)

    if result != w:
        print(result)
        continue
    else:
        user_turn = False
        result, word = choose_word(w[len(w) - 1], used, user_turn)

        if result:
            user_turn = True
            s = word
        else:
            print("[System] : 승리하셨습니다!")
            break

driver.quit()
print("Thank you for playing!")
