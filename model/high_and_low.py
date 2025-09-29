import random

class HighLowGame:
    def __init__(self, chips=100):
        self.chips = chips
        self.deck = list(range(1, 14))
        random.shuffle(self.deck)
        self.history = []

    def play_round(self, base_card, choice, bet):
        result_card = self.deck.pop()
        outcome = self.judge(base_card, choice, result_card)

        if outcome == "win":
            self.chips += bet
        else:
            self.chips -= bet

        record = {
            "base_card": base_card,
            "choice": choice,
            "result_card": result_card,
            "bet": bet,
            "outcome": outcome,
            "chips_after": self.chips,
            "remaining_deck": self.deck.copy()
        }
        self.history.append(record)
        return record

    def judge(self, base, choice, result):
        if choice == "High" and result > base:
            return "win"
        if choice == "Low" and result < base:
            return "win"
        return "lose"
