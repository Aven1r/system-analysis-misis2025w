from typing import Dict, List, Tuple


def walk(root: int, node: int, graph: Dict[int, List[int]], reach: List[List[bool]]) -> None:
    for nxt in graph.get(node, []):
        if not reach[root - 1][nxt - 1]:
            reach[root - 1][nxt - 1] = True
            walk(root, nxt, graph, reach)


def solve(edges_text: str) -> Tuple[
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
]:
    edges = [tuple(map(int, line.split(","))) for line in edges_text.splitlines() if line.strip()]
    n = max(max(u, v) for u, v in edges)

    direct_parent = [[False] * n for _ in range(n)]
    graph: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    parent_of: Dict[int, int] = {}

    for u, v in edges:
        direct_parent[u - 1][v - 1] = True
        graph[u].append(v)
        parent_of[v] = u

    direct_child = [[direct_parent[j][i] for j in range(n)] for i in range(n)]

    reach = [[False] * n for _ in range(n)]
    for v in range(1, n + 1):
        walk(v, v, graph, reach)

    indirect_parent = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and reach[i][j] and not direct_parent[i][j]:
                indirect_parent[i][j] = True

    indirect_child = [[indirect_parent[j][i] for j in range(n)] for i in range(n)]

    co_level = [[False] * n for _ in range(n)]
    for i in range(1, n + 1):
        pi = parent_of.get(i)
        if pi is None:
            continue
        for j in range(1, n + 1):
            if i != j and parent_of.get(j) == pi:
                co_level[i - 1][j - 1] = True

    return direct_parent, direct_child, indirect_parent, indirect_child, co_level


def print_matrix(title: str, m: List[List[bool]]) -> None:
    print(f"{title}:")
    for row in m:
        print(" ".join("1" if x else "0" for x in row))
    print()


if __name__ == "__main__":
    s = "1,2\n1,3\n3,4\n3,5"

    dir_parent, dir_child, indir_parent, indir_child, co_parent = solve(s)

    print_matrix("Непосредственное управление", dir_parent)
    print_matrix("Непосредственное подчинение", dir_child)
    print_matrix("Опосредованное управление", indir_parent)
    print_matrix("Опосредованное подчинение", indir_child)
    print_matrix("Соподчинение на одном уровне", co_parent)
