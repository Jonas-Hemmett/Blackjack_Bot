import playerBase as pl
import random
import bots as b1
DS = 1 # Number of decks played with
HS = 1 # Default number of hands
LT = 21 # Card Value limit
COST = 10
SINGLE = True #more than 2 people in real game, treats other players as split hand

class LowBot(pl.Player):
    def __init__(self):
        pl.Player.__init__(self)
    
    def makeMove(self):
        if self.getVal() >= 17:
            return "stay"
        else:
            return "hit"
            
class DeckSim():
    def __init__(self):
        self.deck = []
        
    def createDeck(self):
        deck = []
        for w in range(DS):
            for x in range(1, 4 + 1):
                for y in range(1, 10 + 1):
                    deck.append(y)
                for y in range(1, 3 + 1):
                    deck.append(10)
        
        random.shuffle(deck)
        return deck
    
    def deal(self):
        if not self.deck:
            self.deck = self.createDeck()

        return self.deck.pop()

    
class GameSim():
    def __init__(self, players, cost, prints):
        self.prints = prints
        self.deck = DeckSim()
        self.cost = cost
        self.players = players
        self.ratio = []
        for p in self.players:
            if isinstance(p, pl.Player):
                p.setCost(cost)

    def addCard(self, p):
        p.addCard(self.deck.deal())

    def split(self, p):
        mc = p.popHand()
        p.popVal()

        while mc:
            p.addHand([mc.pop(), self.deck.deal()])

            # p.hand.insert(p.hI, [])

            # p.hIP(p.hI + n)
            # p.addCard(mc[n])
            # p.addCard(self.deck.deal())

        # p.hIP(oldHIP)
        # print(p.hI)
        return True

    def hit(self, p):
        if self.prints:
            print(" " * 4, "Hit!")

        self.addCard(p)

        return True

    def stay(self, p):
        if self.prints:
            print(" " * 4, "Stay")

        return False 
    
    def dDown(self, p):
        if self.prints:
            print(" " * 4, "Double Down")

        p.bankroll -= p.betAmount
        self.addCard(p)
        return False

    def sur(self, p):
        if self.prints:
            print(" " * 4, "sur")
        return False

    def makeMove(self, p):
        return p.makeMove()
    
    def findState(self, p):
        moves = {"hit": False, "stay": False, "dDown": False, "split": False, "sur": False}

        if p.getVal() < LT:
            if isinstance(p, pl.Dealer):
                if len(p.getHand()) == 1:
                    self.addCard(p)

                moves["hit"] = p.getVal() < 17 
      
                moves["stay"] = p.getVal() >= 17

            else:
                moves["hit"] = True
                moves["stay"] = True
                moves["dDown"] = len(p.getHand()) <= 2 and p.bankroll >= p.cost

                moves["split"] = moves["dDown"] and len(set(p.getHand())) <= 1  

                moves["sur"] = len(p.getHands()) <= HS and len(p.getHand()) <= 2 

            return moves            
            
    def reset(self):
        for p in self.players:
                p.reset()

    def newGame(self, rounds):
        print(self.players)
        self.ratio.clear()
        for p in self.players:
            if not isinstance(p, pl.Dealer):
                self.ratio.append({"wins": 0, "losses": 0, "ties": 0})

        self.deck.createDeck()
        playersIn = []

        for _ in range(rounds):
            self.reset()
            playersIn.clear()

            if self.prints:
                print("New Round")
                print(" " * 2, "Dealer's Card")

            for p in self.players:
                if p.buyIn():
                    playersIn.append(p)

            for p in playersIn:
                for x in range(2):
                    if not (x == 2 - 1 and isinstance(p, pl.Dealer)):
                        self.addCard(p)
                    elif self.prints:
                        print(" " * 4, p.getHands())

            for p in playersIn:
                if self.prints:
                    print(" " * 2, f"{str(type(p))[8:-2]}'s Turn")

                turn = True
                while turn:
                    moves = self.findState(p)
                    # print(moves)
                    
                    if self.prints:
                        print(" " * 4, p.getHands())
                    if moves:
                        move = self.makeMove(p)
                        for m in moves:
                            if m == move:
                                if moves[m]:
                                    if not eval(f"self.{m}(p)"):
                                        turn = False
                                else:
                                    print(" " * 4, f"Invalid Move: {m}")
                    else:
                        turn = False


            dealerVal = 0
            for p in playersIn:
                if isinstance(p, pl.Dealer):
                    checkVal = p.getVals()  # Call the method to get values
                    maxVal = max(checkVal) if checkVal else 0  # Handle empty values case
                    if dealerVal < maxVal:
                        dealerVal = maxVal

            if self.prints:
                print(" " * 2, "Results")

            ratI = 0
            for p in playersIn:
                if isinstance(p, pl.Player):
                    for v2 in p.getVals() :
                        print(" " * 4, f"betAmount: {p.betAmount}")
                        print(" " * 4, f"Balance: {p.bankroll:.2f}")     

                        # if self.prints:
                        #     print(f"v2: {v2}, dealerVal: {dealerVal}") ifPrints
                        if (v2 > LT) or  (v2 < dealerVal and dealerVal <= LT):
                            self.ratio[ratI]["losses"] += 1
                                
                            if self.prints:
                                print(" " * 4, f"{str(type(p))[8:-2]} Lost, Balance: {p.bankroll:.2f}")     
                        
                        elif (v2 <= LT) and (v2 == dealerVal):
                            p.bankroll += p.betAmount
                            self.ratio[ratI]["ties"] += 1
                            print(" " * 4, f"{str(type(p))[8:-2]} Tied, Balance: {p.bankroll:.2f}")     

                        else:
                            self.ratio[ratI]["wins"] += 1
                            p.bankroll += 2 * p.betAmount
                            print(" " * 4, f"{str(type(p))[8:-2]} Won, Balance: {p.bankroll:.2f}")     


                        # if dealerVal > LT:
                        #     if v2 <= LT:
                        #         p.bankroll += p.cost * p.payout
                        #         self.ratio[ratI]["wins"] += p.payout
                                
                        #         if self.prints:
                        #             print(" " * 4, f"{str(type(p))[8:-2]} Won, Balance: {p.bankroll:.2f}")
                        #     else:
                        #         p.bankroll += p.cost * p.payout

                        #         self.ratio[ratI]["ties"] += p.payout

                        #         if self.prints:
                        #             print(" " * 4, f"{str(type(p))[8:-2]} Tied, Balance: {p.bankroll:.2f}")
                        # else:
                        #     if v2 > dealerVal and v2 <= LT:
                        #         p.bankroll += 2 * p.cost * p.payout
                        #         self.ratio[ratI]["wins"] += 2 * p.payout
                                
                        #         if self.prints:
                        #             print(" " * 4, f"{str(type(p))[8:-2]} Won, Balance: {p.bankroll:.2f}")

                        #     elif v2 == dealerVal:
                        #         p.bankroll += p.cost * p.payout
                        #         self.ratio[ratI]["ties"] += 2 * p.payout
                                
                        #         if self.prints:
                        #             print(" " * 4, f"{str(type(p))[8:-2]} Tied, Balance: {p.bankroll:.2f}")
                            
                        #     else:
                        #         self.ratio[ratI]["losses"] += p.payout

                        #         if self.prints:
                        #             print(" " * 4, f"{str(type(p))[8:-2]} Lost, Balance: {p.bankroll:.2f}")
                    ratI += 1

        return self.players, self.ratio

class GameBotSim(GameSim):
    def __init__(self, players, cost, prints):
        super().__init__(players, cost, prints)
        # self.translate = {"p":[],"d":[]}

    def makeMove(self, p):
        if isinstance(p, b1.BotSimBrain):
            # p.addO(self.translate, self.findState(p))
            p.setMoves(self.findState(p))
            
        return p.makeMove()

    # def reset(self):
    #     for p in self.players:
    #             p.reset()
    #     # for p in self.translate:
    #     #     self.translate[p].clear()


    # # def add(self, role, card):
    # #     if role == "d":
    # #         self.translate["d"].append(card)
    # #     self.translate["p"].append(card)

    def addCard(self, p):
        card = self.deck.deal()
        p.addCard(card)

        if isinstance(p, pl.Dealer):
            for p2 in self.players:
                if isinstance(p2, b1.BotSimBrain):
                    p2.addCardTarget(card, "d")
        else:
            for p2 in self.players:
                if isinstance(p2, b1.BotSimBrain):
                    p2.addCardTarget(card, "p")
                

            
        # if isinstance(p, pl.Dealer):
        #     self.translate["d"].append(card)
        # self.translate["p"].append(card)


#Fix gethands to show all hands or one hand