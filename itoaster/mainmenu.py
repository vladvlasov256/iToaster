import os
from os import path
from math import cos, pi
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from screens import *
from toaster import *


class MainMenu(ToasterScreen):

    class BlinkingLabelController(object):

        def __init__(self, label, interval=.1, duration=10, on_finish=None):
            self._label = label
            self._interval = interval
            self._duration = duration
            self._is_active = False
            self._visible = False
            self._elapsed_time = 0
            self._on_finish = on_finish

        def start(self):
            self._is_active = True
            self._visible = True
            self._elapsed_time = 0
            self._update()

        def abort(self):
            self._is_active = False
            self._label.opacity = 1

        def _update(self, delta=0):
            if not self._is_active:
                return

            self._visible = not self._visible
            self._elapsed_time += delta
            self._label.opacity = self._get_opacity()

            if self._elapsed_time < self._duration:
                Clock.schedule_once(self._update, self._interval)
            else:
                self.abort()
                self._on_finish()

        def _get_opacity(self):
            return .5 + .5 * cos(self._elapsed_time * pi * .5)

    class DisplayController(object):

        WARNING_COLOR = [.21, 0, 0, 1]
        TEXT_COLOR = [.08, .1, .1, 1]
        READY_COLOR = [.24, .16, .13, 1]

        def __init__(self, label):
            self._label = label

        def set_idle_mode(self):
            self._label.color = MainMenu.DisplayController.TEXT_COLOR
            self._label.bold = False
            self._label.text = ''

        def set_offline_mode(self):
            self._label.color = MainMenu.DisplayController.WARNING_COLOR
            self._label.bold = False
            self._label.text = 'OFFLINE'

        def set_toasting_mode(self):
            self._label.color = MainMenu.DisplayController.TEXT_COLOR
            self._label.bold = True

        def set_ready_mode(self):
            self._label.color = MainMenu.DisplayController.READY_COLOR
            self._label.bold = True
            self._label.text = 'READY'

        def set_remaining_time(self, remaining_time):
            self._label.text = '%02d:%02d' % (remaining_time / 60, remaining_time % 60)

    SOUND_DIR = 'data'
    SOUND_READY = 'Ready.wav'

    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)

        self._display_controller = MainMenu.DisplayController(self._get_display())
        self._blinking_label_controller = MainMenu.BlinkingLabelController(
            self._get_display(), on_finish=self._display_controller.set_idle_mode)

        toaster.on_state_changed_event = self.on_toaster_state_changed
        toaster.on_remaining_time_changed_event = self.on_toasting_remaining_time_changed
        toaster.on_toast_ready_event = self.on_toast_ready

        self.sound_ready = SoundLoader.load(path.join(MainMenu.SOUND_DIR, MainMenu.SOUND_READY))

    def show_screen(self, *args):
        self.update_display_state(toaster.state)

    def on_reset_button_press(self):
        toaster.reset_toasting()

    def on_settings_button_press(self):
        ToasterScreen.change_screen(SETTINGS_SCREEN)

    def on_toaster_state_changed(self, state):
        self.update_display_state(state)

    def update_display_state(self, state):
        if state == Toaster.OFFLINE:
            self._display_controller.set_offline_mode()
            self._blinking_label_controller.abort()
        elif state == Toaster.IDLE:
            self._display_controller.set_idle_mode()
        elif state == Toaster.TOASTING:
            self._display_controller.set_toasting_mode()
            self._blinking_label_controller.abort()
        else:
            raise Exception('Unknown toaster state: ' + str(state))

    def on_toasting_remaining_time_changed(self, remaining_time):
        self._display_controller.set_remaining_time(remaining_time)

    def on_toast_ready(self):
        self._display_controller.set_ready_mode()
        self._blinking_label_controller.start()

        if self.sound_ready:
            self.sound_ready.play()

    def _get_display(self):
        return self._get_control('display')
