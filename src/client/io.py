import json


FILE_CACHE = []

class IOFile:
    """
    Helper class for an I/O supporting file which exists.

    [required]

    `path_real` -- the path of the file
    `mode` -- the mode in which to open the file
    """
    def __init__(self, path_real: str, mode: str):
        self.path_real = path_real
        self.file = open(path_real, mode)
        self.mode = mode

    def read(self, line: int = None):
        """
        Read the data/contents of the file.

        [optional]

        `line` -- if provided, returns the contents at the int (if the file is EOF before that, `None` is returned.)
        """
        if self.mode != 'rb' and self.mode != 'r':
            raise TypeError("Invalid operation, requires to be in read/readbytes mode.")

        if line: 
            if len(self.file.read()) >= line:
                return self.readline(line)
            else:
                return None

        return self.file.read()
    
    def readlines(self):
        """
        Return a list of the lines of this file's contents (line=seperated by newline escape literal)
        """
        if self.mode != 'rb' and self.mode != 'r':
            raise TypeError("Invalid operation, requires to be in read/readbytes mode.")

        return self.file.readlines()

    def readline(self, limit: int):
        """
        Read data/contents from a specific line.

        [required]

        `line` -- the line at which to read
        """
        if self.mode != 'rb' and self.mode != 'r':
            raise TypeError("Invalid operation, requires to be in read/readbytes mode.")
        
        return self.file.readline(limit)

    def change_mode(self, mode: str):
        """
        Change the mode of the file (i.e, close the file, and re-open it in the mode requested.)

        [required]

        `mode` -- the mode in which to change the file into
        """
        self.file.close()
        self.mode = mode
        self.file = open(self.path_real, mode)

    def get_mode(self):
        """
        Get the mode of the file we're using.
        """
        return self.mode

    def write(self, data):
        """
        Write data to this file.

        [required]

        `data` -- the data to write to the file
        """
        if self.mode != 'wb' and self.mode != 'w':
            raise TypeError("Invalid operation, requires to be in write/writebytes mode.")

        self.file.write(data)

    def close(self):
        """
        Close the file, (i.e, make it unwritable via this helper object.)
        """
        return self.file.close()

    def search_cache(path, mode):
        """
        **INTERNAL**
        """
        for cached_file in FILE_CACHE:
            if cached_file[0] == path and cached_file[1] == mode: return cached_file

    def new(path, mode):
        """
        Construct a new IOFile helper.

        [required]
        
        `path` -- the path of the file
        `mode` -- the mode in which to open the file
        """
        cache = IOFile.search_cache(path, mode)

        if cache: return cache
        return IOFile(path, mode)

    def json_write(self, data):
        """
        Write the provided data and write it to this file.

        [required]

        `data` -- the data to write.
        """
        if self.get_mode() != 'w': self.change_mode('w')
        json.dump(data, self.file)
    
    def json_read(self):
        """
        Read data from this file, and turn it into an object/dict via JSON.
        """
        if self.get_mode() != 'r': self.change_mode('r')
        return json.load(self.file)