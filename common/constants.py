class ChoicesEnum(object):
    # TODO: see if this is actually used anywhere and remove if not
    def __str__(self):  # pragma: no cover
        return self._value_

    @classmethod
    def values(cls):
        return [value for key, value in vars(cls).items() if not key.startswith('_')]  # noqa

    @classmethod
    def choices(cls):
        return [(i, i.replace("_", " ").title()) for i in cls.values()]

    @classmethod
    def keys(cls):
        return [key for key, _ in vars(cls).items() if not key.startswith("_")]
