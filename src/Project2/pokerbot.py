import random, itertools, time
from collections import Counter

class PokerBot:
    def __init__(self):
        self.deck = Deck()
        self.time_budget = 10.0
        self.phase = 0
        self.p1_cards = [self.deck.generateCard(), self.deck.generateCard()]
        self.known_river_cards = []
        print("Final Result: "+ self.start_game())
    
    def start_game(self):
        total_iterations = 0
        total_wins = 0

        while self.phase < 4:
            start = time.perf_counter()
            wins = 0
            iterations = 0

            if self.phase == 1:
                self.known_river_cards = [self.deck.generateCard(), self.deck.generateCard(), self.deck.generateCard()]
            elif self.phase == 2 or self.phase ==3:
                self.known_river_cards.append(self.deck.generateCard())

            while (time.perf_counter() - start <= self.time_budget):
                iterations+=1
                if self.deal_cards():
                    wins+=1
            self.phase+=1
            total_wins+=wins
            total_iterations+=iterations
            
        win_rate = total_wins / total_iterations if total_iterations else 0.0
        if win_rate > 0.5:
            return "Stay"
        return "Fold"
    
    def deal_cards(self):
        sim_deck = self.deck.copy()
        p2_cards = [sim_deck.generateCard(), sim_deck.generateCard()]
        river_cards = []

        if self.phase==0:
            #deal full river
            river_cards = [sim_deck.generateCard(), sim_deck.generateCard(), sim_deck.generateCard(), sim_deck.generateCard(), sim_deck.generateCard()]

        elif self.phase==1:
            #deal other river cards
            river_cards = [sim_deck.generateCard(), sim_deck.generateCard()]

        elif self.phase==2:
            #deal river card
            river_cards = [(sim_deck.generateCard())]

        river = self.known_river_cards + river_cards
        win=self.calc_scores(p2_cards, river)
        return win
    
    def calc_scores(self, p2cards, river):
        p1cards = self.p1_cards+river
        p2cards.extend(river)
        #simulate 
        p1_score = self.find_winner(p1cards)
        p2_score = self.find_winner(p2cards)

        if p1_score >= p2_score:
            return True
        if p1_score < p2_score:
            return False
    
    def find_winner(self, cards):
        return max(self.score_five(cards) 
                for cards in itertools.combinations(cards, 5))

    def score_five(self, cards):
        """Return a tuple (category, *kickers) for exactly 5 cards."""
        # cards: list of (rank_int, suit_char)
        VALUE_MAP = {r: r for r in range(2, 15)}
        vals = sorted((VALUE_MAP[r] for r, _ in cards), reverse=True)
        suits = [s for _, s in cards]
        counts = Counter(vals)
        counts_by_freq = counts.most_common()  # [(val, freq), ...] sorted by freq then val

        # check for straight (and straight flush)
        unique_vals = sorted(set(vals), reverse=True)
        # handle wheel straight A-5
        if unique_vals[:5] == [14, 5, 4, 3, 2]:
            straight_high = 5
        else:
            straight_high = next((unique_vals[i]
                                for i in range(len(unique_vals) - 4)
                                if unique_vals[i]   - unique_vals[i+4] == 4),
                                None)

        flush_suit = next((s for s in "CDHS"
                        if suits.count(s) >= 5), None)
        if flush_suit:
            flush_cards = sorted([VALUE_MAP[r] for r, s in cards if s == flush_suit],
                                reverse=True)[:5]
        # straight flush?
        if flush_suit and straight_high:
            # check if those straight cards are all in flush_suit
            sf_cards = [c for c in cards 
                        if VALUE_MAP[c[0]] in {straight_high, straight_high-1, straight_high-2,
                                            straight_high-3, straight_high-4}
                        and c[1] == flush_suit]
            if len(sf_cards) == 5:
                return (8, straight_high)  # 8 = Straight Flush

        # Four of a Kind
        if counts_by_freq[0][1] == 4:
            four_val = counts_by_freq[0][0]
            kicker = max(v for v in vals if v != four_val)
            return (7, four_val, kicker)

        # Full House
        if counts_by_freq[0][1] == 3 and counts_by_freq[1][1] >= 2:
            three_val = counts_by_freq[0][0]
            pair_val  = counts_by_freq[1][0]
            return (6, three_val, pair_val)

        # Flush
        if flush_suit:
            return (5, *flush_cards)

        # Straight
        if straight_high:
            return (4, straight_high)

        # Three of a Kind
        if counts_by_freq[0][1] == 3:
            three_val = counts_by_freq[0][0]
            kickers = [v for v in vals if v != three_val][:2]
            return (3, three_val, *kickers)

        # Two Pair
        if counts_by_freq[0][1] == 2 and counts_by_freq[1][1] == 2:
            high_pair, low_pair = counts_by_freq[0][0], counts_by_freq[1][0]
            kicker = next(v for v in vals if v not in (high_pair, low_pair))
            return (2, high_pair, low_pair, kicker)

        # One Pair
        if counts_by_freq[0][1] == 2:
            pair_val = counts_by_freq[0][0]
            kickers = [v for v in vals if v != pair_val][:3]
            return (1, pair_val, *kickers)

        # High Card
        return (0, *vals[:5])

class Deck(list):
        def __init__(self, cards=None):
            super().__init__()
            if cards is None:
                self.extend((rank, suit) 
                    for rank in range(2, 15) 
                    for suit in ['C', 'D', 'H', 'S'])
            else:
                self.extend(cards)
        
        def generateCard(self):
            suits = ['C', 'D', 'H', 'S']
            while True:
                if len(self) ==0:
                    raise ValueError
                card = (random.randint(2,14), random.choice(suits)) 
                try: 
                    self.remove(card)
                    return card
                except ValueError as e:
                    continue
        
        def copy(self):
            return Deck(self)
            