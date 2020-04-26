import bj_components as gc

class GameBackend(object):

    """ Backend class for managing game functionality, participants and state. Communicates with frontend for i/o""" 
    def __init__(self, player, dealer, deck, frontend):
        self.chips_on_table = 0
        self.player = player
        self.dealer = dealer
        self.deck = deck
        self.frontend = frontend

    #Set the output language
    #TODO: enable input to be translated / redo as multiple choice 
    def set_language(self):
       self.frontend.what_lang()

    #Set player state try again if input is yes. 
    #TODO: Improve input handling 
    def try_again(self, player):
        self.frontend.retry()
        answer = self.frontend.player_input_text(10,["no","yes"],True)
        if answer == "no":
            player.try_again = False
            return(False)
        elif answer == "yes":
            player.try_again = True
            return(True)
 
    #Enter name of player 
    def enter_name(self,player):
        self.frontend.p_name()
        response = input()
        player.name = str(response)

    #Test card value for blackjack     
    def blackjack(self, participant):
        if self.compute_card_value(participant) == 21:
            participant.blackjack = True
            return True
        else:
            return False

    #Request bet from player, basic input handling to test if it's int. Set chips on table instance var to bet amount 
    def request_bet(self, player):
        self.frontend.bet_amount(player.name)
        amount = player.place_bet(int(self.frontend.player_input_number()))
        if isinstance(amount,int):
            self.chips_on_table = amount
            player.bet_too_high = False
        else:
            self.frontend.bet_high(player.chips)

    #Starting hand, hide dealers second card 
    def deal_cards_start(self, player, dealer):
        for i in range(2):
            self.pick_a_card(player, False)
            self.pick_a_card(dealer, False)
        self.dealer.card_hidden()

    def pick_a_card(self,participant,report=False):
        card = self.deck.get_card()
        participant.pickup_card(card)
        if report:
            self.frontend.card_pulled(card,participant.name)
                
    #Test if we've hit 21, handle soft hand edge case (ace on hand)
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

    #communicate if player is bust
    def test_bust(self,participant):
        if participant.bust == True:
            self.frontend.player_bust(participant,participant.cards_value,participant.bet)

    #Test if the dealers cards' value is above players    
    def has_dealer_won(self,player,dealer):
        if dealer.cards_value > player.cards_value:
            return(True)
    
    def request_personality(self):
        pmax = len(self.frontend.personalities)
        l = range(0,pmax)
        num_pers = list(zip(l,self.frontend.personalities.keys()))
        self.frontend.what_personalities(num_pers)
   
        response = self.frontend.player_input_number()
        if response < pmax:
            getres = num_pers[response][1]
            pkeys = list(self.frontend.personalities.keys())
            self.frontend.personality = pkeys[response]
            self.frontend.retrive_personality()
            print(getres)
    
    #player has won - if player has blackjack pay out 2:3 
    def player_wins(self,player):
        self.player.has_won = True
        payout_multiplier = 2
        if player.blackjack:
            self.frontend.player_win(player)
            payout_multiplier = 3
        else:
            self.frontend.player_win(player)  
        player.chips += payout_multiplier * self.chips_on_table

    #Dealer always stands on 17
    def should_dealer_stand(self):
        if self.dealer.cards_value >= 17:
            self.dealer.standing = True

    #Ask the player if she wants to hit or stand
    def hit_or_stand(self, player):
        self.frontend.hit_stand()
        while True:
            response = self.frontend.player_input_text(10,["hit", "stand"],True)
            if response == "hit":
                self.pick_a_card(player, True)
                break
            elif response == "stand":
                self.player.stand(True)
                break
        
    #value of the player or dealers cards - handle soft hand case        
    def compute_card_value(self,game_participant):
        c_value = 0
        for card in game_participant.cards:
            #look up picture card value in dict
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
    
    #compute the soft hand value. TODO: implement in main compute value method
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