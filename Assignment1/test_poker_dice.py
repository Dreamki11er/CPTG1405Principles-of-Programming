"""
Extra test suite for poker_dice.py
Usage: python test_poker_dice.py
"""

import sys
import io
from random import seed

# Import the module properly
import poker_dice

passed = 0
failed = 0

def test(name, actual, expected):
    global passed, failed
    if actual == expected:
        passed += 1
    else:
        failed += 1
        print(f"  FAIL [{name}]")
        print(f"     expected: {expected!r}")
        print(f"     got:      {actual!r}")


# ============================================================
# 1. classify_pokers - all hand categories
# ============================================================
print("=" * 50)
print("1. classify_pokers - hand categories")
print("=" * 50)

cf = poker_dice.classify_pokers

# Five of a kind: [5]
test("Five of a kind (all Aces)", cf([0, 0, 0, 0, 0]), "Five of a kind")
test("Five of a kind (all 9s)",   cf([4, 4, 4, 4, 4]), "Five of a kind")

# Four of a kind: [4, 1]
test("Four of a kind (4 Aces)", cf([0, 0, 0, 0, 1]), "Four of a kind")
test("Four of a kind (4 Jacks)", cf([3, 5, 5, 5, 5]), "Four of a kind")

# Full house: [3, 2]
test("Full house (3 Aces + 2 Kings)", cf([0, 0, 0, 1, 1]), "Full house")
test("Full house (3 Queens + 2 Jacks)", cf([2, 2, 3, 3, 3]), "Full house")

# Three of a kind: [3, 1, 1]
test("Three of a kind", cf([0, 0, 0, 1, 2]), "Three of a kind")
test("Three of a kind (3x9)", cf([1, 3, 4, 4, 4]), "Three of a kind")

# Two pair: [2, 2, 1]
test("Two pair", cf([0, 0, 1, 1, 2]), "Two pair")
test("Two pair (Kings + 9s)", cf([1, 1, 4, 4, 5]), "Two pair")

# One pair: [2, 1, 1, 1]
test("One pair", cf([0, 0, 1, 2, 3]), "One pair")
test("One pair (pair of 10s)", cf([1, 2, 3, 5, 5]), "One pair")

# Straight: {0,1,2,3,4} = Ace-King-Queen-Jack-10
#            {1,2,3,4,5} = King-Queen-Jack-10-9
test("Straight (Ace-high)", cf([0, 1, 2, 3, 4]), "Straight")
test("Straight (9-high)", cf([1, 2, 3, 4, 5]), "Straight")
test("Straight (unsorted)", cf([3, 0, 1, 4, 2]), "Straight")

# Bust: all different, not a straight
test("Bust (Ace King Queen Jack 9 -> {0,1,2,3,5})", cf([0, 1, 2, 3, 5]), "Bust")
test("Bust (Ace King Jack 10 9 -> {0,1,3,4,5})", cf([0, 1, 3, 4, 5]), "Bust")
test("Bust (Ace Queen Jack 10 9 -> {0,2,3,4,5})", cf([0, 2, 3, 4, 5]), "Bust")

print(f"   -> {passed}/{passed + failed} so far")


# ============================================================
# 2. simulate - edge cases
# ============================================================
print("\n" + "=" * 50)
print("2. simulate - no crash + sum check")
print("=" * 50)

sim = poker_dice.simulate

# Small n
seed(0)
print("  simulate(1):")
sim(1)
print()

seed(0)
print("  simulate(5):")
sim(5)
print()

# Large n
seed(0)
print("  simulate(100000):")
sim(100000)
print()

# simulate(0) - div by zero?
print("  simulate(0) test:")
try:
    sim(0)
    passed += 1
    print("  OK: simulate(0) ran without crashing")
except ZeroDivisionError:
    failed += 1
    print("  FAIL: simulate(0) raised ZeroDivisionError")
except Exception as e:
    failed += 1
    print(f"  FAIL: simulate(0) raised {e}")


# ============================================================
# 3. roll_dice - return value checks
# ============================================================
print("\n" + "=" * 50)
print("3. roll_dice - return value checks")
print("=" * 50)

rd = poker_dice.roll_dice
all_ok = True
for i in range(20):
    result = rd()
    if len(result) != 5:
        print(f"  FAIL: roll_dice returned length {len(result)}, expected 5")
        all_ok = False; failed += 1; break
    if not all(0 <= v <= 5 for v in result):
        print(f"  FAIL: roll_dice value out of 0-5 range: {result}")
        all_ok = False; failed += 1; break
    if result != sorted(result):
        print(f"  FAIL: roll_dice not sorted: {result}")
        all_ok = False; failed += 1; break
if all_ok:
    passed += 1
    print("  OK: roll_dice passed (20 random tests)")


# ============================================================
# 4. ask_keep - input parsing (via stdin simulation)
# ============================================================
print("\n" + "=" * 50)
print("4. ask_keep - input parsing")
print("=" * 50)

ask = poker_dice.ask_keep

def fake_input(answers):
    """Return a function that yields answers one by one, then raises EOFError."""
    it = iter(answers)
    def _fake(prompt=""):
        return next(it)
    return _fake

def test_keep(name, answers, current_hand, expected):
    global passed, failed
    saved = __builtins__.input
    __builtins__.input = fake_input(answers)
    try:
        result = ask("test", current_hand)
        if result == expected:
            passed += 1
        else:
            failed += 1
            print(f"  FAIL [{name}]")
            print(f"     expected: {expected!r}")
            print(f"     got:      {result!r}")
    except Exception as e:
        failed += 1
        print(f"  FAIL [{name}] - exception: {e}")
    finally:
        __builtins__.input = saved

hand_5 = [0, 1, 2, 3, 4]       # Ace, King, Queen, Jack, 10
hand_pair = [0, 0, 2, 3, 5]    # Ace Ace Queen Jack 9
hand_full = [1, 1, 1, 3, 3]    # King King King Jack Jack

# Empty input -> keep none
test_keep("empty input", [""], hand_5, [])

# "all" / "All"
test_keep("all (lowercase)", ["all"], hand_5, hand_5[:])
test_keep("All (capitalized)", ["All"], hand_5, hand_5[:])

# Full hand in different order -> keep all (order follows input)
test_keep("full hand shuffled", ["King Ace Jack Queen 10"], hand_5,
          [1, 0, 3, 2, 4])

# Keep specific dice
test_keep("keep pair of Aces", ["Ace Ace"], hand_pair, [0, 0])
test_keep("keep one Queen", ["Queen"], hand_pair, [2])   # hand_pair = [0,0,2,3,5]

# Invalid -> then valid (retry)
test_keep("bad case then good", ["ace", "Ace"], hand_5, [0])
test_keep("too many then good", ["Ace Ace Ace", "Ace"], hand_pair, [0])
test_keep("bad number then empty", ["11", ""], hand_5, [])
test_keep("bad word then empty", ["Joker", ""], hand_5, [])

# Count exceeds hand
test_keep("ask 4 Kings, hand has 3", ["King King King King", "King"], hand_full, [1])


# ============================================================
# 5. More edge cases
# ============================================================
print("\n" + "=" * 50)
print("5. More edge cases")
print("=" * 50)

# classify_pokers with empty list (defensive)
try:
    result = cf([])
    print(f"  classify_pokers([]) returned: {result!r}")
    passed += 1
except Exception as e:
    failed += 1
    print(f"  FAIL: classify_pokers([]) raised: {e}")

# 100 consecutive roll_dice should have variety
samples = set()
for _ in range(100):
    samples.add(tuple(rd()))
if len(samples) > 1:
    passed += 1
    print("  OK: 100 roll_dice calls produced varied results")
else:
    failed += 1
    print("  FAIL: 100 roll_dice calls all identical")

# Many roll_dice + classify_pokers never crashes
for _ in range(1000):
    L = rd()
    cat = cf(L)
    if cat not in ("Five of a kind", "Four of a kind", "Full house",
                    "Straight", "Three of a kind", "Two pair", "One pair", "Bust"):
        failed += 1
        print(f"  FAIL: unknown category: {cat!r}")
        break
else:
    passed += 1
    print("  OK: 1000 roll_dice + classify all returned valid categories")


# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 50)
total = passed + failed
print(f"Result: {passed}/{total} passed", end="")
if failed > 0:
    print(f", {failed} failed")
    sys.exit(1)
else:
    print(" - ALL PASSED")
