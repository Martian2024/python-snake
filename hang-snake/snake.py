import os
import sys
import random
import time
from pynput import keyboard

class Snake:
    def __init__(self):
        self.direction = 'up'
        self.points = [[WIDTH // 2, HEIGHT // 2], [WIDTH // 2, HEIGHT // 2 + 1], [WIDTH // 2, HEIGHT // 2 + 1]]
        self.field = []
        self.game = 'play'
        self.direction_changed = False


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
        for i in range(len(self.field)):
            if self.field[i] == self.points[0]:
                flag = True
                self.field.pop(i)
                break
        if not flag:
            self.points.pop()

        if self.points[0][0] < 0 or self.points[0][1] < 0 or self.points[0][0] >= WIDTH or \
                self.points[0][1] >= HEIGHT or self.points.count(self.points[0]) == 2:
            self.game = 'defeat'
        elif len(self.points) == 100:
            self.game = 'win'


    def generate_field(self):
        for i in range(100):
            self.field.append([random.randint(0, WIDTH - 2), random.randint(0, HEIGHT - 2)])


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
    for i in snake.field:
        world[i[1]][i[0]] = '@'
    print(' ' * WIDTH)
    print(' ' + '_' * WIDTH)
    for i in snake.points[1:]:
        world[i[1]][i[0]] = '*'
    world[snake.points[0][1]][snake.points[0][0]] = '0'
    for i in range(len(world)):
        print('|' + ''.join(world[i][:-1]) + '|' + world[i][-1])
    print(' ' + '¯' * WIDTH)


if __name__ == '__main__':
    WIDTH = 50
    HEIGHT = 30
    os.system(f"mode con cols={WIDTH + 50} lines={HEIGHT + 3}")
    fps = 5
    while True:
        snake = Snake()
        listener = keyboard.Listener(on_press=on_press, suppress=False)
        listener.start()
        snake.generate_field()
        while snake.game == 'play':
            snake.direction_changed = False
            snake.move()
            if snake.game == 'play':
                update_world()
                time.sleep(1/fps)
        if snake.game == 'defeat':
            listener.stop()
            os.system('cls||clear')
            if input('Чел, ты лох, и ты проиграл. Можешь поплакать об этом, а можешь начать заново. Ну как? 0 - выйти, 1 - заново: ') == '1':
                snake.game = 'play'
            else:
                break
        elif snake.game == 'win':
            listener.stop()
            os.system('cls||clear')
            if input('Капец, ты выиграл! Можешь начать заново, а можешь пойти потрогать траву. 0 - выйти, 1 - заново:') == '1':
                snake.game = 'play'
            else:
                break