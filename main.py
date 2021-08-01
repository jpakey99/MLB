from prospects.prospect_graphs import WalkRateVsWRAA
from draft.ValueAdded import *
from draft.ValueAdded import ValueAdded
from TeamViz import *
import datetime


def test():
    pass


def value_added():
    va = ValueAdded()
    va.create_image()
    va.save_image()


def prospect_graphs():
    g = WalkRateVsWRAA('2021', all=False, show_teams=['TOR', 'CLE'])
    g.create_image()
    g.save_image()


def run_team_graphs(year):
    time = datetime.datetime.now()
    string_time = time.strftime("%m-%d-%Y")
    tps = TeamPitchingStats(2021)
    tbs = TeamBattingStats(2021)
    toc = TeamOverall([tbs, tps], string_time)
    toc.create_image()
    # toc.display_image()
    toc.save_image()

    ravrf = RAvRF([tbs, tps], string_time)
    ravrf.create_image()
    # tluck.display_image()
    ravrf.save_image()

    xravxrf = xRAvxRF([tbs, tps], string_time)
    xravxrf.create_image()
    # tluck.display_image()
    xravxrf.save_image()

    trvrd = TeamRecordVsRunDif([tbs, tps], string_time)
    trvrd.create_image()
    # tluck.display_image()
    trvrd.save_image()

    trun_diff = RunDiff([tbs, tps], string_time)
    trun_diff.create_image()
    # # trun_diff.display_image()
    trun_diff.save_image()


if __name__ == '__main__':
    selection = input('0: Test\n1: Team Graphs\n2: Value Added\n3: Prospect Graphs')
    if int(selection) == 1:
        year = input('What year do you want the stats from?')
        run_team_graphs(int(year))
    elif int(selection) == 2:
        value_added()
    elif int(selection) == 3:
        prospect_graphs()
    elif int(selection) == 0:
        test()
