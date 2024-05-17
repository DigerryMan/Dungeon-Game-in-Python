from pygame import mixer
import os

def load_sounds(directory):
    sound_files = os.listdir(directory)
    sounds = {}
    for sound_file in sound_files:
        name, _ = os.path.splitext(sound_file)
        path = os.path.join(directory, sound_file)
        sounds[name] = mixer.Sound(path)
    return sounds

class SoundManager:
    def __init__(self):
        mixer.init()
        self.sounds = load_sounds("resources/music")
        self.sounds.update(load_sounds("resources/sounds"))

    def play(self, sound_name, looped=False):
        if sound_name in self.sounds:
            self.sounds[sound_name].play(-1 if looped else 0)
        else:
            print(f"Sound '{sound_name}' not found!")

    def play_with_fadein(self, sound_name, fadein_time, looped=False):
        if sound_name in self.sounds:
            self.sounds[sound_name].play(-1 if looped else 0, fade_ms=fadein_time)
        else:
            print(f"Sound '{sound_name}' not found!")

    def stop(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()
        else:
            print(f"Sound '{sound_name}' not found!")

    def stop_with_fadeout(self, sound_name, fadeout_time):
        if sound_name in self.sounds:
            self.sounds[sound_name].fadeout(fadeout_time)
        else:
            print(f"Sound '{sound_name}' not found!")