import bridge.Card as Card
from functools import reduce

levelLongNames = ["One",  "Two",  "Three",  "Four",  "Five",  "Six",  "Seven"]
levelRankOrder = list(range(1,  len(levelLongNames)+1))
levelShortNames = list(map(lambda i: str(i),  levelRankOrder))

trumpLongNames = list(Card.suitLongNames + ["Notrump"])
trumpRankOrder = list(range(1,  len(trumpLongNames)+1))
trumpShortNames = list(Card.suitShortNames + ['N'])

callLongNames = list(["Pass"] + levelLongNames + ["Double",  "Redouble"])
callRankOrder = list(range(0,  len(callLongNames)))
callShortNames = list(['P'] + Card.suitShortNames + ['D',  'R'])

sideLongNames = ["East-West",  "North-South"]
sideRankOrder = list(range(1,  len(sideLongNames)+1))
sideShortNames = ["EW",  "NS"]

class Bid:
    def __init__(self,  s,  c=0,  t=0):
        self.side = s
        self.call = c
        self.trump = t
    def valid(self):
        isBid = self.call in levelRankOrder
        isCall = not isBid and self.call in callRankOrder
        isSuit = self.trump in trumpRankOrder
        notSuit = not isSuit and self.trump == 0
        return (isBid and isSuit) or (isCall and notSuit)
    def more_than(self,  prev):
        return self.call > prev.call or self.call == prev.call and self.trump > prev.trump
        # 0 == not valid (not more than prev, or redouble after a bid)
        # 1 == not enough to say, look back to another call
        # 2 == definitely valid (more than prev., double after a bid, redouble after a double)
        # assumption: self and prev both passed valid()
    def valid_first(self):
        isBid = self.call in levelRankOrder
        return isBid or self.call == 0 # first call must be a bid or pass
    def valid_over(self,  prev):
        isBid = self.call in levelRankOrder
        prevBid = prev.call in levelRankOrder
        if isBid and prevBid: # bids can be compared directly
            return 2 if self.more_than(prev) else 0
        elif isBid: # prevBid a call, have to look back to find a lower bid
            return 1
        elif self.call == 0: # pass, always valid
            return 2
        elif self.call == 8: # double, valid over a bid by opposition or pass
            if prevBid:
                return 2 if self.side != prev.side else 0
            elif prev.call == 0:
                return 1
            else:
                return 0
        else: # only valid call left is redouble, valid only over a double by opposition
            if prevBid == 0:
                return 1
            elif prevBid == 8:
                return 2 if self.side != prev.side else 0
            else:
                return 0
                
class BidHistory:
    def __init__(self):
        self.history = []
    def valid(self,  prop):
        if not prop.valid():
            return False
        elif len(self.history) == 0:
            return prop.valid_first()
        else:
            for b in reversed(self.history):
                v = prop.valid_over(b)
                if v == 0 or v == 2:
                    return v == 2
            # fall through, all tests resulted in deferral
            return prop.valid_first()
    def passed_out(self):
        # passed out is 4 calls, all pass
        return len(self.history == 4) and len(filter(lambda b: b.call == 0,  self.history)) == 4
    def passed_around(self):
        # passed around is 3 passes after a non-pass call
        if len(self.history) < 4:
            return False
        elif self.history[len(self.history)-4].call != 0:
            pp = self.history[len(self.history)-3:len(self.history)]
            return len(filter(lambda b: b.call == 0,  pp)) == len(pp)
        else:
            return False
    def bidding_finished(self):
        return self.passed_out() or self.passed_around()
    def add(self,  prop):
        if not self.valid(prop):
            return False
        elif self.bidding_finished():
            return False
        else:
            self.history += [prop]
            return True
