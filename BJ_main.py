import bj_components as gc
import bj_frontend as fe
import bj_backend as be
import time
#main game 
#Setup game

#Dealer and player classes 
dealer = gc.Dealer()
player = gc.Player(50,"Player 1")

#Deck of cards, front end for communicating with player, back end for functionality
dek = gc.DeckOfCards()
ux = fe.GameFrontend()
back = be.GameBackend(player,dealer,dek,ux)

#Enter player name 
back.enter_name(player)

#Game loop for player's turn 
def players_turn(): 
    dealer.initialize()
    player.initialize()

    ux.report_chips(player)

    player.cards = [['ace', 'spades'],['hearts', 'queen']]
    while player.bet_too_high:
        back.request_bet(player)

    back.deal_cards_start(player,dealer)
    player.cards = [['spades','ace'],['hearts', 'queen']]

    ux.report_cards(player,dealer)

    if back.blackjack(player):
        player_win()


    #while the player still has chips and wants another hit
    while not player.standing and not player.bust:
        back.hit_or_stand(player)
        back.is_value_threshold(player)
        back.frontend.cards_value(player, player.cards_value)
        time.sleep(1)

        back.test_bust(player)
        if player.bust:
            back.try_again(player)
            main_game_loop()
        
        elif player.standing == True:
            player_standing()

#If the player chooses to stand, reveal dealer's hidden card, test 
def player_standing():
    if player.standing == True:
            ux.card_reveal(dealer)
            dealer.card_reveal()
            dealers_turn()

#Player win sequence 
def player_win():
    back.player_wins(player)
    ux.report_chips(player)
    back.try_again(player)
    main_game_loop()

def main_game_loop():
    while player.try_again and player.chips > 0:
        players_turn()
    else:
        print("Game Over")
        quit()

#Dealer game loop
def dealers_turn():
    #If dealer hasn't gone bust or standing on/after 17
    while not dealer.standing or not dealer.bust:
        ux.report_cards(player,dealer)
        back.should_dealer_stand()
        back.pick_a_card(dealer, True)
        back.is_value_threshold(dealer)
        back.test_bust(dealer)
        time.sleep(1)
        ux.cards_value(dealer,dealer.cards_value)
        ux.cards_value(player,player.cards_value)
        if dealer.bust:
            player_win()
            break

        elif back.has_dealer_won(player,dealer):
            ux.report_chips(player)
            print("house wins")
            back.try_again(player)
            main_game_loop()    
        else:
            dealers_turn()

#Run the game loop
main_game_loop()