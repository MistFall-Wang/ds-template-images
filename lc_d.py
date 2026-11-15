#!/usr/bin/env python3
"""Diagrams for the LeetCode parts of 单链表 / 双链表 (prefix lcd-).

Run from this directory:  python3 lc_d.py
"""
from make_diagrams import *

NONE_W = 46


def row(s, x, y, labels, links, styles=None, gap=GAP):
    """None, nodes, None in a line. links[i] = ('r' | 'l', colour) for the gap between
    node i and node i + 1; i = -1 is the left None, i = n - 1 is the right None.
    Returns the centre x of [left None, node 0 .. node n-1, right None]."""
    styles = styles or {}
    n = len(labels)
    xs, cx = [], x
    s.text(cx + NONE_W / 2, y + NH / 2, 'None', 15, SUB, bold=True, mono=True)
    edges = [(cx, cx + NONE_W)]
    cx += NONE_W + gap
    for i, t in enumerate(labels):
        s.node(cx, y, t, styles.get(i, 'n'))
        edges.append((cx, cx + NW))
        cx += NW + gap
    s.text(cx + NONE_W / 2, y + NH / 2, 'None', 15, SUB, bold=True, mono=True)
    edges.append((cx, cx + NONE_W))
    ym = y + NH / 2
    for i, (d, col) in links.items():
        x1, x2 = edges[i + 1][1] + 3, edges[i + 2][0] - 3
        if d == 'r':
            s.arrow(x1, ym, x2, ym, col)
        else:
            s.arrow(x2, ym, x1, ym, col)
    return [(a + b) / 2 for a, b in edges]


def ptrs(s, y, marks):
    """marks: (x, label, colour). Pointers on the same x share one arrow."""
    by = {}
    for x, t, c in marks:
        by.setdefault(x, []).append((t, c))
    for x, lst in by.items():
        ptr(s, x, y, ' '.join(t for t, _ in lst), lst[0][1] if len(lst) == 1 else 'red')


# ---------- 套法一：dummy ----------

def lcd_merge():
    a, b = [1, 2, 4], [1, 3, 4]
    i = j = 0
    out, rows = [], []
    rows.append(['开始', [(v, 'n') for v in a], [(v, 'hit') for v in b], '', [('dummy', 'sent')]])
    step = 0
    while i < len(a) and j < len(b):
        step += 1
        if a[i] <= b[j]:
            why, st = f'{a[i]} <= {b[j]}，接 list1 的 {a[i]}', 'n'
            out.append((a[i], st)); i += 1
        else:
            why, st = f'{a[i]} > {b[j]}，接 list2 的 {b[j]}', 'hit'
            out.append((b[j], st)); j += 1
        rows.append([f'第 {step} 轮', [(v, 'n') for v in a[i:]], [(v, 'hit') for v in b[j:]], why,
                     [('dummy', 'sent')] + out])
    rest = [(v, 'n') for v in a[i:]] + [(v, 'hit') for v in b[j:]]
    rows.append(['收尾', [], [], ('t', 'list1 空了，把 list2 剩下的整段接上', 'red'), [('dummy', 'sent')] + out + rest])
    table('lcd-merge', ['', 'list1 剩下的', 'list2 剩下的', '比较两个表头', '结果链（tail 是最右边那个）'],
          [78, 150, 150, 270, 330], rows,
          leg=[('n', '来自 list1'), ('hit', '来自 list2'), ('sent', 'dummy：不存数据，只占位')],
          foot='答案是 dummy.next：1 → 1 → 2 → 3 → 4 → 4')


def lcd_remove_nth():
    s = S()
    vals, n = [1, 2, 3, 4, 5], 2
    DX, y, RH = 262, 20, 104
    items = [('dummy', 'sent')] + [str(v) for v in vals] + ['None']
    slow = fast = 0                                   # index into items
    states = [('开始', '都站在 dummy 上', slow, fast)]
    for _ in range(n):
        fast += 1
    states.append((f'① fast 先走 n = {n} 步', '两人隔开 n 个节点', slow, fast))
    while items[fast + 1] != 'None':
        slow += 1
        fast += 1
    states.append(('② 一起走', 'fast 到最后一个节点时停', slow, fast))
    for title, sub, sl, fa in states:
        lab(s, y, title, sub)
        pos = chain(s, DX, y, items)
        ptrs(s, y + NH, [(cxp(pos, sl), 'slow', 'blue'), (cxp(pos, fa), 'fast', 'org')])
        y += RH
    lab(s, y, '③ 删 slow 的下一个', 'slow.next = slow.next.next')
    it = list(items)
    it[slow + 1] = (it[slow + 1], 'del')
    pos = chain(s, DX, y + 14, it, links={slow: None, slow + 1: 'gry'})
    s.curve(pos[slow][0] + pos[slow][1] - 12, y + 11, pos[slow + 2][0] + 12, y + 11, -19, 'red')
    ptrs(s, y + 14 + NH, [(cxp(pos, slow), 'slow', 'blue')])
    note(s, endx(pos) + 26, y + 14, f'倒数第 {n} 个是 {vals[-n]}，slow 正好停在它前面')
    s.save('lcd-remove-nth')


# ---------- 套法二：反转 ----------

def lcd_reverse():
    s = S()
    vals = ['1', '2', '3']
    n = len(vals)
    DX, y, RH = 150, 20, 104
    for k in range(n + 1):
        links = {}
        if k >= 1:
            links[-1] = ('l', 'red' if k == 1 else 'line')
        for i in range(n - 1):
            if i + 1 < k:
                links[i] = ('l', 'red' if i + 1 == k - 1 else 'line')
            elif i >= k:
                links[i] = ('r', 'line')
        if k < n:
            links[n - 1] = ('r', 'line')
        lab(s, y, '开始' if k == 0 else f'第 {k} 轮之后')
        xs = row(s, DX, y, vals, links, {i: 'hit' for i in range(k)})
        marks = [(xs[k], 'prev', 'grn'), (xs[k + 1], 'current', 'blue')]
        ptrs(s, y + NH, marks)
        if k == 0:
            note(s, xs[-1] + 44, y, 'prev = None，current = head')
        elif k < n:
            note(s, xs[-1] + 44, y, f'{vals[k - 1]} 掉头指向前面；{vals[k - 1]} 和 {vals[k]} 之间断开')
        else:
            note(s, xs[-1] + 44, y, 'current 走到 None，结束。新的头是 prev')
        y += RH
    legend(s, DX, y, [('hit', '已经掉头的节点'), ('chg', '红色箭头 = 这一轮改的指针')])
    s.save('lcd-reverse')


# ---------- 套法三：快慢指针 ----------

def lcd_middle():
    s = S()
    DX, y, RH = 150, 20, 100
    for vals in ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6]):
        n = len(vals)
        items = [str(v) for v in vals] + ['None']
        slow = fast = 0
        steps = [(slow, fast)]
        while fast < n and fast + 1 < n:              # fast and fast.next
            slow += 1
            fast += 2
            steps.append((slow, fast))
        s.text(LX, y + 8, f'{n} 个节点（{"奇数" if n % 2 else "偶数"}）', 15, INK, 'start', bold=True)
        y += 34
        for t, (sl, fa) in enumerate(steps):
            last = t == len(steps) - 1
            lab(s, y, '开始' if t == 0 else f'走 {t} 次')
            it = list(items)
            if last:
                it[sl] = (it[sl], 'hit')
            pos = chain(s, DX, y, it)
            ptrs(s, y + NH, [(cxp(pos, sl), 'slow', 'grn' if last else 'blue'), (cxp(pos, fa), 'fast', 'org')])
            if last:
                why = 'fast.next 是 None，停' if fa < n else 'fast 是 None，停'
                note(s, DX + 7 * NW + 6 * GAP + 10, y, f'{why}。slow 在 {vals[sl]}')
            y += RH
        y += 6
    s.save('lcd-middle')


def lcd_cycle():
    s = S()
    n, entry = 7, 2                                   # node n-1 points back to node `entry`
    nxt = lambda i: i + 1 if i < n - 1 else entry
    slow = fast = 0
    t = 0
    while True:
        slow, fast, t = nxt(slow), nxt(nxt(fast)), t + 1
        if slow == fast:
            break
    meet = slow
    a, b, c = entry, meet - entry, n - meet
    assert t == a + b and 2 * t - t == n - entry      # fast 多走的正好是一圈（这个例子里 k = 1）
    p, q, k = 0, meet, 0
    while p != q:
        p, q, k = nxt(p), nxt(q), k + 1
    assert p == entry and k == a == c
    DX, y = 40, 76
    items = [(str(i + 1), 'new' if i == entry else 'hit' if i == meet else 'n') for i in range(n)]
    pos = chain(s, DX, y, items)
    s.curve(cxp(pos, n - 1), y - 4, cxp(pos, entry), y - 4, -30, 'line')
    by = y + NH + 14
    brace(s, cxp(pos, 0), cxp(pos, entry) - 5, by, f'a = {a} 步', 'blue', up=False)
    brace(s, cxp(pos, entry) + 5, cxp(pos, meet) - 5, by, f'b = {b} 步', 'org', up=False)
    brace(s, cxp(pos, meet) + 5, endx(pos) + 30, by, f'c = {c} 步', 'grn', up=False)
    s.text(endx(pos) + 44, y + NH / 2, f'{n} 的 next 绕回 {entry + 1}', 13.5, SUB, 'start')
    ly = by + 46
    legend(s, DX, ly, [('new', f'入环点（{entry + 1}）'), ('hit', f'slow 和 fast 相遇的地方（{meet + 1}）')])
    for i, line in enumerate([
        f'相遇时 slow 走了 a + b = {t} 步，fast 走了 {2 * t} 步，多出来的 {t} 步正好是一圈（b + c = {b + c}）',
        f'所以 a + b = b + c，也就是 a = c：从头走 {a} 步、从相遇点走 {c} 步，都到入环点 {entry + 1}',
    ]):
        s.text(DX, ly + 44 + 24 * i, line, 14, INK, 'start', bold=i == 1)
    s.save('lcd-cycle')


# ---------- 套法四：组合 ----------

def lcd_palindrome():
    s = S()
    vals = ['1', '2', '3', '2', '1']
    n, mid = len(vals), len(vals) // 2
    DX, y, RH = 214, 20, 130
    fwd = {i: ('r', 'line') for i in range(n)}
    lab(s, y, '① 快慢指针找中点', 'slow 停在 3')
    xs = row(s, DX, y, vals, fwd)
    ptrs(s, y + NH, [(xs[mid + 1], 'slow', 'blue'), (xs[n], 'fast', 'org')])
    y += RH
    lab(s, y, '② 从 slow 开始反转', '后半段的箭头全部掉头')
    links = {i: ('r', 'line') for i in range(mid)}
    links.update({i: ('l', 'red') for i in range(mid, n - 1)})
    xs = row(s, DX, y, vals, links, {i: 'hit' for i in range(mid, n)})
    s.text(xs[mid + 1], y - 12, '3.next = None', 12.5, COL['red'], mono=True)
    ptrs(s, y + NH, [(xs[n], 'prev', 'grn')])
    note(s, xs[-1] + 40, y, '两头都指向中间的 3')
    y += RH
    lab(s, y, '③ 两头往中间比', 'right 走到 None 为止')
    xs = row(s, DX, y, vals, links, {i: 'hit' for i in range(mid, n)})
    ptrs(s, y + NH, [(xs[1], 'left', 'blue'), (xs[n], 'right', 'grn')])
    note(s, xs[-1] + 40, y, '比 3 次：1 = 1，2 = 2，3 = 3，是回文')
    s.arrow(xs[1] + 24, y + NH + 30, xs[1] + 60, y + NH + 30, 'blue')
    s.arrow(xs[n] - 24, y + NH + 30, xs[n] - 60, y + NH + 30, 'grn')
    s.save('lcd-palindrome')


# ---------- LRU ----------

class _N:
    def __init__(self, key=0, val=0):
        self.key, self.val, self.prev, self.next = key, val, None, None


class _LRU:
    def __init__(self, cap):
        self.cap, self.d = cap, {}
        self.head, self.tail = _N(), _N()
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node):
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.d:
            return -1
        node = self.d[key]
        self._remove(node)
        self._add_front(node)
        return node.val

    def put(self, key, value):
        if key in self.d:
            node = self.d[key]
            node.val = value
            self._remove(node)
            self._add_front(node)
            return None
        node = _N(key, value)
        self.d[key] = node
        self._add_front(node)
        if len(self.d) > self.cap:
            old = self.tail.prev
            self._remove(old)
            del self.d[old.key]
            return old.key
        return None

    def dump(self):
        out, p = [], self.head.next
        while p is not self.tail:
            out.append((p.key, p.val))
            p = p.next
        return out


def lcd_lru_structure():
    s = S()
    c = _LRU(3)
    for k in (1, 2, 3):
        c.put(k, k * 10)
    c.get(1)
    nodes = c.dump()                                  # [(1, 10), (3, 30), (2, 20)]
    DX, y = 150, 24
    ly = y + 110
    lab(s, y, 'cache（dict）', 'key → 节点')
    lab(s, ly, '双链表', '按使用时间排队')
    items = ['head'] + [(f'{k}:{v}', 'n') for k, v in nodes] + ['tail']
    pos = chain(s, DX, ly, items, double=True)
    for i, (k, v) in enumerate(nodes, 1):
        x = cxp(pos, i)
        s.node(x - 22, y, str(k), 'var', w=44, h=NH)
        s.arrow(x, y + NH + 3, x, ly - 4, 'org')
    s.text(cxp(pos, 1), ly + NH + 20, '最近用过', 13.5, COL['grn'], bold=True)
    s.text(cxp(pos, len(nodes)), ly + NH + 20, '最久没用，满了先淘汰它', 13.5, COL['red'], bold=True)
    note(s, endx(pos) + 26, y, '查 key：cache 一步找到节点')
    note(s, endx(pos) + 26, ly, '节点里写的是 key:value')
    s.save('lcd-lru-structure')


def lcd_lru_trace():
    c = _LRU(2)
    ops = [('put', 1, 1), ('put', 2, 2), ('get', 1), ('put', 3, 3), ('get', 2),
           ('put', 4, 4), ('get', 1), ('get', 3), ('get', 4)]
    rows = []
    for op in ops:
        key = op[1]
        had = key in c.d
        if op[0] == 'put':
            ev = c.put(key, op[2])
            name, ret = f'put({key}, {op[2]})', ''
            why = f'新 key，插到最前' + (f'；超过容量，淘汰最后的 key {ev}' if ev is not None else '')
            st = 'new'
        else:
            r = c.get(key)
            name, ret = f'get({key})', str(r)
            why = f'key {key} 在，挪到最前' if had else f'key {key} 不在'
            st = 'hit'
        lst = [(f'{k}:{v}', st if k == key else 'n') for k, v in c.dump()]
        rows.append([name, lst, ', '.join(map(str, sorted(c.d))), ('t', ret, 'red' if ret == '-1' else 'grn'), why])
    table('lcd-lru-trace', ['操作', '链表（左边最近用，右边最久没用）', 'cache 里的 key', '返回', '说明'],
          [110, 270, 120, 60, 340], rows, cw=52,
          foot='容量 capacity = 2',
          leg=[('new', '新插入的节点'), ('hit', '被访问、挪到最前的节点')])


# ---------- 基本操作图的重画（变量名改成 node / new_node） ----------
import make_diagrams as md


def _renamed(fn, *args, **kw):
    """Run a make_diagrams drawing function with pointer label p -> node and an lcd- file name."""
    old_ptr, old_save, old_note = md.ptr, S.save, md.note
    md.note = lambda s, x, y, text, color=SUB: old_note(s, x, y, text.replace('p 从', 'node 从'), color)
    md.ptr = lambda s, x, y, label, color='blue': old_ptr(s, x, y, 'node' if label in ('p', 'k') else label, color)
    S.save = lambda self, name, pad=20: old_save(self, 'lcd-' + name, pad)
    try:
        fn(*args, **kw)
    finally:
        md.ptr, S.save, md.note = old_ptr, old_save, old_note


def lcd_basic():
    sl = ['head', 'a', 'b', 'c', 'None']
    dl = ['head', 'a', 'b', 'c', 'tail']
    _renamed(md.sll_overview)
    _renamed(md.dll_overview)
    _renamed(md.ins_single, 'sll-add-head', ['head', 'a', 'b', 'None'], 0, 'new_node.next = head', 'head = new_node')
    _renamed(md.ins_single, 'sll-add-after', ['···', 'node', '后一个', '···'], 1,
             'new_node.next = node.next', 'node.next = new_node')
    _renamed(md.rem_single, 'sll-remove-after', ['···', 'node', '要删的', '后一个', '···'], 1,
             'node.next = node.next.next')
    _renamed(md.walk, 'sll-traverse', sl,
             [(1, 'node = head，输出 a', None, 'blue'), (2, 'node = node.next，输出 b', None, 'blue'),
              (3, 'node = node.next，输出 c', None, 'blue'), (4, 'node 是 None，结束', None, 'red')])
    _renamed(md.walk, 'sll-find', sl,
             [(1, 'a != c，往后走', None, 'blue'), (2, 'b != c，往后走', None, 'blue'),
              (3, 'c == c，找到，返回 node', 'hit', 'grn')])
    _renamed(md.walk, 'sll-get', sl,
             [(1, 'node = head，这是第 0 个', None, 'blue'), (2, 'node = node.next，第 1 个', None, 'blue'),
              (3, 'node = node.next，第 2 个，返回 node', 'hit', 'grn')], labels=['起点', '走 1 步', '走 2 步'])
    _renamed(md.walk, 'dll-traverse', dl,
             [(1, 'node = head.next，输出 a', None, 'blue'), (2, 'node = node.next，输出 b', None, 'blue'),
              (3, 'node = node.next，输出 c', None, 'blue'), (4, 'node 是 tail，结束', None, 'red')], double=True)
    _renamed(md.walk, 'dll-find', dl,
             [(1, 'a != b，往右走', None, 'blue'), (2, 'b == b，找到，返回 node', 'hit', 'grn')], double=True)
    for name, double in (('lcd-sll-modify', False), ('lcd-dll-modify', True)):
        s = S()
        DX, y = 110, 20
        pre = ['head', 'a', 'b', 'c', 'tail' if double else 'None']
        lab(s, y, '修改前')
        pos = chain(s, DX, y, pre, double=double)
        ptr(s, cxp(pos, 2), y + NH, 'node', 'blue')
        y += 104
        lab(s, y, '修改后')
        pre[2] = ('y', 'chg')
        pos = chain(s, DX, y, pre, double=double)
        ptr(s, cxp(pos, 2), y + NH, 'node', 'red')
        note(s, endx(pos) + 30, y, 'node.val = y：只有值变了，指针一根没动')
        s.save(name)


def lcd_dll_add():
    s = S()
    DX, G, y = 280, 124, 22
    items = ['···', 'node', '右邻居', '···']
    lab(s, y, '插入前')
    chain(s, DX, y, items, double=True, gap=G)
    y += 84
    steps = [('第 1 步：接 x 自己的两根线', ['① new_node.prev = node', '② new_node.next = node.next']),
             ('第 2 步：改远的右邻居', ['③ node.next.prev = new_node']),
             ('第 3 步：改近的 node', ['④ node.next = new_node'])]
    for n, (title, code) in enumerate(steps, 1):
        lab(s, y + 40, title, code)
        links = {} if n == 1 else {1: ('line', None)} if n == 2 else {1: (None, None)}
        pos = chain(s, DX, y, items, double=True, links=links, gap=G)
        kx, rx = cxp(pos, 1), cxp(pos, 2)
        xl, xy = (kx + rx) / 2 - NW / 2, y + 88
        s.node(xl, xy, 'x', 'new')
        K, R = (kx, y + NH + 4), (rx, y + NH + 4)
        XL, XR = (xl - 3, xy + NH / 2), (xl + NW + 3, xy + NH / 2)
        c12 = 'red' if n == 1 else 'line'
        s.arrow(*XL, *K, c12, off=6, label='①')
        s.arrow(*XR, *R, c12, off=-6, label='②')
        if n >= 2:
            s.arrow(*R, *XR, 'red' if n == 2 else 'line', off=-6, label='③')
        if n == 3:
            s.arrow(*K, *XL, 'red', off=6, label='④')
        if n == 2:
            note(s, endx(pos) + 24, y, '靠 node.next 找到右邻居，所以必须在 ④ 之前', COL['red'])
        y += 168
    lab(s, y, '结果')
    chain(s, DX, y, ['···', 'node', ('x', 'new'), '右邻居', '···'], double=True, gap=G - 71)
    legend(s, DX, y + 62, [('new', '新节点 new_node，值是 x'), ('chg', '红色箭头 = 这一步改的指针')])
    s.save('lcd-dll-add-right')


def lcd_dll_remove():
    s = S()
    DX, G, y = 280, 64, 22
    items = ['···', '左邻居', 'node', '右邻居', '···']
    lab(s, y, '删除前')
    chain(s, DX, y, items, double=True, gap=G)
    y += 108
    lab(s, y, '① 左邻居跳过 node', 'node.prev.next = node.next')
    pos = chain(s, DX, y, items, double=True, links={1: (None, 'line')}, gap=G)
    xa, xc = pos[1][0] + NW - 12, pos[3][0] + 12
    s.curve(xa, y - 3, xc, y - 3, -19, 'red', label='①')
    y += 120
    lab(s, y, '② 右邻居跳过 node', 'node.next.prev = node.prev')
    it = ['···', '左邻居', ('node', 'del'), '右邻居', '···']
    pos = chain(s, DX, y, it, double=True, links={1: (None, 'gry'), 2: ('gry', None)}, gap=G)
    s.curve(xa, y - 3, xc, y - 3, -19, 'line', label='①')
    s.curve(xc, y + NH + 3, xa, y + NH + 3, 19, 'red', label='②')
    note(s, endx(pos) + 24, y, 'node 自己的 prev、next 没动（虚线），所以 ①② 谁先都行')
    y += 112
    lab(s, y, '结果')
    chain(s, DX, y, ['···', '左邻居', '右邻居', '···'], double=True, gap=G)
    s.save('lcd-dll-remove')


def lcd_dll_ends():
    s = S()
    DX, y, RH = 210, 20, 76
    o = 'org'
    rows = [
        ('原链表', ['head', 'a', 'b', 'tail'], {}, ''),
        ('add_right(head, x)', ['head', ('x', 'new'), 'a', 'b', 'tail'], {0: o, 1: o}, '插到最左边：node 是 head，右邻居是 a'),
        ('add_left(tail, x)', ['head', 'a', 'b', ('x', 'new'), 'tail'], {2: o, 3: o}, '插到最右边：等于 add_right(b, x)'),
        ('空链表', ['head', 'tail'], {}, ''),
        ('add_right(head, x)', ['head', ('x', 'new'), 'tail'], {0: o, 1: o}, '空链表不用特判：node 是 head，右邻居是 tail'),
    ]
    NX = DX + 5 * NW + 4 * GAP + 24
    for title, items, links, nt in rows:
        s.text(LX, y + NH / 2, title, 13.5 if '(' in title else 15, INK, 'start', bold=True, mono='(' in title)
        chain(s, DX, y, items, double=True, links=links)
        note(s, NX, y, nt)
        y += RH
    s.save('lcd-dll-ends')


if __name__ == '__main__':
    for f in (lcd_merge, lcd_remove_nth, lcd_reverse, lcd_middle, lcd_cycle, lcd_palindrome,
              lcd_lru_structure, lcd_lru_trace, lcd_basic, lcd_dll_add, lcd_dll_remove, lcd_dll_ends):
        f()
    print('done')
