from game import W, C, B, P, PB, CB, G

level_1 = [
    [0, 0, W, W, W, 0, 0, 0, 0],
    [0, 0, W, B, W, 0, 0, 0, 0],
    [0, 0, W, G, W, W, W, W, 0],
    [W, W, W, C, 0, C, B, W, 0],
    [W, B, 0, C, P, W, W, W, 0],
    [W, W, W, W, C, W, 0, 0, 0],
    [0, 0, 0, W, B, W, 0, 0, 0],
    [0, 0, 0, W, W, W, 0, 0, 0],
]

level_2 = [
    [W, W, W, W, W, 0, 0, 0, 0],
    [W, 0, 0, 0, W, 0, 0, 0, 0],
    [W, 0, C, 0, W, 0, W, W, W],
    [W, 0, C, P, W, 0, W, B, W],
    [W, W, W, C, W, W, W, B, W],
    [0, W, W, 0, 0, 0, 0, B, W],
    [0, W, 0, 0, 0, W, 0, 0, W],
    [0, W, 0, 0, 0, W, W, W, W],
    [0, W, W, W, W, W, W, W, W],
]


level_3 = [
    [0, W, W, W, W, 0],
    [W, W, 0, 0, W, 0],
    [W, 0, P, C, W, 0],
    [W, W, C, 0, W, W],
    [W, W, 0, C, 0, W],
    [W, B, C, 0, 0, W],
    [W, B, B, CB, B, W],
    [W, W, W, W, W, W],
]

level_4 = [
    [0, W, W, W, W, 0, 0, 0],
    [0, W, 0, 0, W, W, W, 0],
    [0, W, 0, 0, 0, 0, W, 0],
    [W, W, W, C, W, P, W, W],
    [W, B, W, 0, W, 0, 0, W],
    [W, B, C, 0, 0, W, 0, W],
    [W, B, 0, 0, 0, C, 0, W],
    [W, W, W, W, W, W, W, W],
]

level_5 = [
    [0, 0, W, W, W, W, W, W],
    [0, 0, W, 0, 0, 0, 0, W],
    [W, W, W, C, C, C, 0, W],
    [W, 0, 0, C, B, B, 0, W],
    [W, P, C, B, B, B, W, W],
    [W, W, W, W, 0, 0, W, 0],
    [0, 0, 0, W, W, W, W, 0],
]

level_6 = [
    [0, 0, W, W, W, W, W, 0],
    [W, W, W, 0, 0, P, W, 0],
    [W, 0, 0, C, B, 0, W, W],
    [W, 0, 0, B, C, B, 0, W],
    [W, W, W, 0, CB, C, 0, W],
    [0, 0, W, 0, 0, 0, W, W],
    [0, 0, W, W, W, W, W, 0],
]

level_7 = [
    [0, 0, W, W, W, W, 0, 0],
    [0, 0, W, B, B, W, 0, 0],
    [0, W, W, 0, B, W, W, 0],
    [0, W, 0, 0, C, B, W, 0],
    [W, W, 0, C, 0, 0, W, W],
    [W, 0, 0, W, C, C, 0, W],
    [W, 0, 0, P, 0, 0, 0, W],
    [W, W, W, W, W, W, W, W],
]

level_8 = [
    [W, W, W, W, W, W, W, W],
    [W, 0, 0, W, 0, 0, 0, W],
    [W, 0, C, B, B, C, 0, W],
    [W, P, C, B, CB, 0, W, W],
    [W, 0, C, B, B, C, 0, W],
    [W, 0, 0, W, 0, 0, 0, W],
    [W, W, W, W, W, W, W, W],
]

levels = [level_1, level_2, level_3, level_4, level_5, level_6, level_7, level_8]
