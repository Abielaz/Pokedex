import requests
import json
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Label, Input, Static
from pokemon.master import catch_em_all, get_pokemon

asciiPokemon = catch_em_all()

class HomePage(Screen):
    def compose(self) -> ComposeResult:
        yield Static("                                  ,'\\\n    _.----.        ____         ,'  _\\   ___    ___     ____\n_,-'       `.     |    |  /`.   \\,-'    |   \\  /   |   |    \\  |`.\n\\      __    \\    '-.  | /   `.  ___    |    \\/    |   '-.   \\ |  |\n \\.    \\ \\   |  __  |  |/    ,','_  `.  |          | __  |    \\|  |\n   \\    \\/   /,' _`.|      ,' / / / /   |          ,' _`.|     |  |\n    \\     ,-'/  /   \\    ,'   | \\/ / ,`.|         /  /   \\  |     |\n     \\    \\ |   \\_/  |   `-.  \\    `'  /|  |    ||   \\_/  | |\\    |\n      \\    \\ \\      /       `-.`.___,-' |  |\\  /| \\      /  | |   |\n       \\    \\ `.__,'|  |`-._    `|      |__| \\/ |  `.__,'|  | |   |\n        \\_.-'       |__|    `-._ |              '-.|     '-.| |   |\n                                `'                            '-._|")
        self.start = Button("Choose Your Pokemon!")
        yield self.start
        self.quit = Button("Quit")
        yield self.quit

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button == self.start:
            self.app.push_screen('search')
        elif event.button == self.quit:
            self.exit()

class Search(Screen):
    def compose(self):
        self.backToHome = Button("Back")
        yield self.backToHome
        self.searchError = Label()
        yield self.searchError
        self.searchInput = Input(placeholder="Who's That Pokemon?!")
        yield self.searchInput

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button == self.backToHome:
            self.app.push_screen('homepage')


    def on_input_submitted(self, event):
        pokeApi = requests.get(f"https://pokeapi.co/api/v2/pokemon/{event.value}")
        if pokeApi.status_code == 200:
            pokeData = json.loads(pokeApi.text)
            asciiData = get_pokemon(pokemons=asciiPokemon, name=event.value)
            for key in asciiData:
                asciiDataKey = asciiData[key]
                searchResults = Results(asciiDataKey['ascii'], pokeData['name'])
                self.app.push_screen(searchResults)
        else:
            self.searchError.update(f"Uhhh Wrong Pokemon?...")

class Results(Screen):
    def __init__ (self, searchAscii, searchPokemon):
        super().__init__()
        self.resultsAscii = searchAscii
        self.resultsPokemon = searchPokemon

    def compose(self):
        self.backToSearch = Button("Back")
        yield self.backToSearch
        self.resultsAsciiWidget = Static(self.resultsAscii)
        yield self.resultsAsciiWidget
        self.resultsPokemonWidget = Static(f"You Chose: {self.resultsPokemon}!")
        yield self.resultsPokemonWidget

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button == self.backToSearch:
            self.app.push_screen('search')


class PokedexApp(App):
    SCREENS = {"homepage":HomePage, "search":Search}
    def on_mount(self) -> None:
      self.push_screen('homepage')


if __name__ == "__main__":
    app = PokedexApp()
    app.run()
