#%%
import random
class DeckOfCards(object):

    """Deck of cards with shuffling and ability to pull a card while managing the number of cards left in deck"""

    def __init__ (self):
        self.initialize_deck()
        self.cards = self.cards

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
            value_suite = [(suite,x) for x in range(1,num_cards_suite)]
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
        picture_cards = {11:'jack', 12:'queen', 13:'king', 14:'ace'}
        #the_cards = list()
        while len(self.cards) > 0:
            if len(self.cards) == 1:
                the_card = self.cards.pop(0)
                #the_cards.append(self.cards.pop(0))
                return(the_card)
            else:
                get_random = random.randint(0,len(self.cards))
                while get_random == True:
                    the_card = self.cards.pop(get_random)
                    #the_cards.append(self.cards.pop(get_random))
                    #print(str(the_cards) + str(i))
                    if the_card[1] in picture_cards:
                        return(the_card[0],picture_cards.get(the_card[1]))
                        
                    #the_cards.append((the_cards[i][0],picture_cards.get(the_cards[i][1])))
                    return(the_card)

#%%
class GameParticipant(object):

    def __init__(self, chips, cards):
        self.chips = chips
        self.cards = cards
        
    def get_cards(self):
        return(self.cards)
    
    def pickup_card(self,card_from_deck):
        self.cards.append(card_from_deck)
    
    def clear_hand(self):
        self.cards.clear()

    #Place bet
    def place_bet(self,bet_amount):
        if bet_amount <= self.chips:
            return (bet_amount)
        else:
            return ("Not enough chips")

class Dealer(GameParticipant):  

    def __init__(self, cards):
        self.cards = cards
        self.hidden_card = []
        super(Dealer, self).__init__ (0, self.cards)

    def card_hidden(self):
        self.hidden_card = self.cards[-1]
        self.cards[-1] = "Hidden"
    
    def card_reveal(self):
        self.cards[-1] = self.hidden_card 

class GameBackend(object):

    def __init__(self, player, dealer, deck):
        self.chips_on_table = 0
        self.player = player
        self.dealer = dealer
        self.deck = deck

    def request_bet(self,amount):
        amount = self.chips_on_table
    
    def deal_cards_start(self):
        for i in range(2):
            self.player.pickup_card(self.deck.get_card())
            self.dealer.pickup_card(self.deck.get_card())

class GameFrontend(object):

    def __init__(self, backend):
        self.backend = backend

    def cards_in_game(self, player_stand):
        player_cards = f"Player cards: {self.backend.player.cards} "
       
        print (player_cards)

        dealer_cards = f"Dealer cards: "

        if not player_stand:
            self.backend.dealer.card_hidden() 
            print(f"{dealer_cards} {self.backend.dealer.cards}")
        else:
            self.backend.dealer.card_reveal()
            print(self.backend.dealer.cards)


#%%
dealer = Dealer([])
player = GameParticipant(50,[])
dek = DeckOfCards()

back = GameBackend(player,dealer,dek)
ux = GameFrontend(back)

back.deal_cards_start()
ux.cards_in_game(False)




        





# %%
