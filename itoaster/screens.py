import os
import os.path as path
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

MAIN_MENU_SCREEN = 'main_menu'
SETTINGS_SCREEN = 'settings'


class ToasterScreen(Screen):

    KV_FILE_DIR = 'data'

    def __init__(self, **kwargs):
        super(ToasterScreen, self).__init__(**kwargs)

        self.bind(on_enter=self.show_screen)

        self.root = Builder.load_file(self._get_kv_file_path())
        self.add_widget(self.root)

    @staticmethod
    def change_screen(screen_name):
        screen_manager.current = screen_name

    def show_screen(self, *args):
        pass

    def resolve_kv_callback(self, name, *args):
        try:
            callback_method = getattr(self, name)
            callback_method(*args)
        finally:
            pass

    def _get_control(self, id):
        return self.root.ids[id]

    def _get_kv_file_path(self):
        return path.join(ToasterScreen.KV_FILE_DIR, self.__class__.__name__.lower() + '.kv')


screen_manager = ScreenManager()