import pickle
import os

from src.log import log, warn, fatal

def deserialize(data: bytes):
    try:
        return pickle.loads(data)
    except: return None

def serialize(data: object):
    try:
        return pickle.dumps(data)
    except: return None

def sread(file: str):
    with open(file, 'rb') as f:
        return serialize(f.read())

def swrite(file: str, data):
    with open(file, 'wb') as f:
        return f.write(deserialize(data))

class Savefile:
    def __init__(self, tuo, name: str):
        self.name = name
        self.tuo = tuo

        if not os.path.exists('saves'):
            os.mkdir('saves')

        os.mkdir(f'saves/{name}')

        self.save_data = {
            'core': {'version': tuo.version}
        }

        log(f'Savefile "{name}" created.')

    def read(self, worldname):
        if not os.path.exists('saves'): return
        for file in os.scandir(f'saves/{worldname}'):
            if file.is_dir(): continue
            with open(f'saves/{worldname}/{file}', 'rb') as fd:
                # protip: always use a context manager to open files so they are automatically closed, otherwise they may get corrupted
                data = sread(file)
                if data: 
                    if file.name == 'core.tuo':
                        if not 'version' in data:
                            fatal('Corrupted/tampered savefile detected! Abort. [core.tuo does not contain key "version"]', 'Worker/Savefile')
                            return -1
                                    
                        if data['version'] != self.tuo.version:
                            warn(f'Savefile has different version than current client version. Attempting to convert, this may corrupt the savefile. Here goes nothing! [core.tuo indicates this world was last loaded in version "{data["version"]}", and this client is running version "{self.tuo.version}" according to VER.', 'Worker/Savefile')

                        self.save_data.update({file.name: data})

        return 0

    def write_data_to_disk(self):
        log('Writing data to disk.')
        for file_name in self.save_data:
            data = self.save_data[file_name]
            with open(f'saves/{self.name}/{file_name}.tuo', 'wb+') as f:
                f.write(serialize(data))
        
    def write_data(self, file: str, key, data):
        self.save_data[file].update({key: data})
    
    def add_new_file(self, fn: str):
        log(f'Adding new file to save folder "{fn}"')
        
        self.save_data.update({fn: {}})

    def get_all_data(self): return self.save_data