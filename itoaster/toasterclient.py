from socket import *
from kivy.clock import Clock
from event import Event


def _check_socket(func):
    def func_wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs) if self._socket else None

    return func_wrapper


class ToasterClient(object):

    MAX_ANSWER_LENGTH = 4096

    PING = 'ping'
    GET_STATE = 'getState'
    GET_REMAINING_TIME = 'getRemainingTime'
    GET_TOASTING_TIME = 'getToastingTime'
    SET_TOASTING_TIME = 'setToastingTime'
    RESET = 'reset'

    OK = 'ok'

    def __init__(self, server_ip, port):
        self._ip = server_ip
        self._port = port
        self._socket = None
        self._on_restart_event = Event()
        self._restart()

        Clock.schedule_interval(self._update, 10)

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, value):
        self._ip = value
        self._restart()

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value
        self._restart()

    @property
    def on_restart_event(self):
        return self._on_restart_event.callbacks

    @on_restart_event.setter
    def on_restart_event(self, callback):
        self._on_restart_event.add_callback(callback)

    @_check_socket
    def shutdown(self):
        if self._socket:
            self._socket.close()

    @_check_socket
    def send_ping(self):
        return self._send_command(ToasterClient.PING)

    @_check_socket
    def set_toasting_time(self, toasting_time):
        self._send_command(ToasterClient.SET_TOASTING_TIME, toasting_time)

    @_check_socket
    def get_state(self):
        return self._send_command(ToasterClient.GET_STATE)

    @_check_socket
    def get_toasting_time(self):
        return self._send_command(ToasterClient.GET_TOASTING_TIME)

    @_check_socket
    def get_remaining_time(self):
        return self._send_command(ToasterClient.GET_REMAINING_TIME)

    @_check_socket
    def reset_toasting(self):
        self._send_command(ToasterClient.RESET)

    @_check_socket
    def _send_command(self, command_name, *args):
        try:
            self._socket.send(ToasterClient._get_command(command_name, *args))
            return self._socket.recv(ToasterClient.MAX_ANSWER_LENGTH)
        except error:
            self._socket = None
            return None

    @staticmethod
    def _get_command(command_name, *args):
        if len(args) == 0:
            return command_name
        return command_name + '?' + ','.join(map(str, args))

    def _restart(self):
        if self._socket:
            self._socket.close()

        try:
            self._socket = socket(family=AF_INET, type=SOCK_STREAM)
            self._socket.settimeout(1)
            self._socket.connect((self.ip, self.port))
        except error:
            self._socket = None

        self._on_restart()

    def _on_restart(self):
        self._on_restart_event()

    def _update(self, delta):
        if not self._socket:
            self._restart()
        if self.send_ping() != ToasterClient.OK:
            self._socket = None
