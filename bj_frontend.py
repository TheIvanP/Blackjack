class GameFrontend(object):

    """Game frontend class for basic terminal based UX with minimal functionality to improve modularity 
    text content is stored in class variable dict -  could in future be parsed in from a json stored seperately to allow for localislation"""

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