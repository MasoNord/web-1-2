
class FileSizeLimitError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class FileDurationLimitError(Exception):
    def __init__(self, msg):
        super().__init__(msg)