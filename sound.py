from pygame import mixer

def init_sound():
    mixer.init()

def play_sfx(track, loops=0, channel=1, volume=1):
    chn = mixer.Channel(channel)
    track_full = "data/sounds/" + str(track) + ".ogg"
    snd = mixer.Sound(track_full)
    chn.set_volume(volume)
    chn.play(snd, loops)

def get_channel_busy(channel):
    chn = mixer.Channel(channel)
    return chn.get_busy()

def set_channel_volume(channel, volume):
    channel = mixer.Channel(channel)
    channel.set_volume(volume)

def stop_channel(channel):
    channel = mixer.Channel(channel)
    channel.stop()
