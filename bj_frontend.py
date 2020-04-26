from translate import Translator
from fuzzywuzzy import fuzz
import json

class GameFrontend(object):

    """Game frontend class for basic terminal based UX with minimal functionality to improve modularity 
    ability change game 'personality' via setting personality attribute on class creation 
    tanslation using Translator / google translate api
    """    
    language = 'en'

    def __init__(self, personality = "neutral"):
        self.personality = personality
        self.comms_strings = dict()
        self.personalities = {"neutral":"dialogue_neutral.json", "dirty harry":"dialogue_dharry.json"}
        self.retrive_personality()
    
    def retrive_personality(self):
        with open(self.personalities.get(self.personality)) as f:
            self.comms_strings = json.load(f)

    def translate_p_output(self, response):
        # https://en.wikipedia.org/wiki/ISO_639-1 for languages
        translator = Translator(to_lang=self.language)
        output = ""
        if self.language == 'en':
            output = response
        else:
            output = translator.translate(str(response))
        return print(output)

    #what language to tranlate into
    def what_lang(self):
        print(self.comms_strings.get(f"ask_language")[0])
        lang = str(input())[:2]
        self.language = lang
        l_response = self.comms_strings.get(f"ask_language")[1] 
        self.translate_p_output(f"{l_response}{lang}")
        return lang

    #Player name
    def p_name(self):
        ask = self.comms_strings.get("name")
        return self.translate_p_output(ask)
    
    def bet_high(self, chips):
        bh_string = self.comms_strings.get("bet_high")
        self.translate_p_output(f"{bh_string}{chips}")
    
    def clean_strings(self,text):
        t = text.translate(str.maketrans('', '', "[],'"))
        return t

    def report_cards(self, player, dealer):
        pstring = self.comms_strings.get("report_cards")
        p_cards = f"{player.name}{pstring[0]}{player.cards[0]}{pstring[1]}{player.cards[1]}"
        d_cards = f"{dealer.name}{pstring[0]}{dealer.cards[0]}{pstring[1]}{dealer.cards[1]}"
        self.translate_p_output("")
        self.translate_p_output((self.clean_strings(f"{p_cards}")))
        self.translate_p_output((self.clean_strings(f"{d_cards}")))
        self.translate_p_output("")

    def report_chips(self, player):
        s_chips = self.comms_strings.get("report_chips")
        self.translate_p_output(f"{s_chips[0]}{player.chips}{s_chips[1]}")
    
    def player_win(self,player):
        w_str = self.comms_strings.get("player_wins")
        if player.blackjack:
            self.translate_p_output(f"{w_str[2]}{w_str[0]}{player.name}{w_str[1]}")        
        else:
            self.translate_p_output(f"{w_str[0]} {player.name} {w_str[1]}")

    #takes a zipped list indexing the dict containing personalities to communicate number choices back to player
    def what_personalities(self,num_pers):
        #[x for x in self.personalities.keys()]
        tp = f"What personality? {num_pers}"
        tp = self.clean_strings(tp)
        print(tp)

    def player_bust(self, player, value, chips):
        b_str = self.comms_strings.get("bust")
        self.translate_p_output(f"{b_str[0]}{player.name}{b_str[1]} {value} {b_str[2]}{chips}")

    def card_pulled(self,card,name):
        cp_str = self.comms_strings.get("card_pulled")
        self.translate_p_output(self.clean_strings(f"{name} {cp_str[0]} {card} {cp_str[1]}"))
    
    def cards_value(self, player, value):
        v_str = self.comms_strings.get("cards_value")
        self.translate_p_output(f"{v_str[0]} {player.name} {v_str[1]} {value}")

    def bet_amount(self, name):
        be_str = self.comms_strings.get("s_bet_amount")
        self.translate_p_output(f"{name}{be_str}")
    
    def player_input_text(self, cap, match, shouldmatch=True):
        done = False
        response = ""
        if shouldmatch == True:
            while not done:
                response = input()
                #if match is a list object:     
                if isinstance(match,list):
                    for m in match:
                        di = fuzz.ratio(m, response)
                        if di > 80:
                            done=True
                            return m
                            
                else:
                    r = fuzz.ratio(response,match)
                    if r > 80:
                        done = True
                        return match
                        
            else:
                try:
                    response = str(input())
                except ValueError:
                    self.translate_p_output("Please enter some text")            
        else:
            try:
                response = str(input())
            except ValueError:
                self.translate_p_output("Please enter some text")
            else:
                return(response)
        
    def player_input_number(self):
        while True:
            try:
                number = int(input())            
            except ValueError:
                print(self.translate_p_output("Please enter a value")) 
            else:
                return number

    def hit_stand(self):
        self.translate_p_output(self.comms_strings.get("s_hit_stand"))
    
    def card_reveal(self, dealer):
        hcard = self.comms_strings.get("s_card_reveal")
        self.translate_p_output(f"{hcard} {dealer.hidden_card}")
    
    def retry(self):
        self.translate_p_output(self.comms_strings.get("retry"))