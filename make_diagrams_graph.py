#!/usr/bin/env python3
"""Diagrams for 常用代码模板3——搜索与图论（Python版）.md  (files gr-*.svg / gr-*.png).

Run:  python3 make_diagrams_graph.py
"""
from make_diagrams_algo import *  # noqa: F401,F403

INF = float('inf')


def und(E, a, b):
    """Is the undirected edge a-b in the edge collection E?"""
    return (a, b) in E or (b, a) in E


# ---------- 存储 ----------

def store():
    s = S()
    s.text(LX, 18, '图', 14.5, INK, 'start', bold=True)
    graph(s, 40, 62, {0: (60, 0), 1: (20, 70), 2: (100, 70), 3: (20, 140)}, [(0, 1), (0, 2), (1, 3)], directed=False)
    ax = 240
    s.text(ax, 18, '邻接表：g[a] = a 能走到的点', 14.5, INK, 'start', bold=True)
    for a, nb in {0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}.items():
        y = 46 + a * 44
        s.text(ax, y + 17, f'g[{a}]', 14, INK, 'start', bold=True, mono=True)
        s.arrow(ax + 46, y + 17, ax + 72, y + 17, 'gry')
        row(s, ax + 80, y, nb, 'n', cw=40)
    mx = 500
    s.text(mx, 18, '邻接矩阵：g[a][b] = 1 表示 a、b 之间有边', 14.5, INK, 'start', bold=True)
    M = [[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]]
    for k in range(4):
        s.text(mx + 36 + k * 38 + 17, 48, k, 13, SUB, bold=True, mono=True)
        s.text(mx + 16, 62 + k * 38 + 17, k, 13, SUB, bold=True, mono=True)
    grid(s, mx + 36, 62, M, lambda i, j: 'new' if M[i][j] else 'off', cw=38)
    s.text(LX, 244, '无向边 0–1 存两次：邻接表里 g[0] 有 1、g[1] 有 0；矩阵里 g[0][1] 和 g[1][0] 都是 1', 13.5, SUB, 'start')
    s.save('gr-store')


# ---------- DFS ----------

def dfs_panels():
    pos = {0: (70, 0), 1: (35, 62), 2: (105, 62), 3: (5, 124), 4: (65, 124)}
    E = [(0, 1), (0, 2), (1, 3), (1, 4)]
    steps = [(0, [0], None, ['进入 0', '邻居 1 没去过：深入']),
             (1, [0, 1], (0, 1), ['进入 1', '邻居 3 没去过：深入']),
             (3, [0, 1, 3], (1, 3), ['进入 3，没有新邻居', '没路了：退回 1']),
             (4, [0, 1, 3, 4], (1, 4), ['回到 1，邻居 4 没去过', '进入 4，再退回 1、0']),
             (2, [0, 1, 3, 4, 2], (0, 2), ['回到 0，邻居 2 没去过', '进入 2，结束'])]

    def draw(s, ox, oy, k):
        cur, order, edge, cap = steps[k]
        used = {steps[i][2] for i in range(k + 1)}
        es = [(a, b, '', 'org' if (a, b) == edge else 'grn' if (a, b) in used else 'line') for a, b in E]
        graph(s, ox + 30, oy + 24, pos, es, {v: 'new' if v == cur else 'hit' if v in order else 'n' for v in pos},
              directed=False)
        lines(s, ox, oy + 190, cap, size=13, gap=20)
        s.text(ox, oy + 236, f'order = {order}', 12.5, COL['grn'], 'start', bold=True, mono=True)

    panel_grid('gr-dfs', 5, 200, 300, draw, titles=[f'第 {k + 1} 步' for k in range(5)],
               leg=[('new', '当前所在的点'), ('hit', '已经去过'), ('n', '还没去过')])


def islands():
    s = S()
    g = ['1100', '1001', '0000', '0100']
    isl = {(0, 0): 'n', (0, 1): 'n', (1, 0): 'n', (1, 3): 'new', (3, 1): 'hit'}
    grid(s, 30, 24, [list(r) for r in g], lambda i, j: isl.get((i, j), 'off'), cw=46, size=16)
    x = 260
    for k, (st, t) in enumerate((('n', '岛 1：从 (0, 0) 出发，dfs 把相连的 3 格全标记掉'),
                                 ('new', '岛 2：(1, 3)，上下左右都不是陆地，只有 1 格'),
                                 ('hit', '岛 3：(3, 1)，只有 1 格'))):
        f, kk, _, d = ST[st]
        s.rect(x, 30 + k * 34, 20, 20, f, kk, d, rx=4)
        s.text(x + 30, 40 + k * 34, t, 14, INK, 'start')
    lines(s, x, 146, [('外层循环：遇到「是陆地 + 没来过」的格子，就 dfs 一次、count 加 1', INK),
                      '一次 dfs 会把整个岛都标记掉，所以每个岛只被数一次  →  3 个岛'], gap=24)
    s.save('gr-islands')


def centroid():
    s = S()
    pos = {0: (150, 0), 1: (90, 70), 2: (210, 70), 3: (50, 140), 4: (130, 140), 5: (130, 210), 6: (210, 140)}
    E = [(0, 1), (0, 2), (1, 3), (1, 4), (4, 5), (2, 6)]
    es = [(a, b, '', 'gry', {'dash': 1}) if 1 in (a, b) else (a, b) for a, b in E]
    st = {0: 'n', 2: 'n', 6: 'n', 1: 'del', 3: 'new', 4: 'hit', 5: 'hit'}
    graph(s, 30, 66, pos, es, st, directed=False)
    s.text(LX, 16, 'n = 7，删掉点 1（虚线）：树断成 3 块', 14.5, INK, 'start', bold=True)
    x = 330
    for k, (stl, t) in enumerate((('n', '上面那一块：n − size[1] = 7 − 4 = 3 个点'), ('new', '孩子 3 的子树：1 个点'),
                                  ('hit', '孩子 4 的子树：2 个点'))):
        f, kk, _, d = ST[stl]
        s.rect(x, 62 + k * 34, 20, 20, f, kk, d, rx=4)
        s.text(x + 30, 72 + k * 34, t, 14, INK, 'start')
    lines(s, x, 176, [('size[1] = 1 + 1 + 2 = 4：dfs(1) 返回的子树大小', INK), ('删掉 1 后最大的一块 = max(1, 2, 3) = 3', 'red'),
                      '每个点都这样算一次，取最小的那个'], gap=26)
    s.save('gr-centroid')


# ---------- 回溯 ----------

def perm_tree():
    s = S()
    leaves = [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]
    Y = [16, 92, 168, 244]
    hot = {(), (1,), (1, 3), (1, 3, 2)}
    cx = {p: 70 + k * 124 for k, p in enumerate(leaves)}
    for p in leaves:
        cx[p[:2]] = cx[p]
    for a in (1, 2, 3):
        two = [cx[p] for p in leaves if p[0] == a]
        cx[(a,)] = sum(two) / 2
    cx[()] = cx[(2,)]
    nodes = [(), (1,), (2,), (3,)] + [p[:2] for p in leaves] + leaves
    for p in nodes[1:]:
        par = p[:-1]
        x1, y1, x2, y2 = cx[par], Y[len(par)] + 37, cx[p], Y[len(p)] - 4
        col = 'org' if p in hot else 'line'
        s.arrow(x1, y1, x2, y2, col, sw=2.6 if p in hot else 1.8)
        off = 0 if abs(x2 - x1) < 5 else (-16 if x2 < x1 else 16)
        s.text((x1 + x2) / 2 + (14 if off == 0 else off), (y1 + y2) / 2 - (0 if off == 0 else 6), p[-1], 14,
               COL['org'] if p in hot else SUB, bold=True, mono=True)
    for p in nodes:
        t = '[' + ', '.join(map(str, p)) + ']'
        w = tw(t, 14) + 20
        s.node(cx[p] - w / 2, Y[len(p)], t, 'new' if p in hot else 'hit' if len(p) == 3 else 'n', w=w, h=34, size=14)
    lines(s, LX, 304, [('边上的数字 = 这一步选了谁；每一层决定一个位置', INK),
                       ('橙色：从根走到底的一条路 = 一个排列 [1, 3, 2]。走到底记下答案，然后撤销选择、退回上一层换下一个', 'org')],
          gap=24)
    s.save('gr-perm-tree')


def queens_diag():
    s = S()
    for k, (title, f, hit) in enumerate((('row − col 相同：同一条 ↘ 斜线', lambda r, c: r - c, 0),
                                         ('row + col 相同：同一条 ↙ 斜线', lambda r, c: r + c, 3))):
        ox = 30 + k * 330
        s.text(ox, 18, title, 14.5, INK, 'start', bold=True)
        grid(s, ox + 20, 42, [[inf(f(r, c)) for c in range(4)] for r in range(4)],
             lambda i, j, f=f, hit=hit: 'new' if f(i, j) == hit else 'off', cw=46)
    s.text(30, 256, '所以用两个集合就能记住「哪些斜线上已经有皇后」：diag1 存 row − col，diag2 存 row + col', 13.5, SUB, 'start')
    s.save('gr-queens-diag')


def queens_step():
    s = S()
    cw = 50
    for c in range(4):
        s.text(60 + c * cw + 23, 26, f'列 {c}', 12, SUB)
    for r in range(4):
        s.text(34, 40 + r * cw + 23, f'行 {r}', 12, SUB)
    cell = {(0, 1): ('Q', 'hit'), (1, 0): ('✗', 'chg'), (1, 1): ('✗', 'chg'), (1, 2): ('✗', 'chg'), (1, 3): ('✓', 'new')}
    grid(s, 60, 40, [[cell.get((r, c), ('', 'off'))[0] for c in range(4)] for r in range(4)],
         lambda i, j: cell.get((i, j), ('', 'off'))[1], cw=cw, size=17)
    lines(s, 300, 34, [('第 0 行：皇后放在第 1 列', 'grn'), 'cols = {1}，diag1 = {0 − 1 = −1}，diag2 = {0 + 1 = 1}',
                       ('第 1 行挨个试每一列：', INK), '列 0：row + col = 1，在 diag2 里 ✗（↙ 斜线冲突）',
                       '列 1：在 cols 里 ✗（同一列）', '列 2：row − col = −1，在 diag1 里 ✗（↘ 斜线冲突）',
                       ('列 3：都不冲突 ✓ 放下，三个集合各加一项，去第 2 行', 'org')], gap=27)
    s.save('gr-queens-step')


def queens_sol():
    s = S()
    for k, q in enumerate(([1, 3, 0, 2], [2, 0, 3, 1])):
        ox = 30 + k * 260
        s.text(ox, 18, f'摆法 {k + 1}：queens = {q}', 14, INK, 'start', bold=True)
        grid(s, ox, 40, [['Q' if q[r] == c else '' for c in range(4)] for r in range(4)],
             lambda i, j, q=q: 'hit' if q[i] == j else 'sent' if (i + j) % 2 else 'off', cw=46, size=17)
    s.text(30, 242, 'queens[row] = 第 row 行的皇后放在第几列', 13.5, SUB, 'start')
    s.save('gr-queens-sol')


# ---------- BFS ----------

BFS_E = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]


def bfs_layers():
    s = S()
    pos = {0: (0, 55), 1: (120, 0), 2: (120, 110), 3: (240, 55), 4: (360, 55)}
    layer = {0: 0, 1: 1, 2: 1, 3: 2, 4: 3}
    stl = ['sent', 'n', 'new', 'hit']
    ox, oy = 60, 86
    for k, x in enumerate((0, 120, 240, 360)):
        s.text(ox + x, 20, f'第 {k} 层', 14, INK, bold=True)
        s.text(ox + x, 40, f'{k} 步能到', 12.5, SUB)
    graph(s, ox, oy, pos, BFS_E, {v: stl[layer[v]] for v in pos},
          {v: (f'dist={layer[v]}', INK, 'b' if v != 1 else 't') for v in pos})
    s.text(LX, 250, '按步数从小到大一层一层往外扩，所以第一次到达某个点时的步数，就是到它的最少步数', 13.5, SUB, 'start')
    s.save('gr-bfs-layers')


def bfs_trace():
    n = 5
    g = [[] for _ in range(n)]
    for a, b in BFS_E:
        g[a].append(b)
    dist = [-1] * n
    dist[0] = 0
    q = deque([0])

    def dc(new):
        return [(inf(d), 'new' if i in new else 'off' if d == -1 else 'n') for i, d in enumerate(dist)]

    rows = [[('t', '开始', INK), ('t', '起点 0 入队，dist[0] = 0', INK), [(0, 'new')], dc({0})]]
    while q:
        u = q.popleft()
        new, old = [], []
        for v in g[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
                new.append(v)
            else:
                old.append(v)
        t = '；'.join(x for x in ('、'.join(map(str, new)) + ' 第一次到，入队' if new else '',
                                 '、'.join(map(str, old)) + ' 到过了，跳过' if old else '') if x) or '没有邻居'
        rows.append([('t', f'u = {u}', INK), ('t', t, INK), [(v, 'new' if v in new else 'n') for v in q], dc(set(new))])
    table('gr-bfs-trace', ['取出', '看邻居', '队列（左 = 队头）', 'dist（下标 0 ~ 4）'], [90, 250, 180, 260], rows, cw=44,
          leg=[('new', '这一步新入队 / 新记下的 dist'), ('off', '-1：还没到过')])


def maze():
    s = S()
    g = [[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 1, 0]]
    R = C = 5
    dist = [[-1] * C for _ in range(R)]
    dist[0][0] = 0
    q = deque([(0, 0)])
    D = ((1, 0), (-1, 0), (0, 1), (0, -1))
    while q:
        x, y = q.popleft()
        for dx, dy in D:
            nx, ny = x + dx, y + dy
            if 0 <= nx < R and 0 <= ny < C and g[nx][ny] == 0 and dist[nx][ny] == -1:
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx, ny))
    path, cur = {(4, 4)}, (4, 4)
    while cur != (0, 0):
        x, y = cur
        cur = next((x + dx, y + dy) for dx, dy in D if 0 <= x + dx < R and 0 <= y + dy < C
                   and dist[x + dx][y + dy] == dist[x][y] - 1)
        path.add(cur)
    grid(s, 30, 24, [['' if g[i][j] else dist[i][j] for j in range(C)] for i in range(R)],
         lambda i, j: 'wall' if g[i][j] else 'hit' if (i, j) in path else 'n', cw=46, size=16)
    lines(s, 300, 40, [('格子里的数 = 从左上角走到这里最少几步', INK), '深色 = 墙，走不了',
                       '数字一圈一圈往外变大：这就是「一层一层往外扩」',
                       (f'绿色 = 一条最短路，到右下角最少 {dist[4][4]} 步', 'grn')], gap=28)
    s.save('gr-maze')


# ---------- 拓扑排序 ----------

def topo():
    pos = {0: (0, 0), 1: (110, 0), 2: (0, 90), 3: (110, 90)}
    E = [(0, 1), (0, 2), (1, 3), (2, 3)]
    ind = [0, 1, 1, 2]
    q, order, gone = deque([0]), [], set()
    states = [(set(), ind[:], list(q), [], None)]
    while q:
        u = q.popleft()
        order.append(u)
        gone.add(u)
        for a, b in E:
            if a == u:
                ind[b] -= 1
                if ind[b] == 0:
                    q.append(b)
        states.append((set(gone), ind[:], list(q), order[:], u))

    def draw(s, ox, oy, k):
        gone, ind, q, order, u = states[k]
        prev = states[k - 1][1] if k else ind
        es = [(a, b, '', 'gry', {'dash': 1}) if a in gone else (a, b) for a, b in E]
        st = {v: 'del' if v in gone else 'new' if v in q else 'n' for v in pos}
        tag = {v: (f'入度 {ind[v]}', 'red' if ind[v] != prev[v] else INK, 't' if v < 2 else 'b')
               for v in pos if v not in gone}
        graph(s, ox + 40, oy + 36, pos, es, st, tag)
        s.text(ox, oy + 180, f'队列 = {q}', 13, INK, 'start', mono=True)
        s.text(ox, oy + 202, f'order = {order}', 13, COL['grn'], 'start', bold=True, mono=True)

    panel_grid('gr-topo', 5, 200, 270, draw, titles=['开始'] + [f'取出 {st[4]}，排进答案' for st in states[1:]],
               leg=[('new', '入度 0：在队列里，可以排了'), ('n', '还有前置没排'), ('del', '已经排好（它的边不再算）')])


def topo_cycle():
    s = S()
    pos = {0: (0, 0), 1: (130, 0), 2: (260, 0)}
    graph(s, 50, 70, pos, [(0, 1, '', 'gry', {'dash': 1}), (1, 2, '', 'red', {'bend': -24}), (2, 1, '', 'red', {'bend': 24})],
          {0: 'del', 1: 'n', 2: 'n'}, {2: ('入度 1', 'red', 'r')})
    s.text(168, 40, '入度 1', 13.5, COL['red'], 'end', bold=True, mono=True)
    s.text(50, 20, '边：0 → 1，1 → 2，2 → 1', 14, INK, bold=False, anchor='start')
    lines(s, 420, 44, [('0 排掉之后：1 和 2 的入度都还是 1', INK), '1 等 2 先排，2 等 1 先排：永远减不到 0，永远进不了队列',
                       ('最后 order 里只有 1 个点，不够 n = 3 个  →  有环', 'red')], gap=27)
    s.save('gr-topo-cycle')


# ---------- 最短路 ----------

DJ_POS = {0: (0, 60), 1: (120, 0), 2: (120, 120), 3: (240, 0), 4: (240, 120)}
DJ_E = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5)]
DJ_W = {0: 't', 1: 't', 2: 'b', 3: 't', 4: 'b'}


def dijkstra():
    n = 5
    dist = [INF] * n
    dist[0] = 0
    done = [False] * n
    states = [(dist[:], set(), None, set(), set(), ['起点 0 的距离是 0', '其余都是 ∞'])]
    for _ in range(n):
        u = min((v for v in range(n) if not done[v]), key=lambda v: (dist[v], v))
        if dist[u] == INF:
            states.append((dist[:], {v for v in range(n) if done[v]}, u, set(), set(),
                           [f'① 挑中 {u}（距离 ∞）', '剩下的点都到不了，结束']))
            break
        done[u] = True
        upd, rel = set(), set()
        for a, b, w in DJ_E:
            if a == u and dist[u] + w < dist[b]:
                dist[b] = dist[u] + w
                upd.add(b)
                rel.add((a, b))
        cap = [f'① 挑中 {u}（距离 {dist[u]}），② 确定',
               '③ 更新：' + ('，'.join(f'{v} 变成 {dist[v]}' for v in sorted(upd)) if upd else '没有能更新的')]
        states.append((dist[:], {v for v in range(n) if done[v]}, u, upd, rel, cap))

    def draw(s, ox, oy, k):
        dist, dn, u, upd, rel, cap = states[k]
        es = [(a, b, w, 'red' if (a, b) in rel else 'line') for a, b, w in DJ_E]
        st = {v: 'new' if v == u else 'hit' if v in dn else 'n' for v in range(n)}
        tag = {v: (f'd={inf(dist[v])}', 'red' if v in upd else INK, DJ_W[v]) for v in range(n)}
        graph(s, ox + 30, oy + 36, DJ_POS, es, st, tag)
        lines(s, ox, oy + 208, cap, size=13, gap=20)
        s.text(ox, oy + 252, 'dist = [' + ', '.join(inf(d) for d in dist) + ']', 12.5, COL['grn'], 'start', bold=True, mono=True)

    panel_grid('gr-dijkstra', len(states), 325, 320, draw, cols=3, titles=['开始'] + [f'第 {k} 轮' for k in range(1, len(states))],
               leg=[('new', '这一轮挑中的点'), ('hit', '已确定，不会再变'), ('n', '还没确定')],
               foot='红色 = 这一轮被更新的距离，以及用来更新它的那条边')


def dijkstra_heap():
    n = 5
    g = [[] for _ in range(n)]
    for a, b, w in DJ_E:
        g[a].append((b, w))
    dist = [INF] * n
    dist[0] = 0
    done = [False] * n
    heap = [(0, 0)]

    def hc(new=()):
        return [(f'({d},{v})', 'new' if (d, v) in new else 'del' if done[v] else 'n') for d, v in sorted(heap)]

    def dc(new=()):
        return [(inf(d), 'new' if i in new else 'off' if d == INF else 'n') for i, d in enumerate(dist)]

    rows = [[('t', '开始', INK), ('t', '起点入堆', INK), hc({(0, 0)}), dc({0})]]
    while heap:
        d, u = heapq.heappop(heap)
        if done[u]:
            rows.append([('t', f'({d}, {u})', 'red'), ('t', f'{u} 已经确定：过期的，跳过', 'red'), hc(), dc()])
            continue
        done[u] = True
        new, upd = set(), set()
        for v, w in g[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
                new.add((dist[v], v))
                upd.add(v)
        t = f'确定 {u}；' + ('更新 ' + '、'.join(map(str, sorted(upd))) if upd else '没有能更新的')
        rows.append([('t', f'({d}, {u})', INK), ('t', t, INK), hc(new), dc(upd)])
    table('gr-dijkstra-heap', ['取出 (距离, 点)', '处理', '堆里剩下的（小的在左）', 'dist（下标 0 ~ 4）'], [150, 250, 250, 320],
          rows, cw=58, leg=[('new', '这一步新放进堆 / 新更新'), ('del', '过期：这个点已经确定了，但旧的那份还留在堆里')])


def dijkstra_path():
    s = S()
    tree_e = {(0, 2), (2, 1), (1, 3)}
    dist = [0, 3, 1, 4, INF]
    es = [(a, b, w, 'grn', {'sw': 3}) if (a, b) in tree_e else (a, b, w, 'gry', {'dash': 1}) for a, b, w in DJ_E]
    graph(s, 50, 50, DJ_POS, es, {0: 'hit', 1: 'hit', 2: 'hit', 3: 'new', 4: 'off'},
          {v: (f'd={inf(dist[v])}', INK, DJ_W[v]) for v in range(5)})
    lines(s, 380, 34, [('绿色的边：dist[v] 最后一次被更新时，v 是从谁走过来的', 'grn'), 'parent = [-1, 2, 0, 1, -1]',
                       ('要 0 到 3 的路径：从终点 3 顺着 parent 往回走', INK), '3  →  parent[3] = 1  →  parent[1] = 2  →  parent[2] = 0  →  -1 停',
                       ('倒过来：[0, 2, 1, 3]，总长 1 + 2 + 1 = 4', 'org')], gap=28)
    s.save('gr-dijkstra-path')


BF_POS = {0: (0, 0), 1: (110, 0), 2: (220, 0)}


def bf_edges(hot, col):
    return [(0, 1, 1, col if (0, 1) in hot else 'line'), (1, 2, 1, col if (1, 2) in hot else 'line'),
            (0, 2, 3, col if (0, 2) in hot else 'line', {'bend': 30})]


def bf_backup():
    data = [('有备份：正确', {(0, 1), (0, 2)}, 'grn', ['0', '1', '3'], 'grn',
             ['处理 (1, 2, 1)：prev[1] 还是 ∞，不更新', '处理 (0, 2, 3)：dist[2] = 0 + 3 = 3', '到 2 的距离 3：只走了 1 条边 ✓']),
            ('没备份：错了', {(0, 1), (1, 2)}, 'red', ['0', '1', '2'], 'red',
             ['处理 (1, 2, 1)：用了这一轮刚算出的 dist[1] = 1', 'dist[2] = 1 + 1 = 2', '到 2 的距离 2：其实走了 2 条边 ✗'])]

    def draw(s, ox, oy, k):
        _, hot, col, d, c2, cap = data[k]
        graph(s, ox + 40, oy + 40, BF_POS, bf_edges(hot, col), {},
              {v: (f'd={d[v]}', c2 if v == 2 else INK) for v in range(3)})
        lines(s, ox, oy + 120, [(cap[0], INK, False), (cap[1], INK, False), (cap[2], col)], size=13, gap=22)

    panel_grid('gr-bf-backup', 2, 400, 230, draw, titles=[d[0] for d in data],
               foot='k = 1（最多走 1 条边），边按 (0,1,1)、(1,2,1)、(0,2,3) 的顺序处理')


def bf_rounds():
    data = [('开始', [0, INF, INF], set(), set(), '只有起点是 0'),
            ('第 1 轮：最多走 1 条边', [0, 1, 3], {1, 2}, {(0, 1), (0, 2)}, 'prev = [0, ∞, ∞]'),
            ('第 2 轮：最多走 2 条边', [0, 1, 2], {2}, {(1, 2)}, 'prev = [0, 1, 3]，2 改走 0 → 1 → 2')]

    def draw(s, ox, oy, k):
        _, d, upd, hot, cap = data[k]
        graph(s, ox + 40, oy + 40, BF_POS, bf_edges(hot, 'red'), {},
              {v: (f'd={inf(d[v])}', 'red' if v in upd else INK) for v in range(3)})
        s.text(ox, oy + 122, cap, 13, INK, 'start')
        s.text(ox, oy + 146, 'dist = [' + ', '.join(inf(x) for x in d) + ']', 12.5, COL['grn'], 'start', bold=True, mono=True)

    panel_grid('gr-bf-rounds', 3, 320, 210, draw, titles=[d[0] for d in data],
               foot='每一轮把所有边都松弛一遍；红色 = 这一轮起作用的边和被更新的距离')


def spfa():
    pos = {0: (0, 45), 1: (95, 0), 2: (95, 90), 3: (190, 0)}
    E = [(0, 1, 5), (0, 2, 2), (2, 1, -4), (1, 3, 1)]
    where = {0: 't', 1: 't', 2: 'b', 3: 't'}
    n = 4
    dist = [INF] * n
    dist[0] = 0
    q, inq = deque([0]), [False] * n
    inq[0] = True
    states = [(dist[:], list(q), None, set(), set(), '起点 0 入队')]
    while q:
        u = q.popleft()
        inq[u] = False
        upd, rel, msg = set(), set(), []
        for a, b, w in E:
            if a == u and dist[u] + w < dist[b]:
                dist[b] = dist[u] + w
                upd.add(b)
                rel.add((a, b))
                again = any(st[2] == b for st in states)
                if not inq[b]:
                    q.append(b)
                    inq[b] = True
                msg.append(f'{b} 变成 {inf(dist[b])}' + ('（再次入队）' if again else ''))
        states.append((dist[:], list(q), u, upd, rel, '，'.join(msg) or '没有能更新的'))

    def draw(s, ox, oy, k):
        dist, q, u, upd, rel, cap = states[k]
        es = [(a, b, inf(w), 'red' if (a, b) in rel else 'line') for a, b, w in E]
        st = {v: 'new' if v == u else 'n' if v in q else 'off' for v in range(n)}
        graph(s, ox + 22, oy + 36, pos, es, st, {v: (f'd={inf(dist[v])}', 'red' if v in upd else INK, where[v]) for v in range(n)})
        s.text(ox, oy + 172, cap, 13, INK, 'start')
        s.text(ox, oy + 194, f'队列 = {q}', 12.5, COL['blue'], 'start', bold=True, mono=True)

    panel_grid('gr-spfa', len(states), 258, 262, draw, cols=4,
               titles=['开始'] + [f'取出 {st[2]}' for st in states[1:]],
               leg=[('new', '刚取出的点'), ('n', '在队列里'), ('off', '不在队列里')],
               foot='点 1 和点 3 各进了两次队：距离每变小一次，就要重新进队去更新别人')


def negcycle():
    pos = {0: (0, 90), 1: (90, 0), 2: (180, 90)}
    E = [(0, 1, 1), (1, 2, -3), (2, 0, 1)]
    where = {0: 'b', 1: 't', 2: 'b'}
    n = 3
    dist, cnt = [0] * n, [0] * n
    q, inq = deque(range(n)), [True] * n
    states = [(dist[:], cnt[:], list(q), None, set(), set(), '所有点入队，dist 全是 0', False)]
    found = False
    while q and not found:
        u = q.popleft()
        inq[u] = False
        upd, rel, msg = set(), set(), '不更新（0 + 1 不小于 0）'
        for a, b, w in E:
            if a == u and dist[u] + w < dist[b]:
                dist[b] = dist[u] + w
                cnt[b] = cnt[u] + 1
                upd.add(b)
                rel.add((a, b))
                msg = f'dist[{b}] = {inf(dist[b])}，count[{b}] = {cnt[b]}'
                if cnt[b] >= n:
                    found = True
                    msg += ' >= n：有负环'
                    break
                if not inq[b]:
                    q.append(b)
                    inq[b] = True
        states.append((dist[:], cnt[:], list(q), u, upd, rel, msg, found))

    def draw(s, ox, oy, k):
        dist, cnt, q, u, upd, rel, cap, fd = states[k]
        es = [(a, b, inf(w), 'red' if (a, b) in rel else 'line') for a, b, w in E]
        st = {v: 'new' if v == u else 'n' if v in q else 'off' for v in range(n)}
        tag = {v: (f'd={inf(dist[v])} c={cnt[v]}', 'red' if v in upd else INK, where[v]) for v in range(n)}
        graph(s, ox + 60, oy + 36, pos, es, st, tag)
        s.text(ox, oy + 178, cap, 13, COL['red'] if fd else INK, 'start', bold=fd)
        s.text(ox, oy + 200, f'队列 = {q}', 12.5, COL['blue'], 'start', bold=True, mono=True)

    panel_grid('gr-negcycle', len(states), 320, 268, draw, cols=3,
               titles=['开始'] + [f'取出 {st[3]}' for st in states[1:]],
               foot='d = dist，c = count（到这个点的最短路走了几条边）。环 0 → 1 → 2 → 0 的总权重是 1 − 3 + 1 = −1')
    return states


def floyd_idea():
    s = S()
    P = {'i': (60, 130), 'k': (240, 50), 'j': (420, 130)}
    graph(s, 0, 0, P, [('i', 'k', '', 'org'), ('k', 'j', '', 'org'), ('i', 'j', '', 'line')], {'k': 'new'}, r=19)
    s.text(140, 76, 'dist[i][k]', 14, COL['org'], 'end', bold=True, mono=True)
    s.text(340, 76, 'dist[k][j]', 14, COL['org'], 'start', bold=True, mono=True)
    s.text(240, 148, 'dist[i][j]（现在已知的）', 14, INK, bold=True)
    s.text(240, 20, '中转点 k', 13.5, COL['org'], bold=True)
    lines(s, 500, 60, [('从 i 到 j：要么走现在已知的路，要么先到 k 再到 j', INK),
                       ('dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])', 'org'), '把每个点轮流拿来当中转点 k 试一遍'], gap=28)
    s.save('gr-floyd-idea')


def floyd_trace():
    n = 3
    d = [[0, 2, 10], [INF, 0, 3], [INF, INF, 0]]
    states = [([r[:] for r in d], set(), None, '直接有边的先填上')]
    for k in range(n):
        ch = set()
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
                    ch.add((i, j))
        states.append(([r[:] for r in d], ch, k, '0 → 2：2 + 3 = 5 < 10，改成 5' if ch else '没有变化'))

    def draw(s, ox, oy, k):
        m, ch, kk, cap = states[k]
        for t in range(n):
            s.text(ox + 40 + t * 46 + 21, oy + 8, t, 13, SUB, bold=True, mono=True)
            s.text(ox + 18, oy + 22 + t * 46 + 21, t, 13, SUB, bold=True, mono=True)
        grid(s, ox + 40, oy + 22, [[inf(v) for v in r] for r in m],
             lambda i, j: 'chg' if (i, j) in ch else 'new' if kk in (i, j) else 'off', cw=46, size=15)
        s.text(ox, oy + 182, cap, 13, COL['red'] if ch else INK, 'start', bold=bool(ch))

    panel_grid('gr-floyd-trace', 4, 225, 240, draw, titles=['初始'] + [f'k = {k}：允许经过 {k}' for k in range(n)],
               leg=[('new', '第 k 行、第 k 列：这一轮用来中转的值'), ('chg', '被改小的格子')])


def sp_choose():
    s = S()
    x, w, y = 40, 240, 20
    for qn, ans, c in (('要所有点对之间的距离吗？', 'Floyd', 'O(n³)'), ('限制最多走几条边吗？', 'Bellman-Ford', 'O(k × m)'),
                       ('有负权边吗？', 'SPFA', '平均 O(m)，最坏 O(n × m)'), ('每条边长度都是 1 吗？', 'BFS', 'O(n + m)')):
        s.node(x, y, qn, 'var', w=w, h=42, size=14, mono=False)
        s.arrow(x + w + 4, y + 21, x + w + 86, y + 21, 'grn', label='是', loff=-12)
        s.node(x + w + 90, y, ans, 'hit', w=150, h=42, size=15, mono=False)
        s.text(x + w + 256, y + 21, c, 13, SUB, 'start', mono=True)
        s.arrow(x + w / 2, y + 45, x + w / 2, y + 79, 'gry', label='否', loff=-16)
        y += 82
    s.node(x, y, '堆优化 Dijkstra', 'hit', w=w, h=42, size=15, mono=False)
    s.text(x + w + 16, y + 21, 'O(m log n)；点少边多的稠密图用朴素版 O(n²)', 13, SUB, 'start')
    s.save('gr-sp-choose')


# ---------- 最小生成树 ----------

MST_POS = {0: (0, 0), 1: (130, 0), 2: (0, 110), 3: (130, 110)}
MST_E = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (1, 3, 6), (2, 3, 3)]


def prim():
    n = 4
    w = {}
    for a, b, c in MST_E:
        w[a, b] = w[b, a] = c
    dist, via = [INF] * n, [None] * n
    dist[0] = 0
    intree, total, tree_e = [False] * n, 0, set()
    states = [(dist[:], set(), None, set(), set(), ['从 0 号点开始', 'total = 0'])]
    for _ in range(n):
        u = min((v for v in range(n) if not intree[v]), key=lambda v: (dist[v], v))
        intree[u] = True
        total += dist[u]
        if via[u] is not None:
            tree_e.add((via[u], u))
        upd = set()
        for v in range(n):
            if not intree[v] and w.get((u, v), INF) < dist[v]:
                dist[v], via[v] = w[u, v], u
                upd.add(v)
        cap = [f'挑中 {u}（边长 {dist[u]}），total = {total}',
               '更新：' + ('，'.join(f'{v} 变成 {dist[v]}' for v in sorted(upd)) if upd else '没有')]
        states.append((dist[:], {v for v in range(n) if intree[v]}, u, upd, set(tree_e), cap))

    def draw(s, ox, oy, k):
        dist, it, u, upd, te, cap = states[k]
        es = [(a, b, c, 'grn' if und(te, a, b) else 'line') for a, b, c in MST_E]
        st = {v: 'new' if v == u else 'hit' if v in it else 'n' for v in range(n)}
        tag = {v: (f'd={inf(dist[v])}', 'red' if v in upd else INK, 't' if v < 2 else 'b') for v in range(n)}
        graph(s, ox + 30, oy + 36, MST_POS, es, st, tag, directed=False)
        lines(s, ox, oy + 196, cap, size=13, gap=20)

    panel_grid('gr-prim', 5, 205, 280, draw, titles=['开始'] + [f'第 {k} 轮' for k in range(1, 5)],
               leg=[('new', '这一轮接进来的点'), ('hit', '已经连好的那一团')],
               foot='d = 这个点到「已经连好的那一团」最短的一条边；绿色的边 = 选中的边，总和 6')


def kruskal():
    order = sorted(MST_E, key=lambda e: e[2])
    comp = [{0}, {1}, {2}, {3}]
    chosen, total = [], 0
    states = [([], None, ['边按权重从小到大排好：', '0–1(1) 1–2(2) 2–3(3) 0–2(4) 1–3(6)'])]
    for a, b, c in order[:3]:
        ca, cb = next(x for x in comp if a in x), next(x for x in comp if b in x)
        comp.remove(ca)
        comp.remove(cb)
        comp.append(ca | cb)
        comp.sort(key=min)
        chosen.append((a, b))
        total += c
        states.append((chosen[:], (a, b), [f'{a}–{b} 两端不连通：选，total = {total}',
                                           '团：' + ' '.join('{' + ', '.join(map(str, sorted(x))) + '}' for x in comp)]))
    states[-1][2].append('选够 n − 1 = 3 条，结束')

    def draw(s, ox, oy, k):
        ch, cur, cap = states[k]
        last = k == len(states) - 1
        es = [(a, b, c, 'org' if (a, b) == cur else 'grn' if (a, b) in ch else 'gry' if last else 'line',
               {'dash': 1} if last and (a, b) not in ch else {}) for a, b, c in MST_E]
        touched = {v for e in ch for v in e}
        graph(s, ox + 30, oy + 30, MST_POS, es, {v: 'hit' if v in touched else 'n' for v in range(4)}, directed=False)
        lines(s, ox, oy + 186, cap, size=13, gap=20)

    panel_grid('gr-kruskal', 4, 250, 290, draw,
               titles=['开始'] + [f'看 {a}–{b}（权重 {c}）' for a, b, c in order[:3]],
               foot='橙色 = 正在看的边，绿色 = 已选的边。剩下的 0–2、1–3 两端早已连通，选了就成环')


# ---------- 二分图 ----------

def bipartite():
    s = S()
    s.text(30, 20, '四个点围成一圈：是二分图', 14.5, COL['grn'], 'start', bold=True)
    graph(s, 70, 70, {0: (0, 0), 1: (110, 0), 2: (110, 100), 3: (0, 100)}, [(0, 1), (1, 2), (2, 3), (3, 0)],
          {0: 'n', 2: 'n', 1: 'new', 3: 'new'}, directed=False)
    lines(s, 30, 212, ['0 染蓝 → 邻居 1、3 被逼成橙', '→ 2 被逼成蓝，没有矛盾'], size=13.5)
    s.seg(330, 14, 330, 240, '#E5E7EB', sw=1)
    s.text(360, 20, '三个点围成一圈：不是二分图', 14.5, COL['red'], 'start', bold=True)
    graph(s, 410, 70, {0: (65, 0), 1: (0, 100), 2: (130, 100)}, [(0, 1), (0, 2), (1, 2, '', 'red')],
          {0: 'n', 1: 'new', 2: 'new'}, directed=False)
    lines(s, 360, 212, ['0 染蓝 → 1 和 2 都被逼成橙', ('但 1–2 之间有边：相邻同色，矛盾', 'red')], size=13.5)
    s.text(660, 80, '蓝 = 颜色 0，橙 = 颜色 1', 13.5, INK, 'start', bold=True)
    s.text(660, 108, '规则：每条边的两端颜色必须不同', 13.5, INK, 'start')
    s.text(660, 136, '颜色是被邻居逼出来的，没得选', 13.5, SUB, 'start')
    s.text(660, 164, '结论：有奇数条边围成的环，就不是二分图', 13.5, SUB, 'start')
    s.save('gr-bipartite')


def hungarian():
    Eg = [(0, 0), (0, 1), (1, 0), (2, 1), (2, 2)]
    data = [({}, set(), None, ['灰线 = 可以配对', '左边的点一个一个来找对象']),
            ({0: 0}, set(), 0, ['左 0：右 0 没人', '直接配上']),
            ({0: 1, 1: 0}, {(0, 0)}, 1, ['左 1 只能配右 0，被左 0 占着', '问左 0：能换成右 1 → 右 0 让给左 1']),
            ({0: 1, 1: 0, 2: 2}, set(), 2, ['左 2：右 1 被左 0 占着，谁都换不了', '改试右 2，没人，配上 → 共 3 对'])]

    def draw(s, ox, oy, k):
        m, moved, cur, cap = data[k]
        for u, v in Eg:
            x1, y1, x2, y2 = ox + 76, oy + 27 + u * 58, ox + 164, oy + 27 + v * 58
            if m.get(u) == v:
                s.seg(x1, y1, x2, y2, 'grn', sw=3.5)
            elif (u, v) in moved:
                s.seg(x1, y1, x2, y2, 'red', dash=1, sw=2)
            else:
                s.seg(x1, y1, x2, y2, '#CBD5E1', sw=1.6)
        for i in range(3):
            s.node(ox + 20, oy + 10 + i * 58, f'左 {i}', 'new' if i == cur else 'hit' if i in m else 'n', w=54, h=34,
                   size=14, mono=False)
            s.node(ox + 166, oy + 10 + i * 58, f'右 {i}', 'hit' if i in m.values() else 'n', w=54, h=34, size=14, mono=False)
        lines(s, ox, oy + 190, cap, size=13, gap=20)
        match = [next((u for u, v in m.items() if v == r), -1) for r in range(3)]
        s.text(ox, oy + 236, f'match = {match}', 12.5, COL['grn'], 'start', bold=True, mono=True)

    panel_grid('gr-hungarian', 4, 262, 300, draw, titles=['能连的边', '轮到左 0', '轮到左 1', '轮到左 2'],
               foot='绿线 = 现在的配对；红虚线 = 被让出去的旧配对；match[v] = 右 v 现在配的是左边的谁')


if __name__ == '__main__':
    for f in (store, dfs_panels, islands, centroid, perm_tree, queens_diag, queens_step, queens_sol, bfs_layers,
              bfs_trace, maze, topo, topo_cycle, dijkstra, dijkstra_heap, dijkstra_path, bf_backup, bf_rounds, spfa,
              floyd_idea, floyd_trace, sp_choose, prim, kruskal, bipartite, hungarian):
        f()
    for st in negcycle():
        print(st[3], st[0], st[1], st[2], st[6])
    print('ok')
