import time
import openAIFunctions as f1
import blackjackGameSim as base
import playerBase as pl

# git commit -am "123" 
# git push origin master 

# pic = "C:/Users/gresh/Documents/CS2210/Current/Blackjack/hand.jpg"
DS = 1 # Number of decks played with
HS = 1 # Default number of hands
LT = 21 # Card Value limit
COST = 10
SINGLE = False #more than 2 people in real game, treats other players as split hand

class BotDeck():
    def __init__(self):
        self.hI = 0
        self.hand = [[]]
        self.value = [0]

    def clear(self):
        self.hI = 0
        self.hand = [[]]
        self.value = [0]

    def hIP(self, num): #hI plus
        if num > self.hI:
            for _ in range(num - len(self.hand) + 1):
                self.hand.append([])
                self.value.append(0)
                self.hI = num

            return False
        else:
            self.hI = num
            return True
    
    def addCard(self, card):
        if card:
            self.hand[self.hI].append(card)
            self.value[self.hI] += card

            # Not very efficient but works with splitting
            for card in self.hand[self.hI]:
                if card == 1 and self.value[self.hI] + 10 <= LT:
                    card = 11 
                    self.value[self.hI] += 10
                
                if card == 11 and self.value[self.hI] > LT:
                    card == 1
                    self.value[self.hI] -= 10
            
            self.hand[self.hI].sort()

    def addHandOld(self, hand):
        #Adds to existing hand
        for card in hand:
            self.addCard(card)
                
    def __eq__(self, other):
        return True if isinstance(other, BotDeck) and self.hand == other.hand else False   

    def getHand(self):
        return self.hand[self.hI]

    def addHand(self, hand):
        #adds new hand
        self.value.insert(self.hI, 0)
        self.hand.insert(self.hI, [])

        for card in hand:
            self.addCard(card)

    def popHand(self):
        return self.hand.pop(self.hI)
    
    def popVal(self):
        return self.value.pop(self.hI)
    
    def getHands(self):
        return self.hand
    
    def getVal(self):
        return self.value[self.hI]

    def getVals(self):
        return self.value
    
class BotDeckCC(): #Keeps track of cards in game as well
    def __init__(self):
        BotDeck.__init__(self)
        self.count = 0 # used for true count, bet units are 1 - tcount, negative dont play
        self.numCards = 52 * DS #number of cards played from a deck
        self.hand = {}
        self.cardsCreate()
        self.alg = [-1, 1, 1, 1, 1, 1, 0, 0, 0, -1] #HiLo, lower better for player

    def cardsCreate(self):
        for n in range(10):
            self.hand[n + 1] = [0, 4 * DS]

        self.hand[10][1] *= 4

    def clear(self):
        pass

    def getBet(self, cost):
        print(f"count {self.count}, numCards {self.numCards}")
        bet = self.count / ((self.numCards + 52) // 52) #can be tweaked
        print(bet)
        if bet < 0:
            bet = 0
        elif bet < 1:
            bet += 1
        return bet

    def getHands(self):
        return self.hand
    
    def countWipe(self):
        self.count = 0
        self.numCards = 52 * DS
        self.cardsCreate()

    def addCard(self, card):
        self.count += self.alg[0 if card == 11 else card - 1]
        self.numCards -= 1
        self.cards[1 if card == 11 else card][0] += 1

        assert self.cards[1 if card == 11 else card][0] <= self.cards[1 if card == 11 else card][1]

        if not self.numCards:
            self.countWipe()

class BotBrain(pl.Player):
    def __init__(self):
        pl.Player.__init__(self)
        self.players = {"u": BotDeck(), "d": BotDeck()}
        
    def reset(self):
        for p in self.players:
            self.players[p].clear()

    def hIP(self, num): #hI plus
        return self.players["u"].hIp(num)
    
    def hIPTarget(self, num, who): #hI plus
        if who in self.players:
            return self.players[who].hIp(num)
        else:
            print(f"getHandsTarget !: {who}")

    def getHands(self):
        return self.players["u"].getHands()
    
    def getHandsTarget(self, who):
        if who in self.players:
            return self.players[who].getHands()
        else:
            print(f"getHandsTarget !: {who}")

    def addCard(self, card):
        self.players["u"].addCard(card)
    
    def addCardTarget(self, card, who):
        if who in self.players:
            self.players[who].addCard(card)
        else:
            print(f"addCardTarget !: {who}")

    def buyIn(self):
        if self.bankroll >= self.cost:
            return True
        else: 
            return False
    
    def playRound(self):
        pass

    def clearTarget(self, who):
        if who in self.players:
            self.players[who].clear(hand)
        else:
            print(f"clearTarget !: {who}")

    def addHand(self, hand):
        self.players["u"].addHand(hand)
    
    def addHandTarget(self, hand, who):
        if who in self.players:
            self.players[who].addHand(hand)
        else:
            print(f"addHandTarget !: {who}")

    def addHandOld(self, hand):
        self.players["u"].addHandOld(hand)
    
    def addHandOldTarget(self, hand, who):
        if who in self.players:
            self.players[who].addHandOld(hand)
        else:
            print(f"addHandOldTarget !: {who}")

    def getHand(self):
        return self.players["u"].getHand()

    def getHandTarget(self, who):
        if who in self.players:
            return self.players[who].getHand()
        else:
            print(f"getHandTarget !: {who}")

    def popHand(self):
        return self.players["u"].popHand()

    def popHandTarget(self, who):
        if who in self.players:
            return self.players[who].popHand()
        else:
            print(f"popHandTarget !: {who}")

    def popVal(self):
        return self.players["u"].popVal()
    
    def popValTarget(self, who):
        if who in self.players:
            return self.players[who].popVal() 
        else:
            print(f"popValTarget !: {who}")
    
    def getVal(self):
        return self.players["u"].getVal()
    
    def getValTarget(self, who):
        if who in self.players:
            return self.players[who].getVal()
        else:
            print(f"getValTarget !: {who}")
    
    def getVals(self):
        return self.players["u"].getVals()
    
    def getValsTarget(self, who):
        if who in self.players:
            return self.players[who].getVals()
        else:
            print(f"getVals !: {who}")

    def __str__(self):
        lst = ""
        counter = 0

        for p in self.players:
            if counter > 0:
                lst += ", "
            counter += 1

            lst += f"{p}: {self.players[p].getHands()}"

        return f"Bot Type: {self.__class__.__name__}. Player Hand's: {lst}"
    
class BotSimBrain(BotBrain):
    def __init__(self):
        BotBrain.__init__(self)
        self.needCard = False
        moves = {}
    
    # def addO(self, ps, moves):
    #     for p in ps:
    #         if p in self.players:
    #             self.players[p].clear()
    #             self.players[p].addHandOld(ps[p])

    #     self.moves = moves

    # def addMoves(self, moves):
    #     self.moves = moves

    def setMoves(self, moves):
        self.moves = moves

    def addMoves(self, moves):
        self.moves = moves
        
    def roundStart(self):
        for p in self.players:
            self.players[p].clear()
        self.payout = 2
        self.bankroll -= self.cost
        return True
 
class BotIrlBrain(BotBrain):
    def __init__(self):
        BotBrain.__init__(self)

    def sOut(self):
        pass
    
    def hit(self):
        print("Hit!")
        return True

    def stay(self):
        print("Stay!")
        return True
    
    def split(self):
        print("Split!")
        return True

    def sur(self):
        print("Sur!")
        return True

    def dDown(self):
        print("dDown!")
        return True

    def calcMove(self):
        print("cCalled")
        return True
    
    def convertAnalyze(self, infRaw):
        inf = ""
        
        alpha = {"", " ", "\n", "|", "(", ")", "?", "'", "E", "p", "u", "d", ",", ":", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}

        out = {"p": [[]], "u": [[]], "d": [[]]}

        splh = 0 #split hand for bot, adds other bots as more hands

        inval = ""

        try:
            for c in infRaw:
                inf if c in infRaw else inval += c
            
            print(f"Invalid Characters: {inval}")
                    
            if "E" in inf:
                print("AI gave error")

            if SINGLE:
                inf = inf.replace("p", "u")
            
            # inf = inf.split("\n") #final
            inf = inf.replace("\n", "|") # testing, new lines are wacky
            inf = inf.split("|") # testing, new lines are wacky

            for l1 in inf: 
                if l1: 
                    l1 = l1.split(":")
                    
                    if l1[0] == "u":
                        if splh > 0:
                            out["u"].append([])
                        splh += 1

                    l1[1] = l1[1].split(",")
                    
                    for l2 in l1[1]:
                        out[l1[0]][-1].append(int(l2))
            return out
            
        except Exception as e:
            print(e)
            return f"convertAnalyze Error: {e}"   
    
    # may not need, change though
    # def waitCheck(self):
    #     left = 2
    #     tries = 3 * left

    #     p1 = self.getPicTest()
    #     while tries and left:
    #         time.sleep(1)

    #         p2 = self.getPicTest()

    #         if p1 == p2:
    #             left -= 1
    #         else:
    #             left = 2
    #             tries -= 1

    #         p1 = p2

    #     if left:
    #         print("Nothing found")
    #     else:
    #         self.players = p1

    def playHand(self):
        self.reset()
        print(self.buyIn())

        while True:
            if input("break?"):
                break
            self.assignAnalyze(self.convertAnalyze(input("Hand: ")))
            print(self)
            eval(f"self.{self.makeMove()}()")

    # def playRound(self):
    #     self.waitCheck()

    #     if self.buyIn():
    #         print("started")
    #         #if SINGLE: # For Multiplayer
    #         for hand in self.getHand():
    #             if hand != []:
    #                 while True:
    #                     if eval(f"self.{self.makeMove()}()"):
    #                         self.waitCheck()
    #                     else:
    #                         break
    #                 continue
            
    #         self.players["u"].hIP(0)
            
    #         print("Dealers Turn")

    #         # p = self.players["p"].hand
    #         # u = self.players["u"].hand
    #         # d = self.players["d"].hand
    #         # print(f"player: {p}, User: {u}, Dealer: {d}")

    #         self.waitCheck()

    #         for x in range(len(self.getHand())):
    #             if self.getHand():
    #                 if self.getVal() > max(self.players["d"].getValue()):
    #                     self.bankroll += self.cost * self.payout
    #                     print(f"Won, bankroll:{self.bankroll}")
                    
    #                 elif self.getVal() < max(self.players["d"].getValue()):
    #                     print("Lost")

    #                 else:
    #                     print("Draw")
            
    #         self.payout = 2
            
    #         again = input("Again?")
    #         if self.bankroll and again:
    #             return True
    #         else:
    #             return False

    def assignAnalyze(self, hands):
        for p in self.players:
            self.clearTarget(p)
            for hand in range(len(hands[p])):
                self.hIPTarget(hands - 1, p)
                self.addHandOldTarget(hands[hand - 1], p)

    # def playGame(self):
    #     gotHands = self.getPicTest() #Used for testing, prints values before start

    #     for p in self.players:
    #         break
    #     p = self.players["p"].hand
    #     u = self.players["u"].hand
    #     d = self.players["d"].hand
    #     print(f"player: {p}, User: {u}, Dealer: {d}")
    #     print("Start")

    #     while True: #change getpic stuff after tests
    #         if not self.playRound():
    #             break

    # # def makeMove(self, val): # For testing
    # #     return val
    
    def getPic(self, pic):
        inhands = {}
        for p in self.players:
            inhands[p] = self.players[p].getHands()

        return self.convertAnalyze(f1.analyzeImage(pic), inhands)
    
    def getPicTest(self): # for testing
        while True:
            try:
                inp = input("- to stop, raw player info to keep going: ")

                if inp:
                    inhands = {}
                    for p in self.players:
                        inhands[p] = self.players[p].getHands()

                    return self.convertAnalyze(inp, inhands)
                
                else:
                    break

            except:
                print("Try again")
        
        
        # self.convertAnalyze(f1.analyzeImage(pic))

    def dDown(self):
        BotBrain.dDown()

        self.waitCheck()

        return False

class BotBasicStratBrain(BotBrain):
    def __init__(self): 
        BotBrain.__init__(self)
        self.basicStrats = {"hard": [
            ["hit", "hit", "hit", "hit", "hit", "hit", "hit", "hit", "hit", "hit"], # 5 to 8
            ["hit", "dDown", "dDown", "dDown", "dDown", "hit", "hit", "hit", "hit", "hit"], # 9
            ["dDown", "dDown", "dDown", "dDown", "dDown", "dDown", "dDown", "dDown", "hit", "hit"], # 10
            ["dDown", "dDown", "dDown", "dDown", "dDown", "dDown", "dDown", "dDown", "dDown", "hit"], # 11
            ["hit", "hit", "stay", "stay", "stay", "hit", "hit", "hit", "hit", "hit"], # 12
            ["stay", "stay", "stay", "stay", "stay", "hit", "hit", "hit", "hit", "hit"], # 13
            ["stay", "stay", "stay", "stay", "stay", "hit", "hit", "hit", "hit", "hit"], # 14
            ["stay", "stay", "stay", "stay", "stay", "hit", "hit", "hit", "sur", "hit"], # 15
            ["stay", "stay", "stay", "stay", "stay", "hit", "hit", "sur", "sur", "sur"], # 16
            ["stay", "stay", "stay", "stay", "stay", "stay", "stay", "stay", "stay", "stay"]],# 17+  
        "soft": [
            ["hit", "hit", "hit", "dDown", "dDown", "hit", "hit", "hit", "hit", "hit"], # A2 (13)
            ["hit", "hit", "hit", "dDown", "dDown", "hit", "hit", "hit", "hit", "hit"], # A3 (14)
            ["hit", "hit", "dDown", "dDown", "dDown", "hit", "hit", "hit", "hit", "hit"], # A4 (15)
            ["hit", "hit", "dDown", "dDown", "dDown", "hit", "hit", "hit", "hit", "hit"], # A5 (16)
            ["dDown", "dDown", "dDown", "dDown", "dDown", "stay", "stay", "stay", "stay", "stay"], # A6 (17)
            ["stay", "stay", "stay", "stay", "stay", "stay", "stay", "stay", "stay", "stay"], # A7 (18)
            ["stay", "stay", "stay", "stay", "stay", "stay", "stay", "stay", "stay", "stay"]],# A8 to A10 (19 to 21)
        "pair": [
            ["split", "split", "split", "split", "split", "split", "hit", "hit", "hit", "hit"], # 2,2 or 3,3 (4) (6)
            ["hit", "hit", "hit", "split", "split", "hit", "hit", "hit", "hit", "hit"], # 4,4 (8)
            ["dDown", "dDown", "dDown", "dDown", "dDown", "dDown", "dDown", "dDown", "hit", "hit"], # 5,5 (10)
            ["split", "split", "split", "split", "split", "hit", "hit", "hit", "hit", "hit"], # 6,6
            ["split", "split", "split", "split", "split", "split", "hit", "hit", "hit", "hit"], # 7,7
            ["split", "split", "split", "split", "split", "split", "split", "split", "split", "split"], # 8,8
            ["split", "split", "split", "split", "split", "stay", "split", "split", "stay", "stay"], # 9,9
            ["stay", "stay", "stay", "stay", "stay", "stay", "stay", "stay", "stay", "stay"], # 10,10 (20)
            ["split", "split", "split", "split", "split", "split", "split", "split", "split", "split"]]}# A,A

    def makeMove(self): 
        # self.players["u"].hIP(0)  # Ensure the hand index is set correctly
        # uM = self.players["u"].hand[self.players["u"].hI]
        # uV = self.players["u"].value[self.players["u"].hI]
        # dM = self.players["d"].hand[self.players["d"].hI]
        # dV = self.players["d"].value[self.players["d"].hI]

        uM = self.getHand()
        uV = self.getVal()
        dM = self.players["d"].getHand()
        dV = self.players["d"].getVal()

        move = "stay"
        # print(f"User: {uV} Dealer: {dV}")
        if dV > 11 or len(dM) > 1:
            print(f"Unsupported Dealer Hand: {dV}")

        elif uV < 21:
            if 1 in uM:
                move =  self.basicStrats["pair"][8][dV - 2] if uV == 12 and len(uM) == 2 else self.basicStrats["soft"][uV - 13 if uV < 19 else 6][dV - 2]

            elif len(uM) == 2 and uM[0] == uM[1]:

                move = self.basicStrats["pair"][int(uV / 2) - 3 if uV > 4 else 0][dV - 2]

            else:
                move = self.basicStrats["hard"][(0 if uV < 8 else (uV - 8 if uV < 17 else 9))][dV - 2]
        
        else:
            print("Can't, 21")

        if (((move == "dDown" or move == "split") and self.bankroll >= self.cost)) and len(self.getHand()) > 2 or (move == "sur" and (len(self.getHands()) > HS or len(self.getHand()) > 2)):
            move = "hit"
        
        return move

class BotCountStratBrain(BotBasicStratBrain):
    def __init__(self): 
        BotBasicStratBrain.__init__(self)
        counting = BotDeckCC()

    def roundStart(self):
        # self.bankroll -= self.cost
        
        pBet = self.players["p"].getBet(self.cost)

        self.payout = (2 * pBet) / self.cost

        # pBet = (1 if pBet < 1 and SINGLE else pBet)

        print(f"pBet: {pBet}")
        if pBet <= self.bankroll and pBet:
            self.bankroll -= pBet
            return super().roundStart()
        else: 
            return False
    
    def addCardTarget(self, card, who):
        if who in self.players:
            self.players[who].addCard(card)
            if who == "d":
                self.players["p"].addCard(card)
        else:
            print(f"addCardTarget !: {who}")
 
class Bot1(BotBasicStratBrain, BotIrlBrain):
    def __init__(self): 
        BotBasicStratBrain.__init__(self)
        BotIrlBrain.__init__(self)

        def addCardOther(card, pl):
            self.players[pl].addCard(card)

class Bot2(BotBasicStratBrain, BotSimBrain):
    def __init__(self): 
        BotSimBrain.__init__(self)
        BotBasicStratBrain.__init__(self)

    def makeMove(self):
        pMove = BotBasicStratBrain.makeMove(self)

        if self.moves[pMove]:
            return pMove
        else:
            print(f"Bot caught invalid move: {pMove}")
            return "stay"

class Bot3(BotCountStratBrain, BotSimBrain):
    def __init__(self): 
        BotSimBrain.__init__(self)
        BotCountStratBrain.__init__(self)

    def roundStart(self):
        return BotCountStratBrain.roundStart(self)
    
    # def addO(self, ps, moves):     
    #     for p in ps:
    #         if p in self.players:
    #             self.players[p].clear()
    #             self.players[p].addHandOld(ps[p])
    #             if p != "p":
    #                 self.players["p"].addHandOld(ps[p])
    #     self.moves = moves

    def makeMove(self):
        pMove = BotBasicStratBrain.makeMove(self)

        print(self.moves)
        if self.moves[pMove]:
            return pMove
        else:
            print(f"Bot caught invalid move: {pMove}")
            return "stay"


