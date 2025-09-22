#!/usr/bin/env python3

def unset(xs):
    """Algorithm to find symbols from runs with maximum length"""
    if not xs:
        return []
    
    # Build runs
    runs = []
    cur = xs[0]
    cnt = 1
    for x in xs[1:]:
        if x == cur:
            cnt += 1
        else:
            runs.append((cur, cnt))
            cur = x
            cnt = 1
    runs.append((cur, cnt))

    max_len = max(length for _, length in runs)
    if max_len == 1:
        return []
    
    # Collect unique symbols from runs with length == max_len, then sort
    chars = []
    for sym, length in runs:
        if length == max_len and sym not in chars:
            chars.append(sym)
    return sorted(chars)

if __name__ == "__main__":
    print("Testing algorithm:")
    test_cases = [
        ['a'],
        ['a','a'],
        ['a','b'],
        ['a','a','b','b'],
        ['a','b','b','a'],
        ['a','a','z','z','z','a','a'],
        ['r','r','r','a','a','g','g','g','r','r','r']
    ]
    
    for case in test_cases:
        result = unset(case)
        print(f'{case} -> {result}')
