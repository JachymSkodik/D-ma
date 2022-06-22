import tkinter
from enums import Color

class BoardSquare:
    def __init__ (self, color, position_x, position_y):
        self.fig = None
        self.color = color
        self.position_x = position_x
        self.position_y = position_y
     
    def has_fig(self): #ověření prázdnosti políčka
        return self.fig != None
    
    def save_fig(self, new_fig):
        if(self.has_fig() and new_fig != None):
            raise Exception("Can't save figure to square which contains figure: ", self.fig, new_fig)
        else:
            self.fig = new_fig #když je políčko prázdné, figurka se uloží
        
    def draw(self, rectangle_width, rectangle_height, canvas):
    
        rectangle_fill = 'pink'  #střídání barev
        if(self.color == Color.BLACK):
            rectangle_fill = 'brown'
    
        #vytvoření čtverce pro políčka, jako parametry souřadnice rohů
        canvas.create_rectangle(
            rectangle_width*self.position_x,
            rectangle_height*self.position_y,
            rectangle_width*(self.position_x+1),
            rectangle_height*(self.position_y+1),
            fill = rectangle_fill) #vyplnění barvou
        
        if(self.has_fig()):
            self.fig.draw(rectangle_width, rectangle_height, canvas)
