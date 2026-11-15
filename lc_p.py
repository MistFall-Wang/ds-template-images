#!/usr/bin/env python3
"""Diagrams for 模板 4 二叉树（前半）：表示和遍历 / 自顶向下 / 自底向上 (files lcp-*.svg / lcp-*.png).

Run:  python3 lc_p.py
"""
from make_diagrams import *  # noqa: F401,F403
from make_diagrams_algo import inf, lines, panel_grid, row  # noqa: F401

NEG_INF = float('-inf')


# ---------- 二叉树：从 LeetCode 的层序列表建出来，按中序位置排版 ----------

class Node:
    def __init__(self, val, depth, ghost=False):
        self.val, self.depth, self.ghost = val, depth, ghost
        self.left = self.right = self.parent = None
        self.col = 0                                # 中序序号，决定横坐标


def parse(values, show_null=False, extra=()):
    """LeetCode 层序列表 -> (root, 所有真实节点按层序排的 list)。

    show_null：列表里写明的 None 也建一个「虚节点」画出来；extra：[(节点序号, 'left' | 'right')] 额外补画的空孩子。
    """
    if not values:
        return None, []
    root = Node(values[0], 0)
    real, queue, i = [root], deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        for side in ('left', 'right'):
            if i < len(values):
                if values[i] is not None:
                    kid = Node(values[i], node.depth + 1)
                    kid.parent = node
                    setattr(node, side, kid)
                    real.append(kid)
                    queue.append(kid)
                elif show_null:
                    kid = Node('None', node.depth + 1, ghost=True)
                    kid.parent = node
                    setattr(node, side, kid)
                i += 1
    for k, side in extra:
        if getattr(real[k], side) is None:
            kid = Node('None', real[k].depth + 1, ghost=True)
            kid.parent = real[k]
            setattr(real[k], side, kid)
    count = [0]

    def place(node):
        if node is None:
            return
        place(node.left)
        node.col = count[0]
        count[0] += 1
        place(node.right)

    place(root)
    return root, real


def walk(root):
    out, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node)
        for kid in (node.right, node.left):
            if kid:
                stack.append(kid)
    return out


def btree(s, ox, oy, root, st=None, edge=None, dx=46, dy=62, r=17, arrows=None):
    """画树。st: {node: style}; edge: {child: colour}（这个孩子连向父节点的那条边）。返回 {node: (x, y)}。"""
    st, edge = st or {}, edge or {}
    allnodes = walk(root)
    pos = {n: (ox + n.col * dx, oy + n.depth * dy) for n in allnodes}
    for n in allnodes:
        if n.parent is None:
            continue
        (ax, ay), (bx, by) = pos[n.parent], pos[n]
        L = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / L, (by - ay) / L
        rb = 13 if n.ghost else r
        p1, p2 = (ax + ux * (r + 2), ay + uy * (r + 2)), (bx - ux * (rb + 3), by - uy * (rb + 3))
        col = edge.get(n, 'gry' if n.ghost else 'line')
        hot = col in ('org', 'red', 'grn', 'blue')
        if arrows == 'down' and not n.ghost:
            s.arrow(*p1, *p2, col, sw=2.6 if hot else 1.8)
        elif arrows == 'up' and not n.ghost:
            s.arrow(*p2, *p1, col, sw=2.6 if hot else 1.8)
        else:
            s.seg(*p1, *p2, col, dash=n.ghost, sw=3 if hot else 1.8)
    for n in allnodes:
        x, y = pos[n]
        if n.ghost:
            s.text(x, y, 'None', 11.5, COL['gry'], bold=True, mono=True)
        else:
            s.circ(x, y, n.val, st.get(n, 'n'), r=r, size=12.5 if len(str(n.val)) > 2 else 15)
    return pos


def width(root, dx=46):
    return (len(walk(root)) - 1) * dx


def is_leaf(n):
    real = [k for k in (n.left, n.right) if k and not k.ghost]
    return not real


def kids(n):
    return [k if k and not k.ghost else None for k in (n.left, n.right)]


def fmt(p):
    return '[' + ', '.join(map(str, p)) + ']'


def orders(root):
    pre, ino, post, events = [], [], [], []

    def dfs(node):
        if node is None:
            return
        pre.append(node)
        events.append((node, 'pre'))
        dfs(kids(node)[0])
        ino.append(node)
        events.append((node, 'in'))
        dfs(kids(node)[1])
        post.append(node)
        events.append((node, 'post'))

    dfs(root)
    return pre, ino, post, events


T6 = [1, 2, 3, 4, 5, None, 6]


# ---------- 第 1 节：表示和遍历 ----------

def tree_terms():
    s = S()
    root, real = parse(T6)
    hs = {}

    def height(n):
        if n is None:
            return 0
        hs[n] = 1 + max(height(kids(n)[0]), height(kids(n)[1]))
        return hs[n]

    height(root)
    ox, oy, dx, dy = 150, 70, 54, 74
    st = {n: 'hit' if is_leaf(n) else 'n' for n in real}
    st[root] = 'new'
    # 以 2 为根的子树：虚线框
    sub = [real[1], real[3], real[4]]
    x1 = ox + min(n.col for n in sub) * dx - 34
    x2 = ox + max(n.col for n in sub) * dx + 34
    s.rect(x1, oy + dy - 30, x2 - x1, dy + 60, '#FFFFFF', COL['org'], dash=1, rx=12, sw=1.6)
    pos = btree(s, ox, oy, root, st, dx=dx, dy=dy)
    s.text((x1 + x2) / 2, oy + 2 * dy + 44, '以 2 为根的子树', 13, COL['org'], bold=True)
    s.text(pos[root][0], oy - 32, '根', 13.5, COL['org'], bold=True)
    rx = ox + width(root, dx) + 70
    s.text(rx, oy - 32, '深度（从根数下来第几层）', 13, SUB, 'start', bold=True)
    s.text(rx + 250, oy - 32, '这一层节点的高度', 13, SUB, 'start', bold=True)
    for depth in range(3):
        y = oy + depth * dy
        s.seg(ox + width(root, dx) + 30, y, rx - 10, y, '#CBD5E1', dash=1, sw=1.2)
        s.text(rx, y, f'深度 {depth + 1}', 14, INK, 'start', bold=True)
        row_nodes = [n for n in real if n.depth == depth]
        s.text(rx + 250, y, '，'.join(f'{n.val} 的高度 {hs[n]}' for n in row_nodes), 13.5, INK, 'start')
    legend(s, LX, oy + 2 * dy + 78, [('new', '根：最上面的节点，没有父节点'), ('hit', '叶子：左右孩子都是空的'), ('n', '其他节点')])
    lines(s, LX, oy + 2 * dy + 122, [
        '2 是 1 的左孩子，3 是 1 的右孩子；1 是 2 和 3 的父节点',
        f'这棵树的最大深度 = 根的高度 = {hs[root]}（LC 104 的数法：数节点，不数边）'], gap=24)
    s.save('lcp-tree-terms')


def level_list():
    s = S()
    values = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]
    root, real = parse(values, show_null=True)
    # 每个列表位置属于哪一层、是谁的孩子：照 build_tree 的过程走一遍
    owner = [None] * len(values)                    # (父节点序号, 'left' | 'right')
    level = [0] * len(values)
    order = [0]                                     # 列表下标 -> 真实节点的出队顺序
    real_index = {0: 0}
    queue, i, made = deque([0]), 1, 1
    depth_of = {0: 0}
    while queue and i < len(values):
        par = queue.popleft()
        for side in ('left', 'right'):
            if i < len(values):
                owner[i] = (par, side)
                level[i] = depth_of[par] + 1
                if values[i] is not None:
                    real_index[i] = made
                    depth_of[made] = depth_of[par] + 1
                    queue.append(made)
                    made += 1
                i += 1
    s.text(LX, 18, 'root = [5, 4, 8, 11, null, 13, 4, 7, 2, null, null, null, 1]', 14, INK, 'start', bold=True, mono=True)
    s.text(LX, 44, '从上到下、每层从左到右写；孩子是空的位置写 null', 13.5, COL['org'], 'start', bold=True)
    cw, y = 50, 92
    sts = ['del' if v is None else ('new', 'n', 'hit', 'chg')[level[k]] for k, v in enumerate(values)]
    cs = row(s, LX + 6, y, ['null' if v is None else v for v in values], sts, cw=cw, size=13.5, idx='bot')
    for depth in range(4):
        idx = [k for k in range(len(values)) if level[k] == depth]
        brace(s, cs[idx[0]] - 20, cs[idx[-1]] + 20, y - 8, f'第 {depth + 1} 层', 'gry')
    ty = y + 110
    st = {n: ('new', 'n', 'hit', 'chg')[n.depth] for n in real}
    pos = btree(s, LX + 60, ty, root, st, dx=50, dy=62)
    tx = LX + 60 + width(root, 50) + 50
    # 每个位置是谁的哪个孩子
    out = []
    for k in range(1, len(values)):
        par, side = owner[k]
        out.append((k, real[par].val, '左' if side == 'left' else '右', 'null' if values[k] is None else values[k]))
    s.text(tx, ty - 22, '按顺序给每个节点发两个位置（左孩子、右孩子）：', 13.5, INK, 'start', bold=True)
    groups = {}
    for k, pv, side, v in out:
        groups.setdefault((owner[k][0], pv), []).append((k, side, v))
    yy = ty + 4
    for (par, pv), items in groups.items():
        txt = f'{pv} 的孩子：' + '，'.join(f'下标 {k} = {v}（{side}）' for k, side, v in items)
        s.text(tx, yy, txt, 13, INK, 'start')
        yy += 23
    s.text(tx, yy + 10, 'null 不是节点，没有孩子，后面不给它留位置', 13.5, COL['red'], 'start', bold=True)
    s.text(tx, yy + 34, '排在最后的 null 省略不写（7、2、1 的孩子全是 null，都在末尾，所以没有出现）', 13.5, SUB, 'start')
    s.save('lcp-level-list')
    return groups


def three_positions():
    s = S()
    root, real = parse(T6)
    pre, ino, post, events = orders(root)
    ox, oy, dx, dy = 70, 78, 96, 96
    pos = btree(s, ox, oy, root, {}, dx=dx, dy=dy, r=19)
    num = {}
    for k, (n, kind) in enumerate(events):
        num[(n, kind)] = k + 1
    for n in real:
        x, y = pos[n]
        s.text(x - 31, y - 4, num[(n, 'pre')], 13, COL['blue'], bold=True, mono=True)
        s.text(x, y + 33, num[(n, 'in')], 13, COL['org'], bold=True, mono=True)
        s.text(x + 31, y - 4, num[(n, 'post')], 13, COL['grn'], bold=True, mono=True)
    s.text(LX, 18, 'dfs 在每个节点上停三次。数字是第几步（一共 6 × 3 = 18 步）', 14.5, INK, 'start', bold=True)
    tx = ox + width(root, dx) + 70
    lines(s, tx, 70, [('节点左边的蓝色数字：前序位置', 'blue'), '    刚进入这个节点，左右子树都还没去',
                      ('节点下面的橙色数字：中序位置', 'org'), '    左子树走完回来，右子树还没去',
                      ('节点右边的绿色数字：后序位置', 'grn'), '    左右子树都走完，马上离开这个节点',
                      '',
                      ('只看蓝色数字从小到大：' + ' '.join(str(n.val) for n in pre), 'blue'),
                      ('只看橙色数字从小到大：' + ' '.join(str(n.val) for n in ino), 'org'),
                      ('只看绿色数字从小到大：' + ' '.join(str(n.val) for n in post), 'grn')], gap=24)
    s.save('lcp-three-positions')


def three_orders():
    root, real = parse(T6)
    pre, ino, post, _ = orders(root)
    data = [('前序：根 → 左 → 右', pre, 'blue'), ('中序：左 → 根 → 右', ino, 'org'), ('后序：左 → 右 → 根', post, 'grn')]

    def draw(s, ox, oy, k):
        _, seq, col = data[k]
        pos = btree(s, ox + 30, oy + 34, root, {seq[0]: 'new'}, dx=42, dy=62)
        for i, n in enumerate(seq):
            x, y = pos[n]
            side = -1 if n.parent and n is n.parent.left else 1
            s.text(x + side * 25, y - 15, i + 1, 12.5, COL[col], bold=True, mono=True)
        s.text(ox, oy + 204, '结果：' + fmt([n.val for n in seq]), 13.5, COL[col], 'start', bold=True, mono=True)

    panel_grid('lcp-three-orders', 3, 300, 268, draw, titles=[x[0] for x in data],
               leg=[('new', '第一个被记下的节点')],
               foot='节点旁边的数字 = 第几个被记下。三种顺序里，左子树都排在右子树前面，变的只是「根」排在哪')


def stack_cells(stack):
    return [(str(v), 'n') for v in stack]


def preorder_stack():
    root, _ = parse(T6)
    result, stack = [], [root]
    rows_ = [('开始', '', stack_cells([n.val for n in stack]), [])]
    while stack:
        node = stack.pop()
        result.append(node.val)
        pushed = []
        left, right = kids(node)
        if right:
            stack.append(right)
            pushed.append(right.val)
        if left:
            stack.append(left)
            pushed.append(left.val)
        act = '放进 ' + '、'.join(map(str, pushed)) if pushed else '没有孩子，不放'
        cur = [(str(n.val), 'new' if n.val in pushed else 'n') for n in stack]
        rows_.append((f'取出 {node.val}', act, cur, [(str(v), 'hit' if v == node.val else 'off') for v in result]))
    assert result == [n.val for n in orders(root)[0]]
    table('lcp-preorder-stack', ['取出', '放进栈（先右后左）', 'stack（右边是栈顶）', 'result'], [100, 190, 210, 280], rows_,
          leg=[('new', '这一轮刚放进去的'), ('hit', '这一轮记下的')],
          foot='先放右孩子、后放左孩子：后放的先取出，所以左子树先走完，顺序是 根 → 左 → 右')
    return rows_


def inorder_stack():
    root, _ = parse(T6)
    result, stack, node = [], [], root
    rows_ = []
    while node or stack:
        pushed = []
        while node:
            stack.append(node)
            pushed.append(node.val)
            node = node.left if node.left and not node.left.ghost else None
        before = [(str(n.val), 'new' if n.val in pushed else 'n') for n in stack]
        node = stack.pop()
        result.append(node.val)
        right = kids(node)[1]
        rows_.append(('进栈 ' + '、'.join(map(str, pushed)) if pushed else 'node 是 None，不走', before, f'取出 {node.val}',
                      [(str(v), 'hit' if v == node.val else 'off') for v in result],
                      f'去 {node.val} 的右孩子 {right.val}' if right else f'{node.val} 没有右孩子，node = None'))
        node = right
    assert result == [n.val for n in orders(root)[1]]
    table('lcp-inorder-stack', ['① 一路向左，路上的都进栈', '这时的 stack', '② 取出栈顶，记下', 'result', '③ 转向右子树'],
          [220, 150, 150, 270, 250], rows_,
          leg=[('new', '这一轮刚进栈的'), ('hit', '这一轮记下的')],
          foot='栈里的节点 = 已经路过、但还没记下的节点（它们的左子树正在走）。取出来的那一刻，它的左子树已经走完')
    return rows_


# ---------- 第 2 节：自顶向下 ----------

def top_down():
    s = S()
    values, target = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], 22
    root, real = parse(values)
    total = {}

    def dfs(node, acc):
        if node is None:
            return
        acc += node.val
        total[node] = acc
        dfs(kids(node)[0], acc)
        dfs(kids(node)[1], acc)

    dfs(root, 0)
    st, edge = {}, {}
    hit = [n for n in real if is_leaf(n) and total[n] == target][0]
    n = hit
    while n.parent:
        edge[n] = 'org'
        n = n.parent
    for n in real:
        st[n] = ('hit' if total[n] == target else 'sent') if is_leaf(n) else 'n'
    ox, oy, dx, dy = 60, 84, 62, 78
    s.text(LX, 18, 'root = [5, 4, 8, 11, null, 13, 4, 7, 2, null, null, null, 1]，targetSum = 22', 14, INK, 'start', bold=True, mono=True)
    s.text(LX, 44, '节点旁边的数字 = 从根走到这个节点，路上的和 total（父节点传下来的 total + 自己的 val）', 13.5, COL['org'], 'start', bold=True)
    pos = btree(s, ox, oy, root, st, edge, dx=dx, dy=dy, arrows='down')
    for n in real:
        x, y = pos[n]
        leaf = is_leaf(n)
        col = COL['grn'] if leaf and total[n] == target else SUB if leaf else COL['blue']
        side = -1 if (n.parent and n is n.parent.left) or n is root else 1
        s.text(x + side * 24, y - 15, total[n], 13.5, col, 'end' if side < 0 else 'start', bold=True, mono=True)
    tx = ox + width(root, dx) + 60
    sums = [total[n] for n in orders(root)[0] if is_leaf(n)]
    lines(s, tx, 96, [('信息只往下传：', INK),
                      '    dfs(node, total) 调孩子时，把 total + node.val 传下去',
                      ('答案在叶子上：', INK),
                      '    走到叶子，一条「根 → 叶子」的路才算走完，',
                      '    这时的 total 就是这条路的和',
                      '',
                      (f'四个叶子的 total：{fmt(sums)}', INK),
                      (f'叶子 2 的 total 是 {target}，等于 targetSum → True', 'grn'),
                      ('橙色的路：5 → 4 → 11 → 2', 'org')], gap=24)
    s.save('lcp-top-down')
    return sums


def leaf_check():
    s = S()
    root, real = parse([1, 2], extra=[(0, 'right'), (1, 'left'), (1, 'right')])
    ox, oy, dx, dy = 70, 100, 62, 78
    s.text(LX, 18, 'root = [1, 2]，targetSum = 1。正确答案是 False：唯一的「根 → 叶子」路径是 1 → 2，和是 3', 14, INK, 'start', bold=True)
    pos = btree(s, ox, oy, root, {real[0]: 'n', real[1]: 'hit'}, dx=dx, dy=dy)
    gx, gy = pos[real[0].right]
    s.rect(gx - 30, gy - 16, 60, 32, 'none', COL['red'], dash=1, rx=8, sw=1.6)
    s.text(gx, gy + 32, 'total = 1', 13.5, COL['red'], bold=True, mono=True)
    s.text(pos[real[0]][0] - 26, pos[real[0]][1], 'total = 1', 13.5, COL['blue'], 'end', bold=True, mono=True)
    s.text(pos[real[1]][0] - 26, pos[real[1]][1], 'total = 3', 13.5, COL['grn'], 'end', bold=True, mono=True)
    tx = 400
    lines(s, tx, 78, [('错误写法：走到 None 才比较 total == targetSum', 'red'),
                      '    1 的右孩子是 None，走到这里时 total = 1，',
                      '    正好等于 targetSum，返回 True。错',
                      '    1 还有左孩子 2，它不是叶子，路没有走完',
                      '',
                      ('正确写法：在节点上判断「左右孩子都是 None」', 'grn'),
                      '    只有 2 是叶子，total = 3，不等于 1，返回 False'], gap=24)
    s.text(LX, oy + 2 * dy + 34, 'None 不是叶子。叶子是一个真实的节点：node.left is None and node.right is None', 13.5, COL['org'], 'start', bold=True)
    s.save('lcp-leaf-check')


def path_backtrack():
    s = S()
    values, target = [1, 2, 3, 5, 6, None, 4], 8
    root, real = parse(values)
    result, path, rows_ = [], [], []

    def dfs(node, total):
        if node is None:
            return
        path.append(node.val)
        total += node.val
        note, col = '', INK
        if is_leaf(node):
            if total == target:
                result.append(path[:])
                note, col = f'叶子，total = {total}，记下 {fmt(path)}', 'grn'
            else:
                note, col = f'叶子，total = {total}，不等于 {target}', SUB
        else:
            note = f'total = {total}'
        rows_.append((f'进入 {node.val}', 'append', path[:], len(path) - 1, 'new', note, col))
        dfs(kids(node)[0], total)
        dfs(kids(node)[1], total)
        gone = path.pop()
        rows_.append((f'离开 {node.val}', 'pop', path[:] + [gone], len(path), 'del', '', INK))

    dfs(root, 0)
    s.text(LX, 18, 'root = [1, 2, 3, 5, 6, null, 4]，targetSum = 8', 14, INK, 'start', bold=True, mono=True)
    pos = btree(s, 50, 84, root, {n: 'hit' if is_leaf(n) else 'n' for n in real}, dx=44, dy=70)
    s.text(LX, 84 + 2 * 70 + 50, '全程只有一个 path。', 13.5, INK, 'start', bold=True)
    s.text(LX, 84 + 2 * 70 + 74, '进入节点 append，', 13.5, COL['org'], 'start', bold=True)
    s.text(LX, 84 + 2 * 70 + 98, '离开节点 pop。', 13.5, SUB, 'start', bold=True)
    s.text(LX, 84 + 2 * 70 + 134, '橙色格 = 这一步刚 append 的', 13, COL['org'], 'start')
    s.text(LX, 84 + 2 * 70 + 158, '虚线格 = 这一步 pop 掉的', 13, SUB, 'start')
    tx, y = 330, 50
    for x, h in ((tx, '步'), (tx + 40, '动作'), (tx + 190, 'path'), (tx + 400, '说明')):
        s.text(x, y, h, 13.5, SUB, 'start', bold=True)
    y += 18
    for k, (what, op, p, hot, st, note, col) in enumerate(rows_):
        s.seg(tx, y, tx + 640, y, '#E5E7EB', sw=1)
        s.text(tx, y + 20, k + 1, 13, SUB, 'start', mono=True)
        s.text(tx + 40, y + 20, f'{what}：{op}', 13.5, COL['org'] if op == 'append' else SUB, 'start', bold=True)
        row(s, tx + 190, y + 5, p, [st if i == hot else 'n' for i in range(len(p))], cw=38, ch=30, size=14)
        s.text(tx + 400, y + 20, note, 13.5, COL.get(col, col), 'start', bold=col == 'grn')
        y += 40
    s.seg(tx, y, tx + 640, y, '#E5E7EB', sw=1)
    s.text(tx, y + 24, f'result = {result}。最后 path 回到空：每个 append 都有一个 pop 和它配对', 13.5, INK, 'start', bold=True)
    s.save('lcp-path-backtrack')
    return rows_, result


def root_numbers():
    s = S()
    values = [4, 9, 0, 5, 1]
    root, real = parse(values)
    number, leaves = {}, []

    def dfs(node, acc):
        if node is None:
            return
        acc = acc * 10 + node.val
        number[node] = acc
        if is_leaf(node):
            leaves.append(acc)
        dfs(kids(node)[0], acc)
        dfs(kids(node)[1], acc)

    dfs(root, 0)
    ox, oy, dx, dy = 110, 80, 62, 78
    s.text(LX, 18, 'root = [4, 9, 0, 5, 1]', 14, INK, 'start', bold=True, mono=True)
    pos = btree(s, ox, oy, root, {n: 'hit' if is_leaf(n) else 'n' for n in real}, dx=dx, dy=dy, arrows='down')
    for n in real:
        x, y = pos[n]
        side = -1 if (n.parent and n is n.parent.left) or n is root else 1
        s.text(x + side * 25, y - 14, number[n], 13.5, COL['grn'] if is_leaf(n) else COL['blue'], 'end' if side < 0 else 'start',
               bold=True, mono=True)
    tx = ox + width(root, dx) + 90
    lines(s, tx, 70, [('传下去的是「走到这里拼出来的数」number', INK),
                      '    每往下走一步：number = number * 10 + node.val',
                      '    4 → 9：4 × 10 + 9 = 49；49 → 5：49 × 10 + 5 = 495',
                      '',
                      (f'叶子上的 number：{fmt(leaves)}', 'grn'),
                      (f'答案 = {" + ".join(map(str, leaves))} = {sum(leaves)}', 'grn')], gap=24)
    s.save('lcp-root-numbers')
    return leaves


# ---------- 第 3 节：自底向上 ----------

def bottom_up():
    s = S()
    values = [3, 9, 20, None, None, 15, 7]
    root, real = parse(values, extra=[(1, 'left'), (1, 'right')])
    ret = {}

    def dfs(node):
        if node is None:
            return 0
        a, b = dfs(kids(node)[0]), dfs(kids(node)[1])
        ret[node] = (a, b, 1 + max(a, b))
        return ret[node][2]

    dfs(root)
    ox, oy, dx, dy = 80, 96, 66, 84
    s.text(LX, 18, 'root = [3, 9, 20, null, null, 15, 7]，求最大深度', 14, INK, 'start', bold=True, mono=True)
    s.text(LX, 44, '箭头 = 返回值的方向：孩子把「我这棵子树有几层」交给父节点', 13.5, COL['org'], 'start', bold=True)
    pos = btree(s, ox, oy, root, {root: 'new'}, dx=dx, dy=dy, arrows='up')
    for n in walk(root):
        if n.parent is None:
            continue
        (ax, ay), (bx, by) = pos[n.parent], pos[n]
        side = -1 if n is n.parent.left else 1
        val = 0 if n.ghost else ret[n][2]
        s.text((ax + bx) / 2 + side * 8, (ay + by) / 2 - 15, f'返回 {val}', 13, COL['gry'] if n.ghost else COL['grn'],
               'end' if side < 0 else 'start', bold=True)
    x, y = pos[root]
    s.text(x, y - 32, f'返回 {ret[root][2]}：答案', 13.5, COL['grn'], bold=True)
    tx = ox + width(root, dx) + 70
    post = [n for n in orders(root)[2]]
    ls = [('每个节点做同一件事：', INK), '    问左孩子几层，问右孩子几层，取大的，加上自己这 1 层', '',
          ('算出结果的先后（从叶子往上）：', INK)]
    for n in post:
        a, b, c = ret[n]
        ls.append(f'    节点 {n.val}：1 + max({a}, {b}) = {c}')
    ls += ['', ('空节点（None）返回 0：空树有 0 层。图里只画了 9 下面的两个', 'gry')]
    lines(s, tx, 86, ls, gap=24)
    s.save('lcp-bottom-up')
    return [(n.val,) + ret[n] for n in post]


def invert():
    values = [4, 2, 7, 1, 3, 6, 9]
    root, real = parse(values)

    def to_values(node):
        out, queue = [], deque([node])
        while queue:
            n = queue.popleft()
            out.append(n.val)
            for k in (n.left, n.right):
                if k:
                    queue.append(k)
        return out

    def flip(node):
        if node is None:
            return None
        a, b = flip(node.left), flip(node.right)
        node.left, node.right = b, a
        return node

    root2, _ = parse(values)
    flip(root2)
    after = to_values(root2)
    root2, real2 = parse(after)
    cols = {1: 'new', 3: 'new', 2: 'new', 6: 'hit', 9: 'hit', 7: 'hit'}
    data = [(root, real, '翻转前  ' + fmt(values)), (root2, real2, '翻转后  ' + fmt(after))]

    def draw(s, ox, oy, k):
        r0, re, _ = data[k]
        btree(s, ox + 40, oy + 34, r0, {n: cols.get(n.val, 'n') for n in re}, dx=46, dy=66)

    panel_grid('lcp-invert', 2, 400, 250, draw, titles=[x[2] for x in data],
               leg=[('new', '原来的左子树'), ('hit', '原来的右子树')],
               foot='每个节点都把自己的左右孩子对调：不只是 2 和 7 换了位置，2 下面的 1、3 和 7 下面的 6、9 也各自对调了')
    return after


def symmetric():
    s = S()
    values = [1, 2, 2, 3, 4, 4, 3]
    root, real = parse(values)
    ox, oy, dx, dy = 70, 96, 66, 84
    s.text(LX, 18, 'root = [1, 2, 2, 3, 4, 4, 3]：沿着中间的竖线对折，两边重合', 14, INK, 'start', bold=True)
    pos = btree(s, ox, oy, root, {real[3]: 'hit', real[6]: 'hit', real[4]: 'new', real[5]: 'new'}, dx=dx, dy=dy)
    x0 = pos[root][0]
    s.seg(x0, oy + 24, x0, oy + 2 * dy + 66, 'gry', dash=1, sw=1.4)
    a, b = pos[real[1]], pos[real[2]]
    s.curve(a[0] + 20, a[1] - 6, b[0] - 20, b[1] - 6, -14, 'blue', dash=1)
    s.curve(b[0] - 20, b[1] - 6, a[0] + 20, a[1] - 6, -14, 'blue', dash=1)
    a, b = pos[real[3]], pos[real[6]]
    s.curve(a[0] + 8, a[1] + 22, b[0] - 8, b[1] + 22, 30, 'grn', dash=1)
    s.curve(b[0] - 8, b[1] + 22, a[0] + 8, a[1] + 22, 30, 'grn', dash=1)
    a, b = pos[real[4]], pos[real[5]]
    s.curve(a[0] + 12, a[1] + 20, b[0] - 12, b[1] + 20, 12, 'org', dash=1)
    s.curve(b[0] - 12, b[1] + 20, a[0] + 12, a[1] + 20, 12, 'org', dash=1)
    tx = ox + width(root, dx) + 70
    lines(s, tx, 78, [('is_mirror(left_node, right_node)：一次拿两个节点，问「这两棵子树是不是镜像」', INK),
                      ('蓝：先比这两个节点自己的值（2 和 2）', 'blue'),
                      ('绿：外侧一对 —— left_node.left 和 right_node.right（3 和 3）', 'grn'),
                      ('橙：内侧一对 —— left_node.right 和 right_node.left（4 和 4）', 'org'),
                      '',
                      '镜子里左右是反的：左边那个节点的左孩子，对着右边那个节点的右孩子',
                      '写成「左对左、右对右」就变成了 LC 100 相同的树'], gap=26)
    s.save('lcp-symmetric')


DIAM = [1, 2, 3, 4, 5, None, None, 6, None, None, 7, 8, None, None, 9]


def diameter():
    s = S()
    root, real = parse(DIAM)
    info, best = {}, [0, None]

    def dfs(node):
        if node is None:
            return 0
        a, b = dfs(kids(node)[0]), dfs(kids(node)[1])
        if a + b > best[0]:
            best[0], best[1] = a + b, node
        info[node] = (a, b, 1 + max(a, b))
        return info[node][2]

    dfs(root)
    # 最长路径：从拐弯的节点出发，两边各沿着更深的孩子走到底
    edge = {}

    def deepest(node):
        while node:
            edge[node] = 'org'
            a, b = kids(node)
            if a is None and b is None:
                break
            node = a if (info[a][2] if a else 0) >= (info[b][2] if b else 0) else b

    top = best[1]
    deepest(top.left)
    deepest(top.right)
    ox, oy, dx, dy = 150, 86, 62, 74
    s.text(LX, 18, 'root = [1, 2, 3, 4, 5, null, null, 6, null, null, 7, 8, null, null, 9]', 14, INK, 'start', bold=True, mono=True)
    s.text(LX, 44, '绿色：返回给父节点的值（这棵子树有几层）。灰色 / 红色：在这个节点拐弯的最长路径（左层数 + 右层数）', 13.5, INK, 'start')
    pos = btree(s, ox, oy, root, {top: 'new'}, edge, dx=dx, dy=dy)
    for n in real:
        x, y = pos[n]
        a, b, d = info[n]
        side = -1 if n.col <= top.col else 1
        up = 13 if n is root else 0
        anchor = 'end' if side < 0 else 'start'
        hot = n is top
        s.text(x + side * 25, y - 9 - up, f'返回 {d}', 12.5, COL['grn'], anchor, bold=True)
        s.text(x + side * 25, y + 9 - up, f'{a} + {b} = {a + b}', 12.5, COL['red'] if hot else SUB, anchor, bold=hot, mono=True)
    by = oy + 4 * dy + 46
    lines(s, LX, by, [(f'最长的路径在节点 {top.val} 拐弯：左边 {info[top][0]} 层 + 右边 {info[top][1]} 层 = {best[0]} 条边（橙色），不经过根',
                       'org'),
                      (f'根节点 1 上算出来的只有 {info[root][0]} + {info[root][1]} = {info[root][0] + info[root][1]}。'
                       '所以不能只在根上算一次，要在每个节点上都算一次、取最大', INK, False)], gap=24)
    s.save('lcp-diameter')
    return [(n.val,) + info[n] for n in orders(root)[2]], best[0]


def gains(root):
    info, best = {}, [NEG_INF, None]

    def dfs(node):
        if node is None:
            return 0
        raw_a, raw_b = dfs(kids(node)[0]), dfs(kids(node)[1])
        a, b = max(raw_a, 0), max(raw_b, 0)
        through = node.val + a + b
        if through > best[0]:
            best[0], best[1] = through, node
        info[node] = (raw_a, raw_b, a, b, through, node.val + max(a, b))
        return info[node][5]

    dfs(root)
    return info, best


def max_path():
    cases = [([-10, 9, 20, None, None, 15, 7], '例 1：最大的路径不经过根'),
             ([1, -2, 3, None, None, -4, 5], '例 2：贡献是负数的孩子，当它不存在')]
    out = []
    prepared = []
    for values, title in cases:
        root, real = parse(values)
        info, best = gains(root)
        top = best[1]
        edge = {}
        # 最优路径：从 top 往两边，沿着贡献 > 0 且较大的那条腿走
        def leg(node):
            while node and info[node][5] > 0:
                edge[node] = 'org'
                a, b = kids(node)
                ga, gb = info[node][2], info[node][3]
                if ga == 0 and gb == 0:
                    break
                node = a if ga >= gb else b
        a, b = kids(top)
        if info[top][2] > 0:
            leg(a)
        if info[top][3] > 0:
            leg(b)
        on_path = {top} | set(edge)
        prepared.append((values, title, root, real, info, best, edge, on_path))
        out.append((values, [(n.val,) + info[n] for n in orders(root)[2]], best[0]))

    def draw(s, ox, oy, k):
        values, title, root, real, info, best, edge, on_path = prepared[k]
        s.text(ox, oy + 2, 'root = ' + fmt(['null' if v is None else v for v in values]), 13, INK, 'start', bold=True, mono=True)
        dx, dy = 84, 92
        st = {n: 'new' if n in on_path else 'n' for n in real}
        pos = btree(s, ox + 96, oy + 66, root, st, edge, dx=dx, dy=dy, r=19)
        for n in real:
            x, y = pos[n]
            raw_a, raw_b, a, b, through, ret = info[n]
            side = -1 if (n.parent and n is n.parent.left) else 1
            if n is root:
                side = -1
            anchor = 'end' if side < 0 else 'start'
            s.text(x + side * 27, y - 10, f'返回 {inf(ret)}', 12.5, COL['red'] if ret < 0 else COL['grn'], anchor, bold=True)
            hot = n is best[1]
            s.text(x + side * 27, y + 9, f'拐弯 {inf(through)}', 12.5, COL['red'] if hot else SUB, anchor, bold=hot)
        top = best[1]
        cap = [(f'答案 {best[0]}：在节点 {top.val} 拐弯，{top.val} + {info[top][2]} + {info[top][3]}', 'org')]
        if k == 0:
            r_ = info[root]
            cap.append(f'根 −10 上：−10 + {r_[2]} + {r_[3]} = {r_[4]}，比 {best[0]} 小')
        else:
            neg = [n for n in real if info[n][5] < 0]
            cap.append('返回 ' + '、'.join(inf(info[n][5]) for n in neg) + ' 的孩子：父节点取 max(返回值, 0) = 0，不接它')
        lines(s, ox, oy + 66 + 2 * dy + 50, cap, size=13, gap=22)

    panel_grid('lcp-maxpath', 2, 560, 396, draw, titles=[c[1] for c in cases],
               leg=[('new', '最大路径上的节点')],
               foot='绿色「返回」= 从这个节点往下走一条腿的最大和（交给父节点）；「拐弯」= 自己 + 左腿 + 右腿（用来更新答案）')
    return out


def one_leg():
    values = [1, 2, 3, 4, 5]
    root0, real0 = parse(values)
    info, _ = gains(root0)
    n2 = info[real0[1]]
    panels = [('在节点 2 拐弯：两条腿都要', {1: 'new', 3: 'new', 4: 'new'}, {3, 4},
               [f'4 → 2 → 5，和 = 2 + 4 + 5 = {n2[4]}', '路径到 2 就结束，不再往上', ('这是用来更新答案的值', 'red')]),
              ('2 交给父节点 1：只能带一条腿', {0: 'new', 1: 'new', 4: 'new', 2: 'new'}, {1, 4, 2},
               [f'2 返回 2 + max(4, 5) = {n2[5]}', '1 把它接上：3 → 1 → 2 → 5，还是一条路',
                ('这是返回给父节点的值', 'grn')]),
              ('如果 2 把两条腿都交上去', {0: 'chg', 1: 'chg', 3: 'chg', 4: 'chg', 2: 'chg'}, {1, 3, 4, 2},
               ['4、5 都接在 2 下面，2 又接着 1：', '在 2 这里分了叉，一笔画不出来', ('这不是一条路径', 'red')])]

    def draw(s, ox, oy, k):
        _, sts, hot, cap = panels[k]
        root, real = parse(values)
        col = 'red' if k == 2 else 'org'
        btree(s, ox + 50, oy + 34, root, {real[i]: v for i, v in sts.items()}, {real[i]: col for i in hot}, dx=50, dy=66)
        lines(s, ox, oy + 216, cap, size=13, gap=22)

    panel_grid('lcp-one-leg', 3, 330, 320, draw, titles=[p[0] for p in panels],
               foot='root = [1, 2, 3, 4, 5]。路径是一笔画下来的：每个节点最多连着路径上的两个邻居')
    return n2


def balanced():
    s = S()
    values = [1, 2, 3, 4, None, None, None, 5]
    root, real = parse(values)
    ret, seen = {}, []

    def dfs(node):
        if node is None:
            return 0
        seen.append(node)
        a = dfs(kids(node)[0])
        if a == -1:
            ret[node] = (a, None, -1)
            return -1
        b = dfs(kids(node)[1])
        if b == -1 or abs(a - b) > 1:
            ret[node] = (a, b, -1)
            return -1
        ret[node] = (a, b, 1 + max(a, b))
        return ret[node][2]

    answer = dfs(root)
    ox, oy, dx, dy = 150, 90, 70, 78
    st = {n: ('off' if n not in seen else 'chg' if ret[n][2] == -1 else 'n') for n in real}
    s.text(LX, 18, 'root = [1, 2, 3, 4, null, null, null, 5]', 14, INK, 'start', bold=True, mono=True)
    s.text(LX, 44, '返回值平时是高度；一旦发现某棵子树不平衡，就返回 −1，并且一路传到根', 13.5, COL['org'], 'start', bold=True)
    pos = btree(s, ox, oy, root, st, dx=dx, dy=dy)
    for n in real:
        x, y = pos[n]
        side = -1 if n.col <= root.col else 1
        anchor = 'end' if side < 0 else 'start'
        if n not in seen:
            s.text(x + 26, y, '没有被访问', 12.5, COL['gry'], 'start', bold=True)
            continue
        a, b, c = ret[n]
        bad = c == -1
        s.text(x + side * 26, y - 9, f'返回 {inf(c)}', 12.5, COL['red'] if bad else COL['grn'], anchor, bold=True)
        txt = f'左 {inf(a)}，右 {inf(b)}' if b is not None else f'左 {inf(a)}，右边不用看了'
        s.text(x + side * 26, y + 9, txt, 12.5, SUB, anchor)
    tx = ox + width(root, dx) + 130
    ls = [('按算出结果的先后：', INK)]
    for n in orders(root)[2]:
        if n not in seen:
            continue
        a, b, c = ret[n]
        if b is None:
            ls.append((f'    节点 {n.val}：左边返回 −1 → 直接返回 −1，右子树（3）不去了', 'red', False))
        elif c == -1:
            ls.append((f'    节点 {n.val}：左 {a}，右 {b}，差 {abs(a - b)} > 1 → 返回 −1', 'red', False))
        else:
            ls.append(f'    节点 {n.val}：左 {a}，右 {b}，差 {abs(a - b)} → 返回 {c}')
    ls += ['', (f'dfs(root) 返回 {inf(answer)}，所以答案是 False', INK)]
    lines(s, tx, 90, ls, gap=24)
    legend(s, LX, oy + 3 * dy + 40, [('chg', '返回 −1 的节点'), ('off', '没有被访问的节点')])
    s.save('lcp-balanced')
    return [(n.val,) + ret[n] for n in seen], answer


if __name__ == '__main__':
    tree_terms()
    print(level_list())
    three_positions()
    three_orders()
    print(preorder_stack())
    print(inorder_stack())
    print(top_down())
    leaf_check()
    print(path_backtrack())
    print(root_numbers())
    print(bottom_up())
    print(invert())
    symmetric()
    print(diameter())
    print(max_path())
    print(one_leg())
    print(balanced())
    print('ok')
