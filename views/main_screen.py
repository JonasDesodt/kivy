from kivy.uix.screenmanager import Screen

class MainScreen(Screen):
    def switch_screen(self, screen_name):
        screen_manager = self.ids.main_screen_manager
        
        screen_manager.current = screen_name