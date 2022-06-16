import tkinter
from enums import Color

class Fig:
    def __init__ (self, position_x, position_y, color):
        self.position_x = position_x
        self.position_y = position_y
        self.color = color
        
    #vykreslení figurky    
    def draw(self, width, height, canvas):
        self.draw_with_offset(width, height, canvas)
        
    #vykreslení figurky tak, aby se nedotýkala hran políčka
    def draw_with_offset(self, width, height, canvas, offset_y=0): 
        r_width = width/2
        r_height = height/2
        x0 = (width*(self.position_x+1)) - (r_width - r_width*0.4 ) - (width/2) #rWidth je polovina délky hrany políčka, figurka má průměr 0,6 hrany políčka, je tedy od hrany vzdálená 0,4 rWidth
        y0 = (height*(self.position_y+1)) - (r_height - r_height*0.4) - (height/2) - offset_y 
        x1 = (width*(self.position_x+1)) + (r_width - r_width*0.4 ) - (width/2)
        y1 = (height*(self.position_y+1)) + (r_height - r_height*0.4) - (height/2) - offset_y 
        
        fill_color = 'white'
        outline_color = 'black'
        if(self.color == Color.BLACK):
            fill_color = 'black'
            outline_color = 'white'
        
        canvas.create_oval(x0, y0, x1, y1, fill = fill_color, outline = outline_color) 

    def possible_moves(self):
        possible_positions =[(self.position_x - 1, self.move_based_on_color()), (self.position_x + 1, self.move_based_on_color())]

        # tady odfiltrujeme možné pohyby, které by přesahovoly naší šachovnici 
        return list(filter(self.are_positions_within_bounds, possible_positions))
    
    #kontrolujeme, aby figurka nevyskočila mimo pole
    @staticmethod
    def is_within_bounds(position):
        return position >= 0 and position < 8
    
    #musíme funkci is_within_bounds použít i na novou pozici figurky
    @staticmethod
    def are_positions_within_bounds(positions):
        return Fig.is_within_bounds(positions[0]) and Fig.is_within_bounds(positions[1])
    
    #omezuje pohyb figurek jedné barvy
    def move_based_on_color(self):
        if(self.color == Color.BLACK):
            return self.move_up()
        else:
            return self.move_down()

    def move_up(self):
        return self.position_y - 1 

    def move_down(self):
        return self.position_y + 1 

    #přiřazení písmen ke sloupcům (šachová notace)
    def to_string(self):
        board_alphabet = "ABCDEFGH"

        return f"{self.position_x + 1}{board_alphabet[self.position_y]}"
    
    #vrátí novou pozici figurky
    def copy_fig(self):
        return Fig(self.position_x, self.position_y, self.color)


class SkippingFig(Fig):
    def __init__(self, position_x, position_y, color):
        super(SkippingFig, self).__init__(position_x, position_y, color)
    
    #figurka skáče přes dvě pole
    def move_up(self):
        return self.position_y - 2 

    def move_down(self):
        return self.position_y + 2 

    #vrátí novou pozici figurky po skoku
    @staticmethod
    def from_fig(fig):
        return SkippingFig(fig.position_x, fig.position_y, fig.color)


class Queen(Fig):

    def __init__ (self, position_x, position_y, color):
        super(Queen, self).__init__(position_x, position_y, color)


    def possible_moves(self):
        possible_positions = []

        #pohyb doprava dolu
        position_x = self.position_x
        position_y = self.position_y
        if Fig.are_positions_within_bounds((position_x, position_y)):
            position_x += 1
            position_y += 1
            possible_positions.append((position_x, position_y))

        #pohyb doleva nahoru
        position_x = self.position_x
        position_y = self.position_y
        if Fig.are_positions_within_bounds((position_x, position_y)):
            position_x -= 1
            position_y -= 1
            possible_positions.append((position_x, position_y))

        #pohyb doprava nahoru
        position_x = self.position_x
        position_y = self.position_y
        if Fig.are_positions_within_bounds((position_x, position_y)):
            position_x += 1
            position_y -= 1
            possible_positions.append((position_x, position_y))

        #pohyb doleva dolu
        position_x = self.position_x
        position_y = self.position_y
        if Fig.are_positions_within_bounds((position_x, position_y)):
            position_x -= 1
            position_y += 1
            possible_positions.append((position_x, position_y))

        # tady odfiltrujeme možné pohyby, které by přesahovoly naší šachovnici 
        return possible_positions 
    
    #skákání dámou (ještě není dodělané)
    def move_up(self):
        return self.position_y - 2, SkippingFig(fig.position_x, fig.position_y, fig.color) 

    def move_down(self):
        return self.position_y + 2, SkippingFig(fig.position_x, fig.position_y, fig.color)
    
    #vykreslení dámy (dvě figurky na sobě)
    def draw(self, width, height, canvas):
        super(Queen, self).draw(width, height, canvas)
        super(Queen, self).draw_with_offset(width, height, canvas, 10) #minus offset_y: druhá vykreslená figurka je posunutá o 10 pixelů nahoru

    #vrátí novou pozici dámy
    def copy_fig(self):
        return Queen(self.position_x, self.position_y, self.color)

    #změna na dámu
    @staticmethod
    def queen_from_fig(fig):
        return Queen(fig.position_x, fig.position_y, fig.color)
    
