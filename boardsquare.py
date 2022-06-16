import tkinter
from enums import Color

class BoardSquare:
    def __init__ (self,color,positionX,positionY):
        self.fig= None
        self.color = color
        self.positionX = positionX
        self.positionY = positionY
     
    def hasFig(self): #ověření prázdnosti políčka
        return self.fig != None
    
    def saveFig(self,newFig):
        if(self.hasFig() and newFig != None):  
            raise Exception("Can't save figure to square which contains figure: ", self.fig, newFig)
        else:
            self.fig = newFig #když je políčko prázdné, figurka se uloží
        
    def draw(self, rectangleWidth, rectangleHeight, canvas):
    
        rectangleFill = 'lightgrey'  #střídání barev
        if(self.color == Color.BLACK):
            rectangleFill = 'brown'
    
        canvas.create_rectangle( #vytvoření čtverce pro políčka, jako parametry souřadnice rohů
            rectangleWidth*self.positionX,
            rectangleHeight*self.positionY,
            rectangleWidth*(self.positionX+1),
            rectangleHeight*(self.positionY+1),
            fill=rectangleFill) #vyplnění barvou
        
        if(self.hasFig()):
            self.fig.draw(rectangleWidth, rectangleHeight, canvas)
