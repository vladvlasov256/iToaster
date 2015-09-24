class Event(object):
    def __init__(self, *args):
        self._callbacks = []
        for callback in args:
            self.add_callback(callback)

    def __call__(self, *args, **kwargs):
        for callback in self._callbacks:
            callback(*args, **kwargs)

    @property
    def callbacks(self):
        return self._callbacks

    def add_callback(self, callback):
        if not callback or self._callbacks.count(callback) > 0:
            return
        self._callbacks.append(callback)

    def remove_callback(self, callback):
        try:
            self._callbacks.remove(callback)
        finally:
            pass