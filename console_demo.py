from blackjack import Blackjack
game = Blackjack()

while not game.is_over():

    print("Dealer cards:", game.dealer.hand.cards[0], "???")
    print("Player cards:", *game.player.hand.cards, "| Value:", game.player.hand.get_optimal_value())
    
    prompt = "[H]it or [S]tand? "
    selection = input(prompt).lower()
    while True:
        if selection == "h": 
            game.hit()
            break
        elif selection == "s":
            game.stand()
            break
        else: 
            print("Invalid input. Try again!")
            selection = input(prompt).lower()

game.play_dealer()
result = game.get_outcome()
print(f"== RESULT : {result.name} ==")
print("Dealer cards:", *game.dealer.hand.cards, "| Value:", game.dealer.hand.get_optimal_value())
print("Player cards:", *game.player.hand.cards, "| Value:", game.player.hand.get_optimal_value())