import os
import time

from pygame import mixer


def load_sounds(directory):
    sound_files = os.listdir(directory)
    sounds = {}
    for sound_file in sound_files:
        name, _ = os.path.splitext(sound_file)
        path = os.path.join(directory, sound_file)
        sounds[name] = mixer.Sound(path)
    return sounds


music_volumes = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
effect_volumes = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]


class SoundManager:
    def __init__(self):
        mixer.init()
        mixer.set_num_channels(32)
        self.music = load_sounds("resources/music")
        self.sounds = load_sounds("resources/sounds2")
        self.set_music_volume(2)
        self.set_sound_volume(4)
        self.last_played = {}

    def set_music_volume(self, volume):
        for sound in self.music.values():
            sound.set_volume(music_volumes[volume])

    def set_sound_volume(self, volume):
        for sound in self.sounds.values():
            sound.set_volume(effect_volumes[volume])

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

    def play_if_not_playing(self, sound_name):
        current_time = time.time()
        if (
            sound_name in self.last_played
            and current_time - self.last_played[sound_name] < 0.05
        ):
            return

        if sound_name in self.sounds:
            self.sounds[sound_name].play()
            self.last_played[sound_name] = current_time
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
