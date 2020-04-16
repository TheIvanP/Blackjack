#%%
import bj_components as gc
import bj_frontend as fe
import bj_backend as be
import time
    
#%%
#test game
dealer = gc.Dealer([])
player = gc.Player(50,"Player 1")
dek = gc.DeckOfCards()

ux = fe.GameFrontend()
back = be.GameBackend(player,dealer,dek,ux)

back.enter_name(player)
while not back.request_bet(player):
    back.request_bet(player)
back.deal_cards_start()
#player.cards = [['diamonds', 6], ['diamonds', 7], ['spades', 8]]
is_first_hand = True

def main_game_loop():
    while not player.standing and not player.bust:
        back.game_turn(player)
        back.test_bust(player)
    if player.standing == True:
            ux.card_reveal(dealer)
            dealer.card_reveal()
            while not dealer.standing:
                ux.report_cards(player,dealer)
                back.is_value_threshold(player)
                back.should_dealer_stand()
                back.pick_a_card(dealer)
                back.compute_card_value(dealer)
                back.is_value_threshold(dealer)
                back.test_bust(dealer)
                if back.has_dealer_won(player,dealer):
                    break
                else:
                    ux.player_win(player.name)
                    break
                time.sleep(1)

#TODO: make game loop repeat if we want to try again.
if not is_first_hand:
    had_enough = False
    while not had_enough:
        main_game_loop()
        had_enough = back.dont_try_again(player)

if is_first_hand:
    main_game_loop()
    is_first_hand = False
