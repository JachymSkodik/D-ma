from board import Board
from enums import Color
from fig import Fig


class GameLoader:  # funkce pro načtení hry z csv souboru
    @staticmethod  # funkce není vázaná objektem
    def parse_input_line(file_reader):
        line = file_reader.readline()  # do proměnné line se uloží string z řádku z csv

        if len(line) == 0: return None  # když je řádek prázdný, vrátí None

        from_pos_char, to_pos_char, color = line.split(',')  # rozdělí proměnnou line na prvky seznamu

        # Fig.py metoda toString, proto je zde - 1
        # odečte z první souřadnice jedničku, protože hra indexuje od 0, ale zápis je od indexu 1
        # a převede písmeno na číslo v souřadnici
        from_pos = (int(from_pos_char[0]) - 1, GameLoader.alphabet_to_num(from_pos_char[1]))
        to_pos = (int(to_pos_char[0]) - 1, GameLoader.alphabet_to_num(to_pos_char[1]))
        color_enum = None  # vymaže se obsah proměnné

        if color == "Black\n":  # zjišťuje, jakou barvu má mít nasazená figurka
            color_enum = Color.BLACK
        elif color == "White\n":
            color_enum = Color.WHITE
        else:
            raise Exception("Csv file is in incorrect format")  # když je zápis barvy špatně, vyhodí se exception

        return (from_pos, to_pos, color_enum)  # vrátí souřadnice a barvu ve formátu pro hru

    @staticmethod
    def play_game(file_reader):
        parsed_line = GameLoader.parse_input_line(file_reader)  # souřadnice a barvy se uloží do proměnné
        board = Board()  # po načtení se musí vytvořit nové hrací pole

        last_player = Color.BLACK  # při nové hře začíná černý
        # kontrola správného zápisu
        # pokud jsou v zápisu dvě figurky na stejném políčku, hra se nenačte, vyvolá se výjimka
        while parsed_line:
            from_pos, to_pos, color_enum = parsed_line
            if not board.is_move_figure_on_board_success(from_pos[0], from_pos[1],
                                                         Fig(to_pos[0], to_pos[1], color_enum)):
                raise Exception("Can't load corrupted game")
            # když je zápis správně, vrátí souřadnice, barvy figurek a posledního hráče na tahu
            parsed_line = GameLoader.parse_input_line(file_reader)
            last_player = color_enum

        return (board, last_player)

    # převede písmena z csv zápisu zpátky na čísla
    @staticmethod
    def alphabet_to_num(char_input):  # písmena odshora dolů, čísla zleva doprava
        alphabet_dictionary = {
            'A': 0,
            'B': 1,
            'C': 2,
            'D': 3,
            'E': 4,
            'F': 5,
            'G': 6,
            'H': 7
        }

        return alphabet_dictionary[char_input]  # vrátí index písmena, které se objevilo v zápisu