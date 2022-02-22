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
        return f'Current chips balance: {self.total}'

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
        _hand = ''
        for card in self.cards:
            _hand += ' ' + card
        return _hand

    def add_card(self, card):
        """
        Add a single card to the hand. If the card is an Ace, add it to the Ace count.
        """
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':  # Count aces
            self.aces += 1

    def adjust_for_ace(self):
        """
        If user has at least one ace and hand value goes over 21, reduce hand value by 10 (ace goes from 11 -> 1)
        """
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


# Set up game
game_on = True
deck = Deck()
deck.shuffle()
player_hand = Hand()
dealer_hand = Hand()
bankroll = Chips()


def play_again():
    """
    Let the player decide if they would like to play another hand
    """
    answer = ''
    while answer not in ['y', 'n']:  # Validate input
        answer = input("Would you like to play again? Y/N").lower()
        if answer == 'y':
            return True
        elif answer == 'n':
            return False


while game_on:
    """
    Game logic
    """

    # Prompt player for a bet
    print(bankroll)
    bankroll.bet = int(input("Please select an amount to wager: "))
    while bankroll.bet > bankroll.total:  # Make sure they're not betting more than they have
        bankroll.bet = int(input(f"That's more than you have left! The number entered must be less than "
                                 f"{str(bankroll)}.\n"
                                 f"Please select an amount to wager"))

    # Deal cards to player and dealer
    for i in [1, 2]:
        player_hand.add_card(deck.remove_card())
        dealer_hand.add_card(deck.remove_card())

    # Tell the player what their cards are and what the dealer's face-up card is
    print(f"You are showing {str(player_hand)} for a total of {player_hand.value}")
    print(f"The dealer is showing {str(dealer_hand[1])}")

    player_turn = True  # Time for the player to choose to hit or stay
    while player_turn:
        action = input("Would you like to hit or stay? ").lower()
        while action not in ['hit', 'stay']:  # Check that they are entering valid command
            print("Invalid input. Please enter only the word 'hit' or 'stay'.")
            action = input("Would you like to hit or stay? ").lower()

        if action == 'hit':
            player_hand.add_card(deck.remove_card())
            print(f"You have pulled the {player_hand[-1]}. Your hand is now worth {player_hand.value}")
            if player_hand.value > 21:
                print("Bust! You lose!")
                player_turn = False
                game_on = play_again()
                bankroll.lose_bet()










