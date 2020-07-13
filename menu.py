from tkinter import Tk, Frame, BOTH, Button

class Menu:
    def __init__(self):
        self.window = Tk()
        self.state = "inMenu"
        self.main()

    def on_closing(self):
        self.window.destroy()
        del self

    def __del__(self):
        pass

    def playTheGame(self):
        self.state = "playTheGame"
        self.on_closing()

    def trainTheAI(self):
        self.state = "trainTheAI"
        self.on_closing()

    def setup_menu(self):
        self.window.focus_force()
        frame = Frame(self.window)
        window_width, window_height = (400, 200)
        ''' window_width, window_height --> Width and height of window. '''
        screen_width, screen_height = (self.window.winfo_screenwidth(), self.window.winfo_screenheight())
        ''' screen_width, screen_height --> Width and height of screen. '''
        x_coordinate, y_coordinate = (int((screen_width / 2) - (window_width / 2)),
                                      int((screen_height / 2) - (window_height / 2)))
        ''' x_coordinate, y_coordinate --> The starting points of window. '''

        self.window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
        self.window.resizable(False, False)

        frame.master.title("Snake Game - Menu")
        frame.pack(fill=BOTH, expand=1)

        B1 = Button(frame, text="Play The Game", command=self.playTheGame)
        B1.pack(fill=BOTH, expand=True)
        B2 = Button(frame, text="Train The AI", command=self.trainTheAI)
        B2.pack(fill=BOTH, expand=True)

    def main(self):
        self.setup_menu()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()
