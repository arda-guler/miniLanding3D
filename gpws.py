from sound import *

prev_engine = None

def gpws(ship, terrain, delta_t):

    global prev_engine

    if get_channel_busy(5):
        return

    def play_gpws(snd_name):
        play_sfx("gpws/" + snd_name, 0, 5)

    vert_speed = ship.get_vel()[1]
    horiz_speed = (ship.get_vel()[0]**2 + ship.get_vel()[2]**2)**0.5
    sink_rate = -vert_speed
    alt = ship.get_alt_quick(terrain)

    if sink_rate > 6 and sink_rate * 25 >= alt:
        play_gpws("sinkrate")

    elif 2.5 < sink_rate <= 6 and sink_rate * 10 >= alt:
        play_gpws("sinkrate")

    elif prev_engine and not ship.get_main_engine() and alt > 15:
        play_gpws("stall")

    elif horiz_speed > 15 and alt < 150:
        if sink_rate > 1:
            play_gpws("dontsink")
        elif sink_rate <= 1:
            play_gpws("toolowterrain")

    elif alt < 300:
        if alt > 50 and sink_rate < 0.05 and horiz_speed < 10:
            play_gpws("descend")
        elif alt <= 50 and sink_rate < 0.05 and horiz_speed < 5:
            play_gpws("retard")
        elif ship.get_orient()[1][1] < 0.5:
            play_gpws("bankangle")
        
    elif alt >= 300:
        if sink_rate < 3 and horiz_speed < 200:
            if 0 < sink_rate < 3:
                play_gpws("increasedescent")
            elif sink_rate <= 0:
                play_gpws("descend")
            
        else:
            if ship.get_orient()[1][1] < 0.3:
                play_gpws("bankangle")

    prev_engine = ship.get_main_engine()
        

        
