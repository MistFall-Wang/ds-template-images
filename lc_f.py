#!/usr/bin/env python3
"""Diagrams for the 哈希表 / 并查集 / Trie sections (LeetCode 套法). Prefix: lcf-.

Run from this directory:  python3 lc_f.py
"""
from collections import defaultdict

from make_diagrams import *


# ---------- 哈希表 ----------

def hash_chain():
    """拉链法 vs 开放寻址法, same keys, N = 5."""
    keys, N = [12, 7, 3, 22], 5
    s = S()
    s.text(LX, 20, f'依次放进 {keys}，位置 = x % {N}', 14.5, INK, 'start', bold=True)
    s.text(LX, 46, '，'.join(f'{k} % {N} = {k % N}' for k in keys), 13.5, SUB, 'start', mono=True)

    # 拉链法
    X, y, W = 30, 120, 62
    s.text(X, 86, '拉链法：每个位置挂一个 list，撞了就接在后面', 14, COL['blue'], 'start', bold=True)
    buckets = [[] for _ in range(N)]
    for k in keys:
        buckets[k % N].append(k)
    for i in range(N):
        s.text(X + i * W + (W - 6) / 2, y - 12, i, 13, SUB, mono=True)
        s.node(X + i * W, y, '', 'n' if buckets[i] else 'off', w=W - 6, h=30)
        cy = y + 30
        for k in buckets[i]:
            s.arrow(X + i * W + (W - 6) / 2, cy + 2, X + i * W + (W - 6) / 2, cy + 20)
            s.node(X + i * W, cy + 22, k, 'new', w=W - 6, h=32, size=15)
            cy += 54
    s.text(X, y + 208, '查 22：算出位置 2，只在 2 号的 list 里找', 13.5, INK, 'start')

    # 开放寻址法
    X2 = 440
    s.text(X2, 86, '开放寻址法：撞了就往后找下一个空位', 14, COL['org'], 'start', bold=True)
    slot, notes = [None] * N, []
    for k in keys:
        p, tried = k % N, []
        while slot[p] is not None:
            tried.append(p)
            p = (p + 1) % N
        slot[p] = k
        notes.append(f'{k}：位置 {k % N}' + (f'，{"、".join(map(str, tried))} 号被占，放到 {p} 号' if tried else ' 是空的，直接放'))
    for i in range(N):
        s.text(X2 + i * W + (W - 6) / 2, y - 12, i, 13, SUB, mono=True)
        s.node(X2 + i * W, y, '' if slot[i] is None else slot[i], 'off' if slot[i] is None else 'new', w=W - 6, h=34, size=15)
    for i, t in enumerate(notes):
        s.text(X2, y + 62 + i * 25, t, 13.5, INK, 'start')
    s.text(X2, y + 208, '查 22：从 2 号开始往后一个个比，直到找到或碰到空位', 13.5, INK, 'start')
    s.save('lcf-hash-chain')


def longest_consec():
    nums = [100, 4, 200, 1, 3, 2]
    st, rows, best = set(nums), [], 0
    for x in st:
        if x - 1 in st:
            rows.append([('t', f'x = {x}', INK), ('t', f'{x - 1} 在', 'gry'), ('t', '不是起点，跳过', 'gry'), ''])
            continue
        y = x
        while y + 1 in st:
            y += 1
        best = max(best, y - x + 1)
        rows.append([('t', f'x = {x}', INK), ('t', f'{x - 1} 不在', 'org'), ('t', f'是起点，往后数到 {y}', 'org'),
                     [(v, 'new' if v == x else 'n') for v in range(x, y + 1)] + [(f'长度 {y - x + 1}', 'sent')]])
    table('lcf-longest-consec', ['当前 x', 'x - 1 在不在 num_set 里', '做什么', '从 x 往后数出来的一段'], [110, 230, 230, 330], rows,
          foot=f'nums = {nums}  →  最长的一段是 [1, 2, 3, 4]，答案 {best}')


def group_anagrams():
    strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    g, rows, keys = defaultdict(list), [], []
    for w in strs:
        key = ''.join(sorted(w))
        if key not in keys:
            keys.append(key)
        g[key].append(w)
        rows.append((w, key, {k: list(v) for k, v in g.items()}))
    out = []
    for w, key, snap in rows:
        row = [('t', f'"{w}"', INK), ('t', f'"{key}"', 'org')]
        for k in keys:
            row.append([(v, 'new' if v == w else 'n') for v in snap[k]] if k in snap else '')
        out.append(row)
    table('lcf-group-anagrams', ['当前单词', '排序后的 key'] + [f'groups["{k}"]' for k in keys], [110, 140, 210, 150, 90], out, cw=30,
          foot='strs = ["eat", "tea", "tan", "ate", "nat", "bat"]：字母相同的单词，排序后是同一个 key')


def rand_set():
    """LC 380 remove(8) from nums = [5, 8, 3, 9]."""
    nums = [5, 8, 3, 9]
    pos = {v: i for i, v in enumerate(nums)}
    x = 8
    snaps = [('开始', [], list(nums), dict(pos), {}, '要删 8：pos[8] = 1，它在下标 1')]
    i, last = pos[x], nums[-1]
    nums[i] = last
    snaps.append(('① 最后一个抄过来', [f'nums[{i}] = {last}'], list(nums), dict(pos), {i: 'chg'}, f'最后一个数 {last} 盖住下标 {i} 上的 {x}'))
    pos[last] = i
    snaps.append(('② 改它的下标', [f'pos[{last}] = {i}'], list(nums), dict(pos), {i: 'chg'}, f'{last} 搬家了，pos 里跟着改'))
    nums.pop()
    del pos[x]
    snaps.append(('③ 删掉末尾和 8', ['nums.pop()', f'del pos[{x}]'], list(nums), dict(pos), {}, '末尾那份多余的删掉，O(1)'))
    s = S()
    X, y = 210, 48
    s.text(X, 10, 'nums（下标在上面）', 13, SUB, 'start')
    s.text(X + 230, 10, 'pos（值 → 下标）', 13, SUB, 'start')
    for title, code, ns, ps, hot, nt in snaps:
        lab(s, y, title, code)
        for j, v in enumerate(ns):
            s.text(X + j * 43 + 20, y - 9, j, 12, SUB, mono=True)
        st = [(v, hot.get(j, 'del' if title.startswith('①') and j == len(ns) - 1 or title.startswith('②') and j == len(ns) - 1 else 'n'))
              for j, v in enumerate(ns)]
        cells(s, X, y + 3, st)
        s.text(X + 230, y + 20, '{' + ', '.join(f'{k}: {v}' for k, v in ps.items()) + '}', 14, INK, 'start', mono=True)
        note(s, X + 480, y, nt)
        y += 78
    legend(s, LX, y - 12, [('chg', '被改写的位置'), ('del', '多出来的一份，马上删掉')])
    s.save('lcf-rand-set')


# ---------- 并查集 ----------

def uf_grid():
    grid = ["1100", "1001", "0011"]
    m, n = len(grid), len(grid[0])
    s = S()
    X, Y, C = 80, 58, 56
    s.text(LX, 18, '格子 (row, col) 的编号 = row * n + col（这里 n = 4 列）', 14.5, INK, 'start', bold=True)
    for c in range(n):
        s.text(X + c * C + (C - 6) / 2, Y - 14, f'col {c}', 12, SUB, mono=True)
    unions = []
    for r in range(m):
        s.text(X - 12, Y + r * C + (C - 6) / 2, f'row {r}', 12, SUB, 'end', mono=True)
        for c in range(n):
            land = grid[r][c] == '1'
            s.node(X + c * C, Y + r * C, r * n + c, 'new' if land else 'off', w=C - 6, h=C - 6, size=16)
            if land and r + 1 < m and grid[r + 1][c] == '1':
                unions.append((r * n + c, (r + 1) * n + c))
            if land and c + 1 < n and grid[r][c + 1] == '1':
                unions.append((r * n + c, r * n + c + 1))
    for a, b in unions:
        ra, ca, rb, cb = a // n, a % n, b // n, b % n
        ax, ay = X + ca * C + (C - 6) / 2, Y + ra * C + (C - 6) / 2
        bx, by = X + cb * C + (C - 6) / 2, Y + rb * C + (C - 6) / 2
        if ra == rb:
            s.seg(ax + 17, ay, bx - 17, by, 'red', sw=3)
        else:
            s.seg(ax, ay + 15, bx, by - 15, 'red', sw=3)
    water = sum(row.count('0') for row in grid)
    TX = X + n * C + 40
    lines = [(f'例：(1, 3) → 1 * 4 + 3 = 7', INK, True),
             ('每块陆地只看「下面」和「右边」：是陆地就 union', INK, False),
             ('union：' + '，'.join(f'({a}, {b})' for a, b in unions), COL['red'], True),
             (f'开始 count = {m * n}，成功合并 {len(unions)} 次，剩 {m * n - len(unions)} 个集合', INK, False),
             (f'其中 {water} 个是水格子各自为一个集合，要减掉', INK, False),
             (f'岛屿数 = {m * n - len(unions)} - {water} = {m * n - len(unions) - water}', COL['grn'], True)]
    for i, (t, col, b) in enumerate(lines):
        s.text(TX, Y + 6 + i * 28, t, 13.5, col, 'start', bold=b)
    legend(s, X, Y + m * C + 12, [('new', '陆地 "1"'), ('off', '水 "0"')])
    s.text(X + 230, Y + m * C + 21, '红线 = 一次 union', 13, COL['red'], 'start', bold=True)
    s.save('lcf-uf-grid')


class _UF:
    def __init__(self, n):
        self.p = list(range(n))
        self.sz = [1] * n

    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.sz[ra] > self.sz[rb]:
            ra, rb = rb, ra
        self.p[ra] = rb
        self.sz[rb] += self.sz[ra]
        return True


def uf_redundant():
    edges = [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]
    P = {1: (0, 0), 2: (90, 0), 3: (90, 80), 4: (0, 80), 5: (-70, 40)}
    uf, s, ox, done = _UF(6), S(), 110, []
    for a, b in edges:
        ra, rb = uf.find(a), uf.find(b)
        ok = uf.union(a, b)
        s.text(ox + 20, 18, f'加边 [{a}, {b}]', 14.5, INK, bold=True)
        nodes = {k: (x, y, k, 'new' if k in (a, b) else 'n') for k, (x, y) in P.items()}
        es = [(u, v, '', None) for u, v in done] + [(a, b, '', 'org' if ok else 'red', 0 if ok else 1)]
        tree(s, ox, 66, nodes, es)
        s.text(ox + 20, 190, f'find({a}) = {ra}，find({b}) = {rb}', 13, INK, mono=True)
        s.text(ox + 20, 214, '根不同：合并' if ok else '根相同：已经连通', 13.5, COL['org'] if ok else COL['red'], bold=True)
        if not ok:
            s.text(ox + 20, 238, f'再加就成环，答案 [{a}, {b}]', 13.5, COL['red'], bold=True)
            break
        done.append((a, b))
        ox += 250
    s.save('lcf-uf-redundant')


def uf_accounts():
    accounts = [["John", "a@x", "b@x"], ["John", "c@x"], ["John", "b@x", "c@x"], ["Mary", "m@x"]]
    uf, owner, rows = _UF(len(accounts)), {}, []

    def sets():
        g = defaultdict(list)
        for i in range(len(accounts)):
            g[uf.find(i)].append(i)
        return '  '.join('{' + ', '.join(map(str, v)) + '}' for v in g.values())

    for i, acc in enumerate(accounts):
        for e in acc[1:]:
            if e in owner:
                uf.union(i, owner[e])
                what = ('t', f'见过，在账户 {owner[e]} 里：union({i}, {owner[e]})', 'red')
            else:
                owner[e] = i
                what = ('t', f'第一次见：owner["{e}"] = {i}', 'gry')
            rows.append([('t', f'账户 {i}', INK), ('t', f'"{e}"', INK), what, ('t', sets(), INK)])
    table('lcf-uf-accounts', ['当前账户', '邮箱', '发生了什么', '现在的集合（账户编号）'], [110, 100, 330, 230], rows,
          foot='账户 0: [a@x, b@x]　账户 1: [c@x]　账户 2: [b@x, c@x]　账户 3: [m@x]　→　0、1、2 是同一个人')


# ---------- Trie ----------

def _trie_layout(words, xs, dy=62):
    """Each word is its own chain under the root (words share no prefix here)."""
    nodes, edges = {'': (0, 0, 'root', 'sent')}, []
    for w, x in zip(words, xs):
        for i in range(1, len(w) + 1):
            nodes[w[:i]] = (x, i * dy, 1 if i == len(w) else '', 'hit' if i == len(w) else 'n')
            edges.append(('' if i == 1 else w[:i - 1], w[:i], w[i - 1]))
    return nodes, edges


def trie_wild():
    words = ['bad', 'dad', 'mad']
    nodes, edges = _trie_layout(words, [-90, 0, 90])
    s, ox = S(), 160
    panels = [('查 ".ad"', {'b', 'ba', 'bad'}, None,
               ['"." ：根的 3 个孩子都可以试', '先试 b：a、d 都走通，落脚处是单词', '→ True，后面的 d、m 不用再试']),
              ('查 "..e"', {'b', 'ba', 'd', 'da', 'm', 'ma'}, 'e',
               ['两个 "." ：3 条路都往下走了两步', '第 3 步要 e，三条路上都没有这条边', '全部试完都不行 → False'])]
    for title, path, miss, cap in panels:
        s.text(ox, 18, title, 15, INK, bold=True)
        nd = dict(nodes)
        es = [(a, b, c, 'org' if b in path else None) for a, b, c in edges]
        tree(s, ox, 60, nd, es)
        if miss:
            for w in words:
                x = nodes[w][0]
                s.text(ox + x - 26, 60 + 186, '✗', 16, COL['red'], bold=True)
        for i, c in enumerate(cap):
            s.text(ox, 290 + i * 23, c, 13.5, INK if i == 2 else SUB, bold=i == 2)
        ox += 360
    legend(s, 30, 372, [('hit', '有单词在这里结束'), ('new', '橙色的边 = DFS 走过的路')])
    s.save('lcf-trie-wild')


def trie_board():
    board = ["oaan", "etae", "ihkr", "iflv"]
    words = ["oath", "pea", "eat", "rain"]
    path = [(0, 0), (0, 1), (1, 1), (2, 1)]                  # o a t h
    assert ''.join(board[r][c] for r, c in path) == 'oath'
    s = S()
    X, Y, C = 40, 62, 52
    s.text(X, 20, 'board：从 (0, 0) 的 o 出发', 14.5, INK, 'start', bold=True)
    for r in range(4):
        for c in range(4):
            st = 'new' if (r, c) in path else 'chg' if (r, c) == (1, 0) else 'off'
            s.node(X + c * C, Y + r * C, board[r][c], st, w=C - 6, h=C - 6, size=17)
    for (r1, c1), (r2, c2) in zip(path, path[1:]):
        x1, y1 = X + c1 * C + (C - 6) / 2, Y + r1 * C + (C - 6) / 2
        x2, y2 = X + c2 * C + (C - 6) / 2, Y + r2 * C + (C - 6) / 2
        dx, dy = (x2 - x1) / C, (y2 - y1) / C
        s.arrow(x1 + dx * 15, y1 + dy * 15, x2 - dx * 15, y2 - dy * 15, 'org', sw=2.4)
    legend(s, X, Y + 4 * C + 10, [('new', '走出来的路 o → a → t → h')])
    legend(s, X, Y + 4 * C + 38, [('chg', 'o 下面的 e：Trie 里 o 后面没有 e，不走')])

    nodes, edges = _trie_layout(words, [-135, -45, 45, 135], dy=58)
    ox = 520
    s.text(ox, 20, 'Trie：存了 oath、pea、eat、rain', 14.5, INK, bold=True)
    hot = {'o', 'oa', 'oat', 'oath'}
    tree(s, ox, 62, nodes, [(a, b, c, 'org' if b in hot else None) for a, b, c in edges])
    s.text(ox, 62 + 4 * 58 + 44, '格子走一步，Trie 里沿同一个字母也走一步', 13.5, INK, bold=True)
    s.text(ox, 62 + 4 * 58 + 68, '走到绿色节点：找到一个单词 "oath"', 13.5, COL['grn'], bold=True)
    s.save('lcf-trie-board')


# ---------- replacements for older diagrams that showed short names ----------

def hash_buckets2():
    s = S()
    s.text(LX, 40, 'price["apple"] = 3', 14.5, INK, 'start', bold=True, mono=True)
    s.node(250, 20, '"apple"', 'n', w=96, size=14)
    s.arrow(349, 40, 396, 40)
    s.node(400, 20, '哈希函数', 'sent', w=104, size=14, mono=False)
    s.text(530, 40, '算出位置 2', 14, COL['org'], 'start', bold=True)
    X, y, W = 110, 126, 124
    s.arrow(452, 63, X + 2 * W + W / 2 - 2, y - 30, 'org')
    s.text(LX, y - 16, '位置', 13, SUB, 'start')
    for i in range(5):
        s.text(X + i * W + W / 2 - 2, y - 16, i, 13, COL['org'] if i == 2 else SUB, bold=i == 2, mono=True)
        s.node(X + i * W, y, 'apple : 3' if i == 2 else '', 'new' if i == 2 else 'off', w=W - 4, h=40, size=14)
    s.text(LX, y + 72, '查 price["apple"]：再算一次位置，还是 2，直接去 2 号拿到 3，不用一个个找。', 14, INK, 'start')
    s.text(LX, y + 98, '改 price["apple"] = 5：算出位置 2，把 2 号里的值换成 5。', 14, INK, 'start')
    s.text(LX, y + 124, '删 del price["apple"]：算出位置 2，把 2 号清空。', 14, INK, 'start')
    s.text(LX, y + 156, '（位置编号是示意，真实的由 Python 内部算）', 12.5, SUB, 'start')
    s.save('lcf-hash-buckets')


def set_venn2():
    s = S()
    for cx, col in ((170, '#2563EB'), (290, '#D97706')):
        s.e.append(f'<circle cx="{cx}" cy="120" r="95" fill="{col}" fill-opacity="0.14" stroke="{col}" stroke-width="1.8"/>')
    s.b(385, 215)
    s.text(110, 18, 'first = {1, 2, 3}', 14, COL['blue'], bold=True, mono=True)
    s.text(350, 18, 'second = {2, 3, 4}', 14, COL['org'], bold=True, mono=True)
    for x, y, v in ((115, 120, 1), (230, 104, 2), (230, 138, 3), (345, 120, 4)):
        s.text(x, y, v, 20, INK, bold=True, mono=True)
    first, second = {1, 2, 3}, {2, 3, 4}
    rows = ((f'first & second = {first & second}', '中间：两边都有'), (f'first | second = {first | second}', '三块全要'),
            (f'first - second = {first - second}', '左边：只在 first 里'))
    for i, (code, t) in enumerate(rows):
        s.text(450, 76 + i * 44, code, 14.5, INK, 'start', bold=True, mono=True)
        s.text(450, 96 + i * 44, t, 13, SUB, 'start')
    s.save('lcf-set-venn')


def group_by2():
    words, g, rows = ['apple', 'bee', 'ant', 'bat'], {}, []
    for word in words:
        isnew = word[0] not in g
        g.setdefault(word[0], []).append(word)
        row = [('t', f'"{word}"', INK),
               ('t', f'{word[0]} 不存在：自动建 []，再 append' if isnew else f'{word[0]} 已经有了：直接 append', 'org' if isnew else 'gry')]
        for k in 'ab':
            row.append([(k + ':', 'sent')] + [(v, 'new' if v == word else 'n') for v in g[k]] if k in g else '')
        rows.append(row)
    table('lcf-group-by', ['当前单词', '发生了什么', 'groups["a"]', 'groups["b"]'], [120, 300, 250, 220], rows, cw=30,
          foot='words = ["apple", "bee", "ant", "bat"]，按首字母分组：groups[word[0]].append(word)')


def uf_weighted2():
    s = S()
    X, y = 180, 20
    lab(s, y, 'find(x) 之前')
    for i, t in enumerate(('x', 'parent', 'root')):
        s.node(X + i * 190, y, t, 'new' if t == 'root' else 'n', w=74, size=14)
    s.arrow(X + 77, y + 20, X + 187, y + 20, 'line', label='dist[x] = 2', loff=-14, lsize=13)
    s.arrow(X + 190 + 77, y + 20, X + 377, y + 20, 'line', label='dist[parent] = 3', loff=-14, lsize=13)
    y += 104
    lab(s, y + 30, 'find(x) 之后')
    s.node(X, y, 'x', w=74, size=14)
    s.node(X + 190, y + 66, 'parent', w=74, size=14)
    s.node(X + 380, y + 30, 'root', 'new', w=74, size=14)
    s.arrow(X + 77, y + 22, X + 377, y + 44, 'red', label='dist[x] = 2 + 3 = 5', loff=-15, lsize=13)
    s.arrow(X + 190 + 77, y + 84, X + 377, y + 58, 'line')
    s.text(X + 190 + 140, y + 100, 'dist[parent] = 3', 13, COL['line'], 'start', bold=True)
    note(s, X + 480, y + 30, 'x 直接挂到根上，dist[x] 变成到根的距离')
    y += 150
    lab(s, y, 'union(a, b, distance)')
    xs = [X, X + 130, X + 380, X + 510]
    for x, t in zip(xs, ('a', 'root_a', 'root_b', 'b')):
        s.node(x, y, t, 'new' if t.startswith('root') else 'n', w=74, size=14)
    s.arrow(xs[0] + 77, y + 20, xs[1] - 3, y + 20, 'line')
    s.arrow(xs[1] + 77, y + 20, xs[2] - 3, y + 20, 'red', label='dist[root_a] = distance', loff=-14, lsize=13)
    s.arrow(xs[3] - 3, y + 20, xs[2] + 77, y + 20, 'line')
    note(s, xs[3] + 100, y, '只在两个根之间连一条线')
    s.save('lcf-uf-weighted')


def heap_array2():
    s = S()
    vals = [1, 3, 2, 7, 4]
    lv = {0: 'new', 1: 'n', 2: 'n', 3: 'hit', 4: 'hit'}
    s.text(145, 18, '看成一棵树', 14.5, INK, bold=True)
    heap_tree(s, 20, 62, vals, lv, idx=True)
    big_arrow(s, 300, 120, '按层排')
    s.text(520, 18, '实际存在 list 里', 14.5, INK, bold=True)
    X = 420
    for i in range(5):
        s.text(X + i * 46 + 21, 78, i, 13, SUB, mono=True)
    s.text(X - 12, 78, '下标', 13, SUB, 'end')
    cells(s, X, 94, [(v, lv[i]) for i, v in enumerate(vals)], cw=43, ch=38)
    s.text(X, 160, f'heap = {vals}', 14, INK, 'start', bold=True, mono=True)
    s.text(X, 190, '每个节点都不大于它的两个孩子，所以堆顶 heap[0] 最小', 13.5, SUB, 'start')
    legend(s, X, 214, [('new', '第 1 层'), ('n', '第 2 层'), ('hit', '第 3 层')])
    s.save('lcf-heap-array')


def heap_lazy2():
    """Same four operations as the LazyHeap class in the heap section, computed here."""
    heap, current, inserted, rows = [], {}, 0, []

    def show(styles):
        return [(f'({v},{k})', styles.get((v, k), 'n')) for v, k in sorted(heap)]

    def cur():
        return ('t', '{' + ', '.join(f'{k}: {v}' for k, v in current.items()) + '}', INK)

    for x in (5, 3):
        inserted += 1
        current[inserted] = x
        heapq.heappush(heap, (x, inserted))
        rows.append([('t', f'insert({x})', INK), show({(x, inserted): 'new'}), cur(), f'第 {inserted} 个数是 {x}'])
    current[2] = 8
    heapq.heappush(heap, (8, 2))
    rows.append([('t', 'change(2, 8)', INK), show({(3, 2): 'del', (8, 2): 'new'}), cur(), '再放一份新的，旧的 (3,2) 不删'])
    stale = [e for e in heap if current.get(e[1]) != e[0]]
    top = min(e for e in heap if e not in stale)
    assert stale == [(3, 2)] and top == (5, 1)
    rows.append([('t', 'top()', INK), show({(3, 2): 'chg', top: 'hit'}), cur(),
                 '(3,2) 和 current[2] = 8 对不上，丢掉；(5,1) 对得上，返回 5'])
    table('lcf-heap-lazy', ['操作', '堆里的 (值, 编号)，最左 = 堆顶', 'current（编号 → 现在的值）', '说明'],
          [140, 290, 240, 440], rows, cw=58,
          leg=[('del', '已经过期，但还留在堆里'), ('chg', '浮到堆顶时才丢掉'), ('hit', '有效的堆顶')])


def strhash2():
    s = S()
    X, W, y = 110, 49, 14
    s.text(LX, y + 6, '下标', 13, SUB, 'start')
    for i in range(6):
        s.text(X + i * W + 23, y + 6, i, 13, SUB, mono=True)
    y += 24
    s.text(LX, y + 19, 'text', 16, INK, 'start', bold=True, mono=True)
    cells(s, X, y, [(ch, 'chg' if i < 3 else 'hit') for i, ch in enumerate('abcabc')], cw=46, ch=38)
    y += 54
    brace(s, X + 2, X + 6 * W - 5, y, 'prefix_hash[6]：前 6 个字符 "abcabc"', 'blue', up=False)
    y += 42
    brace(s, X + 2, X + 3 * W - 5, y, 'prefix_hash[3]：要去掉的', 'red', up=False)
    brace(s, X + 3 * W + 2, X + 6 * W - 5, y, 'get(3, 5)：要的', 'grn', up=False)
    TX = X + 6 * W + 60
    s.text(TX, 50, 'get(3, 5) = prefix_hash[6] - prefix_hash[3] × BASE³', 15, INK, 'start', bold=True, mono=True)
    s.text(TX, 80, 'prefix_hash[3] 乘 BASE³：左移 3 位，和 prefix_hash[6] 的高位对齐', 13.5, SUB, 'start')
    s.text(TX, 104, '一减，前面的 "abc" 抵消，只剩后面这段', 13.5, SUB, 'start')
    s.save('lcf-strhash')


if __name__ == '__main__':
    for f in (hash_chain, longest_consec, group_anagrams, rand_set, uf_grid, uf_redundant, uf_accounts, trie_wild, trie_board,
              hash_buckets2, set_venn2, group_by2, uf_weighted2, heap_array2, heap_lazy2, strhash2):
        f()
