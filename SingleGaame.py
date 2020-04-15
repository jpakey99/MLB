from dataclasses import dataclass
from random import random
from typing import Union


@dataclass
class BasePaths:
    first_base: bool
    second_base: bool
    third_base: bool


@dataclass
class AtBatInfo:
    result: str
    next_at_bat: Union[None, 'AtBatInfo']


@dataclass
class Player:
    name: str
    next_batter: Union[None, 'Player']
    at_bat = AtBatInfo


@dataclass
class BattingOrder:
    current_batter: Player


def sim_at_bat():
    """Simulates 1 at bat.
    Return: -1: out,0: walk 1: single, 2:double, 3:triple, 4:HR"""
    strike = 0
    ball = 0
    while strike < 3 and ball < 4:
        rand = random()
        if rand >= .3527:
            return -1
        elif rand < .0513:
            return 2
        elif .0513 <= rand < .0565:
            return 3
        elif .0565 <= rand < .0844:
            return 4
        elif .0844 <= rand < .1798:
            return 0
        else:
            return 1


def move_runners(base_paths, result):
    score = 0
    if result == 1:
        if base_paths.third_base:
            score += 1
            base_paths.third_base = False
        if base_paths.second_base:
            base_paths.third_base = True
            base_paths.second_base = False
        if base_paths.first_base:
            base_paths.second_base = True
        base_paths.first_base = True
    if result == 2:
        if base_paths.third_base:
            score += 1
            base_paths.third_base = False
        if base_paths.second_base:
            score += 1
        if base_paths.first_base:
            base_paths.third_base = True
            base_paths.first_base = False
        base_paths.second_base = True
    if result == 3:
        if base_paths.third_base:
            score += 1
        if base_paths.second_base:
            score += 1
            base_paths.second_base = False
        if base_paths.first_base:
            score += 1
            base_paths.first_base = False
        base_paths.third_base = True
    if result == 4:
        if base_paths.third_base:
            score += 1
            base_paths.third_base = False
        if base_paths.second_base:
            score += 1
            base_paths.second_base = False
        if base_paths.first_base:
            score += 1
            base_paths.first_base = False
        score += 1
    if result == 0:
        if base_paths.first_base and base_paths.second_base and base_paths.third_base:
            score += 1
        elif base_paths.first_base and base_paths.second_base:
            base_paths.third_base = True
        elif base_paths.first_base:
            base_paths.second_base = True
    return base_paths, score


def is_game_over(inning, home_score, away_score, top_inning):
    """
    Method checks to see if the game is over.  True -> game is over.  False -> the game keeps playing
    """
    if inning >= 9 and not top_inning and home_score > away_score:
        # This handles any scenario where the home team leads after 9.5 innings
        return True
    elif inning >= 10 and top_inning and home_score != away_score:
        # This handles any scenario where the game finished the ninth inning and the score is not tied (inning number goes up before method is called)
        return True
    else:
        return False


def add_at_bat(player, result):
    string = ''
    if result == -1:
        string = 'out'
    elif result == 1:
        string = 'single'
    elif result == 2:
        string = 'double'
    elif result == 3:
        string = 'triple'
    elif result == 4:
        string = 'homerun'
    if player.at_bat is None:
        player.at_bat = AtBatInfo(string, None)
    else:
        # print_player(player)
        at_bat = player.at_bat
        print(at_bat)
        while at_bat is not None:
            if at_bat.next_at_bat is None:
                player.at_bat.next_at_bat = AtBatInfo(string, None)
            at_bat = at_bat.next_at_bat


def print_player(player):
    string = player.name + ' '
    while player.at_bat is not None:
        string += player.at_bat.result
    return string


def sim_game(home_batting_order, away_batting_order):
    home_score, away_score, outs = 0, 0, 0
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
                #add_at_bat(batters.current_batter, result)
                print(batters.current_batter.name + ':' + str(result))
                batters.current_batter = batters.current_batter.next_batter
            else:
                base_paths, score = move_runners(base_paths, result)
                #add_at_bat(batters.current_batter, result)
                print(batters.current_batter.name + ':' + str(result))
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


def print_batting_order(batting_order):
    for i in range(0,9):
        hey = batting_order.current_batter.name
        print(hey)
        batting_order.current_batter = batting_order.current_batter.next_batter


def get_batting_order():
    batters = [None] * 9
    for i in range(8, 0, -1):
        name = 'batter' + str(i)
        if i == 8:
            batters[i] = Player(name, None)
        else:
            batters[i] = Player(name, batters[(i + 1)])
    name = 'batter0'
    batters[0] = Player(name, batters[1])
    batters[8].next_batter = batters[0]
    return batters


def main():
    batters = get_batting_order()
    home_batting_order = BattingOrder(batters[0])
    away_batting_order = BattingOrder(batters[0])

    home_score, away_score = sim_game(home_batting_order, away_batting_order)
    print(str(home_score) + ':home team\taway team:' + str(away_score))


main()
