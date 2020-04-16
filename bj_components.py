import random
class DeckOfCards(object):

    """Deck of cards with shuffling and ability to pull a card while managing the number of cards left in deck"""

    def __init__ (self):
        self.initialize_deck()
        self.cards = self.cards
        self.picture_cards = {11:'jack', 12:'queen', 13:'king', 14:'ace'}

    #Get a full set of cards and shuffle them. 
    #TODO: Consider if shuffle should be separate
    def initialize_deck(self):
        self.cards = self.create_deck()
        self.shuffle_deck()

    #create the deck of cards
    #TODO: move functionality for picture cards from get_card into this function
    #TODO: optimize multiple loops 
    def create_deck(self):
        num_cards_suite = 14
        cards = []
        for suite in ["spades", "clubs", "hearts", "diamonds"]:
            value_suite = [[suite,x] for x in range(2,num_cards_suite)]
            cards.append(value_suite)
        #flatten nested array
        cards = [item for sublist in cards for item in sublist]
        return(cards)

    #shuffle deck of cards
    def shuffle_deck(self):
        return(random.shuffle(self.cards))

    #get a card from the deck
    #TODO: handle empty deck better. currently will return None
    #TODO: clean up logic 
    #TODO: figure out why append the cards doesnt get the elements from self.cards 
    def get_card(self):

        while len(self.cards) > 0:
            if len(self.cards) == 1:
                the_card = self.cards.pop(0)
                return(the_card)
            else:
                get_random = random.randint(0,len(self.cards))
                while get_random == True:
                    the_card = self.cards.pop(get_random)
                    if the_card[1] in self.picture_cards:
                        return([the_card[0],self.picture_cards.get(the_card[1])])
                    return(the_card)

#%%
class GameParticipant(object):

    """Base game participant class for holding data and shared functionality"""

    def __init__(self, chips, cards, name):
        self.chips = chips
        self.cards = cards
        self.cards_value = 0
        self.soft_hand = False
        self.blackjack = False
        self.bust = False
        self.standing = False
        self.name = name
        
    def get_cards(self):
        return(self.cards)
    
    def pickup_card(self,card_from_deck):
        self.cards.append(card_from_deck)
        
    def clear_hand(self):
        self.cards.clear()
            
    def hit(self,deck):
        self.pickup_card(deck.get_card())

class Dealer(GameParticipant):  

    """Dealer class - inherits from GameParticipant""" 

    def __init__(self, cards):
        self.cards = cards
        self.hidden_card = []
        self.bet = 0
        super(Dealer, self).__init__ (0, self.cards, "Dealer")

    def card_hidden(self):
        self.hidden_card = self.cards[-1]
        self.cards[-1] = "Hidden"
    
    def card_reveal(self):
        self.cards[-1] = self.hidden_card 

class Player(GameParticipant):

    """Player specific functionality - place a bet, stand""" 

    def __init__(self, chips, name):
        self.cards = []
        self.chips = chips
        self.bet = 0
        super(Player, self).__init__(self.chips, self.cards, name)

    #Place bet 
    def place_bet(self,bet_amount):
        if bet_amount <= self.chips:
            self.bet = bet_amount
            return(bet_amount)
        else:
            return ("Not enough chips")
    
    def stand(self,is_standing):
        self.standing = is_standing