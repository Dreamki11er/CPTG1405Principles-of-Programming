"""
Verify expected values by computing them with the same algorithm.
This is a self-consistency check: the test runner uses the same
compute_perimeter function, so expected values must match.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from perimeter import compute_perimeter

test_cases = {
    "1_single.txt":      18,
    "2_separate.txt":    20,
    "3_two_overlap.txt": 28,
    "4_three_overlap.txt": 26,
    "5_staircase.txt":   30,
    "6_donut.txt":       30,
    "7_nested.txt":      40,
    "8_shared_edge.txt": 26,
    "9_corner_touch.txt": 32,
    "10_cross.txt":      800,
}

print("Expected value verification")
print("-" * 45)
for fname, expected in test_cases.items():
    path = os.path.join(os.path.dirname(__file__), fname)
    frames = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                p = line.split()
                frames.append((int(p[0]), int(p[1]), int(p[2]), int(p[3])))
    result = compute_perimeter(frames)
    match = "MATCH" if result == expected else f"MISMATCH (got {result})"
    print(f"  {fname:25s} expect {expected:5d}  {match}")
