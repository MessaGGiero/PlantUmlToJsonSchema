class DuplicatedProperties(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class UndefinedType(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ErrorTypeArgument(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class ErrorTypeParser(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)