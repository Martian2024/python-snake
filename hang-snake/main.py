import os
import sys
import random
import time
from pynput import keyboard

class Snake:
    def __init__(self):
        self.direction = 'down'
        self.points = [[49, 26], [49, 25], [49, 24]]

    def move(self):
        new_x, new_y = self.points[0]
        self.points.pop()
        match self.direction:
            case 'up':
                self.points.insert(0, [new_x, new_y - 1])
            case 'left':
                self.points.insert(0, [new_x - 1, new_y])
            case 'right':
                self.points.insert(0, [new_x + 1, new_y])
            case 'down':
                self.points.insert(0, [new_x, new_y + 1])

        for i in range(len(self.letters_on_field)):
            if self.letters_on_field[i][1] == self.points[0]:
                self.eat()
                self.letters_on_field.pop(i)
                break


    def eat(self):
        new_x, new_y = self.points[0]
        self.points.insert(0, [new_x, new_y])

    def generate_field(self, word):
        self.alpha = ALPHA[:]
        random.shuffle(list(self.alpha))
        self.letters_on_field = []
        for i in word:
            if i not in guessed:
                self.letters_on_field.append([i, [random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)]])
                break
        for i in self.alpha:
            x = random.randint(0, WIDTH - 1)
            while self.letters_on_field[0][1][0] - 1 < x < self.letters_on_field[0][1][0] + 1:
                x = random.randint(0, WIDTH - 1)
            y = random.randint(0, HEIGHT - 1)
            while self.letters_on_field[0][1][1] - 1 < x < self.letters_on_field[0][1][1] + 1:
                y = random.randint(0, HEIGHT - 1)
            self.letters_on_field.append([i, [x, y]])

def on_press(key):
    match key:
        case keyboard.Key.left:
            if snake.direction != 'right':
                snake.direction = 'left'
        case keyboard.Key.up:
            if snake.direction != 'down':
                snake.direction = 'up'
        case keyboard.Key.right:
            if snake.direction != 'left':
                snake.direction = 'right'
        case keyboard.Key.down:
            if snake.direction != 'up':
                snake.direction = 'down'


def update_world():
    os.system('cls||clear')
    world = [[" " for i in range(WIDTH)] for i in range(HEIGHT)]
    for i in snake.letters_on_field:
        world[i[1][1]][i[1][0]] = i[0]
    print('_' * WIDTH)
    for i in snake.points[1:]:
        world[i[1]][i[0]] = '*'
    world[snake.points[0][1]][snake.points[0][0]] = '0'
    for i in world:
        print('|' + ''.join(i) + '|')
    print(' ' + '¯' * WIDTH)


if __name__ == '__main__':
    WIDTH = 100
    HEIGHT = 50
    os.system(f"mode con cols={WIDTH + 2} lines={HEIGHT + 2}")
    fps = 10
    listener = keyboard.Listener(on_press=on_press, suppress=False)
    file = open('nouns_list.txt', encoding='utf-8')
    WORDS = file.readlines()
    ALPHA = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    file.close()
    used_words = []
    MAX_MISTAKES = 5
    sys.stdin = open('input.txt', mode='r')
    while True:
        try:
            word = random.choice(WORDS)
            print(word)
            while word in used_words:
                word = random.choice(WORDS)
            used_words.append(word)
            world = [[" " for i in range(WIDTH)] for i in range(HEIGHT)]
            mistakes = 0
            guessed = []
            wrong = []
            snake = Snake()
            snake.generate_field(word)
            game_flag = True
            listener.start()
            while game_flag:
                snake.move()
                update_world()
                time.sleep(1/fps)
        except Exception:
            listener.stop()
            os.system('cls||clear')
            # TODO: clear stdin
            game_flag = input('Чел, ты лох, и ты проиграл. Можешь поплакать об этом, а можешь начать заново. Ну как? 0 - выйти, 1 - заново: ') == '1'
            if not game_flag:
                break
        else:
            listener.stop()
            os.system('cls||clear')
            game_flag = ('Капец, ты выиграл! Можешь начать заново, а можешь пойти потрогать траву. 0 - выйти, 1 - заново:')
            if not game_flag:
                break