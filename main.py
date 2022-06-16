from os import getcwd #načte aktuální adresář
import tkinter
from tkinter import filedialog #knihovna pro otevření okna pro načtení hry
from game import Game
from os.path import exists #ověřuje existenci souboru
from gameLoader import GameLoader


def load_board_from_csv(game):
	current_directory = getcwd() #zjistí aktuální adresář a uloží do proměnné
	#vyvolá okno pro výběr souboru a uloží do proměnné jméno souboru
	filename = filedialog.askopenfilename(initialdir = current_directory, #otevře se v aktuální složce
                                          title = "Select a File", #hláška
                                          filetypes = (("Game csv saved files", #popisek při výběru ve file exploreru
                                                        "*.csv*"), #podporované soubory
                                                       ("all files",
                                                        "*.*")))


	if len(filename) == 0 : return #když se nezvolí soubor, vyskočí z funkce (funguje zde jako break)

	saved_file = open(filename) #otevře soubor se zvoleným jménem
	game_board_state, last_player = GameLoader.play_game(saved_file) #je rozsekáno v gameLoader
	# Poté co je vše přečtené, můžeme zavřít stream
	saved_file.close()

	game.board = game_board_state #vytvoří board dle csv
	game.active_player = last_player #nastaví posledního hráče z csv

	# načtením získáme posledního hráče co hrál, ale na tahu má být ten druhý
	game.toggle_players()

	# po načtení souboru se musí automaticky přerendrovat pole
	game.draw()

	return


file_writer = None
#maximálně 10 csv souborů, každý dostane index
for i in range (0,10):
	file_name = f"dama{i}.csv"
	if exists(file_name): #když existuje soubor se stejným jménem, přejde na další index
		continue
	else:
		file_writer = open(file_name, "w") #připraví se nový soubor pro zápis
		break


if file_writer is None: file_writer = open("dama.csv", "w") #jedenáctý soubor nedostane index a je po každém uložení přepsán

root = tkinter.Tk() #inicializece tkinter a vytvoření okna root
root.title('Dáma™') #pojmenování okna

game = Game(root, file_writer = file_writer) #spustí hru znova, přiřadí file_writer se zápisem

# vytvoří tlačítko k načítání hry z csv
# při stisku tlačítka spustí load_board_from_csv
w = tkinter.Button(root, text = "Load game from csv file", command=lambda: load_board_from_csv(game))
# pack umístí tlačítko vedle hracího pole
# parametr side určuje stranu, kam se tlačítko umístí
# padx určí vzdálenost od pole a kraje okna
w.pack(side = tkinter.RIGHT, padx = 10)

game.play() # spuštění hry



