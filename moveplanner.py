from fig import Fig
from enums import Color

#vybírá možné tahy pro figurku
class MovePlanner:
    def __init__(self):
        self.figure = None

    #na poli musí být figurka, jinak vyhodí False
    def save_figure(self, figure):
        assert(figure != None)
        self.figure = figure
        
    #zjistí, zda-li byl tah úspěšný, a vrátí novou pozici figurky
    def move_saved_figure_successful(self, board, to_x, to_y, file_writer):
        if (self.figure == None): #kontrola, jestli je figurka označena
            return False

        new_fig = self.figure.copy_fig() 
        new_fig.position_x = to_x
        new_fig.position_y = to_y

        #jestliže byl tah úspěšný, zapíše se barva a nová pozice figurky do zapisovače file_writer
        if(board.is_move_figure_on_board_success(self.figure.position_x, self.figure.position_y, new_fig)):
            file_writer.write(f"{self.figure.to_string()},{new_fig.to_string()},{ 'Black' if self.figure.color == Color.BLACK else 'White'}\n")
            self.figure = None #zruší označení políčka potom, co tah proběhl a byl zapsán do csv
            return True #tah byl úspěšný (v dalším kódu bude použito ke změně hráče, který je na tahu)
        return False #tah neproběhl, hráč je pořád na tahu
    
    #zvýrazní políčka, na které může figurka táhnout
    def draw(self, board, rectangle_width, rectangle_height, canvas):
        if(self.figure == None):
            return #když je políčko prázdné, nic nevrátí

        move_infos = board.get_possible_figure_moves(self.figure) #funkce z boardu, která načte možné tahy pro figurku do proměnné

        #každé políčko v možných tazích je zvýrazněno
        for move_info in move_infos:
            fig = move_info.played_figure
            canvas.create_rectangle(
                rectangle_width*fig.position_x,
                rectangle_height*fig.position_y,
                rectangle_width*(fig.position_x + 1),
                rectangle_height*(fig.position_y + 1),
                fill='white',
                stipple= 'gray50') #šrafování šedě

        #políčko s vybranou figurkou je označeno
        canvas.create_rectangle(
            rectangle_width*self.figure.position_x,
            rectangle_height*self.figure.position_y,
            rectangle_width*(self.figure.position_x+1),
            rectangle_height*(self.figure.position_y+1), 
            fill='blue',
            stipple= 'gray12')

#výsledky tahu (buď je  figurka stále ve hře, nebo je přeskočená)
class MoveInfo:
    def __init__(self, played_figure):
        self.played_figure = played_figure 
        self.skipped_figure = None 

    def set_skipped_figure(self, skipped_figure):
        self.skipped_figure = skipped_figure
