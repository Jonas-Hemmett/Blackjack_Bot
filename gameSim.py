import openAIFunctions as f1
import bots as b
import blackjackGameSim as game
import playerBase as pl

players = [b.Bot2(), pl.BotDealer()]

printOutput = True
g = game.GameBotSim(players, 1, True)

 
while True:
    try:
        trackIndex = int(input("Player index to track: ")) 
        assert trackIndex < len(players), "Player index out of range!"
        assert trackIndex >= 0, "Player index out of range!"
        break
  
    except AssertionError:
        print("Invalid Player!")

while True:
    try:
        numGames = int(input("Number of games to simulate or 0 to exit: "))
        if not numGames:
            break

        players = g.newGame(numGames)
        
        # for p in players[0]:
        #     if isinstance(p, pl.Player):
        #         print(p.bankroll)
    except Exception as e:
        print(e)

# print(f"{str(type(players[trackIndex]))[8:-2]} had a win rate of {(game1[trackIndex]['wins'] / sum(game1[trackIndex].values())):.2%}, tie rate of {(game1[trackIndex]['ties'] / sum(game1[trackIndex].values())):.2%}, and loss rate of {(game1[trackIndex]['losses'] / sum(game1[trackIndex].values())):.2%} ")
# over {numGames:,} game{'' if numGames == 1 else 's'} 