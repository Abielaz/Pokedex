import requests
import json
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Label, Input, Static
from textual.containers import Center
from pokemon.master import catch_em_all, get_pokemon

asciiPokemon = catch_em_all() #loads ASCII database so that it doesn't need to load with each search

class HomePage(Screen): #each Screen subclass represents one full page of the app
    CSS_PATH = "style.tcss"
    def compose(self) -> ComposeResult:
        self.notify("App Works Best When Maximized! ^-^", title = "Quick Tip:", severity="information", timeout=10) #notification added for end-user tip
        with Center():
            yield Static("                                  ,'\\\n    _.----.        ____         ,'  _\\   ___    ___     ____\n_,-'       `.     |    |  /`.   \\,-'    |   \\  /   |   |    \\  |`.\n\\      __    \\    '-.  | /   `.  ___    |    \\/    |   '-.   \\ |  |\n \\.    \\ \\   |  __  |  |/    ,','_  `.  |          | __  |    \\|  |\n   \\    \\/   /,' _`.|      ,' / / / /   |          ,' _`.|     |  |\n    \\     ,-'/  /   \\    ,'   | \\/ / ,`.|         /  /   \\  |     |\n     \\    \\ |   \\_/  |   `-.  \\    `'  /|  |    ||   \\_/  | |\\    |\n      \\    \\ \\      /       `-.`.___,-' |  |\\  /| \\      /  | |   |\n       \\    \\ `.__,'|  |`-._    `|      |__| \\/ |  `.__,'|  | |   |\n        \\_.-'       |__|    `-._ |              '-.|     '-.| |   |\n                                `'                            '-._|", id="asciiHome")
        self.start = Button("Choose Your Pokemon!")
        with Center():
            yield self.start
        self.quit = Button("Quit")
        with Center():
            yield self.quit

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button == self.start:
            self.app.push_screen('search')
        elif event.button == self.quit:
            self.exit()

class Search(Screen):
    CSS_PATH = "style.tcss"
    def compose(self):
        self.backToHome = Button("Back")
        yield self.backToHome
        self.searchAscii = Static( "                                                                 \n                                                                 \n                                                                 \n                                                                 \n                                                                 \n                        .@@@@@@@@@@@@@.                          \n                     @@@@@@@@%:  #@@@@@@@@                       \n                   @@@@@.              @@@@@.                    \n                 @@@@:                   .@@@@                   \n                @@@@                       .@@@.                 \n              .@@@.                         .@@@.                \n              @@@.            .-.            .@@@                \n             +@@@          @@@@@@@@@.         .@@%               \n             @@@.         @@@     @@@          @@@               \n             @@@@@@@@@@@@@@@       @@@@@@@@@@@@@@@               \n             @@@.........-@@.     .@@=::.......@@@               \n             @@@.         @@@@...@@@@         .@@@               \n             .@@@           @@@@@@@           @@@.               \n              @@@%                           @@@@                \n               @@@@                         @@@@                 \n                %@@@.                     :@@@@                  \n                 .@@@@.                 #@@@@.                   \n                    @@@@@@.         .@@@@@@.                     \n                      .@@@@@@@@@@@@@@@@@.                        \n                          ..@@@@@@@..                            \n                                                                 \n                                                                 \n                                                                 \n                                                                 \n                                                                 \n                                                                 ", id="asciiSearch")
        with Center():
            yield self.searchAscii
        self.searchError = Label(id="errorSearch")
        with Center():
            yield self.searchError
        self.searchInput = Input(placeholder="Who's That Pokemon?!", id="inputSearch")
        with Center():
            yield self.searchInput

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button == self.backToHome:
            self.app.pop_screen()


    def on_input_submitted(self, event):
        pokeApi = requests.get(f"https://pokeapi.co/api/v2/pokemon/{event.value}")
        if pokeApi.status_code == 200: #status 200 means the Pokemon was found successfully
            self.searchError.update("")
            pokeData = json.loads(pokeApi.text)
            asciiData = get_pokemon(pokemons=asciiPokemon, name=event.value) #looks up ascii art matching the searched Pokemon name
            for key in asciiData:
                asciiDataKey = asciiData[key] #ascii data is nested under the Pokemon's ID number as the dict key
                searchResults = Results(asciiDataKey['ascii'], pokeData['name'], pokeData['stats'], pokeData['abilities'], pokeData['moves']) #passing fetched data into Results so it can display without re-fetching
                self.app.push_screen(searchResults)
        else:
            self.searchError.update(f"Hmmm... Wrong Pokemon?...") #error handling added for incorrect end-user input ensuring no crashes

class Results(Screen):
    def __init__ (self, searchAscii, searchPokemon, statsData, abilitiesData, movesData): #storing data passed in from Search for use in compose()
        super().__init__()
        self.searchAscii = searchAscii
        self.searchPokemon = searchPokemon
        self.statsData = statsData
        self.abilitiesData = abilitiesData
        self.movesData = movesData

    def compose(self):
        self.backToSearch = Button("Back")
        yield self.backToSearch
        self.resultsAsciiWidget = Static(self.searchAscii, id="asciiResults")
        with Center():
            yield self.resultsAsciiWidget
        self.resultsPokemonWidget = Static(f"You Chose: {self.searchPokemon.capitalize()}!", id="pokemonResults")
        with Center():
            yield self.resultsPokemonWidget
        self.statsButton = Button("Stats")
        with Center():
                yield self.statsButton

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button == self.backToSearch:
            self.app.pop_screen()
        elif event.button == self.statsButton:
            sendStats = Stats(self.statsData, self.abilitiesData, self.movesData)
            self.app.push_screen(sendStats) #sending data to stats screen

class Stats(Screen):
    def __init__(self, searchPokemonStats, searchPokemonAbilities, searchMovesData):
        super().__init__()
        self.searchPokemonStats = searchPokemonStats
        self.searchPokemonAbilities = searchPokemonAbilities
        self.searchPokemonMoves = searchMovesData

    def compose(self):
        self.backToResults = Button("Back")
        yield self.backToResults

        pokeStats = ""
        for stats in self.searchPokemonStats:
            pokeStats += stats["stat"]["name"] + ": " + str(stats["base_stat"]) + "\n" #builds one combined string since static widgets only accept a single string, not a list
        cleanStats = pokeStats.rstrip() #removes trailing characters from loop to make output cleaner
        self.statsWidget = Static(f"Stats: \n{cleanStats.title()}", id="stats")
        with Center():
            yield self.statsWidget

        pokeMoves = ""
        for moves in self.searchPokemonMoves[0:5]:
            pokeMoves += moves["move"]["name"] + ", " + "\n"
        cleanMoves = pokeMoves.rstrip(", \n")
        self.movesWidget = Static(f"Moves: \n{cleanMoves.title()}", id = "moves")
        with Center():
            yield self.movesWidget

        pokeAbilities = ""
        for abilities in self.searchPokemonAbilities:
            pokeAbilities += abilities["ability"]["name"] + ", " + "\n"
        cleanAbilities = pokeAbilities.rstrip(", \n")
        self.abilitiesWidget = Static(f"Abilities: \n{cleanAbilities.title()}", id = "abilities")
        with Center():
            yield self.abilitiesWidget




    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button == self.backToResults:
            self.app.pop_screen()


class PokedexApp(App):
    SCREENS = {"homepage":HomePage, "search":Search, "results":Results, "stats":Stats}
    def on_mount(self) -> None:
      self.push_screen('homepage')


if __name__ == "__main__":
    app = PokedexApp()
    app.run()
