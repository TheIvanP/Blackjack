class GameFrontend(object):

    """Game frontend class for basic terminal based UX with minimal functionality to improve modularity 
    text content is stored in class variable dict -  could in future be parsed in from a json stored seperately to allow for localislation"""

    #TODO: parse this from json stored on dist instead to enable localislation. Investigate if it's possible to 'translate on the fly' from requested language
    comms_strings = {
        "s_report_cards":["'s cards are: ", "'s cards are: "],
        "s_hit_stand": "Do you hit or do you stand?",
        "s_bet_amount": ", how much do you want to bet?",
        "s_card_reveal": "Dealer's hidden card is: ",
        "bust": ["Ooops, ", " your cards' value are: ", "which is more than 21 - you've gone bust and lost "],
        "soft hand": "we have an ace on the hand which can be worth either 11 or 1",
        "cards_value": "the value of the cards are: ",
        "card_pulled":  [" pulls ","from the deck. "],
        "player_wins": ["Contratulations ", "you won the game"],
        "name": ["Please enter your name"],
        "bet_high": "Sorry, you can't afford that bet, you have: ",
        "retry": "Do you want to bet again?"
        }

    def __init__(self):
        pass

    def p_name(self):
        print(self.comms_strings.get("name"))
    
    def bet_high(self, chips):
        bh_string = self.comms_strings.get("bet_high")
        print(f"{bh_string}{chips}")

    def report_cards(self, player, dealer):
        pstring = self.comms_strings.get("s_report_cards")[0]
        p_cards = f"{player.name}{pstring}{player.cards}"
        dstring = self.comms_strings.get("s_report_cards")[1]
        d_cards = f"{dealer.name}{dstring}{dealer.cards}"
        print(f"{p_cards} and {d_cards}")
    
    def player_win(self,name):
        w_str = self.comms_strings.get("player_wins")
        print(f"{w_str[0]} {name} {w_str[1]}")

    def player_bust(self, player, value, chips):
        b_str = self.comms_strings.get("bust")
        print(f"{b_str[0]}{player.name}{b_str[1]} {value} {b_str[2]}{chips}")

    def card_pulled(self,card,name):
        cp_str = self.comms_strings.get("card_pulled")
        print(f"{name} {cp_str[0]} {card} {cp_str[1]}")
    
    def cards_value(self, player, value):
        v_str = self.comms_strings.get("cards_value")
        print(f"{v_str} {value}")

    def bet_amount(self, name):
        be_str = self.comms_strings.get("s_bet_amount")
        print(f"{name}{be_str}")
    
    def player_input(self):
        return(str(input())[0:10])
    
    def hit_stand(self):
        print(self.comms_strings.get("s_hit_stand"))
    
    def card_reveal(self, dealer):
        hcard = self.comms_strings.get("s_card_reveal")
        print(f"{hcard} {dealer.hidden_card}")
    
    def retry(self):
        print(self.comms_strings.get("retry"))