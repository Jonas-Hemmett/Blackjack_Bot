# Safely launches the Blackjack Bot Pi program

import blackjackDisplay_Pi
import os
from DisplayBase_Pi import *
import Spin

if __name__ == "__main__":
    print("Launcher!")
    menu = [[["Blackjack Bot"], ["Card Spin"]], [["Pi"], ["Reboot"], ["Shutdown"]]]
    val = ""
    while True:
        if not backlight.value:
            backlight.value = True

        draw.rectangle((0, 0, width, height - 60), fill = (0, 0, 0))
        disp.image(image)

        val = blackjackDisplay_Pi.menuMegaMind(menu, "")
        print(val)

        if val == "Blackjack Bot":
            blackjackDisplay_Pi.launch()

        elif val == "Card Spin":
            Spin.doSpin(2)

        elif val == "Pi":
            try:
                backlight.value = False
            except:
                print("Screen already closed")
            exit() 
        
        
        elif val == "Reboot":
            try:
                backlight.value = False
            except:
                print("Screen already closed")
            
            # I needed to change sudo file to get this working
            os.system("sudo /sbin/reboot -h now")

        elif val == "Shutdown":
            try:
                backlight.value = False
            except:
                print("Screen already closed")
            
            # I needed to change sudo file to get this working
            os.system("sudo /sbin/shutdown -h now")
