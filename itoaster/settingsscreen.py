from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from screens import *
from settings import *
from toaster import *


class SettingsScreen(ToasterScreen):

    class StateDisplayController(object):

        dir_path = 'data/'
        on_filename = 'checkbox_on.png'
        off_filename = 'checkbox_off.png'

        def __init__(self, image):
            self._state = False
            self._image = image
            self._update()

        @property
        def state(self):
            return self._state

        @state.setter
        def state(self, value):
            if value == self._state:
                return
            self._state = value
            self._update()

        def _update(self):
            self._image.source = self._get_file_path()
            self._image.reload()

        def _get_file_path(self):
            if self.state:
                return SettingsScreen.StateDisplayController.dir_path + SettingsScreen.StateDisplayController.on_filename
            else:
                return SettingsScreen.StateDisplayController.dir_path + SettingsScreen.StateDisplayController.off_filename

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self._state_display_controller = SettingsScreen.StateDisplayController(self._get_control('toaster_state'))
        toaster.on_state_changed_event = lambda state: self._update_toaster_state()

    def show_screen(self, *args):
        self._get_control('ip').text = toaster.ip
        self._get_control('port').text = str(toaster.port)

        self._update_toaster_state()

    def on_ok_button_press(self):
        self._apply_settings()
        ToasterScreen.change_screen(MAIN_MENU_SCREEN)

    def on_cancel_button_press(self):
        ToasterScreen.change_screen(MAIN_MENU_SCREEN)

    def on_ip_enter(self, *args):
        try:
            toaster.ip = args[0]
            self._update_toaster_state()
        except ValueError:
            self.root.ids['ip'].text = toaster.ip

    def on_port_enter(self, *args):
        try:
            toaster.port = int(args[0])
            self._update_toaster_state()
        except ValueError:
            self.root.ids['port'].text = str(toaster.port)

    def _update_toaster_state(self):
        self._state_display_controller.state = toaster.ping()

        toasting_time = toaster.toasting_time
        self._get_control('time_slider').value = toasting_time
        self._get_control('time_label').text = '%02d:%02d' % (toasting_time / 60, toasting_time % 60)

    def _apply_settings(self):
        settings.ip = toaster.ip
        settings.port = toaster.port
        toaster.toasting_time = int(self._get_control('time_slider').value)
