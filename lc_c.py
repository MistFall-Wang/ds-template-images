#!/usr/bin/env python3
"""Diagrams for the 双指针 and 区间合并 sections of template 1 (files lcc-*.svg / lcc-*.png).

Run from this directory:  python3 lc_c.py
"""
from make_diagrams import *  # noqa: F401,F403
from make_diagrams_algo import row, marks, lines, bar, BAR

BAR['red'] = '#FEE2E2'
BAR['gry'] = '#F3F4F6'


def harrow(s, x, y, right, col):
    """Short horizontal arrow above a cell: which way the pointer walks."""
    s.arrow(x - 16, y, x + 16, y, col) if right else s.arrow(x + 16, y, x - 16, y, col)


# ---------- 双指针 ----------

def tp_forms():
    s = S()
    X, cw, y = 150, 46, 40
    vals = ['·'] * 7
    T = X + 7 * cw + 30

    def head(t, sub):
        s.text(LX, y + 8, t, 15, INK, 'start', bold=True)
        s.text(LX, y + 30, sub, 12.5, SUB, 'start')

    # 滑动窗口
    head('滑动窗口', '同向')
    cs = row(s, X, y, vals, ['off', 'n', 'n', 'n', 'new', 'off', 'off'], cw=cw)
    marks(s, cs, y + 34, [('left', 1, 'blue'), ('right', 4, 'org')])
    harrow(s, cs[1], y - 12, True, 'blue')
    harrow(s, cs[4], y - 12, True, 'org')
    lines(s, T, y + 6, ['两个指针都从左往右，中间夹着一段「窗口」', '求满足条件的最长 / 最短的连续一段'], gap=22)
    y += 112
    # 相向
    head('相向双指针', '一头一尾')
    cs = row(s, X, y, vals, ['new', 'n', 'n', 'n', 'n', 'n', 'new'], cw=cw)
    marks(s, cs, y + 34, [('left', 0, 'blue'), ('right', 6, 'red')])
    harrow(s, cs[0], y - 12, True, 'blue')
    harrow(s, cs[6], y - 12, False, 'red')
    lines(s, T, y + 6, ['一个从最左往右，一个从最右往左，碰面就结束', '有序数组里找两个数、盛水、接雨水'], gap=22)
    y += 112
    # 快慢
    head('快慢指针', '同向，一读一写')
    cs = row(s, X, y, vals, ['hit', 'hit', 'n', 'n', 'new', 'n', 'n'], cw=cw)
    marks(s, cs, y + 34, [('slow', 2, 'grn'), ('fast', 4, 'org')])
    harrow(s, cs[2], y - 12, True, 'grn')
    harrow(s, cs[4], y - 12, True, 'org')
    lines(s, T, y + 6, ['fast 每个都看一遍，slow 指着「下一个要写的位置」', '原地删除、去重、把 0 挪到最后'], gap=22)
    y += 112
    # 两个数组
    head('两个数组', '各一个指针')
    cs = row(s, X, y, ['·'] * 3, ['n', 'new', 'n'], cw=cw)
    marks(s, cs, y + 34, [('i', 1, 'blue')])
    harrow(s, cs[1], y - 12, True, 'blue')
    cs = row(s, X + 4 * cw, y, ['·'] * 3, ['n', 'new', 'n'], cw=cw)
    marks(s, cs, y + 34, [('j', 1, 'red')])
    harrow(s, cs[1], y - 12, False, 'red')
    lines(s, T, y + 6, ['两个有序数组，各走各的，都不回头', '两个数组里各取一个数凑目标和、合并有序数组'], gap=22)
    s.save('lcc-tp-forms')


def win_compare():
    s = S()
    X, cw = 40, 44

    def step(y, vals, lo, hi, ok, txt):
        row(s, X, y, vals, [('hit' if ok else 'chg') if lo <= j <= hi else 'off' for j in range(len(vals))], cw=cw)
        s.text(X + len(vals) * cw + 22, y + 17, txt, 14, COL['grn'] if ok else COL['red'], 'start', bold=True)

    # 求最长：LC 3，s = "abcbd"，right = 3
    y = 18
    s.text(LX, y, '求最长（LC 3 无重复字符的最长子串，s = "abcbd"，right 走到 3）', 15, INK, 'start', bold=True)
    s.text(LX, y + 24, 'while 窗口不合法：缩。  循环停下时窗口刚变合法  →  在 while 之后更新答案', 13.5, SUB, 'start')
    st, right, left = 'abcbd', 3, 0
    y += 48
    while True:
        w = st[left:right + 1]
        ok = len(set(w)) == len(w)
        step(y, list(st), left, right, ok,
             f'窗口 "{w}" 合法，while 结束  →  更新答案：长度 {len(w)}' if ok else f'窗口 "{w}" 有重复，不合法  →  left 右移，不更新')
        y += 46
        if ok:
            break
        left += 1
    # 求最短：LC 209，target = 7，right = 4
    y += 26
    s.seg(LX, y - 14, 760, y - 14, '#E5E7EB', sw=1)
    s.text(LX, y + 6, '求最短（LC 209 长度最小的子数组，target = 7，right 走到 4）', 15, INK, 'start', bold=True)
    s.text(LX, y + 30, 'while 窗口满足要求：先更新答案，再缩。  循环停下时窗口已经不满足了  →  只能在 while 里面更新', 13.5, SUB, 'start')
    nums, target, right, left = [2, 3, 1, 2, 4, 3], 7, 4, 1
    y += 54
    while True:
        w = nums[left:right + 1]
        ok = sum(w) >= target
        step(y, nums, left, right, ok,
             f'和 {sum(w)} >= 7，满足  →  更新答案：长度 {len(w)}，然后 left 右移' if ok
             else f'和 {sum(w)} < 7，不满足，while 结束  →  不更新')
        y += 46
        if not ok:
            break
        left += 1
    legend(s, LX, y + 8, [('hit', '这个窗口算数，更新答案'), ('chg', '这个窗口不算数'), ('off', '窗口外')])
    s.save('lcc-win-compare')


def win_short():
    nums, target = [2, 3, 1, 2, 4, 3], 7
    s = S()
    X, cw, y = 150, 44, 46
    s.text(LX, 18, 'target = 7：和 >= 7 的最短的一段有多长', 14.5, INK, 'start', bold=True)
    T = X + 6 * cw + 22
    res, total, left = float('inf'), 0, 0

    def draw(right, ok, first, txt):
        if first:
            s.text(LX, y + 17, f'right = {right}', 14, INK, 'start', bold=True, mono=True)
        row(s, X, y, nums, [('hit' if ok else 'n') if left <= j <= right else 'off' for j in range(6)], cw=cw)
        s.text(T, y + 17, txt, 14, COL['grn'] if ok else INK, 'start', bold=ok)

    for right, x in enumerate(nums):
        total += x
        first = True
        while total >= target:
            res = min(res, right - left + 1)
            draw(right, True, first, f'和 {total} >= 7：记下长度 {right - left + 1}（答案 {res}），移出 {nums[left]}')
            total -= nums[left]
            left += 1
            first = False
            y += 44
        draw(right, False, first, f'和 {total} < 7：' + ('不够，right 继续走' if right < 5 else '结束'))
        y += 52
        if right < 5:
            s.seg(LX, y - 9, T + 330, y - 9, '#E5E7EB', sw=1)
    legend(s, LX, y, [('hit', '和够了：更新答案，再缩左边'), ('n', '和不够'), ('off', '窗口外')])
    s.text(LX, y + 44, f'nums = [2, 3, 1, 2, 4, 3]  →  最短长度 {res}（[4, 3]）', 14, INK, 'start', bold=True)
    s.save('lcc-win-short')


def win_fixed():
    nums, k = [1, 12, -5, -6, 50, 3], 4
    s = S()
    X, cw, y = 150, 52, 46
    s.text(LX, 18, 'k = 4：窗口长度固定是 4，每一步进一个、出一个', 14.5, INK, 'start', bold=True)
    total, best = 0, float('-inf')
    for right, x in enumerate(nums):
        total += x
        out = None
        if right >= k:
            out = right - k
            total -= nums[out]
        full = right >= k - 1
        if full:
            best = max(best, total)
        s.text(LX, y + 17, f'right = {right}', 14, INK, 'start', bold=True, mono=True)
        row(s, X, y, [str(v).replace('-', '−') for v in nums],
            ['del' if j == out else 'new' if j == right else 'n' if right - k < j < right else 'off' for j in range(6)], cw=cw)
        t = f'进 {x}' + (f'，出 {nums[out]}' if out is not None else '') + f'，和 = {total}。'
        t += f'窗口满了，最大的和 = {best}' if full else f'窗口还没满 {k} 个，不更新'
        s.text(X + 6 * cw + 22, y + 17, t.replace('-', '−'), 14, INK, 'start', bold=full)
        y += 50
    legend(s, LX, y + 4, [('n', '窗口里'), ('new', '这一步进窗口'), ('del', '这一步出窗口'), ('off', '窗口外')])
    s.text(LX, y + 48, f'最大的和 {best}  →  最大平均数 {best} / {k} = {best / k}', 14, INK, 'start', bold=True)
    s.save('lcc-win-fixed')


def three_sum():
    nums = sorted([-1, 0, 1, 2, -1, -4])
    n = len(nums)
    s = S()
    X, cw, y = 40, 52, 50
    s.text(LX, 18, '排序后 nums = [−4, −1, −1, 0, 1, 2]：固定 i，在它右边用相向双指针找和为 −nums[i] 的两个数', 14.5, INK, 'start',
           bold=True)
    T = X + n * cw + 26
    shown = [str(v).replace('-', '−') for v in nums]

    def draw(i, left, right, found, txt, skip=False):
        nonlocal y
        sts = []
        for j in range(n):
            if j < i:
                sts.append('off')
            elif j == i:
                sts.append('del' if skip else 'pur')
            elif skip:
                sts.append('n')
            elif j in (left, right):
                sts.append('hit' if found else 'new')
            else:
                sts.append('n' if left < j < right else 'off')
        cs = row(s, X, y, shown, sts, cw=cw)
        ps = [('i', i, 'pur')] + ([] if skip else [('left', left, 'blue'), ('right', right, 'red')])
        marks(s, cs, y + 34, ps)
        s.text(T, y + 17, txt.replace('-', '−'), 14, COL['grn'] if found else COL['red'] if skip else INK, 'start',
               bold=found or skip)
        y += 84

    for i in range(n - 2):
        if nums[i] > 0:
            break
        if i > 0 and nums[i] == nums[i - 1]:
            draw(i, 0, 0, False, f'nums[{i}] = {nums[i]} 和前一个一样：跳过，否则会得到重复的三元组', skip=True)
            continue
        left, right = i + 1, n - 1
        while left < right:
            a, b, c = nums[i], nums[left], nums[right]
            tot = a + b + c
            expr = f'{a} + ({b}) + {c} = {tot}' if b < 0 else f'{a} + {b} + {c} = {tot}'
            if tot < 0:
                draw(i, left, right, False, expr + '，太小：left 右移')
                left += 1
            elif tot > 0:
                draw(i, left, right, False, expr + '，太大：right 左移')
                right -= 1
            else:
                draw(i, left, right, True, expr + f'，记下 [{a}, {b}, {c}]，两个指针都往里走')
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
    legend(s, LX, y + 10, [('pur', '固定的第一个数'), ('new', '正在试的两个数'), ('hit', '和为 0'), ('off', '不用看')])
    s.save('lcc-three-sum')


def trap():
    h = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    n, top = len(h), max(h)
    lm = [max(h[:i + 1]) for i in range(n)]
    rm = [max(h[i:]) for i in range(n)]
    water = [min(lm[i], rm[i]) - h[i] for i in range(n)]
    s = S()
    X, U, y0 = 150, 44, 30
    base = y0 + top * U
    for i in range(n):
        for lv in range(top):
            x, y = X + i * U, base - (lv + 1) * U
            if lv < h[i]:
                s.rect(x, y, U - 3, U - 3, '#374151', '#374151', rx=5)
            elif lv < h[i] + water[i]:
                s.rect(x, y, U - 3, U - 3, '#DBEAFE', '#2563EB', rx=5)
    s.text(LX, base - U * 1.5, '黑：柱子', 13.5, INK, 'start', bold=True)
    s.text(LX, base - U * 1.5 + 22, '蓝：接到的水', 13.5, COL['blue'], 'start', bold=True)
    for k, (name, vals, col) in enumerate((('下标', range(n), SUB), ('高度 height', h, INK), ('左边最高', lm, INK),
                                           ('右边最高', rm, INK), ('这一格的水', water, COL['blue']))):
        y = base + 20 + k * 26
        s.text(LX, y, name, 13.5, col, 'start', bold=k > 0)
        for i, v in enumerate(vals):
            s.text(X + i * U + (U - 3) / 2, y, v, 13.5, col, bold=k == 4, mono=True)
    y = base + 20 + 5 * 26 + 8
    lines(s, LX, y, [('每一格的水 = min(左边最高, 右边最高) − 自己的高度　　（左边最高、右边最高都把自己算在内）', INK, True),
                     f'例：下标 5，左边最高 2，右边最高 3，自己高 0  →  min(2, 3) − 0 = 2。全部加起来 = {sum(water)}'], gap=24)
    s.save('lcc-trap')


def fast_slow():
    a = [1, 1, 2, 2, 3]
    s = S()
    X, cw, y = 150, 50, 50
    s.text(LX, 18, 'nums = [1, 1, 2, 2, 3]（已排序）：原地去重。绿色是已经确定留下的部分', 14.5, INK, 'start', bold=True)
    slow = 0
    for fast in range(len(a)):
        keep = fast == 0 or a[fast] != a[fast - 1]
        v, prev = a[fast], a[fast - 1] if fast else None
        if keep:
            a[slow] = a[fast]
            slow += 1
        s.text(LX, y + 17, f'fast = {fast}', 14, INK, 'start', bold=True, mono=True)
        cs = row(s, X, y, a, ['hit' if j < slow else 'new' if j == fast else 'n' for j in range(5)], cw=cw)
        marks(s, cs, y + 34, [('slow', slow, 'grn'), ('fast', fast, 'org')])
        if fast == 0:
            t = f'第一个数 {v} 一定留下：写到 nums[0]，slow 变 1'
        elif keep:
            t = f'{v} 和前一个 {prev} 不同，是新的数：写到 nums[{slow - 1}]，slow 变 {slow}'
        else:
            t = f'{v} 和前一个 {prev} 相同，重复：跳过，slow 不动'
        s.text(X + 5 * cw + 26, y + 17, t, 14, INK if keep else COL['gry'], 'start', bold=keep)
        y += 96
    legend(s, LX, y - 8, [('hit', '留下的（nums[0 .. slow-1]）'), ('new', 'fast 正在看的'), ('n', '其余')])
    s.text(LX, y + 36, f'返回 slow = {slow}，nums 的前 {slow} 个是 {a[:slow]}', 14, INK, 'start', bold=True)
    s.save('lcc-fast-slow')


# ---------- 区间 ----------

X0, U = 150, 38


def px(v):
    return X0 + v * U


def axis(s, ay, hi):
    s.seg(px(0), ay, px(hi), ay, '#94A3B8', sw=1.5)
    for v in range(hi + 1):
        s.seg(px(v), ay - 4, px(v), ay + 4, '#94A3B8', sw=1.2)
        s.text(px(v), ay + 15, v, 11, SUB, mono=True)


def ibar(s, a, b, y, col, dash=False):
    if dash:
        s.rect(px(a), y - 7, px(b) - px(a), 14, '#F9FAFB', COL['gry'], dash=1, rx=7)
    else:
        bar(s, px(a), px(b), y, col)
    s.text((px(a) + px(b)) / 2, y - 19, f'[{a}, {b}]', 13, COL['gry' if dash else col], bold=True, mono=True)


def iv_insert():
    iv, new = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]
    l, r = new
    s = S()
    s.text(LX, 46, '原来的区间', 14, INK, 'start', bold=True)
    kinds = []
    for a, b in iv:
        if b < l:
            kinds.append('blue')
        elif a <= r:
            kinds.append('org')
            l, r = min(l, a), max(r, b)
        else:
            kinds.append('blue')
    for (a, b), c in zip(iv, kinds):
        ibar(s, a, b, 46, c)
    s.text(LX, 98, '新区间', 14, INK, 'start', bold=True)
    ibar(s, new[0], new[1], 98, 'red')
    axis(s, 134, 17)
    s.text(LX, 190, '结果', 14, INK, 'start', bold=True)
    for (a, b), c in zip(iv, kinds):
        if c == 'blue':
            ibar(s, a, b, 190, 'grn')
    ibar(s, l, r, 190, 'grn')
    lines(s, LX, 228, ['① [1, 2]：右端点 2 < 4，完全在新区间左边 → 原样放进结果',
                       (f'② [3, 5]、[6, 7]、[8, 10]：左端点 <= 新区间的右端点，有重叠 → 全部并进新区间，'
                        f'新区间变成 [min, max] = [{l}, {r}]', 'org'),
                       '③ [12, 16]：左端点 12 > 10，完全在右边 → 原样放进结果'], gap=24)
    s.save('lcc-iv-insert')


def iv_why_right():
    iv = [[1, 10], [2, 3], [4, 5]]
    s = S()
    y = 18
    for key, title in ((0, '按左端点排序，能留就留：先留下了 [1, 10]，它很长，把后面两个都挡住了  →  只留下 1 个'),
                       (1, '按右端点排序，能留就留：先留下结束最早的 [2, 3]，后面还有地方放 [4, 5]  →  留下 2 个')):
        s.text(LX, y, title, 14.5, INK, 'start', bold=True)
        end, kept = float('-inf'), []
        for a, b in sorted(iv, key=lambda x: x[key]):
            if a >= end:
                kept.append([a, b])
                end = b
        for k, (a, b) in enumerate(sorted(iv, key=lambda x: x[key])):
            yy = y + 52 + (0 if [a, b] != [1, 10] else 44)
            ibar(s, a, b, yy, 'grn', dash=[a, b] not in kept)
        s.text(LX, y + 52, '短的两个', 13, SUB, 'start')
        s.text(LX, y + 96, '长的一个', 13, SUB, 'start')
        axis(s, y + 126, 11)
        y += 180
    legend(s, LX, y - 14, [('hit', '留下'), ('del', '删掉')])
    s.text(LX, y + 26, '右端点越小，给后面的区间留下的地方越多。所以「选最多个不重叠的区间」按右端点排序。', 14, INK, 'start', bold=True)
    s.save('lcc-iv-why-right')


def iv_arrows():
    pts = sorted([[10, 16], [2, 8], [1, 6], [7, 12]], key=lambda x: x[1])
    s = S()
    s.text(LX, 18, '按右端点排序后的气球。每支箭射在「还没被射到的第一个气球」的右端点', 14.5, INK, 'start', bold=True)
    end, arrows, col = float('-inf'), [], []
    for a, b in pts:
        if a > end:
            end = b
            arrows.append(b)
        col.append(len(arrows) - 1)
    ys = [62, 106, 150, 194]
    for (a, b), y, c in zip(pts, ys, col):
        ibar(s, a, b, y, ('blue', 'org')[c])
    ay = 232
    axis(s, ay, 17)
    for k, x in enumerate(arrows):
        c = ('blue', 'org')[k]
        s.arrow(px(x), ay - 8, px(x), 40, c, dash=1, sw=2.2)
        s.text(px(x), ay + 38, f'第 {k + 1} 支箭 x = {x}', 13.5, COL[c], bold=True)
    lines(s, LX, ay + 72, ['[1, 6]：还没有箭 → 射第 1 支，射在右端点 6', '[2, 8]：左端点 2 <= 6，第 1 支箭已经穿过它 → 不用新箭',
                            '[7, 12]：左端点 7 > 6，够不着 → 射第 2 支，射在 12',
                            '[10, 16]：左端点 10 <= 12，第 2 支箭穿过它 → 不用新箭', (f'一共 {len(arrows)} 支箭', INK, True)],
          gap=23)
    s.save('lcc-iv-arrows')


if __name__ == '__main__':
    for f in (tp_forms, win_compare, win_short, win_fixed, three_sum, trap, fast_slow, iv_insert, iv_why_right,
              iv_arrows):
        f()
    print('ok')
