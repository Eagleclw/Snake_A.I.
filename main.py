from json import dump, load
from game import *
from menu import *

main_menu = "Not initiated yet."
q_table = {}
game_data = {}
best_score = 0
score = 0
missed = 0
ai_best_score = 0
ai_trained_time = 0

def load_file():
    global game_data
    global best_score
    global q_table
    global score
    global missed
    global ai_best_score
    global ai_trained_time

    try:
        f = open('game_data.json')
        game_data = load(f)

        best_score = game_data["best_score"]
        score = game_data["score"]
        missed = game_data["missed"]
        ai_best_score = game_data["ai_best_score"]
        ai_trained_time = game_data["ai_trained_time"]
        q_table = game_data["q_table"]

        print("")
        print("------------------------------")
        print("Saved game data and trained AI loaded.")
        print("------------------------------")
        print("")
    except:
        print("")
        print("------------------------------")
        print("You don't have to required files to load saved game data and trained AI.")
        print("Creating a new game and a new AI.")
        print("------------------------------")
        print("")

def save_file():
    global game_data
    global best_score
    global q_table
    global score
    global missed
    global ai_best_score
    global ai_trained_time

    game_data = {"best_score": best_score,
                 "score": score,
                 "missed": missed,
                 "ai_best_score": ai_best_score,
                 "ai_trained_time": ai_trained_time,
                 "q_table": q_table}

    with open('game_data.json', 'w') as f:
        dump(game_data, f)

def main():
    global main_menu
    global best_score
    global q_table
    global score
    global missed
    global ai_best_score
    global ai_trained_time

    if main_menu == "Not initiated yet." or main_menu == "Deleted.":
        main_menu = Menu()
        if main_menu.state == "playTheGame" or main_menu.state == "trainTheAI":
            x = main_menu.state
            del main_menu
            main_menu = "Deleted."
            snake_game = Game(x, best_score, q_table, score, missed, ai_best_score, ai_trained_time)
            if snake_game.state == "gameClosed":
                if snake_game.BEST_SCORE > best_score:
                    best_score = snake_game.BEST_SCORE
                if x == "trainTheAI":
                    q_table = snake_game.ai_q_table
                    score = snake_game.ai_score
                    missed = snake_game.ai_missed
                    ai_best_score = snake_game.ai_best
                    ai_trained_time = snake_game.ai_trained_time

                del snake_game
        main()

if __name__ == '__main__':
    load_file()
    main()
    save_file()
