#!/usr/bin/env python3
"""Diagrams for 动态规划怎么想 / 线性 DP：一维 / 线性 DP：网格 in 常用代码模板5 (files lcr-*.svg / lcr-*.png).

Run from this directory:  python3 lc_r.py
"""
from bisect import bisect_left

from make_diagrams import *  # noqa: F401,F403
from make_diagrams_algo import row, lines, grid, inf  # also registers the 'pur' style


def label(s, y, t, mono=False, x=LX):
    s.text(x, y + 17, t, 14, INK, 'start', bold=True, mono=mono)


def outline(s, x, y, w, h, color, sw=3):
    s.rect(x, y, w, h, 'none', COL[color], rx=6, sw=sw)


# ====================== 动态规划怎么想 ======================

def climb_tree(name, memo):
    """Recursion tree of ways(5). memo=False: every call; memo=True: calls skipped by the memo are greyed out."""
    nodes, edges, order, seen = {}, [], [], set()
    leaf = [0]

    def build(i, depth, alive):
        key = len(nodes)
        nodes[key] = None
        hit = alive and memo and i > 1 and i in seen          # answered from the memo, no further calls
        if alive:
            order.append(i)
        kids = []
        if i > 1:
            for child in (i - 1, i - 2):
                kids.append(build(child, depth + 1, alive and not hit))
            x = (nodes[kids[0]][0] + nodes[kids[1]][0]) / 2
        else:
            x = leaf[0] * 50
            leaf[0] += 1
        if alive and not hit:
            seen.add(i)
        style = 'del' if not alive else 'hit' if hit else 'n'
        if not memo and order.count(i) > 1 and alive:
            style = 'chg'
        nodes[key] = (x, depth * 62, i, style)
        for kid in kids:
            edges.append((key, kid, '', 'gry' if nodes[kid][3] == 'del' else None, nodes[kid][3] == 'del'))
        return key

    build(5, 0, True)
    s = S()
    title = ('加上「记下来」：每个 i 只真正算一次，一共 %d 次调用' if memo else '暴力递归 climb_stairs(5)：一共 %d 次调用') % len(order)
    s.text(LX, 20, title, 15, INK, 'start', bold=True)
    tree(s, 40, 70, nodes, edges)
    if memo:
        assert len(order) == 9
        legend(s, LX, 350, [('n', '第一次算，算完记进 memo'), ('hit', '已经记过，直接查到'), ('del', '不会再调用')])
    else:
        assert len(order) == 15
        counts = '、'.join(f'参数 {i} 算了 {order.count(i)} 次' for i in (3, 2, 1, 0))
        legend(s, LX, 350, [('n', '第一次算这个 i'), ('chg', '重复算')])
        s.text(LX, 392, '同一个问题被算了很多遍：' + counts, 14, INK, 'start', bold=True)
    s.save(name)


def climb_table():
    n = 5
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    assert dp == [1, 1, 2, 3, 5, 8]
    s = S()
    cw, X, y = 64, 100, 78
    label(s, y, 'dp', True)
    sts = ['sent', 'sent', 'n', 'new', 'new', 'hit']
    cs = row(s, X, y, dp, sts, cw=cw, idx='bot')
    s.text(X + 3 * cw, y + 62, '下标 i = 台阶数', 12.5, SUB)
    s.curve(cs[4], y - 4, cs[5] - 6, y - 4, -16, 'org')
    s.curve(cs[3], y - 4, cs[5] + 6, y - 4, -30, 'org')
    s.text(cs[2], y - 30, '算 dp[5] 要读的两格（橙）', 13.5, COL['org'], bold=True)
    s.arrow(X, y + 88, X + 6 * cw - 6, y + 88, 'blue')
    s.text(X + 3 * cw, y + 104, '从小到大填：算 dp[i] 时，dp[i − 1] 和 dp[i − 2] 已经填好了', 13, COL['blue'])
    lines(s, X + 6 * cw + 40, y - 30,
          [('n = 5', INK), 'dp[0] = 1，dp[1] = 1：初始值，直接知道（灰）',
           'dp[2] = dp[1] + dp[0] = 2', 'dp[3] = dp[2] + dp[1] = 3', 'dp[4] = dp[3] + dp[2] = 5',
           (f'dp[5] = dp[4] + dp[3] = {dp[4]} + {dp[3]} = {dp[5]}（绿）', 'grn'),
           ('答案在最后一格 dp[n]', INK)], gap=24)
    s.save('lcr-climb-table')


def climb_split():
    def all_ways(i):
        if i == 0:
            return [[]]
        found = []
        for step in (1, 2):
            if i >= step:
                found += [way + [step] for way in all_ways(i - step)]
        return found

    n = 4
    ways = all_ways(n)
    assert len(ways) == 5
    s = S()
    s.text(LX, 20, f'dp[{n}] 代表的集合：所有爬到第 {n} 阶的走法（存的属性：个数 = {len(ways)}）', 15, INK, 'start', bold=True)
    s.text(LX, 46, '按「最后一步跨了几阶」把集合分成两块，两块不重复、不遗漏', 13.5, SUB, 'start')
    X = LX
    for step, st, col in ((1, 'n', 'blue'), (2, 'new', 'org')):
        part = [way for way in ways if way[-1] == step]
        w, h = 400, 82 + 34 * 3
        s.rect(X, 66, w, h, '#FFFFFF', COL[col], rx=10)
        s.text(X + 14, 86, f'最后一步跨 {step} 阶：{len(part)} 种', 14.5, COL[col], 'start', bold=True)
        for k, way in enumerate(part):
            yy = 108 + 34 * k
            cs = cells(s, X + 14, yy, [(str(v), 'off') for v in way[:-1]] + [(str(way[-1]), st)], cw=34, ch=28, size=14)
            s.text(X + 14 + 4 * 37 + 10, yy + 14, '前面是一种爬到第 %d 阶的走法' % (n - step) if k == 0 else '', 12.5, SUB, 'start')
        s.text(X + 14, 66 + h - 16, f'去掉最后一步，就是「爬到第 {n - step} 阶的全部走法」：dp[{n - step}] = {len(part)}', 13, INK,
               'start')
        X += w + 24
    s.text(LX, 66 + 184 + 28, f'所以 dp[{n}] = dp[{n - 1}] + dp[{n - 2}] = 3 + 2 = {len(ways)}。一般地 dp[i] = dp[i − 1] + dp[i − 2]',
           15, COL['grn'], 'start', bold=True)
    s.save('lcr-climb-split')


def cost_trace():
    cost = [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]
    n = len(cost)
    dp = [0] * (n + 1)
    for i in range(2, n + 1):
        dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])
    assert dp[n] == 6
    i = 7
    s = S()
    cw, X, y = 62, 110, 40
    label(s, y, 'cost', True)
    row(s, X, y, cost, ['new' if k in (i - 1, i - 2) else 'n' for k in range(n)], cw=cw, idx='top')
    s.text(X + n * cw + cw / 2 - 2, y + 17, '楼顶', 14, COL['grn'], bold=True)
    y2 = y + 78
    label(s, y2, 'dp', True)
    sts = ['sent' if k < 2 else 'chg' if k in (i - 1, i - 2) else 'hit' if k == i else 'n' for k in range(n + 1)]
    sts[n] = 'hit'
    row(s, X, y2, dp, sts, cw=cw, idx='bot')
    a, b = dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2]
    lines(s, LX, y2 + 78,
          [(f'dp[i]：站到第 i 阶上，最少已经付了多少。dp[0] = dp[1] = 0：可以直接从第 0 阶或第 1 阶出发（灰）', INK, False),
           (f'算 dp[{i}]：从第 {i - 1} 阶跨 1 阶上来，dp[{i - 1}] + cost[{i - 1}] = {dp[i - 1]} + {cost[i - 1]} = {a}；'
            f'从第 {i - 2} 阶跨 2 阶上来，dp[{i - 2}] + cost[{i - 2}] = {dp[i - 2]} + {cost[i - 2]} = {b}', 'red', False),
           (f'取小的：dp[{i}] = min({a}, {b}) = {dp[i]}。楼顶是下标 {n}（数组外面一格），答案 dp[{n}] = {dp[n]}', 'grn')], gap=25)
    s.save('lcr-cost-trace')


# ====================== 线性 DP：一维 ======================

def two_states():
    nums = [2, 7, 9, 3, 1]
    s = S()
    cw, X = 64, 150
    y = 76
    s.text(LX, 20, '定义一：前 i 个。dp[i] 管的是 nums[0..i − 1] 这一整段，方案里可以没有最后一个', 15, COL['blue'], 'start', bold=True)
    label(s, y, 'nums', True)
    cs = row(s, X, y, nums, ['n', 'n', 'n', 'n', 'off'], cw=cw, idx='bot')
    brace(s, cs[0] - 28, cs[3] + 28, y - 8, 'dp[4]：前 4 个里随便选（比如只选 2 和 9，最后一个 3 没用上）', 'blue')
    s.text(X + 5 * cw + 30, y + 17, '答案 = dp[n]（最后一格）', 14, COL['blue'], 'start', bold=True)
    y = 232
    s.text(LX, y - 56, '定义二：以第 i 个结尾。方案必须用上 nums[i]，而且 nums[i] 是方案的最后一个', 15, COL['org'], 'start', bold=True)
    label(s, y, 'nums', True)
    cs = row(s, X, y, nums, ['off', 'n', 'n', 'new', 'off'], cw=cw, idx='bot')
    brace(s, cs[1] - 28, cs[3] + 28, y - 8, 'dp[3]：结尾钉死在 nums[3]，往前延伸多长都行', 'org')
    s.text(X + 5 * cw + 30, y + 17, '答案 = max(dp)（每一格都可能是答案）', 14, COL['org'], 'start', bold=True)
    s.save('lcr-two-states')


def rob_trace():
    nums = [2, 7, 9, 3, 1]
    n = len(nums)
    dp = [0] * (n + 1)
    dp[1] = nums[0]
    for i in range(2, n + 1):
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i - 1])
    assert dp == [0, 2, 7, 11, 11, 12]
    i = 5
    s = S()
    cw, X, y = 64, 130, 34
    label(s, y, 'nums', True)
    row(s, X + cw, y, nums, ['n'] * 4 + ['new'], cw=cw, idx='top')
    y2 = y + 76
    label(s, y2, 'dp', True)
    cs = row(s, X, y2, dp, ['sent', 'sent', 'n', 'chg', 'chg', 'hit'], cw=cw, idx='bot')
    s.text(LX, y2 + 60, 'dp[i]：前 i 间房', 12.5, SUB, 'start')
    lines(s, X + 6 * cw + 36, y - 4,
          [(f'算 dp[{i}]（绿）：最后一间是 nums[{i - 1}] = {nums[i - 1]}（橙）', INK),
           f'不偷它：前 {i - 1} 间随便偷，dp[{i - 1}] = {dp[i - 1]}',
           f'偷它：第 {i - 1} 间不能偷，前 {i - 2} 间随便偷，dp[{i - 2}] + {nums[i - 1]} = {dp[i - 2] + nums[i - 1]}',
           (f'dp[{i}] = max({dp[i - 1]}, {dp[i - 2] + nums[i - 1]}) = {dp[i]}', 'grn'),
           'dp 比 nums 多一格：dp[0] 是「一间都没有」，等于 0',
           ('第 i 间房是 nums[i − 1]，所以 dp 画得比 nums 靠左一格', INK, False)], gap=24)
    s.save('lcr-rob-trace')


def rob_circle():
    def rob_line(houses):
        n = len(houses)
        dp = [0] * (n + 1)
        dp[1] = houses[0]
        for i in range(2, n + 1):
            dp[i] = max(dp[i - 1], dp[i - 2] + houses[i - 1])
        return dp[n]

    nums = [1, 2, 3, 1]
    a, b = rob_line(nums[1:]), rob_line(nums[:-1])
    assert (a, b) == (3, 4)
    s = S()
    cw, X, y = 64, 240, 60
    label(s, y, '围成一圈的 nums', False)
    cs = row(s, X, y, nums, 'n', cw=cw, idx='bot')
    s.curve(cs[0], y - 4, cs[-1], y - 4, -22, 'red', dash=1, label='首尾相邻，不能都偷')
    y += 84
    label(s, y, '① 不偷第一间：nums[1:]')
    row(s, X, y, nums, ['del', 'new', 'new', 'new'], cw=cw)
    s.text(X + 4 * cw + 24, y + 17, f'剩下的是一排，LC 198 → {a}', 14, COL['org'], 'start', bold=True)
    y += 52
    label(s, y, '② 不偷最后一间：nums[:-1]')
    row(s, X, y, nums, ['hit', 'hit', 'hit', 'del'], cw=cw)
    s.text(X + 4 * cw + 24, y + 17, f'剩下的是一排，LC 198 → {b}', 14, COL['grn'], 'start', bold=True)
    s.text(LX, y + 62, f'首尾不能都偷 = 至少有一头不偷。两种情况各算一次，取大的：max({a}, {b}) = {max(a, b)}', 14.5, INK, 'start',
           bold=True)
    s.save('lcr-rob-circle')


def kadane_trace():
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    for i in range(1, n):
        dp[i] = max(nums[i], dp[i - 1] + nums[i])
    best = max(dp)
    end = dp.index(best)
    assert best == 6 and end == 6
    s = S()
    cw, X, y = 64, 110, 62
    label(s, y, 'nums', True)
    cs = row(s, X, y, [inf(v) for v in nums], ['new' if 3 <= k <= end else 'n' for k in range(n)], cw=cw, idx='bot')
    brace(s, cs[3] - 28, cs[end] + 28, y - 8, '以 nums[6] 结尾、和最大的一段：4 + (−1) + 2 + 1 = 6', 'org')
    y2 = y + 76
    label(s, y2, 'dp', True)
    row(s, X, y2, [inf(v) for v in dp], ['hit' if k == end else 'chg' if k == 3 else 'n' for k in range(n)], cw=cw)
    lines(s, LX, y2 + 64,
          [('dp[i]：以 nums[i] 结尾的子数组里，最大的和。每一格只有两种选法：接在前一段后面，或者从自己重新开始', INK, False),
           (f'dp[3]（红）：前一段 dp[2] = {inf(dp[2])} 是负的，接上去只会更小，所以从自己重新开始，dp[3] = 4', 'red', False),
           (f'答案不在最后一格：最后一格 dp[8] = {dp[8]}，最大的是 dp[{end}] = {best}（绿），所以返回 max(dp)', 'grn')], gap=25)
    s.save('lcr-kadane-trace')


def lis_trace():
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    n = len(nums)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    assert dp == [1, 1, 1, 2, 2, 3, 4, 4]
    i = 5
    smaller = [j for j in range(i) if nums[j] < nums[i]]
    s = S()
    cw, X, y = 64, 110, 34
    label(s, y, 'nums', True)
    row(s, X, y, nums, ['new' if j in smaller else 'hit' if j == i else 'off' if j < i else 'n' for j in range(n)],
        cw=cw, idx='top')
    y2 = y + 56
    label(s, y2, 'dp', True)
    row(s, X, y2, dp, ['new' if j in smaller else 'hit' if j == i else 'off' if j < i else 'n' for j in range(n)], cw=cw)
    lines(s, LX, y2 + 62,
          [(f'算 dp[{i}]（绿，nums[{i}] = {nums[i]}）：子序列以 7 结尾，按「7 的前一个数是谁」分', INK),
           '前面比 7 小的（橙）才能排在 7 前面：' + '，'.join(f'nums[{j}] = {nums[j]}（dp[{j}] = {dp[j]}）' for j in smaller),
           f'接在它们后面，长度分别是 ' + '、'.join(f'{dp[j]} + 1' for j in smaller) + '；7 也可以自己单独一个，长度 1',
           (f'dp[{i}] = 这些里最大的 = {dp[i]}（比如 2, 5, 7 或 2, 3, 7）', 'grn'),
           (f'全部填完后答案 = max(dp) = {max(dp)}（2, 3, 7, 18 或 2, 3, 7, 101）', INK)], gap=24)
    s.save('lcr-lis-trace')


def lis_tails():
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    tails, rows = [], []
    for x in nums:
        index = bisect_left(tails, x)
        if index == len(tails):
            tails.append(x)
            action = ('t', f'比 tails 里的都大：追加，长度变成 {len(tails)}', 'grn')
        else:
            action = ('t', f'第一个 >= {x} 的是 tails[{index}] = {tails[index]}：换成 {x}', 'org')
            tails[index] = x
        rows.append([[(str(x), 'n')], str(index), action,
                     [(str(v), 'new' if k == index else 'off') for k, v in enumerate(tails)]])
    assert tails == [2, 3, 7, 18]
    table('lcr-lis-tails', ['读到 x', 'bisect_left 的结果', '动作', '之后的 tails'], [80, 150, 330, 240], rows, cw=46,
          foot=f'nums = {nums}：最后 tails 的长度 {len(tails)} 就是答案',
          leg=[('new', '这一步改动的位置')])


def word_break():
    text, words = 'leetcode', {'leet', 'code'}
    n = len(text)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and text[j:i] in words:
                dp[i] = True
                break
    assert [i for i in range(n + 1) if dp[i]] == [0, 4, 8]
    s = S()
    cw, X, y = 64, 110, 66
    label(s, y, 's', True)
    row(s, X + cw / 2, y, list(text), ['n'] * 4 + ['new'] * 4, cw=cw, idx='top')
    y2 = y + 84
    label(s, y2, 'dp', True)
    cs = row(s, X, y2, ['T' if v else 'F' for v in dp], ['hit' if v else 'off' for v in dp], cw=cw, idx='bot')
    for c in cs:
        s.seg(c, y + 38, c, y2 - 4, '#94A3B8', dash=1, sw=1.2)
    brace(s, cs[4] + 4, cs[8] - 4, y - 26, '最后一个词 s[4:8] = "code"，在字典里', 'org')
    brace(s, cs[0] + 4, cs[4] - 4, y - 26, '前 4 个字符：dp[4] = True', 'grn')
    lines(s, X + 9 * cw + 30, y - 24,
          [('wordDict = ["leet", "code"]', INK),
           'dp[i]：虚线左边的 i 个字符能不能拆',
           'dp[0] = True：空串，什么都不用拆',
           ('dp[8]：找一个切口 j，让', INK), ('  dp[j] 是 True（前 j 个能拆）', 'grn'), ('  并且 s[j:8] 是字典里的词', 'org'),
           ('j = 4 满足，所以 dp[8] = True', INK)], gap=24)
    s.save('lcr-word-break')


def decode_trace():
    s = S()
    cw, X = 64, 110
    y = 36
    for text in ('226', '2101'):
        n = len(text)
        dp = [0] * (n + 1)
        dp[0] = 1
        notes = []
        for i in range(1, n + 1):
            one = text[i - 1] != '0'
            two = i >= 2 and 10 <= int(text[i - 2:i]) <= 26
            if one:
                dp[i] += dp[i - 1]
            if two:
                dp[i] += dp[i - 2]
            notes.append(f'dp[{i}]：单独解 "{text[i - 1]}" ' + (f'可以 +dp[{i - 1}]' if one else '不行（0 没有对应的字母）')
                         + ('' if i < 2 else f'；一起解 "{text[i - 2:i]}" ' + (f'可以 +dp[{i - 2}]' if two else '不行'))
                         + f' → {dp[i]}')
        label(s, y, f's = "{text}"', True)
        row(s, X + cw + cw / 2, y, list(text), ['chg' if ch == '0' else 'n' for ch in text], cw=cw)
        label(s, y + 46, 'dp', True)
        row(s, X + cw, y + 46, dp, ['sent'] + ['hit' if i == n else 'n' for i in range(1, n + 1)], cw=cw, idx='bot')
        lines(s, X + 6 * cw + 50, y - 4, notes, gap=23)
        y += 150
    assert dp[-1] == 1
    s.text(LX, y - 16, 'dp[0] = 1（灰）：空串算一种，表示「前面已经全部解完」。答案在最后一格（绿）', 14, INK, 'start', bold=True)
    s.save('lcr-decode-trace')


# ====================== 线性 DP：网格 ======================

CELL = 46


def cell_xy(X, Y, r, c, cw=CELL):
    return X + c * cw + (cw - 3) / 2, Y + r * cw + (cw - 3) / 2


def headers(s, X, Y, m, n, cw=CELL):
    for c in range(n):
        s.text(X + c * cw + (cw - 3) / 2, Y - 11, c, 12, SUB, mono=True)
    for r in range(m):
        s.text(X - 12, Y + r * cw + (cw - 3) / 2, r, 12, SUB, mono=True)


def reads(s, X, Y, r, c, up=True, left=True, diag=False, cw=CELL):
    x, y = cell_xy(X, Y, r, c, cw)
    half = (cw - 3) / 2
    if up:
        s.arrow(x + half * 0.62, y - half - 12, x + half * 0.62, y - half + 9, 'red', sw=2.4)
    if left:
        s.arrow(x - half - 12, y + half * 0.62, x - half + 9, y + half * 0.62, 'red', sw=2.4)
    if diag:
        s.arrow(x - half - 10, y - half - 10, x - half + 8, y - half + 8, 'red', sw=2.4)


def grid_idea():
    m, n, r, c = 4, 5, 2, 3
    s = S()
    X, Y = 60, 60
    s.text(LX, 20, 'dp[row][col]：走到这一格的答案。只能往右或往下走，所以走进一个格子的最后一步只有两种', 15, INK, 'start', bold=True)
    headers(s, X, Y, m, n, 58)

    def st(i, j):
        if (i, j) == (r, c):
            return 'hit'
        if (i, j) in ((r - 1, c), (r, c - 1)):
            return 'new'
        return 'sent' if i == 0 or j == 0 else 'off'
    grid(s, X, Y, [['起点' if (i, j) == (0, 0) else '终点' if (i, j) == (m - 1, n - 1) else '上' if (i, j) == (r - 1, c)
                    else '左' if (i, j) == (r, c - 1) else '?' if (i, j) == (r, c) else '' for j in range(n)]
                   for i in range(m)], st, cw=58, size=13)
    reads(s, X, Y, r, c, cw=58)
    lines(s, X + n * 58 + 34, Y + 4,
          [('最后一步只有两种：', INK), ('从上面的格子往下走一步', 'org'), ('从左边的格子往右走一步', 'org'),
           ('所以 dp[row][col] 只由「上」和「左」两格算出来', 'grn'),
           '第一行只能从左边来，第一列只能从上面来：', '它们是初始值（灰），先单独填好',
           '然后一行一行、每行从左到右填，', '轮到一个格子时，它的上面和左边都已经填好了'], gap=24)
    s.save('lcr-grid-idea')


def paths_62():
    m, n = 3, 7
    dp = [[1] * n for _ in range(m)]
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
    assert dp[m - 1][n - 1] == 28
    r, c = 2, 3
    s = S()
    X, Y, cw = 60, 44, 56
    headers(s, X, Y, m, n, cw)

    def st(i, j):
        if (i, j) == (r, c):
            return 'chg'
        if (i, j) in ((r - 1, c), (r, c - 1)):
            return 'new'
        if (i, j) == (m - 1, n - 1):
            return 'hit'
        return 'sent' if i == 0 or j == 0 else 'n'
    grid(s, X, Y, dp, st, cw=cw, size=15)
    reads(s, X, Y, r, c, cw=cw)
    lines(s, X + n * cw + 30, Y + 2,
          [('LC 62：m = 3，n = 7，dp[row][col] = 走到这一格有几条路', INK),
           '第一行、第一列都是 1（灰）：只有一条路，一直往右或一直往下',
           (f'dp[{r}][{c}]（红）= 上 + 左 = dp[{r - 1}][{c}] + dp[{r}][{c - 1}] = {dp[r - 1][c]} + {dp[r][c - 1]} = {dp[r][c]}', 'red'),
           (f'答案在右下角：dp[{m - 1}][{n - 1}] = {dp[m - 1][n - 1]}（绿）', 'grn')], gap=26)
    s.save('lcr-paths-62')


def paths_63():
    obstacle_grid = [[0, 0, 0, 1, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
    m, n = len(obstacle_grid), len(obstacle_grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = 1
    for c in range(1, n):
        if obstacle_grid[0][c] == 0:
            dp[0][c] = dp[0][c - 1]
    for r in range(1, m):
        if obstacle_grid[r][0] == 0:
            dp[r][0] = dp[r - 1][0]
    for r in range(1, m):
        for c in range(1, n):
            if obstacle_grid[r][c] == 0:
                dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
    s = S()
    X, Y, cw = 60, 62, 54
    s.text(X, 20, 'obstacleGrid（1 = 障碍）', 14.5, INK, 'start', bold=True)
    headers(s, X, Y, m, n, cw)
    grid(s, X, Y, obstacle_grid, lambda i, j: 'wall' if obstacle_grid[i][j] else 'off', cw=cw, size=15)
    X2 = X + n * cw + 80
    s.text(X2, 20, 'dp（走到这一格有几条路）', 14.5, INK, 'start', bold=True)
    headers(s, X2, Y, m, n, cw)
    grid(s, X2, Y, dp, lambda i, j: 'wall' if obstacle_grid[i][j] else 'hit' if (i, j) == (m - 1, n - 1)
         else 'chg' if (i, j) == (0, 4) else 'sent' if i == 0 or j == 0 else 'n', cw=cw, size=15)
    lines(s, X2 + n * cw + 30, Y + 2,
          [('障碍格：走不到，dp = 0（黑）', INK),
           '其余的格子照旧：上 + 左',
           ('第一行只能从左边来：dp[0][3] 是障碍，', 'red', False), ('它右边的 dp[0][4] 也走不到，是 0（红）', 'red', False),
           ('所以第一行、第一列要一格一格往后传，', 'red', False), ('不能像 LC 62 那样直接全填 1', 'red', False),
           (f'答案 dp[{m - 1}][{n - 1}] = {dp[m - 1][n - 1]}（绿）', 'grn')], gap=25)
    s.save('lcr-paths-63')
    return dp


def minpath_64():
    grid_values = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
    m, n = 3, 3
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid_values[0][0]
    for c in range(1, n):
        dp[0][c] = dp[0][c - 1] + grid_values[0][c]
    for r in range(1, m):
        dp[r][0] = dp[r - 1][0] + grid_values[r][0]
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = min(dp[r - 1][c], dp[r][c - 1]) + grid_values[r][c]
    assert dp[2][2] == 7
    path, r, c = [(2, 2)], 2, 2
    while (r, c) != (0, 0):
        if r == 0 or (c > 0 and dp[r][c - 1] <= dp[r - 1][c]):
            c -= 1
        else:
            r -= 1
        path.append((r, c))
    s = S()
    X, Y, cw = 60, 62, 58
    s.text(X, 20, 'grid', 14.5, INK, 'start', bold=True, mono=True)
    headers(s, X, Y, m, n, cw)
    grid(s, X, Y, grid_values, lambda i, j: 'new' if (i, j) in path else 'off', cw=cw, size=16)
    X2 = X + n * cw + 80
    s.text(X2, 20, 'dp（走到这一格的最小路径和）', 14.5, INK, 'start', bold=True)
    headers(s, X2, Y, m, n, cw)
    grid(s, X2, Y, dp, lambda i, j: 'hit' if (i, j) == (2, 2) else 'chg' if (i, j) in ((1, 2), (2, 1))
         else 'sent' if i == 0 or j == 0 else 'n', cw=cw, size=16)
    reads(s, X2, Y, 2, 2, cw=cw)
    lines(s, X2 + n * cw + 30, Y - 6,
          [('第一行：只能从左边来，一路累加 1, 4, 5', INK, False), ('第一列：只能从上面来，一路累加 1, 2, 6', INK, False),
           (f'dp[2][2] = min(上 {dp[1][2]}, 左 {dp[2][1]}) + grid[2][2]', 'red'), (f'        = {min(dp[1][2], dp[2][1])} + 1 = {dp[2][2]}（绿）', 'grn'),
           ('左图橙色是这条最小的路：1 → 3 → 1 → 1 → 1', 'org')], gap=26)
    s.save('lcr-minpath-64')


def triangle_120():
    triangle = [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]
    n = len(triangle)
    dp = [[0] * (r + 1) for r in range(n)]
    dp[0][0] = triangle[0][0]
    for r in range(1, n):
        dp[r][0] = dp[r - 1][0] + triangle[r][0]
        dp[r][r] = dp[r - 1][r - 1] + triangle[r][r]
        for c in range(1, r):
            dp[r][c] = min(dp[r - 1][c - 1], dp[r - 1][c]) + triangle[r][c]
    assert min(dp[n - 1]) == 11
    path, c = [], dp[n - 1].index(min(dp[n - 1]))
    for r in range(n - 1, -1, -1):
        path.append((r, c))
        if r and (c == r or (c > 0 and dp[r - 1][c - 1] < dp[r - 1][c])):
            c -= 1
    s = S()
    cw, Y = 56, 62
    X = 60
    s.text(X, 20, '题目画的样子', 14.5, INK, 'start', bold=True)
    for r in range(n):
        for c in range(r + 1):
            s.node(X + (n - 1 - r) * cw / 2 + c * cw, Y + r * cw, triangle[r][c], 'new' if (r, c) in path else 'off',
                   w=cw - 3, h=cw - 3)
    X2 = X + n * cw + 70
    s.text(X2, 20, '存在 list 里的样子：triangle', 14.5, INK, 'start', bold=True)
    headers(s, X2, Y, n, n, cw)
    for r in range(n):
        for c in range(r + 1):
            s.node(X2 + c * cw, Y + r * cw, triangle[r][c], 'new' if (r, c) in path else 'off', w=cw - 3, h=cw - 3)
    X3 = X2 + n * cw + 70
    s.text(X3, 20, 'dp（从顶走到这一格的最小路径和）', 14.5, INK, 'start', bold=True)
    headers(s, X3, Y, n, n, cw)
    for r in range(n):
        for c in range(r + 1):
            st = ('hit' if (r, c) == (3, 1) else 'chg' if (r, c) in ((2, 0), (2, 1)) else
                  'sent' if c == 0 or c == r else 'n')
            s.node(X3 + c * cw, Y + r * cw, dp[r][c], st, w=cw - 3, h=cw - 3)
    reads(s, X3, Y, 3, 1, up=True, left=False, diag=True, cw=cw)
    lines(s, LX, Y + n * cw + 22,
          [('左对齐以后，「下一行相邻的两个」是正下方 [row + 1][col] 和右下方 [row + 1][col + 1]', INK, False),
           ('反过来，走进 [row][col] 的只有：正上方 [row − 1][col] 和左上方 [row − 1][col − 1]', 'red'),
           ('每行最左一格只有正上方，最右一格只有左上方（灰）', INK, False),
           (f'dp[3][1] = min(左上 {dp[2][0]}, 正上 {dp[2][1]}) + 1 = {dp[3][1]}。终点可以是最后一行任何一格：答案 = min(最后一行) = {min(dp[-1])}',
            'grn')], gap=25)
    s.save('lcr-triangle-120')


def square_dp(matrix):
    m, n = len(matrix), len(matrix[0])
    dp = [[0] * n for _ in range(m)]
    for r in range(m):
        for c in range(n):
            if matrix[r][c] == '1':
                dp[r][c] = 1 if r == 0 or c == 0 else min(dp[r - 1][c], dp[r][c - 1], dp[r - 1][c - 1]) + 1
    return dp


def square_221():
    matrix = [list('10100'), list('10111'), list('11111'), list('10010')]
    m, n = len(matrix), len(matrix[0])
    dp = square_dp(matrix)
    side = max(max(r) for r in dp)
    assert side == 2
    best = [(r, c) for r in range(m) for c in range(n) if dp[r][c] == side]
    r0, c0 = best[0]
    s = S()
    X, Y, cw = 60, 62, 54
    s.text(X, 20, 'matrix', 14.5, INK, 'start', bold=True, mono=True)
    headers(s, X, Y, m, n, cw)
    grid(s, X, Y, matrix, lambda i, j: 'n' if matrix[i][j] == '1' else 'off', cw=cw, size=15)
    outline(s, X + (c0 - side + 1) * cw - 3, Y + (r0 - side + 1) * cw - 3, side * cw + 3, side * cw + 3, 'grn')
    X2 = X + n * cw + 80
    s.text(X2, 20, 'dp（以这一格为右下角的最大正方形的边长）', 14.5, INK, 'start', bold=True)
    headers(s, X2, Y, m, n, cw)
    grid(s, X2, Y, dp, lambda i, j: 'hit' if (i, j) == (r0, c0) else 'new' if (i, j) in ((r0 - 1, c0), (r0, c0 - 1), (r0 - 1, c0 - 1))
         else 'n' if dp[i][j] else 'off', cw=cw, size=15)
    reads(s, X2, Y, r0, c0, diag=True, cw=cw)
    lines(s, X2 + n * cw + 30, Y + 2,
          [(f'dp[{r0}][{c0}]（绿）：matrix[{r0}][{c0}] 是 "1"', INK),
           f'上 {dp[r0 - 1][c0]}、左 {dp[r0][c0 - 1]}、左上 {dp[r0 - 1][c0 - 1]}（橙），最小的是 '
           f'{min(dp[r0 - 1][c0], dp[r0][c0 - 1], dp[r0 - 1][c0 - 1])}',
           (f'dp[{r0}][{c0}] = 1 + 1 = {dp[r0][c0]}：左图绿框那个 2 × 2', 'grn'),
           'matrix 是 "0" 的格子：dp = 0',
           (f'最大的 dp 是 {side}，答案是面积 {side} × {side} = {side * side}', INK)], gap=26)
    s.save('lcr-square-221')


def square_why():
    panels = [
        ('三个邻居都是 2 → 这一格是 3', [list('111'), list('111'), list('111')]),
        ('上面的邻居只有 1 → 这一格只能是 2', [list('110'), list('111'), list('111')]),
    ]
    s = S()
    cw, Y = 62, 96
    X = 50
    for title, matrix in panels:
        dp = square_dp(matrix)
        up, left, diag = dp[1][2], dp[2][1], dp[1][1]
        s.text(X - 10, 20, title, 15, INK, 'start', bold=True)
        s.text(X - 10, 46, f'上 = {up}，左 = {left}，左上 = {diag}，min = {min(up, left, diag)}，dp = {dp[2][2]}', 13.5,
               COL['grn'], 'start', bold=True)
        grid(s, X, Y, matrix, lambda i, j: 'hit' if (i, j) == (2, 2) else 'chg' if matrix[i][j] == '0' else 'off', cw=cw, size=16)
        for (r, c, value, col, inset) in ((1, 2, up, 'blue', 4), (2, 1, left, 'org', 8), (1, 1, diag, 'pur', 12)):
            outline(s, X + (c - value + 1) * cw + inset - 2, Y + (r - value + 1) * cw + inset - 2,
                    value * cw - 2 * inset + 1, value * cw - 2 * inset + 1, col, sw=2.6)
        new = dp[2][2]
        s.rect(X + (3 - new) * cw - 5, Y + (3 - new) * cw - 5, new * cw + 7, new * cw + 7, 'none', COL['grn'], dash=1, rx=8, sw=2.6)
        X += 3 * cw + 150
    lines(s, X - 30, Y - 40,
          [('绿格 = 要算的格子，它自己是 "1"', 'grn'),
           ('蓝框：以「上」为右下角的最大正方形', 'blue'), ('橙框：以「左」为右下角的最大正方形', 'org'),
           ('紫框：以「左上」为右下角的最大正方形', 'pur'),
           ('绿虚线：以这一格为右下角能得到的最大正方形', 'grn'),
           '三个邻居里最小的是 k：蓝、橙、紫三个框里都有 k × k，',
           '再加上绿格自己，正好拼出 (k + 1) × (k + 1)，',
           ('所以 dp = min(上, 左, 左上) + 1', INK)], gap=25)
    s.save('lcr-square-why')


def rolling():
    m, n = 3, 7
    full = [[1] * n for _ in range(m)]
    for r in range(1, m):
        for c in range(1, n):
            full[r][c] = full[r - 1][c] + full[r][c - 1]
    r, c = 2, 3
    dp = [1] * n
    for rr in range(1, m):
        for cc in range(1, n):
            if (rr, cc) == (r, c):
                snapshot = dp[:]
            dp[cc] = dp[cc] + dp[cc - 1]
    assert dp == full[m - 1] and snapshot == full[r][:c] + full[r - 1][c:]
    s = S()
    X, Y, cw = 150, 44, 56
    label(s, Y + cw * 0.3, '二维的 dp')
    headers(s, X, Y, m, n, cw)
    grid(s, X, Y, [[full[i][j] if (i < r or (i == r and j < c)) else '?' if (i, j) == (r, c) else '' for j in range(n)]
                   for i in range(m)],
         lambda i, j: 'hit' if (i, j) == (r, c) else 'new' if (i == r and j < c) else 'pur' if (i == r - 1 and j >= c)
         else 'off', cw=cw, size=15)
    reads(s, X, Y, r, c, cw=cw)
    y2 = Y + m * cw + 44
    label(s, y2 + 6, '只留一行的 dp')
    grid(s, X, y2, [snapshot], lambda i, j: 'new' if j < c else 'pur', cw=cw, size=15)
    outline(s, X + c * cw - 4, y2 - 4, cw + 5, cw + 5, 'grn')
    s.text(X + c * cw / 2, y2 + cw + 14, '新值（这一行刚算的）', 13, COL['org'], bold=True)
    s.text(X + c * cw + (n - c) * cw / 2, y2 + cw + 14, '旧值（上一行留下的，还没更新）', 13, '#7C3AED', bold=True)
    lines(s, X + n * cw + 30, Y + 4,
          [(f'正要算第 {r} 行第 {c} 列（绿）', 'grn'),
           (f'左 = dp[col − 1] = {snapshot[c - 1]}：这一行刚算好的', 'org'),
           (f'上 = dp[col] = {snapshot[c]}：还是上一行留下的', '#7C3AED'),
           ('dp[col] = dp[col] + dp[col − 1]', INK),
           f'        = {snapshot[c]} + {snapshot[c - 1]} = {full[r][c]}',
           '算完后 dp[col] 就从旧值变成了新值',
           '再往上的行（灰）以后用不到，不用留'], gap=25)
    s.save('lcr-rolling')


if __name__ == '__main__':
    climb_tree('lcr-climb-tree', False)
    climb_tree('lcr-climb-memo', True)
    for f in (climb_table, climb_split, cost_trace, two_states, rob_trace, rob_circle, kadane_trace, lis_trace, lis_tails,
              word_break, decode_trace, grid_idea, paths_62, paths_63, minpath_64, triangle_120, square_221, square_why,
              rolling):
        f()
    print('ok')
