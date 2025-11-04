from DisplayBase import *
import openAIFunctions as f1

print("current")
# Lets the program be run on the Pi without a camera
try:
    from picamera2 import Picamera2
    camTest = Picamera2()
    camTest.start()
    camTest.close()
except:
    isCam = False
else:
    isCam = True

from time import sleep
import time
from bots import BotIrlBrain, Bot1C

fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
fnt2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

LT = 21 # Maximum hand sum


camRatio = 4 / 3

# Adds arrows to the menu options, letting the user know the options available 
def menuMind(menu, rc):
    if rc["r"] < 0:
        rc["r"] = 0
    elif rc["r"] > len(menu) - 1:
        rc["r"] = len(menu) - 1
    if rc["c"] < 0:
        rc["c"] = 0
    elif rc["c"] > len(menu[rc["r"]]) - 1:
        rc["c"] = len(menu[rc["r"]]) - 1
    return rc

# Runs the user interface menu
def menuMegaMind(menu, loopCode):
    # Adds on arrows to the menu options
    for o1 in range(len(menu)): # Rows
        for o2 in range(len(menu[o1])): # Column
            if len(menu[o1][o2]) == 1:
                menu[o1][o2].append(menu[o1][o2][0])
                menu[o1][o2][0] = ("\u2190" if o1 > 0 else "") + \
                ("\u2191" if o2 > 0 else "") + \
                menu[o1][o2][0] + \
                ("\u2193" if o2 < len(menu[o1]) - 1 else "") + \
                ("\u2192" if o1 < len(menu) - 1 else "")
    
    # Saves the current menu position in rows and columns
    rc = {"r": 0, "c": 0}
    while True:
        aAllow = False
        uAllow = False
        dAllow = False
        lAllow = False
        rAllow = False

        draw.rectangle((0, height - 60, width, height), fill = (100, 100, 100))

        _, _, textWidth, textHeight = draw.textbbox((0, 0), menu[rc["r"]][rc["c"]][0], font=fnt)
        draw.text(((width-textWidth)/2, height-textHeight - 20), menu[rc["r"]][rc["c"]][0], font=fnt, fill = (255, 255, 255))

        disp.image(image)
        
        if loopCode:
            loopCode(rc)
        
        # Checks for button presses
        while True:
            
            # Pressing C allows for buttons to be held down
            if not button_C.value:
                uAllow = True
                dAllow = True
                lAllow = True
                rAllow = True

            if button_U.value:
                uAllow = True
            elif uAllow:
                uAllow = False
                rc["c"] -= 1
                rc = menuMind(menu, rc)
                break

            if button_D.value:
                dAllow = True
            elif dAllow:
                dAllow = False
                rc["c"] += 1
                rc = menuMind(menu, rc)
                break

            if button_L.value:
                lAllow = True
            elif lAllow:
                lAllow = False
                rc["r"] -= 1
                rc["c"] = 0
                rc = menuMind(menu, rc)
                break

            if button_R.value:
                rAllow = True
            elif rAllow:
                rAllow = False
                rc["r"] += 1
                rc["c"] = 0
                rc = menuMind(menu, rc)
                break

            if button_A.value:
                aAllow = True

            # Returns the current row and column which corresponds to a menu option
            elif aAllow:
                return menu[rc["r"]][rc["c"]][1]
                
            if not button_B.value:
                pass
            time.sleep(0.01)
    

# Displays saved photos
def dispPic(rc, ):
    draw.rectangle((0, 0, width, height - 60), fill = (92, 155, 51))

    picIndex = -1
    try:
        if rc["r"] == 0:
            if rc["c"] == 0:
                picIndex = int(BotIrlBrain.readSave([5])[0])
            else:
                picIndex = rc['c'] - 1
        if picIndex == - 1:
            pass
        else:
            picIn = Image.open(f"/home/pi/CS2210/Blackjack/pic{picIndex}.jpg").convert('RGB').crop((0, 0, width, height - 60))
            image.paste(picIn, (0, 0))

    except  Exception as e:
        print(e)
        if rc["r"] == 0:

            _, _, textWidth, textHeight = draw.textbbox((0, 0), "None", font=fnt2)
            draw.text(((width-textWidth)/2, (height-textHeight - 20) / 2), "None", font=fnt2, fill = (255, 255, 255))
    disp.image(image)

# Displays an input hand on screen as a stack of cards
def dispHands(hands):
    cardDim = (30, 40)
    splitNum = len(hands)

    print(f"Hands: {hands}")

    for split in range(splitNum):
        hidden = len(hands[split]) <= 1

        splitCenter = ((width - 30) * (1 / (splitNum + 1)) * split) + 15 +  (width - 30) * (1 / (splitNum + 1))
        # draw.rectangle((splitCenter - 2, 0, splitCenter + 2, 180), fill = (0, 0, 0))
        for num in range(len(hands[split]) + hidden):
            draw.rectangle((splitCenter - 0.5 * cardDim[0] + num * 0.35 * cardDim[0], (-0.5 * cardDim[1]) - num * 0.75 *  cardDim[1] + height - 90, splitCenter + 0.5 * cardDim[0] + num * 0.35 * cardDim[0], (0.5 * cardDim[1]) - num * 0.75 * cardDim[1] + height - 90), fill = (100, 0, 0))
            
            if num < len(hands[split]):
                draw.rectangle((splitCenter - 0.5 * cardDim[0] + num * 0.35 * cardDim[0] + 2, (-0.5 * cardDim[1]) - num * 0.75 *  cardDim[1] + height - 90 + 2, splitCenter + 0.5 * cardDim[0] + num * 0.35 * cardDim[0] - 2, (0.5 * cardDim[1]) - num * 0.75 * cardDim[1] + height - 90 - 2), fill = (255, 255, 255))
                _, _, textWidth, textHeight = draw.textbbox((0, 0), str(hands[split][num]), font=fnt)

                draw.text((((splitCenter - 0.5 * cardDim[0] + num * 0.35 * cardDim[0]) + 0.5 * (cardDim[0] - textWidth)), ((-0.5 * cardDim[1]) - num * 0.75 *  cardDim[1] + height - 90) + 0.5 * (cardDim[1] - textHeight)), str(hands[split][num]), font=fnt, fill = (0, 0, 0))

# Plays games in real time
def playGamePic():
    # Might want to change menu depending on bot type, like you don't need to wipe if no card coutning
    menu = [[["Scan Cards"], ["Enter Cards Manually"]], [["View Cards"]], [["Exit"]]]

    if not isCam:
        menu.pop(0)

    if "p" in bot.players:
        menu[-2].append(["Other Players'"])
    if "d" in bot.players:
        menu[-2].append(["Dealer's"])

    viewTarget = "u"

    val = ""
    
    disp.image(image)
    print(bot.players["p"].cards)
    while True:
        print(f"menu: {menu}")
        draw.rectangle((0, 0, width, height - 60), fill = (92, 155, 51))


        if viewTarget == "u":
            whoCard = "Your Cards"
        elif viewTarget == "p":
            whoCard = "Other Players'"
        elif viewTarget == "d":
            whoCard == "Dealer's"
        else:
            whoCard == "Cards"
        
        _, _, textWidth, textHeight = draw.textbbox((0, 0), whoCard, font=fnt2)

        draw.text(((width-textWidth)/2, 15), whoCard, font=fnt2, fill = (255, 255, 255))
        dispHands(bot.getHandsTarget(viewTarget))


        disp.image(image)
        val = menuMegaMind(menu, "")

        if val == "Exit":
            return "mainMenu()"

        elif val == "Enter Cards Manually":
            players = manualAdd()
            
            for p in players:
                if p not in bot.players:
                    players.pop[0]
            
            bot.assignAnalyze(players)
            
            if (isCam and len(menu) == 3) or (not isCam and len(menu) == 4):
                menu = [[["Scan Cards"], ["Enter Cards Manually"]], [["New Hand"], ["New Deck"]], [["Buy In"]], [["View Cards"]], [["Exit"]]]

                if not isCam:
                    menu.pop(0)

                if "p" in bot.players:
                    menu[-2].append(["Other Players'"])
                if "d" in bot.players:
                    menu[-2].append(["Dealer's"])
                
        
        

        elif val == "Scan Cards":
            val2 = ""
            menu2 = [[["Continue"]], [["Retry"], ["Exit"]]]
            cam.start()
            while True:
                frame = cam.capture_array()

                camIn = Image.fromarray(frame).rotate(270).resize((int(width * (1 if camRatio > 1 else camRatio)), int(height * (1 if camRatio < 1 else 1 / camRatio))), Image.NEAREST)

                image.paste(camIn, (0, 0))
                disp.image(image)

                val2 = menuMegaMind(menu2, "")

                if val2 == "Continue":
                    f1.client = f1.keyRead()
                    playersRaw = f1.analyzeImagePIL(camIn)
                    print(playersRaw)
                    players = bot.convertAnalyze(playersRaw)
                    menu = [[["Scan Cards"], ["Enter Cards Manually"]], [["New Hand"], ["New Deck"]], [["Buy In"]], [["View Cards"]], [["Exit"]]]

                    if "p" in bot.players:
                        menu[-2].append(["Other Players'"])
                    if "d" in bot.players:
                        menu[-2].append(["Dealer's"])

                    print(f"players: {players}")
                    bot.assignAnalyze(players)
            


                    break

                elif val2 == "Exit":
                    cam.stop()

                    break

                elif val2 == "Retry":
                    menu2 = [[["Retry"], ["Exit"]], [["Continue"]]]
                    pass
        
        elif val == "View Cards":
            viewTarget = "u"
        elif val == "Dealer's":
            viewTarget = "d"
        elif val == "Other Players'":
            viewTarget = "p"
        elif val == "New Hand":
            bot.reset()
            menu = [[["Scan Cards"], ["Enter Cards Manually"]], [["View Cards"]], [["Exit"]]]
            if "p" in bot.players:
                menu[-2].append(["Other Players'"])
            if "d" in bot.players:
                menu[-2].append(["Dealer's"])
            if not isCam:
                menu.pop(0)


        elif val == "New Deck":
            bot.players["p"].countWipe()
            print("New Deck")

        elif val == "Buy In":
            buy = bot.buyIn()

            print(buy)

            if buy:
                txt = f"Bet {buy} Units"
            else:
                txt = "Sit Out"

            _, _, textWidth, textHeight = draw.textbbox((0, 0), txt, font=fnt)

            draw.rectangle((0, width, 0, height - 60), fill=(92, 0, 51))

            draw.text(((width-textWidth)/2, 40), txt, font=fnt, fill = (0, 0, 0))
            
            disp.image(image)
            
            sleep(4)
            menu = [[["Scan Cards"], ["Enter Cards Manually"]], [["New Hand"], ["New Deck"]], [["Buy In"], ["Calculate Move"]], [["View Cards"]], [["Exit"]]]

            if "p" in bot.players:
                menu[-2].append(["Other Players'"])
            if "d" in bot.players:
                menu[-2].append(["Dealer's"])
            if not isCam:
                menu.pop(0)

            

        elif val == "Calculate Move":
            handsI = len(bot.getHands())

            if handsI > 1:
                val2 = ""
                menu2 = [[]]
                for i in range(handsI):
                    menu2[0].append([f"Hand #{i + 1}"])
                
                print(menu2)
                val2 = int(menuMegaMind(menu2, "").strip("Hand #")) - 1
                print(val2)
                bot.hIP(val2)

            try:
                move = bot.makeMove()
            except:
                move = "Error"
            print(move)
            _, _, textWidth, textHeight = draw.textbbox((0, 0), move, font=fnt)

            draw.rectangle((0, width, 0, height - 60), fill=(92, 0, 51))

            draw.text(((width-textWidth)/2, 40), move, font=fnt, fill = (0, 0, 0))
            disp.image(image)    
            sleep(4)


def manualAdd():
    players = {"u": {"cards": [[]], "vals": [0]}, "p": {"cards": [[]], "vals": [0]}, "d": {"cards": [[]], "vals": [0]}}


    # Reversed because a 10 is the most common card, it would be annoying ig it was at the bottom of the menu.

    for p in players:  

        val = ""

        menu = [[["Ace"]]]

        if p == "u":
            txt = "Your Cards"
        
        elif p == "d":
            txt = "Dealer's"
    
        else:
            print(f"p: {p}")
            txt = "Other Players'"

        for i in range(10, 1, -1):
                menu[0].append([str(i)])

        # textWidthS, textHeightS, textWidth, textHeight = draw.textbbox((0, 0), str(players[p]), font=fnt)

        # draw.rectangle(((width - textWidth) / 2 + textWidthS, (height - textHeight - 20) / 2 + textHeightS, (width - textWidth) / 2 + textWidth, (height - textHeight - 20) / 2 + textHeight),fill=(92, 0, 51))
                        
        # draw.text(((width-textWidth)/2, (height-textHeight - 20) / 2), str(players[p]), font=fnt, fill = (255, 255, 255))
        # disp.image(image)
        while True: 

            if val == "Next":
                break
            
            elif val == "Split":
                print(players[p]["cards"])
                print(players[p]["cards"][-1][0])
                # Might break stuff, if in doubt do [] and 0
                players[p]["cards"].append([players[p]["cards"][-1][0]])
                players[p]["vals"].append(players[p]["cards"][-1][0])
                
                menu = [[["Ace"]]]
                for i in range(10, 1, -1):
                    menu[0].append([str(i)])
                
                print(f"Menu Test: {menu}")
                print(f"Players Test: {players}")

                # players[p][1].append(players[p][0][-1][-1])

            elif val.isdigit() and int(val) in range(1, 11):
                players[p]["cards"][-1].append(int(val))
                players[p]["vals"][-1] += int(val)

            
            elif val == "Ace":
                players[p]["cards"][-1].append(1)
                players[p]["vals"][-1] += 1

            elif val == "Exit":
                break

            for card in range(len(players[p]["cards"][-1])):
                    print(f"val: {players[p]['vals'][-1]}")
                    print(f"card: {players[p]['cards'][-1][card]}")
                    if players[p]["cards"][-1][card] == 1 and players[p]["vals"][-1] <= LT - 10:
                        print("Ace Made Higher")
                        players[p]["cards"][-1][card] = 11
                        players[p]["vals"][-1] += 10
                    elif players[p]["cards"][-1][card] == 11 and players[p]["vals"][-1] > LT:
                        print("Ace Made Lower")
                        players[p]["cards"][-1][card] = 1
                        players[p]["vals"][-1] -= 10
            
            if p == "u":
                if players[p]["vals"][-1] >= LT:
                    menu = [[["Next"]], [["Split"]]]

                if len(players[p]["cards"][-1]) == 2:
                    menu.append([["Split"]])
                    menu.append([["Next"]])

            elif p == "d":
                # if max(len(sub) for sub in players[p][0]):
                #     menu = [["Next"]]
                if len(players[p]["cards"][-1]):
                    menu = [[["Next"]]]
                    
            else:
                if not len(players[p]["cards"][-1]):
                    menu.append([["Next"]])

                if players[p]["vals"][-1] >= LT:
                    menu = [[["Next"]]]

            print(f"New Menu: {menu}")

            # textWidthS, textHeightS, textWidth, textHeight = draw.textbbox((0, 0), str(players[p][0]), font=fnt)

            # draw.rectangle(((width - textWidth) / 2 + textWidthS, (height - textHeight - 20) / 2 + textHeightS, (width - textWidth) / 2 + textWidth, (height - textHeight - 20) / 2 + textHeight),fill=(92, 0, 51))
                            
            # draw.text(((width-textWidth)/2, (height-textHeight - 20) / 2), str(players[p][0]), font=fnt, fill = (255, 255, 255))

            draw.rectangle((0, 0, width, 180), fill = (92, 155, 51))

            _, _, textWidth, _ = draw.textbbox((0, 0), txt, font=fnt2)
            draw.text(((width-textWidth)/2, 15), txt, font=fnt2, fill = (255, 255, 255))
            dispHands(players[p]["cards"])
            disp.image(image)
            
            val = menuMegaMind(menu, "")
    
    for p in players:
        players[p] = players[p]["cards"]

    disp.image(image)
    print(f"players 2: {players}")
    return players

def picMoves():
    print("picMoves")
    bot.hardReset()

    try:
        menu = [[["Most Recent"]], [["Manual Input"]], [["Exit"]]]

        high = int(BotIrlBrain.readSave([8])[0])

        for x in range(high + 1):
            menu[0].append([f"pic{x}"])
    
    except Exception as e:
        print (e)
        menu = [[["Manual Input"]], [["Exit"]]]

    print(menu)
    val = ""

    while True:
        draw.rectangle((0, 0, width, height - 60), fill = (92, 155, 51))
        # disp.image(image)

        if val == "Exit":
            return "mainMenu()"
    
        elif val == "Most Recent":
            picIndex = int(BotIrlBrain.readSave([5])[0])

            break
        
        elif val and val[0] == "p" and int(val.strip("pic")) in range(high):
            picIndex = int(val.strip("pic"))
            break

        elif val == "Manual Input":
            break

        val = menuMegaMind(menu, dispPic)

    if val == "Manual Input":
        players = manualAdd()
        

    else:
        #DEBUG
        f1.client = f1.keyRead()
        res = f1.analyzeImage(f"/home/pi/CS2210/Blackjack/pic{picIndex}.jpg")
        print("analyzeImage type:", type(res))
        converted = bot.convertAnalyze(res)
        print("convertAnalyze type:", type(converted))


        picIn = Image.open(f"/home/pi/CS2210/Blackjack/pic{picIndex}.jpg").convert("RGB")
        # picIn = Image.open(f"../hand2Crop.jpg").convert("RGB")
        image.paste(picIn, (0, 0))
        disp.image(image)
        f1.client = f1.keyRead()
        players = bot.convertAnalyze(f1.analyzeImage(f"/home/pi/CS2210/Blackjack/pic{picIndex}.jpg"))
        print(f"Players: {players}")
        # players = bot.convertAnalyze(f1.analyzeImage("../hand2.jpg"))
    
    print(f"players: {players}")
    bot.assignAnalyze(players)  
    print(bot.getHands())
    #handindex
    for i in range(len(bot.getHands())):
        bot.hIP(i)
        print(f"2 hand: i")
        try:
            move = bot.makeMove()
        except:
            move = "Error"
        
        print(move)

        textWidthS, textHeightS, textWidth, textHeight = draw.textbbox((0, 0), move, font=fnt)

        draw.rectangle(((width - textWidth) / 2 + textWidthS, (height - textHeight - 20) / 2 + textHeightS, (width - textWidth) / 2 + textWidth, (height - textHeight - 20) / 2 + textHeight),fill=(92, 0, 51))

        draw.text(((width-textWidth)/2, (height-textHeight - 20) / 2), move, font=fnt, fill = (255, 255, 255))

        disp.image(image)
    menuMegaMind([[["Continue"]]], "")

def mainMenu():
    if isCam:
        menu = [[["Exit"]], [["Camera"]], [["Pic Moves"]], [["Game"]]]
    else:
        menu = [[["Exit"]], [["Pic Moves"]], [["Game"]]]

    val = ""

    draw.rectangle((0, 0, width, 180), fill = (92, 155, 51))
    disp.image(image)
    
    while True:

        if val == "Exit":
            return "EXIT"
        elif val == "Camera":
            return "inputTest()"
        elif val == "Pic Moves":
            return "picMoves()"
        elif val == "Game":
            return "playGamePic()"
        val = menuMegaMind(menu, "")
        
def inputTest():
    draw.rectangle((0, 0, width, height - 60), fill = (92, 155, 51))
    menu = [[["Refresh"], ["Save"]], [["Exit"]]]
    disp.image(image)

    val = ""

    freshCamIn = True
    # cam.configure(cam.create_preview_configuration(transform=Transform(rotation=90)))

    cam.start()
    sleep(0.5)
    while True:
        if val == "Exit":
            cam.stop()

            return "mainMenu()"
        
        elif val == "Refresh":
            print("Refreshing")
            freshCamIn = True
        
        elif val == "Save":
            saveNums = BotIrlBrain.readSave([5, 8])

            saveNums[0] = int(saveNums[0])
            saveNums[1] = int(saveNums[1])

            if saveNums[0] >= saveNums[1]:
                saveNums[0] = 0
            else:
                saveNums[0] += 1        
            # Go back
            
            print(f"saveNums: {saveNums}")
            camIn.convert("RGB").save(f"/home/pi/CS2210/Blackjack/pic{saveNums[0]}.jpg")            
            BotIrlBrain.writeSave([5], [str(saveNums[0])])

        if freshCamIn:
            print('fresh')

            frame = cam.capture_array()

            camIn = Image.fromarray(frame).rotate(270).resize((int(width * (1 if camRatio > 1 else camRatio)), int(height * (1 if camRatio < 1 else 1 / camRatio))), Image.NEAREST)

            image.paste(camIn, (0, 0))
            disp.image(image)
            freshCamIn = False

        # val = menuMegaMind(menu, "")
        
    

def launch():
    if isCam:
        global cam
        cam = Picamera2()

    global bot
    bot = Bot1C()

    crashes = 0
    while True:
            outP = None
            while crashes <= 10:
                try:
                    print(f"Outer: {outP}")
                    if not outP:
                        # Defaults to main menu
                        outP = mainMenu()
                    elif outP == "EXIT":
                        break
                    else:
                        try:
                            outP = exec(outP)
                        except Exception as e:
                            print(f"{outP} could not be run, error: {e})")
                    crashes = 0
                except Exception as e: 
                    print(f"Crash {crashes}/10. Error: {e}")
                    crashes += 1
            
            menu = [[["Cancel"]], [["Close Program"]]]
            val = menuMegaMind(menu, "")

            if val == "Cancel":
                pass
            elif val == "Close Program":
                break
    if isCam:
        cam.close()
    backlight.value = False
        
if __name__ == "__main__":
    # try:
    #     launch()
    # except:
    #     print("Could not launch")

    # try:
    #     if isCam:
    #         cam.stop()
    # except:
    #     print("Camera already closed")
    
    # try:
    #     backlight.value = False
    # except:
    # #     print("Screen already closed")
    # cam = Picamera2()
    # cam.configure(cam.create_preview_configuration(transform=Transform(rotation=90)))

    # cam.start()
    # sleep(0.5)

    # counter = 0
    # while counter < 30:
    #     frame = cam.capture_array()
    #     camIn = Image.fromarray(frame).rotate(90).resize((int(width * (1 if camRatio > 1 else camRatio)), int(height * (1 if camRatio < 1 else 1 / camRatio))), Image.NEAREST)
    #     cam.close()

    #     draw.rectangle((0, 0, width, 180), fill = (92, 155, 51))
    #     image.paste(camIn, (0, 0))
    #     disp.image(image)
    
    #     counter += 1
    print("1234")
    inputTest()
    # exit()