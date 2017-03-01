from functools import reduce
from random import shuffle

suitLongNames = ["Clubs", "Diamonds",  "Hearts",  "Spades"]
suitShortNames = ['C',  'D',  'H', 'S']
suitRankOrder = list(range(1,  len(suitShortNames)+1))

rankLongNames = ["Deuce",  "Trey",  "Four",  "Five",  "Six",  "Seven",  "Eight",  "Nine",  "Ten",  "Jack",  "Queen",  "King",  "Ace"]
rankShortNames = ['2', '3', '4',  '5', '6',  '7',  '8',  '9',  'T',  'J',  'Q',  'K',  'A']
rankRankOrder = list(range(2,  len(rankShortNames)+2))
# rPC[0], rPC[1] don't map to anything, so rank 2:14 can be used as sn index without offset
rankPointCount = [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  2,  3,  4]

playerLongNames = ["West",  "North",  "East",  "South"]
playerShortNames = ['W',  'N',  'E',  'S']
playerRankOrder = list(range(1,  len(playerShortNames)+1))

class Card :
    def setOrder(self,  o):
        self.order = o
        return self
    def __init__(self,  s,  r):
        self.suit = s
        self.rank = r
        self.setOrder(0)
    def short_name(self):
        return rankShortNames[self.rank-2]+suitShortNames[self.suit-1]
    def long_name(self):
        return rankLongNames[self.rank-2]+" of "+suitLongNames[self.suit-1]
        
cardsInDeck = len(suitRankOrder)*len(rankRankOrder)
cardsInHand = cardsInDeck/len(playerRankOrder)

class Hand :
    def deal_cards(self,  d):
        self.cards = list(filter(lambda c: (c.order % len(playerRankOrder)) == (self.player - 1),  d.cards))      
        self.cards.sort(key=lambda c: c.suit*len(rankRankOrder)+c.rank,  reverse=True)
    def __init__(self,  p,  d):
        self.player = p
        self.cards = []
        self.deal_cards(d)
    def short_list(self):
        return list(map(lambda c: c.short_name(),  self.cards))
    def long_list(self):
        return list(map(lambda c: c.long_name(),  self.cards))
    def suit_count(self):
        self.countBySuit = [0,  0,  0,  0]
        for c in range(0,  len(self.cards)):
            card = self.cards[c]
            self.countBySuit[card.suit-1] += 1
        return self.countBySuit
    def hcp_count(self):
        return reduce(lambda p,  c: p + rankPointCount[c.rank],  self.cards,  0)
class Deck :
    def order(self,  ord):
        self.cards = list (map(lambda c,  o: c.setOrder(o),  self.cards,  ord))
        self.cards.sort(key=lambda c: c.order)
        return self.cards
    def __init__(self):
        # 2, 3, 4 ... A, 2, 3, 4 ... A etc.
        ranks = rankRankOrder * len(suitRankOrder)
        # C, C ... C, D, D ... D etc.
        suits = reduce(lambda a,  s: a + ([s] * len(rankRankOrder)),  suitRankOrder,  [])
        self.cards = list(map(lambda s,  r: Card(s,  r),  suits,  ranks))
    def deal(self):
        self.hands = list(map(lambda p: Hand(p,  self),  playerRankOrder))
        
class NewDeck(Deck):
    def order(self):
        ord = list(range(0,  cardsInDeck))
        return super().order(ord)
    def __init__(self):
        super().__init__()
        self.cards = self.order()
        self.deal()

class ShuffledDeck(Deck):
    def order(self):
        ord = list(range(0,  cardsInDeck))
        shuffle(ord)
        return super().order(ord)
    def __init__(self):
        super().__init__()
        self.cards = self.order()
        self.deal()
        
d = ShuffledDeck()
h = list(map(lambda p,  h: playerShortNames[p-1] + " : " + str(h.short_list()) + ", " + str(h.hcp_count()) + ", " + str(h.suit_count()),  playerRankOrder,  d.hands))
pass
