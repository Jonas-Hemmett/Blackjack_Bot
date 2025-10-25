import blackjackDisplay
import os
from DisplayBase import *
import spinStable

# Safely launches the blackjack program
if __name__ == "__main__":
    print("Launcher!")
    menu = [[["Blackjack Bot"], ["Card Spin"]], [["Pi"], ["Reboot"], ["Shutdown"]]]
    val = ""
    while True:
        if not backlight.value:
            backlight.value = True

        draw.rectangle((0, 0, width, height - 60), fill = (0, 0, 0))
        disp.image(image)

        val = blackjackDisplay.menuMegaMind(menu, "")
        print(val)

        if val == "Blackjack Bot":
            blackjackDisplay.launch()

        elif val == "Card Spin":
            spinStable.launch()

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
