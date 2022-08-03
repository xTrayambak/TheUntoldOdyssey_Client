import os
from src.log import log, warn

from src.client.savefile import sread

def get_all_savefiles():
    savefiles = []

    if not os.path.exists('saves'): os.mkdir('saves')
    for dir in os.scandir('saves'):
        if dir.is_dir():
            for file in os.scandir(f'saves/{dir.name}'):
                if file.is_file():
                    if file.name == 'core.tuo':
                        if sread(file):
                            log(f'Found save file "{dir.name}"')
                            savefiles.append(dir.name)

    return savefiles