from collections import deque
from math import trunc
from tkinter import Tk, Canvas, Frame, BOTH, messagebox
from ai import *
from random import randint
from time import time

class Game:
    def __init__(self, data, best_score, q_table, score, missed, ai_best_score, ai_trained_time):
        self.window = Tk()
        self.frame = Frame(self.window)
        self.canvas = Canvas(self.frame)
        self.state = "gameRunning"
        self.run_type = data
        self.ai_q_table = q_table
        self.ai_score = score
        self.ai_missed = missed
        self.ai_best = ai_best_score
        self.play_speed = 10
        self.train_speed = 1000000000
        self.ai_trained_time = ai_trained_time
        self.ai_timer = time()

        # AI Observer
        self.ai_observer_key = ""
        # AI Observer

        print("")
        print("------------------------------")
        if self.run_type == "playTheGame":
            print("Game Created for player to play.")
        elif self.run_type == "trainTheAI":
            print("Game Created for AI to train.")
        print("---------------")

        self.X, self.Y = (10, 10)
        ''' X, Y --> Count of blocks in window. '''
        self.BLOCK_SIZE = 75
        ''' BLOCK_SIZE --> Size of one block. '''

        self.BACKGROUND_COLOR = '#303030'
        self.SNAKE_COLOR = '#0f0'
        self.SNAKE_HEAD_COLOR = '#003300'
        self.FOOD_COLOR = '#f00'
        self.INITIAL_SPEED = 10
        self.BEST_SCORE = best_score
        self.PAUSED = 0

        self.KEY_LEFT = 'Left'
        self.KEY_RIGHT = 'Right'
        self.KEY_UP = 'Up'
        self.KEY_DOWN = 'Down'
        self.KEY_QUIT = 'q'
        self.KEY_PAUSE = 'p'
        self.KEY_SPEED = 's'

        self.VALID_DIRECTIONS = {
            self.KEY_LEFT: {self.KEY_LEFT, self.KEY_UP, self.KEY_DOWN},
            self.KEY_RIGHT: {self.KEY_RIGHT, self.KEY_UP, self.KEY_DOWN},
            self.KEY_UP: {self.KEY_UP, self.KEY_LEFT, self.KEY_RIGHT},
            self.KEY_DOWN: {self.KEY_DOWN, self.KEY_LEFT, self.KEY_RIGHT}
        }

        self.MOVEMENTS = {
            self.KEY_LEFT: lambda x, y: (x - 1, y),
            self.KEY_RIGHT: lambda x, y: (x + 1, y),
            self.KEY_UP: lambda x, y: (x, y - 1),
            self.KEY_DOWN: lambda x, y: (x, y + 1)
        }

        self.INITIAL_SPEED = self.play_speed

        self.game = self.create_game()
        self.snake_ai = None
        self.avg_score = 0
        self.ai_current_score = 0
        self.ai_gen = 1
        self.reward = 0
        self.tickID = None
        self.main()

    def on_closing(self):
        if self.ai_current_score > 0:
            self.snake_ai.score -= self.ai_current_score
        self.window.after_cancel(self.tickID)
        self.window.destroy()
        self.state = "gameClosed"

        self.snake_ai.save_informations()
        del self.snake_ai

    def __del__(self):
        if self.run_type == "playTheGame":
            print("---------------")
        print("Game Closed.")
        print("------------------------------")
        print("")

    def save_informations(self):
        pass

    def setup_game(self):
        self.window.focus_force()
        window_width, window_height = (self.X * self.BLOCK_SIZE, self.Y * self.BLOCK_SIZE)
        ''' window_width, window_height --> Width and height of window. '''
        screen_width, screen_height = (self.window.winfo_screenwidth(), self.window.winfo_screenheight())
        ''' screen_width, screen_height --> Width and height of screen. '''
        x_coordinate, y_coordinate = (int((screen_width / 2) - (window_width / 2)),
                                      int((screen_height / 2) - (window_height / 2)))
        ''' x_coordinate, y_coordinate --> The starting points of window. '''

        self.window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
        self.window.resizable(False, False)

        self.frame.master.title("Snake Game   |   SCORE : 0   |   Best Score : 0    |   Best AI Score : 0 ")
        self.frame.pack(fill=BOTH, expand=1)
        self.canvas.pack(fill=BOTH, expand=1)

    def create_game(self):
        snake_randX = randint(0, self.X - 1)
        snake_randY = randint(0, self.Y - 1)

        direction_selector = randint(0, len(self.VALID_DIRECTIONS) - 1)

        food_randX = randint(0, self.X - 1)
        food_randY = randint(0, self.Y - 1)
        while (food_randX, food_randY) == (snake_randX, snake_randY):
            food_randX = randint(0, self.X - 1)
            food_randY = randint(0, self.Y - 1)

        # AI Observer
        self.ai_observer_key = list(self.VALID_DIRECTIONS.keys())[direction_selector]
        # AI Observer

        return {
            'snake': deque(((snake_randX, snake_randY), (snake_randX, snake_randY))),
            'food': (food_randX, food_randY),
            'direction': list(self.VALID_DIRECTIONS.keys())[direction_selector],
            'moves': deque(),
            'points': 0,
            'speed': self.INITIAL_SPEED
        }

    def reset(self):
        current_speed = self.game['speed']
        self.game = self.create_game()
        self.game['speed'] = current_speed

    def message_box(self, subject, content):
        root = Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        messagebox.showinfo(subject, content)
        try:
            root.destroy()
        except:
            pass

    def draw_rect(self, x, y, color=None):
        if color is None:
            color = self.SNAKE_COLOR
        x1 = x * self.BLOCK_SIZE
        y1 = y * self.BLOCK_SIZE
        x2 = x1 + self.BLOCK_SIZE
        y2 = y1 + self.BLOCK_SIZE
        return self.canvas.create_rectangle(x1, y1, x2, y2, outline='', fill=color)

    def render(self):
        self.canvas.delete('all')
        self.canvas.configure(background=self.BACKGROUND_COLOR)

        for i in range((len(self.game['snake']) - 1), 0, -1):
            if i == (len(self.game['snake']) - 1):
                self.draw_rect(self.game['snake'][i][0], self.game['snake'][i][1], self.SNAKE_HEAD_COLOR)
            else:
                self.draw_rect(self.game['snake'][i][0], self.game['snake'][i][1])

        x, y = self.game['food']
        self.draw_rect(x, y, color=self.FOOD_COLOR)

    def gen_food(self, snake):
        while True:
            food = randint(0, self.X - 1), randint(0, self.Y - 1)
            if food not in snake:
                return food

    def eat(self, snake):
        self.game['food'] = self.gen_food(snake)
        self.game['points'] += 1

        if self.run_type == "trainTheAI":
            self.reward = 1
            self.ai_current_score += 1

            if self.ai_current_score > self.ai_best:
                self.ai_best = self.ai_current_score

        if self.run_type == "playTheGame":
            if self.game['points'] > self.BEST_SCORE:
                self.BEST_SCORE = self.game['points']

            # AI Observer
            self.reward = 1
            # AI Observer

    def move_snake(self, direction):
        snake = set(self.game['snake'])
        u, w = self.game['snake'][-1]
        next_point = self.MOVEMENTS[direction](u, w)

        x, y = next_point

        if x < 0:
            x = x + self.X
        if x >= self.X:
            x = x - self.X
        if y < 0:
            y = y + self.Y
        if y >= self.Y:
            y = y - self.Y

        next_point = x, y

        if next_point == self.game['food'] or self.game['snake'][-1] == self.game['food']:
            self.eat(snake)
        else:
            self.game['snake'].popleft()
            self.reward = - 0.1

        self.frame.master.title("Snake Game   |   SCORE : " + str(self.game['points']) +
                                "   |   Best Score : " + str(self.BEST_SCORE) +
                                "   |   Best AI Score : " + str(self.ai_best))

        in_snake = 0

        if len(self.game['snake']) > 1:
            for i in range(1, len(self.game['snake'])):
                if next_point == self.game['snake'][i]:
                    in_snake = 1

            if in_snake == 1:
                if self.run_type == "playTheGame":
                    self.message_box('You Lost!', 'Play again...')
                    print("Player Score: " + str(self.game['points']) +
                          "   |   Best Player Score: " + str(self.BEST_SCORE))

                    # AI Observer
                    self.reward = -1
                    # AI Observer

                if self.run_type == "trainTheAI":
                    if self.snake_ai.missed != 0:
                        self.ai_gen = abs(self.snake_ai.missed) + 1
                    if self.ai_current_score != 0 and self.ai_gen != 0:
                        self.avg_score = self.snake_ai.score / self.ai_gen

                    ai_training_time = time() - self.ai_timer
                    self.ai_trained_time = ai_training_time

                    ai_training_time_seconds = int((ai_training_time % 3600) % 60)
                    ai_training_time_minutes = int(((ai_training_time - ai_training_time_seconds) % 3600) / 60)
                    ai_training_time_hours = int((ai_training_time - 60 * ai_training_time_minutes -
                                                  ai_training_time_seconds) / 3600)

                    hours = str(ai_training_time_hours)
                    if ai_training_time_hours < 10:
                        hours = "0" + str(ai_training_time_hours)

                    minutes = str(ai_training_time_minutes)
                    if ai_training_time_minutes < 10:
                        minutes = "0" + str(ai_training_time_minutes)

                    seconds = str(ai_training_time_seconds)
                    if ai_training_time_seconds < 10:
                        seconds = "0" + str(ai_training_time_seconds)

                    fixed_ai_gen = ""
                    while len(fixed_ai_gen) < 7 - len(str(self.ai_gen)):
                        fixed_ai_gen += "0"
                    fixed_ai_gen += str(self.ai_gen)

                    fixed_ai_current_score = ""
                    while len(fixed_ai_current_score) < 7 - len(str(self.ai_current_score)):
                        fixed_ai_current_score += "0"
                    fixed_ai_current_score += str(self.ai_current_score)

                    fixed_ai_best = ""
                    while len(fixed_ai_best) < 7 - len(str(self.ai_best)):
                        fixed_ai_best += "0"
                    fixed_ai_best += str(self.ai_best)

                    fixed_avg_score = str(self.avg_score)
                    if len(fixed_avg_score) > 7:
                        fixed_avg_score = str(self.avg_score)[:7]
                    else:
                        while len(fixed_avg_score) < 7:
                            fixed_avg_score += "0"

                    print("AI Training Time: " + hours + ":" + minutes + ":" + seconds +
                          "   |   AI Generation: " + fixed_ai_gen +
                          "   |   AI Current Score: " + fixed_ai_current_score +
                          "   |   AI Best Score: " + fixed_ai_best +
                          "   |   AI Average Score: " + fixed_avg_score)
                    self.reward = -1
                    self.ai_current_score = 0
                self.reset()
            else:
                self.game['snake'].append(next_point)
        else:
            self.game['snake'].append(next_point)

    def handle_next_movement(self):
        direction = self.game['moves'].popleft() if self.game['moves'] else self.game['direction']
        self.game['direction'] = direction
        self.move_snake(direction)

    def on_press(self, event):
        key = event.keysym
        if self.PAUSED == 0 and self.run_type == "playTheGame":
            prev_direction = self.game['moves'][-1] if self.game['moves'] else self.game['direction']
            if key in self.VALID_DIRECTIONS[prev_direction]:
                self.game['moves'].append(key)

            # AI Observer
            self.ai_observer_key = key
            # AI Observer

        if self.run_type == "trainTheAI":
            if key.lower() == self.KEY_SPEED:
                if self.game['speed'] == self.play_speed:
                    self.game['speed'] = self.train_speed
                else:
                    self.game['speed'] = self.play_speed
        if key.lower() == self.KEY_QUIT:
            self.on_closing()
        elif key.lower() == self.KEY_PAUSE:
            if self.PAUSED == 0:
                self.PAUSED = 1
                self.frame.master.title("Snake Game   |   PAUSED.")
            else:
                self.PAUSED = 0
                self.frame.master.title("Snake Game   |   SCORE : " + str(self.game['points']) +
                                        "   |   Best Score : " + str(self.BEST_SCORE) +
                                        "   |   Best AI Score : " + str(self.ai_best))

    def tick(self):
        if self.PAUSED == 0:
            if self.run_type == "playTheGame":
                # AI Observer
                currentState = self.snake_ai.whichStateNow()
                key = self.ai_observer_key
                # AI Observer
                self.handle_next_movement()
                self.render()

                # AI Observer
                instantReward = self.reward
                nextState = self.snake_ai.whichStateNow()
                if key == "Left" or key == "Right" or key == "Up" or key == "Down":
                    self.snake_ai.updateQTable(currentState, nextState, instantReward, key)
                # AI Observer

            elif self.run_type == "trainTheAI":
                self.Algorithm()

        self.tickID = self.window.after(int(1000 / self.game['speed']), self.tick)

    def Algorithm(self):
        currentState = self.snake_ai.whichStateNow()
        key = self.snake_ai.bestAction(currentState)
        prev_direction = self.game['moves'][-1] if self.game['moves'] else self.game['direction']
        if key in self.VALID_DIRECTIONS[prev_direction]:
            self.game['moves'].append(key)

        self.handle_next_movement()
        self.render()

        instantReward = self.reward
        nextState = self.snake_ai.whichStateNow()
        self.snake_ai.updateQTable(currentState, nextState, instantReward, key)

        if instantReward > 0:
            self.snake_ai.score += trunc(instantReward)
        if instantReward < 0:
            self.snake_ai.missed += trunc(instantReward)

    def main(self):
        self.setup_game()
        if self.run_type == "trainTheAI":
            self.snake_ai = AI(self)
            self.snake_ai.qTable = self.ai_q_table
            self.snake_ai.score = self.ai_score
            self.snake_ai.missed = self.ai_missed
            self.ai_timer = time() - self.ai_trained_time
        else:
            self.snake_ai = AI(self)
            self.snake_ai.qTable = self.ai_q_table
        self.tick()
        self.window.bind('<Key>', self.on_press)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()
