from random import random
from dataclasses import dataclass
from typing import Union

@dataclass
class BasePaths:
    first_base: bool
    second_base: bool
    third_base: bool

@dataclass
class Player:
    name: str
    next_batter: Union[None, 'Player']

@dataclass
class BattingOrder:
    current_batter: Player

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


def move_runners(basepaths, result):
    score = 0
    if result == 1:
        if basepaths.third_base == True:
            score += 1
            basepaths.third_base = False
        if basepaths.second_base == True:
            basepaths.third_base = True
            basepaths.second_base = False
        if basepaths.first_base == True:
            basepaths.second_base = True
        basepaths.first_base = True
    if result == 2:
        if basepaths.third_base == True:
            score += 1
            basepaths.third_base = False
        if basepaths.second_base == True:
            score += 1
        if basepaths.first_base == True:
            basepaths.third_base = True
            basepaths.first_base = False
        basepaths.second_base = True
    if result == 3:
        if basepaths.third_base == True:
            score += 1
        if basepaths.second_base == True:
            score += 1
            basepaths.second_base = False
        if basepaths.first_base == True:
            score += 1
            basepaths.first_base = False
        basepaths.third_base = True
    if result == 4:
        if basepaths.third_base == True:
            score += 1
            basepaths.third_base = False
        if basepaths.second_base == True:
            score += 1
            basepaths.second_base = False
        if basepaths.first_base == True:
            score += 1
            basepaths.first_base = False
        score += 1
    return basepaths, score


def is_game_over(inning, home_score, away_score, top_inning):
    """
    Method checks to see if the game is over.  True -> game is over.  False -> the game keeps playing
    """
    if inning >= 9 and not top_inning and home_score > away_score:
        #This handles any scenario where the home team leads after 9.5 innings
        return True
    elif inning >= 10 and top_inning and home_score != away_score:
        #This handles any scenario where the game finished the ninth inning and the score is not tied (inning number goes up before method is called)
        return True
    else:
        return False


def sim_game(home_batting_order, away_batting_order):
    home_score, away_score, outs = 0,0,0
    game_playing, top_inning = True, True
    inning = 1
    batters = away_batting_order
    while game_playing:
        base_paths = BasePaths(False, False, False)
        score = 0
        while outs < 3:
            result = sim_at_bat()
            if result == -1:
                outs += 1
                batters.current_batter = batters.current_batter.next_batter
            else:
                base_paths, score = move_runners(base_paths, result)
                batters.current_batter = batters.current_batter.next_batter
        if top_inning:
            top_inning = False
            away_batting_order = batters
            away_score += score
            batters = home_batting_order
        else:
            top_inning = True
            inning += 1
            home_score += score
            home_batting_order = batters
            batters = away_batting_order
        outs = 0
        game_playing = not is_game_over(inning, home_score, away_score, top_inning)
    return home_score, away_score


def main():
    batters = [None] *9
    bat = 0
    for i in range(8,0, -1):
        name = 'batter' + str(i)
        if i == 8:
            batters[i] = Player(name, None)
            bat += 1
        else:
            batters[i] = Player(name, batters[(i+1)])
            bat += 1
    name = 'batter0'
    batters[0] = Player(name, batters[8])
    bat += 1
    batters[8].next_batter = batters[7]
    home_batting_order = BattingOrder(batters[0])
    away_batting_order = BattingOrder(batters[0])

    home_score, away_score = sim_game(home_batting_order, away_batting_order)
    print(str(home_score) + ':home team\taway team:' + str(away_score))


main()