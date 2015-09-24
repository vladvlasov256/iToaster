import kivy
kivy.require('1.8.0')

from kivy.app import App
from mainmenu import MainMenu
from settingsscreen import SettingsScreen
from screens import *
from settings import *
from toaster import *


class ToasterApp(App):

    def build(self):
        screen_manager.add_widget(MainMenu(name=MAIN_MENU_SCREEN))
        screen_manager.add_widget(SettingsScreen(name=SETTINGS_SCREEN))
        return screen_manager

    def kv_callback(self, name, *args):
        screen_manager.current_screen.resolve_kv_callback(name, *args)


if __name__ == '__main__':
    ToasterApp().run()
    toaster.shutdown()
    settings.save()