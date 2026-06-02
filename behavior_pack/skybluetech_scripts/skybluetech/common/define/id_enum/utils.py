# coding=utf-8


class SimpleEnum(object):
    _alls = {}  # type: dict[type[SimpleEnum], set[str]]
    _keywords = {"all"}

    @classmethod
    def all(cls):
        allset = SimpleEnum._alls.get(cls, None)
        if allset is None:
            allset = {
                getattr(cls, name)
                for name in dir(cls)
                if name[0] != "_" and name not in cls._keywords
            }
            SimpleEnum._alls[cls] = allset
        return allset
