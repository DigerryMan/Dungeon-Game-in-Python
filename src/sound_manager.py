from pygame import mixer

class SoundManager:
    def __init__(self):
        mixer.init()
        self.sounds = {
            "basementLoop": mixer.Sound("resources/music/basementLoop.ogg"),
            "tearPop": mixer.Sound("resources/sounds/tearPop.wav"),
        }

    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"Sound '{sound_name}' not found!")