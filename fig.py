import tkinter
from enums import Color

class Fig:
    def __init__ (self, positionX, positionY, color):
        self.positionX = positionX
        self.positionY = positionY
        self.color = color
        
    #vykreslení figurky    
    def draw(self,width,height,canvas):
        self.drawWithOffset(width,height,canvas)
        
    #vykreslení figurky tak, aby se nedotýkala hran políčka
    def drawWithOffset(self,width,height,canvas, offsetY=0): 
        rWidth = width/2
        rHeight = height/2
        x0 = (width*(self.positionX+1)) - (rWidth - rWidth*0.4 ) - (width/2) #rWidth je polovina délky hrany políčka, figurka má průměr 0,6 hrany políčka, je tedy od hrany vzdálená 0,4 rWidth
        y0 = (height*(self.positionY+1)) - (rHeight - rHeight*0.4) - (height/2) - offsetY 
        x1 = (width*(self.positionX+1)) + (rWidth - rWidth*0.4 ) - (width/2)
        y1 = (height*(self.positionY+1)) + (rHeight - rHeight*0.4) - (height/2) - offsetY 
        
        fillColor = 'white'
        outlineColor = 'black'
        if(self.color == Color.BLACK):
            fillColor = 'black'
            outlineColor = 'white'
        
        canvas.create_oval(x0, y0, x1, y1, fill = fillColor, outline = outlineColor) 

    def possibleMoves(self):
        possiblePositions =[(self.positionX - 1, self.moveBasedOnColor()), (self.positionX + 1, self.moveBasedOnColor())]

        # tady odfiltrujeme možné pohyby, které by přesahovoly naší šachovnici 
        return list(filter(self.arePositionsWithinBounds, possiblePositions))
    
    #kontrolujeme, aby figurka nevyskočila mimo pole
    @staticmethod
    def isWithinBounds(position):
        return position >= 0 and position < 8
    
    #musíme funkci isWithinBounds použít i na novou pozici figurky
    @staticmethod
    def arePositionsWithinBounds(positions):
        return Fig.isWithinBounds(positions[0]) and Fig.isWithinBounds(positions[1])
    
    #omezuje pohyb figurek jedné barvy
    def moveBasedOnColor(self):
        if(self.color == Color.BLACK):
            return self.moveUp()
        else:
            return self.moveDown()

    def moveUp(self):
        return self.positionY - 1 

    def moveDown(self):
        return self.positionY + 1 

    #přiřazení písmen ke sloupcům (šachová notace)
    def toString(self):
        boardAlphabet = "ABCDEFGH"

        return f"{self.positionX + 1}{boardAlphabet[self.positionY]}"
    
    #vrátí novou pozici figurky
    def copyFig(self):
        return Fig(self.positionX, self.positionY, self.color)


class SkippingFig(Fig):
    def __init__(self, positionX, positionY, color):
        super(SkippingFig, self).__init__(positionX, positionY, color)
    
    #figurka skáče přes dvě pole
    def moveUp(self):
        return self.positionY - 2 

    def moveDown(self):
        return self.positionY + 2 

    #vrátí novou pozici figurky po skoku
    @staticmethod
    def fromFig(fig):
        return SkippingFig(fig.positionX, fig.positionY, fig.color)


class Queen(Fig):

    def __init__ (self, positionX, positionY, color):
        super(Queen, self).__init__(positionX, positionY, color)


    def possibleMoves(self):
        possiblePositions = []

        #pohyb doprava dolu
        positionX = self.positionX
        positionY = self.positionY
        if Fig.arePositionsWithinBounds((positionX, positionY)):
            positionX += 1
            positionY += 1
            possiblePositions.append((positionX, positionY))

        #pohyb doleva nahoru
        positionX = self.positionX
        positionY = self.positionY
        if Fig.arePositionsWithinBounds((positionX, positionY)):
            positionX -= 1
            positionY -= 1
            possiblePositions.append((positionX, positionY))

        #pohyb doprava nahoru
        positionX = self.positionX
        positionY = self.positionY
        if Fig.arePositionsWithinBounds((positionX, positionY)):
            positionX += 1
            positionY -= 1
            possiblePositions.append((positionX, positionY))

        #pohyb doleva dolu
        positionX = self.positionX
        positionY = self.positionY
        if Fig.arePositionsWithinBounds((positionX, positionY)):
            positionX -= 1
            positionY += 1
            possiblePositions.append((positionX, positionY))

        # tady odfiltrujeme možné pohyby, které by přesahovoly naší šachovnici 
        return possiblePositions 
    
    #skákání dámou (ještě není dodělané)
    def moveUp(self):
        return self.positionY - 2, SkippingFig(fig.positionX, fig.positionY, fig.color) 

    def moveDown(self):
        return self.positionY + 2, SkippingFig(fig.positionX, fig.positionY, fig.color)
    
    #vykreslení dámy (dvě figurky na sobě)
    def draw(self,width,height,canvas):
        super(Queen, self).draw(width,height, canvas)
        super(Queen, self).drawWithOffset(width,height, canvas, 10) #minus offsetY: druhá vykreslená figurka je posunutá o 10 pixelů nahoru

    #vrátí novou pozici dámy
    def copyFig(self):
        return Queen(self.positionX, self.positionY, self.color)

    #změna na dámu
    @staticmethod
    def queenFromFig(fig):
        return Queen(fig.positionX, fig.positionY, fig.color)