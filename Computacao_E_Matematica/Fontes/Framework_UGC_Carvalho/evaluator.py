def compute_value(A, pi, labels):
    total = 0
    satisfied = 0

    for (i, j), perm in pi.items():
        total += 1
        if perm[labels[i].item()] == labels[j].item():
            satisfied += 1

    return satisfied / total if total > 0 else 0