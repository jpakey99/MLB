import mlbSingleSimulationEO as mlbSSEO

game = mlbSSEO.SingleGameSimulationEO("Pirates", "Reds")
game.runSimulation()
print(game.winningTeam)
