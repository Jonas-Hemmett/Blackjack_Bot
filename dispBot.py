# Safely imports bot to be run the PI
from bots import *
class Bot4(BotBasicStratBrain, BotIrlBrain):
    def __init__(self): 
        BotIrlBrain.__init__(self)
        BotCountStratBrain.__init__(self)
        cam = Picamera2()
        config = cam.create_still_configuration()
        cam.configure(config)
        cam.start()
        camRatio = 4 / 3
        
    def playHand(self):
        self.players = self.getPicReal2()
        
        for hand in self.getHand():
            if hand != []:
                while True:
                    move = self.makeMove()
                    print(f"Move: {move} Hand: {self.getHand()}")
                    if not eval(f"self.{move}()"):
                        break
                # continue # might not need