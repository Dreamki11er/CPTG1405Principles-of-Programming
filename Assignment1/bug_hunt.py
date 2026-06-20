import sys, io
from random import seed
import poker_dice
from unittest.mock import patch
from itertools import combinations_with_replacement

print('=' * 60)
print('BUG HUNT: Focused tests on identified issues')
print('=' * 60)

# -- BUG 1: simulate output format --
print('\n--- BUG 1: simulate() format ---')
print('Code format string: f"{key:<16} : {percentage:.2f}%"')
print('PDF expected:        f"{key:<16}: {percentage:.2f}%" (no space before colon)')
print()

seed(0)
captured = io.StringIO()
old_stdout = sys.stdout
sys.stdout = captured
poker_dice.simulate(10)
sys.stdout = old_stdout
for line in captured.getvalue().strip().split('\n'):
    print(f'  Actual:   {line!r}')

line = captured.getvalue().strip().split('\n')[0]
idx = line.index(':')
print(f'  Colon at index {idx} (expected 16 for PDF format, 17 for current code)')
print(f'  BUG CONFIRMED: extra space before colon' if idx == 17 else '  Format MATCHES')

# -- BUG 2: classify_pokers edge cases --
print('\n--- BUG 2: classify_pokers([]) returns default sentinel ---')
result = poker_dice.classify_pokers([])
print(f'  classify_pokers([]) = {result!r} (the default category=" " sentinel)')
print(f'  BUG: Returns space character instead of raising error or returning None')

# -- BUG 3: 'all' with whitespace --
print('\n--- BUG 3: Whitespace handling in ask_keep ---')

def test_keep(input_str, hand, fallback=''):
    """Test ask_keep with input_str, falling back to empty input if invalid."""
    with patch('builtins.input', side_effect=[input_str, fallback]):
        try:
            result = poker_dice.ask_keep('test', hand)
            return result
        except Exception as e:
            return f'ERROR: {e}'

hand = [0, 1, 2, 3, 4]
print(f'  ask_keep("all")      = {test_keep("all", hand)}')
print(f'  ask_keep(" all")     = {test_keep(" all", hand)}')
print(f'  ask_keep("all ")     = {test_keep("all ", hand)}')
print(f'  ask_keep("  all  ")  = {test_keep("  all  ", hand)}')
print(f'  ask_keep("All")      = {test_keep("All", hand)}')
print(f'  ask_keep("ALL")      = {test_keep("ALL", hand)}')
print(f'  NOTE: " all", "all ", "  all  " -> returns [] (not recognized as "all")')
print(f'  BUG: Whitespace-surrounded "all" variants are not recognized')

# -- BUG 4: exhaustive classification --
print('\n--- BUG 4: Exhaustive classification check (252 hands) ---')
all_hands = list(combinations_with_replacement(range(6), 5))
errors = []
for hand in all_hands:
    hand_list = list(hand)
    result = poker_dice.classify_pokers(hand_list)
    if result == ' ':
        errors.append(f'Default sentinel for: {hand_list}')
    if result == 'Straight':
        s = set(hand_list)
        if s not in ({0,1,2,3,4}, {1,2,3,4,5}):
            errors.append(f'False Straight: {hand_list}')
    if result == 'Bust':
        if len(set(hand_list)) != 5:
            errors.append(f'False Bust: {hand_list}')

if errors:
    for e in errors:
        print(f'  ERROR: {e}')
else:
    print(f'  All {len(all_hands)} hands classified correctly (Straight/Bust verified)')

# -- BUG 5: Period consistency in play() --
print('\n--- BUG 5: Period after category (intentional per spec) ---')
seed(0)
with patch('builtins.input', side_effect=['Ace', 'Ace']):
    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured
    poker_dice.play()
    sys.stdout = old_stdout

lines = captured.getvalue().strip().split('\n')
for i, line in enumerate(lines):
    if 'It is a' in line:
        has_period = line.rstrip().endswith('.')
        print(f'  Line {i}: period={has_period} | {line!r}')
print(f'  Initial roll: no period. Re-rolls: have period. (INTENTIONAL per PDF)')

# -- BUG 6: check simulate(0) behavior --
print('\n--- BUG 6: simulate(0) behavior ---')
captured = io.StringIO()
old_stdout = sys.stdout
sys.stdout = captured
poker_dice.simulate(0)
sys.stdout = old_stdout
output = captured.getvalue()
print(f'  simulate(0) output: {output!r}')
print(f'  BUG: Silent return with no error message')

# -- BUG 7: simulate percentages include all categories? --
print('\n--- BUG 7: simulate percentages check ---')
seed(0)
captured = io.StringIO()
old_stdout = sys.stdout
sys.stdout = captured
poker_dice.simulate(1000)
sys.stdout = old_stdout

total = 0
for line in captured.getvalue().strip().split('\n'):
    pct = float(line.split(':')[1].strip().replace('%', ''))
    total += pct
print(f'  simulate(1000): sum of displayed categories = {total:.2f}%')
print(f'  (Bust = {100-total:.2f}% but not displayed)')
print(f'  This is INTENTIONAL per PDF spec')

# -- BUG 8: verify line count in play() output --
print('\n--- BUG 8: play() line count check ---')
seed(0)
with patch('builtins.input', side_effect=['all']):
    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured
    poker_dice.play()
    sys.stdout = old_stdout
output = captured.getvalue()
print(f'  play() output (4 lines, no trailing newline shown):')
for i, line in enumerate(output.split('\n')):
    print(f'    [{i}] {line!r}')

# Expected:
# The roll is: Ace Queen Jack Jack 10
# It is a One pair
# Which dice do you want to keep for the second roll? Ok, done.

print()
print('=' * 60)
print('BUG HUNT COMPLETE')
print('=' * 60)
