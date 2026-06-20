from random import randint

pokers = {0: 'Ace',
          1: 'King',
          2: 'Queen',
          3: 'Jack',
          4: '10',
          5: '9'}

name_to_value = {'Ace': 0, 
                 'King': 1, 
                 'Queen': 2, 
                 'Jack': 3, 
                 '10': 4, 
                 '9': 5}


def play():
    L = roll_dice()
    hand = ' '.join(pokers[i] for i in L)
    category = classify_pokers(L)
    print(f'The roll is: {hand}')
    print(f'It is a {category}')

    for roll_num in range(1, 3):         
        label = ['second', 'third'][roll_num - 1]
        kept = ask_keep(label, L)

        if sorted(kept) == sorted(L):
            print('Ok, done.')
            return

        L = sorted(kept + [randint(0, 5) for _ in range(5 - len(kept))])

        hand = ' '.join(pokers[i] for i in L)
        category = classify_pokers(L)
        print(f'The roll is: {hand}')
        print(f'It is a {category}.')



def simulate(n):
    categories = {'Five of a kind': 0,
                  'Four of a kind': 0,
                  'Full house': 0,
                  'Straight': 0,
                  'Three of a kind': 0,
                  'Two pair': 0,
                  'One pair': 0}
    
    for _ in range(n):
        L = roll_dice()
        category = classify_pokers(L)
        if category == 'Bust':
            continue
        else:
            categories[category] += 1

    if n == 0:
        return
    for key, value in categories.items():
        percentage = value / n * 100
        print(f'{key:<16} : {percentage:.2f}%')

def roll_dice():
    L = [randint(0, 5) for i in range(5)]
    return sorted(L)


def classify_pokers(n):
    L = n
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

def ask_keep(label, current_hand):
    
    while True:
        answer = input(f'Which dice do you want to keep for the {label} roll? ')
       
        if answer == '':
            return []
        
        if answer.lower() == 'all':
            return current_hand[:]

        words = answer.split()
        result = []
        valid = True
        for w in words:
            if w not in name_to_value:
                valid = False
                break
            result.append(name_to_value[w])

        if not valid:
            print('That is not possible, try again!')
            continue

        for v in set(result):
            if result.count(v) > current_hand.count(v):
                print('That is not possible, try again!')
                valid = False
                break

        if valid:
            return result

