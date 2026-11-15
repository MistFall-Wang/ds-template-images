#!/usr/bin/env python3
"""Diagrams for 层序遍历 / 二叉搜索树 / 最近公共祖先和构造二叉树 in 常用代码模板4 (files lcq-*.svg / lcq-*.png).

Run:  python3 lc_q.py
Every trace shown in a picture is computed here by the same algorithm as the text.
"""
from collections import deque

from make_diagrams import *  # noqa: F401,F403
from make_diagrams_algo import lines, row  # noqa: F401

N = None
RUN = [1, 2, 3, 4, 5, N, 6, 7]                          # 层序遍历一节一直用的树
BST = [8, 3, 10, 1, 6, N, 14, N, N, 4, 7]               # 二叉搜索树一节一直用的树
LEVEL_ST = ['sent', 'n', 'new', 'hit']                  # 第 0、1、2、3 层的颜色


# ---------- 二叉树：从层序 list 建、摆位置、画 ----------

class TN:
    def __init__(self, val, label=None):
        self.val, self.left, self.right = val, None, None
        self.label = val if label is None else label
        self.next = None


def build(values):
    if not values:
        return None
    root = TN(values[0])
    queue, i = deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        if values[i] is not None:
            node.left = TN(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TN(values[i])
            queue.append(node.right)
        i += 1
    return root


def levels_of(root):
    out, queue = [], deque([root] if root else [])
    while queue:
        out.append(list(queue))
        for _ in range(len(queue)):
            node = queue.popleft()
            for child in (node.left, node.right):
                if child:
                    queue.append(child)
    return out


def find(node, val):
    if node is None or node.val == val:
        return node
    return find(node.left, val) or find(node.right, val)


def draw(s, ox, oy, root, st=None, hot=None, dx=46, dy=62, r=17):
    """x = inorder rank * dx, y = depth * dy. Returns {val: (x, y)} in canvas coordinates."""
    st, hot = st or {}, hot or {}
    order, depth, kids = [], {}, []

    def walk(node, d):
        if node is None:
            return
        walk(node.left, d + 1)
        order.append(node)
        depth[node.val] = d
        walk(node.right, d + 1)
        for child in (node.left, node.right):
            if child:
                kids.append((node.val, child.val))

    walk(root, 0)
    nodes = {n.val: (k * dx, depth[n.val] * dy, n.label, st.get(n.val, 'n')) for k, n in enumerate(order)}
    edges = [(a, b, '', hot.get(b)) for a, b in kids]
    tree(s, ox, oy, nodes, edges, r=r)
    return {v: (ox + x, oy + y) for v, (x, y, _, _) in nodes.items()}


def level_styles(root):
    return {n.val: LEVEL_ST[d] for d, lv in enumerate(levels_of(root)) for n in lv}


def side_label(s, pos, root, texts, size=12.5, bold=True):
    """texts: {val: (text, colour)}. Left children get the label up-left, right children up-right."""
    def walk(node, where):
        if node is None:
            return
        if node.val in texts:
            t, col = texts[node.val]
            x, y = pos[node.val]
            if where == 'top':
                s.text(x, y - 28, t, size, COL.get(col, col), bold=bold)
            else:
                sg = -1 if where == 'l' else 1
                s.text(x + sg * 14, y - 24, t, size, COL.get(col, col), 'end' if sg < 0 else 'start', bold=bold)
        walk(node.left, 'l')
        walk(node.right, 'r')
    walk(root, 'top')


# ---------- 层序遍历 ----------

def level_mixed():
    s = S()
    root = build(RUN)
    st = level_styles(root)
    s.text(LX, 18, '同一棵树，两种循环', 14.5, INK, 'start', bold=True)
    draw(s, 110, 70, root, st)
    for k in range(4):
        s.text(LX, 70 + k * 62, f'第 {k} 层', 12.5, SUB, 'start')
    # 不分层：取出 1、2 之后的队列
    queue = deque([root])
    for _ in range(2):
        node = queue.popleft()
        for child in (node.left, node.right):
            if child:
                queue.append(child)
    mixed = [n.val for n in queue]
    x = 440
    s.text(x, 58, '只写 while queue，取出 1、2 之后的队列：', 13.5, INK, 'start', bold=True)
    cells(s, x, 76, [(v, st[v]) for v in mixed])
    s.text(x + 150, 93, '第 1 层的 3 和第 2 层的 4、5 排在一起', 13, COL['red'], 'start', bold=True)
    s.text(x, 132, '节点还是按层序出队的，但是看不出一层在哪里结束', 13, SUB, 'start')
    lv = levels_of(root)
    s.text(x, 186, '加上 for _ in range(len(queue))，每一轮开始时的队列：', 13.5, INK, 'start', bold=True)
    cx = x
    for k, level in enumerate(lv):
        cs = cells(s, cx, 204, [(n.val, st[n.val]) for n in level])
        s.text(cx, 252, f'第 {k + 1} 轮', 12.5, SUB, 'start')
        cx = cs[-1][0] + cs[-1][1] + 34
    s.text(x, 280, '每一轮开始时，队列里正好是完整的一层', 13, COL['grn'], 'start', bold=True)
    s.save('lcq-level-mixed')


def level_trace():
    s = S()
    root = build(RUN)
    st = level_styles(root)
    draw(s, 110, 62, root, st)
    for k in range(4):
        s.text(LX, 62 + k * 62, f'第 {k} 层', 12.5, SUB, 'start')
    x = 430
    for dx, h in ((0, '进入 for 时的队列'), (180, 'len(queue)'), (275, '取出的 level'), (410, '放进去的孩子')):
        s.text(x + dx, 18, h, 13, SUB, 'start', bold=True)
    queue, k, result = deque([root]), 0, []
    while queue:
        y = 45 + k * 62
        cells(s, x, y, [(n.val, st[n.val]) for n in queue])
        s.text(x + 215, y + 17, len(queue), 15, INK, bold=True, mono=True)
        level, added = [], []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            for child in (node.left, node.right):
                if child:
                    queue.append(child)
                    added.append(child.val)
        result.append(level)
        s.text(x + 275, y + 17, str(level), 14, COL['grn'], 'start', bold=True, mono=True)
        s.text(x + 410, y + 17, '、'.join(map(str, added)) or '无', 14, INK, 'start')
        k += 1
    s.text(LX, 308, f'返回 {result}', 14, INK, 'start', bold=True, mono=True)
    s.save('lcq-level-trace')


def level_right():
    s = S()
    root = build(RUN)
    lv = levels_of(root)
    last = [level[-1].val for level in lv]
    st = {n.val: ('hit' if n.val in last else 'n') for level in lv for n in level}
    s.text(LX, 18, '从右边看：每一层只看得到最后一个节点', 14.5, INK, 'start', bold=True)
    pos = draw(s, 60, 72, root, st)
    right = max(x for x, _ in pos.values()) + 150
    for k, v in enumerate(last):
        x, y = pos[v]
        s.arrow(right, y, x + 24, y, 'grn')
        s.text(right + 12, y, f'第 {k} 层看到 {v}', 13.5, COL['grn'], 'start', bold=True)
    s.text(right + 70, 30, '眼睛在这一侧', 13, SUB, 'start')
    s.text(LX, 300, f'答案 {last}。节点 7 在左子树里，但是第 3 层只有它，右边没有东西挡住', 13.5, INK, 'start', bold=True)
    walk, node = [], root
    while node:
        walk.append(node.val)
        node = node.right
    s.text(LX, 324, '错误的想法「从根一直往右孩子走」：' + ' → '.join(map(str, walk)) + '，漏掉 7', 13.5, COL['red'], 'start')
    legend(s, LX, 344, [('hit', '每层最后出队的节点'), ('n', '被挡住的节点')])
    s.save('lcq-level-right')


def level_zigzag():
    s = S()
    root = build(RUN)
    lv = levels_of(root)
    pos = draw(s, 110, 62, root, level_styles(root))
    x = 420
    for dx, h in ((0, '出队顺序'), (150, 'left_to_right'), (280, '方向'), (350, '存进 result 的')):
        s.text(x + dx, 18, h, 13, SUB, 'start', bold=True)
    left_to_right, result = True, []
    for k, level in enumerate(lv):
        y = 45 + k * 62
        s.text(LX, 62 + k * 62, f'第 {k} 层', 12.5, SUB, 'start')
        vals = [n.val for n in level]
        cells(s, x, y, vals)
        s.text(x + 150, y + 17, str(left_to_right), 14, INK, 'start', bold=True, mono=True)
        col = 'grn' if left_to_right else 'org'
        if left_to_right:
            s.arrow(x + 282, y + 17, x + 322, y + 17, col, sw=2.4)
        else:
            s.arrow(x + 322, y + 17, x + 282, y + 17, col, sw=2.4)
        stored = vals if left_to_right else vals[::-1]
        cells(s, x + 350, y, [(v, 'hit' if left_to_right else 'new') for v in stored])
        result.append(stored)
        left_to_right = not left_to_right
    s.text(LX, 308, f'返回 {result}', 14, INK, 'start', bold=True, mono=True)
    s.text(LX, 332, '出队顺序永远是从左到右。只有标成橙色的层在存进 result 之前反转了一次', 13.5, SUB, 'start')
    s.save('lcq-level-zigzag')


def next_arrows(s, pos, pairs, col, r=17):
    for a, b in pairs:
        (x1, y1), (x2, _) = pos[a], pos[b]
        s.arrow(x1 + r + 3, y1, x2 - r - 3, y1, col, sw=2.2)


def level_connect():
    s = S()
    root = build([1, 2, 3, 4, 5, 6, 7])
    # 队列版的真实执行
    made = []
    queue = deque([root])
    while queue:
        prev = None
        for _ in range(len(queue)):
            node = queue.popleft()
            if prev:
                prev.next = node
                made.append((prev.val, node.val))
            prev = node
            for child in (node.left, node.right):
                if child:
                    queue.append(child)
    s.text(LX, 18, '同一层里，上一个出队的节点（prev）的 next 指向当前节点', 14.5, INK, 'start', bold=True)
    pos = draw(s, 70, 70, root, dx=62)
    next_arrows(s, pos, made, 'red')
    for level in levels_of(root):
        x, y = pos[level[-1].val]
        s.arrow(x + 20, y, x + 58, y, 'gry', dash=1)
        s.text(x + 84, y, 'None', 13.5, SUB, bold=True, mono=True)
    s.text(LX, 232, '红色箭头：这次改的 next，共 ' + '、'.join(f'{a}.next = {b}' for a, b in made), 13.5, COL['red'], 'start', bold=True)
    s.text(LX, 256, '灰色虚线：每层最后一个节点的 next 没有人改，保持 None', 13.5, SUB, 'start')
    s.save('lcq-level-connect')


def level_connect_o1():
    s = S()
    root = build([1, 2, 3, 4, 5, 6, 7])
    root.left.next = root.right                         # 第 1 层已经连好
    same, cross = [], []
    node = root.left                                    # leftmost = 2
    while node:
        same.append((node.left.val, node.right.val))
        if node.next:
            cross.append((node.right.val, node.next.left.val))
        node = node.next
    s.text(LX, 18, 'leftmost = 2：站在已经连好的第 1 层，顺着 next 走，把第 2 层连起来', 14.5, INK, 'start', bold=True)
    pos = draw(s, 70, 70, root, {2: 'hit', 3: 'hit'}, dx=62)
    next_arrows(s, pos, [(2, 3)], 'grn')
    next_arrows(s, pos, same, 'org')
    next_arrows(s, pos, cross, 'red')
    x = 540
    lines(s, x, 62, [('绿色：上一轮已经连好的 next', 'grn'), '    靠它从节点 2 走到节点 3',
                     ('橙色 ①：node.left.next = node.right', 'org'),
                     '    ' + '、'.join(f'{a}.next = {b}' for a, b in same),
                     ('红色 ②：node.right.next = node.next.left', 'red'),
                     '    ' + '、'.join(f'{a}.next = {b}' for a, b in cross) + '（node = 2，node.next = 3）'], gap=25)
    s.text(LX, 232, '① 连的是同一个父亲的两个孩子；② 连的是相邻两个父亲之间的那一对，要靠父亲的 next 才找得到', 13.5, SUB, 'start')
    s.save('lcq-level-connect-o1')


def level_min_depth():
    s = S()
    root = build([3, 9, 20, N, N, 15, 7])
    queue, depth, seen, answer = deque([root]), 1, [], None
    while queue and answer is None:
        for _ in range(len(queue)):
            node = queue.popleft()
            seen.append(node.val)
            if not node.left and not node.right:
                answer = (node.val, depth)
                break
            for child in (node.left, node.right):
                if child:
                    queue.append(child)
        depth += 1
    waiting = [n.val for n in queue]
    st = {v: 'n' for v in seen}
    st[answer[0]] = 'hit'
    for v in waiting:
        st[v] = 'new'
    for v in (15, 7):
        st.setdefault(v, 'del')
    s.text(LX, 18, 'BFS 一层一层往下，第一次遇到的叶子就是最浅的叶子', 14.5, INK, 'start', bold=True)
    pos = draw(s, 150, 70, root, st, dx=52)
    for k in range(3):
        s.text(LX, 70 + k * 62, f'depth = {k + 1}', 12.5, SUB, 'start', mono=True)
    x = 450
    lines(s, x, 62, [f'出队顺序：{"、".join(map(str, seen))}',
                     (f'节点 {answer[0]} 没有孩子，是叶子：返回 depth = {answer[1]}', 'grn'),
                     f'节点 {"、".join(map(str, waiting))} 还在队列里，没有处理',
                     '节点 15、7 根本没有入队'], gap=26)
    legend(s, LX, 226, [('n', '处理过'), ('hit', '第一个叶子'), ('new', '还在队列里'), ('del', '没有入队')])
    s.save('lcq-level-min-depth')


# ---------- 二叉搜索树 ----------

def bst_def():
    s = S()
    good, bad = build([5, 4, 7, N, N, 6, 8]), build([5, 4, 6, N, N, 3, 7])
    s.text(LX, 18, '是 BST', 14.5, COL['grn'], 'start', bold=True)
    pos = draw(s, 50, 72, good, {6: 'hit'}, dx=52)
    s.text(LX, 232, '6 在 5 的右子树里，比 5 大', 13.5, INK, 'start')
    s.text(LX, 256, '每个节点：左子树全部更小，右子树全部更大', 13.5, SUB, 'start')
    ox = 400
    s.seg(ox - 30, 10, ox - 30, 262, '#E5E7EB', sw=1)
    s.text(ox, 18, '不是 BST', 14.5, COL['red'], 'start', bold=True)
    pos = draw(s, ox + 32, 72, bad, {3: 'chg'}, dx=52)
    s.text(ox, 232, '3 在 5 的右子树里，却比 5 小', 13.5, COL['red'], 'start', bold=True)
    s.text(ox, 256, '只和孩子比看不出来：4 < 5 < 6，3 < 6 < 7 都成立', 13.5, SUB, 'start')
    s.save('lcq-bst-def')


def bst_inorder():
    s = S()
    root = build(BST)
    order = []

    def inorder(node):
        if node:
            inorder(node.left)
            order.append(node.val)
            inorder(node.right)
    inorder(root)
    s.text(LX, 18, '把每个节点垂直投到下面：从左到右读出来，就是中序遍历，也就是升序', 14.5, INK, 'start', bold=True)
    dx = 58
    pos = draw(s, 60, 68, root, dx=dx)
    y = 68 + 3 * 62 + 62
    for v in order:
        x, ny = pos[v]
        s.seg(x, ny + 20, x, y - 4, 'gry', dash=1, sw=1.2)
        s.node(x - 21, y, v, 'hit', w=42, h=34, size=15)
    s.text(60 + len(order) * dx - 10, y + 17, '中序遍历', 13.5, COL['grn'], 'start', bold=True)
    assert order == sorted(order)
    s.save('lcq-bst-inorder')


def search_path(root, target):
    path, node = [], root
    while node:
        path.append(node.val)
        if target == node.val:
            return path, True
        node = node.left if target < node.val else node.right
    return path, False


def bst_search():
    s = S()
    for k, target in enumerate((7, 5)):
        root = build(BST)
        path, found = search_path(root, target)
        ox = 18 + k * 470
        if k:
            s.seg(ox - 22, 10, ox - 22, 392, '#E5E7EB', sw=1)
        s.text(ox, 18, f'找 {target}', 14.5, INK, 'start', bold=True)
        st = {v: 'new' for v in path}
        if found:
            st[path[-1]] = 'hit'
        hot = {v: 'org' for v in path[1:]}
        pos = draw(s, ox + 30, 72, root, st, hot, dx=50)
        steps = []
        for v in path:
            steps.append(f'{target} = {v}' if target == v else f'{target} < {v} 往左' if target < v else f'{target} > {v} 往右')
        for i, t in enumerate(steps):
            last_miss = i == len(steps) - 1 and not found
            s.text(ox + (i % 2) * 190, 336 + (i // 2) * 22, f'{"①②③④"[i]} {t}', 13,
                   COL['red'] if last_miss else INK, 'start')
        steps_y = 336 + ((len(steps) - 1) // 2 + 1) * 22
        if found:
            s.text(ox, steps_y, f'找到，返回节点 {target}', 13.5, COL['grn'], 'start', bold=True)
        else:
            x, y = pos[path[-1]]
            s.seg(x + 12, y + 14, x + 30, y + 44, 'gry', dash=1)
            s.text(x + 40, y + 56, 'None', 13, COL['red'], bold=True, mono=True)
            s.text(ox, steps_y, f'{path[-1]} 没有右孩子，node 变成 None，返回 None', 13.5, COL['red'], 'start', bold=True)
    s.save('lcq-bst-search')


def bst_insert():
    s = S()
    root = build(BST)
    val = 5
    node, path = root, []
    while True:
        path.append(node.val)
        if val < node.val:
            if node.left is None:
                node.left = TN(val)
                side = 'left'
                break
            node = node.left
        else:
            if node.right is None:
                node.right = TN(val)
                side = 'right'
                break
            node = node.right
    st = {v: 'sent' for v in path}
    st[val] = 'new'
    hot = {v: 'org' for v in path[1:]}
    hot[val] = 'org'
    s.text(LX, 18, f'插入 {val}：像查找一样往下走，走到空位就把新节点接上', 14.5, INK, 'start', bold=True)
    draw(s, 50, 72, root, st, hot, dx=52)
    x = 520
    lines(s, x, 72, ['走过的路：' + ' → '.join(map(str, path)),
                     (f'{val} > {path[-1]}，该往右，{path[-1]} 的右边是空位', INK, False),
                     (f'{path[-1]}.{side} = TreeNode({val})', 'org'),
                     ('原来的节点一个都没有动', 'gry', False)], gap=27)
    legend(s, LX, 362, [('sent', '路上经过的节点'), ('new', '新接上的叶子')])
    s.save('lcq-bst-insert')


def bst_lca():
    s = S()
    values = [6, 2, 8, 0, 4, 7, 9, N, N, 3, 5]
    for k, (a, b) in enumerate(((3, 5), (2, 4))):
        root = build(values)
        node, path = root, []
        while node:
            path.append(node.val)
            if a < node.val and b < node.val:
                node = node.left
            elif a > node.val and b > node.val:
                node = node.right
            else:
                break
        answer = path[-1]
        ox = 18 + k * 480
        if k:
            s.seg(ox - 22, 10, ox - 22, 356, '#E5E7EB', sw=1)
        s.text(ox, 18, f'p = {a}，q = {b}', 14.5, INK, 'start', bold=True)
        st = {v: 'sent' for v in path}
        st[a] = st[b] = 'new'
        st[answer] = 'hit'
        pos = draw(s, ox + 30, 72, root, st, {v: 'org' for v in path[1:]}, dx=48)
        for v, name in ((a, 'p'), (b, 'q')):
            x, y = pos[v]
            s.text(x, y + 30, name, 13.5, COL['org'], bold=True, mono=True)
        s.text(ox, 322, '走过的路：' + ' → '.join(map(str, path)), 13.5, INK, 'start')
        why = (f'{a} < {answer} < {b}：p、q 分到了两边' if answer not in (a, b)
               else f'node 就是 {"p" if answer == a else "q"} 自己，不能再往下走')
        s.text(ox, 346, f'在 {answer} 停下：{why}', 13.5, COL['grn'], 'start', bold=True)
    s.save('lcq-bst-lca')


def bst_bounds():
    s = S()
    root = build([5, 4, 6, N, N, 3, 7])
    ranges, visited = {}, []

    def give(node, low, high):                          # 每个节点应得的范围（不管走没走到）
        if node:
            ranges[node.val] = (low, high)
            give(node.left, low, node.val)
            give(node.right, node.val, high)

    def check(node, low, high):                         # 正文里的 check，记下真正访问过的节点
        if node is None:
            return True
        visited.append(node.val)
        if not (low < node.val < high):
            return False
        return check(node.left, low, node.val) and check(node.right, node.val, high)

    give(root, float('-inf'), float('inf'))
    ok = check(root, float('-inf'), float('inf'))
    bad = visited[-1]

    def show(v):
        low, high = ranges[v]
        f = lambda t: '-∞' if t == float('-inf') else '+∞' if t == float('inf') else str(t)
        return f'({f(low)}, {f(high)})'

    st = {v: 'hit' for v in visited}
    st[bad] = 'chg'
    for v in ranges:
        st.setdefault(v, 'off')
    s.text(LX, 18, '每个节点旁边是它允许的范围 (low, high)。往左走收紧上界，往右走收紧下界', 14.5, INK, 'start', bold=True)
    pos = draw(s, 150, 84, root, st, dx=92)
    texts = {}
    for v in ranges:
        col = 'red' if v == bad else 'grn' if v in visited else 'gry'
        texts[v] = (show(v), col)
    side_label(s, pos, root, texts, size=13)
    x, y = pos[bad]
    s.text(x, y + 32, f'{bad} 不在 {show(bad)} 里', 13, COL['red'], bold=True)
    s.text(LX, 262, f'节点 {bad} 的下界 5 是从祖先 5 传下来的。检查到它就返回 {ok}，节点 7 没有走到', 13.5, INK, 'start', bold=True)
    legend(s, LX, 284, [('hit', '在范围里'), ('chg', '不在范围里'), ('off', '没有走到')])
    s.save('lcq-bst-bounds')


def bst_kth():
    s = S()
    root = build(BST)
    k, stack, node, visited = 3, [], root, []
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        visited.append(node.val)
        k -= 1
        if k == 0:
            break
        node = node.right
    in_stack = [n.val for n in stack]
    st = {v: 'hit' for v in visited}
    for v in in_stack:
        st[v] = 'new'
    for v in (7, 10, 14):
        st.setdefault(v, 'off')
    s.text(LX, 18, 'k = 3：中序遍历访问到第 3 个节点就返回', 14.5, INK, 'start', bold=True)
    pos = draw(s, 96, 76, root, st, dx=54)
    side_label(s, pos, root, {v: (f'第 {i + 1} 个', 'grn') for i, v in enumerate(visited)})
    x = 566
    lines(s, x, 76, ['访问顺序：' + '、'.join(map(str, visited)),
                     (f'第 3 个是 {visited[-1]}，返回 {visited[-1]}', 'grn'),
                     f'这时栈里还有 {"、".join(map(str, in_stack))}，不用管了',
                     ('节点 7、10、14 没有碰过', 'gry', False)], gap=27)
    legend(s, LX, 344, [('hit', '访问过'), ('new', '还在栈里'), ('off', '没有碰过')])
    s.save('lcq-bst-kth')


def delete_node(root, key):
    if root is None:
        return None
    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        successor = root.right
        while successor.left:
            successor = successor.left
        root.val = root.label = successor.val
        root.right = delete_node(root.right, successor.val)
    return root


def bst_delete():
    s = S()
    cases = [(4, '① 没有孩子：直接去掉', '6.left 变成 None'),
             (10, '② 只有一个孩子：孩子顶上来', '8.right 变成 14'),
             (3, '③ 有两个孩子：换成右子树里最小的值', '右子树里最小的是 4：把 3 改成 4，再去右子树删掉 4')]
    dx, ph = 40, 318
    for k, (key, title, how) in enumerate(cases):
        oy = 14 + k * ph
        if k:
            s.seg(LX, oy - 14, 900, oy - 14, '#E5E7EB', sw=1)
        s.text(LX, oy + 10, f'{title}（删 {key}）', 14.5, INK, 'start', bold=True)
        before = build(BST)
        st = {key: 'chg'}
        if k == 1:
            st[14] = 'new'
        if k == 2:
            st[4] = 'new'
        draw(s, 50, oy + 58, before, st, dx=dx)
        s.text(50 + 3.5 * dx, oy + 36, '删之前', 12.5, SUB)
        big_arrow(s, 380, oy + 140, f'delete_node(root, {key})')
        after = delete_node(build(BST), key)
        st2 = {14: 'hit'} if k == 1 else {4: 'hit'} if k == 2 else {}
        draw(s, 520, oy + 58, after, st2, dx=dx)
        s.text(520 + 3 * dx, oy + 36, '删之后', 12.5, SUB)
        s.text(LX, oy + 284, how, 13.5, COL['grn'], 'start', bold=True)
    legend(s, LX, 14 + 3 * ph - 6, [('chg', '要删的节点'), ('new', '顶替它的节点 / 值'), ('hit', '删完后在它位置上的')])
    s.save('lcq-bst-delete')


# ---------- 最近公共祖先 ----------

def lca_cases():
    s = S()
    panels = [('p', 'q', '返回 root', 'grn', '左右都找到：在这里汇合'),
              ('p', 'None', '返回左边的结果', 'org', '只有左边找到：原样往上交'),
              ('None', 'q', '返回右边的结果', 'org', '只有右边找到：原样往上交'),
              ('None', 'None', '返回 None', 'gry', '两边都没找到')]
    pw = 240
    for k, (lt, rt, out, col, cap) in enumerate(panels):
        ox = 18 + k * pw
        if k:
            s.seg(ox - 12, 10, ox - 12, 250, '#E5E7EB', sw=1)
        cx = ox + 100
        s.text(cx, 18, f'情况 {k + 1}', 14, INK, bold=True)
        s.arrow(cx, 86, cx, 52, col, sw=2.2)
        s.text(cx + 10, 66, out, 13, COL[col], 'start', bold=True)
        s.node(cx - 34, 90, 'root', 'hit' if k == 0 else 'n', w=68, h=34, size=14)
        for sg, t in ((-1, lt), (1, rt)):
            bx = cx + sg * 56
            found = t != 'None'
            s.seg(cx + sg * 14, 126, bx, 164, 'org' if found else 'gry', sw=2.4 if found else 1.6, dash=0 if found else 1)
            s.node(bx - 40, 166, '左子树' if sg < 0 else '右子树', 'new' if found else 'off', w=80, h=34, size=13, mono=False)
            s.text(bx, 214, f'返回 {t}' if found else '返回 None', 12.5, COL['org'] if found else SUB, bold=found, mono=found)
        s.text(cx, 240, cap, 13, SUB)
    s.text(18, 276, '「返回 p」的意思是：那棵子树里找到了东西（p、q，或者它们已经汇合出的公共祖先）', 13.5, SUB, 'start')
    s.save('lcq-lca-cases')


def lca_trace():
    s = S()
    values = [3, 5, 1, 6, 2, 0, 8, N, N, 7, 4]
    root = build(values)
    p, q = find(root, 6), find(root, 4)
    returned = {}

    def lca(node):
        if node is None or node is p or node is q:
            if node is not None:
                returned[node.val] = node
            return node
        left_found, right_found = lca(node.left), lca(node.right)
        out = node if (left_found and right_found) else (left_found or right_found)
        returned[node.val] = out
        return out

    answer = lca(root)
    st = {v: ('n' if r else 'off') for v, r in returned.items()}
    st[p.val] = st[q.val] = 'new'
    st[answer.val] = 'hit'
    hot = {v: 'org' for v, r in returned.items() if r is not None and v != root.val}
    s.text(LX, 18, f'p = {p.val}，q = {q.val}。每个节点旁边是它返回给父节点的值', 14.5, INK, 'start', bold=True)
    pos = draw(s, 90, 96, root, st, hot, dx=74, dy=66)
    texts = {v: ((f'返回 {r.val}', 'org' if v != answer.val else 'grn') if r else ('返回 None', 'gry'))
             for v, r in returned.items()}
    side_label(s, pos, root, texts, size=13)
    for node, name in ((p, 'p'), (q, 'q')):
        x, y = pos[node.val]
        s.text(x, y + 30, name, 13.5, COL['org'], bold=True, mono=True)
    x, y = pos[answer.val]
    s.text(x - 26, y + 8, '左 6、右 4', 12.5, COL['grn'], 'end', bold=True)
    s.text(LX, 382, f'节点 {answer.val}：左子树返回 6，右子树返回 4，两边都找到了，返回自己。'
                    f'节点 3 只有左边有返回值，把 {answer.val} 原样交上去', 13.5, INK, 'start', bold=True)
    legend(s, LX, 404, [('new', 'p 和 q'), ('hit', '最近公共祖先'), ('n', '返回了找到的节点'), ('off', '返回 None')])
    s.save('lcq-lca-trace')


# ---------- 构造二叉树 ----------

def split_rows(s, x, y, name, arr, root_at, left_len, cw=52):
    """One array split into root / left / right. root_at: 'first' | 'mid' | 'last'."""
    n = len(arr)
    if root_at == 'first':
        ri, lo, ro = 0, 1, 1 + left_len
    elif root_at == 'mid':
        ri, lo, ro = left_len, 0, left_len + 1
    else:
        ri, lo, ro = n - 1, 0, left_len
    sts = ['chg' if i == ri else 'n' if lo <= i < lo + left_len else 'new' for i in range(n)]
    s.text(x - 14, y + 17, name, 14, INK, 'end', bold=True, mono=True)
    cs = row(s, x, y, arr, sts, cw=cw, idx='top')
    brace(s, cs[ri] - 20, cs[ri] + 20, y + 44, '根', 'red', up=False)
    if left_len:
        brace(s, cs[lo] - 20, cs[lo + left_len - 1] + 20, y + 44, f'左子树 {left_len} 个', 'blue', up=False)
    if n - 1 - left_len:
        brace(s, cs[ro] - 20, cs[n - 1] + 20, y + 44, f'右子树 {n - 1 - left_len} 个', 'org', up=False)
    return cs


def build_split():
    s = S()
    preorder, inorder = [3, 9, 20, 15, 7], [9, 3, 15, 20, 7]
    root_index = inorder.index(preorder[0])
    left_size = root_index
    s.text(LX, 18, 'build(0, 0, 5)：用根把两个数组各切成三块', 14.5, INK, 'start', bold=True)
    x = 150
    split_rows(s, x, 66, 'preorder', preorder, 'first', left_size)
    split_rows(s, x, 176, 'inorder', inorder, 'mid', left_size)
    tx = 470
    lines(s, tx, 62, [('① 前序的第一个数是根：preorder[0] = 3', 'red'),
                      ('② 根在中序里的下标 root_index = 1', INK),
                      (f'    它左边有 left_size = {root_index} - 0 = {left_size} 个数：左子树', 'blue'),
                      ('    它右边的 3 个数：右子树', 'org'),
                      ('③ 前序里根后面先是左子树的 1 个数，再是右子树的 3 个数', INK)], gap=26)
    lines(s, tx, 204, [('左子树  build(1, 0, 1)：preorder 从下标 1 起 1 个，inorder 从下标 0 起 1 个', 'blue'),
                       ('右子树  build(2, 2, 3)：preorder 从下标 2 起 3 个，inorder 从下标 2 起 3 个', 'org')], gap=26)
    legend(s, LX, 262, [('chg', '根'), ('n', '左子树'), ('new', '右子树')])
    s.save('lcq-build-split')


def build_trace():
    s = S()
    preorder, inorder = [3, 9, 20, 15, 7], [9, 3, 15, 20, 7]
    index_of = {v: i for i, v in enumerate(inorder)}
    calls = {}

    def go(pre_start, in_start, size):
        if size == 0:
            return None
        node = TN(preorder[pre_start])
        calls[node.val] = (pre_start, in_start, size)
        root_index = index_of[node.val]
        left_size = root_index - in_start
        node.left = go(pre_start + 1, in_start, left_size)
        node.right = go(pre_start + 1 + left_size, root_index + 1, size - 1 - left_size)
        return node

    root = go(0, 0, len(preorder))
    s.text(LX, 18, '每个节点由一次 build(pre_start, in_start, size) 建出来', 14.5, INK, 'start', bold=True)
    pos = draw(s, 190, 96, root, dx=104, dy=70)
    side_label(s, pos, root, {v: (f'build{c}', 'blue') for v, c in calls.items()}, size=13)
    x = 150
    y = 300
    for name, arr, yy in (('preorder', preorder, y), ('inorder', inorder, y + 62)):
        s.text(x - 14, yy + 17, name, 14, INK, 'end', bold=True, mono=True)
        row(s, x, yy, arr, 'n', cw=52, idx='top')
    s.text(x + 300, y + 17, '叶子 9：build(1, 0, 1) 用的是 preorder[1] 和 inorder[0]', 13.5, SUB, 'start')
    s.text(x + 300, y + 79, '节点 20：build(2, 2, 3) 用的是 preorder[2..4] 和 inorder[2..4]', 13.5, SUB, 'start')
    s.save('lcq-build-trace')


def build_post():
    s = S()
    inorder, postorder = [9, 3, 15, 20, 7], [9, 15, 7, 20, 3]
    root_index = inorder.index(postorder[-1])
    left_size = root_index
    s.text(LX, 18, 'build(0, 0, 5)：后序的最后一个数是根，其余和 LC 105 一样', 14.5, INK, 'start', bold=True)
    x = 150
    split_rows(s, x, 66, 'postorder', postorder, 'last', left_size)
    split_rows(s, x, 176, 'inorder', inorder, 'mid', left_size)
    tx = 470
    lines(s, tx, 62, [('① 后序的最后一个数是根：postorder[0 + 5 - 1] = 3', 'red'),
                      ('② 根在中序里的下标 root_index = 1，left_size = 1', INK),
                      ('③ 后序里先是左子树的 1 个数，再是右子树的 3 个数，最后是根', INK)], gap=26)
    lines(s, tx, 178, [('左子树  build(0, 0, 1)：postorder 从下标 0 起 1 个', 'blue'),
                       ('右子树  build(1, 2, 3)：postorder 从下标 1 起 3 个', 'org'),
                       ('中序那一边的两个起点（0 和 2）和 LC 105 完全相同', 'gry', False)], gap=26)
    legend(s, LX, 262, [('chg', '根'), ('n', '左子树'), ('new', '右子树')])
    s.save('lcq-build-post')


def codec():
    s = S()
    root = build([1, 2, 3, N, N, 4, 5])
    parts, order = [], []
    counter = [0]

    def dfs(node, parent, side):
        if node is None:
            counter[0] += 1
            ghost = TN(f'N{counter[0]}', 'N')
            setattr(parent, side, ghost)                # 把空位置也画成一个节点
            parts.append('N')
            order.append(ghost.val)
            return
        parts.append(str(node.val))
        order.append(node.val)
        left, right = node.left, node.right
        dfs(left, node, 'left')
        dfs(right, node, 'right')

    dfs(root, None, None)
    st = {v: 'del' for v in order if str(v).startswith('N')}
    s.text(LX, 18, '前序遍历，空孩子也记一笔（N）。节点旁边的数字是写出来的先后顺序', 14.5, INK, 'start', bold=True)
    pos = draw(s, 60, 80, root, st, dx=50, dy=62)
    side_label(s, pos, root, {v: (str(i + 1), 'org') for i, v in enumerate(order)}, size=12)
    y = 80 + 3 * 62 + 52
    s.text(LX, y + 17, '写出的各项', 13.5, INK, 'start', bold=True)
    x0 = 110
    for i, t in enumerate(parts):
        s.node(x0 + i * 45, y, t, 'del' if t == 'N' else 'n', w=42, h=34, size=15)
        s.text(x0 + i * 45 + 21, y - 11, i + 1, 11.5, COL['org'], bold=True, mono=True)
    s.text(LX, y + 62, 'serialize 的结果："' + ','.join(parts) + '"', 14, INK, 'start', bold=True, mono=True)
    n_nodes = sum(1 for t in parts if t != 'N')
    s.text(LX, y + 88, f'{n_nodes} 个节点，{len(parts) - n_nodes} 个空位置，一共 {len(parts)} 项。'
                       '反序列化按同样的顺序一项一项读回来', 13.5, SUB, 'start')
    s.save('lcq-codec')


if __name__ == '__main__':
    for func in (level_mixed, level_trace, level_right, level_zigzag, level_connect, level_connect_o1, level_min_depth,
                 bst_def, bst_inorder, bst_search, bst_insert, bst_lca, bst_bounds, bst_kth, bst_delete,
                 lca_cases, lca_trace, build_split, build_trace, build_post, codec):
        func()
    print('ok')
