from fig import Fig
from enums import Color

#vybírá možné tahy pro figurku
class MovePlanner:
    def __init__(self):
        self.figure = None

    #na poli musí být figurka, jinak vyhodí False
    def saveFigure(self, figure):
        assert(figure != None)
        self.figure = figure
        
    #zjistí, zda-li byl tah úspěšný, a vrátí novou pozici figurky
    def moveSavedFigureSuccessful(self, board, toX, toY, fileWriter):
        if (self.figure == None): #kontrola, jestli je figurka označena
            return False

        newFig = self.figure.copyFig() 
        newFig.positionX = toX
        newFig.positionY = toY

        #jestliže byl tah úspěšný, zapíše se barva a nová pozice figurky do zapisovače fileWriter
        if(board.isMoveFigureOnBoardSuccess(self.figure.positionX, self.figure.positionY, newFig)):
            fileWriter.write(f"{self.figure.toString()},{newFig.toString()},{ 'Black' if self.figure.color == Color.BLACK else 'White'}\n")
            self.figure = None #zruší označení políčka potom, co tah proběhl a byl zapsán do csv
            return True #tah byl úspěšný (v dalším kódu bude použito ke změně hráče, který je na tahu)
        return False #tah neproběhl, hráč je pořád na tahu
    
    #zvýrazní políčka, na které může figurka táhnout
    def draw(self, board, rectangleWidth, rectangleHeight, canvas):
        if(self.figure == None):
            return #když je políčko prázdné, nic nevrátí

        moveInfos = board.getPossibleFigureMoves(self.figure) #funkce z boardu, která načte možné tahy pro figurku do proměnné

        #každé políčko v možných tazích je zvýrazněno
        for moveInfo in moveInfos:
            fig = moveInfo.playedFigure
            canvas.create_rectangle(
                rectangleWidth*fig.positionX,
                rectangleHeight*fig.positionY,
                rectangleWidth*(fig.positionX + 1),
                rectangleHeight*(fig.positionY + 1),
                fill='white',
                stipple= 'gray50') #šrafování šedě

        #políčko s vybranou figurkou je označeno
        canvas.create_rectangle(
            rectangleWidth*self.figure.positionX,
            rectangleHeight*self.figure.positionY,
            rectangleWidth*(self.figure.positionX+1),
            rectangleHeight*(self.figure.positionY+1), 
            fill='blue',
            stipple= 'gray12')

#výsledky tahu (buď je  figurka stále ve hře, nebo je přeskočená)
class MoveInfo:
    def __init__(self, playedFigure):
        self.playedFigure = playedFigure 
        self.skippedFigure = None 

    def setSkippedFigure(self, skippedFigure):
        self.skippedFigure = skippedFigure
