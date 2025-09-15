import csv
import sys


def build_adjacency_matrix(rows, is_directed=False):
    edges = []
    vertices = set()

    for row in rows:
        left, right = map(int, row.split(','))
        edges.append((left, right))
        vertices.update([left, right])

    size = max(vertices)
    matrix = [[0 for _ in range(size)] for _ in range(size)]

    for u, v in edges:
        matrix[u - 1][v - 1] = 1
        if not is_directed:
            matrix[v - 1][u - 1] = 1

    return matrix


def main():
    if len(sys.argv) != 2:
        print("Usage: python task.py <file.csv>")
        sys.exit(0)

    filename = sys.argv[1]
    with open(filename, newline="") as file:
        reader = csv.reader(file)
        rows = [",".join(r) for r in reader]

    adj_matrix = build_adjacency_matrix(rows)

    for line in adj_matrix:
        print(line)


if __name__ == "__main__":
    main()
