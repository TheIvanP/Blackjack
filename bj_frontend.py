class GameFrontend(object):

    """Game frontend class for basic terminal based UX with minimal functionality to improve modularity 
    text content is stored in class variable dict -  could in future be parsed in from a json stored seperately to allow for localislation"""

    #TODO: parse this from json stored on dist instead to enable localislation. Investigate if it's possible to 'translate on the fly' from requested language
    #TODO: fuzzy strings to handle input 
    comms_strings = {
        "report_cards": "'s cards are: ",
        "s_hit_stand": "Do you hit or do you stand?",
        "s_bet_amount": ", how much do you want to bet?",
        "s_card_reveal": "Dealer's hidden card is: ",
        "bust": ["Ooops, ", " your cards' value is: ", "which is more than 21 - you've gone bust and lost "],
        "soft hand": "we have an ace on the hand which can be worth either 11 or 1",
        "cards_value": ["the value of", "'s cards are: "],
        "card_pulled":  [" pulls ","from the deck. "],
        "player_wins": ["Contratulations ", "you won the game"],
        "name": ["Please enter your name"],
        "bet_high": "Sorry, you can't afford that bet, you have: ",
        "retry": "Do you want to bet again?",
        "report_chips": ["Player has"," chips"]
        }

    def __init__(self):
        pass

    def p_name(self):
        print(self.comms_strings.get("name"))
    
    def bet_high(self, chips):
        bh_string = self.comms_strings.get("bet_high")
        print(f"{bh_string}{chips}")
    
    def clean_strings(self,text):
        t = text.translate(str.maketrans('', '', "[],'"))
        return t

    def report_cards(self, player, dealer):
        pstring = self.comms_strings.get("report_cards")
        p_cards = f"{player.name}{pstring}{player.cards[0]} and {player.cards[1]}"
        d_cards = f"{dealer.name}{pstring}{dealer.cards[0]} and {dealer.cards[1]}"
        print("")
        print(self.clean_strings(f"{p_cards}"))
        print(self.clean_strings(f"{d_cards}"))
        print("")

    def report_chips(self, player):
        s_chips = self.comms_strings.get("report_chips")
        print(s_chips[0],player.chips,s_chips[1])
    
    def player_win(self,player):
        w_str = self.comms_strings.get("player_wins")
        print(f"{w_str[0]} {player.name} {w_str[1]}")

    def player_bust(self, player, value, chips):
        b_str = self.comms_strings.get("bust")
        print(f"{b_str[0]}{player.name}{b_str[1]} {value} {b_str[2]}{chips}")

    def card_pulled(self,card,name):
        cp_str = self.comms_strings.get("card_pulled")
        print(self.clean_strings(f"{name} {cp_str[0]} {card} {cp_str[1]}"))
    
    def cards_value(self, player, value):
        v_str = self.comms_strings.get("cards_value")
        print(f"{v_str[0]} {player.name} {v_str[1]} {value}")

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