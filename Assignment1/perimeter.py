import sys


def compute_perimeter(frames):
    """Return the perimeter of the union of all rectangles in frames.
    Each frame is a tuple (x1, y1, x2, y2)."""
    # Step 1: Collect all boundary x and y coordinates
    xs = []
    ys = []
    for (x1, y1, x2, y2) in frames:
        xs.extend([x1, x2])
        ys.extend([y1, y2])
    xs = sorted(set(xs))
    ys = sorted(set(ys))

    # Step 2: Mark which grid cells are covered
    cols = len(xs) - 1
    rows = len(ys) - 1

    covered = []
    for i in range(cols):
        row = []
        for j in range(rows):
            row.append(False)
        covered.append(row)

    for i in range(cols):
        cell_x1 = xs[i]
        cell_x2 = xs[i + 1]
        for j in range(rows):
            cell_y1 = ys[j]
            cell_y2 = ys[j + 1]
            for (fx1, fy1, fx2, fy2) in frames:
                if fx1 <= cell_x1 and cell_x2 <= fx2 and fy1 <= cell_y1 and cell_y2 <= fy2:
                    covered[i][j] = True
                    break

    # Step 3: Compute the perimeter
    perimeter = 0

    for i in range(cols):
        for j in range(rows):
            if not covered[i][j]:
                continue

            cell_width = xs[i + 1] - xs[i]
            cell_height = ys[j + 1] - ys[j]

            # Left neighbour
            if i == 0 or not covered[i - 1][j]:
                perimeter += cell_height

            # Right neighbour
            if i == cols - 1 or not covered[i + 1][j]:
                perimeter += cell_height

            # Bottom neighbour
            if j == 0 or not covered[i][j - 1]:
                perimeter += cell_width

            # Top neighbour
            if j == rows - 1 or not covered[i][j + 1]:
                perimeter += cell_width

    return perimeter


if __name__ == '__main__':
    filename = input('Which data file do you want to use? ')
    try:
        with open(filename) as file:
            frames = []
            for line in file:
                line = line.strip()
                if line:
                    numbers = line.split()
                    x1 = int(numbers[0])
                    y1 = int(numbers[1])
                    x2 = int(numbers[2])
                    y2 = int(numbers[3])
                    frames.append((x1, y1, x2, y2))
    except FileNotFoundError:
        print('Could not open a file named', filename)
        print('Giving up...')
        sys.exit()

    result = compute_perimeter(frames)
    print(f'The perimeter is: {result}')
