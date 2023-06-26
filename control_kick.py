from confirm_kick import *
from operations import *

while True:
    kick_loss_volume = 0.03
    kick,loss = confirm_kick_loss(kick_loss_volume)

    if kick == 1:
        print("Kick detected")
        try:
            control_kick()
            print("Action Taken")
        except:
            print("Error occurred in control_kick(). Recalling...")
            control_kick()
            print("Action Taken")

        #kick_loss_volume += 50

    elif loss == 1:
        print("Loss detected")
        control_loss()
        print("Action Taken")

    else:
        #print(f"operation = {detect_operation()}")
        print("No Actin Taken")









