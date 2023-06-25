from confirm_kick import *
from detect_operation import *
from operations import *

while True:
    kick_volume = 50
    kick = confirm_kick(kick_volume)

    if kick == 1:
        print("Kick detected")
        control_kick()
        print("Action Taken")
        kick_volume += 50

    else:
        print(f"operation = {detect_operation()}")









