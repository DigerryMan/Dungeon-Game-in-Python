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
        mixer.set_num_channels(32)
        self.music = load_sounds("resources/music")
        self.sounds = load_sounds("resources/sounds")
        self.set_music_volume(0.2)
        self.set_sound_volume(0.5)
        self.decrease_volume()

    def decrease_volume(self):
        sounds_to_decrease = ["satanFound", "satanAppear", "satanShootHands", "satanLaser", "satanShoot", "satanFly", "satanHit"]
        for sound in sounds_to_decrease:
            self.sounds[sound].set_volume(0.1) # 0.01 - 1 krecha 


    def set_music_volume(self, volume):
        for sound in self.music.values():
            sound.set_volume(volume)

    def set_sound_volume(self, volume):
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def play(self, sound_name, looped=False):
        if sound_name in self.sounds:
            self.sounds[sound_name].play(-1 if looped else 0)
        elif sound_name in self.music:
            self.music[sound_name].play(-1 if looped else 0)
        else:
            print(f"Sound '{sound_name}' not found!")

    def play_with_fadein(self, sound_name, fadein_time, looped=False):
        if sound_name in self.sounds:
            self.sounds[sound_name].play(-1 if looped else 0, fade_ms=fadein_time)
        elif sound_name in self.music:
            self.music[sound_name].play(-1 if looped else 0, fade_ms=fadein_time)
        else:
            print(f"Sound '{sound_name}' not found!")

    def stop(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()
        elif sound_name in self.music:
            self.music[sound_name].stop()
        else:
            print(f"Sound '{sound_name}' not found!")

    def stop_with_fadeout(self, sound_name, fadeout_time):
        if sound_name in self.sounds:
            self.sounds[sound_name].fadeout(fadeout_time)
        elif sound_name in self.music:
            self.music[sound_name].fadeout(fadeout_time)
        else:
            print(f"Sound '{sound_name}' not found!")

    def stop_all(self):
        mixer.stop()

    def stop_all_with_fadeout(self, fadeout_time):
        mixer.fadeout(fadeout_time)