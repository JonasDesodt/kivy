from kivy.uix.screenmanager import Screen

class MainScreen(Screen):
    def switch_screen(self, screen_name, id = None):
        screen_manager = self.ids.main_screen_manager
        
        if id:
            next_screen = screen_manager.get_screen(screen_name)

            next_screen.id = id

        screen_manager.current = screen_name

        