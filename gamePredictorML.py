from sklearn.neural_network import MLPClassifier
import pybaseball, mlbgame, statsapi, requests, datetime


# X = [[5, 0.], [10., 1.]]
# y = [0, 1]
# clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
# clf.fit(X, y)
# clf.n_outputs_ = 1
# # MLPClassifier(alpha=1e-05, hidden_layer_sizes=(5, 2), random_state=1, solver='lbfgs')
# print(clf.predict([[15, 10]]))


# for date since 2015:
print('getting scheule')
# schedule = statsapi.schedule(start_date='2015-04-05', end_date='2015-05-05')
schedule = pybaseball.schedule_and_record(2015, 'PIT')
print('GAMES: ', len(schedule))
for day in schedule:
    print(day)
    # for each game in schedule:
        # grab teamid
        # save following information [home, 1b, 2b, tripples, hr, rbi, wrc+, bb, so, gb, fb, ld, r, h, r, bb, so, hr, FIP]