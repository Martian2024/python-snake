import os
import sys
import random
import time


def update_world():
    os.system('cls||clear')
    print(' '.join(word_line))
    for i in hangman:
        print(i)

def upload_templates():
        templates = [[] for _ in range(6)]
        file = open('template.txt').readlines()
        for i in range(6):
            for j in range(30):
                templates[i].append(file[30 * i + j].replace('\n', ''))
        hangman = templates[0]
        return hangman, templates



if __name__ == '__main__':
    WIDTH = 50
    HEIGHT = 30
    os.system(f"mode con cols={WIDTH + 60} lines={HEIGHT + 3}")
    fps = 5
    file = open('nouns_list.txt', encoding='utf-8')
    WORDS = list(map(lambda x: x.strip(), file.readlines()))
    ALPHA = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    file.close()
    MAX_MISTAKES = 5
    used_words = []
    win = False
    while True:
        current_mistakes = 0
        game_state = True
        word = random.choice(WORDS)
        hangman, templates = upload_templates()
        while word in used_words:
            word = random.choice(WORDS)
        word_line = ['_' for _ in range(len(word))]
        while game_state:
            update_world()
            a = input('Введите букву: ')
            if a in word:
                print(word)
                print(word_line)
                for i in range(len(word)):
                    if word[i] == a:
                        word_line[i] = a
                if ''.join(word_line) == word:
                    win = True
                    game_state = False
            else:
                current_mistakes += 1
                hangman = templates[current_mistakes]
            if current_mistakes >= MAX_MISTAKES:
                game_state = False
        if win:
            update_world()
            if input('Капец, ты выиграл! Можешь начать заново, а можешь пойти потрогать траву. 0 - выйти, 1 - заново:') == '1':
                game_state = True
            else:
                break
        else:
            word_line = list(word)
            update_world()
            if input('Чел, ты лох, и ты проиграл. Можешь поплакать об этом, а можешь начать заново. Ну как? 0 - выйти, 1 - заново: ') == '1':
                game_state = True
            else:
                break