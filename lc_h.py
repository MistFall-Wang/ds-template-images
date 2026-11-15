#!/usr/bin/env python3
"""LeetCode 套法 diagrams for BFS / 拓扑排序 / 堆优化 Dijkstra / Kruskal in
常用代码模板3——搜索与图论（Python版）.md  (files lch-*.svg / lch-*.png).

Run:  python3 lc_h.py
"""
from make_diagrams_graph import *  # noqa: F401,F403  (S, graph, grid, table, lines, panel_grid, ...)

D4 = ((1, 0), (-1, 0), (0, 1), (0, -1))


# ---------- BFS ----------

def bfs_mark():
    """入队时标记 vs 出队时标记，菱形图 0→1, 0→2, 1→3, 2→3。"""
    E = [(0, 1), (0, 2), (1, 3), (2, 3)]
    g = {u: [b for a, b in E if a == u] for u in range(4)}

    def run(at_push):
        seen, q = ({0} if at_push else set()), deque([0])
        rows = [('开始', list(q))]
        while q:
            u = q.popleft()
            if not at_push:
                seen.add(u)
            for v in g[u]:
                if v not in seen:
                    if at_push:
                        seen.add(v)
                    q.append(v)
            rows.append((f'取出 {u}', list(q)))
        return rows

    s = S()
    s.text(LX, 18, '图', 14.5, INK, 'start', bold=True)
    graph(s, 44, 96, {0: (0, 50), 1: (80, 0), 2: (80, 100), 3: (160, 50)}, E)
    for k, (title, col, rows) in enumerate((('入队时标记（对）', 'grn', run(True)), ('出队时才标记（错）', 'red', run(False)))):
        x = 280 + k * 300
        s.text(x, 18, title, 14.5, COL[col], 'start', bold=True)
        s.text(x, 44, '操作', 12.5, SUB, 'start', bold=True)
        s.text(x + 78, 44, '操作后的队列', 12.5, SUB, 'start', bold=True)
        for i, (op, q) in enumerate(rows):
            y = 62 + i * 42
            s.text(x, y + 17, op, 14, INK, 'start')
            dup = {v for v in q if q.count(v) > 1}
            cells(s, x + 78, y, [(v, 'chg' if v in dup else 'n') for v in q])
        n3 = sum(1 for op, _ in rows if op == '取出 3')
        s.text(x, 62 + 6 * 42 + 14, f'3 被取出 {n3} 次', 14, COL[col], 'start', bold=True)
    s.text(LX, 62 + 7 * 42 + 6, '右边：取出 1 时把 3 放进队列，但 3 还没出队、没标记；取出 2 时又放了一次（红色）', 13.5, SUB, 'start')
    s.save('lch-bfs-mark')


def bfs_1091():
    g = [[0, 0, 0, 1], [1, 1, 0, 1], [0, 0, 0, 0], [0, 1, 1, 0]]
    n = 4
    dist = [[-1] * n for _ in range(n)]
    dist[0][0] = 1
    q = deque([(0, 0)])
    D8 = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)]
    while q:
        x, y = q.popleft()
        for dx, dy in D8:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == 0 and dist[nx][ny] == -1:
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx, ny))
    path, cur = {(n - 1, n - 1)}, (n - 1, n - 1)
    while cur != (0, 0):
        x, y = cur
        cur = next((x + dx, y + dy) for dx, dy in D8 if 0 <= x + dx < n and 0 <= y + dy < n
                   and dist[x + dx][y + dy] == dist[x][y] - 1)
        path.add(cur)
    s = S()
    grid(s, 30, 24, [['' if g[i][j] else dist[i][j] for j in range(n)] for i in range(n)],
         lambda i, j: 'wall' if g[i][j] else 'hit' if (i, j) in path else 'n', cw=46, size=16)
    lines(s, 250, 40, [('格子里的数 = dist：从左上角到这格，最少经过几个格子', INK), '起点自己算 1 个，所以 dist[0][0] = 1',
                       '可以斜着走：(0, 1) 的下一步直接到 (1, 2)',
                       (f'绿色 = 一条最短路，答案 {dist[n - 1][n - 1]}', 'grn')], gap=28)
    s.save('lch-bfs-1091')
    print('1091', dist)


def bfs_oranges():
    g = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
    R, C = 3, 3
    q = deque((i, j) for i in range(R) for j in range(C) if g[i][j] == 2)
    fresh = sum(r.count(1) for r in g)
    states = [([r[:] for r in g], set(q), list(q), fresh)]
    while q and fresh:
        new = set()
        for _ in range(len(q)):
            x, y = q.popleft()
            for dx, dy in D4:
                nx, ny = x + dx, y + dy
                if 0 <= nx < R and 0 <= ny < C and g[nx][ny] == 1:
                    g[nx][ny] = 2
                    fresh -= 1
                    q.append((nx, ny))
                    new.add((nx, ny))
        states.append(([r[:] for r in g], new, list(q), fresh))

    def draw(s, ox, oy, k):
        gg, new, qq, fr = states[k]
        grid(s, ox + 10, oy, gg, lambda i, j: 'new' if (i, j) in new else 'chg' if gg[i][j] == 2 else
             'hit' if gg[i][j] == 1 else 'off', cw=44, size=16)
        s.text(ox, oy + 152, '队列：' + ' '.join(f'({a},{b})' for a, b in qq), 12.5, INK, 'start', mono=True)
        s.text(ox, oy + 174, f'fresh = {fr}', 12.5, COL['grn'], 'start', bold=True, mono=True)

    panel_grid('lch-bfs-oranges', len(states), 196, 240, draw,
               titles=['开始：烂橘子全部入队'] + [f'第 {k} 分钟后' for k in range(1, len(states))],
               leg=[('new', '这一分钟刚烂的（刚入队）'), ('chg', '之前就烂了'), ('hit', '新鲜'), ('off', '空格子')])
    print('oranges', [(st[2], st[3]) for st in states])


def bfs_542():
    m = [[0, 0, 0], [0, 1, 0], [1, 1, 1]]
    R, C = 3, 3
    dist = [[-1] * C for _ in range(R)]
    q = deque()
    for i in range(R):
        for j in range(C):
            if m[i][j] == 0:
                dist[i][j] = 0
                q.append((i, j))
    while q:
        x, y = q.popleft()
        for dx, dy in D4:
            nx, ny = x + dx, y + dy
            if 0 <= nx < R and 0 <= ny < C and dist[nx][ny] == -1:
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx, ny))
    s = S()
    stl = ['sent', 'n', 'new']
    s.text(30, 18, '输入 mat', 14.5, INK, 'start', bold=True)
    grid(s, 30, 40, m, lambda i, j: 'sent' if m[i][j] == 0 else 'off', cw=46, size=16)
    s.arrow(184, 108, 226, 108, 'gry')
    s.text(244, 18, '输出 dist', 14.5, INK, 'start', bold=True)
    grid(s, 244, 40, dist, lambda i, j: stl[dist[i][j]], cw=46, size=16)
    lines(s, 420, 52, [('灰色：所有的 0，一开始全部入队，dist = 0（第 0 层）', INK), ('蓝色：离最近的 0 一步（第 1 层）', INK),
                       ('橙色：离最近的 0 两步（第 2 层）', INK), '每个 1 被「最先扩到它的那个 0」记下距离，那就是最近的 0'], gap=28)
    s.save('lch-bfs-542')
    print('542', dist)


def bfs_levels():
    s = S()
    pos = {3: (90, 0), 9: (40, 70), 20: (140, 70), 15: (100, 140), 7: (180, 140)}
    E = [(3, 9), (3, 20), (20, 15), (20, 7)]
    stl = {3: 'sent', 9: 'n', 20: 'n', 15: 'new', 7: 'new'}
    graph(s, 40, 60, pos, E, stl, directed=False)
    for k in range(3):
        s.text(LX, 60 + k * 70, f'第 {k} 层', 12.5, SUB, 'start')
    x = 300
    s.text(x, 18, '每一轮开始时的队列', 13, SUB, 'start', bold=True)
    s.text(x + 170, 18, 'len(queue)', 13, SUB, 'start', bold=True)
    s.text(x + 260, 18, '这一轮取出的 level', 13, SUB, 'start', bold=True)
    s.text(x + 420, 18, '这一轮放进去的', 13, SUB, 'start', bold=True)
    rounds = [([3], [9, 20]), ([9, 20], [15, 7]), ([15, 7], [])]
    for k, (q, nxt) in enumerate(rounds):
        y = 43 + k * 70
        cells(s, x, y, [(v, stl[v]) for v in q])
        s.text(x + 210, y + 17, len(q), 15, INK, bold=True, mono=True)
        s.text(x + 260, y + 17, str(q), 14, COL['grn'], 'start', bold=True, mono=True)
        s.text(x + 420, y + 17, '、'.join(map(str, nxt)) or '无', 14, INK, 'start')
    s.text(LX, 250, '进入 for 之前先算好 len(queue)：这一轮只取这么多个，新放进去的孩子留到下一轮', 13.5, SUB, 'start')
    s.save('lch-bfs-levels')


def bfs_lock():
    s = S()
    s.node(30, 122, '0000', 'sent', w=70, h=38, size=15)
    for i in range(4):
        y = 26 + i * 68
        s.text(170, y + 19, f'拨第 {i + 1} 个轮', 13, SUB, 'start')
        for k, d in enumerate((1, 9)):
            t = '0' * i + str(d) + '0' * (3 - i)
            x = 270 + k * 100
            s.node(x, y, t, 'n', w=70, h=38, size=15)
        s.arrow(102, 141, 164, y + 19, 'gry')
    s.text(270 + 35, 10, '往上拨 +1', 12.5, SUB)
    s.text(370 + 35, 10, '往下拨 −1', 12.5, SUB)
    lines(s, 480, 60, [('点 = 一个四位字符串，一共 10000 个', INK), ('边 = 拨一下：4 个轮 × 2 个方向 = 8 个邻居', INK),
                       '0 往下拨是 9，9 往上拨是 0：(digit + 1) % 10、(digit − 1) % 10', '不用提前建图：取出一个状态，现场算出它的 8 个邻居',
                       ('deadends 里的状态 = 墙，不能走', 'red')], gap=28)
    s.save('lch-bfs-lock')


def bfs_ladder():
    words = ['hot', 'dot', 'dog', 'lot', 'log', 'cog']
    b, e = 'hit', 'cog'
    dist = {b: 1}
    q = deque([b])
    while q:
        w = q.popleft()
        for x in words:
            if x not in dist and sum(p != c for p, c in zip(w, x)) == 1:
                dist[x] = dist[w] + 1
                q.append(x)
    assert dist == {'hit': 1, 'hot': 2, 'dot': 3, 'lot': 3, 'dog': 4, 'log': 4, 'cog': 5}
    s = S()
    X = {1: 30, 2: 180, 3: 330, 4: 480, 5: 630}
    Y = {'hit': 95, 'hot': 95, 'dot': 50, 'lot': 140, 'dog': 50, 'log': 140, 'cog': 95}
    for d in X:
        s.text(X[d] + 32, 14, f'dist = {d}', 13, SUB, bold=True, mono=True)
    for a, c, key, hot in (('hit', 'hot', 'h*t', 1), ('hot', 'dot', '*ot', 1), ('hot', 'lot', '*ot', 0),
                           ('dot', 'dog', 'do*', 1), ('lot', 'log', 'lo*', 0), ('dog', 'cog', '*og', 1),
                           ('log', 'cog', '*og', 0)):
        x1, y1, x2, y2 = X[dist[a]] + 67, Y[a] + 18, X[dist[c]] - 3, Y[c] + 18
        s.arrow(x1, y1, x2, y2, 'grn' if hot else 'line', sw=2.6 if hot else 1.8)
        up = y2 < y1 or (y1 == y2 and True)
        if a == 'lot' or (a, c) in (('hot', 'lot'), ('log', 'cog')):
            up = False
        s.text((x1 + x2) / 2, (y1 + y2) / 2 + (-13 if up else 15), key, 13, COL['grn'] if hot else SUB, bold=True, mono=True)
    for w in dist:
        s.node(X[dist[w]], Y[w], w, 'sent' if w == b else 'hit' if w == e else 'n', w=64, h=36, size=15)
    lines(s, LX, 214, [('边上写的是两个词共用的桶：hit 和 hot 都能变成 h*t，所以它们只差一个字母', INK),
                       ('绿色 = 一条最短的转换序列 hit → hot → dot → dog → cog，一共 5 个词，答案 5', 'grn'),
                       'dot 和 lot、dog 和 log 之间也有边（同一个桶），但对方已经到过，不会再入队'], gap=24)
    s.save('lch-bfs-ladder')


# ---------- 拓扑排序 ----------

def topo_dir():
    s = S()
    pre = [[1, 0], [2, 0], [3, 1], [3, 2]]
    s.text(LX, 18, 'prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]', 14, INK, 'start', bold=True, mono=True)
    s.text(LX, 52, '[a, b]', 13, SUB, 'start', bold=True, mono=True)
    s.text(LX + 90, 52, '意思', 13, SUB, 'start', bold=True)
    s.text(LX + 280, 52, '建的边', 13, SUB, 'start', bold=True)
    for k, (a, b) in enumerate(pre):
        y = 84 + k * 36
        s.text(LX, y, f'[{a}, {b}]', 14, INK, 'start', mono=True)
        s.text(LX + 90, y, f'先修 {b}，才能修 {a}', 14, INK, 'start')
        s.text(LX + 280, y, f'{b} → {a}', 14, COL['org'], 'start', bold=True, mono=True)
        s.text(LX + 350, y, f'graph[{b}].append({a})；indegree[{a}] += 1', 12.5, SUB, 'start', mono=True)
    graph(s, 720, 70, {0: (0, 0), 1: (110, 0), 2: (0, 90), 3: (110, 90)}, [(0, 1), (0, 2), (1, 3), (2, 3)])
    s.text(775, 30, '箭头从「先修的」指向「后修的」', 13, SUB)
    s.text(LX, 236, '写在后面的 b 是先修课，是箭头的起点。照着字面写成 a → b 就全反了', 13.5, COL['red'], 'start', bold=True)
    s.save('lch-topo-dir')


def topo_2050():
    n, rel, time = 5, [[1, 5], [2, 5], [3, 5], [3, 4], [4, 5]], [1, 2, 3, 4, 5]
    g = [[] for _ in range(n)]
    ind = [0] * n
    for a, b in rel:
        g[a - 1].append(b - 1)
        ind[b - 1] += 1
    finish, best = time[:], [-1] * n
    q = deque(u for u in range(n) if ind[u] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in g[u]:
            if finish[u] + time[v] > finish[v]:
                finish[v], best[v] = finish[u] + time[v], u
            ind[v] -= 1
            if ind[v] == 0:
                q.append(v)
    crit, v = set(), max(range(n), key=lambda i: finish[i])
    while best[v] != -1:
        crit.add((best[v], v))
        v = best[v]
    s = S()
    pos = {0: (0, 0), 1: (0, 80), 2: (0, 160), 3: (150, 200), 4: (300, 80)}
    es = [(a - 1, b - 1, '', 'org' if (a - 1, b - 1) in crit else 'line') for a, b in rel]
    where = {0: 'l', 1: 'l', 2: 'l', 3: 'b', 4: 'r'}
    graph(s, 150, 50, pos, es, {v: 'new' if any(v in e for e in crit) else 'n' for v in pos},
          {v: (f'{time[v]} 个月' if where[v] != 'b' else f'{time[v]} 个月', SUB, where[v]) for v in pos},
          names={v: v + 1 for v in pos})
    x = 560
    s.text(x, 22, 'finish[node] = 这门课最早第几个月修完', 14.5, INK, 'start', bold=True)
    txt = []
    for u in order:
        pre = [a - 1 for a, b in rel if b - 1 == u]
        if not pre:
            txt.append(f'课 {u + 1}：没有前置，finish = {time[u]}')
        else:
            txt.append((f'课 {u + 1}：max({", ".join(str(finish[p]) for p in pre)}) + {time[u]} = {finish[u]}',
                        'org' if u == 4 else INK, u == 4))
    lines(s, x, 56, txt, gap=27, size=14)
    lines(s, x, 56 + 27 * len(txt) + 10, [(f'答案 = max(finish) = {max(finish)}', 'red'), '橙色：决定答案的那条路 3 → 4 → 5（3 + 4 + 5）'],
          gap=26)
    s.text(LX, 330, '按拓扑序算：轮到一门课时，它的所有前置课的 finish 都已经算好了', 13.5, SUB, 'start')
    s.save('lch-topo-2050')
    print('2050 order', [u + 1 for u in order], 'finish', finish)


def topo_check():
    E = [(0, 1), (0, 2), (1, 3), (2, 3)]
    s = S()
    for k, (order, title) in enumerate((([0, 2, 1, 3], 'order = [0, 2, 1, 3]'), ([0, 1, 3, 2], 'order = [0, 1, 3, 2]'))):
        ox = 50 + k * 440
        pos = {u: i for i, u in enumerate(order)}
        bad = [(a, b) for a, b in E if pos[a] > pos[b]]
        s.text(ox, 18, title, 14.5, INK, 'start', bold=True, mono=True)
        cs = row(s, ox + 40, 118, order, 'n', cw=62, ch=38, size=16, idx='bot')
        s.text(ox + 40 - 8, 118 + 38 + 11, 'position', 12, SUB, 'end', mono=True)
        for a, b in E:
            x1, x2 = cs[pos[a]], cs[pos[b]]
            ok = pos[a] < pos[b]
            span = abs(pos[a] - pos[b])
            if ok:
                s.curve(x1 + 6, 114, x2 - 6, 114, -14 * span, 'grn')
            else:
                s.curve(x1 - 6, 114, x2 + 6, 114, -14 * span, 'red')
        if bad:
            a, b = bad[0]
            lines(s, ox, 206, [(f'边 {a} → {b}：position[{a}] = {pos[a]} > position[{b}] = {pos[b]}，{a} 排到了 {b} 后面', 'red'),
                               ('不合法', 'red')], gap=24)
        else:
            lines(s, ox, 206, [('4 条边的箭头全部从左指向右', 'grn'), ('合法', 'grn')], gap=24)
    s.text(30, 270, '边：0 → 1，0 → 2，1 → 3，2 → 3。弧线 = 一条边，画在 order 上；合法的顺序里，所有弧线都朝右', 13.5, SUB, 'start')
    s.save('lch-topo-check')


# ---------- Dijkstra ----------

def dij_743():
    times, n, k = [[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2
    g = [[] for _ in range(n)]
    for a, b, w in times:
        g[a - 1].append((b - 1, w))
    dist = [INF] * n
    dist[k - 1] = 0
    heap, done = [(0, k - 1)], [False] * n
    while heap:
        d, u = heapq.heappop(heap)
        if done[u]:
            continue
        done[u] = True
        for v, w in g[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    s = S()
    pos = {1: (0, 0), 0: (0, 110), 2: (130, 0), 3: (260, 0)}
    graph(s, 70, 60, pos, [(a - 1, b - 1, w) for a, b, w in times], {1: 'new', 0: 'n', 2: 'n', 3: 'hit'},
          {v: (f'dist = {dist[v]}', 'red' if dist[v] == max(dist) else INK, 'b' if v == 0 else 't') for v in pos},
          names={v: v + 1 for v in pos})
    lines(s, 420, 40, [('从 2 号点发信号，边上的数 = 传过去要多久', INK), 'dist[node] = 这个点最早什么时候收到信号（起点到它的最短路）',
                       ('所有点都收到 = 等最晚的那个：max(dist) = 2', 'red'), '有的点 dist 还是 ∞：永远收不到，返回 −1'], gap=28)
    s.save('lch-dij-743')
    print('743', dist)


def minimax(n_rows, n_cols, start, cost):
    """Dijkstra with max instead of sum; returns dist grid, parent map, pop order."""
    dist = [[INF] * n_cols for _ in range(n_rows)]
    dist[0][0] = start
    par, order = {}, []
    heap, done = [(start, 0, 0)], set()
    while heap:
        d, x, y = heapq.heappop(heap)
        if (x, y) in done:
            continue
        done.add((x, y))
        order.append((d, x, y))
        for dx, dy in D4:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n_rows and 0 <= ny < n_cols:
                nd = max(d, cost(x, y, nx, ny))
                if nd < dist[nx][ny]:
                    dist[nx][ny] = nd
                    par[(nx, ny)] = (x, y)
                    heapq.heappush(heap, (nd, nx, ny))
    path, cur = [(n_rows - 1, n_cols - 1)], (n_rows - 1, n_cols - 1)
    while cur in par:
        cur = par[cur]
        path.append(cur)
    return dist, path[::-1], order


def dij_1631():
    h = [[1, 2, 2], [3, 8, 2], [5, 3, 5]]
    dist, path, order = minimax(3, 3, 0, lambda x, y, a, b: abs(h[a][b] - h[x][y]))
    s = S()
    s.text(30, 18, 'heights（格子的高度）', 14.5, INK, 'start', bold=True)
    grid(s, 30, 40, h, lambda i, j: 'hit' if (i, j) in path else 'n', cw=50, size=17)
    s.text(250, 18, 'dist（走到这格，路上最大的高度差最小是多少）', 14.5, INK, 'start', bold=True)
    grid(s, 250, 40, dist, lambda i, j: 'hit' if (i, j) in path else 'off', cw=50, size=17)
    hs = [h[x][y] for x, y in path]
    diffs = [abs(a - b) for a, b in zip(hs, hs[1:])]
    lines(s, 30, 216, [(f'绿色路线的高度：{" → ".join(map(str, hs))}，相邻高度差 {"、".join(map(str, diffs))}，最大的是 {max(diffs)}', 'grn'),
                       ('沿第一行再往下走：1 → 2 → 2 → 2 → 5，高度差 1、0、0、3，最大的是 3，比 2 差', INK, False),
                       ('一条路的代价 = 路上最大的那一步，不是把每一步加起来', INK)], gap=26)
    s.save('lch-dij-1631')
    print('1631 dist', dist, 'path', path, 'order', order)


def dij_778():
    g = [[0, 1, 2, 3, 4], [24, 23, 22, 21, 5], [12, 13, 14, 15, 16], [11, 17, 18, 19, 20], [10, 9, 8, 7, 6]]
    dist, path, _ = minimax(5, 5, g[0][0], lambda x, y, a, b: g[a][b])
    top = max(g[x][y] for x, y in path)
    s = S()
    grid(s, 30, 24, g, lambda i, j: 'chg' if g[i][j] == top else 'hit' if (i, j) in path else 'off', cw=46, size=15)
    lines(s, 290, 44, [('格子里的数 = 这格的高度；水位涨到它才能游进去', INK), ('绿色 = 代价最小的路线，绕了一大圈', 'grn'),
                       (f'红色 = 这条路上最高的格子 {top}：要等到时刻 {top} 才能游完', 'red'),
                       '直着往下走要经过 21 ~ 24，更晚', (f'答案 {dist[4][4]}', INK)], gap=28)
    s.save('lch-dij-778')
    print('778', dist[4][4], path)


def dij_787():
    s = S()
    pos = {0: (0, 70), 1: (130, 0), 2: (260, 70), 3: (390, 70)}
    E = [(0, 1, 100, 'red'), (1, 2, 100, 'red'), (0, 2, 500, 'grn', {'side': -1}), (2, 3, 100, 'grn')]
    graph(s, 50, 50, pos, E, {0: 'sent', 3: 'hit'})
    lines(s, 30, 170, [('从 0 到 3，最多坐 2 趟航班（k = 1）', INK),
                       ('红色 0 → 1 → 2：到 2 只花 200，但 2 趟航班已经用完，去不了 3', 'red'),
                       ('绿色 0 → 2 → 3：到 2 要花 500，只用了 1 趟，还能再坐一趟到 3，一共 600（正确答案）', 'grn'),
                       ('Dijkstra 认定「到 2 最便宜是 200」，把 2 标成 done，500 那一份出堆时被当成过期的扔掉', INK, False),
                       ('结果：算不出 600，返回「到不了」', 'red')], gap=26)
    s.save('lch-dij-787')


def dij_787_bf():
    n, flights, src, k = 4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 1
    dist = [INF] * n
    dist[src] = 0

    def dc(prev=None):
        return [(inf(d), 'off' if d == INF else 'new' if prev is not None and prev[i] != d else 'n')
                for i, d in enumerate(dist)]

    rows = [[('t', '开始', INK), ('t', '一趟都不坐', INK), ('t', '只有起点 0', INK), dc()]]
    for r in range(k + 1):
        prev = dist[:]
        ups = []
        for a, b, w in flights:
            if prev[a] + w < dist[b]:
                dist[b] = prev[a] + w
                ups.append(f'{a}→{b}：{inf(prev[a])} + {w} = {dist[b]}')
        rows.append([('t', f'第 {r + 1} 轮', INK), ('t', f'最多坐 {r + 1} 趟', INK), ('t', '；'.join(ups), INK), dc(prev)])
    table('lch-dij-787-bf', ['轮', 'dist 的含义', '这一轮更新了谁（用的是上一轮的 prev）', 'dist（下标 0 ~ 3）'],
          [80, 120, 330, 260], rows, cw=58,
          foot=f'k = 1：最多中转 1 站 = 最多坐 2 趟，跑 2 轮。dist[3] = {dist[3]}', leg=[('new', '这一轮变小了'), ('off', '∞：还到不了')])
    print('787', rows and dist)


# ---------- Kruskal ----------

def kruskal_1584():
    pts = [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]
    n = len(pts)
    edges = sorted(((abs(pts[i][0] - pts[j][0]) + abs(pts[i][1] - pts[j][1]), i, j) for i in range(n) for j in range(i + 1, n)))
    p = list(range(n))

    def find(x):
        while p[x] != x:
            x = p[x]
        return x

    log, chosen, total = [], [], 0
    for w, a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            p[ra] = rb
            total += w
            chosen.append((a, b, w))
            log.append((a, b, w, True, total))
        else:
            log.append((a, b, w, False, total))
        if len(chosen) == n - 1:
            break
    s = S()
    U = 24
    pos = {i: (x * U, (10 - y) * U) for i, (x, y) in enumerate(pts)}
    side = {(0, 1): -1, (1, 3): 1, (3, 4): 1, (1, 2): 1}
    graph(s, 110, 40, pos, [(a, b, w, 'grn', {'side': side.get((a, b), 1)}) for a, b, w in chosen],
          {i: 'n' for i in pos}, {i: (f'({pts[i][0]},{pts[i][1]})', SUB, 'r' if i in (2, 4) else 'l' if i in (0, 1) else 't') for i in pos},
          directed=False)
    x = 390
    s.text(x, 22, f'{n} 个点，两两之间都有边，共 {n * (n - 1) // 2} 条。从小到大看：', 14, INK, 'start', bold=True)
    txt = []
    for a, b, w, ok, tot in log:
        txt.append((f'{a}–{b}（{w}）  ' + (f'选，total = {tot}' if ok else '两端已连通，跳过'), 'grn' if ok else SUB, ok))
    lines(s, x, 54, txt, gap=25, size=14)
    lines(s, x, 54 + 25 * len(txt) + 8, [(f'选够 {n - 1} 条，结束。答案 {total}', 'red')])
    s.text(LX, 318, '边的权重 = 两点的曼哈顿距离 |x1 − x2| + |y1 − y2|；绿色 = 最小生成树选中的边', 13.5, SUB, 'start')
    s.save('lch-kruskal-1584')
    print('1584', log)


# ---------- 旧图（gr-*）换新变量名，另存为 lch-* ----------

import re
import make_diagrams_graph as _old

RENAMES = [(r'^d=', 'dist='), (r' c=', ' count='), (r'^u = (\d+)$', r'node = \1'),
           (r'^绿色的边：dist\[v\] 最后一次被更新时，v 是从谁走过来的$', '绿色的边：dist[neighbor] 最后一次被更新时，是从哪个 node 走过来的'),
           (r'^d = dist，c = count（到这个点的最短路走了几条边）。', 'count = 到这个点的最短路走了几条边。')]


def as_lch(func):
    """Redraw an older gr-* diagram as lch-* with the renamed variables; the gr-* files are not touched."""
    old_text, old_save = S.text, S.save

    def text(self, x, y, t, *a, **k):
        t = str(t)
        for pat, new in RENAMES:
            t = re.sub(pat, new, t)
        return old_text(self, x, y, t, *a, **k)

    def save(self, name, *a, **k):
        assert name.startswith('gr-'), name          # never write over an old image
        return old_save(self, 'lch-' + name[3:], *a, **k)

    S.text, S.save = text, save
    try:
        func()
    finally:
        S.text, S.save = old_text, old_save


if __name__ == '__main__':
    for f in (_old.bfs_trace, _old.dijkstra, _old.dijkstra_path, _old.bf_backup, _old.bf_rounds, _old.spfa, _old.negcycle):
        as_lch(f)
    for f in (bfs_mark, bfs_1091, bfs_oranges, bfs_542, bfs_levels, bfs_lock, bfs_ladder, topo_dir, topo_2050,
              topo_check, dij_743, dij_1631, dij_778, dij_787, dij_787_bf, kruskal_1584):
        f()
    print('ok')
