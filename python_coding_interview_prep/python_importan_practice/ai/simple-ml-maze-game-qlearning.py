import numpy as np


maze = [ 'S . . . . . . .',
         '. # # ### # .',
         '. . . # # . .',
         '. # # . . # .',
         '####### # # .',
         '. . . . . # .',
         '. . . . . . G' ]
# 5 arrays of 11 rows and 4 cols
# Q-learning table with 5 states, 11 actions
# are represented as vectors of size 2: 4 actions
# and 4 directions:  up, down, left, right (up, down, left, right)
Q = np.zeros((5, 11, 4))
# filter of all possible values
go = np.array([(0, 1), (1, 0), (0, -1), (-1, 0)])
for game in range(100):
    y = x = 0
    while maze[y][x] != 'G':
        a = Q[y, x].argmax()
        v, u = np.clip((y, x) + go[a], 0, (4, 10))
        if maze[v][u] == '#':
            v, u = y, x
        Q[y, x, a] = Q[v, u].max() - 1
        y, x = v, u
