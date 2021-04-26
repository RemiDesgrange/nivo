from typing import Any


class FakeRowProxy(dict):
    """
    It's like a row proxy, but you don't have to provide a keymap etc...
    """

    def __init__(self, seq=None, **kwargs):
        super().__init__(seq, **kwargs)

    def has_key(self, key: Any) -> bool:
        k = self.get(key)
        return bool(k)
