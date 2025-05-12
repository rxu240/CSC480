import unittest
import random
from pokerbot import PokerBot, Deck

# class TestDeck(unittest.TestCase):
#     def setUp(self):
#         self.deck = Deck()

#     def test_initial_deck_size(self):
#         # Deck should contain 52 cards initially
#         self.setUp()
#         self.assertEqual(len(self.deck), 52)

#     def test_generate_card_removes_from_deck(self):
#         # generateCard should remove the card from the deck
#         card = self.deck.generateCard()
#         self.assertNotIn(card, self.deck)
#         self.setUp() #reset

#     def test_deck_exhaustion_raises(self):
#         # After drawing 52 cards, the next draw should raise ValueError
#         for _ in range(52):
#             self.deck.generateCard()
#         with self.assertRaises(ValueError):
#             self.deck.generateCard()

# class TestScoreFive(unittest.TestCase):
#     def setUp(self):
#         # Bypass __init__ so we don't run the full game setup
#         self.bot = PokerBot.__new__(PokerBot)

#     def test_high_card(self):
#         # 5 random distinct cards with no combo => category 0
#         cards = [(2, 'C'), (5, 'D'), (8, 'H'), (11, 'S'), (14, 'C')]
#         expected_category = 0
#         score = self.bot.score_five(cards)
#         self.assertEqual(score[0], expected_category)

#     def test_one_pair(self):
#         cards = [(2, 'C'), (2, 'D'), (8, 'H'), (11, 'S'), (14, 'C')]
#         expected_category = 1
#         score = self.bot.score_five(cards)
#         self.assertEqual(score[0], expected_category)

# class TestCompareHands(unittest.TestCase):
#     def setUp(self):
#         self.bot = PokerBot.__new__(PokerBot)

#     def test_two_pair_vs_one_pair(self):
#         board = [(2, 'C'), (2, 'D'), (9, 'H'), (11, 'S'), (14, 'C')]
#         p1 = [(3, 'H'), (3, 'S')]  # will have two pair (3s and 2s)
#         p2 = [(4, 'H'), (5, 'S')]  # will have one pair (2s)
#         score1 = self.bot.find_winner(p1 + board)
#         score2 = self.bot.find_winner(p2 + board)
#         self.assertGreater(score1, score2)

class TestPokerBot():
    poker = PokerBot()

if __name__ == '__main__':
    unittest.main()

