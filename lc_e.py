#!/usr/bin/env python3
"""Diagrams for the 栈 / 队列 / 单调栈 / 单调队列 sections (LeetCode worked examples).

Run from this directory:  python3 lc_e.py      (writes lce-*.svg and lce-*.png)
Every trace is computed here by running the same algorithm the text shows.
"""
from collections import deque

from make_diagrams import *

T = lambda t, c=INK: ('t', t, c)
DASH = T('—', 'gry')


def brackets():
    s, stk, rows = '{[()]}', [], []
    pair = {')': '(', ']': '[', '}': '{'}
    for c in s:
        if c in pair:
            assert stk and stk[-1] == pair[c]
            before = [(v, 'chg' if i == len(stk) - 1 else 'n') for i, v in enumerate(stk)]
            stk.pop()
            rows.append([T(c), T(f'右括号，要配 {pair[c]}'), before, T('配上了，弹出', 'red'), [(v, 'n') for v in stk] or []])
        else:
            before = [(v, 'n') for v in stk]
            stk.append(c)
            rows.append([T(c), T('左括号'), before, T('入栈，等它的右括号', 'org'),
                         [(v, 'new' if i == len(stk) - 1 else 'n') for i, v in enumerate(stk)]])
    assert not stk
    table('lce-brackets', ['字符', '它是', '读到它时的栈（栈底 → 栈顶）', '做什么', '之后的栈'],
          [70, 170, 280, 210, 170], rows,
          leg=[('new', '新入栈'), ('chg', '栈顶，和右括号配成一对后弹出')],
          foot='s = "{[()]}"  →  最后栈空，返回 True')


def minstack():
    ops = [('push', 5), ('push', 3), ('push', 7), ('push', 2), ('pop',), ('pop',), ('pop',)]
    stk, rows = [], []
    for op in ops:
        if op[0] == 'push':
            x = op[1]
            m = min(x, stk[-1][1]) if stk else x
            stk.append((x, m))
            cs = [(f'{v},{mm}', 'new' if i == len(stk) - 1 else 'n') for i, (v, mm) in enumerate(stk)]
            why = f'min({x}, {stk[-2][1]}) = {m}' if len(stk) > 1 else f'第一个数，最小值就是 {m}'
            rows.append([T(f'push({x})'), cs, T(why), T(str(stk[-1][1]), 'grn')])
        else:
            stk.pop()
            cs = [(f'{v},{mm}', 'hit' if i == len(stk) - 1 else 'n') for i, (v, mm) in enumerate(stk)]
            rows.append([T('pop()'), cs, T('弹掉栈顶，新栈顶自带最小值'), T(str(stk[-1][1]), 'grn')])
    table('lce-minstack', ['操作', '栈（每格是 值,最小值；栈底 → 栈顶）', '这一步', 'get_min()'],
          [110, 330, 290, 90], rows, cw=52,
          leg=[('new', '新入栈'), ('hit', '弹出后的栈顶')],
          foot='每一格的第二个数 = 从栈底到这一格的最小值。get_min() 只读栈顶的第二个数。')


def calc():
    s = '3+5*2-6/4'
    stk, num, op, rows = [], 0, '+', []
    for c in s + '+':
        if c.isdigit():
            num = num * 10 + int(c)
            rows.append([T(c), T(f'数字，num = {num}'), T(op), DASH, [(v, 'n') for v in stk]])
        elif c != ' ':
            if op == '+':
                stk.append(num); act = f'op 是 +：{num} 入栈'
            elif op == '-':
                stk.append(-num); act = f'op 是 -：-{num} 入栈'
            elif op == '*':
                a = stk.pop(); stk.append(a * num); act = f'op 是 *：弹出 {a}，{a} * {num} = {a * num} 入栈'
            else:
                a = stk.pop(); stk.append(int(a / num)); act = f'op 是 /：弹出 {a}，{a} / {num} 取整 = {int(a / num)} 入栈'
            who = '末尾补的 +' if len(rows) == len(s) else c
            rows.append([T(who), T(f'运算符，num = {num} 读完了'), T(op), T(act, 'red'),
                         [(v, 'new' if i == len(stk) - 1 else 'n') for i, v in enumerate(stk)]])
            op, num = c, 0
    assert sum(stk) == 12
    table('lce-calc', ['读到', '它是', 'op（num 前面的运算符）', '按 op 结算 num', '栈（栈底 → 栈顶）'],
          [110, 230, 200, 340, 170], rows, cw=44,
          leg=[('new', '这一步入栈的数')],
          foot=f's = "{s}"  →  栈里是 {stk}，加起来 = {sum(stk)}')


def decode():
    s = '3[a2[c]]'
    stk, cur, num, rows = [], '', 0, []
    show = lambda: [(f'("{p}", {k})', 'n') for p, k in stk]
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c); act = T(f'数字，num = {num}'); cs = show()
        elif c == '[':
            stk.append((cur, num)); act = T(f'进里层：("{cur}", {num}) 入栈，cur 清空', 'org')
            cur, num = '', 0
            cs = show(); cs[-1] = (cs[-1][0], 'new')
        elif c == ']':
            prev, k = stk.pop()
            act = T(f'出里层：弹出 ("{prev}", {k})，cur = "{prev}" + "{cur}" * {k}', 'red')
            cur = prev + cur * k; cs = show()
        else:
            cur += c; act = T('字母，接到 cur 后面'); cs = show()
        rows.append([T(c), act, cs, T(f'"{cur}"', 'grn')])
    assert cur == 'accaccacc'
    table('lce-decode', ['字符', '做什么', '栈：(外层已拼好的, 重复次数)', 'cur（当前这一层）'],
          [70, 430, 280, 160], rows, cw=52,
          leg=[('new', '新入栈：外层的状态')],
          foot=f's = "{s}"  →  "{cur}"')


def two_stacks():
    ops = [('push', 1), ('push', 2), ('push', 3), ('pop',), ('push', 4), ('pop',), ('pop',), ('pop',)]
    inn, out, rows = [], [], []
    for op in ops:
        if op[0] == 'push':
            inn.append(op[1])
            rows.append([T(f'push({op[1]})'), [(v, 'new' if i == len(inn) - 1 else 'n') for i, v in enumerate(inn)],
                         [(v, 'n') for v in out], T('放进 inn'), DASH])
        else:
            moved = not out
            if moved:
                n = len(inn)
                while inn:
                    out.append(inn.pop())
            x = out.pop()
            rows.append([T('pop()'), [(v, 'n') for v in inn], [(v, 'n') for v in out] + [(x, 'chg')],
                         T(f'out 空：inn 的 {n} 个全部倒进 out，再弹' if moved else 'out 不空：直接弹 out 的栈顶',
                           'red' if moved else INK), T(str(x), 'grn')])
    table('lce-two-stacks', ['操作', 'inn（栈底 → 栈顶）', 'out（栈底 → 栈顶）', '这一步', '返回'],
          [110, 200, 200, 350, 60], rows,
          leg=[('new', '新放进 inn'), ('chg', '从 out 的栈顶弹出')],
          foot='倒一次，顺序反过来一次：inn 里最早进来的，到了 out 的栈顶，最先出去。')


def temps():
    a = [73, 74, 75, 71, 69, 72, 76, 73]
    stk, res, rows = [], [0] * len(a), []
    for i, x in enumerate(a):
        before, got = list(stk), []
        while stk and a[stk[-1]] < x:
            j = stk.pop()
            res[j] = i - j
            got.append(f'res[{j}] = {i} - {j} = {i - j}')
        bc = [(f'{j}:{a[j]}', 'n' if j in stk else 'chg') for j in before]
        stk.append(i)
        rows.append([T(f'i = {i}，{x} 度'), bc, T('，'.join(got) or '—', 'red' if got else 'gry'),
                     [(f'{j}:{a[j]}', 'new' if j == i else 'n') for j in stk]])
    rows.append([T('结束'), [(f'{j}:{a[j]}', 'n') for j in stk], T('还在栈里的没等到，保持 0', 'gry'), ''])
    assert res == [1, 1, 4, 2, 1, 1, 0, 0]
    table('lce-temps', ['今天', '进来时的栈（下标:温度）', '被弹出的那些天记答案', '入栈后'],
          [150, 250, 400, 240], rows, cw=58,
          leg=[('chg', '被弹出：今天比它暖，它等到了'), ('new', '新入栈：开始等')],
          foot=f'temperatures = {a}  →  {res}')


U, BW, X0 = 30, 50, 60


def bars(s, hs, base, st='n', top=True):
    for i, v in enumerate(hs):
        f, k, c, d = ST[st]
        x = X0 + i * BW
        if v:
            s.rect(x, base - v * U, BW, v * U, f, k, d, rx=0)
        else:
            s.seg(x, base, x + BW, base, k)
        if top:
            s.text(x + BW / 2, base - v * U - 12, v, 15, INK, bold=True, mono=True)
        s.text(x + BW / 2, base + 14, i, 13, SUB, mono=True)
        if not top:
            s.text(x + BW / 2, base + 38, v, 15, INK, bold=True, mono=True)
    s.text(X0 - 12, base + 14, '下标', 13, SUB, 'end')
    if not top:
        s.text(X0 - 12, base + 38, '高度', 13, SUB, 'end')


def hist():
    hs, s, base = [2, 1, 5, 6, 2, 3], S(), 232
    s.text(18, 16, 'heights = [2, 1, 5, 6, 2, 3]，以下标 2 那根（高 5）为高，能扩多宽', 14.5, INK, 'start', bold=True)
    bars(s, hs, base)
    f, k, _, _ = ST['hit']
    s.rect(X0 + 2 * BW, base - 5 * U, 2 * BW, 5 * U, f, k, rx=0, sw=2.4)
    s.text(X0 + 3 * BW, base - 2.5 * U, '5 × 2 = 10', 16, INK, bold=True)
    for i, t, col in ((1, '左边第一根更矮的', 'red'), (4, '右边第一根更矮的', 'red')):
        ptr(s, X0 + i * BW + BW / 2, base + 24, 'left' if i == 1 else 'i', col)
    tx = X0 + 6 * BW + 50
    s.text(tx, 70, '往左扩：下标 1（高 1）比 5 矮，挡住', 14, COL['red'], 'start', bold=True)
    s.text(tx, 98, '往右扩：下标 3（高 6）不矮，能过；下标 4（高 2）比 5 矮，挡住', 14, COL['red'], 'start', bold=True)
    s.text(tx, 138, '能用的柱子是 left 和 i 之间的那些：下标 2、3', 14, INK, 'start')
    s.text(tx, 166, '宽 = i - left - 1 = 4 - 1 - 1 = 2', 14, INK, 'start', bold=True, mono=True)
    s.text(tx, 194, '面积 = 高 × 宽 = 5 × 2 = 10', 14, COL['grn'], 'start', bold=True)
    s.text(tx, 234, '对每根柱子都这样算一次，取最大的。', 14, INK, 'start')
    s.save('lce-hist')


def hist_trace():
    hs = [2, 1, 5, 6, 2, 3]
    h, stk, best, rows = hs + [0], [], 0, []
    for i, x in enumerate(h):
        before, got = list(stk), []
        while stk and h[stk[-1]] >= x:
            j = stk.pop()
            left = stk[-1] if stk else -1
            area = h[j] * (i - left - 1)
            best = max(best, area)
            ls = f'({left})' if left < 0 else left
            got.append(f'弹 {j}：高 {h[j]}，left = {left}，宽 {i} - {ls} - 1 = {i - left - 1}，面积 {area}')
        bc = [(f'{j}:{h[j]}', 'n' if j in stk else 'chg') for j in before]
        stk.append(i)
        rows.append([T(f'i = {i}，x = {x}' + ('（补的）' if i == len(hs) else '')), bc, got,
                     [(f'{j}:{h[j]}', 'new' if j == i else 'n') for j in stk], T(str(best), 'grn')])
    assert best == 10
    # table() draws one text line per cell, so lay this one out by hand to stack the pops
    s = S()
    heads, widths = ['当前', '进来时的栈（下标:高度）', '弹出时结算（一行一根）', '入栈后', 'best'], [160, 230, 430, 230, 50]
    xs = [18]
    for w in widths[:-1]:
        xs.append(xs[-1] + w)
    right, y = xs[-1] + widths[-1], 14
    for x, t in zip(xs, heads):
        s.text(x, y + 10, t, 13.5, SUB, 'start', bold=True)
    y += 30
    s.seg(18, y, right, y, '#CBD5E1', sw=1.5)
    for r in rows:
        RH = max(54, 24 * len(r[2]) + 22)
        s.text(xs[0], y + RH / 2, r[0][1], 14, INK, 'start', bold=True)
        cells(s, xs[1], y + (RH - 34) / 2, r[1], 46)
        if r[2]:
            for n, t in enumerate(r[2]):
                s.text(xs[2], y + RH / 2 + (n - (len(r[2]) - 1) / 2) * 24, t, 13.5, COL['red'], 'start', bold=True)
        else:
            s.text(xs[2], y + RH / 2, '—', 14, COL['gry'], 'start', bold=True)
        cells(s, xs[3], y + (RH - 34) / 2, r[3], 46)
        s.text(xs[4], y + RH / 2, r[4][1], 14, COL['grn'], 'start', bold=True)
        y += RH
        s.seg(18, y, right, y, '#E5E7EB', sw=1)
    legend(s, 18, y + 16, [('chg', '被弹出：右边界找到了，结算它的面积'), ('new', '新入栈')])
    s.text(18, y + 56, f'heights = {hs}  →  最大面积 {best}', 14, INK, 'start', bold=True)
    s.save('lce-hist-trace')


def rain():
    hs, s, base = [4, 2, 0, 3, 2, 5], S(), 222
    s.text(18, 16, 'height = [4, 2, 0, 3, 2, 5]：水是一层一层横着算的', 14.5, INK, 'start', bold=True)
    bars(s, hs, base, 'sent', top=False)
    stk, water, lines = [], 0, []
    for i, x in enumerate(hs):
        while stk and hs[stk[-1]] < x:
            b = stk.pop()
            if not stk:
                break
            left = stk[-1]
            hh, w = min(hs[left], x) - hs[b], i - left - 1
            water += hh * w
            n = '①②③④⑤⑥'[len(lines)]
            if hh:
                s.rect(X0 + (left + 1) * BW + 2, base - (hs[b] + hh) * U + 2, w * BW - 4, hh * U - 4, '#DBEAFE', COL['blue'], rx=4)
                s.text(X0 + (left + 1) * BW + w * BW / 2, base - (hs[b] + hh / 2) * U, n, 16, COL['blue'], bold=True)
            lines.append(f'{n}  i = {i}：弹出坑底 {b}（高 {hs[b]}），左墙 {left}（高 {hs[left]}），右墙 {i}（高 {x}）'
                         f'  →  高 {hh} × 宽 {w} = {hh * w}')
        stk.append(i)
    assert water == 9
    tx = X0 + 6 * BW + 50
    for n, t in enumerate(lines):
        s.text(tx, 62 + 30 * n, t, 13.5, INK, 'start')
    s.text(tx, 62 + 30 * len(lines) + 10, '高 = min(左墙, 右墙) - 坑底，宽 = i - left - 1', 14, COL['blue'], 'start', bold=True)
    s.text(tx, 62 + 30 * len(lines) + 40, f'合计 {water}', 14, COL['grn'], 'start', bold=True)
    s.save('lce-rain')


def window_max():
    nums, k, q, rows, res = [1, 3, -1, -3, 5, 3, 6, 7], 3, deque(), [], []
    for i, x in enumerate(nums):
        out = []
        if q and q[0] <= i - k:
            out.append(f'队头过期：下标 {q.popleft()}')
        tail = []
        while q and nums[q[-1]] <= x:
            tail.append(str(q.pop()))
        if tail:
            out.append('队尾没用：下标 ' + '、'.join(tail))
        q.append(i)
        full = i >= k - 1
        if full:
            res.append(nums[q[0]])
        win = [(v, ('hit' if full and j == q[0] else 'n') if i - k < j <= i else 'off') for j, v in enumerate(nums)]
        rows.append([T(f'i = {i}'), win, T('；'.join(out) or '—', 'red' if out else 'gry'),
                     [(f'{j}:{nums[j]}', 'new' if j == i else 'n') for j in q],
                     T(str(nums[q[0]]), 'grn') if full else T('窗口没满', 'gry')])
    assert res == [3, 3, 5, 5, 6, 7]
    table('lce-window-max', ['右端', '窗口（蓝色 = 窗口内，绿色 = 最大值）', '弹掉', '队列（下标:值，左 = 队头）', '输出'],
          [80, 380, 330, 260, 80], rows, cw=40,
          leg=[('n', '窗口内'), ('hit', '窗口最大值 = 队头'), ('new', '新入队')],
          foot=f'nums = {nums}，k = 3  →  结果 {res}')


if __name__ == '__main__':
    for f in (brackets, minstack, calc, decode, two_stacks, temps, hist, hist_trace, rain, window_max):
        f()
