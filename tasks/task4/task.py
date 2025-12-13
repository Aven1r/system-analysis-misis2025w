import json
import numpy as np


def as_group(x):
    return x if isinstance(x, list) else [x]


def flatten(ranking):
    out = []
    for g in ranking:
        out.extend(as_group(g))
    return out


def build_matrix(ranking, items):
    n = len(items)
    idx = {v: i for i, v in enumerate(items)}
    m = np.zeros((n, n), dtype=int)

    for level, group in enumerate(ranking):
        group = as_group(group)

        for x in group:
            ix = idx[x]
            m[ix, :] = 1

        for prev in ranking[:level]:
            prev = as_group(prev)
            for x in group:
                ix = idx[x]
                for p in prev:
                    ip = idx[p]
                    m[ix, ip] = 0
                    m[ip, ix] = 1

    return m


def find_contradictions(A, B, items):
    n = len(items)
    res = []
    for i in range(n):
        for j in range(i + 1, n):
            a_ij, a_ji = A[i, j], A[j, i]
            b_ij, b_ji = B[i, j], B[j, i]

            if a_ij == 1 and a_ji == 0 and b_ij == 0 and b_ji == 1:
                res.append([items[i], items[j]])
            elif a_ij == 0 and a_ji == 1 and b_ij == 1 and b_ji == 0:
                res.append([items[j], items[i]])
    return res


def build_final_ranking(items, contradictions):
    conflicts = {}
    for a, b in contradictions:
        conflicts.setdefault(a, []).append(b)

    result = []
    used = set()

    for x in items:
        if x in used:
            continue

        if x in conflicts:
            group = [x]
            used.add(x)
            for y in conflicts[x]:
                if y not in used:
                    group.append(y)
                    used.add(y)
            result.append(group)
        else:
            result.append(x)
            used.add(x)

    return result


def main(json_a: str, json_b: str) -> str:
    rank_a = json.loads(json_a)
    rank_b = json.loads(json_b)

    items = sorted(set(flatten(rank_a)) | set(flatten(rank_b)))

    A = build_matrix(rank_a, items)
    B = build_matrix(rank_b, items)

    contradictions = find_contradictions(A, B, items)
    final_rank = build_final_ranking(items, contradictions)

    return json.dumps(final_rank, ensure_ascii=False)


if __name__ == "__main__":
    a = json.dumps([1, [2, 3], 4, [5, 6, 7], 8, 9, 10])
    b = json.dumps([[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]])
    print(main(a, b))
