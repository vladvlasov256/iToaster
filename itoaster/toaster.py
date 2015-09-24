from kivy.clock import Clock
from settings import *
from toasterclient import ToasterClient
from event import Event


def _int_parser(func):
    def func_wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except TypeError:
            pass
        except ValueError:
            pass

    return func_wrapper


class Toaster(object):

    IDLE = 'idle'
    TOASTING = 'toasting'
    OFFLINE = 'offline'

    def __init__(self, sever_ip, server_port):
        self._toasting_time = Settings.MIN_TOASTING_TIME
        self._state = Toaster.OFFLINE

        self._on_state_changed_event = Event()
        self._on_remaining_time_changed_event = Event()
        self._on_toast_ready_event = Event()

        self._client = ToasterClient(sever_ip, server_port)
        self._client.on_restart_event = self._on_restart_client
        self._on_restart_client()

        Clock.schedule_interval(self._tick, 1)

    def shutdown(self):
        if self._client:
            self._client.shutdown()

    @property
    def toasting_time(self):
        return self._toasting_time

    @toasting_time.setter
    def toasting_time(self, value):
        if self._toasting_time == value:
            return
        self._toasting_time = value
        self._client.set_toasting_time(value)

    @property
    def ip(self):
        return self._client.ip

    @ip.setter
    def ip(self, value):
        self._client.ip = value

    @property
    def port(self):
        return self._client.port

    @port.setter
    def port(self, value):
        self._client.port = value

    @property
    def state(self):
        return self._state

    @property
    def on_state_changed_event(self):
        return self._on_state_changed_event.callbacks

    @on_state_changed_event.setter
    def on_state_changed_event(self, callback):
        self._on_state_changed_event.add_callback(callback)

    @property
    def on_remaining_time_changed_event(self):
        return self._on_remaining_time_changed_event.callbacks

    @on_remaining_time_changed_event.setter
    def on_remaining_time_changed_event(self, callback):
        self._on_remaining_time_changed_event.add_callback(callback)

    @property
    def on_toast_ready_event(self):
        return self._on_toast_ready_event.callbacks

    @on_toast_ready_event.setter
    def on_toast_ready_event(self, callback):
        self._on_toast_ready_event.add_callback(callback)

    def ping(self):
        return self._client.send_ping() == ToasterClient.OK

    def is_online(self):
        return self.state != Toaster.OFFLINE

    def reset_toasting(self):
        if self.state == Toaster.TOASTING:
            self._client.reset_toasting()

    def _on_restart_client(self):
        self._update_toasting_time()
        self._update_state()

    def _tick(self, delta):
        self._update_state()
        if self.state == Toaster.TOASTING:
            self._update_remaining_time()

    def _update_state(self):
        def convert_client_state(client_state):
            return client_state if client_state else Toaster.OFFLINE

        old_state = self.state
        self._state = convert_client_state(self._client.get_state())
        if old_state != self.state:
            self._on_state_changed(old_state)

    @_int_parser
    def _update_toasting_time(self):
        self._toasting_time = int(self._client.get_toasting_time())

    @_int_parser
    def _update_remaining_time(self):
        self._on_remaining_time_changed(int(self._client.get_remaining_time()))

    def _on_state_changed(self, old_state):
        self._on_state_changed_event(self.state)
        if old_state == Toaster.TOASTING and self.state == Toaster.IDLE:
            self._on_toast_ready()

    def _on_toast_ready(self):
        self._on_toast_ready_event()

    def _on_remaining_time_changed(self, remaining_time):
        self._on_remaining_time_changed_event(remaining_time)


toaster = Toaster(settings.ip, settings.port)