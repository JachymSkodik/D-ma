from boardsquare import BoardSquare
from enums import Color
from fig import Fig, Queen, SkippingFig
from moveplanner import MoveInfo
#vylepšit názvy fcí
#přidat konstanty nad funkce
class Board:
    def __init__ (self):
        #inicializace prázdné čtvercové matice 8x8, která bude obsahovat instance třídy BoardSquare
        self.board_squares = [[None for _ in range(8) ] for _ in range(8)]
        self.init_board_squares()
        self.init_figures()
    
    #zajišťuje střídání barev políček
    def init_board_squares (self):
        number_iterator = 0
        
        for y in range(0,8):
            for x in range(0,8):
                color = Color.WHITE
                if((number_iterator+y) % 2 == 0):
                    color = Color.BLACK
                
                self.board_squares[x][y] = BoardSquare(color,x,y)
                number_iterator += 1
    
    #nasází figurky na jejich počáteční pozici
    def init_figures (self):
        #míň přehledná verze, ale kód je kratší
        for i in range (0,7,2):
            for j in range(0,3,2):
                self.save_fig_to_board(Fig(i,j,Color.WHITE))
            self.save_fig_to_board(Fig(i,6,Color.BLACK))
        for i in range(1,8,2):
            for j in range(5,8,2):
                self.save_fig_to_board(Fig(i,j,Color.BLACK))
            self.save_fig_to_board(Fig(i,1,Color.WHITE))

    #uloží figurku na políčko        
    def save_fig_to_board(self,fig):
        self.board_squares[fig.positionX][fig.positionY].saveFig(fig)
        
    def save_none_to_board(self,x,y): #smazání figurky
        self.board_squares[x][y].saveFig(None)

    #vrátí souřadnice figurky
    def get_figure_from_board(self,x,y):
        return self.board_squares[x][y].fig

    def has_square_figure(self,x,y): #ověření, zda je na políčku figurka
        return Fig.arePositionsWithinBounds((x,y)) and self.board_squares[x][y].hasFig()

    #zjišťuje, kam může figurka táhnout
    def get_possible_figure_moves(self, fig):
        figure_move_set = fig.possibleMoves()
        moveset_accumulator = []

        #Byla tu primární snaha, neporovnávat všechno v závislosti na barvě
        for [posX,posY] in figure_move_set:
            #pokud políčko nemá figurku, tak daná figurka se může na to pole pohnout
            if(not self.has_square_figure(posX,posY)):
                moveInfo = MoveInfo(Fig(posX,posY,fig.color))
                moveset_accumulator.append(moveInfo)
                continue

            #Zde nemusíme kontrolovat None, protože s jistotou můžeme říci,
            #že na danné pozici se již nachází figurka (to nám zajišťuje předchozí podmínka)
            #Pokud se na pozici nachází figurka stejné barvy, tak ji nemůžeme přeskočit
            adjacent_fig = self.get_figure_from_board(posX,posY)
            if(adjacent_fig.color == fig.color):
                continue
                
            #vrátí souřadnice figurky, kterou můžeme přeskočit
            skipping_fig_pos_x = -1
            skipping_fig_pos_y = SkippingFig.fromFig(fig).moveBasedOnColor()
            
            if(fig.positionX > adjacent_fig.positionX):
                #skáčeme doleva
                skipping_fig_pos_x = fig.positionX - 2
            else:
                #skáčeme doprava
                skipping_fig_pos_x = fig.positionX + 2

            #kontrola, jestli máme před sebou figurku na přeskočení
            if(self.has_square_figure(skipping_fig_pos_x,skipping_fig_pos_y)):
                continue

            moveInfo = MoveInfo(SkippingFig(skipping_fig_pos_x,skipping_fig_pos_y,fig.color)) #zaznamená souřadnice figurky, která skákala
            moveInfo.setSkippedFigure(adjacent_fig) #nastaví figurku jako přeskočenou
            moveset_accumulator.append(moveInfo) #přidává možné tahy do seznamu

        return moveset_accumulator

    def is_move_figure_on_board_success(self, fromX,fromY, fig):
        #Musíme zjistit, zda-li je tah vůbec možný z počáteční pozice na novou 
        startFigure = self.get_figure_from_board(fromX,fromY)
        if(startFigure == None):
            return False
        
        #možné tahy se uloží do proměnné
        possibleMoves = self.get_possible_figure_moves(startFigure)

        #Zkontrolujeme, zda-li je možné se s figurkou na danou pozici posunout
        #A zároveň pokud figurka byla přeskočena
        isMovePossible = False
        skippedFigure = None
        
        #projíždíme možné tahy z moveset_accumulator
        for moveInfo in possibleMoves:

            #filtr možných tahů, když se označí figurka a vybere se tah, který nemůže provést, vrátí False
            #když nové políčko vybrané pro tah odpovídá omezením stanoveným pro figurku, vrátí True
            #proto se tah porovnává se stanovným pohybem figurky (moveBasedOnColor ve fig)
            #když se tento filtr odebere, figurka může táhnout na jakékoliv políčko
            isMovePossibleInMoveInfo = moveInfo.playedFigure.positionX == fig.positionX and moveInfo.playedFigure.positionY == fig.positionY

            #jestliže vybraný tah odpovídá omezením stanoveným pro figurku (když isMovePossibleInMoveInfo je True),
            #moveInfo se bude rovnat skippedFigure, tedy None
            #k moveset_accumulator se appenduje None
            if(isMovePossibleInMoveInfo):
                skippedFigure = moveInfo.skippedFigure

            # když je isMovePossible False, tak se rovná isMovePossibleInMoveInfo a spustí se filtr
            if (not isMovePossible):
                isMovePossible = isMovePossibleInMoveInfo

        #když filtr z for cyklu vrátí hodnotu False, tak tah není možný
        if(not isMovePossible):
            return False

        #Nemůžeme přesunout figurku, kde již existuje figurka
        if(self.board_squares[fig.positionX][fig.positionY].hasFig()):
            return False
        
        #když tah figurku dostane na druhou stranu hracího pole, přemění se na Dámu
        if fig.positionY == 7 or fig.positionY == 0:
            self.save_fig_to_board(Queen.queenFromFig(fig))
        else:
            self.save_fig_to_board(fig)

        self.save_none_to_board(fromX, fromY) #po tahu vymaže figurku z původní pozice

        #Smažeme přeskočenou figurku
        if(skippedFigure != None):
            self.save_none_to_board(skippedFigure.positionX, skippedFigure.positionY)

        #Tah byl úspěšný
        return True
    
    #prochází celé hrací pole a zaznamenává počet figurek každé barvy
    def count_colors(self):
        count_white = 0
        count_black = 0
        for y in range(0,8):
            for x in range(0,8):
                if(not self.board_squares[x][y].hasFig()):
                    continue
                
                color = self.board_squares[x][y].fig.color

                if(color == Color.WHITE):
                    count_white += 1
                else:
                    count_black += 1

        #vrátí počet bílých figurek a počet černých figurek
        return count_white, count_black

    #determinuje, jestli jeden z hráčů nevyhrál v závislosti na count_white a count_black
    #v game se vrátí oznámení, kdo vyhrál
    def has_any_player_won(self):
        count_white, count_black = self.count_colors()

        return count_white == 0 or count_black == 0

    #vykreslí hrací pole, přičemž políčka si bere z boardsquare a canvas si bere z game
    def draw(self,widthOfBoard,heightOfBoard,canvas):
        width = widthOfBoard/8
        height = heightOfBoard/8
        
        for y in range(0,8):
            for x in range(0,8):
                self.board_squares[x][y].draw(width,height,canvas)