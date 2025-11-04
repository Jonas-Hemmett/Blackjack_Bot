
DS = 1 # Number of decks played with
HS = 1 # Default number of hands
LT = 21 # Card Value limit
COST = 10
SINGLE = True #more than 2 people in real game, treats other players as split hand

class Person:
    def __init__(self):
        self.hand = [[]]  * HS
        self.hI = 0
        self.moves = {}
        self.value = [0]
    
    def addHand(self, hand):
        self.hand.insert(self.hI, [])
        self.value.insert(self.hI, 0)

        for card in hand:
            self.addCard(card)

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
    
    def popHand(self):
        return self.hand.pop(self.hI)
    
    def popValTarget(self):
        return self.value.pop(self.hI)
    
    def getHand(self):
        return self.hand[self.hI]

    def getHands(self):
        return self.hand
     
    def getHi(self):
        return self.hI
    
    def getVal(self):
        return self.value[self.hI]

    def getVals(self):
        return self.value
    
    def calcMoves(self):
        if self.value[self.hI] >= 21:
            return True
        else:
            return False

    def buyIn(self):
        self.hand = [[]]  * HS
        self.value = [0]
        return True

    def reset(self):
        self.hand = [[]]  * HS
        self.value = [0]
        
    def addCard(self, card):
        # print(f"hI: {self.hI}") ifPrint
        self.hand[self.hI].append(card)
        self.value[self.hI] += card

        # Not very efficient but works with splitting
        for ace in self.hand[self.hI]:
            if ace == 1 and self.value[self.hI] + 10 <= LT:
                ace = 11 
                self.value[self.hI] += 10
            #Elif should be fine, changed later
            elif ace == 11 and self.value[self.hI] > LT:
                ace == 1
                self.value[self.hI] -= 10
        
        if self.value[self.hI] >= 21: 
            return True 
        else: 
            return False

class Player(Person):
    def __init__(self):
        Person.__init__(self)
        self.bankroll = 1000000
        self.payout = 0
        self.cost = 1

    def setCost(self, cost):
        self.cost = cost

    def buyIn(self):
        self.payout = 2
        self.bankroll -= self.cost
        return True

    # def calcMoves(self):
    #     if Person.calcMoves(self):
    #         return True

    #     if len(self.hand[self.hI]) == 2:
    #         self.moves["dDown"] = True if self.bankroll >= self.cost else False
           
    #         self.moves["split"] = True if (self.hand[self.hI][0] == self.hand[self.hI][1] or (self.hand[self.hI][0] == (1 or 11) and self.hand[self.hI][1] == (1 or 11))) else False
            
    #         self.moves["sur"] = True if len(self.hand) <= HS else False
    #     self.moves["hit"] = True

    #     self.moves["stay"] = True

    #     return False
        
    # def split(self, card1, card2):
    #     self.value[self.hI] -= self.hand[self.hI][-1]
    #     self.value.insert(self.hI + 1, 0)
    #     self.hand.insert(self.hI + 1, [])
    #     self.hI += 1
    #     self.addCard(self.hand[self.hI - 1].pop())
    #     self.addCard(card1)
    #     self.hI -= 1
    #     self.addCard(card2)

    #     return 1

    # def split(self):
    #     pass

    # def dDown(self):
    #     self.bankroll -= COST
    #     self.payout = 2
    #     self.hit()
    #     self.stay()

    # def sur(self):
    #     self.payout = 0.5
    #     self.stay()

class Dealer(Person):
    def __init__(self):
        Person.__init__(self)
        # self.hiddenCard = []

    # def reveal(self):
    #     self.hand[self.hI][1] = self.hiddenCard.pop(self.hI)

    # def calcMoves(self):
    #     if self.moves > 0: # Checks if person can make a move
    #         if self.value[self.hI] >= LT:
    #             self.stay()
    #         else:
    #             self.moves = 2 if self.value[self.hI] <= 16 else 3
    #     return self.moves
    # def calcMoves(self):
    #     if super().calcMoves():
    #         return True

    #     # if self.hiddenCard[self.hI]:
    #     #     self.reveal()
    #     self.moves["stay"] = False if self.value[self.hI] <= 16 else True
    #     self.moves["hit"] = True
    #     return False


    # def addCard(self, card):
    #     # Hides card
    #     print(f"dcard: {card}, hidden: {self.hiddenCard}")
    #     if len(self.hand[self.hI]) == 1:
    #         print("hidden")
    #         self.hiddenCard.insert(self.hI, card)
    #         print(f"hiddencheck: {self.hiddenCard}")
    #     # else:
    #     #     if len(self.hand[self.hI]) == 2 and self.hiddenCard and self.hiddenCard[self.hI]:
    #     #         self.reveal()
                
    #     #     super().addCard(card)
    #     #     self.value[self.hI] += card
    #     # return True #used to be 1
    #     else:
    #         super().addCard(card)

class User(Player):
    def __init__(self):
        Player.__init__(self)


    def makeMove(self):
        # self.calcMoves()

        # print(self.getHands())
        return input("Move: ")

        # if testi == "2":
        #     print("added")
        #     moves = self.addCard(self.deck.deal())
        # elif testi == "3":
        #     moves = self.stay()
        # elif testi == "4":
        #     moves = self.dDown(self.deck.deal())
        # elif testi == "5":
        #     moves = self.split(self.deck.deal(), self.deck.deal())
        #     return split()
class UserDealer(Dealer):
    def __init__(self):
        Dealer.__init__(self)
    
    def makeMove(self):
        return input("Dealer move: ")

class BotDealer(Dealer):
    def __init__(self):
        Dealer.__init__(self)
    
    def makeMove(self):
        if self.getVal() >= 17:
            return "stay"
        else:
            return "hit"
