from random import uniform
from math import floor

class AI:
    def __init__(self, data):
        print("AI Created.")
        print("-----")
        self.snake_game = data

        self.qTable = {}
        self.learningRate = 0.85
        self.discountFactor = 0.9
        self.randomize = 0.05

        self.availableActions = ['Up', 'Down', 'Left', 'Right']

        self.score = 0
        self.missed = 0

        self.intervalID = None
        self.speed = self.snake_game.game['speed']

    def on_closing(self):
        del self

    def __del__(self):
        print("-----")
        print("AI Closed.")
        print("---------------")

    def save_informations(self):
        self.snake_game.ai_q_table = self.qTable
        self.snake_game.ai_score = self.score
        self.snake_game.ai_missed = self.missed

    def whichStateNow(self):
        tileCount = self.snake_game.X
        player = self.snake_game.game['snake'][-1]
        fruit = self.snake_game.game['food']
        fruitRelativePose = [0, 0]
        trail = self.snake_game.game['snake']
        trailRelativePose = []

        fruitRelativePose[0] = fruit[0] - player[0]
        while fruitRelativePose[0] < 0:
            fruitRelativePose[0] += tileCount
        while fruitRelativePose[0] > tileCount:
            fruitRelativePose[0] -= tileCount

        fruitRelativePose[1] = fruit[1] - player[1]
        while fruitRelativePose[1] < 0:
            fruitRelativePose[1] += tileCount
        while fruitRelativePose[1] > tileCount:
            fruitRelativePose[1] -= tileCount

        stateName = str(fruitRelativePose[0]) + "," + str(fruitRelativePose[1])

        if len(trailRelativePose) == 0:
            trailRelativePose.append([0, 0])

        trailRelativePose[0][0] = trail[1][0] - player[0]
        while trailRelativePose[0][0] < 0:
            trailRelativePose[0][0] += tileCount
        while trailRelativePose[0][0] > tileCount:
            trailRelativePose[0][0] -= tileCount

        trailRelativePose[0][1] = trail[1][1] - player[1]
        while trailRelativePose[0][1] < 0:
            trailRelativePose[0][1] += tileCount
        while trailRelativePose[0][1] > tileCount:
            trailRelativePose[0][1] -= tileCount

        stateName += ',' + str(trailRelativePose[0][0]) + ',' + str(trailRelativePose[0][1])

        return stateName

    def whichTable(self, s):
        if s not in self.qTable:
            self.qTable[s] = {'Up': 0, 'Down': 0, 'Left': 0, 'Right': 0}

        return self.qTable[s]

    def bestAction(self, s):
        q = self.whichTable(s)

        if uniform(0, 1) < self.randomize:
            random = floor(uniform(0, 1) * len(self.availableActions))
            return self.availableActions[random]

        maxValue = q[self.availableActions[0]]
        choseAction = self.availableActions[0]
        actionsZero = []

        for i in range(0, len(self.availableActions)):
            if q[self.availableActions[i]] == 0:
                actionsZero.append(self.availableActions[i])
            if q[self.availableActions[i]] > maxValue:
                maxValue = q[self.availableActions[i]]
                choseAction = self.availableActions[i]

        if maxValue == 0:
            random = floor(uniform(0, 1) * len(actionsZero))
            choseAction = actionsZero[random]

        return choseAction

    def updateQTable(self, state0, state1, reward, act):
        q0 = self.whichTable(state0)
        q1 = self.whichTable(state1)

        newValue = reward + self.discountFactor * max(q1['Up'], q1['Down'], q1['Left'], q1['Right']) - q0[act]
        self.qTable[state0][act] = q0[act] + self.learningRate * newValue
