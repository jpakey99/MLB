from prospects.prospect_graphs import WalkRateVsWRAA

g = WalkRateVsWRAA('928')
g.create_image()
g.save_image()