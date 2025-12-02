import openAIFunctions as f1
import playerBase as pl
import copy

DS = 1 # Number of decks played with
HS = 1 # Default number of hands
MH = 16 * DS - 1 # Maximum number of hands
LT = 21 # Card Value limit
COST = 1 # Cost to play a round 
OTHER_PLAYERS = True #more than 2 people in real game, treats other players as split hand
BROUND = 2 # How much bet should be rounded, money to cents, tokens to token

# Stores hand information
class BotDeck():
    def __init__(self):
        self.hI = 0 # The current hand index
        self.hand = [[]] # Hands
        self.value = [0] # Hand values

    # Clears current hand
    def clear(self):
        self.hI = 0
        self.hand = [[]]
        self.value = [0]

    # Goes to a hand index, if the index is out of range more hands are created
    def hIP(self, num): # hI plus
        if num > self.hI:
            for _ in range(num - len(self.hand) + 1):
                self.hand.append([])
                self.value.append(0)
        self.hI = num
        return self.hI
    
    # Adds a card to the hand list
    def addCard(self, card):
        if card:
            self.hand[self.hI].append(card)
            self.value[self.hI] += card

            # Makes sure aces are stored as the right value
            for card in self.hand[self.hI]:
                if card == 1 and self.value[self.hI] + 10 <= LT:
                    card = 11 
                    self.value[self.hI] += 10
                
                if card == 11 and self.value[self.hI] > LT:
                    card == 1
                    self.value[self.hI] -= 10
            
            self.hand[self.hI].sort()

    # Adds to existing hand
    def addHandOld(self, hand):
        for card in hand:
            self.addCard(card)
    
    def __eq__(self, other):
        return True if isinstance(other, BotDeck) and self.hand == other.hand else False   

    # Gets the current hand
    def getHand(self):
        return self.hand[self.hI]

    # Creates a new hand
    def addHand(self, hand):
        self.value.insert(self.hI, 0)
        self.hand.insert(self.hI, [])

        for card in hand:
            self.addCard(card)

    # Pops the current hand
    def popHand(self):
        return self.hand.pop(self.hI)
    
    # Pops the current hand value
    def popVal(self):
        return self.value.pop(self.hI)
    
    # Gets all of the hands
    def getHands(self):
        return self.hand
    
    # Gets the current hand value
    def getVal(self):
        return self.value[self.hI]

    # Gets all of the hand values
    def getVals(self):
        return self.value
    
# Stores card counting info
class BotDeckCC(): # Keeps track of cards in game as well
    def __init__(self):
        BotDeck.__init__(self)
        self.count = 0 # Stores the running count for card counting
        self.numCards = 52 * DS # number of cards played from a deck
        self.cards = {} # A dictionary of all the cards, aces are always stored as 1
        self.cardsCreate()
        self.alg = [-1, 1, 1, 1, 1, 1, 0, 0, 0, -1] # The default card counting algorithm, I'm using Hi-Lo
     
    # Creates a dictonary for all card values, aces are always stored as 1
    def cardsCreate(self):
        for n in range(10):
            self.cards[n + 1] = [0, 4 * DS]

        self.cards[10][1] *= 4

    # Clears current hand, has no hands so does nothing
    def clear(self):
        pass

    # Gets the amount that should be bet, calculated using card counting
    def getBet(self):
        print(f"count {self.count}, numCards {self.numCards}")
        bet = self.count / ((self.numCards + 52) // 52) # Can be tweaked
        if bet < 0:
            bet = 0
        elif bet < 1:
            bet = 1
        return bet

    # Gets all of the cards played by other players
    def getHands(self):
        return self.getCards()

    # Gets all of the cards
    def getCards(self):
        return self.cards
    
    # Resets the running count
    def countWipe(self):
        self.count = 0
        self.numCards = 52 * DS
        self.cardsCreate()

    # Adds a card
    def addCard(self, card):
        self.count += self.alg[0 if card == 11 else card - 1]
        self.numCards -= 1
        self.cards[1 if card == 11 else card][0] += 1

        if not (self.cards[1 if card == 11 else card][0] <= self.cards[1 if card == 11 else card][1]):
            print("card added to many times, resetting the running count is recommended")
        
        # Resets the running count if all cards have been played
        if not self.numCards:
            self.countWipe()

class BotBrain(pl.Player):
    def __init__(self):
        pl.Player.__init__(self)
        self.players = {"u": BotDeck(), "d": BotDeck()}
    
    # def buyInAmount(self, amount):
    #     if self.bankroll >= amount:
    #         self.bankroll -= amount
    #         self.payout = amount / self.cost
    #         return amount

    #     elif self.bankroll == -1:
    #         self.payout = amount / self.cost 
    #         return amount
        
    #     else:
    #         return 0
    
    # Resets everything for new game
    def hardReset(self):
        self.reset()

    # Resets for each round
    def reset(self):
        for p in self.players:
            self.players[p].clear()

    # Goes to the bot's card index, if it is out of range more cards are added
    def hIP(self, num):
        return self.players["u"].hIP(num)
    
    # Goes to a specific player's card index, if it is out of range more cards are added
    def hIPTarget(self, num, who): #hI plus
        if who in self.players:
            return self.players[who].hIP(num)
        else:
            # print(f"getHandsTarget !: {who}")
            pass

    # Gets the all of the bot's hands
    def getHands(self):
        return self.players["u"].getHands()
    
    # Gets all the hands of a specific player
    def getHandsTarget(self, who):
        if who in self.players:
            return self.players[who].getHands()
        else:
            # print(f"getHandsTarget !: {who}")
            pass

    # Adds a card to the bot's hand
    def addCard(self, card):
        self.players["u"].addCard(card)
    
    # Adds a card to the hand of a specific player
    def addCardTarget(self, card, who):
        if who in self.players:
            self.players[who].addCard(card)
        else:
            # print(f"addCardTarget !: {who}")
            pass

    # Buys in for a round
    def buyIn(self):
        # print(f"bankroll: {self.bankroll}. Cost: {self.cost}")
        if self.bankroll >= self.cost:
            self.bankroll -= self.cost
            return self.cost
        
        elif self.bankroll == -1:
            return self.cost
        else: 
            return 0
    
    def playRound(self):
        pass
    
    # Clears a specific player's hand
    def clearTarget(self, who):
        if who in self.players:
            self.players[who].clear()
        else:
            print(f"clearTarget !: {who}")

    def addHand(self, hand):
        self.players["u"].addHand(hand)
    
    def addHandTarget(self, hand, who):
        if who in self.players:
            self.players[who].addHand(hand)
        else:
            print(f"addHandTarget !: {who}")

    # def addHandOld(self, hand):
    #     self.players["u"].addHandOld(hand)
    
    # def addHandOldTarget(self, hand, who):
    #     if who in self.players:
    #         self.players[who].addHandOld(hand)
    #     else:
    #         print(f"addHandOldTarget !: {who}")

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

        return f"Bot Type: {self.__class__.__name__}. Player Hand's: {lst}. bankroll: {self.bankroll}"
    
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

    # Sets the allowable moves
    def setMoves(self, moves):
        self.moves = moves
    
    # Sets the allowable moves
    def addMoves(self, moves):
        self.moves = moves
        
    # def roundStart(self):
    #     for p in self.players:
    #         self.players[p].clear()
    #     self.payout = 2
    #     self.bankroll -= self.cost
    #     return True
 
class BotIrlBrain(BotBrain):
    def __init__(self):
        BotBrain.__init__(self)

    # Reads information from a save file
    @staticmethod
    def readSave(nums):
        out = []
        with open("/home/pi/CS2210/Blackjack/Blackjack/saveData.txt", "r") as file:
                for i, line in enumerate(file):
                    if not nums or i in nums:
                        out.append(line)
                    elif i > max(nums):
                        #Stops early
                        break

        return out

    # Writes to a save file
    @staticmethod
    def writeSave(nums, data):
        out = BotIrlBrain.readSave([])
        
        print(f"out1: {out}")
        counter = 0

        for i in range(len(out)):
            print(f"i1: {i}")
            
            if i in nums:
                print(f"i2: {i}")
                out[i] = f"{data[counter]}\n"
                counter += 1    
            
            if counter >= len(data):
                # Stops early
                break
        out = [str(line) for line in out]
        print(f"out2: {out}")
        try:
            with open("/home/pi/CS2210/Blackjack/Blackjack/saveData.txt", "w") as file:
                file.writelines(out)
        except:
            with open("../saveData.txt", "w") as file:
                file.writelines(out)

    # def readSave(self, nums):
    #     # nums is a tuple of line numbers we want to read, if empty we read all save data.

    #     with open("saveData.txt", "r") as file:
    #         for i, line in enumerate(file):
    #             if (not nums or i in nums) and i == 2 and line.rstrip("\n"):
    #                 self.cost = int(line.rstrip("\n"))
    #                 print("self.cost: {self.cost}")

                    
    
    # If an API key can't be read from file the user can input one

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
    
    # Converts the text output from the AI card recognition into a useable format. 
    @staticmethod
    def convertAnalyze(infRaw):
        inf = ""
        
        # Alphabet for card information
        alpha = {"", " ", "\n", "|", "(", ")", "?", "'", "E", "p", "u", "d", ",", ":", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}

        out = {"p": [[]], "u": [[]], "d": [[]]}

        splh = 0 #split hand for bot, adds other bots as more hands

        inval = ""

        # Removes invalid characters
        try:
            for c in infRaw:
                if c in alpha:
                    inf += c
                else:
                    inval += c
           
            if inval:
                print(f"Invalid Characters: {inval}")

            if "E" in inf:
                print("AI Could not read image")

            # If playing against the dealer, other player's hands are treated as the bot's split hands
            if not OTHER_PLAYERS:
                inf = inf.replace("p", "u")
            
            # Splits for each player
            inf = inf.replace("\n", "|")

            inf = inf.split("|") 

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

    def playGameManual(self):
        self.hardReset()
    
    # Plays a hand
    def playHand(self):
        self.hardReset()
        
        while True:
            self.reset()
            if not input("Round?"):
                break
           
            print(f"recommended bet: {self.players['p'].getBet()}")
            self.buyInAmount(int(input("Bet Amount:")))


            while True:
                self.assignAnalyze(self.convertAnalyze(input("Hand: ")))
                print(self)
                self.hIP(0)
                for hand in range(len(self.getHands())):                    
                    self.hIP(hand)
                    print(f"Hand: {self.getHand()}")
                    eval(f"self.{self.makeMove()}()")
                    if not input("Stay?"):
                        break

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

    # Assigns the input card information into player hands
    def assignAnalyze(self, hands):
        for p in self.players:
            self.clearTarget(p)
        
            for handIndex in range(len(hands[p])):
                self.hIPTarget(handIndex, p)
                
                for card in hands[p][handIndex]:
                    self.addCardTarget(card, p)

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
    
    # Gets a picture of the game
    def getPic(self, pic):
        inhands = {}
        for p in self.players:
            inhands[p] = self.players[p].getHands()

        return self.convertAnalyze(f1.analyzeImage(pic), inhands)
    
    # Bypasses the AI card recogntion, used for testing
    def getPicTest(self):
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

# Bot for basic strategy
class BotBasicStratBrain(BotBrain):
    def __init__(self): 
        BotBrain.__init__(self)

        # Stores every blackjack card combination 
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

    # Makes a move by inputting the player hands into the basic strategy table
    def makeMove(self): 
        uM = self.getHand()
        uV = self.getVal()
        dM = self.getHandTarget("d")
        dV = self.getValTarget("d")

        assert uV != 0 and dV != 0

        move = "stay"
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

        if (((move == "dDown" or move == "split") and (self.bankroll >= self.cost or self.bankroll == -1))) and len(self.getHand()) > 2 or (move == "sur" and (len(self.getHands()) > HS or len(self.getHand()) > 2)):
            move = "hit"
        
        return move

# Bot using card coutning
class BotCountStratBrain(BotBasicStratBrain):
    def __init__(self): 
        BotBasicStratBrain.__init__(self)
        # Needs to store the cards for all other players
        self.players["p"] = BotDeckCC()

    def hardReset(self):
        self.reset()
        self.players["p"].countWipe()
        
    def buyIn(self):
        bet = self.players["p"].getBet()
        print(f"card count: {self.players['p'].numCards}")
        bet = round(self.cost * bet, BROUND)

        if self.bankroll == -1:
            return bet
        
        else:
            if bet > self.bankroll:
                if self.cost <= self.bankroll:
                    self.bankroll -= self.cost
                    return self.cost
                else:
                    return 0
            else:
                self.bankroll -= bet
                return bet


    # def roundStart(self):
    #     # self.bankroll -= self.cost
        
    #     pBet = self.players["p"].getBet()

    #     self.payout = (2 * pBet) / self.cost

    #     # pBet = (1 if pBet < 1 and SINGLE else pBet)

    #     print(f"pBet: {pBet}")
    #     if pBet <= self.bankroll and pBet:
    #         self.bankroll -= pBet
    #         return super().roundStart()
    #     else: 
    #         return False
        
    def hIPTarget(self, num, who): #hI plus
        if who in self.players:
            if who != "p":
                return self.players[who].hIP(num)
        else:
            print(f"getHandsTarget !: {who}")

    def addCardTarget(self, card, who):
        if who in self.players:
            if who != "p":
                self.players[who].addCard(card)
        else:
            print(f"addCardTarget (count)!: {who}")
        
        self.players["p"].addCard(card)

# I developed  this part seperatly, so some conversion is needed
class BotJonasStratBrain(BotCountStratBrain):
    def __init__(self): 
        BotCountStratBrain.__init__(self)
    def handSum(self, hand):
        #TODO sort better, maybe
        hand = sorted(hand, reverse = True)
        valSum = 0
        for card in hand:
            if card != 1:
                valSum += card
            else:
                if valSum + 11 > 21:
                    valSum += 1
                else:
                    valSum += 11
        
        return valSum
    
    def formatDeck(self):
        oldDeck = self.players["p"].getCards()
        deck = {}
        for card in oldDeck :
            played, maxCount = oldDeck[card]
            deck[card] = maxCount - played
        return deck
    def stand(self, userHand, dealerHand, deck, memoVal):
        return self.dealerScore(userHand, dealerHand, deck, memoVal)

    def hit(self, userHand, dealerHand, deck, memoVal):

        userVal = self.handSum(userHand)
        dealerVal = self.handSum(dealerHand)

        key = (tuple(sorted(userHand)), tuple(sorted(dealerHand)), tuple(sorted(deck.items())))

        if key in memoVal:
            return memoVal[key]
        
        if userVal > 21:
            ev = -1
            memoVal[key] = ev
            return ev 
        
        if userVal == 21:
            ev = self.stand(userHand, dealerHand, deck, memoVal)
            memoVal[key] = ev
            return ev
        
        ev = 0
        totalCards = sum(deck[card] for card in deck)

        if totalCards == 0:
            print("No cards")
            totalCards = 1
        for card in deck:
            if deck[card]:  
                weight = deck[card] / totalCards
                deckNew = deck.copy()
                deckNew[card]-= 1         
                userHandNew = userHand + [card]

                ev += self.hit(userHandNew, dealerHand, deckNew, memoVal) * weight
        
        standEv = self.stand(userHand, dealerHand, deck, memoVal)
        
        # Make to pick standEv if standEv = hitEv
        if ev > standEv:
            memoVal[key] = ev
            return ev
        else:
            memoVal[key] = standEv
            return standEv

    def split(self, userHand, dealerHand, deck, memoVal):
        if len(userHand) != 2 or userHand[0] != userHand[1]:
            return -1

        totalCards = sum(deck[card] for card in deck)
        ev = 0


        # like, hit atleast once
        for card in deck:
            if deck[card]:
                weight = deck[card] / totalCards
                deckNew = copy.deepcopy(deck)
                deckNew[card] -= 1
                userHandNew = [userHand[0], card]  
                ev += weight * self.hit(userHandNew, dealerHand, deckNew, memoVal)


        return 2 * ev

    def doubleDown(self, userHand, dealerHand, deck, memoVal):
        totalCards = sum(deck[card] for card in deck)
        ev = 0

        # like, hit atleast once
        for card in deck:
            if deck[card]:
                weight = deck[card] / totalCards
                deckNew = deck.copy()
                deckNew[card] -= 1
                userHandNew = userHand + [card]
                ev += weight * self.stand(userHandNew, dealerHand, deckNew, memoVal)

        return 2 * ev

    def dealerScore(self, userHand, dealerHand, deck, memoVal):

        dealerVal =  self.handSum(dealerHand)
        userVal = self.handSum(userHand)

        key = (tuple(sorted(userHand)), tuple(sorted(dealerHand)), tuple(sorted(deck.items())))

        if key in memoVal:
            return memoVal[key]
        ev = 0
        totalCards = sum(deck[card] for card in deck)
        if totalCards == 0:
            print("No cards")
            totalCards = 1
        
        if dealerVal < 17:
            for card in deck:
                if deck[card]: 
                    weight = deck[card]/ totalCards
                    deckNew = deck.copy()
                    deckNew[card] -= 1          
                    dealerHandNew = dealerHand + [card]

                    ev += self.dealerScore(userHand, dealerHandNew, deckNew, memoVal) * weight

            return ev
                
        result = 0

        if userVal > 21:
            result = -1
        if dealerVal > 21:
            result = 1
        if userVal > dealerVal:
            result = 1
        if userVal < dealerVal:
            result = -1
        
        memoVal[key] = result
        return result

    def makeMove(self): 
        user = self.getHand().copy()
        dealer = self.getHandTarget("d").copy()
        deck = self.formatDeck()
        memo = {}


        bestEv = self.stand(user, dealer, deck, memo)
        move = "stay"

        ev = self.hit(user, dealer, deck, memo)
        if ev > bestEv:
            move = "hit"
            bestEv = ev
        
        ev = self.doubleDown(user, dealer, deck, memo)
        if ev > bestEv:
            move = "dDown"
            bestEv = ev
        
        ev = self.split(user, dealer, deck, memo)
        if ev > bestEv:
            move = "split" 
            bestEv = ev

        return move
        
        
class Bot1(BotBasicStratBrain, BotIrlBrain):
    def __init__(self): 
        BotBasicStratBrain.__init__(self)
        BotIrlBrain.__init__(self)

        def addCardOther(card, pl):
            self.players[pl].addCard(card)

class Bot1C(BotCountStratBrain, BotIrlBrain):
    def __init__(self): 
        BotIrlBrain.__init__(self)
        BotCountStratBrain.__init__(self)

#   def assignAnalyze(self, hands):
#         for p in self.players:
#             self.clearTarget(p)
        
#             for handIndex in range(len(hands[p])):
#                 self.hIPTarget(handIndex, p)
                
#                 for card in hands[p][handIndex]:
#                     self.addCardTarget(card, p)     

    def assignAnalyze(self, new):
        countCards = self.players["p"].getCards()
        lst = []
        for p in new:
            if p in self.players and p != "p":
                self.clearTarget(p)
                for handsIndex in range(len(new[p])):
                    
                    lst += new[p][handsIndex]
                    
                    self.players[p].hIP(handsIndex)
                    self.players[p].addHandOld(new[p][handsIndex])
        
        new["p"][0] += new["p"][1:]
        new["p"][0] += lst

        for card in new["p"][0]:

            ind = 1 if card == 11 else card
            assert ind > 0 and ind < 11
            
            if len(countCards[ind]) == 2:
                countCards[ind].append(countCards[ind][0])
                
            if countCards[ind][2] > 0:    
                countCards[ind][2] -= 1
            else:
                self.players["p"].addCard(card)
        
        for card in countCards:
            if len(countCards[card]) == 3:
                countCards[card].pop(2)
            

                
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

    # def roundStart(self):
    #     return BotCountStratBrain.roundStart(self)
    
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


class Bot4(BotJonasStratBrain, BotSimBrain):
    def __init__(self): 
        super().__init__()

    # def roundStart(self):
    #     return BotCountStratBrain.roundStart(self)
    
    # def addO(self, ps, moves):     
    #     for p in ps:
    #         if p in self.players:
    #             self.players[p].clear()
    #             self.players[p].addHandOld(ps[p])
    #             if p != "p":
    #                 self.players["p"].addHandOld(ps[p])
    #     self.moves = moves

    def makeMove(self):
        pMove = BotJonasStratBrain.makeMove(self)

        print(self.moves)
        if self.moves[pMove]:
            return pMove
        else:
            print(f"Bot caught invalid move: {pMove}")
            return "stay"