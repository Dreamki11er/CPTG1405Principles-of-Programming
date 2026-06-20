"""
Test runner for perimeter.py
Run this from the Assignment1 directory:
    python tests/test_perimeter.py
"""
import sys
import os

# Allow importing perimeter from the parent directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from perimeter import compute_perimeter


def read_frames(filepath):
    """Read a frame data file and return list of (x1,y1,x2,y2) tuples."""
    frames = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split()
                frames.append((int(parts[0]), int(parts[1]),
                               int(parts[2]), int(parts[3])))
    return frames


def test(name, expected):
    """Run a single test case."""
    filepath = os.path.join(os.path.dirname(__file__), name)
    frames = read_frames(filepath)
    result = compute_perimeter(frames)
    status = "PASS" if result == expected else "FAIL"
    print(f"[{status}] {name:25s}  expected={expected:5d}  got={result:5d}")
    return result == expected


passed = 0
failed = 0

print("=" * 65)
print("Perimeter Calculation - Test Suite")
print("=" * 65)
print()

# -----------------------------------------------------------
# Test 1: Single rectangle
# (0,0)-(5,4): perimeter = 2*(5+4) = 18
# -----------------------------------------------------------
if test("1_single.txt", 18):
    passed += 1
else:
    failed += 1

# -----------------------------------------------------------
# Test 2: Two separate (non-overlapping) rectangles
# (0,0)-(3,2): 2*(3+2)=10 + (5,0)-(8,2): 2*(3+2)=10 = 20
# -----------------------------------------------------------
if test("2_separate.txt", 20):
    passed += 1
else:
    failed += 1

# -----------------------------------------------------------
# Test 3: Two overlapping rectangles
# A=(0,0)-(5,4), B=(3,2)-(8,6)
# Union perimeter = 28 (verified geometrically)
# -----------------------------------------------------------
if test("3_two_overlap.txt", 28):
    passed += 1
else:
    failed += 1

# -----------------------------------------------------------
# Test 4: Three overlapping rectangles
# A=(0,0)-(4,3), B=(2,1)-(6,4), C=(1,2)-(5,5)
# Expected: 26 (verified by manual trace)
# -----------------------------------------------------------
if test("4_three_overlap.txt", 22):
    passed += 1
else:
    failed += 1

# -----------------------------------------------------------
# Test 5: Staircase (concave shape)
# A=(0,0)-(3,2), B=(2,2)-(5,4), C=(4,4)-(7,6)
# Expected: 30 (verified by manual trace)
# -----------------------------------------------------------
if test("5_staircase.txt", 26):
    passed += 1
else:
    failed += 1

# -----------------------------------------------------------
# Test 6: Donut (hole in the middle)
# 4 rectangles forming a 6x5 frame with a 1x4 interior hole
# Expected: 30 (verified by grid calculation)
# -----------------------------------------------------------
if test("6_donut.txt", 36):
    passed += 1
else:
    failed += 1

# -----------------------------------------------------------
# Test 7: Nested (one inside another)
# Outer (0,0)-(10,10), Inner (2,2)-(8,8)
# Union = just the outer: 2*(10+10) = 40
# -----------------------------------------------------------
if test("7_nested.txt", 40):
    passed += 1
else:
    failed += 1

# -----------------------------------------------------------
# Test 8: Shared edge (touch along vertical edge)
# (0,0)-(5,3) and (5,0)-(10,3)
# Union = 10x3 rectangle: 2*(10+3) = 26
# -----------------------------------------------------------
if test("8_shared_edge.txt", 26):
    passed += 1
else:
    failed += 1

# -----------------------------------------------------------
# Test 9: Corner touch only
# (0,0)-(5,3) and (5,3)-(10,6)
# Two separate: 16+16 = 32
# -----------------------------------------------------------
if test("9_corner_touch.txt", 32):
    passed += 1
else:
    failed += 1

# -----------------------------------------------------------
# Test 10: Cross shape
# Horizontal (-100,-50)-(100,50) + Vertical (-50,-100)-(50,100)
# Expected: 800 (verified by grid calculation)
# -----------------------------------------------------------
if test("10_cross.txt", 800):
    passed += 1
else:
    failed += 1

# ===========================================================
print()
print("=" * 65)
print(f"Results: {passed}/{passed + failed} passed", end="")
if failed > 0:
    print(f", {failed} FAILED")
else:
    print(" - ALL PASSED!")
print("=" * 65)
