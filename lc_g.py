#!/usr/bin/env python3
"""Diagrams for the LeetCode parts of 图的存储 / DFS / 回溯 in 常用代码模板3 (files lcg-*.svg / lcg-*.png).

Run:  python3 lc_g.py
"""
from make_diagrams import *  # noqa: F401,F403
from make_diagrams_algo import graph, grid, inf, lines, panel_grid, row  # noqa: F401

INF = float('inf')

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))          # 下、上、右、左，和正文代码一致


# ---------- 画「选择的树」 ----------

def nd(t, st='n', e='', kids=None):
    return {'t': t, 'st': st, 'e': e, 'kids': kids or []}


def dtree(s, ox, oy, root, dy=74, gap=14, size=13.5, h=32, minw=40):
    """Lay out and draw a decision tree. Returns (right edge, bottom edge)."""
    cur = [ox]

    def width(n):
        return max(minw, tw(n['t'], size) + 18)

    def shift(n, d):
        n['x'] += d
        for k in n['kids']:
            shift(k, d)

    def place(n, d):
        n['d'], w, start = d, width(n), cur[0]
        if not n['kids']:
            n['x'] = cur[0] + w / 2
            cur[0] += w + gap
            return
        for k in n['kids']:
            place(k, d + 1)
        n['x'] = (n['kids'][0]['x'] + n['kids'][-1]['x']) / 2
        if n['x'] - w / 2 < start:                  # 自己比孩子们加起来还宽
            shift(n, start + w / 2 - n['x'])
        cur[0] = max(cur[0], n['x'] + w / 2 + gap)

    place(root, 0)
    deep = [0]

    def draw(n):
        y = oy + n['d'] * dy
        deep[0] = max(deep[0], y + h)
        for k in n['kids']:
            dead = k['st'] == 'del'
            col = 'gry' if dead else 'org' if k['st'] == 'new' else 'line'
            x1, y1, x2, y2 = n['x'], y + h + 2, k['x'], y + dy - 4
            s.arrow(x1, y1, x2, y2, col, dash=dead)
            if k['e'] != '':
                half = tw(k['e'], 13) / 2 + 7
                if abs(x2 - x1) < 5:                # 竖直的边：标在右边
                    lx, ly = x1 + half, (y1 + y2) / 2 - 3
                else:                               # 斜的边：标在靠近孩子的那一段、线的外侧上方
                    L = math.hypot(x2 - x1, y2 - y1)
                    ux, uy = (x2 - x1) / L, (y2 - y1) / L
                    px, py = (uy, -ux) if ux > 0 else (-uy, ux)     # 指向线的上方
                    outer = k is (n['kids'][-1] if ux > 0 else n['kids'][0])
                    if not outer:                   # 夹在兄弟中间的边：标在线的下方，不压到外侧兄弟的线
                        px, py = -px, -py
                    m = 10 + half * abs(uy)
                    f = 0.62 if outer else 0.42
                    lx, ly = x1 + (x2 - x1) * f + px * m, y1 + (y2 - y1) * f + py * m
                s.text(lx, ly, k['e'], 13,
                       COL['gry'] if dead else COL['org'] if col == 'org' else SUB, bold=True, mono=True)
            draw(k)
        w = width(n)
        s.node(n['x'] - w / 2, y, n['t'], n['st'], w=w, h=h, size=size)

    draw(root)
    return cur[0] - gap, deep[0]


def fmt(p):
    return '[' + ', '.join(map(str, p)) + ']'


# ---------- 图的存储 ----------

def prereq():
    s = S()
    pre = [[1, 0], [2, 0], [3, 1], [3, 2]]
    n = 4
    g = [[] for _ in range(n)]
    for a, b in pre:
        g[b].append(a)
    s.text(LX, 18, 'prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]', 14, INK, 'start', bold=True, mono=True)
    s.text(LX, 44, '[a, b] 的意思：想学 a，要先学 b   →   边的方向是 b → a（先学的指向后学的）', 13.5, COL['org'], 'start', bold=True)
    pos = {0: (0, 60), 1: (110, 0), 2: (110, 120), 3: (220, 60)}
    graph(s, 50, 96, pos, [(b, a) for a, b in pre])
    ax = 360
    s.text(ax, 78, '建出来的邻接表：graph[b].append(a)', 14, INK, 'start', bold=True)
    for a in range(n):
        y = 100 + a * 40
        s.text(ax, y + 17, f'graph[{a}]', 14, INK, 'start', bold=True, mono=True)
        s.arrow(ax + 76, y + 17, ax + 102, y + 17, 'gry')
        if g[a]:
            row(s, ax + 110, y, g[a], 'n', cw=40)
        else:
            s.text(ax + 112, y + 17, '空', 13.5, COL['gry'], 'start')
    s.text(LX, 262, 'graph[0] = [1, 2]：学完 0 才能学 1 和 2。方向写反，拓扑排序出来的顺序就是倒的', 13.5, SUB, 'start')
    s.save('lcg-prereq')


def clone():
    s = S()
    pos = {1: (0, 0), 2: (110, 0), 3: (110, 100), 4: (0, 100)}
    E = [(1, 2), (2, 3), (3, 4), (4, 1)]
    s.text(LX, 18, '原图：只拿到节点 1', 14.5, INK, 'start', bold=True)
    graph(s, 50, 70, pos, E, {1: 'hit'}, directed=False)
    mx = 240
    s.text(mx, 18, 'copies：旧节点 → 新节点', 14.5, INK, 'start', bold=True)
    for k in range(4):
        y = 52 + k * 36
        s.circ(mx + 20, y, k + 1, 'n', r=14, size=13)
        s.arrow(mx + 42, y, mx + 92, y, 'org', dash=1)
        s.circ(mx + 112, y, f"{k + 1}'", 'new', r=14, size=12)
    rx = 470
    s.text(rx, 18, '新图：全是新建的节点', 14.5, INK, 'start', bold=True)
    graph(s, rx + 30, 70, pos, E, {v: 'new' for v in pos}, directed=False, names={v: f"{v}'" for v in pos})
    lines(s, LX, 216, [('dfs(node)：node 已经在 copies 里，直接返回那个新节点；', INK, False),
                       ('否则新建一个，先记进 copies，再把每个邻居 dfs 一遍，返回值接到新节点的 neighbors 上', INK, False),
                       ('copies 同时是 visited：走回 1 时，1 已经在字典里，直接拿到 1′，不会绕圈', 'org')], gap=24)
    s.save('lcg-clone')


def implicit():
    s = S()
    words = ['hot', 'dot', 'dog', 'lot', 'log', 'cog']
    begin, end = 'hit', 'cog'
    pos = {'hit': (0, 60), 'hot': (120, 60), 'dot': (240, 0), 'lot': (240, 120), 'dog': (360, 0), 'log': (360, 120),
           'cog': (480, 60)}
    allw = [begin] + words

    def adj(a, b):
        return sum(x != y for x, y in zip(a, b)) == 1

    # 真的跑一遍 BFS，算每个词在第几层
    dist = {begin: 1}
    q = deque([begin])
    while q:
        u = q.popleft()
        for v in allw:
            if v not in dist and adj(u, v):
                dist[v] = dist[u] + 1
                q.append(v)
    ox, oy, w, h = 40, 90, 62, 34
    s.text(LX, 18, "begin = 'hit'，end = 'cog'，词表 = ['hot', 'dot', 'dog', 'lot', 'log', 'cog']", 13.5, INK, 'start',
           bold=True, mono=True)
    s.text(LX, 44, '题目没有给边。规则是：两个单词只差一个字母，就算相邻', 13.5, COL['org'], 'start', bold=True)
    for i, a in enumerate(allw):
        for b in allw[i + 1:]:
            if adj(a, b):
                (x1, y1), (x2, y2) = pos[a], pos[b]
                if y1 == y2:
                    s.seg(ox + min(x1, x2) + w + 2, oy + y1 + h / 2, ox + max(x1, x2) - 2, oy + y1 + h / 2)
                elif x1 == x2:
                    s.seg(ox + x1 + w / 2, oy + min(y1, y2) + h + 2, ox + x1 + w / 2, oy + max(y1, y2) - 2)
                else:
                    if x1 > x2:
                        (x1, y1), (x2, y2) = (x2, y2), (x1, y1)
                    s.seg(ox + x1 + w + 2, oy + y1 + h / 2, ox + x2 - 2, oy + y2 + h / 2)
    for t, (x, y) in pos.items():
        s.node(ox + x, oy + y, t, 'hit' if t == begin else 'new' if t == end else 'n', w=w, h=h, size=14)
        s.text(ox + x + w / 2, oy + y - 13 if y == 0 else oy + y + h + 13, f'第 {dist[t]} 层', 12, SUB)
    s.text(LX, 290, f'点 = 单词，边 = 只差一个字母。BFS 一层层走，cog 在第 {dist[end]} 层，答案就是 {dist[end]}', 13.5, SUB, 'start')
    s.save('lcg-implicit')


# ---------- DFS ----------

def sink():
    g0 = ['1100', '1001', '0000', '0100']
    R, C = 4, 4
    g = [list(r) for r in g0]
    snaps = [([r[:] for r in g], set(), '开始', ['按行扫描，找值是 1 的格子'])]

    def dfs(x, y, got):
        g[x][y] = '0'
        got.append((x, y))
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < R and 0 <= ny < C and g[nx][ny] == '1':
                dfs(nx, ny, got)

    count = 0
    for x in range(R):
        for y in range(C):
            if g[x][y] == '1':
                got = []
                dfs(x, y, got)
                count += 1
                snaps.append(([r[:] for r in g], set(got), f'扫到 ({x}, {y})：count = {count}',
                              [f'dfs 淹掉 {len(got)} 格：', ' '.join(f'({a},{b})' for a, b in got)]))

    def draw(s, ox, oy, k):
        cur, got, _, cap = snaps[k]
        grid(s, ox + 6, oy, cur, lambda i, j: 'new' if (i, j) in got else 'n' if cur[i][j] == '1' else 'off', cw=40, size=15)
        lines(s, ox, oy + 180, cap, size=13, gap=20)

    panel_grid('lcg-sink', len(snaps), 208, 262, draw, titles=[x[2] for x in snaps],
               leg=[('n', '陆地 1'), ('new', '这一次 dfs 刚淹掉的（改成 0）'), ('off', '水 0')],
               foot=f'扫完整张图，dfs 一共被外层循环调了 {count} 次，所以是 {count} 个岛')


def area():
    s = S()
    g = [[0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 1]]
    R, C = 4, 4
    seen = set()

    def dfs(x, y, node):
        seen.add((x, y))
        a = 1
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < R and 0 <= ny < C and g[nx][ny] == 1 and (nx, ny) not in seen:
                kid = nd('', e='')
                node['kids'].append(kid)
                a += dfs(nx, ny, kid)
        node['t'] = f'dfs({x}, {y}) 返回 {a}'
        return a

    isl = []
    for x in range(R):
        for y in range(C):
            if g[x][y] == 1 and (x, y) not in seen:
                before = set(seen)
                root = nd('', 'hit')
                isl.append((root, dfs(x, y, root), seen - before))
    s.text(LX, 18, 'grid', 14.5, INK, 'start', bold=True, mono=True)
    stm = {}
    for k, (_, _, cs) in enumerate(isl):
        for c in cs:
            stm[c] = ('n', 'new')[k]
    for k in range(4):
        s.text(40 + k * 44 + 20, 44, k, 12, SUB, mono=True)
        s.text(26, 58 + k * 44 + 20, k, 12, SUB, mono=True)
    grid(s, 40, 58, g, lambda i, j: stm.get((i, j), 'off'), cw=44, size=15)
    tx = 270
    s.text(tx, 18, '第一个岛：每个格子返回「从我这里新淹掉了几格」', 14.5, INK, 'start', bold=True)
    dtree(s, tx, 48, isl[0][0], dy=66, gap=18)
    lines(s, tx, 250, [('返回值 = 1（自己）+ 四个方向的返回值之和', INK),
                       '出界、是水、已经淹掉的方向不进去，相当于加 0，图里没画'], gap=22)
    s.text(LX, 306, f'蓝色的岛面积 {isl[0][1]}，橙色的岛面积 {isl[1][1]}，答案取最大的：{max(a for _, a, _ in isl)}', 13.5,
           COL['org'], 'start', bold=True)
    s.save('lcg-area')


def border():
    b0 = ['XXXX', 'XOOX', 'XXOX', 'XOXX']
    R, C = 4, 4
    b = [list(r) for r in b0]

    def dfs(x, y):
        b[x][y] = '#'
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < R and 0 <= ny < C and b[nx][ny] == 'O':
                dfs(nx, ny)

    for x in range(R):
        for y in range(C):
            if (x in (0, R - 1) or y in (0, C - 1)) and b[x][y] == 'O':
                dfs(x, y)
    mid = [r[:] for r in b]
    for x in range(R):
        for y in range(C):
            b[x][y] = 'O' if b[x][y] == '#' else 'X'
    snaps = [([list(r) for r in b0], lambda i, j: 'new' if b0[i][j] == 'O' else 'off',
              ['直接判断「被围住」不好写；', '反过来找「没被围住」的 O：', '就是和边界上的 O 连着的那些']),
             (mid, lambda i, j: 'hit' if mid[i][j] == '#' else 'new' if mid[i][j] == 'O' else 'off',
              ['边界上只有 (3, 1) 是 O，', '从它出发 dfs，走到的都标成 #', '（这里只有它自己）']),
             (b, lambda i, j: 'hit' if mid[i][j] == '#' else 'chg' if mid[i][j] == 'O' else 'off',
              ['全图扫一遍：', '还是 O 的（被围住）→ 改成 X', '是 # 的（没被围住）→ 改回 O'])]

    def draw(s, ox, oy, k):
        data, st, cap = snaps[k]
        grid(s, ox + 20, oy, data, st, cw=44, size=16)
        lines(s, ox, oy + 196, cap, size=13, gap=20)

    panel_grid('lcg-border', 3, 250, 300, draw, titles=['① 原图', '② 从边界上的 O 出发，标记', '③ 按标记改写'],
               leg=[('new', 'O'), ('hit', '和边界连着，保留'), ('chg', '被围住，改成 X')])


def pacific():
    hs = [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]
    R, C = 5, 5

    def reach(starts):
        seen = set()

        def dfs(x, y):
            seen.add((x, y))
            for dx, dy in DIRS:
                nx, ny = x + dx, y + dy
                if 0 <= nx < R and 0 <= ny < C and (nx, ny) not in seen and hs[nx][ny] >= hs[x][y]:
                    dfs(nx, ny)

        for x, y in starts:
            if (x, y) not in seen:
                dfs(x, y)
        return seen

    pac = reach([(0, y) for y in range(C)] + [(x, 0) for x in range(R)])
    atl = reach([(R - 1, y) for y in range(C)] + [(x, C - 1) for x in range(R)])
    both = pac & atl
    sets = [(pac, 'n', f'从上边、左边出发往高处走：{len(pac)} 格'), (atl, 'new', f'从下边、右边出发往高处走：{len(atl)} 格'),
            (both, 'hit', f'两次都走到的格子：{len(both)} 格，就是答案')]

    def draw(s, ox, oy, k):
        st, col, cap = sets[k]
        grid(s, ox + 10, oy, hs, lambda i, j: col if (i, j) in st else 'off', cw=40, size=15)
        s.text(ox, oy + 218, cap, 13, INK, 'start')

    panel_grid('lcg-pacific', 3, 250, 290, draw, titles=['① 能流到太平洋的格子', '② 能流到大西洋的格子', '③ 取交集'],
               foot='水从高往低流；倒过来从海边出发，只往「不比当前低」的格子走，走到的就是能流进这片海的格子')


def provinces():
    s = S()
    n, E = 5, [(0, 1), (1, 2), (3, 4)]
    M = [[1 if i == j or (i, j) in E or (j, i) in E else 0 for j in range(n)] for i in range(n)]
    seen, comp = [False] * n, {}

    def dfs(u, c):
        seen[u] = True
        comp[u] = c
        for v in range(n):
            if M[u][v] == 1 and not seen[v]:
                dfs(v, c)

    cnt = 0
    for i in range(n):
        if not seen[i]:
            dfs(i, cnt)
            cnt += 1
    s.text(LX, 18, 'isConnected', 14.5, INK, 'start', bold=True, mono=True)
    mx, my, cw = 46, 62, 38
    for k in range(n):
        s.text(mx + k * cw + 17, my - 14, k, 13, SUB, bold=True, mono=True)
        s.text(mx - 16, my + k * cw + 17, k, 13, SUB, bold=True, mono=True)
    grid(s, mx, my, M, lambda i, j: 'sent' if i == j else ('n', 'new')[comp[i]] if M[i][j] else 'off', cw=cw)
    gx = 320
    s.text(gx, 18, '同一张图画出来', 14.5, INK, 'start', bold=True)
    pos = {0: (0, 0), 1: (80, 60), 2: (0, 120), 3: (190, 20), 4: (190, 110)}
    graph(s, gx + 30, 80, pos, E, {v: ('n', 'new')[comp[v]] for v in pos}, directed=False)
    lines(s, LX, 276, [('第 i 行就是 i 的邻居表：isConnected[i][j] == 1 的那些 j（对角线是自己连自己，不用管）', INK, False),
                       (f'外层循环调了 {cnt} 次 dfs：{{0, 1, 2}} 一个省，{{3, 4}} 一个省，答案 {cnt}', 'org')], gap=24)
    s.save('lcg-provinces')


def diameter():
    s = S()
    kids = {1: (2, 3), 2: (4, 5), 3: (None, None), 4: (None, None), 5: (None, None)}
    info, best = {}, [0]

    def depth(v):
        if v is None:
            return 0
        l, r = depth(kids[v][0]), depth(kids[v][1])
        best[0] = max(best[0], l + r)
        info[v] = (l, r, 1 + max(l, r))
        return info[v][2]

    depth(1)
    pos = {1: (150, 0), 2: (80, 80), 3: (220, 80), 4: (30, 160), 5: (130, 160)}
    path = [(4, 2), (2, 1), (1, 3)]
    E = [(a, b, '', 'org' if (b, a) in path or (a, b) in path else 'line')
         for a, (l, r) in kids.items() for b in (l, r) if b]
    s.text(LX, 18, 'depth(node) 返回：以 node 为根的子树有几层', 14.5, INK, 'start', bold=True)
    graph(s, 130, 76, pos, E, {v: 'n' for v in pos}, directed=False)
    for v, (x, y) in pos.items():
        l, r, d = info[v]
        side = -1 if v in (2, 4) else 1
        s.text(130 + x + side * 26, 76 + y - 9, f'返回 {d}', 12.5, COL['grn'], 'end' if side < 0 else 'start', bold=True)
        s.text(130 + x + side * 26, 76 + y + 9, f'左{l} + 右{r} = {l + r}', 12.5, COL['red'] if l + r == best[0] else SUB,
               'end' if side < 0 else 'start', bold=l + r == best[0])
    tx = 500
    lines(s, tx, 70, [('绿色：返回给父节点的值', 'grn'), '    1 + max(左子树层数, 右子树层数)',
                      ('灰色 / 红色：在这个点「拐弯」的最长路径', 'red'), '    左子树层数 + 右子树层数（边数）',
                      ('全局答案 = 所有点里「左 + 右」最大的', INK),
                      (f'这里是节点 1：{info[1][0]} + {info[1][1]} = {best[0]}，路径 4 → 2 → 1 → 3（橙色）', 'org')], gap=25)
    s.text(LX, 282, '返回值和答案不是同一个东西：返回的是「一条腿」的长度，答案要的是「两条腿」加起来', 13.5, SUB, 'start')
    s.save('lcg-diameter')


# ---------- 回溯 ----------

def subset_tree():
    s = S()
    nums = [1, 2, 3]

    def bt(start, path):
        node = nd(fmt(path), 'hit')
        for i in range(start, len(nums)):
            k = bt(i + 1, path + [nums[i]])
            k['e'] = str(nums[i])
            node['kids'].append(k)
        return node

    root = bt(0, [])
    s.text(LX, 18, 'nums = [1, 2, 3]：每个节点都是一个子集（共 8 个）', 14.5, INK, 'start', bold=True)
    _, bot = dtree(s, 30, 44, root, gap=22)
    lines(s, LX, bot + 28, [('边上的数字 = 这一步选了谁。只能选「上一个选的数」后面的：选了 2 之后只能再选 3，不能回头选 1', INK),
                            ('所以 [1, 2] 出现了，[2, 1] 不会出现。子集不讲顺序，这样每个子集正好出现一次', 'org')], gap=24)
    s.save('lcg-subset-tree')


def perm_dedupe():
    s = S()
    nums = [1, 1, 2]
    n = len(nums)
    used = [False] * n

    def bt(path):
        node = nd(fmt(path), 'hit' if len(path) == n else 'n')
        for i in range(n):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                node['kids'].append(nd('✗', 'del', f'i={i}'))
                continue
            used[i] = True
            k = bt(path + [nums[i]])
            used[i] = False
            k['e'] = f'i={i}'
            node['kids'].append(k)
        return node

    root = bt([])
    s.text(LX, 18, 'nums = [1, 1, 2]（已排序）。边上写的是选了哪个下标：i=0 和 i=1 都是 1', 14.5, INK, 'start', bold=True)
    _, bot = dtree(s, 30, 44, root, gap=26)
    lines(s, LX, bot + 28, [('✗：nums[i] == nums[i-1]，而且 nums[i-1] 现在没被用（not used[i-1]）→ 跳过', 'red'),
                            ('意思是：同一层里，前一个 1 已经试过并撤销了，再拿后一个 1 放在这个位置，得到的排列一模一样', INK, False),
                            ('最左边那条路上 i=1 没被剪：那时 i=0 正在用（used[0] 是 True），两个 1 是放在不同位置', INK, False)], gap=24)
    s.save('lcg-perm-dedupe')


def subset_dedupe():
    s = S()
    nums = [1, 2, 2]

    def bt(start, path):
        node = nd(fmt(path), 'hit')
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                node['kids'].append(nd('✗', 'del', f'i={i}'))
                continue
            k = bt(i + 1, path + [nums[i]])
            k['e'] = f'i={i}'
            node['kids'].append(k)
        return node

    root = bt(0, [])
    s.text(LX, 18, 'nums = [1, 2, 2]（已排序）。边上写的是选了哪个下标：i=1 和 i=2 都是 2', 14.5, INK, 'start', bold=True)
    _, bot = dtree(s, 30, 44, root, gap=26)
    lines(s, LX, bot + 28, [('✗：i > start 而且 nums[i] == nums[i-1] → 跳过', 'red'),
                            ('i > start 说明 i 不是这一层试的第一个；它和前一个一样，前一个刚试过，再试就重复', INK, False),
                            ('[1, 2, 2]、[2, 2] 没被剪：第二个 2 是下一层的第一个选择（i == start），是「接着往下选」', INK, False)], gap=24)
    s.save('lcg-subset-dedupe')


def combsum_tree():
    s = S()
    cand, target = [2, 3, 6, 7], 7

    def bt(start, remain, path):
        node = nd(f'剩 {remain}', 'hit' if remain == 0 else 'n')
        if remain == 0:
            node['t'] = f'剩 0 ✓ {fmt(path)}'
            return node
        for i in range(start, len(cand)):
            if cand[i] > remain:
                node['kids'].append(nd('✗', 'del', str(cand[i])))
                break
            k = bt(i, remain - cand[i], path + [cand[i]])
            k['e'] = str(cand[i])
            node['kids'].append(k)
        return node

    root = bt(0, target, [])
    s.text(LX, 18, 'candidates = [2, 3, 6, 7]（已排序），target = 7。节点里是还差多少，边上是选了谁', 14.5, INK, 'start', bold=True)
    _, bot = dtree(s, 30, 44, root, gap=18, dy=68)
    lines(s, LX, bot + 28, [('可以重复选：选了 2 之后，下一层还是从 2 开始（传 i，不是 i + 1）', 'org'),
                            ('✗：这个数比剩下的还大。数组排过序，后面的更大，直接 break，后面的都不用试', INK, False),
                            ('剩 0 就是一个答案：[2, 2, 3] 和 [7]', 'grn')], gap=24)
    s.save('lcg-combsum-tree')


def paren_tree():
    s = S()
    n = 2

    def bt(cur, op, cl):
        node = nd(cur or '空', 'hit' if len(cur) == 2 * n else 'n')
        if len(cur) == 2 * n:
            return node
        for ch, ok in (('(', op < n), (')', cl < op)):
            if ok:
                k = bt(cur + ch, op + (ch == '('), cl + (ch == ')'))
                k['e'] = ch
                node['kids'].append(k)
            else:
                node['kids'].append(nd('✗', 'del', ch))
        return node

    root = bt('', 0, 0)
    s.text(LX, 18, 'n = 2：一共 4 个位置，每个位置填 ( 或 )', 14.5, INK, 'start', bold=True)
    _, bot = dtree(s, 60, 44, root, gap=30, dy=64, minw=46)
    lines(s, LX, bot + 28, [('填 ( 的条件：已经用的左括号 < n', INK), ('填 ) 的条件：已经用的右括号 < 已经用的左括号', INK),
                            ('✗ 是不满足条件、根本不往下走的分支。剩下的路走到底都是合法的：(()) 和 ()()', 'org')], gap=24)
    s.save('lcg-paren-tree')


def palin_tree():
    s = S()
    w = 'aab'

    def bt(start, path):
        node = nd(' | '.join(path) if path else '空', 'hit' if start == len(w) else 'n')
        for end in range(start + 1, len(w) + 1):
            piece = w[start:end]
            if piece != piece[::-1]:
                node['kids'].append(nd('✗', 'del', piece))
                continue
            k = bt(end, path + [piece])
            k['e'] = piece
            node['kids'].append(k)
        return node

    root = bt(0, [])
    s.text(LX, 18, "s = 'aab'：每一层决定「下一段切到哪」，边上是切下来的那一段", 14.5, INK, 'start', bold=True)
    _, bot = dtree(s, 40, 44, root, gap=30, dy=66, minw=46)
    lines(s, LX, bot + 28, [('✗：切下来的这一段不是回文，剪掉', 'red'),
                            ('切到字符串末尾就是一个答案：a | a | b 和 aa | b', 'grn')], gap=24)
    s.save('lcg-palin-tree')


def word_search():
    board = ['ABCE', 'SFCS', 'ADEE']
    R, C = 3, 4

    def run(word):
        """返回 (找到没有, 最后的路径, 失败时走得最远的路径)"""
        b = [list(r) for r in board]
        path, far = [], []

        def dfs(x, y, k):
            nonlocal far
            if b[x][y] != word[k]:
                return False
            path.append((x, y))
            if len(path) > len(far):
                far = path[:]
            if k == len(word) - 1:
                return True
            b[x][y] = '#'
            for dx, dy in DIRS:
                nx, ny = x + dx, y + dy
                if 0 <= nx < R and 0 <= ny < C and dfs(nx, ny, k + 1):
                    return True
            b[x][y] = word[k]
            path.pop()
            return False

        ok = any(dfs(x, y, 0) for x in range(R) for y in range(C))
        return ok, path[:], far

    ok1, p1, _ = run('ABCCED')
    ok2, _, far2 = run('ABCB')
    assert ok1 and not ok2
    cw = 46
    snaps = [(p1, None, "word = 'ABCCED'：找到", ['格子右下角的数字是第几步走到的', '走过的格子临时改成 #，这条路不会再踩它']),
             (far2, None, "word = 'ABCB'：找不到", ['走到 C 之后要找 B：', 'C 四周唯一的 B 就是第 2 步踩过的那个，', '它现在是 #，不能再用 → 返回 False'])]

    def draw(s, ox, oy, k):
        path, _, _, cap = snaps[k]
        order = {c: i + 1 for i, c in enumerate(path)}
        grid(s, ox + 10, oy, [list(r) for r in board], lambda i, j: 'new' if (i, j) in order else 'off', cw=cw, size=16)
        for (i, j), o in order.items():
            s.text(ox + 10 + j * cw + cw - 11, oy + i * cw + cw - 12, o, 10.5, COL['org'], bold=True, mono=True)
        for a, b2 in zip(path, path[1:]):
            x1, y1 = ox + 10 + a[1] * cw + (cw - 3) / 2, oy + a[0] * cw + (cw - 3) / 2
            x2, y2 = ox + 10 + b2[1] * cw + (cw - 3) / 2, oy + b2[0] * cw + (cw - 3) / 2
            ux, uy = (x2 - x1) / cw, (y2 - y1) / cw
            s.arrow(x1 + ux * 14 - 12 * abs(uy), y1 + uy * 14 - 9 * abs(ux), x2 - ux * 14 - 12 * abs(uy), y2 - uy * 14 - 9 * abs(ux), 'org')
        lines(s, ox, oy + 160, cap, size=13, gap=20)

    panel_grid('lcg-word-search', 2, 330, 262, draw, titles=[x[2] for x in snaps])


def unmark():
    board, word = ['ABB'], 'BBA'
    C = 3
    b = list(board[0])
    snaps = []

    def dfs(y, k, undo):
        if b[y] != word[k]:
            return False
        if k == len(word) - 1:
            return True
        b[y] = '#'
        found = False
        for dy in (1, -1):                          # 右、左
            ny = y + dy
            if 0 <= ny < C and dfs(ny, k + 1, undo):
                found = True
                break
        if undo:
            b[y] = word[k]
        return found

    res = {}
    for undo in (False, True):
        b[:] = list(board[0])
        log = []
        for y in range(C):
            before = b[:]
            ok = dfs(y, 0, undo)
            log.append((y, before, b[:], ok))
            if ok:
                break
        res[undo] = log
    assert not res[False][-1][3] and res[True][-1][3]
    s = S()
    s.text(LX, 18, "board = [['A', 'B', 'B']]，word = 'BBA'。正确的路是：下标 2 → 1 → 0", 14.5, INK, 'start', bold=True)
    for k, undo in enumerate((False, True)):
        ox = LX + k * 400
        s.text(ox, 52, '不撤销：答案错' if not undo else '撤销：答案对', 14.5, COL['red'] if not undo else COL['grn'], 'start', bold=True)
        y = 76
        for st, before, after, ok in res[undo]:
            s.text(ox, y + 17, f'从下标 {st} 出发', 13, INK, 'start')
            row(s, ox + 100, y, before, ['sent' if c == '#' else 'n' for c in before], cw=38)
            s.arrow(ox + 222, y + 17, ox + 246, y + 17, 'gry')
            row(s, ox + 254, y, after, ['sent' if c == '#' else 'n' for c in after], cw=38)
            s.text(ox + 254 + 3 * 38 + 6, y + 17, '✓' if ok else '✗', 15, COL['grn'] if ok else COL['red'], 'start', bold=True)
            y += 46
    s.text(LX + 100, 222, '出发前', 12, SUB, 'start')
    s.text(LX + 254, 222, '返回后', 12, SUB, 'start')
    lines(s, LX, 250, [('从下标 1 出发：先往右踩到下标 2，再往后没路，失败。这条路上踩过的两个 B 都被标成了 #', INK, False),
                       ('不撤销：# 留在棋盘上，轮到从下标 2 出发时，它自己就是 #，正确的路被堵死', 'red'),
                       ('撤销：返回前把 # 改回原来的字母，棋盘恢复原样，下一条路不受影响', 'grn')], gap=24)
    s.save('lcg-unmark')


# ---------- 替换旧图里的旧变量名（gr-store / gr-prim / gr-hungarian） ----------

def store():
    s = S()
    n, E = 4, [(0, 1), (0, 2), (1, 3)]
    adj = [[] for _ in range(n)]
    M = [[0] * n for _ in range(n)]
    for a, b in E:
        adj[a].append(b)
        adj[b].append(a)
        M[a][b] = M[b][a] = 1
    s.text(LX, 18, '图', 14.5, INK, 'start', bold=True)
    graph(s, 40, 62, {0: (60, 0), 1: (20, 70), 2: (100, 70), 3: (20, 140)}, E, directed=False)
    ax = 230
    s.text(ax, 18, '邻接表：graph[a] = a 的邻居', 14.5, INK, 'start', bold=True)
    for a in range(n):
        y = 46 + a * 44
        s.text(ax, y + 17, f'graph[{a}]', 14, INK, 'start', bold=True, mono=True)
        s.arrow(ax + 76, y + 17, ax + 102, y + 17, 'gry')
        row(s, ax + 110, y, adj[a], 'n', cw=40)
    mx = 520
    s.text(mx, 18, '邻接矩阵：graph[a][b] = 1 表示 a、b 之间有边', 14.5, INK, 'start', bold=True)
    for k in range(n):
        s.text(mx + 36 + k * 38 + 17, 48, k, 13, SUB, bold=True, mono=True)
        s.text(mx + 16, 62 + k * 38 + 17, k, 13, SUB, bold=True, mono=True)
    grid(s, mx + 36, 62, M, lambda i, j: 'new' if M[i][j] else 'off', cw=38)
    s.text(LX, 244, '无向边 0–1 存两次：邻接表里 graph[0] 有 1、graph[1] 有 0；矩阵里 graph[0][1] 和 graph[1][0] 都是 1',
           13.5, SUB, 'start')
    s.save('lcg-store')


def prim():
    n = 4
    pos = {0: (0, 0), 1: (130, 0), 2: (0, 110), 3: (130, 110)}
    E = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (1, 3, 6), (2, 3, 3)]
    mat = [[INF] * n for _ in range(n)]
    for a, b, weight in E:
        mat[a][b] = mat[b][a] = weight
    dist, via = [INF] * n, [None] * n
    dist[0] = 0
    in_tree, total, tree_e = [False] * n, 0, set()
    states = [(dist[:], set(), None, set(), set(), ['从 0 号点开始', 'total = 0'])]
    for _ in range(n):
        node = -1
        for j in range(n):
            if not in_tree[j] and (node == -1 or dist[j] < dist[node]):
                node = j
        in_tree[node] = True
        total += dist[node]
        if via[node] is not None:
            tree_e.add((via[node], node))
        upd = set()
        for j in range(n):                          # 和正文模板一样：不管 j 连没连上都更新
            if mat[node][j] < dist[j]:
                dist[j], via[j] = mat[node][j], node
                upd.add(j)
        cap = [f'挑中 {node}（边长 {dist[node]}），total = {total}',
               '更新：' + ('，'.join(f'{j} 变成 {dist[j]}' for j in sorted(upd)) if upd else '没有')]
        states.append((dist[:], {j for j in range(n) if in_tree[j]}, node, upd, set(tree_e), cap))

    def draw(s, ox, oy, k):
        dist, it, node, upd, te, cap = states[k]
        es = [(a, b, c, 'grn' if (a, b) in te or (b, a) in te else 'line') for a, b, c in E]
        st = {j: 'new' if j == node else 'hit' if j in it else 'n' for j in range(n)}
        tag = {j: (f'dist={inf(dist[j])}', 'red' if j in upd else INK, 't' if j < 2 else 'b') for j in range(n)}
        graph(s, ox + 36, oy + 36, pos, es, st, tag, directed=False)
        lines(s, ox, oy + 196, cap, size=13, gap=20)

    panel_grid('lcg-prim', 5, 222, 280, draw, titles=['开始'] + [f'第 {k} 轮' for k in range(1, 5)],
               leg=[('new', '这一轮接进来的点'), ('hit', '已经连好的那一团')],
               foot=f'dist = 这个点到「已经连好的那一团」最短的一条边；绿色的边 = 选中的边，总和 {total}')


def hungarian():
    Eg = [(0, 0), (0, 1), (1, 0), (2, 1), (2, 2)]
    adj = [[] for _ in range(3)]
    for a, b in Eg:
        adj[a].append(b)
    match = [-1] * 3
    snaps = [({}, set(), None)]

    def try_match(left_node, seen):
        for right_node in adj[left_node]:
            if right_node in seen:
                continue
            seen.add(right_node)
            if match[right_node] == -1 or try_match(match[right_node], seen):
                match[right_node] = left_node
                return True
        return False

    for left_node in range(3):
        before = {match[r]: r for r in range(3) if match[r] != -1}
        assert try_match(left_node, set())
        after = {match[r]: r for r in range(3) if match[r] != -1}
        snaps.append((after, {(a, b) for a, b in before.items() if after.get(a) != b}, left_node))
    caps = [['灰线 = 可以配对', '左边的点一个一个来找对象'], ['左 0：右 0 没人', '直接配上'],
            ['左 1 只能配右 0，被左 0 占着', '问左 0：能换成右 1 → 右 0 让给左 1'],
            ['左 2：右 1 被左 0 占着，谁都换不了', f'改试右 2，没人，配上 → 共 {sum(m != -1 for m in match)} 对']]
    assert snaps[2][0] == {0: 1, 1: 0} and snaps[3][0] == {0: 1, 1: 0, 2: 2}

    def draw(s, ox, oy, k):
        m, moved, cur = snaps[k]
        for a, b in Eg:
            x1, y1, x2, y2 = ox + 76, oy + 27 + a * 58, ox + 164, oy + 27 + b * 58
            if m.get(a) == b:
                s.seg(x1, y1, x2, y2, 'grn', sw=3.5)
            elif (a, b) in moved:
                s.seg(x1, y1, x2, y2, 'red', dash=1, sw=2)
            else:
                s.seg(x1, y1, x2, y2, '#CBD5E1', sw=1.6)
        for i in range(3):
            s.node(ox + 20, oy + 10 + i * 58, f'左 {i}', 'new' if i == cur else 'hit' if i in m else 'n', w=54, h=34,
                   size=14, mono=False)
            s.node(ox + 166, oy + 10 + i * 58, f'右 {i}', 'hit' if i in m.values() else 'n', w=54, h=34, size=14, mono=False)
        lines(s, ox, oy + 190, caps[k], size=13, gap=20)
        cur_match = [next((a for a, b in m.items() if b == r), -1) for r in range(3)]
        s.text(ox, oy + 236, f'match = {cur_match}', 12.5, COL['grn'], 'start', bold=True, mono=True)

    panel_grid('lcg-hungarian', 4, 262, 300, draw, titles=['能连的边', '轮到左 0', '轮到左 1', '轮到左 2'],
               foot='绿线 = 现在的配对；红虚线 = 被让出去的旧配对；match[right_node] = 右边这个点现在配的是左边的谁')


if __name__ == '__main__':
    store()
    prim()
    hungarian()
    prereq()
    clone()
    implicit()
    sink()
    area()
    border()
    pacific()
    provinces()
    diameter()
    subset_tree()
    perm_dedupe()
    subset_dedupe()
    combsum_tree()
    paren_tree()
    palin_tree()
    word_search()
    unmark()
    print('ok')
