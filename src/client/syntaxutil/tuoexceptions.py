class OutOfMemoryError(Exception):
    """
    This exception is raised when the game consumes more memory than allocated.
    """

class OpenGLError(Exception):
    """
    This exception is raised when OpenGL / GLSL raises a non-terminating error.
    """

class AuthenticationFailError(Exception):
    """
    This exception is raised when authentication fails.
    """