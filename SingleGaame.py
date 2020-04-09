from random import random

def sim_at_bat():
    """Simulates 1 at bat.
    Return: -1: out, 1: single, 2:double, 3:triple, 4:HR"""
    strike = 0
    ball = 0
    while strike < 3 and ball < 4:
        rand = random()
        if rand >= .2574:
            return -1
        elif rand < .0513:
            return 2
        elif .0513 <= rand < .0565:
            return 3
        elif .0565 <= rand < .0844:
            return 4
        else:
            return 1


def move_runners(basepaths):
    return basepaths

def sim_inning():
    runs_scored = 0
    outs = 0
    base_paths = [0,0,0]
    while outs < 3:
        batter = sim_at_bat()
        if batter == 4:
            runs_scored += 1
        elif batter == 3:
            base_paths[2] = 1
        elif batter == 2:
            base_paths[1] = 1
        elif batter == 1:
            base_paths[0] = 1
        else:
            outs += 1
    return runs_scored


def main():
    results = [0,0,0,0,0,0]
    for i in range(0, 1000000):
        result = sim_at_bat()
        results[result] += 1
    print(results)

main()