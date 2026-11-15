#!/usr/bin/env python3
"""Diagrams for 双序列 DP / 背包 in 常用代码模板5——动态规划 (files lcs-*.svg / lcs-*.png).

Run from this directory:  python3 lc_s.py
"""
from make_diagrams import *  # noqa: F401,F403
from make_diagrams_algo import row, grid, inf  # also registers the 'pur' style
from make_diagrams_algo import lines as plain_lines


def lines(s, x, y, ts, size=13.5, gap=22, color=INK):
    """Like make_diagrams_algo.lines, but a leading full-width space indents the line (SVG drops leading blanks)."""
    for k, item in enumerate(ts):
        text = item[0] if isinstance(item, tuple) else item
        body = text.lstrip('\u3000')
        indent = (len(text) - len(body)) * 24
        plain_lines(s, x + indent, y + k * gap, [(body,) + item[1:] if isinstance(item, tuple) else body], size, gap, color)

CW = 46


def centre(X, Y, i, j, cw=CW):
    return X + j * cw + (cw - 3) / 2, Y + i * cw + (cw - 3) / 2


def dp_grid(s, X, Y, data, st, cw=CW, top=None, left=None, size=15):
    """Filled table with labels above the columns and to the left of the rows."""
    grid(s, X, Y, [[inf(v) for v in r] for r in data], st, cw=cw, size=size)
    for j, t in enumerate(top or []):
        s.text(centre(X, Y, 0, j, cw)[0], Y - 13, t, 12.5, SUB, mono=True)
    for i, t in enumerate(left or []):
        s.text(X - 10, centre(X, Y, i, 0, cw)[1], t, 12.5, SUB, 'end', mono=True)


def string_table(s, X, Y, data, a, b, key, cw=CW):
    """Two-string table: row i = first i chars of a, column j = first j chars of b."""
    def st(i, j):
        if (i, j) in key:
            return key[(i, j)]
        return 'sent' if i == 0 or j == 0 else 'off'
    dp_grid(s, X, Y, data, st, cw, top=['空'] + list(b), left=['0  空'] + [f'{i + 1}  {ch}' for i, ch in enumerate(a)])
    for j in range(len(b) + 1):
        s.text(centre(X, Y, 0, j, cw)[0], Y - 30, j, 12.5, SUB, mono=True)
    s.text(X - 10, Y - 30, 'j', 12.5, SUB, 'end', mono=True, bold=True)
    s.text(X - 34, Y - 13, 'i', 12.5, SUB, 'end', mono=True, bold=True)


# ---------- 双序列 DP ----------

def lcs_dp(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp


def offset():
    a, b = 'abcde', 'ace'
    dp = lcs_dp(a, b)
    s = S()
    s.text(LX, 20, 'text1 = "abcde"：下标从 0 开始，「第几个字符」从 1 开始', 14.5, INK, 'start', bold=True)
    X, Y = 150, 70
    cs = row(s, X, Y, list(a), ['hit' if k < 3 else 'off' for k in range(5)], cw=46)
    s.text(X - 12, Y - 13, 'Python 下标', 12.5, SUB, 'end')
    s.text(X - 12, Y + 47, '第几个字符', 12.5, SUB, 'end')
    for k, c in enumerate(cs):
        s.text(c, Y - 13, k, 12.5, SUB, mono=True)
        s.text(c, Y + 47, k + 1, 12.5, COL['grn'] if k < 3 else SUB, mono=True, bold=k < 3)
    brace(s, cs[0] - 20, cs[2] + 20, Y + 68, '前 3 个字符（i = 3）', 'grn', up=False)
    lines(s, LX, Y + 118, ['dp 的下标 i 数的是「前 i 个字符」。', '前 3 个字符是 text1[0]、text1[1]、text1[2]，',
                           ('其中最后一个（第 3 个）是 text1[2]，也就是 text1[i − 1]。', 'red')], size=14, gap=25)
    X2, Y2 = 560, 70
    s.text(X2 - 70, 20, 'dp 表：6 行 4 列，比两个串各多 1', 14.5, INK, 'start', bold=True)
    string_table(s, X2, Y2, dp, a, b, {(3, 2): 'hit'})
    lines(s, X2 + 4 * CW + 26, Y2 + 6,
          [('灰色：第 0 行、第 0 列', SUB), ('有一边是空串（前 0 个字符）', SUB), '',
           ('绿色：dp[3][2]', 'grn'), '"abc" 和 "ac" 的答案', '', ('算它时比较的是', 'red'), ('text1[2] 和 text2[1]', 'red')],
          size=14, gap=25)
    s.save('lcs-offset')


def lcs_table():
    a, b = 'abcde', 'ace'
    dp = lcs_dp(a, b)
    assert dp[5][3] == 3 and a[2] == b[1] and a[3] != b[2]
    s = S()
    s.text(LX, 20, 'LC 1143：text1 = "abcde"，text2 = "ace"，dp[i][j] = 前 i 个和前 j 个的最长公共子序列长度', 14.5, INK, 'start', bold=True)
    X, Y = 90, 84
    key = {(3, 2): 'hit', (2, 1): 'new', (4, 3): 'chg', (3, 3): 'pur', (4, 2): 'pur', (5, 3): 'n'}
    string_table(s, X, Y, dp, a, b, key)
    lines(s, X + 4 * CW + 34, Y + 2,
          [('最后一个字符相同（绿）', 'grn'),
           f'dp[3][2]：text1[2] = text2[1] = "c"',
           (f'读左上角 dp[2][1] = {dp[2][1]}（橙），加 1 得 {dp[3][2]}', 'org'), '',
           ('最后一个字符不同（红）', 'red'),
           f'dp[4][3]：text1[3] = "d"，text2[2] = "e"',
           (f'读上面 dp[3][3] = {dp[3][3]} 和左边 dp[4][2] = {dp[4][2]}（紫），取大的得 {dp[4][3]}', 'pur'), '',
           (f'答案在右下角 dp[5][3] = {dp[5][3]}（蓝）', 'blue')], size=14, gap=25)
    s.save('lcs-lcs-table')


def edit_dp(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
    return dp


def edit_ops():
    s = S()
    s.text(LX, 20, 'LC 72：最后一步做的是哪种操作，决定 dp[i][j] 从哪个邻居来', 14.5, INK, 'start', bold=True)
    X, Y, w, h, gx, gy = 40, 56, 190, 64, 70, 60
    boxes = {'diag': (X, Y, 'dp[i−1][j−1]', '左上', 'new'), 'up': (X + w + gx, Y, 'dp[i−1][j]', '上', 'pur'),
             'left': (X, Y + h + gy, 'dp[i][j−1]', '左', 'chg'), 'me': (X + w + gx, Y + h + gy, 'dp[i][j]', '正在算', 'hit')}
    for x, y, t, where, st in boxes.values():
        s.node(x, y, t, st, w=w, h=h, size=16)
        s.text(x + w / 2, y - 12, where, 13, SUB)
    mx, my = X + w + gx, Y + h + gy
    s.arrow(X + w + 4, Y + h + 4, mx - 4, my - 4, 'org')
    s.text(X + w - 6, Y + h + 22, '替换 +1', 14, COL['org'], 'end', bold=True)
    s.arrow(mx + w / 2, Y + h + 4, mx + w / 2, my - 22, 'pur')
    s.text(mx + w / 2 + 44, Y + h + gy / 2 - 6, '删除 +1', 14, COL['pur'], bold=True)
    s.arrow(X + w + 4, my + h / 2, mx - 4, my + h / 2, 'red', label='插入 +1', loff=-14)
    lines(s, mx + w + 44, Y + 2,
          [('word1[i−1] == word2[j−1]：不用操作', 'grn'), '\u3000dp[i][j] = dp[i−1][j−1]', '',
           ('不相同：三种操作里挑最少的，再加 1', INK),
           ('\u3000替换：把 word1[i−1] 改成 word2[j−1]，剩下前 i−1 个对前 j−1 个', 'org'),
           ('\u3000删除：删掉 word1[i−1]，剩下前 i−1 个对前 j 个', 'pur'),
           ('\u3000插入：在 word1 末尾补一个 word2[j−1]，剩下前 i 个对前 j−1 个', 'red')], size=14, gap=27)
    s.save('lcs-edit-ops')


def edit_table():
    a, b = 'horse', 'ros'
    dp = edit_dp(a, b)
    assert dp[5][3] == 3
    # walk back from the bottom-right corner along one optimal sequence of operations
    i, j, path, ops = len(a), len(b), [(len(a), len(b))], []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1]:
            ops.append((f'"{a[i - 1]}" 相同，不操作', SUB))
            i, j = i - 1, j - 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            ops.append((f'替换：第 {i} 个字符 "{a[i - 1]}" 改成 "{b[j - 1]}"', 'org'))
            i, j = i - 1, j - 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ops.append((f'删除：第 {i} 个字符 "{a[i - 1]}"', 'pur'))
            i -= 1
        else:
            ops.append((f'插入："{b[j - 1]}"', 'red'))
            j -= 1
        path.append((i, j))
    print('edit path', path, [o[0] for o in ops])
    assert sum(1 for o in ops if o[1] != SUB) == dp[5][3]
    s = S()
    s.text(LX, 20, 'LC 72：word1 = "horse"，word2 = "ros"，dp[i][j] = 前 i 个变成前 j 个最少几步', 14.5, INK, 'start', bold=True)
    X, Y = 90, 84
    string_table(s, X, Y, dp, a, b, {p: 'hit' for p in path})
    out = [('绿色：从右下角 dp[5][3] = 3 倒着走回 dp[0][0] 的一条路', 'grn'), '每一格记下它是从哪个邻居算出来的：', '']
    for (pi, pj), (t, col) in zip(path, ops):
        out.append((f'dp[{pi}][{pj}] = {dp[pi][pj]}，{t}', col))
    out += ['', ('三步有操作（一次替换、两次删除），答案是 3', INK)]
    lines(s, X + 4 * CW + 34, Y - 6, out, size=14, gap=25)
    s.save('lcs-edit-table')


def distinct_table():
    a, b = 'babgbag', 'bag'
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = 1
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = dp[i - 1][j] + (dp[i - 1][j - 1] if a[i - 1] == b[j - 1] else 0)
    assert dp[n][m] == 5 and a[6] == b[2] and a[5] != b[2]
    s = S()
    s.text(LX, 20, 'LC 115：s = "babgbag"，t = "bag"，dp[i][j] = s 的前 i 个字符里选出 t 的前 j 个，有几种选法', 14.5, INK, 'start', bold=True)
    X, Y = 90, 84
    key = {(7, 3): 'hit', (6, 3): 'pur', (6, 2): 'new', (6, 1): 'chg', (5, 1): 'pur'}
    string_table(s, X, Y, dp, a, b, key)
    lines(s, X + 4 * CW + 34, Y + 2,
          [('相同：dp[7][3]（绿），s[6] = t[2] = "g"', 'grn'),
           (f'\u3000不用 s 的这个 g：上面 dp[6][3] = {dp[6][3]}（紫）', 'pur'),
           (f'\u3000用它配 t 的 g：左上 dp[6][2] = {dp[6][2]}（橙）', 'org'),
           f'\u3000{dp[6][3]} + {dp[6][2]} = {dp[7][3]}', '',
           ('不同：dp[6][1]（红），s[5] = "a"，t[0] = "b"', 'red'),
           (f'\u3000这个 a 配不上，只能不用：上面 dp[5][1] = {dp[5][1]}（紫）', 'pur'), '',
           ('第 0 列全是 1：t 的前 0 个字符是空串，什么都不选，1 种', SUB),
           ('第 0 行其余是 0：s 是空串，选不出非空的 t', SUB)], size=14, gap=25)
    s.save('lcs-distinct-table')


# ---------- 背包 ----------

VOLUMES, VALUES, CAPACITY = [1, 2, 3, 4], [2, 4, 4, 5], 5


def knap_2d():
    n = len(VOLUMES)
    dp = [[0] * (CAPACITY + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        volume, value = VOLUMES[i - 1], VALUES[i - 1]
        for capacity in range(CAPACITY + 1):
            dp[i][capacity] = dp[i - 1][capacity]
            if capacity >= volume:
                dp[i][capacity] = max(dp[i][capacity], dp[i - 1][capacity - volume] + value)
    assert dp[n][CAPACITY] == 8
    s = S()
    s.text(LX, 20, 'AcWing 2：4 件物品，背包容量 5。dp[i][capacity] = 只从前 i 件里选、总体积不超过 capacity 的最大总价值',
           14.5, INK, 'start', bold=True)
    X, Y = 270, 80
    left = ['i = 0  一件都没有'] + [f'i = {i + 1}  体积 {VOLUMES[i]} 价值 {VALUES[i]}' for i in range(n)]
    key = {(3, 5): 'hit', (2, 5): 'pur', (2, 2): 'new', (4, 5): 'n'}
    dp_grid(s, X, Y, dp, lambda i, j: key.get((i, j), 'sent' if i == 0 else 'off'), top=list(range(CAPACITY + 1)), left=left)
    s.text(X - 10, Y - 13, 'capacity', 12.5, SUB, 'end', mono=True, bold=True)
    lines(s, X + 6 * CW + 34, Y + 2,
          [('正在算 dp[3][5]（绿）：第 3 件体积 3、价值 4', 'grn'),
           (f'\u3000不选第 3 件：正上方 dp[2][5] = {dp[2][5]}（紫）', 'pur'),
           (f'\u3000选第 3 件：上一行往左 3 格 dp[2][2] = {dp[2][2]}（橙），加 4 得 {dp[2][2] + 4}', 'org'),
           f'\u3000取大的：max({dp[2][5]}, {dp[2][2] + 4}) = {dp[3][5]}', '',
           ('每一格只读上一行：正上方，和左上方某一格', INK), '',
           (f'答案在右下角 dp[4][5] = {dp[4][5]}（蓝）', 'blue')], size=14, gap=25)
    s.save('lcs-knap-2d')


def knap_rows():
    s = S()

    def panel(ox, title, read_row, color, words):
        s.text(ox, 20, title, 14.5, INK, 'start', bold=True)
        X, Y, cw = ox + 86, 62, 62
        for i, name in enumerate(['第 i−1 行', '第 i 行']):
            s.text(X - 12, Y + i * 70 + 20, name, 13, SUB, 'end')
            row(s, X, Y + i * 70, [''] * 6, ['off'] * 6, cw=cw, ch=40)
        tx, ty = X + 4 * cw + (cw - 3) / 2, Y + 70
        s.node(X + 4 * cw, ty, '在算', 'hit', w=cw - 3, h=40, size=14, mono=False)
        s.node(X + 4 * cw, Y, '不选', 'pur', w=cw - 3, h=40, size=14, mono=False)
        ry = Y + read_row * 70
        s.node(X + 1 * cw, ry, '选', color_st[color], w=cw - 3, h=40, size=14, mono=False)
        s.arrow(tx, Y + 42, tx, ty - 3, 'pur')
        if read_row == 0:
            s.arrow(X + 2 * cw, Y + 42, X + 4 * cw - 2, ty - 3, color)
        else:
            s.arrow(X + 2 * cw - 2, ty + 20, X + 4 * cw - 3, ty + 20, color)
        brace(s, X + 1 * cw + (cw - 3) / 2, tx, Y + 128, '往左 volume 格', color, up=False)
        lines(s, ox, Y + 172, words, size=14, gap=25)

    color_st = {'org': 'new', 'red': 'chg'}
    panel(18, '01 背包：「选」读的是上一行', 0, 'org',
          ['dp[i][capacity] = max(dp[i−1][capacity],', ('\u3000\u3000\u3000\u3000dp[i−1][capacity − volume] + value)', 'org'),
           '上一行里还没有第 i 件，所以它最多被用 1 次。', '',
           ('压成一维：容量从大到小。', 'org'),
           '算到 capacity 时，它左边的格子还没被这一轮改过，', '还是「上一行」的值。'])
    s.seg(548, 14, 548, 400, '#E5E7EB', sw=1)
    panel(574, '完全背包：「选」读的是这一行', 1, 'red',
          ['dp[i][capacity] = max(dp[i−1][capacity],', ('\u3000\u3000\u3000\u3000dp[i][capacity − volume] + value)', 'red'),
           '这一行里可能已经用过第 i 件，所以它能被用很多次。', '',
           ('压成一维：容量从小到大。', 'red'),
           '算到 capacity 时，它左边的格子已经被这一轮改过，', '是「这一行」的值。'])
    s.save('lcs-knap-rows')


def knap_direction():
    """Process the second item (volume 2, value 4) on dp = [0, 2, 2, 2, 2, 2] in both directions."""
    start = [0, 2, 2, 2, 2, 2]
    volume, value = 2, 4
    s = S()
    s.text(LX, 20, '01 背包：dp = [0, 2, 2, 2, 2, 2]（只放过第 1 件），现在处理第 2 件（体积 2，价值 4）', 14.5, INK, 'start', bold=True)

    def panel(ox, oy, title, order, good):
        s.text(ox, oy, title, 14.5, COL['grn'] if good else COL['red'], 'start', bold=True)
        dp = start[:]
        X, y = ox + 150, oy + 40
        s.text(X - 12, y + 17, '开始', 13, SUB, 'end')
        cs = row(s, X, y, dp, 'off', cw=46, idx='top')
        s.text(X - 12, y - 11, 'capacity', 12.5, SUB, 'end', mono=True, bold=True)
        trace = []
        for capacity in order:
            y += 48
            old = dp[capacity - volume]
            dp[capacity] = max(dp[capacity], old + value)
            fresh = (capacity - volume) in trace          # the cell we read was already rewritten this round
            trace.append(capacity)
            sts = ['off'] * 6
            sts[capacity] = 'hit' if not fresh else 'chg'
            sts[capacity - volume] = 'new'
            s.text(X - 12, y + 17, f'capacity = {capacity}', 13, SUB, 'end', mono=True)
            row(s, X, y, dp, sts, cw=46)
            t = f'dp[{capacity - volume}] + {value} = {old + value}'
            if fresh:
                t += f'，但 dp[{capacity - volume}] 里已经放过第 2 件'
            s.text(X + 6 * 46 + 10, y + 17, t, 13, COL['red'] if fresh else INK, 'start', bold=fresh)
        print(title, dp)
        return dp, y

    good, y1 = panel(18, 56, '容量从大到小（对）', range(CAPACITY, volume - 1, -1), True)
    s.seg(18, y1 + 54, 780, y1 + 54, '#E5E7EB', sw=1)
    bad, y2 = panel(18, y1 + 80, '容量从小到大（错）', range(volume, CAPACITY + 1), False)
    assert good == [0, 2, 4, 6, 6, 6] and bad == [0, 2, 4, 6, 8, 10]
    y = y2 + 60
    legend(s, 18, y, [('new', '读的格子'), ('hit', '写的格子（读到的是旧值）'), ('chg', '写的格子（读到的是这一轮刚改过的值）')])
    lines(s, 18, y + 44,
          [('从大到小：dp[5] = 6，就是第 1 件加第 2 件，每件只用了一次。', 'grn'),
           ('从小到大：dp[4] = 8 是第 2 件放了两次，dp[5] = 10 是第 1 件一次加第 2 件两次。', 'red'),
           ('一件物品被放了不止一次：01 背包里这是错的，完全背包要的正是这个效果。', 'red')],
          size=14, gap=26)
    s.save('lcs-knap-direction')


def knap_416():
    nums = [1, 5, 11, 5]
    target = sum(nums) // 2
    dp = [False] * (target + 1)
    dp[0] = True
    snaps = [('开始', dp[:], set())]
    for x in nums:
        fresh = set()
        for capacity in range(target, x - 1, -1):
            if not dp[capacity] and dp[capacity - x]:
                fresh.add(capacity)
            dp[capacity] = dp[capacity] or dp[capacity - x]
        snaps.append((f'放进 {x} 之后', dp[:], fresh))
    assert dp[target]
    s = S()
    s.text(LX, 20, f'LC 416：nums = [1, 5, 11, 5]，总和 22，目标是凑出 {target}。dp[capacity] = 能不能挑一些数，和正好是 capacity',
           14.5, INK, 'start', bold=True)
    X, y = 150, 76
    s.text(X - 12, y - 11, 'capacity', 12.5, SUB, 'end', mono=True, bold=True)
    for k, (name, snap, fresh) in enumerate(snaps):
        sts = ['new' if c in fresh else 'hit' if v else 'off' for c, v in enumerate(snap)]
        s.text(X - 12, y + 17, name, 13, SUB, 'end')
        row(s, X, y, ['T' if v else 'F' for v in snap], sts, cw=46, idx='top' if k == 0 else None)
        print(name, [c for c, v in enumerate(snap) if v])
        y += 48
    legend(s, 18, y + 8, [('hit', '之前就能凑出'), ('new', '这一轮新凑出的'), ('off', '凑不出')])
    s.text(18, y + 52, f'dp[{target}] 是 T：能挑出和为 {target} 的一组（就是 11 自己），剩下的 1 + 5 + 5 也是 {target}，返回 True',
           14, INK, 'start', bold=True)
    s.save('lcs-knap-416')


def knap_322():
    coins, amount = [1, 2, 5], 11
    INF = float('inf')
    dp = [INF] * (amount + 1)
    dp[0] = 0
    snaps = [('开始', dp[:], set())]
    for coin in coins:
        changed = set()
        for capacity in range(coin, amount + 1):
            if dp[capacity - coin] + 1 < dp[capacity]:
                dp[capacity] = dp[capacity - coin] + 1
                changed.add(capacity)
        snaps.append((f'加入面值 {coin} 之后', dp[:], changed))
    assert dp[amount] == 3
    s = S()
    s.text(LX, 20, 'LC 322：coins = [1, 2, 5]，amount = 11。dp[capacity] = 凑出金额 capacity 最少用几枚硬币，∞ 表示凑不出',
           14.5, INK, 'start', bold=True)
    X, y = 170, 76
    s.text(X - 12, y - 11, 'capacity', 12.5, SUB, 'end', mono=True, bold=True)
    for k, (name, snap, changed) in enumerate(snaps):
        sts = ['new' if c in changed else 'off' for c in range(amount + 1)]
        if k == len(snaps) - 1:
            sts[amount] = 'hit'
        s.text(X - 12, y + 17, name, 13, SUB, 'end')
        row(s, X, y, [inf(v) for v in snap], sts, cw=46, idx='top' if k == 0 else None)
        print(name, snap)
        y += 48
    legend(s, 18, y + 8, [('new', '这一轮变小了的格子'), ('hit', '答案')])
    s.text(18, y + 52, f'dp[11] = {dp[11]}：11 = 5 + 5 + 1。最后一轮里 dp[11] = dp[6] + 1 = {snaps[-1][1][6]} + 1，而 dp[6] = dp[1] + 1 也是这一轮刚算的（同一种硬币用了两次）',
           14, INK, 'start', bold=True)
    s.save('lcs-knap-322')


def knap_order():
    coins, amount = [1, 2], 3
    # carry the actual ways along with the counts
    ways = [[] for _ in range(amount + 1)]
    ways[0] = [[]]
    for coin in coins:
        for capacity in range(coin, amount + 1):
            ways[capacity] = ways[capacity] + [w_ + [coin] for w_ in ways[capacity - coin]]
    comb = ways
    ways = [[] for _ in range(amount + 1)]
    ways[0] = [[]]
    for capacity in range(1, amount + 1):
        for coin in coins:
            if coin <= capacity:
                ways[capacity] = ways[capacity] + [w_ + [coin] for w_ in ways[capacity - coin]]
    perm = ways
    assert len(comb[3]) == 2 and len(perm[3]) == 3
    print('comb', comb, 'perm', perm)
    s = S()
    s.text(LX, 20, '硬币 [1, 2]，凑出 3。两层循环谁在外面，数出来的东西不一样', 14.5, INK, 'start', bold=True)

    def panel(ox, title, code, data, color, foot):
        s.text(ox, 58, title, 14.5, COL[color], 'start', bold=True)
        for k, c in enumerate(code):
            s.text(ox + (len(c) - len(c.lstrip())) * 7.5, 88 + 21 * k, c.lstrip(), 12.5, INK, 'start', mono=True)
        X, y = ox + 30, 190
        for capacity in range(amount + 1):
            s.text(ox, y + 17, f'dp[{capacity}] = {len(data[capacity])}', 14, INK, 'start', bold=True, mono=True)
            txt = '\u00a0\u00a0\u00a0'.join('+'.join(map(str, w_)) if w_ else '什么都不放' for w_ in data[capacity])
            s.text(ox + 110, y + 17, txt, 14, COL[color] if capacity == amount else SUB, 'start', mono=True, bold=capacity == amount)
            y += 34
        lines(s, ox, y + 14, foot, size=14, gap=25)

    panel(18, '先物品后容量：数的是组合（LC 518）',
          ['for coin in coins:', '    for capacity in range(coin, amount + 1):', '        dp[capacity] += dp[capacity - coin]'],
          comb, 'grn', ['面值 1 的全部放完，才轮到面值 2。', '每种方案里硬币都是按 coins 的顺序排的，', ('2+1 这种顺序根本写不出来，所以不重复数。', 'grn')])
    s.seg(520, 44, 520, 420, '#E5E7EB', sw=1)
    panel(546, '先容量后物品：数的是排列（LC 377）',
          ['for capacity in range(1, amount + 1):', '    for coin in coins:', '        if coin <= capacity:',
           '            dp[capacity] += dp[capacity - coin]'],
          perm, 'red', ['每个金额都问一遍「最后一枚是哪种」。', '最后一枚是 1 和最后一枚是 2 各算各的，', ('1+2 和 2+1 被当成两种。', 'red')])
    s.save('lcs-knap-order')


if __name__ == '__main__':
    for f in (offset, lcs_table, edit_ops, edit_table, distinct_table, knap_2d, knap_rows, knap_direction, knap_416,
              knap_322, knap_order):
        f()
    print('ok')
