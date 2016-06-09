def game_loop(game):
    game.game_start()

    done = False

    while not done:
        game.main_game()
        done = True


