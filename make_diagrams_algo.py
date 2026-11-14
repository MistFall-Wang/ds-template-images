#!/usr/bin/env python3
"""Diagrams for 常用代码模板1——基础算法（Python版）.md  (files alg-*.svg / alg-*.png).

Run:  python3 make_diagrams_algo.py
Also holds the helpers shared with make_diagrams_graph.py.
"""
from make_diagrams import *  # noqa: F401,F403  (S, ST, COL, cells, table, ptr, legend, brace, ...)

ST['pur'] = ('#EDE9FE', '#7C3AED', INK, 0)
ST['wall'] = ('#374151', '#374151', '#FFFFFF', 0)
COL['pur'] = '#7C3AED'


# ---------- helpers ----------

def row(s, x, y, vals, st='n', cw=42, ch=34, size=15, idx=None, i0=0):
    """Fixed-width cells. Returns the x centre of every cell. idx: 'top' | 'bot' draws indices."""
    sts = [st] * len(vals) if isinstance(st, str) else st
    cs = []
    for i, v in enumerate(vals):
        s.node(x + i * cw, y, v, sts[i], w=cw - 3, h=ch, size=size)
        c = x + i * cw + (cw - 3) / 2
        cs.append(c)
        if idx == 'top':
            s.text(c, y - 11, i + i0, 12, SUB, mono=True)
        if idx == 'bot':
            s.text(c, y + ch + 11, i + i0, 12, SUB, mono=True)
    return cs


def marks(s, cs, y, ps):
    """Pointer labels under a row. ps: (label, cell index, colour); labels sharing a cell are stacked."""
    by = {}
    for label, i, col in ps:
        by.setdefault(i, []).append((label, col))
    for i, ls in by.items():
        s.arrow(cs[i], y + 22, cs[i], y + 4, ls[0][1])
        for k, (label, col) in enumerate(ls):
            s.text(cs[i], y + 33 + 16 * k, label, 13.5, COL[col], bold=True, mono=True)


def lines(s, x, y, ts, size=13.5, gap=22, color=INK):
    """Left-aligned text lines. Item: str or (str, colour[, bold])."""
    for k, t in enumerate(ts):
        col, bold = color, False
        if isinstance(t, tuple):
            col, bold = COL.get(t[1], t[1]), (t[2] if len(t) > 2 else True)
            t = t[0]
        s.text(x, y + k * gap, t, size, col, 'start', bold=bold)


def grid(s, x, y, data, st, cw=36, size=14):
    for i, r in enumerate(data):
        for j, v in enumerate(r):
            s.node(x + j * cw, y + i * cw, v, st(i, j) if callable(st) else st[i][j], w=cw - 3, h=cw - 3, size=size)


def panel_grid(name, n, pw, ph, draw, cols=None, titles=None, foot=None, leg=None):
    """n panels laid out in a grid; draw(s, ox, oy, k) paints panel k below its title."""
    s = S()
    cols = cols or n
    for k in range(n):
        ox, oy = 18 + (k % cols) * pw, 14 + (k // cols) * ph
        if k % cols:
            s.seg(ox - 14, oy, ox - 14, oy + ph - 26, '#E5E7EB', sw=1)
        if titles:
            s.text(ox, oy + 10, titles[k], 14.5, INK, 'start', bold=True)
        draw(s, ox, oy + 30, k)
    y = 14 + ((n - 1) // cols + 1) * ph - 10
    if leg:
        legend(s, 18, y, leg)
        y += 30
    if foot:
        s.text(18, y + 8, foot, 14, INK, 'start', bold=True)
    s.save(name)


def graph(s, ox, oy, pos, edges, st=None, tag=None, r=17, directed=True, names=None):
    """pos: {id: (x, y)}; edges: (a, b[, label[, colour[, opts]]]); tag: {id: (text, colour[, 't'|'b'|'l'|'r'])}."""
    st, tag = st or {}, tag or {}
    for e in edges:
        a, b = e[0], e[1]
        label = e[2] if len(e) > 2 else ''
        col = (e[3] if len(e) > 3 else None) or 'line'
        o = e[4] if len(e) > 4 else {}
        ax, ay, bx, by = ox + pos[a][0], oy + pos[a][1], ox + pos[b][0], oy + pos[b][1]
        dash = o.get('dash', 0)
        hot = col in ('grn', 'org', 'red')
        sw = o.get('sw', 3 if hot and not directed else 1.8)
        if 'bend' in o:
            sg, dy = (1 if bx > ax else -1), (r * 0.75 if o['bend'] > 0 else -r * 0.75)
            s.curve(ax + sg * r * 0.8, ay + dy, bx - sg * r * 0.8, by + dy, o['bend'], col, dash,
                    label if label != '' else None)
            continue
        L = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / L, (by - ay) / L
        p1, p2 = (ax + ux * (r + 2), ay + uy * (r + 2)), (bx - ux * (r + 3), by - uy * (r + 3))
        if directed:
            s.arrow(*p1, *p2, col, dash=dash, sw=sw)
        else:
            s.seg(*p1, *p2, col, dash=dash, sw=sw)
        if label != '':
            nx, ny = -uy, ux
            if ny > 0.3 or (abs(ny) <= 0.3 and nx < 0):
                nx, ny = -nx, -ny
            sd, t = o.get('side', 1), o.get('t', 0.5)
            s.text(ax + (bx - ax) * t + nx * 13 * sd, ay + (by - ay) * t + ny * 13 * sd, label, 14,
                   COL[col] if hot else INK, bold=True, mono=True)
    for v, (x, y) in pos.items():
        s.circ(ox + x, oy + y, names[v] if names else v, st.get(v, 'n'), r=r)
        if v in tag:
            t = tag[v]
            where = t[2] if len(t) > 2 else 't'
            dx, dy = {'t': (0, -r - 11), 'b': (0, r + 12), 'l': (-r - 6, 0), 'r': (r + 6, 0)}[where]
            s.text(ox + x + dx, oy + y + dy, t[0], 13.5, COL.get(t[1], t[1]),
                   {'l': 'end', 'r': 'start'}.get(where, 'middle'), bold=True, mono=True)


def blk(s, x, y, w, h, t, st, size=18):
    f, k, _, d = ST[st]
    s.rect(x, y, w - 3, h - 3, f, k, d)
    s.text(x + w / 2 - 1, y + h / 2 - 1, t, size, INK, bold=True)


def inf(v):
    return '∞' if v == float('inf') else str(v).replace('-', '−')


# ---------- 快速排序 ----------

def qs_regions():
    s = S()
    x, y, w, h = 40, 30, 150, 44
    for k, (t, st) in enumerate((('比 x 小', 'n'), ('等于 x', 'hit'), ('还没看', 'off'), ('比 x 大', 'new'))):
        blk(s, x + k * w, y, w, h, t, st, 15)
    for label, px, col in (('l', x + 16, 'gry'), ('lt', x + w + 16, 'blue'), ('i', x + 2 * w + 16, 'org'),
                           ('gt', x + 3 * w - 20, 'red'), ('r', x + 4 * w - 20, 'gry')):
        ptr(s, px, y + h, label, col)
    lines(s, x, y + h + 64, ['lt：下一个「比 x 小」的数该放的位置  ｜  i：正在看的数  ｜  gt：下一个「比 x 大」的数该放的位置'],
          color=SUB)
    s.save('alg-qs-regions')


def qs_trace():
    a, x = [4, 2, 5, 4, 1], 4
    lt, i, gt = 0, 0, 4
    states = [('开始：基准 x = 4', a[:], lt, i, gt)]
    while i <= gt:
        v = a[i]
        if v < x:
            d = f'看 {v}：比 4 小，和下标 {lt} 交换，lt、i 右移'
            a[lt], a[i] = a[i], a[lt]
            lt, i = lt + 1, i + 1
        elif v > x:
            d = f'看 {v}：比 4 大，和下标 {gt} 交换，gt 左移，i 不动'
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
        else:
            d = f'看 {v}：相等，i 右移'
            i += 1
        states.append((d, a[:], lt, i, gt))
    s = S()
    X, y = 390, 16
    for d, arr, lt, i, gt in states:
        s.text(LX, y + 17, d, 14, INK, 'start', bold=True)
        cs = row(s, X, y, arr, ['n' if j < lt else 'hit' if j < i else 'off' if j <= gt else 'new' for j in range(5)], cw=46)
        marks(s, cs, y + 34, [('lt', lt, 'blue'), ('i', i, 'org'), ('gt', gt, 'red')])
        y += 104
    legend(s, LX, y, [('n', '比 x 小'), ('hit', '等于 x'), ('off', '还没看'), ('new', '比 x 大')])
    s.text(LX, y + 44, 'i 超过 gt，停。结果 [2, 1 | 4, 4 | 5]，再递归排左边的 [2, 1] 和右边的 [5]', 14, INK, 'start', bold=True)
    s.save('alg-qs-trace')


def quickselect():
    s = S()
    nums = [3, 8, 1, 5, 9, 5, 2, 7, 6]
    s.text(LX, 33, 'nums', 15, INK, 'start', bold=True, mono=True)
    row(s, 130, 16, nums, ['n' if v < 5 else 'hit' if v == 5 else 'new' for v in nums])
    s.text(130 + 9 * 42 + 24, 33, '基准 x = 5，要找第 k = 7 小', 14, INK, 'start', bold=True)
    y = 118
    s.text(LX, y + 17, '分三段', 15, INK, 'start', bold=True)
    for x0, vals, st, label in ((130, [3, 1, 2], 'n', 'left：第 1~3 小'), (306, [5, 5], 'hit', 'mid：第 4~5 小'),
                                (440, [8, 9, 7, 6], 'new', 'right：第 6~9 小')):
        cs = row(s, x0, y, vals, st)
        brace(s, cs[0] - 19, cs[-1] + 19, y - 10, label, {'n': 'blue', 'hit': 'grn', 'new': 'org'}[st])
    lines(s, 130, y + 62, [('k = 7 落在 right 里：只进 right，别的两段直接扔掉', 'org'),
                           '前面已经排除了 3 + 2 = 5 个，所以在 right 里找第 7 − 5 = 2 小  →  答案 7'])
    s.save('alg-quickselect')


# ---------- 归并排序 ----------

def merge_two():
    L, R, i, j, res, rows = [1, 4, 7], [2, 3, 9], 0, 0, [], []

    def side(a, p):
        return [(v, 'off' if k < p else 'new' if k == p else 'n') for k, v in enumerate(a)]

    while i < len(L) and j < len(R):
        lc, rc = side(L, i), side(R, j)
        if L[i] <= R[j]:
            t = f'{L[i]} 和 {R[j]} 比：拿左边的 {L[i]}'
            res.append(L[i])
            i += 1
        else:
            t = f'{L[i]} 和 {R[j]} 比：拿右边的 {R[j]}'
            res.append(R[j])
            j += 1
        rows.append([('t', t, INK), lc, rc, [(v, 'hit' if k == len(res) - 1 else 'n') for k, v in enumerate(res)]])
    rest = L[i:] + R[j:]
    rows.append([('t', '左边拿完：右边剩下的直接接上', INK), side(L, i), side(R, j),
                 [(v, 'n') for v in res] + [(v, 'hit') for v in rest]])
    table('alg-merge-two', ['每一步', 'left', 'right', 'res（这一步之后）'], [270, 160, 160, 290], rows,
          leg=[('new', '两边各自「还没拿的第一个」（指针 i、j）'), ('off', '已经拿走'), ('hit', '刚放进 res')])


def merge_tree():
    s = S()
    Y = [16, 86, 156, 226, 296]
    N = {'r': (330, 0, '[5, 2, 4, 1]', 'n'), 'a': (190, 1, '[5, 2]', 'n'), 'b': (470, 1, '[4, 1]', 'n'),
         'a1': (120, 2, '[5]', 'sent'), 'a2': (260, 2, '[2]', 'sent'), 'b1': (400, 2, '[4]', 'sent'),
         'b2': (540, 2, '[1]', 'sent'), 'ma': (190, 3, '[2, 5]', 'hit'), 'mb': (470, 3, '[1, 4]', 'hit'),
         'm': (330, 4, '[1, 2, 4, 5]', 'hit')}
    E = [('r', 'a', 'blue'), ('r', 'b', 'blue'), ('a', 'a1', 'blue'), ('a', 'a2', 'blue'), ('b', 'b1', 'blue'),
         ('b', 'b2', 'blue'), ('a1', 'ma', 'grn'), ('a2', 'ma', 'grn'), ('b1', 'mb', 'grn'), ('b2', 'mb', 'grn'),
         ('ma', 'm', 'grn'), ('mb', 'm', 'grn')]
    for a, b, c in E:
        s.arrow(N[a][0], Y[N[a][1]] + 37, N[b][0], Y[N[b][1]] - 4, c)
    for cx, lv, t, st in N.values():
        w = tw(t, 15) + 22
        s.node(cx - w / 2, Y[lv], t, st, w=w, h=34, size=15)
    s.text(640, Y[1] - 18, '往下：从中间劈开', 14.5, COL['blue'], 'start', bold=True)
    s.text(640, Y[2] + 17, '只剩 1 个数：本身就有序，不用再劈', 13.5, SUB, 'start')
    s.text(640, Y[3] + 52, '往上：两个有序的合并成一个有序的', 14.5, COL['grn'], 'start', bold=True)
    s.save('alg-merge-tree')


def inversions():
    s = S()
    y = 62
    s.text(LX, y + 17, 'left', 15, INK, 'start', bold=True, mono=True)
    cl = row(s, 80, y, [2, 5, 8], ['off', 'chg', 'chg'])
    s.text(246, y + 17, 'right', 15, INK, 'start', bold=True, mono=True)
    cr = row(s, 316, y, [3, 6, 9], ['new', 'n', 'n'])
    brace(s, cl[1] - 19, cl[2] + 19, y - 10, '还没拿的：都比 3 大', 'red')
    marks(s, cl, y + 34, [('i = 1', 1, 'red')])
    marks(s, cr, y + 34, [('j = 0', 0, 'org')])
    lines(s, 480, y - 22, [('5 > 3：这一步拿的是右边的 3', 'org'), 'left 是有序的 → 5 后面的数也都比 3 大',
                           '它们在原数组里都排在 3 前面 → 每个都和 3 组成一个逆序对',
                           ('cnt += len(left) − i = 3 − 1 = 2', 'red')], gap=24)
    s.save('alg-inversions')


# ---------- 二分 ----------

def bs_idea():
    s = S()
    X, y = 150, 34
    s.text(LX, y + 17, 'nums', 15, INK, 'start', bold=True, mono=True)
    cs = row(s, X, y, [1, 2, 2, 3, 3, 4], ['sent'] * 3 + ['hit'] * 3, cw=52, idx='top')
    s.text(LX, y + 56, '>= 3 吗？', 14, SUB, 'start')
    for i, c in enumerate(cs):
        s.text(c, y + 56, '否' if i < 3 else '是', 15, COL['gry' if i < 3 else 'grn'], bold=True)
    ptr(s, cs[3], y + 68, '第一个「是」= 要找的位置', 'grn')
    lines(s, X + 6 * 52 + 24, y + 6, [('target = 3', INK), '前面一段全是「否」，后面一段全是「是」', '看中间：是「否」扔左半边，是「是」扔右半边'],
          gap=24)
    s.save('alg-bs-idea')


def bs_trace():
    nums, t = [1, 2, 2, 3, 3, 4], 3
    left, right = 0, 5
    s = S()
    X, y = 40, 30
    while True:
        done = left > right
        mid = None if done else (left + right) // 2
        sts = ['sent' if j < left else 'hit' if j > right else 'n' for j in range(6)]
        if mid is not None:
            sts[mid] = 'new'
        cs = row(s, X, y, nums, sts, cw=52, idx='top')
        marks(s, cs, y + 34, [('left', left, 'blue'), ('right', right, 'red')] + ([] if done else [('mid', mid, 'org')]))
        tx = X + 6 * 52 + 28
        if done:
            s.text(tx, y + 17, 'left 超过 right，结束：返回 left = 3，nums[3] 是第一个 3', 14, COL['grn'], 'start', bold=True)
            break
        if nums[mid] < t:
            s.text(tx, y + 17, f'nums[{mid}] = {nums[mid]} < 3：mid 太小，left = mid + 1 = {mid + 1}', 14, INK, 'start', bold=True)
            left = mid + 1
        else:
            s.text(tx, y + 17, f'nums[{mid}] = {nums[mid]} >= 3：mid 够大，right = mid − 1 = {mid - 1}', 14, INK, 'start', bold=True)
            right = mid - 1
        y += 152
    legend(s, LX, y + 104, [('sent', '已确定「否」（比 target 小）'), ('hit', '已确定「是」（>= target）'), ('n', '还没确定'), ('new', 'mid')])
    s.save('alg-bs-trace')


def bs_four():
    s = S()
    cw = 126
    s.text(LX, 18, 'x = 3', 15, INK, 'start', bold=True, mono=True)
    cs = row(s, 30, 52, [1, 2, 3, 3, 3, 5], ['n', 'n', 'hit', 'hit', 'hit', 'n'], cw=cw, idx='top')
    for i, (a, b, col) in {1: ('最后一个 < 3', 'lower_bound(3) - 1', 'red'), 2: ('第一个 >= 3', 'lower_bound(3)', 'grn'),
                           4: ('最后一个 <= 3', 'lower_bound(4) - 1', 'org'), 5: ('第一个 > 3', 'lower_bound(4)', 'blue')}.items():
        s.arrow(cs[i], 112, cs[i], 91, col)
        s.text(cs[i], 124, a, 14, COL[col], bold=True)
        s.text(cs[i], 144, b, 12, SUB, mono=True)
    s.save('alg-bs-four')


def bs_answer():
    s = S()
    X, y, cw = 170, 50, 50
    s.text(LX, 18, '求 n = 10 的平方根（向下取整）：check(x) = x * x > n', 14.5, INK, 'start', bold=True)
    xs = list(range(11))
    s.text(LX, y + 17, 'x', 15, INK, 'start', bold=True, mono=True)
    cs = row(s, X, y, xs, ['sent' if v * v <= 10 else 'hit' for v in xs], cw=cw)
    s.text(LX, y + 54, 'x * x', 14, SUB, 'start', mono=True)
    s.text(LX, y + 80, 'check(x)', 14, SUB, 'start', mono=True)
    for v, c in zip(xs, cs):
        s.text(c, y + 54, v * v, 13, SUB, mono=True)
        s.text(c, y + 80, '是' if v * v > 10 else '否', 15, COL['grn' if v * v > 10 else 'gry'], bold=True)
    s.arrow(cs[4], y + 118, cs[4], y + 96, 'grn')
    s.text(cs[4] - 8, y + 130, '第一个「是」：first_true 返回 4', 13.5, COL['grn'], 'start', bold=True)
    s.arrow(cs[3], y + 118, cs[3], y + 96, 'red')
    s.text(cs[3] + 8, y + 130, '答案 = 4 − 1 = 3', 13.5, COL['red'], 'end', bold=True)
    s.save('alg-bs-answer')


def float_bs():
    s = S()
    X0, W, n = 70, 440, 2
    lo, hi, y = 0.0, 2.0, 62

    def px(v):
        return X0 + v / 2 * W

    s.text(LX, 18, '求 2 的立方根：check(x) = x³ >= 2，区间从 [0, 2] 开始，每次砍一半', 14.5, INK, 'start', bold=True)
    top = y - 24
    for _ in range(5):
        s.seg(px(0), y, px(2), y, '#CBD5E1', sw=2)
        s.rect(px(lo), y - 5, px(hi) - px(lo), 10, '#BFDBFE', COL['blue'], rx=5)
        mid = (lo + hi) / 2
        s.seg(px(mid), y - 13, px(mid), y + 13, 'org', sw=2.5)
        s.text(px(lo) - 4, y + 20, f'{lo:g}', 12, COL['blue'], 'end', mono=True)
        s.text(px(hi) + 4, y + 20, f'{hi:g}', 12, COL['blue'], 'start', mono=True)
        ok = mid ** 3 >= n
        s.text(px(2) + 60, y, f'mid = {mid:g}：{mid:g}³ = {mid ** 3:.3f}  ' + ('>= 2，是：right = mid' if ok else '< 2，否：left = mid'),
               13.5, INK, 'start')
        if ok:
            hi = mid
        else:
            lo = mid
        y += 70
    ax = px(2 ** (1 / 3))
    s.seg(ax, top, ax, y - 44, 'grn', dash=1, sw=1.5)
    s.text(ax, y - 30, '答案 ≈ 1.26', 13, COL['grn'], bold=True)
    s.text(LX, y, '蓝色 = 当前区间 [left, right]，一直包着答案；橙色竖线 = mid；循环 100 次后区间长度是原来的 1/2¹⁰⁰', 13.5, SUB, 'start')
    s.save('alg-float-bs')


# ---------- 高精度 ----------

def add_column():
    s = S()

    def cx(c):
        return 96 + c * 46

    s.text(LX, 22, '进位', 13, COL['red'], 'start', bold=True)
    for c in (0, 1, 2):
        s.text(cx(c), 22, 1, 14, COL['red'], bold=True, mono=True)
    for c, d in zip((1, 2, 3), '957'):
        s.text(cx(c), 54, d, 22, INK, bold=True, mono=True)
    s.text(cx(0), 94, '+', 22, INK, bold=True, mono=True)
    for c, d in zip((2, 3), '68'):
        s.text(cx(c), 94, d, 22, INK, bold=True, mono=True)
    s.seg(cx(0) - 22, 120, cx(3) + 22, 120, INK, sw=2)
    for c, d in enumerate('1025'):
        s.node(cx(c) - 18, 132, d, 'hit', w=36, h=36, size=20)
    lines(s, 320, 30, ['① 个位：7 + 8 = 15  →  写 5，进 1', '② 十位：5 + 6 + 1 = 12  →  写 2，进 1',
                       '③ 百位：9 + 0 + 1 = 10  →  写 0，进 1',
                       ('④ 两个数都加完了，但还有进位 1：再写一位 1（循环条件里的 or carry）', 'red')], size=14, gap=34)
    s.text(320, 168, '从最低位开始逐位相加，满十进一；结果是从低位往高位写的，最后反过来', 13.5, SUB, 'start')
    s.save('alg-add-column')


def mul_pos():
    s = S()
    a, b, X, cw = '123', '45', 270, 66
    s.text(LX, 20, 'a = "123"，b = "45"：a[i] × b[j] 落在结果的第 i + j + 1 位', 14.5, INK, 'start', bold=True)
    s.text(LX, 52, 'res 的下标', 13, SUB, 'start')
    for k in range(5):
        s.text(X + k * cw + (cw - 3) / 2, 52, k, 13, SUB, mono=True)
    y, res = 68, [0] * 5
    for i in (2, 1, 0):
        for j in (1, 0):
            p = int(a[i]) * int(b[j])
            res[i + j + 1] += p
            s.text(LX, y + 15, f'a[{i}] × b[{j}] = {a[i]} × {b[j]} = {p}', 13.5, INK, 'start', mono=True)
            s.node(X + (i + j + 1) * cw, y, f'+{p}', 'new', w=cw - 3, h=30, size=14)
            y += 36
    s.seg(LX, y + 2, X + 5 * cw, y + 2, '#CBD5E1', sw=1.5)
    s.text(LX, y + 28, '全部加完（先不管进位）', 14, INK, 'start', bold=True)
    row(s, X, y + 12, res, 'n', cw=cw, ch=32)
    for k in range(4, 0, -1):
        res[k - 1] += res[k] // 10
        res[k] %= 10
    s.text(LX, y + 72, '从低位到高位统一进位', 14, INK, 'start', bold=True)
    row(s, X, y + 56, res, 'hit', cw=cw, ch=32)
    s.text(X + 5 * cw + 20, y + 72, '去掉开头的 0  →  "5535"', 14, COL['grn'], 'start', bold=True)
    s.save('alg-mul-pos')


# ---------- 前缀和 ----------

def prefix_1d():
    s = S()
    cw, X, y = 64, 130, 36
    s.text(LX, y + 17, 'nums', 15, INK, 'start', bold=True, mono=True)
    row(s, X + cw / 2, y, [3, 1, 4, 1, 5], ['n', 'new', 'new', 'new', 'n'], cw=cw, idx='top')
    y2 = y + 84
    s.text(LX, y2 + 17, 's', 15, INK, 'start', bold=True, mono=True)
    cs = row(s, X, y2, [0, 3, 4, 8, 9, 14], ['off', 'chg', 'off', 'off', 'hit', 'off'], cw=cw, idx='bot')
    for c in cs:
        s.seg(c, y + 38, c, y2 - 4, '#94A3B8', dash=1, sw=1.2)
    lines(s, X + 6 * cw + 34, y - 4, [('s[i] = 虚线左边所有数的和（前 i 个数）', INK), 's[4] = 3 + 1 + 4 + 1 = 9（绿）',
                                      's[1] = 3（红）', ('nums[1..3] = s[4] − s[1] = 9 − 3 = 6（橙）', 'org'),
                                      ('一般地：nums[l..r] 的和 = s[r + 1] − s[l]', INK)], gap=27)
    s.save('alg-prefix-1d')


def prefix_2d_build():
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
    for k, t in enumerate(['s[i][j+1] = A + B', 's[i+1][j] = A + C', 's[i][j] = A', 'matrix[i][j] = x']):
        s.text(450, y + 4 + k * 26, t, 14, INK, 'start', mono=True)
    lines(s, 450, y + 122, [('s[i+1][j+1] = (A + B) + (A + C) − A + x', 'red'), 'A 被加了两次，所以减掉一次'], size=14, gap=26)
    s.save('alg-prefix-2d-build')


def prefix_2d_query():
    s = S()
    x, y = 110, 52
    blk(s, x, y, 120, 70, 'A', 'n')
    blk(s, x + 120, y, 172, 70, 'B', 'new')
    blk(s, x, y + 70, 120, 110, 'C', 'pur')
    blk(s, x + 120, y + 70, 172, 110, 'D（要求的）', 'hit', 16)
    s.text(x + 140, y - 18, 'y1', 14, INK, bold=True, mono=True)
    s.text(x + 272, y - 18, 'y2', 14, INK, bold=True, mono=True)
    s.text(x - 22, y + 86, 'x1', 14, INK, bold=True, mono=True)
    s.text(x - 22, y + 164, 'x2', 14, INK, bold=True, mono=True)
    for k, t in enumerate(['s[x2+1][y2+1] = A + B + C + D（整块）', 's[x1][y2+1] = A + B（D 上面的）',
                           's[x2+1][y1] = A + C（D 左边的）', 's[x1][y1] = A']):
        s.text(450, y + 4 + k * 26, t, 14, INK, 'start', mono=True)
    lines(s, 450, y + 126, [('D = 整块 − 上面的 − 左边的 + A', 'grn'), 'A 被减了两次，所以加回来一次'], size=14, gap=26)
    s.save('alg-prefix-2d-query')


# ---------- 差分 ----------

def diff_1d():
    s = S()
    X, cw, y = 170, 60, 36
    s.text(LX, y + 17, 'd', 15, INK, 'start', bold=True, mono=True)
    row(s, X, y, ['0', '0', '+c', '0', '0', '−c'], ['off', 'off', 'new', 'off', 'off', 'chg'], cw=cw, idx='top')
    y2 = y + 60
    s.text(LX, y2 + 17, 'd 的前缀和', 15, INK, 'start', bold=True)
    cs = row(s, X, y2, ['0', '0', 'c', 'c', 'c', '0'], ['off', 'off', 'hit', 'hit', 'hit', 'off'], cw=cw)
    brace(s, cs[2] - 28, cs[4] + 28, y2 + 44, '只有 2 到 4 加了 c', 'grn', up=False)
    lines(s, X + 6 * cw + 30, y + 6, [('把 [l, r] = [2, 4] 这一段加 c', INK), ('d[l] += c：从 l 开始，后面全部多 c', 'org'),
                                      ('d[r + 1] −= c：从 r + 1 开始，把这个 c 抵消掉', 'red')], gap=27)
    s.save('alg-diff-1d')


def diff_trace():
    s = S()
    X, cw, y = 260, 54, 34
    nums, ups = [1, 2, 2, 1, 2], [(0, 2, 1), (2, 4, 1)]
    s.text(LX, y + 17, '原数组 nums', 14, INK, 'start', bold=True)
    row(s, X, y, nums, 'n', cw=cw, idx='top')
    s.text(X + 5 * cw + (cw - 3) / 2, y - 11, 5, 12, SUB, mono=True)
    d = [0] * 6
    for l, r, c in ups:
        y += 50
        d[l] += c
        d[r + 1] -= c
        s.text(LX, y + 17, f'操作 ({l}, {r}, {c}) 之后的 d', 14, INK, 'start', bold=True)
        row(s, X, y, [inf(v) for v in d], ['new' if k == l else 'chg' if k == r + 1 else 'off' for k in range(6)], cw=cw)
        s.text(X + 6 * cw + 20, y + 17, f'd[{l}] += {c}，d[{r + 1}] −= {c}', 13.5, SUB, 'start', mono=True)
    y += 50
    pre, cur = [], 0
    for v in d[:5]:
        cur += v
        pre.append(cur)
    s.text(LX, y + 17, 'd 的前缀和：每个位置加了多少', 14, INK, 'start', bold=True)
    row(s, X, y, pre, 'pur', cw=cw)
    y += 50
    s.text(LX, y + 17, '加上原数组：结果', 14, INK, 'start', bold=True)
    row(s, X, y, [a + b for a, b in zip(nums, pre)], 'hit', cw=cw)
    s.save('alg-diff-trace')


def diff_2d():
    n, x1, y1, x2, y2, cw = 6, 1, 1, 3, 3, 30
    pts = [(x1, y1, 1), (x2 + 1, y1, -1), (x1, y2 + 1, -1), (x2 + 1, y2 + 1, 1)]
    titles = ['① d[x1][y1] += c', '② d[x2+1][y1] −= c', '③ d[x1][y2+1] −= c', '④ d[x2+1][y2+1] += c']
    caps = [['右下方全部 +c', '范围太大了'], ['子矩阵下面多加的', '抵消掉了'], ['右边多加的也抵消了', '但右下角被减了两次：−c'],
            ['右下角补回一次', '只剩目标子矩阵 +c']]

    def draw(s, ox, oy, k):
        d = [[0] * n for _ in range(n)]
        for a, b, c in pts[:k + 1]:
            d[a][b] += c
        gx, gy = ox + 28, oy + 22
        for i in range(n):
            for j in range(n):
                v = sum(d[a][b] for a in range(i + 1) for b in range(j + 1))
                s.node(gx + j * cw, gy + i * cw, {1: 'c', -1: '−c', 0: '0'}[v],
                       'new' if v == 1 else 'chg' if v == -1 else 'off', w=cw - 3, h=cw - 3, size=12)
        for q, (a, b, c) in enumerate(pts[:k + 1]):
            s.rect(gx + b * cw - 2, gy + a * cw - 2, cw + 1, cw + 1, 'none', COL['pur'], rx=8, sw=3.2 if q == k else 1.6)
        for j, t in ((y1, 'y1'), (y2, 'y2')):
            s.text(gx + j * cw + 13, gy - 11, t, 12, SUB, bold=True, mono=True)
        for i, t in ((x1, 'x1'), (x2, 'x2')):
            s.text(gx - 14, gy + i * cw + 13, t, 12, SUB, bold=True, mono=True)
        lines(s, ox, gy + n * cw + 18, caps[k], size=13, gap=20)

    panel_grid('alg-diff-2d', 4, 236, 300, draw, titles=titles,
               foot='紫框 = 在 d 上改的那个点（粗框是这一步改的）；格子里 = 求完二维前缀和后，这个位置一共多了多少')


# ---------- 位运算 ----------

def bits_row(s, x, y, label, bits, sts, note=None, color=SUB):
    s.text(LX, y + 16, label, 14, INK, 'start', bold=True, mono=True)
    row(s, x, y, list(bits), sts, cw=40, ch=32)
    if note:
        s.text(x + len(bits) * 40 + 18, y + 16, note, 13.5, color, 'start')


def bit_lowest():
    s = S()
    X = 150
    s.text(LX, 18, 'n & (n - 1)：去掉最低位的 1', 14.5, INK, 'start', bold=True)
    bits_row(s, X, 36, 'n', '101100', ['n', 'n', 'n', 'new', 'n', 'n'], '橙色 = 最低位的 1')
    bits_row(s, X, 76, 'n - 1', '101011', ['n', 'n', 'n', 'chg', 'chg', 'chg'], '减 1：那个 1 变成 0，它右边的 0 全变成 1')
    bits_row(s, X, 116, 'n & (n - 1)', '101000', ['n', 'n', 'n', 'hit', 'hit', 'hit'], '上下都是 1 才是 1：这一段全没了，最低位的 1 被去掉',
             COL['grn'])
    s.seg(LX, 166, 820, 166, '#E5E7EB', sw=1)
    s.text(LX, 186, 'n & -n：只保留最低位的 1（lowbit）', 14.5, INK, 'start', bold=True)
    bits_row(s, X, 204, 'n', '101100', ['n', 'n', 'n', 'new', 'n', 'n'], '= 44')
    bits_row(s, X, 244, 'n & -n', '000100', ['off', 'off', 'off', 'new', 'off', 'off'], '= 4：只剩最低位的那个 1', COL['org'])
    s.save('alg-bit-lowest')


def bit_kth():
    s = S()
    X, n, k = 200, '101100', 2
    s.text(LX, 20, '第几位', 13, SUB, 'start')
    for c in range(6):
        s.text(X + c * 40 + 18.5, 20, 5 - c, 13, COL['pur'] if 5 - c == k else SUB, bold=5 - c == k, mono=True)
    col = 5 - k

    def sts(bits, base='n'):
        return ['off' if b == '0' else base for b in bits]

    a = sts(n)
    a[col] = 'new'
    bits_row(s, X, 34, 'n', n, a, '要操作第 k = 2 位（最低位是第 0 位）')
    m = sts('000100', 'pur')
    bits_row(s, X, 74, '1 << 2', '000100', m, '「定位器」：只有第 2 位是 1')
    s.seg(LX, 120, 840, 120, '#E5E7EB', sw=1)
    sh = sts('001011')
    sh[5] = 'new'
    bits_row(s, X, 132, 'n >> 2', '001011', sh, '整体右移 2 位，第 2 位跑到了最低位')
    bits_row(s, X, 172, 'n >> 2 & 1', '000001', ['off'] * 5 + ['hit'], '只留最低位：结果 1，说明第 2 位是 1', COL['grn'])
    s.seg(LX, 218, 840, 218, '#E5E7EB', sw=1)
    for y, label, bits, note in ((230, 'n | (1 << 2)', '101100', '把第 2 位变成 1（这里本来就是 1）'),
                                 (270, 'n & ~(1 << 2)', '101000', '把第 2 位变成 0'),
                                 (310, 'n ^ (1 << 2)', '101000', '把第 2 位翻转：1 变 0')):
        b = sts(bits)
        b[col] = 'hit' if bits[col] == n[col] else 'chg'
        bits_row(s, X, y, label, bits, b, note)
    s.save('alg-bit-kth')


def bit_subset():
    s = S()
    X, y, cw = 110, 76, 50
    s.text(LX, 18, 'nums = [a, b, c]：第 k 位是 1 表示选了第 k 个元素', 14.5, INK, 'start', bold=True)
    s.text(LX, 54, 'mask', 13, SUB, 'start', mono=True)
    for c, (t, e) in enumerate((('第 2 位', 'c'), ('第 1 位', 'b'), ('第 0 位', 'a'))):
        s.text(X + c * cw + 23.5, 44, t, 11.5, SUB)
        s.text(X + c * cw + 23.5, 62, e, 14, INK, bold=True, mono=True)
    s.text(X + 3 * cw + 44, 54, '选出的子集', 13, SUB, 'start')
    for m in range(8):
        bits = f'{m:03b}'
        s.text(LX + 8, y + 15, m, 14, INK, 'start', bold=True, mono=True)
        row(s, X, y, list(bits), ['new' if c == '1' else 'off' for c in bits], cw=cw, ch=30)
        sub = ['abc'[k] for k in range(3) if m >> k & 1]
        if sub:
            row(s, X + 3 * cw + 44, y, sub, 'hit', cw=40, ch=30)
        else:
            s.text(X + 3 * cw + 44, y + 15, '[ ]  空集', 13.5, COL['gry'], 'start')
        y += 36
    s.text(LX, y + 14, 'mask 从 0 数到 2³ − 1 = 7，正好不重不漏地列出全部 8 个子集', 13.5, SUB, 'start')
    s.save('alg-bit-subset')


# ---------- 双指针 ----------

def window_trace():
    st, left, seen = 'abcbd', 0, set()
    s = S()
    X, y = 150, 24
    for right, c in enumerate(st):
        removed = []
        while c in seen:
            seen.remove(st[left])
            removed.append(left)
            left += 1
        seen.add(c)
        s.text(LX, y + 17, f'right = {right}', 14, INK, 'start', bold=True, mono=True)
        cs = row(s, X, y, list(st), ['del' if j in removed else 'off' if j < left or j > right else 'new' if j == right
                                     else 'n' for j in range(5)], cw=46)
        marks(s, cs, y + 34, [('left', left, 'blue'), ('right', right, 'org')])
        t = (f'{c} 和窗口里的重复：移出 ' + '、'.join(st[j] for j in removed) + f'，left 到 {left}。' if removed
             else f'{c} 不重复，left 不动。')
        s.text(X + 5 * 46 + 26, y + 17, t + f'窗口 "{st[left:right + 1]}"，长度 {right - left + 1}', 14,
               COL['red'] if removed else INK, 'start', bold=bool(removed))
        y += 100
    legend(s, LX, y, [('n', '窗口里'), ('new', '新进窗口'), ('del', '这一步被移出'), ('off', '窗口外')])
    s.text(LX, y + 44, 's = "abcbd"  →  最长长度 3', 14, INK, 'start', bold=True)
    s.save('alg-window-trace')


def two_sum_sorted():
    nums, t = [1, 2, 4, 7, 11, 15], 15
    left, right = 0, 5
    s = S()
    X, y = 40, 24
    s.text(LX, y - 6, 'target = 15，数组已经从小到大排好', 14.5, INK, 'start', bold=True)
    y += 26
    while left < right:
        tot = nums[left] + nums[right]
        found = tot == t
        cs = row(s, X, y, nums, ['off' if j < left or j > right else ('hit' if found else 'new') if j in (left, right)
                                 else 'n' for j in range(6)], cw=50)
        marks(s, cs, y + 34, [('left', left, 'blue'), ('right', right, 'red')])
        msg = '找到' if found else '太大：right 左移（15 配谁都太大，扔掉）' if tot > t and right == 5 else \
            '太大：right 左移' if tot > t else '太小：left 右移（它配最大的都不够，扔掉）'
        s.text(X + 6 * 50 + 28, y + 17, f'{nums[left]} + {nums[right]} = {tot}，{msg}', 14, COL['grn'] if found else INK,
               'start', bold=True)
        if found:
            break
        if tot < t:
            left += 1
        else:
            right -= 1
        y += 94
    s.save('alg-two-sum-sorted')


def pair_sum():
    a, b, t = [1, 2, 7, 9], [1, 3, 4, 6], 11
    s = S()
    y, j = 50, 3
    s.text(LX, 18, 'target = 11：i 在 a 上从左往右，j 在 b 上从右往左，都不回头', 14.5, INK, 'start', bold=True)
    for i, x in enumerate(a):
        while True:
            tot = x + b[j]
            found = tot == t
            s.text(LX, y + 17, 'a', 15, INK, 'start', bold=True, mono=True)
            ca = row(s, 50, y, a, [('hit' if found else 'new') if k == i else 'off' if k < i else 'n' for k in range(4)], cw=46)
            marks(s, ca, y + 34, [('i', i, 'blue')])
            s.text(270, y + 17, 'b', 15, INK, 'start', bold=True, mono=True)
            cb = row(s, 302, y, b, [('hit' if found else 'new') if k == j else 'off' if k > j else 'n' for k in range(4)], cw=46)
            marks(s, cb, y + 34, [('j', j, 'red')])
            msg = '找到' if found else '太大：j 左移' if tot > t else '不够：换下一个 i（a[i] 变大，j 不用回头）'
            s.text(520, y + 17, f'{x} + {b[j]} = {tot}，{msg}', 14, COL['grn'] if found else INK, 'start', bold=True)
            y += 84
            if tot > t and j > 0:
                j -= 1
                continue
            break
        if found:
            break
    s.save('alg-pair-sum')


# ---------- 离散化 / 区间合并 ----------

def discretize():
    s = S()
    X, cw = 170, 100
    nums = [100, 5, 100000, 5]
    vals = sorted(set(nums))
    stm = {5: 'n', 100: 'new', 100000: 'hit'}
    s.text(LX, 37, 'nums', 15, INK, 'start', bold=True, mono=True)
    row(s, X, 20, nums, [stm[v] for v in nums], cw=cw)
    s.text(LX, 109, '① ② 去重、排序', 14, INK, 'start', bold=True)
    cs = row(s, X, 92, vals, [stm[v] for v in vals], cw=cw)
    for c in cs:
        s.arrow(c, 130, c, 150, 'gry')
    s.text(LX, 171, '③ 编号', 14, INK, 'start', bold=True)
    row(s, X, 154, [0, 1, 2], [stm[v] for v in vals], cw=cw)
    s.text(LX, 243, '结果', 15, INK, 'start', bold=True)
    row(s, X, 226, [vals.index(v) for v in nums], [stm[v] for v in nums], cw=cw)
    lines(s, X + 4 * cw + 30, 37, [('颜色相同 = 同一个数 = 同一个编号', INK), '排在第几个，编号就是几',
                                   '只保留了谁大谁小，没保留差多少'], gap=26)
    s.save('alg-discretize')


BAR = {'blue': '#DBEAFE', 'org': '#FEF3C7', 'grn': '#D1FAE5'}


def bar(s, x1, x2, y, col, l=None, r=None):
    s.rect(x1, y - 7, x2 - x1, 14, BAR[col], COL[col], rx=7)
    if l:
        s.text(x1 + 4, y - 18, l, 13, COL[col], bold=True, mono=True)
    if r:
        s.text(x2 - 4, y - 18, r, 13, COL[col], bold=True, mono=True)


def interval_cases():
    s = S()
    for k, (title, old, new, res, cap) in enumerate((
            ('有重叠：l <= R', (0, 170), (110, 270), [(0, 270)], '合并成 [L, max(R, r)]'),
            ('没有重叠：l > R', (0, 110), (160, 270), [(0, 110), (160, 270)], '[L, R] 定下来，[l, r] 新开一个'),
            ('新区间被完全包住', (0, 270), (80, 180), [(0, 270)], '还是 [L, R]：所以右端点要取 max'))):
        ox = 24 + k * 320
        if k:
            s.seg(ox - 26, 14, ox - 26, 190, '#E5E7EB', sw=1)
        s.text(ox, 22, title, 14.5, INK, 'start', bold=True)
        bar(s, ox + old[0], ox + old[1], 70, 'blue', 'L', 'R')
        bar(s, ox + new[0], ox + new[1], 108, 'org', 'l', 'r')
        s.arrow(ox + 135, 124, ox + 135, 144, 'gry')
        for a, b in res:
            bar(s, ox + a, ox + b, 158, 'grn')
        s.text(ox, 186, cap, 13.5, COL['grn'], 'start', bold=True)
    s.save('alg-interval-cases')


def interval_trace():
    s = S()
    X0, U = 130, 38

    def px(v):
        return X0 + v * U

    s.text(LX, 46, '排序后的区间', 14, INK, 'start', bold=True)
    for (a, b), y in (((1, 3), 46), ((8, 10), 46), ((15, 18), 46), ((2, 6), 92)):
        bar(s, px(a), px(b), y, 'blue')
        s.text((px(a) + px(b)) / 2, y - 19, f'[{a}, {b}]', 13, COL['blue'], bold=True, mono=True)
    ay = 128
    s.seg(px(0), ay, px(19), ay, '#94A3B8', sw=1.5)
    for v in range(20):
        s.seg(px(v), ay - 4, px(v), ay + 4, '#94A3B8', sw=1.2)
        s.text(px(v), ay + 15, v, 11, SUB, mono=True)
    s.text(LX, 186, '合并后', 14, INK, 'start', bold=True)
    for a, b in ((1, 6), (8, 10), (15, 18)):
        bar(s, px(a), px(b), 186, 'grn')
        s.text((px(a) + px(b)) / 2, 167, f'[{a}, {b}]', 13, COL['grn'], bold=True, mono=True)
    lines(s, LX, 222, ['[2, 6]：左端点 2 <= 3，和 [1, 3] 有重叠 → 右端点延长到 max(3, 6) = 6，合并成 [1, 6]',
                       '[8, 10]：8 > 6，没有重叠 → 新开一个；[15, 18]：15 > 10 → 再新开一个'])
    s.save('alg-interval-trace')


if __name__ == '__main__':
    for f in (qs_regions, qs_trace, quickselect, merge_two, merge_tree, inversions, bs_idea, bs_trace, bs_four,
              bs_answer, float_bs, add_column, mul_pos, prefix_1d, prefix_2d_build, prefix_2d_query, diff_1d,
              diff_trace, diff_2d, bit_lowest, bit_kth, bit_subset, window_trace, two_sum_sorted, pair_sum,
              discretize, interval_cases, interval_trace):
        f()
    print('ok')
