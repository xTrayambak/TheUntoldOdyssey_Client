class Audio:
    def __init__(self, path: str, tuo):
        self.tuo = tuo
        self.path = path

        self.sound = tuo.loader.loadSfx(path)
        
    
    # Instruction functions.

    def play(self):
        """
        Play the sound.
        """
        self.sound.play()

    def stop(self):
        """
        Stop the sound.
        """
        self.sound.stop()


    # Attribute-set functions.

    def set_volume(self, volume: float | int):
        """
        Set the volume of the audio.

        `volume`<int|float> :: The volume of the audio (according to docs; must be around 0 and 1.)
        """
        if volume > 1 or volume < 0:
            raise Exception("Audio volume cannot be lower than 0 and higher than 1; got {}!".format(volume))
        
        self.sound.setVolume(volume)

    def set_balance(self, balance: float | int):
        """
        Set the balance (i.e, the bias between the left and right speakers) of the audio.

        `balance`<int|float> :: The balance factor of the audio (according to docs; must be around -1 and 1.)

        
        -1: EXTREME LEFT
        +1: EXTREME RIGHT
        """
        if balance > 1 or balance < -1:
            raise Exception("Audio balance cannot be lower than -1 and higher than 1; got {}!".format(balance))

        self.sound.setBalance(balance)

    def set_time(self, time: float):
        """
        Set the time (i.e, the current area of the data being streamed as per time) of the audio.

        `time`<float> :: The time factor. 
        """
        self.sound.setTime(time)

    def set(self, attr: str, val):
        """
        Generic function for any attributes-set method not implemented via built-in functions.
        """
        return getattr(self.sound, f'set{attr}')(val)


    # Attribute-get functions.
    def get_status(self):
        """
        Get the status of the song playing currently.
        """
        return self.sound.status()

    def is_corrupted(self) -> bool:
        """
        Determine whether the track is `BAD` (i.e, corrupted)
        """
        return self.get_status() == self.sound.BAD

    def is_playing(self) -> bool:
        """
        Determine whether the track is `PLAYING` (i.e, playing the data onto the audio device provided)
        """
        return self.get_status() == self.sound.PLAYING

    def get_balance(self) -> int | float:
        return self.sound.balance

    def get(self, attr: str):
        """
        Generic function for any attribute-get method not implemented via built-in functions.
        """
        return getattr(self.sound, f'get{attr}')()