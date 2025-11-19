import json


def to_list(x):
    return x if isinstance(x, list) else [x]


def all_items(ranking):
    out = []
    for g in ranking:
        out.extend(to_list(g))
    return out


def build_matrix(ranking, items):
    n = len(items)
    pos = {v: i for i, v in enumerate(items)}
    m = [[0] * n for _ in range(n)]

    for gi, group in enumerate(ranking):
        group = to_list(group)

        for x in group:
            ix = pos[x]
            for y in items:
                m[ix][pos[y]] = 1

        for prev in ranking[:gi]:
            prev = to_list(prev)
            for x in group:
                ix = pos[x]
                for p in prev:
                    ip = pos[p]
                    m[ix][ip] = 0
                    m[ip][ix] = 1

    return m


def find_contradictions(A, B, items):
    n = len(items)
    res = []
    for i in range(n):
        for j in range(i + 1, n):
            a_ij, a_ji = A[i][j], A[j][i]
            b_ij, b_ji = B[i][j], B[j][i]

            if a_ij == 1 and a_ji == 0 and b_ij == 0 and b_ji == 1:
                res.append([items[i], items[j]])
            if a_ij == 0 and a_ji == 1 and b_ij == 1 and b_ji == 0:
                res.append([items[j], items[i]])
    return res


def main(json_a: str, json_b: str) -> str:
    rank_a = json.loads(json_a)
    rank_b = json.loads(json_b)

    items = sorted(set(all_items(rank_a)) | set(all_items(rank_b)))

    A = build_matrix(rank_a, items)
    B = build_matrix(rank_b, items)

    contradictions = find_contradictions(A, B, items)
    return json.dumps(contradictions, ensure_ascii=False)


if __name__ == "__main__":
    a = json.dumps([1, [2, 3], 4, [5, 6, 7], 8, 9, 10])
    b = json.dumps([[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]])
    print(main(a, b))
