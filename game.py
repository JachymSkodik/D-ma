import tkinter
import math
from moveplanner import MovePlanner
from board import Board
from enums import Color


class Game:

    def __init__(self, tkinterRoot, width=500, height=500, file_writer=None, board=None):
        self.root = tkinterRoot
        # na zmáčnkutí křížku zavolej metodu close
        self.root.protocol("WM_DELETE_WINDOW", self.close) #po zmáčknutí křížku se zavolá fce close
        self.width = width
        self.height = height
        self.file_writer = file_writer

        self.active_player = Color.BLACK #výchozí hráč

        # create canvas s vlastnostmi udanými v initu
        self.canvas = tkinter.Canvas(self.root, bg="white", height=height, width=width)

        if board == None: #pokud ještě neexistuje hrací pole, je zavolána fce pro vytvoření
            self.board = Board()
        else:
            self.board = board

        self.move_planner = MovePlanner()
        self.should_quit = False #výchozí stav - okno se nezavře

    def close(self):
        self.should_quit = True
        self.root.destroy()  # odstraní widgety a ukončí běh kódu
        self.file_writer.close() #ukončí se zapisovač do souboru

    def play(self):
        self.canvas.pack() #uspořádá hrací pole a tlačítka do bloků
        self.add_events()
        self.draw()
        # je zde potřeba, aby se okno hned nezavřelo
        while not self.should_quit:
            self.root.update()

    def handle_click(self, ev):
        # pokud hráč vyhrál, není třeba nic dál dělat
        if self.board.has_any_player_won(): return

        mouse_x = ev.x
        mouse_y = ev.y

        if (not (self.is_mouse_within_borders(mouse_x, mouse_y))):
            return

        # zaokrouhlení myši na celé políčko
        mouse_width = math.floor(mouse_x / (self.width / 8))
        mouse_height = math.floor(mouse_y / (self.height / 8))

        fig = self.board.get_figure_from_board(mouse_width, mouse_height)

        # posuneme figurku kde není figurka
        if (fig == None):
            self.move_figure(mouse_width, mouse_height)
        else:
            # Ze začátku uložíme figurku a pak ji posuneme
            if (fig.color == self.active_player):
                self.move_planner.save_figure(fig)

        # přerendrování po kliknutí
        self.draw()

    def move_figure(self, x, y):
        if self.move_planner.move_saved_figure_successful(self.board, x, y, self.file_writer):
            self.toggle_players()  # po úspěšném tahu je na řadě druhá barva a zapsán tah do csv

    # je potřeba dodělat možnost více tahů po sobě

    def toggle_players(self):
        if (self.active_player == Color.BLACK):
            self.active_player = Color.WHITE
            return

        self.active_player = Color.BLACK

    def is_mouse_within_borders(self, mouse_x, mouse_y):
        return not (mouse_x >= self.width and mouse_y >= self.height and mouse_x < 0 and mouse_y < 0)

    def add_events(self):
        self.root.bind('<Button-1>', self.handle_click)  # <Button-1> je levé tlačítko myši

    def check_winner(self):
        count_white, count_black = self.board.count_colors() #bere hodnoty z has_any_player_won z boardu

        if count_black == 0:
            return "White won!"

        if count_white == 0:
            return "Black won!"

        return ""

    def draw(self):
        self.board.draw(self.width, self.height, self.canvas)  # vykreslení grafiky hracího pole
        self.move_planner.draw(self.board, self.width / 8, self.height / 8, self.canvas)  # vykreslení nabídky tahů

        winner_text = self.check_winner()

        self.canvas.create_text(self.width / 2, self.height / 2, fill="darkblue", font="Times 40 italic bold",
                                text=winner_text)