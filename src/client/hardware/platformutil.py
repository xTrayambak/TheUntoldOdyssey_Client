import sys

class PlatformUtil:
    """
    The platform utility for detecting the current OS we're using, except this shows even finer details.
    """
    def __init__(self):
        self.data = {
            'os.global.architecture': 'NOINIT',
            'device.is_phone': 'NOINIT', 
            'os.linux.distro_data': 'NOINIT'
        }

    def collect(self):
        """
        Collect all the data about this system and store it.
        """
        self.data['os.global.architecture'] = sys.platform,
        self.data['device.is_phone'] = hasattr(sys, 'getandroidapilevel')

        if sys.platform == 'linux':
            import distro
            self.data['os.linux.distro_data'] = {
                'name': distro.name(True),
                'name_plain': distro.name(),

                'codename': distro.codename(),
                'based_on': distro.like(),

                'distro_id': distro.id(),
                'distro_build_number': distro.build_number(),
                'distro_release_attr': distro.distro_release_info(),
                'distro_release_version': distro.version()
            }

    def get(self, val: str = None):
        """
        Get an attribute from the data.

        If *val* is `None`, the entire data will be returned, else the key will be checked and returned, if the key does not exist then `None` will be returned.        
        """
        if not val: return self.data
        if val in self.data: return self.data[val]
