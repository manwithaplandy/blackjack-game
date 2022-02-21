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

    face_up = True

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

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

    def is_face_up(self):
        if self.face_up:
            return True
        else:
            return False


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

    def __str__(self):
        return f'This chip has a value of {self.value}'


class Hand:

    total = 0

    def __init__(self):
        self.cards = []

    def __str__(self):
        return f'The current number of cards in your hand are: {len(self.cards)}'

    def print_hand(self):
        str_hand = []
        for card_obj in self.cards:
            str_hand.append(str(card_obj))
        return str_hand

    def value(self):
        # Find total points value for hand
        self.total = 0
        has_ace = False
        for card in self.cards:
            if card.rank == 'Ace':  # Determine if player has Ace in their hand
                if self.total + 11 > 21:
                    self.total += 1
                    has_ace = True
                else:
                    self.total += 11
                    has_ace = True
            else:
                self.total += card.value
        if self.total > 21 and has_ace:
            return self.total - 10
        else:
            return self.total

    def add_cards(self, cards):
        if type(cards) == type([]):
            self.cards.extend(cards)
        else:
            self.cards.append(cards)


class Player:
    # Player has bankroll and hand, and bankroll has a total value equal to adding up all chips
    def __init__(self):
        self.bankroll = []
        self.hand = Hand()
        # Give the player 20 chips to play with
        while len(self.bankroll) < 20:
            self.bankroll.append(Chip(1))
        self.total_cash = len(self.bankroll)

    def __str__(self):
        return f'Money remaining: {self.total_cash}'

    def deal_cards(self, cards):
        self.hand.add_cards(cards)

    def bet_chip(self):
        return self.bankroll.pop(0)


class Pot:

    def __init__(self):
        self.chips = []

    def __str__(self):
        return f'The value of the pot is: {self.value()}'

    def bet(self, chip):
        if type(chip) == type([]):
            self.chips.extend(chip)
        else:
            self.chips.append(chip)

    def payout(self):  # Empty the pot and pay the player
        _payout = self.chips
        self.chips = []
        return _payout

    def value(self):
        total = 0
        for chip in self.chips:
            total += 1
        return total

    def empty(self):
        self.chips = []


# Set up game
game_on = True
main_deck = Deck()
main_deck.shuffle()
player = Player()
dealer = Player()
pot = Pot()
dealer_turn = False


def deal_cards():
    # Deal two face-up cards to player
    player.deal_cards([main_deck.remove_card(), main_deck.remove_card()])
    # Deal one face-up and one face-down card to dealer
    dealer.deal_cards([main_deck.remove_card(), main_deck.remove_card().flip])
    # Print the cards on the field for the player
    print(f'The dealer is showing {str(dealer.hand.cards[0])}')
    print(f'You have {player.hand.print_hand()} worth {player.hand.value()}')


def player_turn():
    # Player decides to hit or stay
    action = input("Would you like to hit or stay? ")
    if action.lower() not in ['hit', 'stay']:
        print("Invalid input. Please type either 'hit' or 'stay'")
    else:
        return action


def play_again():
    # Player decides to play again or not
    action = ''
    while action.upper() not in ['Y', 'N']:
        action = input("Would you like to play again? Y/N ")
        if action.upper() == 'Y':
            return True
        elif action.upper() == 'N':
            print(f"Thank you for playing! You ended with {len(player.bankroll)} chips.")
            return False
        else:
            print('Invalid input. Please enter only "Y" or "N"')


while game_on:

    if not pot.value():  # Make sure not a push with a full pot
        if player.total_cash > 0:  # Make sure a player has enough money to bet
            bet = int(input("Please enter how many chips you would like to bet: "))
            if bet < player.total_cash:
                dealer_bet = 0
                for i in range(bet):  # Player bets chips from bankroll
                    pot.bet(player.bet_chip())
                    dealer_bet += 1
                for i in range(bet):
                    pot.bet(Chip(1))  # Dealer matches player bet in pot
            else:
                print("You don't have enough chips for that bet! Please only bet money you have.")
        else:
            print('Player is out of money! Game over.')
            game_on = False
            break
    else:
        print(f'Pot currently has {pot.value()}')

    # Deal initial hand
    deal_cards()

    if player.hand.value == 21 and dealer.hand.value != 21:
        print(f'Player {player.hand.value()} beats Dealer {dealer.hand.value()}. Player wins!')
        player.bankroll.extend(pot.payout())
        game_on = play_again()

    while player.hand.value() < 21:
        player_hit = player_turn()
        if player_hit == 'stay':
            print(f'You stay. Hand value: {player.hand.value()}')
            dealer_turn = True
            break
        elif player_hit == 'hit':
            hit_card = main_deck.remove_card()
            player.deal_cards(hit_card)
            print(f"You hit! It's the {hit_card} Hand value: {player.hand.value()}")
            if player.hand.value() <= 21:
                continue
            else:
                print('Bust! You lose')
                pot.empty()
                game_on = play_again()
                break

    while dealer_turn:
        while dealer.hand.value() < 17:
            dealer.deal_cards(main_deck.remove_card())
            dealer.hand.print_hand()
        if dealer.hand.value() > 21:
            print('Dealer bust! Player wins!')
            player.bankroll.extend(pot.payout())
            game_on = play_again()
            dealer_turn = False
            break
        elif dealer.hand.value() > player.hand.value():
            print(f'Dealer {dealer.hand.value()} beats Player {player.hand.value()}. Dealer wins!')
            pot.empty()
            game_on = play_again()
            dealer_turn = False
            break
        elif dealer.hand.value() < player.hand.value():
            print(f'Player {player.hand.value()} beats Dealer {dealer.hand.value()}. Player wins!')
            player.bankroll.extend(pot.payout())
            game_on = play_again()
            dealer_turn = False
            break
        elif dealer.hand.value() == player.hand.value():
            print(f'Push! Player and dealer tie')
            dealer_turn = False
            game_on = True
            break
