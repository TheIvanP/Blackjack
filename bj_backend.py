import bj_components as gc

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

    def is_value_threshold(self,game_participant):
        #Defauling to player value
        value_threshold = 21
        #If we're testing for value of dealer cards, set different threshold
        if isinstance(game_participant,gc.Dealer):
            value_threshold = 16
        
        if game_participant.cards_value > value_threshold and game_participant.soft_hand == False:
            game_participant.bust = True
        elif game_participant.cards_value > value_threshold and game_participant.soft_hand == True: 
            game_participant.cards_value = self.compute_soft_hand_value(game_participant)
            if game_participant.cards_value > value_threshold:
                game_participant.bust = True
            else:
                return(False)
        else:
            return(False)

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

        #TODO:move input handling to front end
        if answer in ["Hit", "hit", "hi"]:
            self.player.hit(self.deck)
        elif answer in ["Stand", "stand", "sta"]:
            self.player.stand(True)
        
    def compute_card_value(self,game_participant):
        c_value = 0
        for card in game_participant.cards:
            if card[1] in self.deck.picture_cards.values():
                if card[1] == "ace":
                    game_participant.soft_hand = True
                    c_value += 11
                else:
                    c_value += 10
            if not isinstance(card[1], str):
                c_value += int(card[1])
        game_participant.cards_value = c_value
        return(c_value)
        
    def compute_soft_hand_value(self,game_participant):
        c_value = 0
        for card in game_participant.cards:
            if card[1] in self.deck.picture_cards.values():
                if card[1] == "ace":
                    c_value += 1
                else:
                    c_value += 10
            if not isinstance(card[1], str):
                c_value += int(card[1])
        game_participant.cards_value = c_value
        return(c_value)