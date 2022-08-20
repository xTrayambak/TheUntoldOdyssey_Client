"""
LUA VM in Python, so cool man

- This post was made by the KenzieLucyIcey gang
"""
import _io
import threading

from src.log import log, warn

UNSAFE_ATTR_NAMES = (
    'token'
)

class CriticalSecurityException(Exception):
    """
    Raised by the VM when something reaaallyyyy sketchy happens.
    """

# This should be an actual war crime.
try:
    import lupa.luajit20 as lua
except ImportError:
    try:
        import lupa.lua54 as lua
    except ImportError:
        try:
            import lupa.lua53 as lua
        except ImportError:
            try:
                import lupa as lua
            except ImportError:
                # What in the actual hell?
                import sys; sys.stdout.write("Unable to locate LUA implementation, tried to find LUAJIT, LUA54, LUA53 but none were found.\n"); del sys; exit(-1)

class VM:
    def __init__(self):
        self.runtime = lua.LuaRuntime(
                register_eval = False,
                attribute_filter = self.filter_attrib_access
        )

    def globals(self): return self.runtime.globals()

    def filter_attrib_access(self, obj, attr_name, is_setting):
        """
        Security mechanism -- preventing access to any object that can allow unsafe access.
        """
        if attr_name not in UNSAFE_ATTR_NAMES:
            return attr_name

        warn('VM.filter_attrib_access(): blocked LUA call to read/write into a restricted Python object.', 'Worker/TLVM/Security')

        raise CriticalSecurityException(f'Attempt to access restricted attribute "{attr_name}"') 

    def eval_expr(self, data: str | _io.TextIOWrapper):
        try:
            self._eval_expr(data)
        except lua._lupa.LuaError as exc:
            warn('VM.eval_expr(): The LUA VM implementation has raised an error!', 'Worker/TLVM')
            print(exc)

    def _eval_expr(self, data: str | _io.TextIOWrapper):
        if isinstance(data, _io.TextIOWrapper):
            return self.runtime.eval(data.read())
        else:
            return self.runtime.eval(data)

    def run(self, file: str, threaded: bool = False):
        with open(file, 'r') as fh:
            try:
                if not threaded:
                    self.runtime.execute(fh.read())
                else:
                    threading.Thread(target=self.runtime.execute, args=(fh.read(),)).start()
            except lua._lupa.LuaError as exc:
                warn('VM.run(): The LUA VM implementation has raised an error!', 'Worker/TLVM')
                print(exc)
            except CriticalSecurityException as exc:
                warn('VM.run(): Caught potentially malicious mod trying to access a forbidden variable; terminate!', 'Worker/TLVM/SecurityManager')
                return 'terminate-unsafe'
