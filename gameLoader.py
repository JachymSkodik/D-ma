from board import Board
from enums import Color
from fig import Fig

class GameLoader: #funkce pro načtení hry z csv souboru
	@staticmethod #funkce není vázaná objektem
	def parseInputLine(fileReader):
		line = fileReader.readline() #do proměnné line se uloží string z řádku z csv

		if len(line) == 0: return None #když je řádek prázdný, vrátí None

		fromPosChar, toPosChar, color = line.split(',') #rozdělí proměnnou line na prvky seznamu

		# Fig.py metoda toString, proto je zde - 1
		# odečte z první souřadnice jedničku, protože hra indexuje od 0, ale zápis je od indexu 1
		#a převede písmeno na číslo v souřadnici
		fromPos = (int(fromPosChar[0]) - 1, GameLoader.alphabetToNum(fromPosChar[1]))
		toPos = (int(toPosChar[0]) - 1, GameLoader.alphabetToNum(toPosChar[1]))
		colorEnum = None #vymaže se obsah proměnné

		if color == "Black\n" : #zjišťuje, jakou barvu má mít nasazená figurka
			colorEnum = Color.BLACK
		elif color == "White\n":
			colorEnum = Color.WHITE
		else:
			raise Exception("Csv file is in incorrect format") #když je zápis barvy špatně, vyhodí se exception
		
		return (fromPos, toPos, colorEnum) #vrátí souřadnice a barvu ve formátu pro hru

	@staticmethod
	def playGame(fileReader):
		parsedLine = GameLoader.parseInputLine(fileReader) #souřadnice a barvy se uloží do proměnné
		board = Board() #po načtení se musí vytvořit nové hrací pole

		lastPlayer = Color.BLACK #při nové hře začíná černý
		# kontrola správného zápisu
		# pokud jsou v zápisu dvě figurky na stejném políčku, hra se nenačte, vyvolá se výjimka
		while parsedLine:
			fromPos, toPos, colorEnum = parsedLine
			if not board.isMoveFigureOnBoardSuccess(fromPos[0], fromPos[1], Fig(toPos[0], toPos[1], colorEnum)):
				raise Exception("Can't load corrupted game")
			# když je zápis správně, vrátí souřadnice, barvy figurek a posledního hráče na tahu
			parsedLine = GameLoader.parseInputLine(fileReader)
			lastPlayer = colorEnum

		return (board, lastPlayer)

		
	# převede písmena z csv zápisu zpátky na čísla
	@staticmethod
	def alphabetToNum(charInput): #písmena odshora dolů, čísla zleva doprava
		alphabetDictionary = {
			'A': 0,
			'B': 1,
			'C': 2,
			'D': 3,
			'E': 4,
			'F': 5,
			'G': 6,
			'H': 7
		}

		return alphabetDictionary[charInput]