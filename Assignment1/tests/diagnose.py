"""
Diagnostic: print coverage grid and perimeter breakdown for a test file.
Usage: python tests/diagnose.py <test_file>
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from perimeter import compute_perimeter


def diagnose(filepath):
    frames = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line:
                p = line.split()
                frames.append((int(p[0]), int(p[1]), int(p[2]), int(p[3])))

    print(f"Frames: {frames}")

    xs = []; ys = []
    for (x1, y1, x2, y2) in frames:
        xs.extend([x1, x2]); ys.extend([y1, y2])
    xs = sorted(set(xs)); ys = sorted(set(ys))

    print(f"xs = {xs}")
    print(f"ys = {ys}")
    print(f"Grid: {len(xs)-1} cols x {len(ys)-1} rows")

    # Coverage grid
    cols, rows = len(xs)-1, len(ys)-1
    covered = [[False]*rows for _ in range(cols)]

    for i in range(cols):
        cx1, cx2 = xs[i], xs[i+1]
        for j in range(rows):
            cy1, cy2 = ys[j], ys[j+1]
            for (fx1, fy1, fx2, fy2) in frames:
                if fx1 <= cx1 and cx2 <= fx2 and fy1 <= cy1 and cy2 <= fy2:
                    covered[i][j] = True
                    break

    # Print grid (flipped vertically: top row first)
    print("\nCoverage grid (T=covered, .=empty):")
    print("        ", end="")
    for i in range(cols):
        print(f"col{i}  ", end="")
    print()
    for j in range(rows-1, -1, -1):
        print(f"row{j} y=[{ys[j]:3d},{ys[j+1]:3d}] ", end="")
        for i in range(cols):
            marker = "T" if covered[i][j] else "."
            w = xs[i+1]-xs[i]
            h = ys[j+1]-ys[j]
            print(f"[{marker} {w}x{h:2d}]", end="")
        print()

    # Perimeter breakdown
    print(f"\nPerimeter breakdown:")
    total = 0
    for i in range(cols):
        for j in range(rows):
            if not covered[i][j]:
                continue
            w, h = xs[i+1]-xs[i], ys[j+1]-ys[j]
            contrib = 0
            parts = []
            if i == 0 or not covered[i-1][j]:
                contrib += h; parts.append(f"L+{h}")
            if i == cols-1 or not covered[i+1][j]:
                contrib += h; parts.append(f"R+{h}")
            if j == 0 or not covered[i][j-1]:
                contrib += w; parts.append(f"B+{w}")
            if j == rows-1 or not covered[i][j+1]:
                contrib += w; parts.append(f"T+{w}")
            if contrib > 0:
                print(f"  [{i}][{j}] ({xs[i]},{ys[j]})-({xs[i+1]},{ys[j+1]}) "
                      f"w={w} h={h}: {' '.join(parts)} = {contrib}")
            total += contrib
    print(f"\nTotal perimeter: {total}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python tests/diagnose.py <test_file>")
        sys.exit(1)
    diagnose(sys.argv[1])
