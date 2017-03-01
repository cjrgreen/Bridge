from context import Card
import unittest
from functools import reduce

class DealtHandsUnitTests(unittest.TestCase):
    def setUp(self):
        self.deck = Card.ShuffledDeck()
    def allCardsInDeck(self):
        self.assert_(len(self.deck.cards) == 52,  "not 52 cards in deck")
    def allCardsInHands(self):
        fullHands = list(map(lambda h: 1 if (len(h.cards) == 13) else 0,  self.deck.hands))
        self.assert_(reduce(lambda c,  h: c + h,  fullHands,  0) == 4,  "not 13 cards in some hand")
    def noDupsInHands(self):
        withoutDups = list(map(lambda h: 1 if (len(set(h.cards)) == 13) else 0,  self.deck.hands))
        self.assert_(reduce(lambda c,  h: c + h,  withoutDups,  0) == 4,  "duplicates in some hand")
    def noDupsBetweenHands(self):
        hl = [1,  1,  1,  2,  2,  3]
        hr = [2,  3,  4,  3,  4,  4]
        withoutDups = list(map(lambda h1,  h2: 1 if (len(set(self.deck.hands[h1-1].cards) & set(self.deck.hands[h2-1].cards))) == 0 else 0, hl, hr))    
        self.assert_(reduce(lambda c,  h: c + h,  withoutDups,  0) == 6,  "duplicates between some hands")
    def noForeignCards(self):
        cardsInDeck = list(map(lambda h: 1 if (len(set(h.cards) & set(self.deck.cards))) == 13 else 0, self.deck.hands))    
        self.assert_(reduce(lambda c,  h: c + h,  cardsInDeck,  0) == 4,  "foreign cards in some hands")
    def validPointCounts(self):
        hcpCounts = list(map(lambda h: h.hcp_count(),  self.deck.hands))
        self.assert_(reduce(lambda p,  q: p + q,  hcpCounts,  0) == 40,  "high card points do not add up to 40")
        self.assert_(len(list(filter(lambda p: p < 0 or p > 37,  hcpCounts))) == 0,  "too many high card points in some hand")

class DealtHandsUnitTestSuite(unittest.TestSuite):
    def __init__(self):
        super().__init__(map(
            DealtHandsUnitTests,  
            ["allCardsInDeck",  
                "allCardsInHands",  
                "noDupsInHands",  
                "noDupsBetweenHands",  
                "noForeignCards",  
                "validPointCounts"
            ]))
        
runner = unittest.TextTestRunner()
suite = DealtHandsUnitTestSuite()
runner.run(suite)
