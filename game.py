import tkinter
import math
from moveplanner import MovePlanner
from board import Board
from enums import Color


class Game:

    def __init__(self, tkinterRoot, width=500, height=500, fileWriter=None, board=None):
        self.root = tkinterRoot
        # na zmáčnkutí křížku zavolej metodu close
        self.root.protocol("WM_DELETE_WINDOW", self.close) #po zmáčknutí křížku se zavolá fce close
        self.width = width
        self.height = height
        self.fileWriter = fileWriter

        self.activePlayer = Color.BLACK #výchozí hráč

        # create canvas s vlastnostmi udanými v initu
        self.canvas = tkinter.Canvas(self.root, bg="white", height=height, width=width)

        if board == None: #pokud ještě neexistuje hrací pole, je zavolána fce pro vytvoření
            self.board = Board()
        else:
            self.board = board

        self.movePlanner = MovePlanner()
        self.shouldQuit = False #výchozí stav - okno se nezavře

    def close(self):
        self.shouldQuit = True
        self.root.destroy()  # odstraní widgety a ukončí běh kódu
        self.fileWriter.close() #ukončí se zapisovač do souboru

    def play(self):
        self.canvas.pack() #uspořádá hrací pole a tlačítka do bloků
        self.addEvents()
        self.draw()
        # je zde potřeba, aby se okno hned nezavřelo
        while not self.shouldQuit:
            self.root.update()

    def handleClick(self, ev):
        # pokud hráč vyhrál, není třeba nic dál dělat
        if self.board.hasAnyPlayerWon(): return

        mouseX = ev.x
        mouseY = ev.y

        if (not (self.isMouseWithinBorders(mouseX, mouseY))):
            return

        # zaokrouhlení myši na celé políčko
        mouseWidth = math.floor(mouseX / (self.width / 8))
        mouseHeight = math.floor(mouseY / (self.height / 8))

        fig = self.board.getFigureFromBoard(mouseWidth, mouseHeight)

        # posuneme figurku kde není figurka
        if (fig == None):
            self.moveFigure(mouseWidth, mouseHeight)
        else:
            # Ze začátku uložíme figurku a pak ji posuneme
            if (fig.color == self.activePlayer):
                self.movePlanner.saveFigure(fig)

        # přerendrování po kliknutí
        self.draw()

    def moveFigure(self, x, y):
        if self.movePlanner.moveSavedFigureSuccessful(self.board, x, y, self.fileWriter):
            self.togglePlayers()  # po úspěšném tahu je na řadě druhá barva a zapsán tah do csv

    # je potřeba dodělat možnost více tahů po sobě

    def togglePlayers(self):
        if (self.activePlayer == Color.BLACK):
            self.activePlayer = Color.WHITE
            return

        self.activePlayer = Color.BLACK

    def isMouseWithinBorders(self, mouseX, mouseY):
        return not (mouseX >= self.width and mouseY >= self.height and mouseX < 0 and mouseY < 0)

    def addEvents(self):
        self.root.bind('<Button-1>', self.handleClick)  # <Button-1> je levé tlačítko myši

    def checkWinner(self):
        countWhite, countBlack = self.board.countColors() #bere hodnoty z hasAnyPlayerWon z boardu

        if countBlack == 0:
            return "White won!"

        if countWhite == 0:
            return "Black won!"

        return ""

    def draw(self):
        self.board.draw(self.width, self.height, self.canvas)  # vykreslení grafiky hracího pole
        self.movePlanner.draw(self.board, self.width / 8, self.height / 8, self.canvas)  # vykreslení nabídky tahů

        winnerText = self.checkWinner()

        self.canvas.create_text(self.width / 2, self.height / 2, fill="darkblue", font="Times 40 italic bold",
                                text=winnerText)