from kivy.app import App
from app_container import AppContainer
from views.main_screen import MainScreen

from create_database import *

# create_and_seed_database()
    
class PlaylistApp(App):
    def build(self):
        self.container = AppContainer()

        self.container.wire(modules=
                            [__name__, 
                             'views.tracklist_view', 
                             'views.tracklist_item', 
                             'views.playlist_view',
                             'views.playlist_item',
                             'views.suggestionlist_screen',
                             'views.suggestionlist_view',
                             'views.suggestionlist_item'])

        return MainScreen()  
    
if __name__ == '__main__':
    PlaylistApp().run() 