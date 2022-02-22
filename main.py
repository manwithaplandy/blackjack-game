"""
This is a game of Blackjack. There are two players - a computer dealer and a human
There is a full deck of 52 cards.
The Human player has a bankroll with money in it. From that bank, the human places a bet.
The player starts with 2 cards face-up. Dealer starts with 1 face up and 1 face down.
Player goal is to get closer to 21 than the dealer without going over.
Player has two options - Hit (receive another card) and Stay (stop receiving cards).
Once player has finished, computer's turn. If player is still under 21, dealer hits until they beat the player or bust.
Ways game can end:
    1. Player hits and goes over 21, dealer gets the money
    2. Computer beats the player - higher total than player but under 21, dealer gets the money
    3. Player wins after computer done - If player is under 21 and computer dealer busts, human doubles their money
Rules:
    1. Face cards count as value of 10
    2. Aces can be either 1 or 11, whichever is preferable to the player
"""
import random

# Define card attributes and values
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
chip_colors = {1: 'Red', 5: 'Blue', 10: 'Green', 20: 'Black', 50: 'White'}


class Card:
    """
    Class for each card object in the deck
    """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f'The {self.rank} of {self.suit}.'


class Deck:
    """
    Class for the main deck from which cards are dealt
    """
    def __init__(self):
        self.all_cards = []

        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))

    def remove_card(self):

        return self.all_cards.pop(0)

    def shuffle(self):

        random.shuffle(self.all_cards)


class Chips:
    """
    Keep track of the player's chips
    """
    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def __str__(self):
        return f'You currently have {self.total}'

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


class Hand:
    """
    Keep track of the cards in the player's hand
    """
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def __str__(self):
        return f'The current number of cards in your hand are: {len(self.cards)}'

    def add_cards(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':  # Count aces
            self.aces += 1

    def adjust_for_ace(self):

        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


# Set up game
game_on = True
main_deck = Deck()
main_deck.shuffle()
player_hand = Hand()
dealer_hand = Hand()
bankroll = Chips()


while game_on:

