import random

random.seed(1) # for testing


class HanabiDeck:
    NUMBERS = [1,2,3,4,5]
    COLORS = ['R','Y','G','B','W']
    def __init__(self):
        deck = list()
        for n in HanabiDeck.NUMBERS:
            for c in HanabiDeck.COLORS:
                card = (c,n)
                deck.append(card)
                if n < 5:
                    deck.append(card)
                if n == 1:
                    deck.append(card)
        self.cards = deck
    
    def draw(self):
        return self.cards.pop()

    def deal(self, num_cards):
        top_cards = list()
        for i in range(num_cards):
            if len(self.cards) == 0:
                break
            top_cards.append(self.draw()) # last item = top of deck
        return top_cards

    def shuffle(self):
        random.shuffle(self.cards)
        return self.cards
    
    def __str__(self):
        return str(sorted(self.cards))


class HanabiBoard:
    color_map = dict((c,n) for n,c in enumerate(HanabiDeck.COLORS))
    def __init__(self):
        self.state = [0, 0, 0, 0, 0]

    def get_current(self, color):
        return self.state[self.color_map[color]]

    def play(self, color):
        self.state[self.color_map[color]] += 1
        return self.state

    def __str__(self):
        return " ".join(HanabiDeck.COLORS) + "\n" + " ".join(map(str,self.state))
    

class HanabiGame:
    def __init__(self):
        self.deck = HanabiDeck()
        self.deck.shuffle()
        self.clue_tokens = 8
        self.strikes = 0
        self.player1_hand = self.deck.deal(5)
        self.player2_hand = self.deck.deal(5)
        self.discard = []
        self.board = HanabiBoard()
    
    def print_state(self):
        print(self.deck)
        print("clues:", self.clue_tokens)
        print("strikes:", self.strikes)
        print("player1:", self.player1_hand)
        print("player2:", self.player2_hand)
        print("discard pile:", self.discard)
        print("board:\n", self.board, sep='')

    def action_play(self, player, card_index):
        print(f"attempting to play player {player}'s card {card_index + 1}:")
        player_hand = self.player1_hand if player == 1 else self.player2_hand
        card = player_hand.pop(card_index) # remove card from hand
        color, number = card
        print(f"{color} {number}")

        #successful play
        if self.board.get_current(color) + 1 == number:   
            print("Play successful")    
            self.board.play(color) # add card to board    
            if number == 5:
                self.clue_tokens = min(self.clue_tokens + 1, 8) # no bonus if already at max
        # misplay
        else: 
            print("Play unsuccessful")
            self.strikes += 1
            self.discard.append(card)
            if self.strikes == 3:
                print("BOOM! You accidentally triggered the show.")
                print(f"You got {sum(self.board.state)} points.")
        
        # draw new card (refactor to method)
        if (len(self.deck.cards) > 0):
            player_hand.append(self.deck.draw()) # draw replacement card
            # potentially check if deck empty now
        
        self.print_state()

    def action_clue(self):
        print("Clue given")
        if self.clue_tokens == 0:
            print("You don't have any clue tokens")
            return
        self.clue_tokens -= 1

        self.print_state()

    def action_discard(self, player, card_index):
        if self.clue_tokens == 8:
            print("You cannot discard when you have all your clue tokens")
            return

        print(f"discarding {player}'s card {card_index + 1}:")

        player_hand = self.player1_hand if player == 0 else self.player2_hand
        card = player_hand.pop(card_index) # TODO: select card helper? select(player, index) -> pop card from hand
        color, number = card
        print(f"{color} {number}")
        self.discard.append(card)
        self.clue_tokens += 1

        # draw new card (refactor to method)
        if (len(self.deck.cards) > 0):
            player_hand.append(self.deck.draw()) # draw replacement card
            # potentially check if deck empty now

        self.print_state()

game = HanabiGame()
game.print_state()

game.action_play(1, 0)
game.action_play(1, 0)
game.action_play(1, 0)
game.action_play(1, 0)
game.action_play(1, 0)
game.action_clue()
game.action_discard(1,0)