from Game import Game


game = Game()
game.startScreen()
state = game.getState()
while True:
    if state == 'game':
        game.run()
    if state == 'score':
        game.scoreScreen()
    if state == 'menu':
        game.drawMenuWindow()
    state = game.getState()
