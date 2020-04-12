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

    """Base game participant class for holding data and shared functionality"""

    def __init__(self, chips, cards):
        self.chips = chips
        self.cards = cards
        
    def get_cards(self):
        return(self.cards)
    
    def pickup_card(self,card_from_deck):
        self.cards.append(card_from_deck)
    
    def clear_hand(self):
        self.cards.clear()
            
    def hit(self,deck):
        player.pickup_card(deck.get_card())

class Dealer(GameParticipant):  

    """Dealer class - can hide a card""" 

    def __init__(self, cards):
        self.cards = cards
        self.hidden_card = []
        super(Dealer, self).__init__ (0, self.cards)

    def card_hidden(self):
        self.hidden_card = self.cards[-1]
        self.cards[-1] = "Hidden"
    
    def card_reveal(self):
        self.cards[-1] = self.hidden_card 

class Player(GameParticipant):

    """Player specific functionality - place a bet, stand""" 

    def __init__(self, chips):
        self.cards = []
        self.chips = chips
        super(Player, self).__init__(self.chips, self.cards)
        self.standing = False

    #Place bet
    def place_bet(self,bet_amount):
        if bet_amount <= self.chips:
            return (bet_amount)
        else:
            return ("Not enough chips")
    
    def stand(self,is_standing):
        self.standing = is_standing

class GameBackend(object):

    """ Backend class for managing game functionality, participants and state. Communicates with frontend for i/o""" 
    def __init__(self, player, dealer, deck, frontend):
        self.chips_on_table = 0
        self.player = player
        self.dealer = dealer
        self.deck = deck
        self.frontend = frontend
        self.bet = 0

    def request_bet(self):
        self.frontend.bet_amount()
        amount = self.player.place_bet(int(self.frontend.player_input()))
        if isinstance(amount,int):
            self.bet = amount 
    
    def deal_cards_start(self):
        for i in range(2):
            self.player.pickup_card(self.deck.get_card())
            self.dealer.pickup_card(self.deck.get_card())
        self.dealer.card_hidden()

    def game_turn(self):        
        if not self.player.standing: 
            self.frontend.report_cards(self.player,self.dealer)
        else:
            self.frontend.report_cards(self.player,self.dealer)
            self.frontend.card_reveal(self.dealer)
            self.dealer.card_reveal()
            self.frontend.report_cards(self.player,self.dealer)

    def hit_or_stand(self):

        self.frontend.hit_stand()
        answer = self.frontend.player_input()

        if answer in ["Hit", "hit", "hi"]:
            self.player.hit(self.deck)
        elif answer in ["Stand", "stand", "sta"]:
            self.player.stand(True)
    
    #TODO: implement this
    def compute_card_value(self,game_participant):
        pass

class GameFrontend(object):

    """Game frontend class for basic terminal based UX with minimal functionality to improve modularity 
    text content is stored in class variable dict - but should be parsed in from a json stored seperately to allow for localislation"""

    #TODO: parse this from json stored on dist instead to enable localislation. Investigate if it's possible to 'translate on the fly' from requested language
    comms_strings = {
        "s_report_cards":["Player's cards are: ", "Dealer's cards are: "],
        "s_hit_stand": "Do you hit or do you stand?",
        "s_bet_amount": "How much do you want to bet?",
        "s_card_reveal": "Dealer's hidden card is: "
        }

    def __init__(self):
        pass
    
    def report_cards(self,player,dealer):
        pstring = self.comms_strings.get("s_report_cards")[0]
        p_cards = f"{pstring}{player.cards}"
        dstring = self.comms_strings.get("s_report_cards")[1]
        d_cards = f"{dstring}{dealer.cards}"
        print(f"{p_cards} and {d_cards}")
    
    def bet_amount(self):
        print(self.comms_strings.get("s_bet_amount"))
    
    def player_input(self):
        return(str(input())[0:10])
    
    def hit_stand(self):
        print(self.comms_strings.get("s_hit_stand"))
    
    def card_reveal(self, dealer):
        hcard = self.comms_strings.get("s_card_reveal")
        print(f"{hcard} {dealer.hidden_card}")
    
#%%
#test game
dealer = Dealer([])
player = Player(50)
dek = DeckOfCards()

ux = GameFrontend()
back = GameBackend(player,dealer,dek,ux)

#game loop 
back.request_bet()
back.deal_cards_start()
back.game_turn()
back.hit_or_stand()
back.game_turn()


        





# %%
