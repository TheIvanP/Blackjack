#%%
import bj_components as gc
import bj_frontend as fe
import bj_backend as be
    
#%%
#test game
dealer = gc.Dealer([])
player = gc.Player(50)
dek = gc.DeckOfCards()

ux = fe.GameFrontend()
back = be.GameBackend(player,dealer,dek,ux)
 
#game loop 
#back.request_bet()
back.deal_cards_start()
player.cards.append(["spades","ace"])
player.cards.append(["spades","queen"])

ux.report_cards(player,dealer)
cv = back.compute_card_value(player)
print(cv)
back.is_value_threshold(player)
print(f"is player bust? {player.bust}")
cvs = back.compute_soft_hand_value(player)
back.is_value_threshold(player)
print(f"is player bust? {player.bust}")
print(cvs)



#back.game_turn()
#back.hit_or_stand()
#back.game_turn()


        





# %%
