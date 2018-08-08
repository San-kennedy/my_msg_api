"""

Generic exceptions

"""

class ContentTypeUnsupported(Exception):
    """exception when unsupported content type is sent as msg"""
    def __init__(self):
        Exception.__init__(self, "Unsupported content type. Supported application JSON")

class IllegalArgumentException(Exception):
    """exception when argument are illegel/undefined"""
    def __init__(self):
        Exception.__init__(self, "illegal_argument_exception")