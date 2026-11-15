#!/usr/bin/env python3
"""Diagrams for 状态机 DP（股票）/ 区间 DP / 树形 DP in 常用代码模板5 (files lcu-*.svg / lcu-*.png).

Run from this directory:  python3 lc_u.py
"""
from make_diagrams import *  # noqa: F401,F403
from make_diagrams_algo import inf, row  # also registers the 'pur' style

INF = float('inf')


# ---------- shared pieces ----------

def lines(s, x, y, ts, size=13.5, gap=22, color=INK):
    """Like make_diagrams_algo.lines, but leading spaces become a real indent (SVG drops them)."""
    for k, t in enumerate(ts):
        col, bold = color, False
        if isinstance(t, tuple):
            col, bold = COL.get(t[1], t[1]), (t[2] if len(t) > 2 else True)
            t = t[0]
        body = t.lstrip(' ')
        s.text(x + (len(t) - len(body)) * size * 0.45, y + k * gap, body, size, col, 'start', bold=bold)


def box(s, cx, cy, t, st='n', w=120, h=44, sub=None):
    """A state box centred at (cx, cy)."""
    f, k, c, d = ST[st]
    s.rect(cx - w / 2, cy - h / 2, w, h, f, k, d)
    if sub:
        s.text(cx, cy - 8, t, 14.5, c, bold=True)
        s.text(cx, cy + 11, sub, 12, SUB, mono=True)
    else:
        s.text(cx, cy, t, 14.5, c, bold=True)


def loop(s, cx, top, label, color='gry', up=True):
    """Self-loop above (or below) a box whose edge is at y = top."""
    col = COL[color]
    k = -1 if up else 1
    x1, x2, y = cx - 20, cx + 20, top + k * 3
    s.e.append(f'<path d="M{x1},{y} C{x1 - 16},{y + k * 40} {x2 + 16},{y + k * 40} {x2 + 2},{y + k * 7}" fill="none" '
               f'stroke="{col}" stroke-width="1.8" stroke-linecap="round"/>')
    s.tip(x2, y, math.atan2(-k * 40, -16) + math.pi, col)
    s.b(x2 + 20, y + (40 if not up else 0))
    s.text(cx, y + k * 42, label, 13, col, bold=True)


def dp_table(s, x, y, data, st, col_heads=None, row_heads=None, cw=50, ch=34, size=14, head_size=12.5, gap=3):
    """Grid with optional headers. st(i, j) -> style or None (cell not drawn). Returns centre(i, j)."""
    for j, h in enumerate(col_heads or []):
        s.text(x + j * cw + (cw - gap) / 2, y - 13, h, head_size, SUB, mono=True)
    for i, h in enumerate(row_heads or []):
        s.text(x - 10, y + i * ch + (ch - gap) / 2, h, head_size, SUB, 'end', mono=True)
    for i, r in enumerate(data):
        for j, v in enumerate(r):
            style = st(i, j)
            if style:
                s.node(x + j * cw, y + i * ch, v, style, w=cw - gap, h=ch - gap, size=size)

    def centre(i, j):
        return x + j * cw + (cw - gap) / 2, y + i * ch + (ch - gap) / 2
    centre.half = ((cw - gap) / 2, (ch - gap) / 2)
    return centre


def link(s, centre, src, dst, color='red'):
    """Arrow from the border of cell src to the border of cell dst (cells given as (i, j))."""
    (x1, y1), (x2, y2) = centre(*src), centre(*dst)
    hw, hh = centre.half
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    reach = min(hw / abs(ux) if ux else INF, hh / abs(uy) if uy else INF) + 1
    if L - 2 * reach < 30:                         # 对角相邻的格子：让箭头伸进格子里一点，否则太短
        reach = (L - 34) / 2
    s.arrow(x1 + ux * reach, y1 + uy * reach, x2 - ux * reach, y2 - uy * reach, color)


def num(v):
    return inf(v)


# ---------- 状态机 DP：股票 ----------

def stock_machine():
    s = S()
    s.text(LX, 18, 'LC 122：每天结束时处在两个状态之一，箭头是「从昨天到今天」能怎么走', 14.5, INK, 'start', bold=True)
    ax, bx, cy = 190, 560, 150
    box(s, ax, cy, '没有股票', 'n', w=140, h=50, sub='dp[i][0]')
    box(s, bx, cy, '有股票', 'new', w=140, h=50, sub='dp[i][1]')
    s.curve(ax + 74, cy - 14, bx - 74, cy - 14, -28, 'red', label='买入：利润 − prices[i]')
    s.curve(bx - 74, cy + 14, ax + 74, cy + 14, 28, 'grn', label='卖出：利润 + prices[i]')
    loop(s, ax, cy - 25, '不动')
    loop(s, bx, cy - 25, '不动')
    lines(s, LX, 232, [
        ('指向「没有股票」的箭头有两条 → dp[i][0] = max(dp[i−1][0], dp[i−1][1] + prices[i])', 'grn'),
        ('指向「有股票」的箭头有两条   → dp[i][1] = max(dp[i−1][1], dp[i−1][0] − prices[i])', 'red')], size=13.5, gap=26)
    s.save('lcu-stock-machine')


def stock_122_trace():
    prices = [7, 1, 5, 3, 6, 4]
    n = len(prices)
    dp = [[0, 0] for _ in range(n)]
    dp[0][1] = -prices[0]
    for i in range(1, n):
        dp[i][0] = max(dp[i - 1][0], dp[i - 1][1] + prices[i])
        dp[i][1] = max(dp[i - 1][1], dp[i - 1][0] - prices[i])
    assert dp[n - 1][0] == 7
    s = S()
    s.text(LX, 18, 'prices = [7, 1, 5, 3, 6, 4]：每一行是一天，每一格只用上一行的两格', 14.5, INK, 'start', bold=True)
    X, Y, cw, ch = 96, 74, 104, 52
    data = [[prices[i], num(dp[i][0]), num(dp[i][1])] for i in range(n)]

    def st(i, j):
        if j == 0:
            return 'sent'
        if (i, j) == (4, 1):
            return 'chg'
        if (i, j) in ((3, 1), (3, 2)):
            return 'new'
        if (i, j) == (n - 1, 1):
            return 'hit'
        return 'n' if i else 'off'
    centre = dp_table(s, X, Y, data, st, ['prices[i]', 'dp[i][0] 没有', 'dp[i][1] 有'], [f'i = {i}' for i in range(n)],
                      cw=cw, ch=ch, gap=20)
    link(s, centre, (3, 1), (4, 1), 'red')
    link(s, centre, (3, 2), (4, 1), 'red')
    tx = X + 3 * cw + 30
    i = 4
    a, b = dp[i - 1][0], dp[i - 1][1] + prices[i]
    lines(s, tx, Y + 8, [
        ('第 0 行直接填：0 和 −prices[0] = −7', SUB, False),
        (f'红色那一格 dp[{i}][0]：', 'red'),
        (f'    昨天就没有，不动      dp[{i - 1}][0] = {a}', INK, False),
        (f'    昨天有，今天卖出      dp[{i - 1}][1] + {prices[i]} = {dp[i - 1][1]} + {prices[i]} = {b}', INK, False),
        (f'    取大的：{max(a, b)}', 'red'),
        ('橙色：它读的两格，都在上一行', 'org'),
        (f'绿色：答案 dp[{n - 1}][0] = {dp[n - 1][0]}', 'grn')], gap=27)
    s.save('lcu-stock-122-trace')


def stock_121():
    prices = [7, 1, 5, 3, 6, 4]
    lows, gains, bests = [], [], []
    min_price, best = prices[0], 0
    for price in prices:
        best = max(best, price - min_price)
        gains.append(price - min_price)
        min_price = min(min_price, price)
        lows.append(min_price)
        bests.append(best)
    assert best == 5
    s = S()
    s.text(LX, 18, 'LC 121：从左到右走一遍，记住见过的最低价；今天卖出能赚「今天的价 − 之前的最低价」', 14.5, INK, 'start', bold=True)
    X, cw = 250, 58
    rows = [('prices', prices, lambda i: 'new' if i == 1 else 'hit' if i == 4 else 'n'),
            ('min_price（走完这一天之后）', lows, lambda i: 'new' if i >= 1 else 'off'),
            ('price − 进入时的 min_price', gains, lambda i: 'hit' if i == 4 else 'off'),
            ('best', bests, lambda i: 'hit' if i >= 4 else 'off')]
    y = 62
    for k, (name, vals, st) in enumerate(rows):
        s.text(LX, y + 17, name, 13.5, INK, 'start', bold=True, mono=k != 1 and k != 2)
        row(s, X, y, [num(v) for v in vals], [st(i) for i in range(len(vals))], cw=cw, idx='top' if k == 0 else None)
        y += 50
    s.text(LX, y + 14, '第 1 天价格 1 是最低价（橙），第 4 天价格 6 卖出（绿）：6 − 1 = 5', 13.5, COL['grn'], 'start', bold=True)
    s.text(LX, y + 38, 'min_price 就是状态机里的 −dp[i][1]，best 就是 dp[i][0]', 13.5, SUB, 'start')
    s.save('lcu-stock-121')


def stock_variants():
    s = S()
    W = 470
    # panel 1: LC 121
    ox, oy = 18, 14
    s.text(ox, oy + 10, 'LC 121 只能一笔：一条链，不能回头', 14.5, INK, 'start', bold=True)
    y = oy + 100
    xs = [ox + 62, ox + 222, ox + 382]
    box(s, xs[0], y, '还没买过', 'off', w=104, sub='利润恒为 0')
    box(s, xs[1], y, '有股票', 'new', w=104, sub='dp[i][1]')
    box(s, xs[2], y, '已经卖掉', 'n', w=104, sub='dp[i][0]')
    s.arrow(xs[0] + 55, y, xs[1] - 55, y, 'red')
    s.text((xs[0] + xs[1]) / 2, y - 15, '买入', 13, COL['red'], bold=True)
    s.text((xs[0] + xs[1]) / 2, y + 40, '0 − prices[i]', 12, COL['red'], mono=True)
    s.arrow(xs[1] + 55, y, xs[2] - 55, y, 'grn')
    s.text((xs[1] + xs[2]) / 2, y - 15, '卖出', 13, COL['grn'], bold=True)
    s.text((xs[1] + xs[2]) / 2, y + 40, '+ prices[i]', 12, COL['grn'], mono=True)
    for x in xs[1:]:
        loop(s, x, y - 22, '不动')
    # panel 2: LC 309
    ox = 18 + W + 30
    s.seg(ox - 18, oy, ox - 18, oy + 170, '#E5E7EB', sw=1)
    s.text(ox, oy + 10, 'LC 309 冷冻期：卖出后先进「今天刚卖出」', 14.5, INK, 'start', bold=True)
    xs = [ox + 62, ox + 232, ox + 402]
    box(s, xs[0], y, '没有，能买', 'n', w=104, sub='dp[i][0]')
    box(s, xs[1], y, '有股票', 'new', w=104, sub='dp[i][1]')
    box(s, xs[2], y, '今天刚卖出', 'chg', w=110, sub='dp[i][2]')
    s.arrow(xs[0] + 55, y, xs[1] - 55, y, 'red')
    s.text((xs[0] + xs[1]) / 2, y - 15, '买入', 13, COL['red'], bold=True)
    s.arrow(xs[1] + 55, y, xs[2] - 58, y, 'grn')
    s.text((xs[1] + xs[2]) / 2, y - 15, '卖出', 13, COL['grn'], bold=True)
    s.curve(xs[2], y + 24, xs[0], y + 24, 26, 'blue', label='过一天，冷冻期结束')
    loop(s, xs[0], y - 22, '不动')
    loop(s, xs[1], y - 22, '不动')
    s.text(xs[2], y - 40, '没有「不动」，也不能买', 12.5, COL['red'], bold=True)
    # panel 3: LC 714
    ox, oy2 = 18, 14 + 200
    s.seg(18, oy2 - 14, 18 + 2 * W + 30, oy2 - 14, '#E5E7EB', sw=1)
    s.text(ox, oy2 + 10, 'LC 714 手续费：状态和箭头不变，卖出那条多扣 fee', 14.5, INK, 'start', bold=True)
    y2 = oy2 + 100
    ax, bx = ox + 90, ox + 370
    box(s, ax, y2, '没有股票', 'n', w=110, sub='dp[i][0]')
    box(s, bx, y2, '有股票', 'new', w=110, sub='dp[i][1]')
    s.curve(ax + 58, y2 - 12, bx - 58, y2 - 12, -20, 'red', label='买入 − prices[i]')
    s.curve(bx - 58, y2 + 12, ax + 58, y2 + 12, 20, 'grn', label='卖出 + prices[i] − fee')
    loop(s, ax, y2 - 22, '不动')
    loop(s, bx, y2 - 22, '不动')
    # panel 4: LC 123
    ox = 18 + W + 30
    s.seg(ox - 18, oy2, ox - 18, oy2 + 170, '#E5E7EB', sw=1)
    s.text(ox, oy2 + 10, 'LC 123 最多两笔：五个状态排成一条链', 14.5, INK, 'start', bold=True)
    names = [('还没买', 'off'), ('第1次持有', 'new'), ('第1次卖出', 'n'), ('第2次持有', 'new'), ('第2次卖出', 'hit')]
    bw, step = 80, 96
    for k, (t, st) in enumerate(names):
        cx = ox + 40 + k * step
        box(s, cx, y2, t, st, w=bw, h=46, sub=f'状态 {k}')
        if k:
            col = 'red' if k % 2 else 'grn'
            s.arrow(cx - step + bw / 2 + 2, y2, cx - bw / 2 - 2, y2, col)
            s.text(cx - step / 2, y2 - 34, '买' if k % 2 else '卖', 13, COL[col], bold=True)
    s.text(ox, y2 + 46, '每个状态还有一条指向自己的「不动」；奇数状态是持有，偶数状态是没有', 12.5, SUB, 'start')
    s.save('lcu-stock-variants')


def stock_309_trace():
    prices = [1, 2, 3, 0, 2]
    n = len(prices)
    dp = [[0, 0, 0] for _ in range(n)]
    dp[0][1] = -prices[0]
    for i in range(1, n):
        dp[i][0] = max(dp[i - 1][0], dp[i - 1][2])
        dp[i][1] = max(dp[i - 1][1], dp[i - 1][0] - prices[i])
        dp[i][2] = dp[i - 1][1] + prices[i]
    assert max(dp[n - 1][0], dp[n - 1][2]) == 3
    s = S()
    s.text(LX, 18, 'prices = [1, 2, 3, 0, 2]：三个状态，三列', 14.5, INK, 'start', bold=True)
    X, Y, cw, ch = 96, 74, 116, 52
    data = [[prices[i]] + [num(v) for v in dp[i]] for i in range(n)]

    def st(i, j):
        if j == 0:
            return 'sent'
        if (i, j) == (3, 2):
            return 'chg'
        if (i, j) in ((2, 1), (2, 2)):
            return 'new'
        if (i, j) == (2, 3):
            return 'del'
        if i == n - 1 and j in (1, 3):
            return 'hit'
        return 'n' if i else 'off'
    centre = dp_table(s, X, Y, data, st, ['prices[i]', 'dp[i][0] 能买', 'dp[i][1] 有', 'dp[i][2] 今天卖出'],
                      [f'i = {i}' for i in range(n)], cw=cw, ch=ch, gap=20)
    link(s, centre, (2, 1), (3, 2), 'red')
    link(s, centre, (2, 2), (3, 2), 'red')
    tx = X + 4 * cw + 30
    a, b = dp[2][1], dp[2][0] - prices[3]
    lines(s, tx, Y + 8, [
        ('红色那一格 dp[3][1]（第 3 天结束时有股票）：', 'red'),
        (f'    昨天就有，不动        dp[2][1] = {num(a)}', INK, False),
        (f'    昨天「能买」，今天买入  dp[2][0] − {prices[3]} = {dp[2][0]} − {prices[3]} = {b}', INK, False),
        (f'    取大的：{max(a, b)}', 'red'),
        (f'灰色虚线 dp[2][2] = {dp[2][2]}：第 2 天刚卖出，第 3 天不能买，这一格不读它', SUB, True),
        (f'绿色：答案 max(dp[{n - 1}][0], dp[{n - 1}][2]) = max({dp[n - 1][0]}, {dp[n - 1][2]}) = 3', 'grn')], gap=27)
    s.save('lcu-stock-309-trace')


def stock_123_trace():
    prices = [3, 3, 5, 0, 0, 3, 1, 4]
    n, k = len(prices), 2
    dp = [[0] * (2 * k + 1) for _ in range(n)]
    for state in range(1, 2 * k + 1, 2):
        dp[0][state] = -prices[0]
    for i in range(1, n):
        for state in range(1, 2 * k + 1):
            if state % 2 == 1:
                dp[i][state] = max(dp[i - 1][state], dp[i - 1][state - 1] - prices[i])
            else:
                dp[i][state] = max(dp[i - 1][state], dp[i - 1][state - 1] + prices[i])
    assert dp[n - 1][2 * k] == 6
    s = S()
    s.text(LX, 18, 'prices = [3, 3, 5, 0, 0, 3, 1, 4]：每一格读正上方（不动）和左上方（买或卖一次）', 14.5, INK, 'start', bold=True)
    X, Y, cw, ch = 96, 90, 96, 50
    data = [[prices[i]] + [num(v) for v in dp[i]] for i in range(n)]

    def st(i, j):
        if j == 0:
            return 'sent'
        if (i, j) == (5, 5):
            return 'chg'
        if (i, j) in ((4, 5), (4, 4)):
            return 'new'
        if (i, j) == (n - 1, 5):
            return 'hit'
        return 'n' if i and j > 1 else 'off'
    centre = dp_table(s, X, Y, data, st, ['prices[i]', '状态 0', '状态 1', '状态 2', '状态 3', '状态 4'],
                      [f'i = {i}' for i in range(n)], cw=cw, ch=ch, gap=20)
    for j, t in enumerate(['还没买', '第1次持有', '第1次卖出', '第2次持有', '第2次卖出']):
        s.text(X + (j + 1) * cw + (cw - 20) / 2, Y - 30, t, 12, COL['org'] if j % 2 else SUB, bold=True)
    link(s, centre, (4, 5), (5, 5), 'red')
    link(s, centre, (4, 4), (5, 5), 'red')
    tx = X + 6 * cw + 26
    a, b = dp[4][4], dp[4][3] + prices[5]
    lines(s, tx, Y + 8, [
        ('红色那一格 dp[5][4]：', 'red'),
        (f'    正上方，不动    dp[4][4] = {a}', INK, False),
        (f'    左上方，今天卖  dp[4][3] + {prices[5]} = {dp[4][3]} + {prices[5]} = {b}', INK, False),
        (f'    取大的：{max(a, b)}', 'red'),
        ('状态 0 那一列一直是 0', SUB, False),
        (f'绿色：答案 dp[{n - 1}][4] = {dp[n - 1][4]}', 'grn')], gap=27)
    s.save('lcu-stock-123-trace')


# ---------- 区间 DP ----------

BAND = {1: 'sent', 2: 'n', 3: 'pur', 4: 'new', 5: 'hit'}


def interval_order():
    n = 5
    s = S()
    s.text(LX, 18, '行是 left，列是 right。格子里的数是区间长度，同一条斜线长度相同', 14.5, INK, 'start', bold=True)
    X, Y, cw = 80, 86, 62
    data = [[(j - i + 1 if j >= i else '') for j in range(n)] for i in range(n)]
    dp_table(s, X, Y, data, lambda i, j: BAND[j - i + 1] if j >= i else None, [f'right={j}' for j in range(n)],
             [f'left={i}' for i in range(n)], cw=cw, ch=cw, size=15, head_size=11, gap=12)
    s.text(LX, Y + n * cw + 14, '填表顺序：长度 1 → 2 → 3 → 4 → 5，一条斜线一条斜线往右上走', 13.5, INK, 'start', bold=True)
    # right panel: what one cell reads
    X2 = X + n * cw + 170
    s.text(X2 - 62, 50, '一格读哪些格子：以 dp[1][4] 为例', 14.5, INK, 'start', bold=True)
    target = (1, 4)

    def st(i, j):
        if j < i:
            return None
        if (i, j) == target:
            return 'chg'
        if i == target[0] and j < target[1]:
            return 'new'
        if j == target[1] and i > target[0]:
            return 'hit'
        if (i, j) == (target[0] + 1, target[1] - 1):
            return 'pur'
        return 'off'
    labels = [[(f'{i},{j}' if j >= i else '') for j in range(n)] for i in range(n)]
    dp_table(s, X2, Y, labels, st, [f'right={j}' for j in range(n)], [f'left={i}' for i in range(n)], cw=cw, ch=cw,
             size=13, head_size=11, gap=12)
    tx = X2 + n * cw + 24
    lines(s, tx, Y + 10, [
        ('红：正在算的 dp[1][4]', 'red'),
        ('橙：同一行左边，左端点相同、更短', 'org'),
        ('    dp[1][1]  dp[1][2]  dp[1][3]', INK, False),
        ('绿：同一列下边，右端点相同、更短', 'grn'),
        ('    dp[2][4]  dp[3][4]  dp[4][4]', INK, False),
        ('紫：左下角 dp[2][3]，两头各缩一格', 'pur'),
        ('这些格子的长度都比 4 小，已经填好', INK)], gap=27)
    s.save('lcu-interval-order')


def stones_table(stones):
    n = len(stones)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + stones[i]
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            best = INF
            for split in range(left, right):
                best = min(best, dp[left][split] + dp[split + 1][right])
            dp[left][right] = best + prefix[right + 1] - prefix[left]
    return dp


def interval_stones():
    stones = [1, 3, 5, 2]
    n = len(stones)
    dp = stones_table(stones)
    assert dp[0][n - 1] == 22
    s = S()
    s.text(LX, 18, 'stones = [1, 3, 5, 2] 的 dp 表', 14.5, INK, 'start', bold=True)
    X, Y, cw = 80, 76, 62

    def st(i, j):
        if j < i:
            return None
        if (i, j) == (0, n - 1):
            return 'chg'
        return BAND[j - i + 1]
    dp_table(s, X, Y, [[(dp[i][j] if j >= i else '') for j in range(n)] for i in range(n)], st,
             [f'right={j}' for j in range(n)], [f'left={i}' for i in range(n)], cw=cw, ch=cw, size=15, head_size=11, gap=12)
    s.text(X, Y + n * cw + 10, '灰：长度 1　蓝：长度 2　紫：长度 3　红：dp[0][3]，答案', 12.5, SUB, 'start')
    # right: the three splits of dp[0][3]
    X2 = X + n * cw + 70
    s.text(X2, 18, 'dp[0][3]：最后一次合并从哪里分开（split 是左半段的最后一堆）', 14.5, INK, 'start', bold=True)
    total = sum(stones)
    y = 58
    best = min(dp[0][sp] + dp[sp + 1][n - 1] for sp in range(n - 1))
    for sp in range(n - 1):
        cand = dp[0][sp] + dp[sp + 1][n - 1]
        good = cand == best
        s.text(X2, y + 17, f'split = {sp}', 13.5, INK, 'start', bold=True, mono=True)
        cx = row(s, X2 + 92, y, stones[:sp + 1], 'n', cw=40)
        cx2 = row(s, X2 + 92 + (sp + 1) * 40 + 22, y, stones[sp + 1:], 'new', cw=40)
        s.text(X2 + 92 + (sp + 1) * 40 + 9, y + 17, '|', 18, COL['red'], bold=True)
        s.text(X2 + 300, y + 17,
               f'dp[0][{sp}] + dp[{sp + 1}][3] = {dp[0][sp]} + {dp[sp + 1][n - 1]} = {cand}', 13.5,
               COL['grn'] if good else INK, 'start', bold=good, mono=True)
        if good:
            s.text(X2 + 590, y + 17, '最小', 13.5, COL['grn'], 'start', bold=True)
        y += 50
    s.text(X2, y + 14, f'dp[0][3] = {best} + 整段的总重量 {total} = {best + total}', 14, COL['red'], 'start', bold=True)
    s.text(X2, y + 40, '不管从哪里分，最后一次合并的代价都是整段的总重量', 13, SUB, 'start')
    s.save('lcu-interval-stones')


def interval_expand():
    s = S()
    s.text(LX, 18, '中心扩展：从中心出发，两边字符相同就各往外走一格', 14.5, INK, 'start', bold=True)
    cw = 46

    def panel(x, y, text, left, right, title):
        n = len(text)
        steps = []
        a, b = left, right
        while a >= 0 and b < n and text[a] == text[b]:
            steps.append((a, b))
            a -= 1
            b += 1
        lo, hi = a + 1, b - 1
        s.text(x, y, title, 13.5, INK, 'start', bold=True)
        sts = ['hit' if lo <= i <= hi else 'off' for i in range(n)]
        for i in range(left, right + 1):
            if lo <= i <= hi:
                sts[i] = 'new'
        cs = row(s, x, y + 34, list(text), sts, cw=cw, idx='top')
        yb = y + 34 + 34
        for k, (p, q) in enumerate(steps[1:], 1):
            s.text(cs[p], yb + 14, f'第{k}步', 11.5, COL['grn'], bold=True)
            s.text(cs[q], yb + 14, f'第{k}步', 11.5, COL['grn'], bold=True)
        why = '出界' if a < 0 or b >= n else f'{text[a]} ≠ {text[b]}'
        s.text(x, yb + 40, f'停下时 left = {a}，right = {b}（{why}）', 12.5, SUB, 'start')
        s.text(x, yb + 62, f'回文是 s[{lo}..{hi}] = "{text[lo:hi + 1]}"，长度 {b} − ({a}) − 1 = {b - a - 1}', 12.5,
               COL['grn'], 'start', bold=True)
        return text[lo:hi + 1]

    assert panel(LX, 56, 'babad', 1, 1, '奇数长度：s = "babad"，从 (1, 1) 出发') == 'bab'
    assert panel(LX + 420, 56, 'cbbd', 1, 2, '偶数长度：s = "cbbd"，从 (1, 2) 出发') == 'bb'
    s.text(LX, 232, '橙：出发时的中心　绿：扩出来的回文', 12.5, SUB, 'start')
    s.save('lcu-interval-expand')


def interval_palin():
    text = 'babad'
    n = len(text)
    dp = [[False] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = True
    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            if text[left] == text[right] and (length == 2 or dp[left + 1][right - 1]):
                dp[left][right] = True
    assert dp[0][2] and dp[1][3] and not dp[0][4]
    s = S()
    s.text(LX, 18, 's = "babad"：dp[left][right] 是不是回文。每一格看两头的字符和左下角那一格', 14.5, INK, 'start', bold=True)
    X, Y, cw = 80, 76, 62

    def st(i, j):
        if j < i:
            return None
        if (i, j) == (0, 2):
            return 'chg'
        if (i, j) == (1, 1):
            return 'pur'
        if (i, j) == (0, 4):
            return 'new'
        return 'hit' if dp[i][j] else 'off'
    centre = dp_table(s, X, Y, [[('T' if dp[i][j] else '') if j >= i else '' for j in range(n)] for i in range(n)], st,
                      [f'{j} {text[j]}' for j in range(n)], [f'{i} {text[i]}' for i in range(n)], cw=cw, ch=cw, size=15, gap=12)
    link(s, centre, (1, 1), (0, 2), 'red')
    tx = X + n * cw + 30
    lines(s, tx, Y + 6, [
        ('红：dp[0][2]，子串 "bab"', 'red'),
        ('    s[0] == s[2]（都是 b）', INK, False),
        ('    左下角 dp[1][1]（紫）是 True', INK, False),
        ('    所以 dp[0][2] = True', 'red'),
        ('橙：dp[0][4]，子串 "babad"', 'org'),
        ('    s[0] = b，s[4] = d，不同，直接 False', INK, False),
        ('绿：其余是 True 的格子（都是回文）', 'grn')], gap=27)
    s.save('lcu-interval-palin')


def interval_516():
    text = 'bbbab'
    n = len(text)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1
    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            if text[left] == text[right]:
                dp[left][right] = dp[left + 1][right - 1] + 2
            else:
                dp[left][right] = max(dp[left + 1][right], dp[left][right - 1])
    assert dp[0][n - 1] == 4
    s = S()
    s.text(LX, 18, 's = "bbbab"：dp[left][right] 是这一段里最长回文子序列的长度', 14.5, INK, 'start', bold=True)
    X, Y, cw = 80, 76, 62

    def st(i, j):
        if j < i:
            return None
        if (i, j) == (0, 4):
            return 'chg'
        if (i, j) == (1, 3):
            return 'pur'
        if (i, j) == (0, 3):
            return 'new'
        if (i, j) in ((0, 2),):
            return 'hit'
        return 'n' if i != j else 'sent'
    centre = dp_table(s, X, Y, [[(dp[i][j] if j >= i else '') for j in range(n)] for i in range(n)], st,
                      [f'{j} {text[j]}' for j in range(n)], [f'{i} {text[i]}' for i in range(n)], cw=cw, ch=cw, size=15, gap=12)
    link(s, centre, (1, 3), (0, 4), 'red')
    link(s, centre, (1, 3), (0, 3), 'org')
    link(s, centre, (0, 2), (0, 3), 'org')
    tx = X + n * cw + 30
    lines(s, tx, Y + 6, [
        ('红：dp[0][4]，两头 s[0] = s[4] = b，相同', 'red'),
        (f'    左下角 dp[1][3]（紫）+ 2 = {dp[1][3]} + 2 = {dp[0][4]}', INK, False),
        ('橙：dp[0][3]，两头 s[0] = b，s[3] = a，不同', 'org'),
        (f'    丢掉左头：下边 dp[1][3] = {dp[1][3]}', INK, False),
        (f'    丢掉右头：左边 dp[0][2] = {dp[0][2]}（绿）', INK, False),
        (f'    取大的：{dp[0][3]}', 'org'),
        (f'答案在右上角：dp[0][4] = {dp[0][4]}', INK)], gap=27)
    s.save('lcu-interval-516')


def interval_312():
    nums = [3, 1, 5, 8]
    values = [1] + nums + [1]
    m = len(values)
    dp = [[0] * m for _ in range(m)]
    for length in range(2, m):
        for left in range(m - length):
            right = left + length
            best = 0
            for last in range(left + 1, right):
                best = max(best, dp[left][last] + dp[last][right] + values[left] * values[last] * values[right])
            dp[left][right] = best
    assert dp[0][m - 1] == 167
    left, right, last = 0, 5, 3
    s = S()
    s.text(LX, 18, 'nums = [3, 1, 5, 8]，两头补 1。算 dp[0][5]，假设最后戳破的是下标 3（数字 5）', 14.5, INK, 'start', bold=True)
    X, Y, cw = 60, 76, 62
    sts = ['sent', 'n', 'n', 'chg', 'new', 'sent']
    cs = row(s, X, Y, values, sts, cw=cw, idx='top')
    s.text(cs[0], Y + 50, 'left', 13, SUB, bold=True, mono=True)
    s.text(cs[5], Y + 50, 'right', 13, SUB, bold=True, mono=True)
    s.text(cs[3], Y + 50, 'last', 13, COL['red'], bold=True, mono=True)
    brace(s, cs[1] - 24, cs[2] + 24, Y + 72, f'先戳完：dp[0][3] = {dp[0][3]}', 'blue', up=False)
    brace(s, cs[4] - 24, cs[4] + 24, Y + 72, f'先戳完：dp[3][5] = {dp[3][5]}', 'org', up=False)
    y = Y + 128
    gain = values[left] * values[last] * values[right]
    lines(s, LX, y, [
        ('last 被戳之前一直在那里，把左边（蓝）和右边（橙）隔开：两边互不影响，各自是一个更短的区间', INK),
        (f'轮到 last 时，中间别的气球都没了，它的邻居是 left 和 right：得 {values[left]} × {values[last]} × {values[right]} = {gain}', 'red'),
        (f'这种选法一共 dp[0][3] + dp[3][5] + {gain} = {dp[0][3]} + {dp[3][5]} + {gain} = {dp[0][3] + dp[3][5] + gain}', INK),
        (f'last 取 1、2、3、4 各算一次，最大的是 last = 4（数字 8 留到最后）：{dp[0][4]} + {dp[4][5]} + 8 = {dp[0][5]}', 'grn')],
          gap=27)
    assert dp[0][4] + dp[4][5] + 8 == dp[0][5]
    s.save('lcu-interval-312')


# ---------- 树形 DP ----------

def tree_337():
    # root = [3, 2, 3, null, 3, null, 1]
    kids = {'a': ('b', 'c'), 'b': (None, 'd'), 'c': (None, 'e'), 'd': (None, None), 'e': (None, None)}
    val = {'a': 3, 'b': 2, 'c': 3, 'd': 3, 'e': 1}
    info = {}

    def dfs(node):
        if node is None:
            return 0, 0
        left_skip, left_take = dfs(kids[node][0])
        right_skip, right_take = dfs(kids[node][1])
        info[node] = (max(left_skip, left_take) + max(right_skip, right_take), val[node] + left_skip + right_skip)
        return info[node]

    assert max(dfs('a')) == 7
    chosen = {'a', 'd', 'e'}
    pos = {'a': (170, 0), 'b': (80, 84), 'c': (260, 84), 'd': (130, 168), 'e': (310, 168)}
    nodes = {k: (x, y, val[k], 'hit' if k in chosen else 'n') for k, (x, y) in pos.items()}
    edges = [(a, b, '', 'line') for a, ks in kids.items() for b in ks if b]
    s = S()
    s.text(LX, 18, 'root = [3, 2, 3, null, 3, null, 1]：每个节点向上返回 (skip, take)', 14.5, INK, 'start', bold=True)
    ox, oy = 60, 76
    tree(s, ox, oy, nodes, edges)
    for k, (x, y) in pos.items():
        skip, take = info[k]
        side = -1 if k in ('b',) else 1
        s.text(ox + x + side * 26, oy + y, f'({skip}, {take})', 13.5, COL['red'], 'end' if side < 0 else 'start',
               bold=True, mono=True)
    tx = 470
    a = info['a']
    lines(s, tx, 70, [
        ('红色：dfs 返回的 (skip, take)', 'red'),
        ('    skip = 不偷这个节点时，子树最多偷多少', INK, False),
        ('    take = 偷这个节点时，子树最多偷多少', INK, False),
        (f'根：skip = max(3, 2) + max(1, 3) = {a[0]}', INK),
        (f'    take = 3 + 3 + 1 = {a[1]}', INK),
        (f'答案 max({a[0]}, {a[1]}) = {max(a)}：偷绿色的三间', 'grn')], gap=27)
    s.save('lcu-tree-337')


def tree_285():
    n = 7
    happy = {i: 1 for i in range(1, n + 1)}
    pairs = [(1, 3), (2, 3), (6, 4), (7, 4), (4, 5), (3, 5)]          # (employee, boss)
    children = {i: [] for i in range(1, n + 1)}
    for employee, boss in pairs:
        children[boss].append(employee)
    info = {}

    def dfs(node):
        skip, take = 0, happy[node]
        for child in children[node]:
            child_skip, child_take = dfs(child)
            skip += max(child_skip, child_take)
            take += child_skip
        info[node] = (skip, take)
        return skip, take

    assert max(dfs(5)) == 5
    chosen = {5, 1, 2, 6, 7}
    pos = {5: (210, 0), 4: (100, 84), 3: (320, 84), 6: (40, 168), 7: (160, 168), 1: (260, 168), 2: (380, 168)}
    nodes = {k: (x, y, k, 'hit' if k in chosen else 'n') for k, (x, y) in pos.items()}
    edges = [(boss, employee, '', 'line') for employee, boss in pairs]
    s = S()
    s.text(LX, 18, 'AcWing 285 的样例：7 个人，快乐指数都是 1。圆里是编号，红色是返回的 (skip, take)', 14.5, INK, 'start',
           bold=True)
    ox, oy = 50, 76
    tree(s, ox, oy, nodes, edges)
    for k, (x, y) in pos.items():
        skip, take = info[k]
        if y == 168:
            s.text(ox + x, oy + y + 34, f'({skip}, {take})', 13.5, COL['red'], bold=True, mono=True)
        else:
            s.text(ox + x + 26, oy + y - 6, f'({skip}, {take})', 13.5, COL['red'], 'start', bold=True, mono=True)
    tx = 540
    lines(s, tx, 70, [
        ('skip = 这个人不来时，他这棵子树的最大值', INK, False),
        ('take = 这个人来时的最大值', INK, False),
        ('3 号：skip = 1 + 1 = 2（两个下属都来）', INK),
        ('       take = 1 + 0 + 0 = 1（下属都不能来）', INK),
        (f'根 5 号：skip = 2 + 2 = {info[5][0]}，take = 1 + 2 + 2 = {info[5][1]}', INK),
        (f'答案 max({info[5][0]}, {info[5][1]}) = 5：绿色的五个人来', 'grn')], gap=27)
    s.save('lcu-tree-285')


def tree_968():
    # root = [0, 0, null, 0, 0]
    kids = {'A': ('B', None), 'B': ('C', 'D'), 'C': (None, None), 'D': (None, None)}
    info = {}

    def dfs(node):
        if node is None:
            return INF, 0, 0
        left_camera, left_covered, left_waiting = dfs(kids[node][0])
        right_camera, right_covered, right_waiting = dfs(kids[node][1])
        with_camera = 1 + min(left_camera, left_covered, left_waiting) + min(right_camera, right_covered, right_waiting)
        covered = min(left_camera + min(right_camera, right_covered), right_camera + min(left_camera, left_covered))
        waiting = left_covered + right_covered
        info[node] = (with_camera, covered, waiting)
        return info[node]

    with_camera, covered, _ = dfs('A')
    assert min(with_camera, covered) == 1
    pos = {'A': (190, 0), 'B': (120, 84), 'C': (50, 168), 'D': (190, 168)}
    nodes = {k: (x, y, k, 'new' if k == 'B' else 'n') for k, (x, y) in pos.items()}
    edges = [(a, b, '', 'line') for a, ks in kids.items() for b in ks if b]
    s = S()
    s.text(LX, 18, 'root = [0, 0, null, 0, 0]：每个节点返回 (with_camera, covered, waiting)', 14.5, INK, 'start', bold=True)
    ox, oy = 60, 76
    tree(s, ox, oy, nodes, edges)

    def fmt(t):
        return '(' + ', '.join(num(v) for v in t) + ')'
    for k, (x, y) in pos.items():
        if y == 168:
            s.text(ox + x, oy + y + 34, fmt(info[k]), 13.5, COL['red'], bold=True, mono=True)
        else:
            s.text(ox + x + 26, oy + y - 4, fmt(info[k]), 13.5, COL['red'], 'start', bold=True, mono=True)
    tx = 420
    lines(s, tx, 62, [
        ('三个数：这种状态下，子树里最少装几个摄像头', 'red'),
        ('    with_camera  这个节点装了', INK, False),
        ('    covered      没装，被某个孩子监控到', INK, False),
        ('    waiting      没装，孩子也没装，等父节点', INK, False),
        ('∞：这种状态不可能', SUB, False),
        (f'根 A：min(with_camera, covered) = min({info["A"][0]}, {info["A"][1]}) = 1', INK),
        ('对应：只在 B（橙）装一个，A、C、D 都被 B 监控到', 'org')], gap=27)
    s.save('lcu-tree-968')


if __name__ == '__main__':
    for f in (stock_machine, stock_122_trace, stock_121, stock_variants, stock_309_trace, stock_123_trace,
              interval_order, interval_stones, interval_expand, interval_palin, interval_516, interval_312,
              tree_337, tree_285, tree_968):
        f()
    print('ok')
