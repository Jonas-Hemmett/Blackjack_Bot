# My new strategy
deck = {}
for i in range(1, 10):
    deck[i] = 4

deck[10] = 16

def handSum(hand):
    #TODO sort better, maybe
    hand.sort(reverse = True)
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

def stand(userHand, dealerHand, deck):
    return dealerScore(userHand, dealerHand, deck)

def hit(userHand, dealerHand, deck, memoVal=None):
    if memoVal is None:
        memoVal = {}

    userVal = handSum(userHand)
    dealerVal = handSum(dealerHand)

    key = (userVal, dealerVal)

    if key in memoVal:
        return memoVal[key]
    
    if userVal > 21:
        ev = -1
        memoVal[key] = ev
        return ev 
    
    if userVal == 21:
        ev = stand(userHand, dealerHand, deck)
        memoVal[key] = ev
        return ev
    
    ev = 0
    totalCards = sum(deck[card] for card in deck)

    if totalCards == 0:
        print("No cards")
        totalCards = 1
    for card in deck:
        if deck[card]:            
            userHandNew = userHand.copy()
            userHandNew.append(card)

            weight = deck[card] / totalCards
            ev += hit(userHandNew, dealerHand, deck, memoVal) * weight
    
    standEv = stand(userHand, dealerHand, deck)
    
    # Make to pick standEv if standEv = hitEv
    if ev > standEv:
        memoVal[key] = ev
        return ev
    else:
        memoVal[key] = standEv
        return standEv

def split(userHand, dealerHand, deck):
    if len(userHand) != 2 or userHand[0] != userHand[1]:
        return -1

    totalCards = sum(deck[card] for card in deck)
    ev = 0


    # like, hit atleast once
    for card in deck:
        if deck[card]:
            userHandNew = [userHand[0], card]  
            weight = deck[card] / totalCards
            ev += weight * hit(userHandNew, dealerHand, deck)

    return 2 * ev

def doubleDown(userHand, dealerHand, deck):
    totalCards = sum(deck[card] for card in deck)
    ev = 0

    # like, hit atleast once
    for card in deck:
        if deck[card]:
            weight = deck[card] / totalCards
            userHandNew = userHand.copy()
            userHandNew.append(card)
            ev += weight * stand(userHandNew, dealerHand, deck)

    return 2 * ev

def dealerScore(userHand, dealerHand, deck):
    dealerVal = handSum(dealerHand)

    ev = 0
    totalCards = sum(deck[card] for card in deck)
    if totalCards == 0:
        print("No cards")
        totalCards = 1
    
    if dealerVal < 17:
        for card in deck:
            if deck[card]:            
                dealerHandNew = dealerHand.copy()
                dealerHandNew.append(card)

                weight = deck[card] / totalCards
                ev += dealerScore(userHand, dealerHandNew, deck) * weight

        return ev
            
    userVal = handSum(userHand)

    if userVal > 21:
        return -1
    if dealerVal > 21:
        return 1
    if userVal > dealerVal:
        return 1
    if userVal < dealerVal:
        return -1
    else:
        return 0


userHand = [6, 7]
dealerHand = [6]

standEv = stand(userHand, dealerHand, deck)
bestEv = standEv
bestName = "Stand"

hitEv = hit(userHand, dealerHand, deck)
if hitEv > bestEv:
    bestEv = hitEv
    bestName = "Hit"

doubleDownEv = doubleDown(userHand, dealerHand, deck)
if doubleDownEv > bestEv:
    bestEv = doubleDownEv
    bestName = "Double Down"

splitEv = split(userHand, dealerHand, deck)
if splitEv > bestEv:
    bestEv = splitEv
    bestName = "Split"

print("- Expected Values -")
print(f"Stand:       {standEv:.2f}")
print(f"Hit:         {hitEv:.2f}")
print(f"Double Down: {doubleDownEv:.2f}")
print(f"Split:       {splitEv:.2f}")
print("- Best Move -")
print(f"Best: {bestName}")