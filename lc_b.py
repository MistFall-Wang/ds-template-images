#!/usr/bin/env python3
"""Diagrams for 高精度 / 前缀和 / 差分 / 位运算 in 常用代码模板1 (files lcb-*.svg / lcb-*.png).

Run from this directory:  python3 lc_b.py
"""
from make_diagrams import *  # noqa: F401,F403
from make_diagrams_algo import row, lines, grid, panel_grid, bits_row, inf, blk  # also registers the 'pur' style


def label(s, y, t, mono=False):
    s.text(LX, y + 17, t, 14, INK, 'start', bold=True, mono=mono)


def signed(v):
    return ('+' if v > 0 else '') + inf(v) if v else '0'


# ---------- 高精度 ----------

def mul_pos():
    s = S()
    num1, num2, X, cw = '123', '45', 330, 66
    s.text(LX, 20, 'num1 = "123"，num2 = "45"：num1[i] × num2[j] 落在 result 的第 i + j + 1 位', 14.5, INK, 'start',
           bold=True)
    s.text(LX, 52, 'result 的下标', 13, SUB, 'start')
    for k in range(5):
        s.text(X + k * cw + (cw - 3) / 2, 52, k, 13, SUB, mono=True)
    y, result = 68, [0] * 5
    for i, digit1 in enumerate(num1):
        for j, digit2 in enumerate(num2):
            p = int(digit1) * int(digit2)
            result[i + j + 1] += p
            s.text(LX, y + 15, f'num1[{i}] × num2[{j}] = {digit1} × {digit2} = {p}', 13.5, INK, 'start', mono=True)
            s.node(X + (i + j + 1) * cw, y, f'+{p}', 'new', w=cw - 3, h=30, size=14)
            y += 36
    s.seg(LX, y + 2, X + 5 * cw, y + 2, '#CBD5E1', sw=1.5)
    s.text(LX, y + 28, '全部加完（先不管进位）', 14, INK, 'start', bold=True)
    row(s, X, y + 12, result, 'n', cw=cw, ch=32)
    for k in reversed(range(1, len(result))):
        result[k - 1] += result[k] // 10
        result[k] %= 10
    s.text(LX, y + 72, '从低位到高位统一进位', 14, INK, 'start', bold=True)
    row(s, X, y + 56, result, 'hit', cw=cw, ch=32)
    out = ''.join(map(str, result)).lstrip('0')
    assert out == str(123 * 45)
    s.text(X + 5 * cw + 20, y + 72, f'去掉开头的 0  →  "{out}"', 14, COL['grn'], 'start', bold=True)
    s.save('lcb-mul-pos')


# ---------- 一维前缀和 ----------

def prefix_1d():
    nums, left, right = [3, 1, 4, 1, 5], 1, 3
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)
    s = S()
    cw, X, y = 64, 130, 36
    label(s, y, 'nums', True)
    row(s, X + cw / 2, y, nums, ['new' if left <= i <= right else 'n' for i in range(len(nums))], cw=cw, idx='top')
    y2 = y + 84
    label(s, y2, 'prefix', True)
    cs = row(s, X, y2, prefix, ['chg' if i == left else 'hit' if i == right + 1 else 'off' for i in range(len(prefix))],
             cw=cw, idx='bot')
    for c in cs:
        s.seg(c, y + 38, c, y2 - 4, '#94A3B8', dash=1, sw=1.2)
    a, b = prefix[right + 1], prefix[left]
    lines(s, X + 6 * cw + 34, y - 4,
          [('prefix[i] = 虚线左边所有数的和（前 i 个数）', INK),
           f'prefix[{right + 1}] = ' + ' + '.join(map(str, nums[:right + 1])) + f' = {a}（绿）',
           f'prefix[{left}] = ' + ' + '.join(map(str, nums[:left])) + '（红）',
           (f'nums[{left}..{right}] 的和 = prefix[{right + 1}] − prefix[{left}] = {a} − {b} = {a - b}（橙）', 'org'),
           ('一般地：nums[left..right] 的和 = prefix[right + 1] − prefix[left]', INK)], gap=27)
    s.save('lcb-prefix-1d')


def prefix_hash_idea():
    """prefix[j] - prefix[i] = k  <=>  prefix[i] = prefix[j] - k, on nums = [1, 2, 3, -3, 3], k = 3, j = 5."""
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
    label(s, y2, 'prefix', True)
    cs = row(s, X, y2, [inf(v) for v in pre], ['chg' if i in hits else 'hit' if i == j else 'off' for i in range(len(pre))],
             cw=cw, idx='bot')
    for c in cs:
        s.seg(c, y + 38, c, y2 - 4, '#94A3B8', dash=1, sw=1.2)
    for n, i in enumerate(hits):                      # one brace per matching i: nums[i..j-1]
        by = y - 30 - 26 * n
        seg = nums[i:j]
        brace(s, cs[i] + 4, cs[j] - 4, by, f'nums[{i}..{j - 1}] 的和 = {pre[j]} − {pre[i]} = {sum(seg)}', 'org')
    lines(s, X + len(pre) * cw + 34, y - 44,
          [(f'k = {k}，现在走到 prefix[{j}] = {pre[j]}（绿）', INK),
           f'以这里结尾、和为 {k} 的一段，开头处的前缀和必须是',
           (f'prefix[{j}] − k = {pre[j]} − {k} = {pre[j] - k}', 'red'),
           f'前面等于 {pre[j] - k} 的前缀和有 {len(hits)} 个（红）：' + '、'.join(f'prefix[{i}]' for i in hits),
           (f'所以以这里结尾的有 {len(hits)} 段（橙）', 'org'),
           ('字典记的就是「每个前缀和出现过几次」', INK)], gap=27)
    s.save('lcb-prefix-hash-idea')


def prefix_560():
    nums, k = [1, 2, 3, -3, 3], 3
    seen, prefix_sum, result, rows = [0], 0, 0, []
    for x in nums:
        prefix_sum += x
        need = prefix_sum - k
        add = seen.count(need)
        result += add
        rows.append([[(inf(x), 'n')], [(inf(prefix_sum), 'new')], f'{inf(prefix_sum)} − {k} = {inf(need)}',
                     [(inf(v), 'hit' if v == need else 'off') for v in seen],
                     ('t', f'{add} 个', 'grn' if add else 'gry'), ('t', str(result), 'red')])
        seen.append(prefix_sum)
    assert result == 5
    table('lcb-prefix-560',
          ['读到 x', 'prefix_sum', '要找 prefix_sum − k', '前面出现过的前缀和（绿 = 要找的）', '找到', 'result'],
          [80, 110, 170, 300, 80, 60], rows,
          foot=f'nums = [1, 2, 3, −3, 3]，k = 3：一共 {result} 段。第一行前面只有一个 0，就是 count[0] = 1',
          leg=[('n', '当前的数'), ('new', '当前的前缀和'), ('hit', '等于 prefix_sum − k 的前缀和')])


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
    brace(s, cs[0] - h + 3, cs[p - 1] + h - 3, y + 46, f'左边的和 left_sum = {sum(nums[:p])}', 'org', up=False)
    brace(s, cs[p + 1] - h + 3, cs[-1] + h - 3, y + 46, f'右边的和 = {sum(nums[p + 1:])}', 'pur', up=False)
    s.text(cs[p], y + 59, '中心', 13, COL['red'], bold=True)
    total = sum(nums)
    lines(s, X + len(nums) * cw + 34, y - 4,
          [(f'总和 total = {total}', INK),
           ('右边的和 = total − left_sum − 自己', INK),
           (f'下标 {p}：{total} − {sum(nums[:p])} − {nums[p]} = {total - sum(nums[:p]) - nums[p]}，和 left_sum 相等', 'red'),
           '右边的和不用另开数组，用总和减出来'], gap=27)
    s.save('lcb-prefix-724')


# ---------- 二维前缀和 ----------

def prefix2d_build():
    s = S()
    x, y = 110, 52
    blk(s, x, y, 220, 120, 'A', 'n')
    blk(s, x + 220, y, 72, 120, 'B', 'new')
    blk(s, x, y + 120, 220, 48, 'C', 'hit')
    blk(s, x + 220, y + 120, 72, 48, 'x', 'chg')
    s.text(x + 110, y - 18, '前 j 列', 13.5, SUB)
    s.text(x + 255, y - 18, '第 j+1 列', 13.5, SUB)
    s.text(LX, y + 60, '前 i 行', 13.5, SUB, 'start')
    s.text(LX, y + 143, '第 i+1 行', 13.5, SUB, 'start')
    for k, t in enumerate(['prefix[i][j+1] = A + B', 'prefix[i+1][j] = A + C', 'prefix[i][j] = A', 'matrix[i][j] = x']):
        s.text(450, y + 4 + k * 26, t, 14, INK, 'start', mono=True)
    lines(s, 450, y + 122, [('prefix[i+1][j+1] = (A + B) + (A + C) − A + x', 'red'), 'A 被加了两次，所以减掉一次'],
          size=14, gap=26)
    s.save('lcb-prefix2d-build')


def prefix2d_query():
    s = S()
    x, y = 110, 52
    blk(s, x, y, 120, 70, 'A', 'n')
    blk(s, x + 120, y, 172, 70, 'B', 'new')
    blk(s, x, y + 70, 120, 110, 'C', 'pur')
    blk(s, x + 120, y + 70, 172, 110, 'D（要求的）', 'hit', 16)
    s.text(x + 146, y - 18, 'col1', 14, INK, bold=True, mono=True)
    s.text(x + 266, y - 18, 'col2', 14, INK, bold=True, mono=True)
    s.text(x - 10, y + 86, 'row1', 14, INK, 'end', bold=True, mono=True)
    s.text(x - 10, y + 164, 'row2', 14, INK, 'end', bold=True, mono=True)
    for k, t in enumerate(['prefix[row2+1][col2+1] = A + B + C + D（整块）', 'prefix[row1][col2+1] = A + B（D 上面的）',
                           'prefix[row2+1][col1] = A + C（D 左边的）', 'prefix[row1][col1] = A']):
        s.text(450, y + 4 + k * 26, t, 14, INK, 'start', mono=True)
    lines(s, 450, y + 126, [('D = 整块 − 上面的 − 左边的 + A', 'grn'), 'A 被减了两次，所以加回来一次'], size=14, gap=26)
    s.save('lcb-prefix2d-query')


def prefix2d_304():
    M = [[3, 0, 1, 4], [5, 6, 3, 2], [1, 2, 0, 1]]
    n, m = len(M), len(M[0])
    P = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            P[i + 1][j + 1] = P[i][j + 1] + P[i + 1][j] - P[i][j] + M[i][j]
    row1, col1, row2, col2 = 1, 1, 2, 2
    a, b, c, d = P[row2 + 1][col2 + 1], P[row1][col2 + 1], P[row2 + 1][col1], P[row1][col1]
    ans = a - b - c + d
    assert ans == sum(M[i][j] for i in range(row1, row2 + 1) for j in range(col1, col2 + 1)) == 11
    s = S()
    cw, X, Y = 46, 44, 62
    s.text(LX, 20, 'matrix（绿 = 要求和的子矩阵）', 14.5, INK, 'start', bold=True)
    for j in range(m):
        s.text(X + j * cw + (cw - 3) / 2, Y - 12, j, 12, SUB, mono=True)
    for i in range(n):
        s.text(X - 14, Y + i * cw + (cw - 3) / 2, i, 12, SUB, mono=True)
    grid(s, X, Y, M, lambda i, j: 'hit' if row1 <= i <= row2 and col1 <= j <= col2 else 'n', cw=cw, size=15)
    X2 = X + m * cw + 90
    s.text(X2 - 26, 20, 'prefix（多一行一列，第 0 行、第 0 列全是 0）', 14.5, INK, 'start', bold=True)
    for j in range(m + 1):
        s.text(X2 + j * cw + (cw - 3) / 2, Y - 12, j, 12, SUB, mono=True)
    for i in range(n + 1):
        s.text(X2 - 14, Y + i * cw + (cw - 3) / 2, i, 12, SUB, mono=True)
    key = {(row2 + 1, col2 + 1): 'hit', (row1, col2 + 1): 'new', (row2 + 1, col1): 'pur', (row1, col1): 'chg'}
    grid(s, X2, Y, P, lambda i, j: key.get((i, j), 'off'), cw=cw, size=15)
    lines(s, X2 + (m + 1) * cw + 30, Y + 4,
          [(f'查询 ({row1}, {col1}) 到 ({row2}, {col2})', INK),
           (f'prefix[{row2 + 1}][{col2 + 1}] = {a}  整块', 'grn'),
           (f'prefix[{row1}][{col2 + 1}] = {b}  上面的', 'org'),
           (f'prefix[{row2 + 1}][{col1}] = {c}  左边的', 'pur'),
           (f'prefix[{row1}][{col1}] = {d}  左上角，被减了两次', 'red'),
           (f'{a} − {b} − {c} + {d} = {ans}', INK)], gap=27)
    s.save('lcb-prefix2d-304')


# ---------- 一维差分 ----------

def diff_1d():
    s = S()
    X, cw, y = 190, 78, 36
    label(s, y, 'diff', True)
    row(s, X, y, ['0', '0', '+value', '0', '0', '−value'], ['off', 'off', 'new', 'off', 'off', 'chg'], cw=cw, idx='top',
        size=14)
    y2 = y + 60
    label(s, y2, 'diff 的前缀和')
    cs = row(s, X, y2, ['0', '0', 'value', 'value', 'value', '0'], ['off', 'off', 'hit', 'hit', 'hit', 'off'], cw=cw,
             size=14)
    h = (cw - 3) / 2
    brace(s, cs[2] - h + 3, cs[4] + h - 3, y2 + 44, '只有下标 2 到 4 加了 value', 'grn', up=False)
    lines(s, X + 6 * cw + 30, y + 6,
          [('把 [left, right] = [2, 4] 这一段加 value', INK),
           ('diff[left] += value：从 left 开始，后面全部多 value', 'org'),
           ('diff[right + 1] −= value：从 right + 1 开始，把它抵消掉', 'red')], gap=27)
    s.save('lcb-diff-1d')


def diff_trace():
    s = S()
    X, cw, y = 300, 54, 34
    nums, updates = [1, 2, 2, 1, 2], [(0, 2, 1), (2, 4, 1)]
    n = len(nums)
    label(s, y, '原数组 nums')
    row(s, X, y, nums, 'n', cw=cw, idx='top')
    s.text(X + n * cw + (cw - 3) / 2, y - 11, n, 12, SUB, mono=True)
    diff = [0] * (n + 1)
    for left, right, value in updates:
        y += 50
        diff[left] += value
        diff[right + 1] -= value
        label(s, y, f'操作 ({left}, {right}, {value}) 之后的 diff')
        row(s, X, y, [inf(v) for v in diff],
            ['new' if k == left else 'chg' if k == right + 1 else 'off' for k in range(n + 1)], cw=cw)
        s.text(X + (n + 1) * cw + 20, y + 17, f'diff[{left}] += {value}，diff[{right + 1}] −= {value}', 13.5, SUB, 'start',
               mono=True)
    y += 50
    added, current = [], 0
    for i in range(n):
        current += diff[i]
        added.append(current)
    label(s, y, 'current：diff 的前缀和，每个位置加了多少')
    row(s, X, y, added, 'pur', cw=cw)
    y += 50
    result = [x + v for x, v in zip(nums, added)]
    assert result == [2, 3, 4, 2, 3]
    label(s, y, 'result：加上原数组')
    row(s, X, y, result, 'hit', cw=cw)
    s.save('lcb-diff-trace')


def diff_1109():
    bookings, n = [[1, 2, 10], [2, 3, 20], [2, 5, 25]], 5
    s = S()
    X, cw, y = 290, 62, 34
    diff = [0] * (n + 1)
    first_row = True
    for first, last, seats in bookings:
        diff[first - 1] += seats
        diff[last] -= seats
        label(s, y, f'预订 [{first}, {last}, {seats}] 之后的 diff')
        cs = row(s, X, y, [inf(v) for v in diff],
                 ['new' if k == first - 1 else 'chg' if k == last else 'off' for k in range(n + 1)],
                 cw=cw, idx='top' if first_row else None)
        first_row = False
        s.text(X + (n + 1) * cw + 20, y + 17, f'diff[{first - 1}] += {seats}，diff[{last}] −= {seats}', 13.5, SUB, 'start',
               mono=True)
        y += 50
    result, current = [], 0
    for i in range(n):
        current += diff[i]
        result.append(current)
    assert result == [10, 55, 45, 25, 25]
    label(s, y, 'diff 的前缀和：每个航班的座位数')
    row(s, X, y, result, 'hit', cw=cw)
    for i, c in enumerate(cs[:n]):
        s.text(c, y + 46, f'航班 {i + 1}', 12.5, SUB)
    s.text(X + (n + 1) * cw + 20, y + 17, '下标 i 对应航班 i + 1；下标 5 是多开的一位', 13.5, SUB, 'start')
    s.save('lcb-diff-1109')


def diff_1094():
    trips, capacity, N = [[2, 1, 5], [3, 3, 7]], 4, 9
    s = S()
    X, cw, y = 280, 58, 34
    diff = [0] * N
    first_row = True
    for k, (num_passengers, start, end) in enumerate(trips):
        diff[start] += num_passengers
        diff[end] -= num_passengers
        label(s, y, f'第 {k + 1} 批：{num_passengers} 人，{start} 上 {end} 下')
        row(s, X, y, [num_passengers if start <= x < end else '' for x in range(N)],
            ['n' if start <= x < end else 'off' for x in range(N)], cw=cw, idx='top' if first_row else None)
        first_row = False
        y += 46
    y += 8
    label(s, y, '差分数组 diff')
    row(s, X, y, [signed(v) for v in diff], ['new' if v > 0 else 'chg' if v < 0 else 'off' for v in diff], cw=cw)
    y += 50
    load, current = [], 0
    for change in diff:
        current += change
        load.append(current)
    assert max(load) == 5
    label(s, y, 'current：diff 的前缀和，车上的人数')
    cs = row(s, X, y, load, ['chg' if v > capacity else 'hit' if v else 'off' for v in load], cw=cw)
    over = [x for x, v in enumerate(load) if v > capacity]
    h = (cw - 3) / 2
    brace(s, cs[over[0]] - h + 3, cs[over[-1]] + h - 3, y + 44, f'{max(load)} 人 > capacity = {capacity}，装不下', 'red',
          up=False)
    s.text(X + N * cw + 20, 34 + 17, '最上面一排数字是位置', 13.5, SUB, 'start')
    s.text(X + N * cw + 20, y - 50 + 17, '上车 +人数，下车 −人数', 13.5, SUB, 'start')
    s.text(X + N * cw + 20, y + 17, f'位置 {trips[0][2]} 的人已经下车，不算在内', 13.5, SUB, 'start')
    s.save('lcb-diff-1094')


# ---------- 二维差分 ----------

def diff_2d():
    n, row1, col1, row2, col2, cw = 6, 1, 1, 3, 3, 30
    pts = [(row1, col1, 1), (row2 + 1, col1, -1), (row1, col2 + 1, -1), (row2 + 1, col2 + 1, 1)]
    titles = ['① diff[row1][col1] += value', '② diff[row2+1][col1] −= value', '③ diff[row1][col2+1] −= value',
              '④ diff[row2+1][col2+1] += value']
    caps = [['右下方全部 +v', '范围太大了'], ['子矩阵下面多加的', '抵消掉了'], ['右边多加的也抵消了', '但右下角被减了两次：−v'],
            ['右下角补回一次', '只剩目标子矩阵 +v']]

    def draw(s, ox, oy, k):
        d = [[0] * n for _ in range(n)]
        for a, b, c in pts[:k + 1]:
            d[a][b] += c
        gx, gy = ox + 50, oy + 22
        for i in range(n):
            for j in range(n):
                v = sum(d[a][b] for a in range(i + 1) for b in range(j + 1))
                s.node(gx + j * cw, gy + i * cw, {1: 'v', -1: '−v', 0: '0'}[v],
                       'new' if v == 1 else 'chg' if v == -1 else 'off', w=cw - 3, h=cw - 3, size=12)
        for q, (a, b, c) in enumerate(pts[:k + 1]):
            s.rect(gx + b * cw - 2, gy + a * cw - 2, cw + 1, cw + 1, 'none', COL['pur'], rx=8, sw=3.2 if q == k else 1.6)
        for j, t in ((col1, 'col1'), (col2, 'col2')):
            s.text(gx + j * cw + 13, gy - 11, t, 12, SUB, bold=True, mono=True)
        for i, t in ((row1, 'row1'), (row2, 'row2')):
            s.text(gx - 8, gy + i * cw + 13, t, 12, SUB, 'end', bold=True, mono=True)
        lines(s, ox, gy + n * cw + 18, caps[k], size=13, gap=20)

    panel_grid('lcb-diff-2d', 4, 292, 300, draw, titles=titles,
               foot='紫框 = 在 diff 上改的那个点（粗框是这一步改的）；格子里的 v 就是 value：求完二维前缀和后，这个位置一共多了多少')


def diff2d_2536():
    n, queries = 3, [[1, 1, 2, 2], [0, 0, 1, 1]]
    snaps, corners = [], []
    diff = [[0] * (n + 1) for _ in range(n + 1)]
    for row1, col1, row2, col2 in queries:
        diff[row1][col1] += 1
        diff[row2 + 1][col1] -= 1
        diff[row1][col2 + 1] -= 1
        diff[row2 + 1][col2 + 1] += 1
        snaps.append([r[:] for r in diff])
        corners.append({(row1, col1), (row2 + 1, col1), (row1, col2 + 1), (row2 + 1, col2 + 1)})
    for i in range(n):
        for j in range(1, n):
            diff[i][j] += diff[i][j - 1]
    for i in range(1, n):
        for j in range(n):
            diff[i][j] += diff[i - 1][j]
    res = [r[:n] for r in diff[:n]]
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
            grid(s, gx, gy, [[signed(v) for v in r] for r in g],
                 lambda i, j: ('new' if g[i][j] > 0 else 'chg') if (i, j) in corners[k] else
                 ('pur' if g[i][j] else 'off'), cw=cw, size=15)
            row1, col1, row2, col2 = queries[k]
            lines(s, ox, gy + size * cw + 14, [f'diff[{row1}][{col1}] += 1，diff[{row2 + 1}][{col1}] −= 1',
                                              f'diff[{row1}][{col2 + 1}] −= 1，diff[{row2 + 1}][{col2 + 1}] += 1'],
                  size=13, color=SUB)
        else:
            grid(s, gx, gy, res, lambda i, j: 'hit' if res[i][j] == 2 else 'n' if res[i][j] else 'off', cw=cw, size=15)
            lines(s, ox, gy + (n + 1) * cw + 14, ['每个位置被几个查询盖住', '中间的 2：两个查询都盖到了它'], size=13,
                  color=SUB)

    panel_grid('lcb-diff2d-2536', 3, 310, 330, draw,
               titles=[f'① 查询 {queries[0]} 之后的 diff', f'② 查询 {queries[1]} 之后的 diff',
                       '③ 对 diff 求二维前缀和，取前 3 行 3 列'],
               leg=[('new', '这一步 +1 的角'), ('chg', '这一步 −1 的角'), ('pur', '上一步留下的')])


# ---------- 位运算 ----------

def bit_191():
    n, W = 11, 4
    s = S()
    X = 150
    s.text(LX, 18, 'n = 11：每做一次 n &= n − 1，最右边的那个 1 就没了', 14.5, INK, 'start', bold=True)
    y, count = 36, 0
    while True:
        bits = format(n, f'0{W}b')
        low = (n & -n).bit_length() - 1 if n else -1
        sts = ['new' if W - 1 - p == low else 'n' if ch == '1' else 'off' for p, ch in enumerate(bits)]
        note_ = (f'= {n}，还不是 0，橙色是这一次要去掉的 1' if n else f'= 0，停。一共去了 {count} 次，所以有 {count} 个 1')
        bits_row(s, X, y, 'n' if count == 0 else f'第 {count} 次之后', bits, sts, note_, COL['grn'] if n == 0 else SUB)
        if n == 0:
            break
        n &= n - 1
        count += 1
        y += 42
    assert count == 3
    s.save('lcb-bit-191')


def bit_136():
    nums, W = [4, 1, 2, 1, 2], 3
    s = S()
    X = 150
    s.text(LX, 18, 'nums = [4, 1, 2, 1, 2]：按位竖着看，每一列有偶数个 1 就抵消成 0', 14.5, INK, 'start', bold=True)
    col = {1: 'new', 2: 'pur', 4: 'hit'}
    y, result = 36, 0
    for x in nums:
        result ^= x
        bits = format(x, f'0{W}b')
        bits_row(s, X, y, str(x), bits, [col[x] if ch == '1' else 'off' for ch in bits],
                 f'异或到这里 result = {format(result, f"0{W}b")}（{result}）')
        y += 40
    s.seg(LX, y + 2, X + W * 40 + 300, y + 2, '#CBD5E1', sw=1.5)
    y += 12
    bits = format(result, f'0{W}b')
    bits_row(s, X, y, '全部异或', bits, ['hit' if ch == '1' else 'off' for ch in bits],
             f'= {result}：两个 1（橙）抵消，两个 2（紫）抵消，只剩 4', COL['grn'])
    assert result == 4
    s.save('lcb-bit-136')


if __name__ == '__main__':
    for f in (mul_pos, prefix_1d, prefix_hash_idea, prefix_560, prefix_238, prefix_724, prefix2d_build, prefix2d_query,
              prefix2d_304, diff_1d, diff_trace, diff_1109, diff_1094, diff_2d, diff2d_2536, bit_191, bit_136):
        f()
    print('ok')
