from prospects.prospect_graphs import WalkRateVsWRAA
from draft.ValueAdded import *
from draft.ValueAdded import ValueAdded


# va = ValueAdded()
# va.create_image()
# va.save_image()


g = WalkRateVsWRAA('2008', all=False, show_teams=['PIT'])
g.create_image()
g.save_image()