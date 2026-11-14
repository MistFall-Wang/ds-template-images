#!/usr/bin/env python3
"""Diagrams for the LeetCode parts of 二分 / 快速排序 / 归并排序 (files lca-*.svg / lca-*.png).

Run from this directory:  python3 lc_a.py
"""
from make_diagrams import *  # noqa: F401,F403
from make_diagrams_algo import row, marks, lines


# ---------- 二分 ----------

def bs_range():
    s = S()
    nums = [5, 7, 7, 8, 8, 10]
    s.text(LX, 18, 'LC 34：nums = [5, 7, 7, 8, 8, 10]，target = 8', 14.5, INK, 'start', bold=True)
    cw = 150
    cs = row(s, 30, 58, nums, ['hit' if v == 8 else 'n' for v in nums], cw=cw, idx='top')
    for i, (a, b, col) in {3: ('start = 3', 'lower_bound(8) = 3', 'grn'), 4: ('end = 5 − 1 = 4', 'lower_bound(9) - 1', 'org'),
                           5: ('第一个 >= 9', 'lower_bound(9) = 5', 'blue')}.items():
        s.arrow(cs[i], 118, cs[i], 97, col)
        s.text(cs[i], 130, a, 14, COL[col], bold=True)
        s.text(cs[i], 150, b, 12, SUB, mono=True)
    s.save('lca-bs-range')


def bs_rotate():
    s = S()
    nums = [4, 5, 6, 7, 0, 1, 2]
    X, y, cw = 190, 62, 52
    s.text(LX, y + 17, 'nums', 15, INK, 'start', bold=True, mono=True)
    ok = [v <= nums[-1] for v in nums]
    cs = row(s, X, y, nums, ['hit' if o else 'sent' for o in ok], cw=cw, idx='top')
    brace(s, cs[0] - 22, cs[3] + 22, y - 26, '前一段：都比 nums[-1] 大', 'gry')
    brace(s, cs[4] - 22, cs[6] + 22, y - 26, '后一段：都 <= nums[-1]', 'grn')
    s.text(LX, y + 56, 'nums[i] <= 2 吗？', 14, SUB, 'start')
    for o, c in zip(ok, cs):
        s.text(c, y + 56, '是' if o else '否', 15, COL['grn' if o else 'gry'], bold=True)
    ptr(s, cs[4], y + 68, '第一个「是」= 最小值的位置', 'grn')
    lines(s, X + 7 * cw + 24, y - 4, [('nums[-1] = 2', INK), '整个数组不是有序的，', '但「nums[i] <= nums[-1] 吗」', '仍然是前面全否、后面全是'], gap=23)
    s.save('lca-bs-rotate')


def bs_rotate_trace():
    nums = [4, 5, 6, 7, 0, 1, 2]
    n = len(nums)
    left, right = 0, n - 1
    s = S()
    X, y = 40, 30
    while True:
        done = left > right
        mid = None if done else (left + right) // 2
        sts = ['sent' if j < left else 'hit' if j > right else 'n' for j in range(n)]
        if mid is not None:
            sts[mid] = 'new'
        cs = row(s, X, y, nums, sts, cw=52, idx='top')
        ps = [('left', left, 'blue')] + ([('right', right, 'red')] if right >= 0 else []) + ([] if done else [('mid', mid, 'org')])
        marks(s, cs, y + 34, ps)
        tx = X + n * 52 + 28
        if done:
            s.text(tx, y + 17, f'left 超过 right，结束：返回 left = {left}，nums[{left}] = {nums[left]} 是最小值', 14, COL['grn'], 'start', bold=True)
            break
        if nums[mid] <= nums[-1]:
            s.text(tx, y + 17, f'nums[{mid}] = {nums[mid]} <= 2：是，right = mid − 1 = {mid - 1}', 14, INK, 'start', bold=True)
            right = mid - 1
        else:
            s.text(tx, y + 17, f'nums[{mid}] = {nums[mid]} > 2：否，left = mid + 1 = {mid + 1}', 14, INK, 'start', bold=True)
            left = mid + 1
        y += 152
    legend(s, LX, y + 104, [('sent', '已确定「否」（在前一段）'), ('hit', '已确定「是」（在后一段）'), ('n', '还没确定'), ('new', 'mid')])
    s.save('lca-bs-rotate-trace')


def bs_koko():
    s = S()
    piles, h = [3, 6, 7, 11], 8
    X, y, cw = 170, 50, 50
    s.text(LX, 18, 'LC 875：piles = [3, 6, 7, 11]，h = 8。check(k) = 用速度 k 吃完要的小时数 <= 8', 14.5, INK, 'start', bold=True)
    ks = list(range(1, max(piles) + 1))
    hrs = [sum((p + k - 1) // k for p in piles) for k in ks]
    s.text(LX, y + 17, '速度 k', 15, INK, 'start', bold=True)
    cs = row(s, X, y, ks, ['hit' if t <= h else 'sent' for t in hrs], cw=cw)
    s.text(LX, y + 54, '要几小时', 14, SUB, 'start')
    s.text(LX, y + 80, 'check(k)', 14, SUB, 'start', mono=True)
    for t, c in zip(hrs, cs):
        s.text(c, y + 54, t, 13, SUB, mono=True)
        s.text(c, y + 80, '是' if t <= h else '否', 15, COL['grn' if t <= h else 'gry'], bold=True)
    first = next(i for i, t in enumerate(hrs) if t <= h)
    s.arrow(cs[first], y + 118, cs[first], y + 96, 'grn')
    s.text(cs[first] - 8, y + 130, f'第一个「是」：答案 k = {ks[first]}', 13.5, COL['grn'], 'start', bold=True)
    s.text(cs[0] - 20, y + 130, '吃得越快，用时越少', 13.5, SUB, 'start')
    s.save('lca-bs-koko')


def bs_matrix():
    s = S()
    M = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    m, n = 3, 4
    cw, X, y = 56, 60, 66
    s.text(LX, 16, 'matrix（3 行 4 列），每格右下角是编号 k', 14.5, INK, 'start', bold=True)
    sty = ['n', 'new', 'pur' if 'pur' in ST else 'hit']
    for i in range(m):
        s.text(X - 22, y + i * 46 + 19, f'行 {i}', 12.5, SUB, 'end')
        for j in range(n):
            x = X + j * cw
            s.node(x, y + i * 46, M[i][j], sty[i], w=cw - 3, h=40, size=15)
            s.text(x + cw - 9, y + i * 46 + 32, i * n + j, 10, SUB, 'end', mono=True)
    for j in range(n):
        s.text(X + j * cw + (cw - 3) / 2, y - 12, f'列 {j}', 12.5, SUB)
    X2 = X + n * cw + 70
    s.arrow(X + n * cw + 12, y + 66, X2 - 14, y + 66, 'gry')
    s.text(X2, 16, '一行接一行摆平：就是一个有序数组', 14.5, INK, 'start', bold=True)
    flat = [v for r in M for v in r]
    cs = row(s, X2, y + 46, flat, [sty[k // n] for k in range(m * n)], cw=46, idx='top')
    s.text(X2 - 10, y + 46 - 11, 'k', 12, SUB, 'end', mono=True)
    k = 6
    ptr(s, cs[k], y + 46 + 36, 'k = 6  →  行 6 // 4 = 1，列 6 % 4 = 2  →  matrix[1][2] = 16', 'org')
    s.save('lca-bs-matrix')


# ---------- 快速排序 ----------

def partition_states(a, l, r, x, st=None):
    lt, i, gt = l, l, r
    while i <= gt:
        if a[i] < x:
            a[lt], a[i] = a[i], a[lt]
            lt, i = lt + 1, i + 1
        elif a[i] > x:
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
        else:
            i += 1
    return lt, gt


def qs_select_trace():
    a, k = [3, 2, 1, 5, 6, 4], 2
    t = len(a) - k
    pivots = [3, 5]                                     # 假设随机挑到的基准
    l, r = 0, len(a) - 1
    s = S()
    X, y, cw = 440, 62, 50
    s.text(LX, 16, f'LC 215：nums = {a}，k = 2  →  排好序后第 2 大在下标 t = 6 − 2 = {t}', 14.5, INK, 'start', bold=True)
    s.text(LX, y + 17, '开始：整段 [0, 5] 都要找', 14, INK, 'start', bold=True)
    cs = row(s, X, y, a, 'off', cw=cw, idx='top')
    marks(s, cs, y + 34, [('t', t, 'red')])
    y += 100
    for rd, x in enumerate(pivots, 1):
        assert x in a[l:r + 1]
        lt, gt = partition_states(a, l, r, x)
        sts = ['del' if j < l or j > r else 'n' if j < lt else 'hit' if j <= gt else 'new' for j in range(len(a))]
        s.text(LX, y + 8, f'第 {rd} 轮：在 [{l}, {r}] 里挑到基准 x = {x}', 14, INK, 'start', bold=True)
        if t < lt:
            d, col = f't = {t} 在左段 → 只留 [{l}, {lt - 1}]', 'blue'
        elif t > gt:
            d, col = f't = {t} 在右段 → 只留 [{gt + 1}, {r}]', 'org'
        else:
            d, col = f't = {t} 在中段 → 答案就是 x = {x}', 'grn'
        s.text(LX, y + 30, f'分完：lt = {lt}，gt = {gt}。{d}', 13.5, COL[col], 'start', bold=True)
        cs = row(s, X, y, a, sts, cw=cw)
        marks(s, cs, y + 34, [('t', t, 'red')])
        if t < lt:
            r = lt - 1
        elif t > gt:
            l = gt + 1
        else:
            break
        y += 92
    legend(s, LX, y + 88, [('n', '比 x 小'), ('hit', '等于 x'), ('new', '比 x 大'), ('del', '已经扔掉，不再看')])
    s.save('lca-qs-select-trace')


def qs_colors():
    a = [2, 0, 2, 1, 1, 0]
    n = len(a)
    lt, i, gt = 0, 0, n - 1
    states = [('开始', a[:], lt, i, gt)]
    while i <= gt:
        v = a[i]
        if v == 0:
            d = f'看 0：和下标 {lt} 交换，lt、i 右移'
            a[lt], a[i] = a[i], a[lt]
            lt, i = lt + 1, i + 1
        elif v == 2:
            d = f'看 2：和下标 {gt} 交换，gt 左移，i 不动'
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
        else:
            d = '看 1：留在中间，i 右移'
            i += 1
        states.append((d, a[:], lt, i, gt))
    s = S()
    for k, (d, arr, lt, i, gt) in enumerate(states):
        ox, y = LX, 16 + k * 104
        s.text(ox, y + 17, d, 14, INK, 'start', bold=True)
        cs = row(s, ox + 330, y, arr, ['n' if j < lt else 'hit' if j < i else 'off' if j <= gt else 'new' for j in range(n)], cw=46)
        ps = [('lt', lt, 'blue')] + ([('i', i, 'org')] if i < n else []) + ([('gt', gt, 'red')] if gt >= 0 else [])
        marks(s, cs, y + 34, ps)
    y = 16 + len(states) * 104
    legend(s, LX, y, [('n', '0（红）'), ('hit', '1（白）'), ('off', '还没看'), ('new', '2（蓝）')])
    s.text(LX, y + 44, f'i 超过 gt，停。结果 {states[-1][1]}', 14, INK, 'start', bold=True)
    s.save('lca-qs-colors')
    return states


# ---------- 归并排序 ----------

def ms_88():
    nums1, m, nums2, n = [1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3
    i, j, k = m - 1, n - 1, m + n - 1
    s = S()
    X1, X2, y = 400, 760, 44
    s.text(X1, 16, 'nums1', 14, SUB, 'start', bold=True, mono=True)
    s.text(X2, 16, 'nums2', 14, SUB, 'start', bold=True, mono=True)
    done1, done2 = set(), set()

    def draw(d):
        nonlocal y
        s.text(LX, y + 17, d, 14, INK, 'start', bold=True)
        st1 = ['hit' if q in done1 else 'n' if q <= i else 'off' for q in range(m + n)]
        c1 = row(s, X1, y, [v if (q in done1 or q <= i) else '' for q, v in enumerate(nums1)], st1, cw=46)
        ps = ([('i', i, 'blue')] if i >= 0 else [])
        if k >= 0:
            ps.append(('k', k, 'grn'))
        marks(s, c1, y + 34, ps)
        c2 = row(s, X2, y, nums2, ['off' if q > j else 'n' for q in range(n)], cw=46)
        if j >= 0:
            marks(s, c2, y + 34, [('j', j, 'org')])
        y += 100

    draw('开始：i、j 指着两边最后一个数，k 指着最后一格')
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            d = f'{nums1[i]} 和 {nums2[j]} 比：{nums1[i]} 大，放到下标 {k}，i 左移'
            nums1[k] = nums1[i]
            i -= 1
        else:
            d = (f'{nums1[i]} 和 {nums2[j]} 比：' if i >= 0 else 'nums1 拿完了：') + f'拿 nums2 的 {nums2[j]}，放到下标 {k}，j 左移'
            nums1[k] = nums2[j]
            j -= 1
        done1.add(k)
        k -= 1
        draw(d)
    y -= 10
    legend(s, LX, y, [('n', '还没拿的'), ('hit', '已经放好的'), ('off', '空位 / 已经拿走')])
    s.text(LX, y + 44, f'j < 0：nums2 全放完了，停。nums1 里剩下的 [1, 2] 本来就在正确的位置。结果 {nums1}', 14, INK, 'start', bold=True)
    s.save('lca-ms-88')


def ms_list():
    s = S()
    Y = [16, 86, 156, 226, 296]
    N = {'r': (330, 0, '4 → 2 → 1 → 3', 'n'), 'a': (190, 1, '4 → 2', 'n'), 'b': (470, 1, '1 → 3', 'n'),
         'a1': (120, 2, '4', 'sent'), 'a2': (260, 2, '2', 'sent'), 'b1': (400, 2, '1', 'sent'),
         'b2': (540, 2, '3', 'sent'), 'ma': (190, 3, '2 → 4', 'hit'), 'mb': (470, 3, '1 → 3', 'hit'),
         'm': (330, 4, '1 → 2 → 3 → 4', 'hit')}
    E = [('r', 'a', 'blue'), ('r', 'b', 'blue'), ('a', 'a1', 'blue'), ('a', 'a2', 'blue'), ('b', 'b1', 'blue'),
         ('b', 'b2', 'blue'), ('a1', 'ma', 'grn'), ('a2', 'ma', 'grn'), ('b1', 'mb', 'grn'), ('b2', 'mb', 'grn'),
         ('ma', 'm', 'grn'), ('mb', 'm', 'grn')]
    for a, b, c in E:
        s.arrow(N[a][0], Y[N[a][1]] + 37, N[b][0], Y[N[b][1]] - 4, c)
    for cx, lv, t, st in N.values():
        w = max(tw(t, 15) + 22, 44)
        s.node(cx - w / 2, Y[lv], t, st, w=w, h=34, size=15)
    s.text(640, Y[0] + 17, '快慢指针找到中点 2，slow.next = None 断开', 13.5, SUB, 'start')
    s.text(640, Y[1] - 18, '往下：从中点断成两条链表', 14.5, COL['blue'], 'start', bold=True)
    s.text(640, Y[2] + 17, '只剩 1 个节点：本身就有序，直接返回', 13.5, SUB, 'start')
    s.text(640, Y[3] + 52, '往上：merge_two_lists 合并两条有序链表', 14.5, COL['grn'], 'start', bold=True)
    s.save('lca-ms-list')


def ms_inv_trace():
    log = []

    def sort(a):
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, c1 = sort(a[:mid])
        right, c2 = sort(a[mid:])
        cnt, res, i, j, parts = 0, [], 0, 0, []
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                res.append(left[i])
                i += 1
            else:
                res.append(right[j])
                parts.append((right[j], len(left) - i))
                j += 1
                cnt += len(left) - i
        res += left[i:] + right[j:]
        log.append((left, right, parts, cnt, res))
        return res, c1 + c2 + cnt

    nums = [9, 7, 5, 4, 6]
    total = sort(nums)[1]
    rows = []
    for left, right, parts, cnt, res in log:
        how = '；'.join(f'拿 {v}：左边还剩 {c} 个' for v, c in parts) or '右边的数是在左边拿完之后才接上的'
        rows.append([[(v, 'chg') for v in left], [(v, 'new') for v in right], how, ('t', f'+{cnt}', 'red'),
                     [(v, 'hit') for v in res]])
    table('lca-ms-inv-trace', ['left', 'right', '每次拿右边的数时', '新增', '合并后'], [150, 150, 440, 70, 240], rows,
          foot=f'nums = {nums}：' + ' + '.join(str(r[3]) for r in log) + f' = {total} 个逆序对')
    return log, total


if __name__ == '__main__':
    bs_range()
    bs_rotate()
    bs_rotate_trace()
    bs_koko()
    bs_matrix()
    qs_select_trace()
    print(qs_colors())
    ms_88()
    ms_list()
    print(ms_inv_trace())
    print('ok')
