#!/usr/bin/env python3
"""Diagrams for the LeetCode parts of 前缀和 / 差分 / 位运算 in 常用代码模板1 (files lcb-*.svg / lcb-*.png).

Run from this directory:  python3 lc_b.py
"""
from make_diagrams import *  # noqa: F401,F403
from make_diagrams_algo import row, lines, grid, panel_grid, bits_row, inf  # also registers the 'pur' style


def label(s, y, t, mono=False):
    s.text(LX, y + 17, t, 14, INK, 'start', bold=True, mono=mono)


# ---------- 一维前缀和 ----------

def prefix_hash_idea():
    """s[j] - s[i] = k  <=>  s[i] = s[j] - k, on nums = [1, 2, 3, -3, 3], k = 3, j = 5."""
    nums, k, j = [1, 2, 3, -3, 3], 3, 5
    pre = [0]
    for x in nums:
        pre.append(pre[-1] + x)
    hits = [i for i in range(j) if pre[i] == pre[j] - k]
    s = S()
    cw, X, y = 64, 130, 96
    label(s, y, 'nums', True)
    row(s, X + cw / 2, y, [inf(v) for v in nums], 'n', cw=cw, idx='top')
    y2 = y + 84
    label(s, y2, 's', True)
    cs = row(s, X, y2, [inf(v) for v in pre], ['chg' if i in hits else 'hit' if i == j else 'off' for i in range(len(pre))],
             cw=cw, idx='bot')
    for c in cs:
        s.seg(c, y + 38, c, y2 - 4, '#94A3B8', dash=1, sw=1.2)
    for n, i in enumerate(hits):                      # one brace per matching i: nums[i..j-1]
        by = y - 30 - 26 * n
        seg = nums[i:j]
        brace(s, cs[i] + 4, cs[j] - 4, by, f'nums[{i}..{j - 1}] 的和 = {pre[j]} − {pre[i]} = {sum(seg)}', 'org')
    lines(s, X + len(pre) * cw + 34, y - 44,
          [(f'k = {k}，现在走到 s[{j}] = {pre[j]}（绿）', INK),
           f'以这里结尾、和为 {k} 的一段，开头处的前缀和必须是',
           (f's[{j}] − k = {pre[j]} − {k} = {pre[j] - k}', 'red'),
           f'前面等于 {pre[j] - k} 的前缀和有 {len(hits)} 个（红）：' + '、'.join(f's[{i}]' for i in hits),
           (f'所以以这里结尾的有 {len(hits)} 段（橙）', 'org'),
           ('字典记的就是「每个前缀和出现过几次」', INK)], gap=27)
    s.save('lcb-prefix-hash-idea')


def prefix_560():
    nums, k = [1, 2, 3, -3, 3], 3
    seen, cur, res, rows = [0], 0, 0, []
    for x in nums:
        cur += x
        need = cur - k
        add = seen.count(need)
        res += add
        rows.append([[(inf(x), 'n')], [(inf(cur), 'new')], f'{inf(cur)} − {k} = {inf(need)}',
                     [(inf(v), 'hit' if v == need else 'off') for v in seen],
                     ('t', f'{add} 个', 'grn' if add else 'gry'), ('t', str(res), 'red')])
        seen.append(cur)
    assert res == 5
    table('lcb-prefix-560', ['读到 x', '前缀和 s', '要找 s − k', '前面出现过的前缀和（绿 = 等于 s − k）', '找到', 'res'],
          [80, 100, 140, 300, 80, 50], rows,
          foot=f'nums = [1, 2, 3, −3, 3]，k = 3：一共 {res} 段。第一行前面只有一个 0，就是 cnt[0] = 1',
          leg=[('n', '当前的数'), ('new', '当前前缀和'), ('hit', '等于 s − k 的前缀和')])


def prefix_238():
    nums = [1, 2, 3, 4]
    n = len(nums)
    left, right = [1] * n, [1] * n
    for i in range(1, n):
        left[i] = left[i - 1] * nums[i - 1]
    for i in range(n - 2, -1, -1):
        right[i] = right[i + 1] * nums[i + 1]
    res = [a * b for a, b in zip(left, right)]
    assert res == [24, 12, 8, 6]
    s = S()
    X, cw, y = 250, 96, 34
    label(s, y, 'nums', True)
    row(s, X, y, nums, 'n', cw=cw, idx='top')
    y += 56
    label(s, y, '左边所有数的乘积')
    row(s, X, y, left, 'new', cw=cw)
    s.text(X + n * cw + 18, y + 17, '从左往右扫：' + '，'.join(
        ['1'] + ['×'.join(map(str, nums[:i])) for i in range(1, n)]), 13.5, SUB, 'start')
    y += 50
    label(s, y, '右边所有数的乘积')
    row(s, X, y, right, 'pur', cw=cw)
    s.text(X + n * cw + 18, y + 17, '从右往左扫：' + '，'.join(
        ['×'.join(map(str, nums[i + 1:])) for i in range(n - 1)] + ['1']), 13.5, SUB, 'start')
    y += 50
    label(s, y, '结果 = 左边 × 右边')
    row(s, X, y, [f'{a}×{b}={c}' for a, b, c in zip(left, right, res)], 'hit', cw=cw, size=13)
    s.text(X + n * cw + 18, y + 17, '最左、最右没有数可乘，记成 1', 13.5, SUB, 'start')
    s.save('lcb-prefix-238')


def prefix_724():
    nums = [1, 7, 3, 6, 5, 6]
    p = next(i for i in range(len(nums)) if sum(nums[:i]) == sum(nums[i + 1:]))
    s = S()
    X, cw, y = 110, 64, 36
    label(s, y, 'nums', True)
    cs = row(s, X, y, nums, ['new' if i < p else 'chg' if i == p else 'pur' for i in range(len(nums))], cw=cw, idx='top')
    h = (cw - 3) / 2
    brace(s, cs[0] - h + 3, cs[p - 1] + h - 3, y + 46, f'左边的和 left = {sum(nums[:p])}', 'org', up=False)
    brace(s, cs[p + 1] - h + 3, cs[-1] + h - 3, y + 46, f'右边的和 = {sum(nums[p + 1:])}', 'pur', up=False)
    s.text(cs[p], y + 59, '中心', 13, COL['red'], bold=True)
    total = sum(nums)
    lines(s, X + len(nums) * cw + 34, y - 4,
          [(f'总和 total = {total}', INK),
           ('右边的和 = total − left − 自己', INK),
           (f'下标 {p}：{total} − {sum(nums[:p])} − {nums[p]} = {total - sum(nums[:p]) - nums[p]}，和 left 相等', 'red'),
           '右边的和不用另开数组，用总和减出来'], gap=27)
    s.save('lcb-prefix-724')


# ---------- 二维前缀和 ----------

def prefix2d_304():
    M = [[3, 0, 1, 4], [5, 6, 3, 2], [1, 2, 0, 1]]
    n, m = len(M), len(M[0])
    P = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            P[i + 1][j + 1] = P[i][j + 1] + P[i + 1][j] - P[i][j] + M[i][j]
    x1, y1, x2, y2 = 1, 1, 2, 2
    a, b, c, d = P[x2 + 1][y2 + 1], P[x1][y2 + 1], P[x2 + 1][y1], P[x1][y1]
    ans = a - b - c + d
    assert ans == sum(M[i][j] for i in range(x1, x2 + 1) for j in range(y1, y2 + 1)) == 11
    s = S()
    cw, X, Y = 46, 44, 62
    s.text(LX, 20, 'matrix（绿 = 要求和的子矩阵）', 14.5, INK, 'start', bold=True)
    for j in range(m):
        s.text(X + j * cw + (cw - 3) / 2, Y - 12, j, 12, SUB, mono=True)
    for i in range(n):
        s.text(X - 14, Y + i * cw + (cw - 3) / 2, i, 12, SUB, mono=True)
    grid(s, X, Y, M, lambda i, j: 'hit' if x1 <= i <= x2 and y1 <= j <= y2 else 'n', cw=cw, size=15)
    X2 = X + m * cw + 90
    s.text(X2 - 26, 20, 's（多一行一列，第 0 行、第 0 列全是 0）', 14.5, INK, 'start', bold=True)
    for j in range(m + 1):
        s.text(X2 + j * cw + (cw - 3) / 2, Y - 12, j, 12, SUB, mono=True)
    for i in range(n + 1):
        s.text(X2 - 14, Y + i * cw + (cw - 3) / 2, i, 12, SUB, mono=True)
    key = {(x2 + 1, y2 + 1): 'hit', (x1, y2 + 1): 'new', (x2 + 1, y1): 'pur', (x1, y1): 'chg'}
    grid(s, X2, Y, P, lambda i, j: key.get((i, j), 'off'), cw=cw, size=15)
    lines(s, X2 + (m + 1) * cw + 30, Y + 4,
          [(f'查询 ({x1}, {y1}) 到 ({x2}, {y2})', INK),
           (f's[{x2 + 1}][{y2 + 1}] = {a}  整块', 'grn'),
           (f's[{x1}][{y2 + 1}] = {b}  上面的', 'org'),
           (f's[{x2 + 1}][{y1}] = {c}  左边的', 'pur'),
           (f's[{x1}][{y1}] = {d}  左上角，被减了两次', 'red'),
           (f'{a} − {b} − {c} + {d} = {ans}', INK)], gap=27)
    s.save('lcb-prefix2d-304')


# ---------- 一维差分 ----------

def diff_1109():
    bookings, n = [[1, 2, 10], [2, 3, 20], [2, 5, 25]], 5
    s = S()
    X, cw, y = 270, 62, 34
    d = [0] * (n + 1)
    first = True
    for f, l, c in bookings:
        d[f - 1] += c
        d[l] -= c
        label(s, y, f'预订 [{f}, {l}, {c}] 之后的 d')
        cs = row(s, X, y, [inf(v) for v in d], ['new' if k == f - 1 else 'chg' if k == l else 'off' for k in range(n + 1)],
                 cw=cw, idx='top' if first else None)
        first = False
        s.text(X + (n + 1) * cw + 20, y + 17, f'd[{f - 1}] += {c}，d[{l}] −= {c}', 13.5, SUB, 'start', mono=True)
        y += 50
    res, cur = [], 0
    for v in d[:n]:
        cur += v
        res.append(cur)
    assert res == [10, 55, 45, 25, 25]
    label(s, y, 'd 的前缀和：每个航班的座位数')
    row(s, X, y, res, 'hit', cw=cw)
    for i, c in enumerate(cs[:n]):
        s.text(c, y + 46, f'航班 {i + 1}', 12.5, SUB)
    s.text(X + (n + 1) * cw + 20, y + 17, '下标 i 对应航班 i + 1；下标 5 是多开的一位', 13.5, SUB, 'start')
    s.save('lcb-diff-1109')


def diff_1094():
    trips, cap, N = [[2, 1, 5], [3, 3, 7]], 4, 9
    s = S()
    X, cw, y = 250, 58, 34
    d = [0] * N
    first = True
    for k, (num, st, en) in enumerate(trips):
        d[st] += num
        d[en] -= num
        label(s, y, f'第 {k + 1} 批：{num} 人，{st} 上 {en} 下')
        row(s, X, y, [num if st <= x < en else '' for x in range(N)],
            ['n' if st <= x < en else 'off' for x in range(N)], cw=cw, idx='top' if first else None)
        first = False
        y += 46
    y += 8
    label(s, y, '差分数组 d')
    row(s, X, y, [('+' if v > 0 else '') + inf(v) if v else '0' for v in d],
        ['new' if v > 0 else 'chg' if v < 0 else 'off' for v in d], cw=cw)
    y += 50
    load, cur = [], 0
    for v in d:
        cur += v
        load.append(cur)
    assert max(load) == 5
    label(s, y, 'd 的前缀和：车上的人数')
    cs = row(s, X, y, load, ['chg' if v > cap else 'hit' if v else 'off' for v in load], cw=cw)
    over = [x for x, v in enumerate(load) if v > cap]
    h = (cw - 3) / 2
    brace(s, cs[over[0]] - h + 3, cs[over[-1]] + h - 3, y + 44, f'{max(load)} 人 > 容量 {cap}，装不下', 'red', up=False)
    s.text(X + N * cw + 20, 34 + 17, '最上面一排数字是位置', 13.5, SUB, 'start')
    s.text(X + N * cw + 20, y - 50 + 17, '上车 +人数，下车 −人数', 13.5, SUB, 'start')
    s.text(X + N * cw + 20, y + 17, f'位置 {trips[0][2]} 的人已经下车，不算在内', 13.5, SUB, 'start')
    s.save('lcb-diff-1094')


# ---------- 二维差分 ----------

def diff2d_2536():
    n, queries = 3, [[1, 1, 2, 2], [0, 0, 1, 1]]
    snaps, corners = [], []
    d = [[0] * (n + 1) for _ in range(n + 1)]
    for r1, c1, r2, c2 in queries:
        d[r1][c1] += 1
        d[r2 + 1][c1] -= 1
        d[r1][c2 + 1] -= 1
        d[r2 + 1][c2 + 1] += 1
        snaps.append([r[:] for r in d])
        corners.append({(r1, c1), (r2 + 1, c1), (r1, c2 + 1), (r2 + 1, c2 + 1)})
    P = [r[:] for r in d]
    for i in range(n):
        for j in range(n):
            if i > 0:
                P[i][j] += P[i - 1][j]
            if j > 0:
                P[i][j] += P[i][j - 1]
            if i > 0 and j > 0:
                P[i][j] -= P[i - 1][j - 1]
    res = [r[:n] for r in P[:n]]
    assert res == [[1, 1, 0], [1, 2, 1], [0, 1, 1]]
    cw = 46

    def draw(s, ox, oy, k):
        gx, gy = ox + 30, oy + 26
        size = n if k == 2 else n + 1
        for j in range(size):
            s.text(gx + j * cw + (cw - 3) / 2, gy - 12, j, 12, SUB, mono=True)
        for i in range(size):
            s.text(gx - 14, gy + i * cw + (cw - 3) / 2, i, 12, SUB, mono=True)
        if k < 2:
            g = snaps[k]
            grid(s, gx, gy, [[('+' if v > 0 else '') + inf(v) if v else '0' for v in r] for r in g],
                 lambda i, j: ('new' if g[i][j] > 0 else 'chg') if (i, j) in corners[k] else
                 ('pur' if g[i][j] else 'off'), cw=cw, size=15)
            r1, c1, r2, c2 = queries[k]
            lines(s, ox, gy + size * cw + 14, [f'd[{r1}][{c1}] += 1，d[{r2 + 1}][{c1}] −= 1',
                                              f'd[{r1}][{c2 + 1}] −= 1，d[{r2 + 1}][{c2 + 1}] += 1'], size=13, color=SUB)
        else:
            grid(s, gx, gy, res, lambda i, j: 'hit' if res[i][j] == 2 else 'n' if res[i][j] else 'off', cw=cw, size=15)
            lines(s, ox, gy + (n + 1) * cw + 14, ['每个位置被几个查询盖住', '中间的 2：两个查询都盖到了它'], size=13,
                  color=SUB)

    panel_grid('lcb-diff2d-2536', 3, 270, 330, draw,
               titles=[f'① 查询 {queries[0]} 之后的 d', f'② 查询 {queries[1]} 之后的 d', '③ 对 d 求二维前缀和，取前 3 行 3 列'],
               leg=[('new', '这一步 +1 的角'), ('chg', '这一步 −1 的角'), ('pur', '上一步留下的')])


# ---------- 位运算 ----------

def bit_191():
    n, W = 11, 4
    s = S()
    X = 150
    s.text(LX, 18, 'n = 11：每做一次 n &= n − 1，最右边的那个 1 就没了', 14.5, INK, 'start', bold=True)
    y, cnt = 36, 0
    while True:
        bits = format(n, f'0{W}b')
        low = (n & -n).bit_length() - 1 if n else -1
        sts = ['new' if W - 1 - p == low else 'n' if ch == '1' else 'off' for p, ch in enumerate(bits)]
        note_ = (f'= {n}，还不是 0，橙色是这一次要去掉的 1' if n else f'= 0，停。一共去了 {cnt} 次，所以有 {cnt} 个 1')
        bits_row(s, X, y, 'n' if cnt == 0 else f'第 {cnt} 次之后', bits, sts, note_, COL['grn'] if n == 0 else SUB)
        if n == 0:
            break
        n &= n - 1
        cnt += 1
        y += 42
    assert cnt == 3
    s.save('lcb-bit-191')


def bit_136():
    nums, W = [4, 1, 2, 1, 2], 3
    s = S()
    X = 150
    s.text(LX, 18, 'nums = [4, 1, 2, 1, 2]：按位竖着看，每一列有偶数个 1 就抵消成 0', 14.5, INK, 'start', bold=True)
    col = {1: 'new', 2: 'pur', 4: 'hit'}
    y, res = 36, 0
    for x in nums:
        res ^= x
        bits = format(x, f'0{W}b')
        bits_row(s, X, y, str(x), bits, [col[x] if ch == '1' else 'off' for ch in bits],
                 f'异或到这里 res = {format(res, f"0{W}b")}（{res}）')
        y += 40
    s.seg(LX, y + 2, X + W * 40 + 300, y + 2, '#CBD5E1', sw=1.5)
    y += 12
    bits = format(res, f'0{W}b')
    bits_row(s, X, y, '全部异或', bits, ['hit' if ch == '1' else 'off' for ch in bits],
             f'= {res}：两个 1（橙）抵消，两个 2（紫）抵消，只剩 4', COL['grn'])
    assert res == 4
    s.save('lcb-bit-136')


if __name__ == '__main__':
    for f in (prefix_hash_idea, prefix_560, prefix_238, prefix_724, prefix2d_304, diff_1109, diff_1094, diff2d_2536,
              bit_191, bit_136):
        f()
    print('ok')
