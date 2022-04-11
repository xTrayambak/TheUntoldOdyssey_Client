"""
Syntax Telemetry.

For those concerned, this only reports your renderer data and system platform, no personal data and this CANNOT be used to identify you or distinguish you as your SS account is not bound to reports.
Aaand, the data is only sent when the game crashes. Never other than that.
"""
import sys

try:
    from pyglet.gl.gl_info import get_renderer, get_vendor, get_version
except:
    def get_renderer(): return "ERROR"
    def get_vendor(): return "ERROR"
    def get_version(): return "ERROR"

from src.client.syntaxutil.authlib.session import Session

def compileCrashReport(instance=None) -> dict:
    """
    Compile a report of all things that happened that caused the crash (for telemetry) and arrange it in a pretty dict.
    """
    crashReport = {
        'platform_architecture': sys.platform
    }

    # Linux (distro) data; possibly we can report to the distro maintainers what is wrong.
    if sys.platform == 'linux':
        import distro
        crashReport.update(
            {
                'linux_distro_id': distro.id(),
                'linux_distro_version': distro.version(),
                'linux_distro_release_name': distro.name()
            }
        )
    
    # Renderer data
    crashReport.update(
        {
            'opengl_vendor': get_vendor(),
            'opengl_version': get_version(),
            'opengl_renderer': get_renderer()
        }
    )

    # Python (interpreter) data [derived from sys module]
    crashReport.update(
        {
            'python_version': sys.version,
            'exc_info': sys.exc_info()[2]
        }
    )

    # TUO game data (to check if crash is from a very explainable reason such as too many entities)
    if instance is not None:
        if instance.game is not None:
            entity_count = instance.game.entityManager.entity_count
        else:
            entity_count = 0

        crashReport.update(
            {
                'tuo_client_version': instance.version,
                'game': {
                    'entity_count': entity_count
                }
            }
        )
    else:
        crashReport.update(
            {
                'tuo_client_version': 'noinit',
                'game': {
                    'entity_count': 0
                }
            }
        )

    return crashReport

def telemetrySend_crash(log_func, instance):
    log_func(f"{'='*8}\nSENDING TELEMETRY DATA TO SYNTAX STUDIOS SERVERS!\n{'='*8}")
    data = compileCrashReport(instance)

    try:
        session_req = Session()
        session_req.send_crash_report(data)
    except Exception as exc:
        log_func(f"{'='*8}\nTELEMETRY DATA SEND FAILED!\n[{exc}]\n{'='*8}")