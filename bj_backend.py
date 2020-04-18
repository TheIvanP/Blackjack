import bj_components as gc

class GameBackend(object):

    """ Backend class for managing game functionality, participants and state. Communicates with frontend for i/o""" 
    def __init__(self, player, dealer, deck, frontend):
        self.chips_on_table = 0
        self.player = player
        self.dealer = dealer
        self.deck = deck
        self.frontend = frontend

    def try_again(self, player):
        self.frontend.retry()
        answer = self.frontend.player_input()
        if answer in ["Yes", "y", "yes"]:
            player.try_again = True
            return(True)
        else:
            player.try_again = False
            return(False)

    def enter_name(self,player):
        self.frontend.p_name()
        player.name = self.frontend.player_input()
    
    def blackjack(self, participant):
        if self.compute_card_value(participant) == 21:
            participant.blackjack = True
            return True
        else:
            return False

    def request_bet(self, player):
        self.frontend.bet_amount(player.name)
        amount = player.place_bet(int(self.frontend.player_input()))
        if isinstance(amount,int):
            self.chips_on_table = amount
            player.bet_too_high = False
        else:
            self.frontend.bet_high(player.chips)
    
    def deal_cards_start(self, player, dealer):
        for i in range(2):
            self.pick_a_card(player, False)
            self.pick_a_card(dealer, False)
        self.dealer.card_hidden()

    #duplicates other functions to get card hit, pickup_card
    def pick_a_card(self,participant,report):
        card = self.deck.get_card()
        participant.pickup_card(card)
        if report:
            self.frontend.card_pulled(card,participant.name)
                
    def is_value_threshold(self,game_participant):
        #Defauling to player value
        value_threshold = 21
        
        self.compute_card_value(game_participant)

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

    def test_bust(self,participant):
        if participant.bust == True:
            self.frontend.player_bust(participant,participant.cards_value,participant.bet)
    
    def has_dealer_won(self,player,dealer):
        if dealer.cards_value > player.cards_value & dealer.bust == False:
            return(True)
    
    def player_wins(self,player):
        self.player.has_won = True
        payout_multiplier = 2
        if player.blackjack:
            self.frontend.player_win(player)
            payout_multiplier = 3
        else:
            self.frontend.player_win(player)  
        player.chips += payout_multiplier * self.chips_on_table

    def should_dealer_stand(self):
        if self.dealer.cards_value >= 17:
            self.dealer.standing = True

    def hit_or_stand(self, player):
        self.frontend.hit_stand()
        answer = self.frontend.player_input()

        #TODO:move input handling to front end, fuzzy strings 
        if answer in ["Hit", "hit", "hi"]:
            self.pick_a_card(player, True)
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