import os
import sys
import random
import time
from pynput import keyboard

class Snake:
    def __init__(self):
        self.direction = 'up'
        self.points = [[WIDTH // 2, HEIGHT // 2], [WIDTH // 2, HEIGHT // 2 + 1], [WIDTH // 2, HEIGHT // 2 + 1]]
        self.letters_on_field = []
        self.game = 'play'
        self.direction_changed = False
        self.used_words = []
        self.guessed = []
        self.mistakes = 0
        self.word = ''
        self.word_line = []
        self.upload_templates()

    def upload_templates(self):
        self.templates = [[] for _ in range(6)]
        file = open('template.txt').readlines()
        for i in range(6):
            l = []
            for j in range(30):
                self.templates[i].append(file[30 * i + j].replace('\n', ''))
            self.templates.append(l)
        self.hangman = self.templates[0]

    def move(self):
        new_x, new_y = self.points[0]
        match self.direction:
            case 'up':
                self.points.insert(0, [new_x, new_y - 1])
            case 'left':
                self.points.insert(0, [new_x - 1, new_y])
            case 'right':
                self.points.insert(0, [new_x + 1, new_y])
            case 'down':
                self.points.insert(0, [new_x, new_y + 1])
        flag = False
        for i in range(len(self.letters_on_field)):
            if self.letters_on_field[i][1] == self.points[0]:
                self.eat(i)
                flag = True
                self.letters_on_field.pop(i)
                break
        if not flag:
            self.points.pop()

        if self.points[0][0] < 0 or self.points[0][1] < 0 or self.points[0][0] >= WIDTH or \
                self.points[0][1] >= HEIGHT or self.points.count(self.points[0]) == 2:
            self.game = 'defeat'




    def eat(self, index):
        if self.letters_on_field[index][0] in self.word:
            for i in range(len(self.word)):
                if self.word[i] == self.letters_on_field[index][0]:
                    self.word_line[i] = self.letters_on_field[index][0]

        else:
            self.mistakes += 1
            self.hangman = self.templates[self.mistakes]
            if self.mistakes >= MAX_MISTAKES:
                self.game = 'defeat'
        print(self.word_line)

    def generate_field(self):
        for i in ALPHA:
            self.letters_on_field.append([i, [random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)]])


def on_press(key):
    if not snake.direction_changed:
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
        snake.direction_changed = True



def update_world():
    os.system('cls||clear')
    world = [[" " for i in range(WIDTH)] for i in range(HEIGHT)]
    for i in snake.letters_on_field:
        world[i[1][1]][i[1][0]] = i[0]
    print(' ' * WIDTH)
    print(' ' + '_' * WIDTH)
    for i in snake.points[1:]:
        world[i[1]][i[0]] = '*'
    world[snake.points[0][1]][snake.points[0][0]] = '0'
    for i in range(len(world)):
        world[i].append(snake.hangman[i])
    world[2][-1] = 5 * ' ' + ' '.join(snake.word_line)
    for i in range(len(world)):
        print('|' + ''.join(world[i][:-1]) + '|' + world[i][-1])
    print(' ' + '¯' * WIDTH)


if __name__ == '__main__':
    WIDTH = 50
    HEIGHT = 30
    os.system(f"mode con cols={WIDTH + 50} lines={HEIGHT + 3}")
    fps = 5
    file = open('nouns_list.txt', encoding='utf-8')
    WORDS = file.readlines()
    ALPHA = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    file.close()

    MAX_MISTAKES = 5
    while True:
        snake = Snake()
        listener = keyboard.Listener(on_press=on_press, suppress=False)
        snake.word = random.choice(WORDS)
        print(snake.word)
        while snake.word in snake.used_words:
            snake.word = random.choice(WORDS)
        snake.used_words.append(snake.word)
        snake.word_line = ['_' for _ in range(len(snake.word))]
        snake.generate_field()
        listener.start()
        for i in range(len(snake.templates)):
            for j in range(len(snake.templates[i])):
                print(snake.templates[i][j])
        while snake.game == 'play':
            snake.direction_changed = False
            snake.move()
            if snake.game == 'play':
                update_world()
                time.sleep(1/fps)
        if snake.game == 'defeat':
            listener.stop()
            os.system('cls||clear')
            print('Загаданное слово:', snake.word)
            if input('Чел, ты лох, и ты проиграл. Можешь поплакать об этом, а можешь начать заново. Ну как? 0 - выйти, 1 - заново: ') == '1':
                snake.game = 'play'
            else:
                break
        elif snake.game == 'win':
            listener.stop()
            os.system('cls||clear')
            if ('Капец, ты выиграл! Можешь начать заново, а можешь пойти потрогать траву. 0 - выйти, 1 - заново:') == '1':
                snake.game = 'play'
            else:
                break
