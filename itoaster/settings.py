from kivy.storage.jsonstore import JsonStore


class Settings(object):

    MIN_TOASTING_TIME = 10
    MAX_TOASTING_TIME = 600

    FILENAME = 'sofatech_toaster_storage'
    SETTINGS_KEY = 'settings'

    def __init__(self):
        self._ip = '127.0.0.1'
        self._port = 50007
        self._store = JsonStore(Settings.FILENAME)

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, value):
        self._ip = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    def load(self):
        if self._store.exists(Settings.SETTINGS_KEY):
            settings_dict = self._store.get(Settings.SETTINGS_KEY)
            self._ip = settings_dict['ip']
            self._port = settings_dict['port']

    def save(self):
        self._store.put(Settings.SETTINGS_KEY, ip=self._ip, port=self._port)


settings = Settings()
settings.load()