"""
This is a game of Blackjack. There are two players - a computer dealer and a human player.
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

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        self.face_up = True

    def __str__(self):
        if self.face_up:
            return f'The {self.rank} of {self.suit}.'
        else:
            pass

    def flip(self):
        if self.face_up:
            self.face_up = False
        else:
            self.face_up = True


class Deck:

    def __init__(self):
        self.all_cards = []

        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))

    def remove_card(self):

        return self.all_cards.pop(0)

    def shuffle(self):

        return random.shuffle(self.all_cards)


class Chip:

    def __init__(self, value):
        self.value = value
        self.color = chip_colors[value]

    def __str__(self):
        return f'This chip is {self.color} with a value of {self.value}'


class Hand:

    def __init__(self):
        self.cards = []

    def __str__(self):
        return f'The current number of cards in your hand are: {len(self.cards)}'

    def print_hand(self):
        str_hand = []
        for card in self.cards:
            str_hand.append(str(card))
        return str_hand

    def value(self):
        # Find total points value for hand
        total = 0
        has_ace = False
        for card in self.cards:
            if card.rank == 'Ace':  # Determine if player has Ace in their hand
                if total + 11 > 21:
                    total += 1
                    has_ace = True
                else:
                    total += 11
                    has_ace = True
            else:
                total += card.value
        if total > 21 and has_ace:
            return total - 10
        else:
            return total


class Player:
    # Player has bankroll and hand, and bankroll has a total value equal to adding up all chips
    def __init__(self):
        self.bankroll = []
        self.total_cash = len(self.bankroll)
        self.hand = Hand()
        # Give the player 20 chips to play with
        while self.total_cash < 20:
            self.bankroll.append(Chip(1))

    def __str__(self):
        return f'Money remaining: {self.total_cash}'

    def deal_cards(self, cards):
        if type(cards) == type([]):
            self.hand.extend(cards)
        else:
            self.hand.append(cards)

    def bet_chip(self):
        return self.bankroll.pop(0)


class Pot:

    def __init__(self):
        self.chips = []
        total = 0
        for i in chips:
            total += 1
        self.value = total

    def __str__(self):
        return f'The value of the pot is: {self.value}'

    def bet(self, number):

        for i in range(number):
            self.chips.append(player.bet_chip())


# Set up game
game_on = True
main_deck = Deck()
main_deck.shuffle()
player = Player()
dealer = Player()
pot = Pot()


def deal_cards():
    # Deal two face-up cards to player
    player.deal_cards([main_deck.remove_card(), main_deck.remove_card()])
    # Deal one face-up and one face-down card to dealer
    dealer.deal_cards([main_deck.remove_card(), main_deck.remove_card().flip])
    # Print the cards on the field for the player
    print(f'The dealer is showing {dealer.hand.cards[0]}')
    print(f'You have {player.hand.print_hand()}')


def player_turn():
    # Player decides to hit or stay
    action = input("Would you like to hit or stay? ")
    if action.lower() not in ['hit', 'stay']:
        print("Invalid input. Please type either 'hit' or 'stay'")
    else:
        return action


while game_on:

    if player.total_cash > 0:  # Make sure a player has enough money to bet
        bet = int(input("Please enter how many chips you would like to bet: "))
        if bet < player.total_cash:
            pot.bet(bet)
        else:
            print("You don't have enough chips for that bet! Please only bet money you have.")

    while player.hand.value() < 21:
        deal_cards()
        if player_turn() == 'stay':
            print(f'You stay. Hand value: {player.hand.value()}')
            break



    else:
        print('Player is out of money! Game over.')
        game_on = False

