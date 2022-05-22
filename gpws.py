from sound import *

prev_engine = None
prev_fuel = None

readout_alts = [10, 20, 30, 40, 50, 100, 200, 300, 400, 500, 1000, 2500]
readout_list = [False] * len(readout_alts)

def alt_readout(ship, terrain):

    global readout_list, readout_alts

    def play_alt_readout(snd_name):
        play_sfx("altitude/" + snd_name, 0, 6)

    if ship.get_alt_quick(terrain) > 50:
        alt = ship.get_alt_quick(terrain)
    else:
        alt = ship.get_alt(terrain)

    #print(readout_list)

    snd_name = None
    for read_alt_index in range(len(readout_alts)):
        read_alt = readout_alts[read_alt_index]
        if read_alt * 0.6 < alt < read_alt and not readout_list[read_alt_index]:
            snd_name = str(read_alt)
            readout_list[read_alt_index] = True
            break

    if snd_name:
        play_alt_readout(snd_name)

    for read_alt_index in range(len(readout_alts)):
        read_alt = readout_alts[read_alt_index]
        if alt > read_alt * 1.5 and readout_list[read_alt_index]:
            readout_list[read_alt_index] = False

def gpws(ship, terrain, delta_t):

    global prev_engine, prev_fuel

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

    elif prev_fuel and prev_fuel > 500 and ship.get_prop_mass() < 500:
        play_gpws("fuellow")

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
        
    elif ship.get_pos()[1] >= 300:
        if sink_rate < 3 and horiz_speed < 200:
            if 0 < sink_rate < 3:
                play_gpws("increasedescent")
            elif sink_rate <= 0:
                play_gpws("descend")
            
        else:
            if ship.get_orient()[1][1] < 0.3:
                play_gpws("bankangle")

    prev_engine = ship.get_main_engine()
    prev_fuel = ship.get_prop_mass()
        

        
