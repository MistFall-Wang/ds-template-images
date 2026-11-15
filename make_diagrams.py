#!/usr/bin/env python3
"""Generate the diagrams used by 常用代码模板2——数据结构（Python版）.md.

Run:  python3 make_diagrams.py      (writes .svg, and .png if rsvg-convert exists)
"""
import heapq
import math
import os
import shutil
import subprocess
from collections import deque

OUT = os.path.dirname(os.path.abspath(__file__))
FONT = "PingFang SC, Hiragino Sans GB, Microsoft YaHei, Noto Sans CJK SC, Helvetica, Arial, sans-serif"
MONO = "Menlo, Consolas, DejaVu Sans Mono, PingFang SC, monospace"
INK, SUB, LINE = '#1F2937', '#6B7280', '#475569'
COL = {'line': LINE, 'blue': '#2563EB', 'org': '#D97706', 'red': '#DC2626',
       'grn': '#059669', 'gry': '#9CA3AF'}
# style -> (fill, stroke, text colour, dashed)
ST = {
    'n':    ('#E8F0FE', '#2563EB', INK, 0),
    'new':  ('#FEF3C7', '#D97706', INK, 0),
    'del':  ('#F9FAFB', '#9CA3AF', '#9CA3AF', 1),
    'hit':  ('#D1FAE5', '#059669', INK, 0),
    'chg':  ('#FEE2E2', '#DC2626', INK, 0),
    'sent': ('#F3F4F6', '#6B7280', SUB, 0),
    'off':  ('#FFFFFF', '#CBD5E1', '#94A3B8', 0),
    'var':  ('#FFFFFF', '#475569', INK, 1),
}
NW, NH, GAP = 58, 40, 46
LX = 18


def tw(t, size):
    return sum(size if ord(c) > 0x2e7f else size * 0.6 for c in str(t))


def esc(t):
    return str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


class S:
    def __init__(self):
        self.e, self.W, self.H = [], 0, 0

    def b(self, x, y):
        self.W, self.H = max(self.W, x), max(self.H, y)

    def text(self, x, y, t, size=15, color=INK, anchor='middle', bold=False, mono=False):
        w = tw(t, size)
        self.b(x + (w if anchor == 'start' else w / 2 if anchor == 'middle' else 0), y + size * 0.7)
        wt = ' font-weight="700"' if bold else ''
        fam = MONO if mono else FONT
        self.e.append(f'<text x="{x:.1f}" y="{y + size * 0.36:.1f}" font-size="{size}" fill="{color}" '
                      f'text-anchor="{anchor}" font-family="{fam}"{wt}>{esc(t)}</text>')

    def rect(self, x, y, w, h, fill, stroke, dash=0, rx=8, sw=1.8):
        self.b(x + w, y + h)
        d = ' stroke-dasharray="5 4"' if dash else ''
        self.e.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
                      f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def node(self, x, y, t, st='n', w=NW, h=NH, size=16, mono=True):
        f, k, c, d = ST[st]
        self.rect(x, y, w, h, f, k, d)
        self.text(x + w / 2, y + h / 2, t, size, c, bold=True, mono=mono)

    def circ(self, x, y, t, st='n', r=17, size=15):
        f, k, c, d = ST[st]
        self.b(x + r, y + r)
        ds = ' stroke-dasharray="5 4"' if d else ''
        self.e.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{f}" stroke="{k}" stroke-width="1.8"{ds}/>')
        if str(t) != '':
            self.text(x, y, t, size, c, bold=True, mono=True)

    def seg(self, x1, y1, x2, y2, color='line', dash=0, sw=1.8):
        col = COL.get(color, color)
        self.b(max(x1, x2), max(y1, y2))
        d = ' stroke-dasharray="5 4"' if dash else ''
        self.e.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" '
                      f'stroke-width="{sw}" stroke-linecap="round"{d}/>')

    def tip(self, x, y, ang, col, size=10):
        p = [(x, y)] + [(x - size * math.cos(ang + a), y - size * math.sin(ang + a)) for a in (-0.42, 0.42)]
        self.e.append('<polygon points="%s" fill="%s"/>' % (' '.join(f'{a:.1f},{b:.1f}' for a, b in p), col))

    def arrow(self, x1, y1, x2, y2, color='line', dash=0, off=0, sw=1.8, label=None, loff=13, lsize=14):
        col = COL.get(color, color)
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        x1, y1, x2, y2 = x1 + nx * off, y1 + ny * off, x2 + nx * off, y2 + ny * off
        self.seg(x1, y1, x2 - dx / L * 7, y2 - dy / L * 7, col, dash, sw)
        self.tip(x2, y2, math.atan2(dy, dx), col)
        if label:
            if off < 0:
                loff = -loff
            self.text((x1 + x2) / 2 + nx * loff, (y1 + y2) / 2 + ny * loff, label, lsize, col, bold=True)

    def curve(self, x1, y1, x2, y2, bend, color='red', dash=0, label=None):
        """Arc from (x1,y1) to (x2,y2); bend<0 bulges up, bend>0 bulges down."""
        col = COL.get(color, color)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2 + 2 * bend
        ang = math.atan2(y2 - cy, x2 - cx)
        ex, ey = x2 - 7 * math.cos(ang), y2 - 7 * math.sin(ang)
        self.b(max(x1, x2), max(y1, y2, (y1 + y2) / 2 + bend))
        d = ' stroke-dasharray="5 4"' if dash else ''
        self.e.append(f'<path d="M{x1:.1f},{y1:.1f} Q{cx:.1f},{cy:.1f} {ex:.1f},{ey:.1f}" fill="none" '
                      f'stroke="{col}" stroke-width="1.8" stroke-linecap="round"{d}/>')
        self.tip(x2, y2, ang, col)
        if label:
            self.text(cx, (y1 + y2) / 2 + bend + (-11 if bend < 0 else 12), label, 14, col, bold=True)

    def save(self, name, pad=20):
        W, H = math.ceil(self.W + pad), math.ceil(self.H + pad)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
               f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>' + ''.join(self.e) + '</svg>')
        path = os.path.join(OUT, name + '.svg')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(svg)
        if shutil.which('rsvg-convert'):
            subprocess.run(['rsvg-convert', '-z', '2', path, '-o', os.path.join(OUT, name + '.png')], check=True)


# ---------- shared pieces ----------

def lab(s, y, t, subs=(), color=INK):
    """Row label in the left column, with optional code lines under it."""
    if isinstance(subs, str):
        subs = [subs]
    n = len(subs)
    top = y + NH / 2 - 10 * n
    s.text(LX, top, t, 15, color, 'start', bold=True)
    for i, c in enumerate(subs):
        s.text(LX, top + 21 + 19 * i, c, 12.5, SUB, 'start', mono=True)


def note(s, x, y, t, color=SUB):
    s.text(x, y + NH / 2, t, 13.5, color, 'start')


def chain(s, x, y, items, double=False, links=None, gap=GAP):
    """Draw a linked list. items: label or (label, style). links[i] styles the link i -> i+1."""
    links = links or {}
    pos, cx = [], x
    for it in items:
        label, st = it if isinstance(it, tuple) else (it, None)
        if st is None:
            st = ('none' if label == 'None' else 'dots' if label == '···' else
                  'var' if label == 'head' and not double else
                  'sent' if label in ('head', 'tail') else 'n')
        if st == 'none':
            w = 46
            s.text(cx + w / 2, y + NH / 2, 'None', 15, SUB, bold=True, mono=True)
        elif st == 'dots':
            w = 30
            s.text(cx + w / 2, y + NH / 2, '···', 18, SUB)
        else:
            w = NW
            s.node(cx, y, label, st, size=14 if len(label) > 3 else 16)
        pos.append((cx, w))
        cx += w + gap
    for i in range(len(items) - 1):
        sp = links.get(i, 'line')
        x1, x2, ym = pos[i][0] + pos[i][1] + 3, pos[i + 1][0] - 3, y + NH / 2
        if double:
            a, c = sp if isinstance(sp, tuple) else (sp, sp)
            if a:
                s.arrow(x1, ym - 7, x2, ym - 7, a, dash=a == 'gry')
            if c:
                s.arrow(x2, ym + 7, x1, ym + 7, c, dash=c == 'gry')
        elif sp:
            s.arrow(x1, ym, x2, ym, sp, dash=sp == 'gry')
    return pos


def cxp(pos, i):
    return pos[i][0] + pos[i][1] / 2


def endx(pos):
    return pos[-1][0] + pos[-1][1]


def ptr(s, x, y, label, color='blue'):
    """Pointer marker: an up arrow whose tip is at (x, y), label underneath."""
    s.arrow(x, y + 26, x, y + 4, color)
    s.text(x, y + 38, label, 14, COL[color], bold=True, mono=True)


def cells(s, x, y, items, cw=40, ch=34, size=15):
    """Row of touching cells. items: label or (label, style). Returns list of (x, w)."""
    if not items:
        s.text(x, y + ch / 2, '空', 14, COL['gry'], 'start')
        return []
    out = []
    for it in items:
        label, st = it if isinstance(it, tuple) else (it, 'n')
        w = max(cw, tw(label, size) + 16)
        s.node(x, y, label, st, w=w, h=ch, size=size)
        out.append((x, w))
        x += w + 3
    return out


def legend(s, x, y, items):
    for st, t in items:
        f, k, _, d = ST[st]
        s.rect(x, y, 18, 18, f, k, d, rx=4)
        s.text(x + 25, y + 9, t, 13, SUB, 'start')
        x += 25 + tw(t, 13) + 24


def brace(s, x1, x2, y, label, color='org', up=True):
    d = -6 if up else 6
    for a, b, c, e in ((x1, y, x2, y), (x1, y, x1, y - d), (x2, y, x2, y - d)):
        s.seg(a, b, c, e, color)
    s.text((x1 + x2) / 2, y + (-12 if up else 13), label, 13, COL[color], bold=True)


def table(name, heads, widths, rows, cw=40, foot=None, leg=None):
    """A drawn trace table. Cell: str | list of cells | ('t', text, colour)."""
    s = S()
    x0, y, RH = 18, 14, 54
    xs = [x0]
    for w in widths[:-1]:
        xs.append(xs[-1] + w)
    right = xs[-1] + widths[-1]
    for x, h in zip(xs, heads):
        s.text(x, y + 10, h, 13.5, SUB, 'start', bold=True)
    y += 30
    s.seg(x0, y, right, y, '#CBD5E1', sw=1.5)
    for r in rows:
        for x, c in zip(xs, r):
            if isinstance(c, list):
                cells(s, x, y + (RH - 34) / 2, c, cw)
            elif isinstance(c, tuple):
                s.text(x, y + RH / 2, c[1], 14, COL.get(c[2], c[2]), 'start', bold=True)
            else:
                s.text(x, y + RH / 2, c, 14, INK, 'start')
        y += RH
        s.seg(x0, y, right, y, '#E5E7EB', sw=1)
    if leg:
        legend(s, x0, y + 16, leg)
        y += 34
    if foot:
        s.text(x0, y + 22, foot, 14, INK, 'start', bold=True)
    s.save(name)


# ---------- singly linked list ----------

def sll_overview():
    s = S()
    DX, y, RH = 178, 44, 88
    NX = DX + 6 * NW + 5 * GAP + 24
    rows = [
        ('原链表', ['head', 'a', 'b', 'c', 'None'], {}, None, ''),
        ('增 · 头部插入 x', ['head', ('x', 'new'), 'a', 'b', 'c', 'None'], {0: 'org', 1: 'org'}, None, '改 2 根指针'),
        ('增 · b 后面插入 x', ['head', 'a', 'b', ('x', 'new'), 'c', 'None'], {2: 'org', 3: 'org'}, None, '改 2 根指针'),
        ('删 · 删头结点', ['head', ('a', 'del'), 'b', 'c', 'None'], {0: None, 1: 'gry'}, (0, 2), 'head 跳过 a，改 1 根指针'),
        ('删 · 删 b 后面的', ['head', 'a', 'b', ('c', 'del'), 'None'], {2: None, 3: 'gry'}, (2, 4), 'b 跳过 c，改 1 根指针'),
        ('改 · b 改成 y', ['head', 'a', ('y', 'chg'), 'c', 'None'], {}, None, '只换 val，指针不动'),
        ('查 · 找 c', ['head', 'a', 'b', ('c', 'hit'), 'None'], {}, None, 'p 从 head 一步步往后走'),
    ]
    for title, items, links, skip, nt in rows:
        lab(s, y, title)
        pos = chain(s, DX, y, items, links=links)
        if skip:
            i, j = skip
            s.curve(pos[i][0] + pos[i][1] - 12, y - 3, pos[j][0] + 12, y + (2 if items[j] == 'None' else -3), -17, 'red')
        if title.startswith('查'):
            for i, c in ((1, 'gry'), (2, 'gry'), (3, 'grn')):
                ptr(s, cxp(pos, i), y + NH, 'p', c)
        note(s, NX, y, nt)
        y += RH
    s.save('sll-overview')


def ins_single(name, items, ki, c1, c2):
    s = S()
    DX, G, y = 232, 96, 22
    lab(s, y, '插入前')
    chain(s, DX, y, items, gap=G)
    y += 84
    for step in (1, 2):
        lab(s, y + 34, '① 先接后面' if step == 1 else '② 再改前面', c1 if step == 1 else c2,
            )
        pos = chain(s, DX, y, items, links={ki: None} if step == 2 else None, gap=G)
        xl = (pos[ki][0] + pos[ki][1] + pos[ki + 1][0]) / 2 - NW / 2
        xy = y + 74
        s.node(xl, xy, 'x', 'new')
        s.arrow(xl + NW + 3, xy + NH / 2, cxp(pos, ki + 1), y + NH + 4, 'red' if step == 1 else 'line')
        if step == 2:
            s.arrow(cxp(pos, ki), y + NH + 4, xl - 3, xy + NH / 2, 'red')
        y += 150
    lab(s, y, '结果')
    chain(s, DX, y, items[:ki + 1] + [('x', 'new')] + items[ki + 1:], gap=G - 58)
    legend(s, DX, y + 62, [('new', '新节点'), ('chg', '红色箭头 = 这一步改的指针')])
    s.save(name)


def rem_single(name, items, ki, code):
    s = S()
    DX, G, y = 232, 60, 22
    lab(s, y, '删除前')
    chain(s, DX, y, items, gap=G)
    y += 104
    lab(s, y, '跳过它', code)
    it = list(items)
    it[ki + 1] = (it[ki + 1], 'del')
    pos = chain(s, DX, y, it, links={ki: None, ki + 1: 'gry'}, gap=G)
    s.curve(pos[ki][0] + pos[ki][1] - 12, y - 3, pos[ki + 2][0] + 12,
            y + (2 if items[ki + 2] == 'None' else -3), -19, 'red')
    note(s, endx(pos) + 26, y, '没人指向它了，自动回收')
    y += 84
    lab(s, y, '结果')
    chain(s, DX, y, items[:ki + 1] + items[ki + 2:], gap=G)
    s.save(name)


def walk(name, items, steps, double=False, labels=None):
    s = S()
    DX, y, RH = 110, 20, 96
    for n, (idx, nt, st, col) in enumerate(steps):
        lab(s, y, labels[n] if labels else f'第 {n + 1} 步')
        it = list(items)
        if st:
            it[idx] = (it[idx], st)
        pos = chain(s, DX, y, it, double=double)
        ptr(s, cxp(pos, idx), y + NH, 'p', col)
        note(s, endx(pos) + 30, y, nt)
        y += RH
    s.save(name)


def modify(name, double):
    s = S()
    DX, y = 110, 20
    pre = ['head', 'a', 'b', 'c', 'tail' if double else 'None']
    lab(s, y, '修改前')
    pos = chain(s, DX, y, pre, double=double)
    ptr(s, cxp(pos, 2), y + NH, 'k', 'blue')
    y += 104
    lab(s, y, '修改后')
    pre[2] = ('y', 'chg')
    pos = chain(s, DX, y, pre, double=double)
    ptr(s, cxp(pos, 2), y + NH, 'k', 'red')
    note(s, endx(pos) + 30, y, 'k.val = y：只有值变了，指针一根没动')
    s.save(name)


# ---------- doubly linked list ----------

def dll_overview():
    s = S()
    DX, y, RH = 178, 44, 98
    NX = DX + 6 * NW + 5 * GAP + 24
    o = 'org'
    rows = [
        ('原链表', ['head', 'a', 'b', 'c', 'tail'], {}, 'head、tail 是哨兵，不存数据'),
        ('增 · a 右边插 x', ['head', 'a', ('x', 'new'), 'b', 'c', 'tail'], {1: o, 2: o}, '改 4 根指针'),
        ('增 · c 左边插 x', ['head', 'a', 'b', ('x', 'new'), 'c', 'tail'], {2: o, 3: o}, '等于在 b 右边插'),
        ('增 · 头部插 x', ['head', ('x', 'new'), 'a', 'b', 'c', 'tail'], {0: o, 1: o}, '等于 add_right(head, x)'),
        ('增 · 尾部插 x', ['head', 'a', 'b', 'c', ('x', 'new'), 'tail'], {3: o, 4: o}, '等于 add_left(tail, x)'),
        ('删 · 删 b', ['head', 'a', ('b', 'del'), 'c', 'tail'], {1: (None, 'gry'), 2: ('gry', None)}, 'a、c 互相指，改 2 根指针'),
        ('改 · b 改成 y', ['head', 'a', ('y', 'chg'), 'c', 'tail'], {}, '只换 val，指针不动'),
        ('查 · 找 c', ['head', 'a', 'b', ('c', 'hit'), 'tail'], {}, '从 head.next 往右走，到 tail 为止'),
    ]
    for title, items, links, nt in rows:
        lab(s, y, title)
        pos = chain(s, DX, y, items, double=True, links=links)
        if title.startswith('删'):
            xa, xc = pos[1][0] + NW - 12, pos[3][0] + 12
            s.curve(xa, y - 3, xc, y - 3, -17, 'red')
            s.curve(xc, y + NH + 3, xa, y + NH + 3, 17, 'red')
        if title.startswith('查'):
            for i, c in ((1, 'gry'), (2, 'gry'), (3, 'grn')):
                ptr(s, cxp(pos, i), y + NH, 'p', c)
        note(s, NX, y, nt)
        y += RH
    s.save('dll-overview')


def dll_init():
    s = S()
    y = 20
    pos = chain(s, 40, y, ['head', 'tail'], double=True, gap=120)
    s.text(40 + NW + 60, y - 6, 'head.next = tail', 12.5, SUB, mono=True)
    s.text(40 + NW + 60, y + NH + 8, 'tail.prev = head', 12.5, SUB, mono=True)
    note(s, endx(pos) + 30, y, '两个哨兵互相指，中间还没有数据')
    s.save('dll-init')


def dll_add():
    s = S()
    DX, G, y = 250, 124, 22
    items = ['···', 'k', 'r', '···']
    lab(s, y, '插入前')
    chain(s, DX, y, items, double=True, gap=G)
    y += 84
    steps = [('第 1 步：接 x 自己的两根线', ['① node.prev = k', '② node.next = k.next']),
             ('第 2 步：改远的 r', ['③ k.next.prev = node']),
             ('第 3 步：改近的 k', ['④ k.next = node'])]
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
            note(s, endx(pos) + 24, y, '靠 k.next 找到 r，所以必须在 ④ 之前', COL['red'])
        y += 168
    lab(s, y, '结果')
    chain(s, DX, y, ['···', 'k', ('x', 'new'), 'r', '···'], double=True, gap=G - 71)
    legend(s, DX, y + 62, [('new', '新节点'), ('chg', '红色箭头 = 这一步改的指针')])
    s.save('dll-add-right')


def dll_remove():
    s = S()
    DX, G, y = 250, 64, 22
    items = ['···', 'l', 'k', 'r', '···']
    lab(s, y, '删除前')
    chain(s, DX, y, items, double=True, gap=G)
    y += 108
    lab(s, y, '① 左邻居跳过 k', 'k.prev.next = k.next')
    pos = chain(s, DX, y, items, double=True, links={1: (None, 'line')}, gap=G)
    xa, xc = pos[1][0] + NW - 12, pos[3][0] + 12
    s.curve(xa, y - 3, xc, y - 3, -19, 'red', label='①')
    y += 120
    lab(s, y, '② 右邻居跳过 k', 'k.next.prev = k.prev')
    it = ['···', 'l', ('k', 'del'), 'r', '···']
    pos = chain(s, DX, y, it, double=True, links={1: (None, 'gry'), 2: ('gry', None)}, gap=G)
    s.curve(xa, y - 3, xc, y - 3, -19, 'line', label='①')
    s.curve(xc, y + NH + 3, xa, y + NH + 3, 19, 'red', label='②')
    note(s, endx(pos) + 24, y, 'k 自己的 prev、next 没动（虚线），所以 ①② 谁先都行')
    y += 112
    lab(s, y, '结果')
    chain(s, DX, y, ['···', 'l', 'r', '···'], double=True, gap=G)
    s.save('dll-remove')


def dll_ends():
    s = S()
    DX, y, RH = 210, 20, 76
    o = 'org'
    rows = [
        ('原链表', ['head', 'a', 'b', 'tail'], {}, ''),
        ('add_right(head, x)', ['head', ('x', 'new'), 'a', 'b', 'tail'], {0: o, 1: o}, '插到最左边：k = head，r = a'),
        ('add_left(tail, x)', ['head', 'a', 'b', ('x', 'new'), 'tail'], {2: o, 3: o}, '插到最右边：等于 add_right(b, x)'),
        ('空链表', ['head', 'tail'], {}, ''),
        ('add_right(head, x)', ['head', ('x', 'new'), 'tail'], {0: o, 1: o}, '空链表不用特判：k = head，r = tail'),
    ]
    NX = DX + 5 * NW + 4 * GAP + 24
    for title, items, links, nt in rows:
        s.text(LX, y + NH / 2, title, 13.5 if '(' in title else 15, INK, 'start', bold=True, mono='(' in title)
        chain(s, DX, y, items, double=True, links=links)
        note(s, NX, y, nt)
        y += RH
    s.save('dll-ends')


# ---------- stack / queue ----------

def stack_ops():
    s = S()
    ops = [('push 1', [1], 'push', '1 进'), ('push 2', [1, 2], 'push', '2 进'), ('push 3', [1, 2, 3], 'push', '3 进'),
           ('query', [1, 2, 3], 'query', '看栈顶 → 3'), ('pop', [1, 2], 'pop', '3 出', 3),
           ('push 4', [1, 2, 4], 'push', '4 进'), ('pop', [1, 2], 'pop', '4 出', 4)]
    CW, CH, x = 58, 34, 70
    top, bot = 118, 118 + 3 * (CH + 4) + 6
    s.text(18, bot - CH / 2 - 6, '栈底', 13, SUB, 'start')
    s.text(18, top + CH / 2, '栈顶', 13, SUB, 'start')
    for op in ops:
        title, st, kind, cap = op[:4]
        s.text(x + CW / 2, 18, title, 15, INK, bold=True, mono=True)
        for a, b, c, d in ((x - 7, top - 12, x - 7, bot), (x - 7, bot, x + CW + 7, bot), (x + CW + 7, bot, x + CW + 7, top - 12)):
            s.seg(a, b, c, d, LINE, sw=2.2)
        for i, v in enumerate(st):
            cy = bot - 6 - (i + 1) * CH - i * 4
            last = i == len(st) - 1
            s.node(x, cy, v, 'new' if last and kind == 'push' else 'hit' if last and kind == 'query' else 'n', w=CW, h=CH)
        ty = bot - 6 - len(st) * (CH + 4) - 4      # just above the current top
        if kind == 'push':
            s.arrow(x + CW / 2, 40, x + CW / 2, ty + 2, 'org')
        if kind == 'pop':
            s.node(x, 46, op[4], 'del', w=CW, h=CH)
            s.arrow(x + CW / 2, ty, x + CW / 2, 46 + CH + 4, 'red')
        s.text(x + CW / 2, bot + 22, cap, 13.5, SUB)
        x += CW + 50
    s.text(18, bot + 56, '进和出都在上面这一头（栈顶），所以最后进去的最先出来：后进先出。', 14, INK, 'start', bold=True)
    s.save('stack-ops')


def queue_ops():
    s = S()
    ops = [('push 1', [1], 'push', '1 进'), ('push 2', [1, 2], 'push', '2 进'), ('push 3', [1, 2, 3], 'push', '3 进'),
           ('query', [1, 2, 3], 'query', '看队头 → 1，队列不变'), ('pop', [2, 3], 'pop', '最先进的 1 先出', 1),
           ('push 4', [2, 3, 4], 'push', '4 进'), ('pop', [3, 4], 'pop', '2 出', 2)]
    CW, CH, X0, y = 54, 34, 210, 44
    X1 = X0 + 4 * (CW + 4) + 8
    s.text(X0 + 4, 16, '队头（出）', 13, SUB, 'start')
    s.text(X1 - 4, 16, '队尾（进）', 13, SUB, 'end')
    for op in ops:
        title, q, kind, cap = op[:4]
        s.text(LX, y + CH / 2, title, 15, INK, 'start', bold=True, mono=True)
        s.seg(X0 - 4, y - 7, X1, y - 7, LINE, sw=2.2)
        s.seg(X0 - 4, y + CH + 7, X1, y + CH + 7, LINE, sw=2.2)
        for i, v in enumerate(q):
            last, first = i == len(q) - 1, i == 0
            s.node(X0 + 4 + i * (CW + 4), y, v,
                   'new' if last and kind == 'push' else 'hit' if first and kind == 'query' else 'n', w=CW, h=CH)
        if kind == 'push':
            s.arrow(X1 + 44, y + CH / 2, X0 + 4 + len(q) * (CW + 4) + 2, y + CH / 2, 'org')
        if kind == 'pop':
            s.node(X0 - 100, y, op[4], 'del', w=CW, h=CH)
            s.arrow(X0 - 2, y + CH / 2, X0 - 100 + CW + 4, y + CH / 2, 'red')
        s.text(X1 + 62, y + CH / 2, cap, 13.5, SUB, 'start')
        y += 66
    s.text(LX, y + 8, '右边进、左边出，所以最先进去的最先出来：先进先出。', 14, INK, 'start', bold=True)
    s.save('queue-ops')


# ---------- monotonic stack / queue ----------

def mono_why():
    s = S()
    base, U, bw = 196, 36, 48
    for x, v, st in ((60, 3, 'del'), (134, 4, 'del'), (208, 2, 'n')):
        f, k, c, d = ST[st]
        s.rect(x, base - v * U, bw, v * U, f, k, d, rx=6)
        s.text(x + bw / 2, base + 16, v, 16, c if st == 'del' else INK, bold=True, mono=True)
        if st == 'del':
            s.seg(x + 8, base - v * U + 10, x + bw - 8, base - 10, 'red', sw=2)
            s.seg(x + bw - 8, base - v * U + 10, x + 8, base - 10, 'red', sw=2)
    s.node(360, base - 2 * U - 30, '?', 'var', w=bw, h=40)
    s.text(384, base + 16, '以后的数', 13, SUB)
    s.text(232, base + 38, '新来的', 13, COL['blue'], bold=True)
    s.arrow(356, base - 2 * U - 10, 262, base - 2 * U - 10 + 26, 'blue')
    s.text(440, base - 2 * U - 10, '往左找「比我小的」，先碰到 2', 14, COL['blue'], 'start', bold=True)
    s.text(440, base - 2 * U + 18, '2 都不够小，那 3、4 更不够小', 14, INK, 'start')
    s.text(440, base - 2 * U + 46, '所以 2 一进来，3 和 4 就再也用不上了：弹掉', 14, COL['red'], 'start', bold=True)
    s.save('mono-stack-why')


def mono_stack_trace():
    nums, stk, rows = [3, 4, 2, 7, 5], [], []
    for x in nums:
        keep = [v for v in stk if v < x]      # stack is increasing, so the kept part is a prefix
        before = [(v, 'hit' if i == len(keep) - 1 else 'n') for i, v in enumerate(keep)]
        before += [(v, 'chg') for v in stk[len(keep):]]
        ans = keep[-1] if keep else -1
        stk = keep + [x]
        rows.append([('t', f'x = {x}', INK), before, ('t', str(ans), 'grn'), [(v, 'new' if v == x else 'n') for v in stk]])
    table('mono-stack-trace', ['当前的数', '① 弹：进来时的栈（栈底 → 栈顶）', '② 读：答案', '③ 进：入栈后'],
          [110, 300, 120, 200], rows,
          leg=[('chg', '被弹掉（>= x）'), ('hit', '弹完后的栈顶 = 答案'), ('new', '新入栈')],
          foot='nums = [3, 4, 2, 7, 5]  →  结果 [-1, 3, -1, 2, 2]')


def mono_stack_index():
    nums, stk, res, rows = [2, 1, 5, 3], [], [-1] * 4, []
    for i, x in enumerate(nums):
        before, got = list(stk), []
        while stk and nums[stk[-1]] < x:
            j = stk.pop()
            res[j] = i
            got.append(f'res[{j}] = {i}')
        bc = [(f'{j}:{nums[j]}', 'n' if j in stk else 'chg') for j in before]
        stk.append(i)
        rows.append([('t', f'i = {i}，x = {x}', INK), bc, ('t', '，'.join(got) or '—', 'red' if got else 'gry'),
                     [(f'{j}:{nums[j]}', 'new' if j == i else 'n') for j in stk]])
    rows.append([('t', '结束', INK), [(f'{j}:{nums[j]}', 'n') for j in stk], ('t', '还在栈里的保持 -1', 'gry'), ''])
    table('mono-stack-index', ['当前', '进来时的栈（下标:值）', '被弹出时记答案', '入栈后'],
          [140, 250, 240, 200], rows, cw=52,
          leg=[('chg', '被弹出：等到答案了，答案是当前的 i'), ('new', '新入栈：开始等答案')],
          foot=f'nums = [2, 1, 5, 3]  →  res = {res}')


def sliding():
    nums, k, q, rows = [1, 3, -1, -3, 5, 3, 6, 7], 3, deque(), []
    for i, x in enumerate(nums):
        out = []
        if q and q[0] <= i - k:
            out.append(f'队头过期：下标 {q.popleft()}')
        tail = []
        while q and nums[q[-1]] >= x:
            tail.append(str(q.pop()))
        if tail:
            out.append('队尾没用：下标 ' + '、'.join(tail))
        q.append(i)
        full = i >= k - 1
        win = [(v, ('hit' if full and j == q[0] else 'n') if i - k < j <= i else 'off') for j, v in enumerate(nums)]
        rows.append([('t', f'i = {i}', INK), win, ('t', '；'.join(out) or '—', 'red' if out else 'gry'),
                     [(f'{j}:{nums[j]}', 'new' if j == i else 'n') for j in q],
                     ('t', str(nums[q[0]]), 'grn') if full else ('t', '窗口没满', 'gry')])
    table('sliding-window', ['右端', '窗口（蓝色 = 窗口内，绿色 = 最小值）', '弹掉', '队列（下标:值，左 = 队头）', '输出'],
          [80, 380, 290, 260, 80], rows, cw=40,
          leg=[('n', '窗口内'), ('hit', '窗口最小值 = 队头'), ('new', '新入队')],
          foot='nums = [1, 3, -1, -3, 5, 3, 6, 7]，k = 3  →  结果 [-1, -3, -3, -3, 3, 3]')


# ---------- KMP ----------

def kmp_shift():
    s = S()
    X, W, y = 170, 43, 14
    st, p = 'aabaabaaf', 'aabaaf'
    s.text(LX, y + 6, '下标', 13, SUB, 'start')
    for i in range(len(st)):
        s.text(X + i * W + 20, y + 6, i, 13, SUB, mono=True)
    y += 24
    s.text(LX, y + 17, 's', 16, INK, 'start', bold=True, mono=True)
    cells(s, X, y, [(c, 'chg' if i == 5 else 'n') for i, c in enumerate(st)])
    y1 = y + 62
    s.text(LX, y1 + 17, 'p（失配时）', 14, INK, 'start', bold=True)
    cells(s, X, y1, [(c, 'hit' if i < 3 else 'new' if i < 5 else 'chg') for i, c in enumerate(p)])
    s.text(X + 6 * W + 16, y1 + 17, 'j = 5 失配：s[5] 是 b，p[5] 是 f', 13.5, COL['red'], 'start', bold=True)
    y2 = y1 + 84
    s.text(LX, y2 + 17, 'p（j 退到 2）', 14, INK, 'start', bold=True)
    cells(s, X + 3 * W, y2, [(c, 'new' if i < 2 else 'n' if i == 2 else 'off') for i, c in enumerate(p)])
    for i in (3, 4):
        s.seg(X + i * W + 20, y1 + 37, X + i * W + 20, y2 - 3, 'org', dash=1)
    s.text(X + 5 * W + 6, (y1 + 34 + y2) / 2, '结尾的 aa = 开头的 aa，直接对齐，不用重比', 13.5, COL['org'], 'start', bold=True)
    ptr(s, X + 5 * W + 20, y2 + 34, 'j = 2', 'blue')
    s.text(X + 5 * W + 54, y2 + 72, '从这里接着和 s[5] 比；s 的指针 i 没有回退', 13.5, COL['blue'], 'start')
    legend(s, LX, y2 + 104, [('hit', '已匹配'), ('new', '相等的前缀 / 后缀'), ('chg', '失配的位置')])
    s.save('kmp-shift')


def kmp_next():
    s = S()
    X, W, y = 110, 43, 44
    p, nxt = 'aabaaf', [0, 1, 0, 1, 2, 0]
    brace(s, X + 2, X + 2 * W - 5, y - 8, '前缀 aa')
    brace(s, X + 3 * W + 2, X + 5 * W - 5, y - 8, '后缀 aa')
    s.text(LX, y + 17, 'p', 16, INK, 'start', bold=True, mono=True)
    cells(s, X, y, [(c, 'new' if i in (0, 1, 3, 4) else 'n' if i == 2 else 'off') for i, c in enumerate(p)])
    y += 46
    s.text(LX, y + 8, '下标 i', 13, SUB, 'start')
    for i in range(6):
        s.text(X + i * W + 20, y + 8, i, 13, SUB, mono=True)
    y += 30
    s.text(LX, y + 17, 'nxt', 16, INK, 'start', bold=True, mono=True)
    cells(s, X, y, [(v, 'hit' if i == 4 else 'off') for i, v in enumerate(nxt)])
    s.text(X + 6 * W + 24, y - 60, '看 i = 4：只看前 5 个字符 "aabaa"', 14, INK, 'start', bold=True)
    s.text(X + 6 * W + 24, y - 34, '开头的 "aa" 和结尾的 "aa" 一样，最长就是 2', 14, INK, 'start')
    s.text(X + 6 * W + 24, y - 8, '所以 nxt[4] = 2', 14, COL['grn'], 'start', bold=True)
    s.save('kmp-next')


# ---------- trees (trie / union-find / heap) ----------

def tree(s, ox, oy, nodes, edges, r=17, directed=False):
    """nodes: {id: (x, y, label, style)}; edges: (parent, child, label, colour[, dash])."""
    for e in edges:
        a, b, label, col = e[:4]
        dash = e[4] if len(e) > 4 else 0
        ax, ay, bx, by = ox + nodes[a][0], oy + nodes[a][1], ox + nodes[b][0], oy + nodes[b][1]
        L = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / L, (by - ay) / L
        p1, p2 = (ax + ux * (r + 2), ay + uy * (r + 2)), (bx - ux * (r + 2), by - uy * (r + 2))
        sw = 3 if col in ('org', 'red', 'grn') and not directed else 1.8
        if directed:
            s.arrow(*p2, *p1, col or 'line', dash=dash)
        else:
            s.seg(*p1, *p2, col or 'line', dash=dash, sw=sw)
        if label != '':
            side = -13 if bx < ax else 13
            s.text((ax + bx) / 2 + side, (ay + by) / 2 - 2, label, 15, COL.get(col, INK) if col else INK, bold=True, mono=True)
    for x, y, label, st in nodes.values():
        s.circ(ox + x, oy + y, label, st, r=r, size=11 if len(str(label)) > 2 else 15)


TRIE = {'root': (0, 0, 'root', 'sent'), 'a': (-48, 64, '', 'n'), 'b': (48, 64, 1, 'hit'),
        'ab': (-48, 128, '', 'n'), 'abc': (-86, 192, 1, 'hit'), 'abd': (-10, 192, 1, 'hit')}
TRIE_E = [('root', 'a', 'a'), ('a', 'ab', 'b'), ('ab', 'abc', 'c'), ('ab', 'abd', 'd'), ('root', 'b', 'b')]


def trie_insert():
    s = S()
    panels = [('① 插入 "abc"', ['root', 'a', 'ab', 'abc'], ['a', 'ab', 'abc'], ['a、b、c 三条边都没有', '一路新建']),
              ('② 再插入 "abd"', ['root', 'a', 'ab', 'abc', 'abd'], ['abd'], ['a、b 已经有了，直接走过去', '只新建 d']),
              ('③ 再插入 "b"', list(TRIE), ['b'], ['根下面没有 b 这条边', '新建'])]
    ox = 130
    for title, keep, new, cap in panels:
        s.text(ox - 20, 18, title, 15, INK, bold=True)
        nodes = {k: v for k, v in TRIE.items() if k in keep}
        edges = [(a, b, c, 'org' if b in new else None) for a, b, c in TRIE_E if b in keep]
        tree(s, ox, 60, nodes, edges)
        for i, c in enumerate(cap):
            s.text(ox - 20, 288 + i * 22, c, 13.5, SUB)
        ox += 250
    legend(s, 30, 346, [('hit', '有单词在这里结束（数字是 count）'), ('new', '橙色的边 = 这次新建的')])
    s.save('trie-insert')


def trie_tree():
    s = S()
    tree(s, 130, 30, dict(TRIE), [(a, b, c, None) for a, b, c in TRIE_E])
    s.text(250, 60, '字符在边上，从根往下走一条路径就拼出一个字符串', 14, INK, 'start', bold=True)
    s.text(250, 92, '"abc" 和 "abd" 共用了 a → b 这一段', 14, INK, 'start')
    s.text(250, 124, '存了 3 个单词："abc"、"abd"、"b"', 14, SUB, 'start')
    legend(s, 250, 160, [('hit', '有单词在这里结束（数字是 count）')])
    s.save('trie-tree')


def group_by():
    words, g, rows = ['apple', 'bee', 'ant', 'bat'], {}, []
    for w in words:
        isnew = w[0] not in g
        g.setdefault(w[0], []).append(w)
        row = [('t', f'"{w}"', INK), ('t', f'{w[0]} 不存在：自动建 []，再 append' if isnew else f'{w[0]} 已经有了：直接 append',
                                      'org' if isnew else 'gry')]
        for k in 'ab':
            row.append([(k + ':', 'sent')] + [(v, 'new' if v == w else 'n') for v in g[k]] if k in g else '')
        rows.append(row)
    table('group-by', ['当前单词', '发生了什么', 'groups["a"]', 'groups["b"]'], [120, 300, 250, 220], rows, cw=30,
          foot='words = ["apple", "bee", "ant", "bat"]，按首字母分组：groups[w[0]].append(w)')


def trie_query():
    s = S()
    panels = [('查 "abc"', ['a', 'ab', 'abc'], 'abc', None, ['走通，落脚处 count = 1', 'query → 1']),
              ('查 "ab"', ['a', 'ab'], 'ab', None, ['走通，但落脚处 count = 0', 'query → 0，starts_with → True']),
              ('查 "ax"', ['a'], 'a', 'x', ['a 下面没有 x 这条边，走不通', 'query → 0，starts_with → False'])]
    ox = 200
    for title, path, stop, miss, cap in panels:
        s.text(ox - 20, 18, title, 15, INK, bold=True)
        nodes = dict(TRIE)
        edges = [(a, b, c, 'org' if b in path else None) for a, b, c in TRIE_E]
        if miss:
            nodes['x'] = (-112, 128, '✗', 'del')
            edges.append(('a', 'x', 'x', 'red', 1))
        tree(s, ox, 60, nodes, edges)
        if not miss:
            x, y = TRIE[stop][0], TRIE[stop][1]
            s.arrow(ox + x - 52, 60 + y, ox + x - 21, 60 + y, 'blue')
            s.text(ox + x - 56, 60 + y, '停', 13, COL['blue'], 'end', bold=True)
        for i, c in enumerate(cap):
            s.text(ox - 20, 288 + i * 22, c, 13.5, SUB if i == 0 else INK, bold=i == 1)
        ox += 290
    legend(s, 30, 346, [('hit', '有单词在这里结束（数字是 count）'), ('new', '橙色的边 = 走过的路')])
    s.save('trie-query')


def forest(s, ox, oy, parent, hot=None):
    """Draw a union-find forest from a parent array; hot = {child: colour} for highlighted edges."""
    hot = hot or {}
    n = len(parent)
    kids = {i: [j for j in range(n) if parent[j] == i and j != i] for i in range(n)}
    nodes, edges, x = {}, [], [0]

    def place(i, d):
        if not kids[i]:
            px = x[0]
            x[0] += 58
        else:
            cs = [place(c, d + 1) for c in kids[i]]
            px = (cs[0] + cs[-1]) / 2
        nodes[i] = (px, d * 62, i, 'new' if parent[i] == i else 'n')
        return px

    for rt in [i for i in range(n) if parent[i] == i]:
        place(rt, 0)
        x[0] += 26
    for j in range(n):
        if parent[j] != j:
            edges.append((parent[j], j, '', hot.get(j)))
    tree(s, ox, oy, nodes, edges, directed=True)
    return ox + x[0]


def uf_repr():
    s = S()
    par = [0, 0, 1, 3, 3]
    s.text(LX, 22, '下标 x', 13, SUB, 'start')
    for i in range(5):
        s.text(130 + i * 43 + 20, 22, i, 13, SUB, mono=True)
    s.text(LX, 57, 'parent[x]', 14, INK, 'start', bold=True, mono=True)
    cells(s, 130, 40, [(v, 'new' if v == i else 'n') for i, v in enumerate(par)])
    forest(s, 450, 34, par)
    s.text(LX, 112, '箭头 = 指向父节点', 13.5, SUB, 'start')
    s.text(LX, 136, '橙色 = 根（parent[x] == x）', 13.5, COL['org'], 'start', bold=True)
    s.text(LX, 160, '两棵树 = 两个集合：{0, 1, 2} 和 {3, 4}', 13.5, INK, 'start')
    s.save('uf-repr')


def big_arrow(s, x, y, label):
    s.arrow(x, y, x + 74, y, 'line', sw=2.4)
    s.text(x + 34, y - 15, label, 13.5, INK, bold=True, mono=True)


def uf_compress():
    s = S()
    s.text(60, 18, 'find(2) 之前', 14.5, INK, bold=True)
    forest(s, 60, 60, [0, 0, 1])
    big_arrow(s, 150, 122, 'find(2)')
    s.text(320, 18, 'find(2) 之后', 14.5, INK, bold=True)
    forest(s, 290, 60, [0, 0, 0], hot={2: 'red'})
    s.text(410, 110, '2 原来挂在 1 下面，现在直接挂到根 0 下面', 13.5, COL['red'], 'start', bold=True)
    s.text(410, 136, '下次 find(2) 一步就到根', 13.5, SUB, 'start')
    s.save('uf-compress')


def uf_union():
    s = S()
    s.text(110, 18, 'union(2, 4) 之前', 14.5, INK, bold=True)
    forest(s, 60, 60, [0, 0, 1, 3, 3])
    s.text(60, 222, '3 个点', 13, SUB)
    s.text(144, 160, '2 个点', 13, SUB)
    big_arrow(s, 220, 122, 'union(2, 4)')
    s.text(420, 18, 'union(2, 4) 之后', 14.5, INK, bold=True)
    forest(s, 340, 60, [0, 0, 0, 0, 3], hot={2: 'org', 3: 'red'})
    s.text(540, 96, '① find(2) 找到根 0，顺手把 2 挂到 0 下面（路径压缩）', 13.5, COL['org'], 'start', bold=True)
    s.text(540, 124, '② find(4) 找到根 3', 13.5, INK, 'start')
    s.text(540, 152, '③ 右边是小树：小树的根 3 挂到大树的根 0 下面', 13.5, COL['red'], 'start', bold=True)
    s.text(540, 180, '4 跟着 3 一起过来，不用动', 13.5, SUB, 'start')
    s.save('uf-union')


def uf_steps():
    s = S()
    rows = [('初始', [0, 1, 2, 3, 4], {}, '每个点自己是一个集合'),
            ('union(0, 1)', [1, 1, 2, 3, 4], {0: 'red'}, '一样大，0 挂到 1 下面'),
            ('union(1, 2)', [1, 1, 1, 3, 4], {2: 'red'}, '{0, 1} 有 2 个点，{2} 只有 1 个：小的挂大的'),
            ('union(3, 4)', [1, 1, 1, 4, 4], {3: 'red'}, '一样大，3 挂到 4 下面')]
    y = 30
    for title, par, hot, nt in rows:
        s.text(LX, y, title, 14.5, INK, 'start', bold=True, mono='(' in title)
        forest(s, 190, y, par, hot)
        s.text(640, y - 4, f'parent = {par}', 13.5, INK, 'start', mono=True)
        s.text(640, y + 20, f'count = {sum(p == i for i, p in enumerate(par))}', 13.5, INK, 'start', mono=True)
        s.text(640, y + 46, nt, 13.5, SUB, 'start')
        y += 128
    s.save('uf-steps')


def wuf():
    s = S()
    X, y = 180, 20
    lab(s, y, 'find(x) 之前')
    for i, t in enumerate(('x', 'p', 'root')):
        s.node(X + i * 170, y, t, 'new' if t == 'root' else 'n')
    s.arrow(X + NW + 3, y + 20, X + 167, y + 20, 'line', label='d[x] = 2', loff=-14, lsize=13)
    s.arrow(X + 170 + NW + 3, y + 20, X + 337, y + 20, 'line', label='d[p] = 3', loff=-14, lsize=13)
    y += 104
    lab(s, y + 30, 'find(x) 之后')
    s.node(X, y, 'x')
    s.node(X + 170, y + 66, 'p')
    s.node(X + 340, y + 30, 'root', 'new')
    s.arrow(X + NW + 3, y + 22, X + 337, y + 44, 'red', label='d[x] = 2 + 3 = 5', loff=-15, lsize=13)
    s.arrow(X + 170 + NW + 3, y + 84, X + 337, y + 58, 'line', label='d[p] = 3', loff=15, lsize=13)
    note(s, X + 430, y + 30, 'x 直接挂到根上，d[x] 变成到根的距离')
    y += 150
    lab(s, y, 'union(a, b, dist)')
    for i, t in enumerate(('a', 'ra', 'rb', 'b')):
        s.node(X + i * 150, y, t, 'new' if t.startswith('r') else 'n')
    s.arrow(X + NW + 3, y + 20, X + 147, y + 20, 'line')
    s.arrow(X + 150 + NW + 3, y + 20, X + 297, y + 20, 'red', label='d[ra] = dist', loff=-14, lsize=13)
    s.arrow(X + 447, y + 20, X + 300 + NW + 3, y + 20, 'line')
    note(s, X + 530, y, '只在两个根之间连一条线')
    s.save('uf-weighted')


def heap_tree(s, ox, oy, vals, styles=None, hot=None, width=250, idx=False):
    styles, hot = styles or {}, hot or {}
    nodes, edges = {}, []
    for i, v in enumerate(vals):
        d = int(math.log2(i + 1))
        k = i - (2 ** d - 1)
        nodes[i] = (width * (k + 0.5) / 2 ** d, d * 62, v, styles.get(i, 'n'))
        if i:
            edges.append(((i - 1) // 2, i, '', hot.get(i)))
    tree(s, ox, oy, nodes, edges)
    if idx:
        for i, (x, y, _, _) in nodes.items():
            s.text(ox + x + 22, oy + y - 16, f'[{i}]', 12, SUB, 'start', mono=True)
    return nodes


def heap_array():
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
    s.text(X, 160, 'h = [1, 3, 2, 7, 4]', 14, INK, 'start', bold=True, mono=True)
    s.text(X, 190, '每个节点都不大于它的两个孩子，所以堆顶 h[0] 最小', 13.5, SUB, 'start')
    legend(s, X, 214, [('new', '第 1 层'), ('n', '第 2 层'), ('hit', '第 3 层')])
    s.save('heap-array')


def heap_panels(name, panels, title):
    s = S()
    s.text(LX, 18, title, 15, INK, 'start', bold=True)
    ox = 20
    for n, (vals, styles, hot, cap) in enumerate(panels):
        heap_tree(s, ox, 66, vals, styles, hot, width=230)
        for i, c in enumerate(cap):
            s.text(ox + 115, 232 + i * 21, c, 13.5, SUB if i else INK, bold=not i)
        if n < len(panels) - 1:
            s.arrow(ox + 240, 128, ox + 290, 128, 'line', sw=2.4)
        ox += 300
    s.save(name)


def heap_push():
    heap_panels('heap-push', [
        ([1, 3, 2, 7, 4, 0], {5: 'new'}, {}, ['① 先放到最后', '0 在最下面']),
        ([1, 3, 0, 7, 4, 2], {2: 'new'}, {5: 'red'}, ['② 比父节点 2 小，交换', '0 往上走一层']),
        ([0, 3, 1, 7, 4, 2], {0: 'new'}, {2: 'red'}, ['③ 比父节点 1 小，交换', '到堆顶了，停']),
    ], '放进 0：上浮')


def heap_pop():
    heap_panels('heap-pop', [
        ([0, 3, 1, 7, 4, 2], {0: 'del', 5: 'new'}, {}, ['① 堆顶 0 要拿走', '最后一个是 2']),
        ([2, 3, 1, 7, 4], {0: 'new'}, {}, ['② 把最后一个 2 挪到堆顶', '2 比孩子 1 大，不对']),
        ([1, 3, 2, 7, 4], {2: 'new'}, {2: 'red'}, ['③ 和较小的孩子 1 交换', '2 下面没有孩子了，停']),
    ], '取出最小值 0：下沉')


def heap_topk():
    nums, k, h, rows = [4, 1, 7, 3, 8], 2, [], []
    for x in nums:
        heapq.heappush(h, x)
        after = sorted(h)
        kicked = heapq.heappop(h) if len(h) > k else None
        rows.append([('t', f'x = {x}', INK), [(v, 'chg' if v == kicked else 'new' if v == x else 'n') for v in after],
                     ('t', f'超过 {k} 个，踢掉最小的 {kicked}' if kicked is not None else '没超，不踢',
                      'red' if kicked is not None else 'gry'),
                     [(v, 'n') for v in sorted(h)]])
    table('heap-topk', ['新来的数', '放进去之后（最左 = 堆顶 = 最小）', '要不要踢', '堆里剩下'],
          [110, 280, 250, 160], rows,
          leg=[('new', '新放进去的'), ('chg', '被踢掉的')],
          foot='nums = [4, 1, 7, 3, 8]，k = 2  →  最大的 2 个是 [8, 7]')


def heap_sort():
    h = [3, 1, 2]
    heapq.heapify(h)
    rows = [[('t', 'heapify', INK), ('t', '—', 'gry'), [(v, 'hit' if i == 0 else 'n') for i, v in enumerate(sorted(h))]]]
    while h:
        v = heapq.heappop(h)
        rows.append([('t', 'heappop', INK), [(v, 'new')], [(u, 'hit' if i == 0 else 'n') for i, u in enumerate(sorted(h))]])
    table('heap-sort', ['操作', '取出', '堆里剩下（最左 = 堆顶）'], [130, 110, 240], rows,
          foot='nums = [3, 1, 2]  →  取出的顺序 [1, 2, 3]')


def heap_lazy():
    rows = [
        [('t', 'insert(5)', INK), [('(5,1)', 'new')], ('t', '{1: 5}', INK), '第 1 个数是 5'],
        [('t', 'insert(3)', INK), [('(3,2)', 'new'), ('(5,1)', 'n')], ('t', '{1: 5, 2: 3}', INK), '第 2 个数是 3'],
        [('t', 'change(2, 8)', INK), [('(3,2)', 'del'), ('(5,1)', 'n'), ('(8,2)', 'new')], ('t', '{1: 5, 2: 8}', INK),
         '再放一份新的，旧的 (3,2) 不删'],
        [('t', 'top()', INK), [('(3,2)', 'chg'), ('(5,1)', 'hit'), ('(8,2)', 'n')], ('t', '{1: 5, 2: 8}', INK),
         '(3,2) 和 cur[2] = 8 对不上，丢掉；(5,1) 对得上，返回 5'],
    ]
    table('heap-lazy', ['操作', '堆里的 (值, 编号)，最左 = 堆顶', 'cur（编号 → 现在的值）', '说明'],
          [140, 290, 220, 420], rows, cw=58,
          leg=[('del', '已经过期，但还留在堆里'), ('chg', '浮到堆顶时才丢掉'), ('hit', '有效的堆顶')])


def heap_build():
    heap_panels('heap-build', [
        ([5, 3, 8, 1, 2], {1: 'new'}, {}, ['① 从下标 1 开始', '3 比较小的孩子 1 大']),
        ([5, 1, 8, 3, 2], {3: 'new'}, {3: 'red'}, ['② 3 和 1 交换', '下标 1 这棵子树已经是堆']),
        ([1, 5, 8, 3, 2], {1: 'new'}, {1: 'red'}, ['③ 轮到下标 0：5 和 1 交换', '5 还比孩子 2 大，继续']),
        ([1, 2, 8, 3, 5], {4: 'new'}, {4: 'red'}, ['④ 5 和较小的孩子 2 交换', '建好了：[1, 2, 8, 3, 5]']),
    ], '建堆 [5, 3, 8, 1, 2]：从最后一个有孩子的节点开始，倒着下沉')


def heap_median():
    small, large, rows = [], [], []
    for x in [5, 2, 8, 1]:
        heapq.heappush(small, -x)
        heapq.heappush(large, -heapq.heappop(small))
        if len(large) > len(small):
            heapq.heappush(small, -heapq.heappop(large))
        a, b = sorted(-v for v in small), sorted(large)
        med = f'{a[-1]}' if len(a) > len(b) else f'({a[-1]} + {b[0]}) / 2 = {(a[-1] + b[0]) / 2}'
        rows.append([('t', f'加入 {x}', INK), [(v, 'hit' if i == len(a) - 1 else 'n') for i, v in enumerate(a)],
                     [(v, 'hit' if i == 0 else 'n') for i, v in enumerate(b)], ('t', med, 'org')])
    table('heap-median', ['操作', 'small：较小的一半（最大堆）', 'large：较大的一半（最小堆）', '中位数'],
          [120, 270, 270, 200], rows,
          leg=[('hit', '堆顶：small 里最大的，large 里最小的')],
          foot='个数是奇数：small 的堆顶；是偶数：两个堆顶的平均')


# ---------- hash ----------

def hash_buckets():
    s = S()
    s.text(LX, 40, 'd["apple"] = 3', 14.5, INK, 'start', bold=True, mono=True)
    s.node(220, 20, '"apple"', 'n', w=96, size=14)
    s.arrow(319, 40, 366, 40)
    s.node(370, 20, '哈希函数', 'sent', w=104, size=14, mono=False)
    s.text(500, 40, '算出位置 2', 14, COL['org'], 'start', bold=True)
    X, y, W = 110, 126, 124
    s.arrow(422, 63, X + 2 * W + W / 2 - 2, y - 30, 'org')
    s.text(LX, y - 16, '位置', 13, SUB, 'start')
    for i in range(5):
        s.text(X + i * W + W / 2 - 2, y - 16, i, 13, COL['org'] if i == 2 else SUB, bold=i == 2, mono=True)
        s.node(X + i * W, y, 'apple : 3' if i == 2 else '', 'new' if i == 2 else 'off', w=W - 4, h=40, size=14)
    s.text(LX, y + 72, '查 d["apple"]：再算一次位置，还是 2，直接去 2 号拿到 3，不用一个个找。', 14, INK, 'start')
    s.text(LX, y + 98, '改 d["apple"] = 5：算出位置 2，把 2 号里的值换成 5。', 14, INK, 'start')
    s.text(LX, y + 124, '删 del d["apple"]：算出位置 2，把 2 号清空。', 14, INK, 'start')
    s.text(LX, y + 156, '（位置编号是示意，真实的由 Python 内部算）', 12.5, SUB, 'start')
    s.save('hash-buckets')


def set_venn():
    s = S()
    for cx, col in ((170, '#2563EB'), (290, '#D97706')):
        s.e.append(f'<circle cx="{cx}" cy="120" r="95" fill="{col}" fill-opacity="0.14" stroke="{col}" stroke-width="1.8"/>')
    s.b(385, 215)
    s.text(120, 18, 'a = {1, 2, 3}', 14, COL['blue'], bold=True, mono=True)
    s.text(340, 18, 'b = {2, 3, 4}', 14, COL['org'], bold=True, mono=True)
    s.text(115, 120, '1', 20, INK, bold=True, mono=True)
    s.text(230, 104, '2', 20, INK, bold=True, mono=True)
    s.text(230, 138, '3', 20, INK, bold=True, mono=True)
    s.text(345, 120, '4', 20, INK, bold=True, mono=True)
    for i, (code, t) in enumerate((('a & b = {2, 3}', '中间：两边都有'), ('a | b = {1, 2, 3, 4}', '三块全要'),
                                   ('a - b = {1}', '左边：只在 a 里'))):
        s.text(430, 76 + i * 44, code, 14.5, INK, 'start', bold=True, mono=True)
        s.text(430, 96 + i * 44, t, 13, SUB, 'start')
    s.save('set-venn')


def two_sum():
    nums, target, index_of, rows = [3, 2, 7, 15], 9, {}, []
    for i, x in enumerate(nums):
        need = target - x
        have = [(f'{k}→{v}', 'hit' if k == need else 'n') for k, v in index_of.items()]
        if need in index_of:
            rows.append([('t', f'i = {i}，x = {x}', INK), ('t', f'9 - {x} = {need}', INK), have,
                         ('t', f'有 {need}，下标 {index_of[need]}  →  返回 [{index_of[need]}, {i}]', 'grn')])
            break
        rows.append([('t', f'i = {i}，x = {x}', INK), ('t', f'9 - {x} = {need}', INK), have,
                     ('t', f'没有 {need}，把 {x}→{i} 存进去', 'gry')])
        index_of[x] = i
    table('two-sum', ['当前', '要找的数', 'index_of 里已有的（值→下标）', '结果'], [150, 130, 250, 300], rows, cw=52,
          foot='nums = [3, 2, 7, 15]，target = 9  →  [1, 2]')


def strhash():
    s = S()
    X, W, y = 110, 49, 14
    s.text(LX, y + 6, '下标', 13, SUB, 'start')
    for i in range(6):
        s.text(X + i * W + 23, y + 6, i, 13, SUB, mono=True)
    y += 24
    s.text(LX, y + 19, 's', 16, INK, 'start', bold=True, mono=True)
    cells(s, X, y, [(c, 'chg' if i < 3 else 'hit') for i, c in enumerate('abcabc')], cw=46, ch=38)
    y += 54
    brace(s, X + 2, X + 6 * W - 5, y, 'h[6]：前 6 个字符 "abcabc"', 'blue', up=False)
    y += 42
    brace(s, X + 2, X + 3 * W - 5, y, 'h[3]：要去掉的', 'red', up=False)
    brace(s, X + 3 * W + 2, X + 6 * W - 5, y, 'get(3, 5)：要的', 'grn', up=False)
    s.text(X + 6 * W + 40, 60, 'get(3, 5) = h[6] - h[3] × P³', 15, INK, 'start', bold=True, mono=True)
    s.text(X + 6 * W + 40, 90, 'h[3] 乘 P³：左移 3 位，和 h[6] 的高位对齐', 13.5, SUB, 'start')
    s.text(X + 6 * W + 40, 114, '一减，前面的 "abc" 抵消，只剩后面这段', 13.5, SUB, 'start')
    s.save('strhash')


if __name__ == '__main__':
    sll_overview()
    ins_single('sll-add-head', ['head', 'a', 'b', 'None'], 0, 'node.next = head', 'head = node')
    ins_single('sll-add-after', ['···', 'k', 'r', '···'], 1, 'node.next = k.next', 'k.next = node')
    rem_single('sll-remove-after', ['···', 'k', 'd', 'r', '···'], 1, 'k.next = k.next.next')
    rem_single('sll-remove-head', ['head', 'a', 'b', 'None'], 0, 'head = head.next')
    walk('sll-traverse', ['head', 'a', 'b', 'c', 'None'],
         [(1, 'p = head，输出 a', None, 'blue'), (2, 'p = p.next，输出 b', None, 'blue'),
          (3, 'p = p.next，输出 c', None, 'blue'), (4, 'p 是 None，结束', None, 'red')])
    walk('sll-find', ['head', 'a', 'b', 'c', 'None'],
         [(1, 'a != c，往后走', None, 'blue'), (2, 'b != c，往后走', None, 'blue'), (3, 'c == c，找到，返回 p', 'hit', 'grn')])
    walk('sll-get', ['head', 'a', 'b', 'c', 'None'],
         [(1, 'p = head，这是第 0 个', None, 'blue'), (2, 'p = p.next，第 1 个', None, 'blue'),
          (3, 'p = p.next，第 2 个，返回 p', 'hit', 'grn')], labels=['起点', '走 1 步', '走 2 步'])
    modify('sll-modify', False)
    trie_tree()
    group_by()
    dll_overview()
    dll_init()
    dll_add()
    dll_remove()
    dll_ends()
    walk('dll-traverse', ['head', 'a', 'b', 'c', 'tail'],
         [(1, 'p = head.next，输出 a', None, 'blue'), (2, 'p = p.next，输出 b', None, 'blue'),
          (3, 'p = p.next，输出 c', None, 'blue'), (4, 'p 是 tail，结束', None, 'red')], double=True)
    walk('dll-find', ['head', 'a', 'b', 'c', 'tail'],
         [(1, 'a != b，往右走', None, 'blue'), (2, 'b == b，找到，返回 p', 'hit', 'grn')], double=True)
    modify('dll-modify', True)
    stack_ops()
    queue_ops()
    mono_why()
    mono_stack_trace()
    mono_stack_index()
    sliding()
    kmp_shift()
    kmp_next()
    trie_insert()
    trie_query()
    uf_repr()
    uf_compress()
    uf_union()
    uf_steps()
    wuf()
    heap_array()
    heap_push()
    heap_pop()
    heap_topk()
    heap_sort()
    heap_lazy()
    heap_build()
    heap_median()
    hash_buckets()
    set_venn()
    two_sum()
    strhash()
    print('ok')
