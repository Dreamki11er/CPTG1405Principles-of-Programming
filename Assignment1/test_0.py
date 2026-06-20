from random import randint

# L = []
# for i in range(5):
#     L.append(randint(0, 5))
pokers = {0: 'Ace',
          1: 'King',
          2: 'Queen',
          3: 'Jack',
          4: '10',
          5: '9'}

L = [randint(0, 5) for i in range(5)]
L.sort()
L1 = [pokers[i] for i in L]

def simulate(n):
    categories = {'Five of a kind': 0,
                  'Four of a kind': 0,
                  'Full house': 0,
                  'Straight': 0,
                  'Three of a kind': 0,
                  'Two pair': 0,
                  'One pair': 0}
    for _ in range(n):
        category = roll_dice()
        if category == 'Bust':
            continue
        else:
            categories[category] += 1
    
    print(categories)
    
    for key, value in categories.items():
        percentage = value / n * 100
        print(f'{key}: {percentage:.2f}%')

def roll_dice():
    L = [randint(0, 5) for i in range(5)]
    L.sort()
    category = ' '
    classify = [0, 0, 0, 0, 0, 0]
    for i in L:
        classify[i] += 1
    classify.sort()
    classify.reverse()

    if classify == [5, 0, 0, 0, 0, 0]:
        category = 'Five of a kind'
    elif classify == [4, 1, 0, 0, 0, 0]:
        category = 'Four of a kind'
    elif classify == [3, 2, 0, 0, 0, 0]:
        category = 'Full house'
    elif classify == [3, 1, 1, 0, 0, 0]:
        category = 'Three of a kind'
    elif classify == [2, 2, 1, 0, 0, 0]:
        category = 'Two pair'
    elif classify == [2, 1, 1, 1, 0, 0]:
        category = 'One pair'
    elif classify == [1, 1, 1, 1, 1, 0]:
        value_set = set(L)
        if value_set == {0, 1, 2, 3, 4} or value_set == {1, 2, 3, 4, 5}:
            category = 'Straight'
        else:
            category = 'Bust'

    return category

# def check_category_of_poker(L):
#     category = ' '
#     classify = [0, 0, 0, 0, 0, 0]
#     for i in L:
#         classify[i] += 1
#     classify.sort()
#     classify.reverse()

#     if classify == [5, 0, 0, 0, 0, 0]:
#         category = 'Five of a kind'
#     elif classify == [4, 1, 0, 0, 0, 0]:
#         category = 'Four of a kind'
#     elif classify == [3, 2, 0, 0, 0, 0]:
#         category = 'Full house'
#     elif classify == [3, 1, 1, 0, 0, 0]:
#         category = 'Three of a kind'
#     elif classify == [2, 2, 1, 0, 0, 0]:
#         category = 'Two pair'
#     elif classify == [2, 1, 1, 1, 0, 0]:
#         category = 'One pair'
#     elif classify == [1, 1, 1, 1, 1, 0]:
#         value_set = set(L)
#         if value_set == {0, 1, 2, 3, 4} or value_set == {1, 2, 3, 4, 5}:
#             category = 'Straight'
#         else:
#             category = 'Bust'

#     return category

simulate(10000)