from os import getcwd #načte aktuální adresář
import tkinter
from tkinter import filedialog #knihovna pro otevření okna pro načtení hry
from game import Game
from os.path import exists #ověřuje existenci souboru
from gameLoader import GameLoader


def loadBoardFromCsv(game):
	currentDirectory = getcwd() #zjistí aktuální adresář a uloží do proměnné
	#vyvolá okno pro výběr souboru a uloží do proměnné jméno souboru
	filename = filedialog.askopenfilename(initialdir = currentDirectory, #otevře se v aktuální složce
                                          title = "Select a File", #hláška
                                          filetypes = (("Game csv saved files", #popisek při výběru ve file exploreru
                                                        "*.csv*"), #podporované soubory
                                                       ("all files",
                                                        "*.*")))


	if len(filename) == 0 : return #když se nezvolí soubor, vyskočí z funkce (funguje zde jako break)

	savedFile = open(filename) #otevře soubor se zvoleným jménem
	gameBoardState, lastPlayer = GameLoader.playGame(savedFile) #je rozsekáno v gameLoader
	# Poté co je vše přečtené, můžeme zavřít stream
	savedFile.close()

	game.board = gameBoardState #vytvoří board dle csv
	game.activePlayer = lastPlayer #nastaví posledního hráče z csv

	# načtením získáme posledního hráče co hrál, ale na tahu má být ten druhý
	game.togglePlayers()

	# po načtení souboru se musí automaticky přerendrovat pole
	game.draw()

	return


filewriter = None
#maximálně 10 csv souborů, každý dostane index
for i in range (0,10):
	fileName = f"dama{i}.csv"
	if exists(fileName): #když existuje soubor se stejným jménem, přejde na další index
		continue
	else:
		filewriter = open(fileName, "w") #připraví se nový soubor pro zápis
		break


if filewriter is None: filewriter = open("dama.csv", "w") #jedenáctý soubor nedostane index a je po každém uložení přepsán

root = tkinter.Tk() #inicializece tkinter a vytvoření okna root
root.title('Dáma™') #pojmenování okna

game = Game(root, fileWriter = filewriter) #spustí hru znova, přiřadí filewriter se zápisem

# vytvoří tlačítko k načítání hry z csv
# při stisku tlačítka spustí loadBoardFromCsv
w = tkinter.Button(root, text = "Load game from csv file", command=lambda: loadBoardFromCsv(game))
# pack umístí tlačítko vedle hracího pole
# parametr side určuje stranu, kam se tlačítko umístí
# padx určí vzdálenost od pole a kraje okna
w.pack(side=tkinter.RIGHT, padx=10)

game.play() # spuštění hry



