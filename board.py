from boardsquare import BoardSquare
from enums import Color
from fig import Fig, Queen, SkippingFig
from moveplanner import MoveInfo

class Board:
    def __init__ (self):
        #inicializace prázdné čtvercové matice 8x8, která bude obsahovat instance třídy BoardSquare
        self.boardSquares = [[None for _ in range(8) ] for _ in range(8)]
        self.initBoardSquares()
        self.initFigures()
    
    #zajišťuje střídání barev políček
    def initBoardSquares (self):
        numberIterator = 0
        
        for y in range(0,8):
            for x in range(0,8):
                color = Color.WHITE
                if((numberIterator+y) % 2 == 0):
                    color = Color.BLACK
                
                self.boardSquares[x][y] = BoardSquare(color,x,y)
                numberIterator += 1
    
    #nasází figurky na jejich počáteční pozici
    def initFigures (self):
        #míň přehledná verze, ale kód je kratší
        for i in range (0,7,2):
            for j in range(0,3,2):
                self.saveFigToBoard(Fig(i,j,Color.WHITE))
            self.saveFigToBoard(Fig(i,6,Color.BLACK))
        for i in range(1,8,2):
            for j in range(5,8,2):
                self.saveFigToBoard(Fig(i,j,Color.BLACK))
            self.saveFigToBoard(Fig(i,1,Color.WHITE))

    #uloží figurku na políčko        
    def saveFigToBoard(self,fig):
        self.boardSquares[fig.positionX][fig.positionY].saveFig(fig)
        
    def saveNoneToBoard(self,x,y): #smazání figurky
        self.boardSquares[x][y].saveFig(None)

    #vrátí souřadnice figurky
    def getFigureFromBoard(self,x,y):
        return self.boardSquares[x][y].fig

    def hasSquareFigure(self,x,y): #ověření, zda je na políčku figurka
        return Fig.arePositionsWithinBounds((x,y)) and self.boardSquares[x][y].hasFig()

    #zjišťuje, kam může figurka táhnout
    def getPossibleFigureMoves(self, fig):
        figureMoveSet = fig.possibleMoves()
        movesetAccumulator = [] 

        #Byla tu primární snaha, neporovnávat všechno v závislosti na barvě
        for [posX,posY] in figureMoveSet:
            #pokud políčko nemá figurku, tak daná figurka se může na to pole pohnout
            if(not self.hasSquareFigure(posX,posY)):
                moveInfo = MoveInfo(Fig(posX,posY,fig.color))
                movesetAccumulator.append(moveInfo)
                continue

            #Zde nemusíme kontrolovat None, protože s jistotou můžeme říci,
            #že na danné pozici se již nachází figurka (to nám zajišťuje předchozí podmínka)
            #Pokud se na pozici nachází figurka stejné barvy, tak ji nemůžeme přeskočit
            adjacentFig = self.getFigureFromBoard(posX,posY)
            if(adjacentFig.color == fig.color):
                continue
                
            #vrátí souřadnice figurky, kterou můžeme přeskočit
            skippingFigPosX = -1
            skippingFigPosY = SkippingFig.fromFig(fig).moveBasedOnColor()
            
            if(fig.positionX > adjacentFig.positionX):
                #skáčeme doleva
                skippingFigPosX = fig.positionX - 2
            else:
                #skáčeme doprava
                skippingFigPosX = fig.positionX + 2

            #kontrola, jestli máme před sebou figurku na přeskočení
            if(self.hasSquareFigure(skippingFigPosX,skippingFigPosY)):
                continue

            moveInfo = MoveInfo(SkippingFig(skippingFigPosX,skippingFigPosY,fig.color)) #zaznamená souřadnice figurky, která skákala
            moveInfo.setSkippedFigure(adjacentFig) #nastaví figurku jako přeskočenou
            movesetAccumulator.append(moveInfo) #přidává možné tahy do seznamu

        return movesetAccumulator

    def isMoveFigureOnBoardSuccess(self, fromX,fromY, fig):
        #Musíme zjistit, zda-li je tah vůbec možný z počáteční pozice na novou 
        startFigure = self.getFigureFromBoard(fromX,fromY)
        if(startFigure == None):
            return False
        
        #možné tahy se uloží do proměnné
        possibleMoves = self.getPossibleFigureMoves(startFigure) 

        #Zkontrolujeme, zda-li je možné se s figurkou na danou pozici posunout
        #A zároveň pokud figurka byla přeskočena
        isMovePossible = False
        skippedFigure = None
        
        #projíždíme možné tahy z movesetAccumulator
        for moveInfo in possibleMoves:

            #filtr možných tahů, když se označí figurka a vybere se tah, který nemůže provést, vrátí False
            #když nové políčko vybrané pro tah odpovídá omezením stanoveným pro figurku, vrátí True
            #proto se tah porovnává se stanovným pohybem figurky (moveBasedOnColor ve fig)
            #když se tento filtr odebere, figurka může táhnout na jakékoliv políčko
            isMovePossibleInMoveInfo = moveInfo.playedFigure.positionX == fig.positionX and moveInfo.playedFigure.positionY == fig.positionY

            #jestliže vybraný tah odpovídá omezením stanoveným pro figurku (když isMovePossibleInMoveInfo je True),
            #moveInfo se bude rovnat skippedFigure, tedy None
            #k movesetAccumulator se appenduje None
            if(isMovePossibleInMoveInfo):
                skippedFigure = moveInfo.skippedFigure

            # když je isMovePossible False, tak se rovná isMovePossibleInMoveInfo a spustí se filtr
            if (not isMovePossible):
                isMovePossible = isMovePossibleInMoveInfo

        #když filtr z for cyklu vrátí hodnotu False, tak tah není možný
        if(not isMovePossible):
            return False

        #Nemůžeme přesunout figurku, kde již existuje figurka
        if(self.boardSquares[fig.positionX][fig.positionY].hasFig()):
            return False
        
        #když tah figurku dostane na druhou stranu hracího pole, přemění se na Dámu
        if fig.positionY == 7 or fig.positionY == 0:
            self.saveFigToBoard(Queen.queenFromFig(fig))
        else:
            self.saveFigToBoard(fig)

        self.saveNoneToBoard(fromX, fromY) #po tahu vymaže figurku z původní pozice

        #Smažeme přeskočenou figurku
        if(skippedFigure != None):
            self.saveNoneToBoard(skippedFigure.positionX, skippedFigure.positionY)

        #Tah byl úspěšný
        return True
    
    #prochází celé hrací pole a zaznamenává počet figurek každé barvy
    def countColors(self):
        countWhite = 0
        countBlack = 0
        for y in range(0,8):
            for x in range(0,8):
                if(not self.boardSquares[x][y].hasFig()):
                    continue
                
                color = self.boardSquares[x][y].fig.color

                if(color == Color.WHITE):
                    countWhite += 1
                else:
                    countBlack += 1

        #vrátí počet bílých figurek a počet černých figurek
        return countWhite, countBlack

    #determinuje, jestli jeden z hráčů nevyhrál v závislosti na countWhite a countBlack
    #v game se vrátí oznámení, kdo vyhrál
    def hasAnyPlayerWon(self):
        countWhite, countBlack = self.countColors()

        return countWhite == 0 or countBlack == 0

    #vykreslí hrací pole, přičemž políčka si bere z boardsquare a canvas si bere z game
    def draw(self,widthOfBoard,heightOfBoard,canvas):
        width = widthOfBoard/8
        height = heightOfBoard/8
        
        for y in range(0,8):
            for x in range(0,8):
                self.boardSquares[x][y].draw(width,height,canvas)