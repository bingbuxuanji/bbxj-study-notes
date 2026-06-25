import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

t = np.linspace(-4, 4, 2000)
dt = t[1] - t[0]

# === 信号定义 ===
f1 = np.where((t >= -1) & (t < 1), 1.0, 0.0)  # 矩形 [-1, 1]
f2 = np.zeros_like(t)
f2[np.argmin(np.abs(t - (-1)))] = 1.0 / dt
f2[np.argmin(np.abs(t - 1))] = 1.0 / dt

# ==================== 四列图：滑动过程 ====================
fig, axes = plt.subplots(2, 4, figsize=(18, 8))

# 共享设置
for ax in axes.flat:
    ax.set_xlim(-4, 4)
    ax.set_ylim(-0.5, 1.8)
    ax.axhline(y=0, color='gray', linewidth=0.5)
    ax.axvline(x=0, color='gray', linewidth=0.3)
    ax.grid(True, alpha=0.2)

# --- Step 0: 两个原始信号 ---
ax = axes[0, 0]
ax.plot(t, f1, 'b', linewidth=2)
ax.fill_between(t, 0, f1, alpha=0.1, color='b')
ax.stem([-1, 1], [1, 1], linefmt='r-', markerfmt='ro', basefmt='gray')
ax.set_title('Step 0: 原始信号\nf1=矩形[-1,1], f2=冲激(-1,1)', fontsize=10)
ax.set_ylabel('f1 & f2')

# --- Step 1: 冲激delta(t+1) 把 f1 搬到 t=-1 ---
ax = axes[0, 1]
# f1(t+1): 矩形搬到 [-2, 0]
f1_shift_left = np.where((t >= -2) & (t < 0), 1.0, 0.0)
ax.plot(t, f1, 'b', linewidth=1, alpha=0.3, label='f1(原始)')
ax.plot(t, f1_shift_left, 'b', linewidth=2, label='f1(t+1)')
ax.fill_between(t, 0, f1_shift_left, alpha=0.15, color='b')
ax.stem([-1], [1], linefmt='r-', markerfmt='ro', basefmt='gray')
ax.annotate('delta(t+1)', xy=(-1, 1), xytext=(-1, 1.5),
            ha='center', fontsize=9, color='red',
            arrowprops=dict(arrowstyle='->', color='red'))
ax.annotate('搬到-1', xy=(-1.5, 0.5), xytext=(-3.5, 1.3),
            ha='center', fontsize=9,
            arrowprops=dict(arrowstyle='->', color='gray'))
ax.set_title('Step 1: delta(t+1)*f1 = f1(t+1)\n矩形搬至 [-2, 0]', fontsize=10)

# --- Step 2: 冲激delta(t-1) 把 f1 搬到 t=1 ---
ax = axes[0, 2]
f1_shift_right = np.where((t >= 0) & (t < 2), 1.0, 0.0)
ax.plot(t, f1, 'b', linewidth=1, alpha=0.3, label='f1(原始)')
ax.plot(t, f1_shift_right, 'b', linewidth=2, label='f1(t-1)')
ax.fill_between(t, 0, f1_shift_right, alpha=0.15, color='b')
ax.stem([1], [1], linefmt='g-', markerfmt='go', basefmt='gray')
ax.annotate('delta(t-1)', xy=(1, 1), xytext=(1, 1.5),
            ha='center', fontsize=9, color='green',
            arrowprops=dict(arrowstyle='->', color='green'))
ax.set_title('Step 2: delta(t-1)*f1 = f1(t-1)\n矩形搬至 [0, 2]', fontsize=10)

# --- Step 3: 两段叠加 = 答案 ---
ax = axes[0, 3]
y = np.where((t >= -2) & (t < 2), 1.0, 0.0)
ax.plot(t, f1_shift_left, 'b', linewidth=1, alpha=0.4, label='f1(t+1)')
ax.plot(t, f1_shift_right, 'g', linewidth=1, alpha=0.4, label='f1(t-1)')
ax.plot(t, y, 'r', linewidth=2.5, label='叠加=答案')
ax.fill_between(t, 0, y, alpha=0.2, color='r')
ax.set_title('Step 3: 叠加\n= u(t+2) - u(t-2)', fontsize=10)
ax.legend(fontsize=8)

# --- 第二行: 滑动过程 (4个典型位置) ---
# 把 f1 的右边缘对齐冲激, 滑过整个过程
shifts = [-2, 0, 1, 2]
shift_labels = [
    'f1右缘对齐delta(-1): 输出区间起点',
    'f1居中: 覆盖两根冲激',
    'f1左缘对齐delta(+1): 即将脱离',
    'f1左缘对齐delta(+1): 输出区间终点',
]
for i, (s, label) in enumerate(zip(shifts, shift_labels)):
    ax = axes[1, i]
    # 滑动中的 f1: 中心在 s 处 (矩形宽2, 右缘在 s+1)
    f1_sliding = np.where((t >= s - 1) & (t < s + 1), 1.0, 0.0)
    ax.plot(t, f1_sliding, 'b', linewidth=2)
    ax.fill_between(t, 0, f1_sliding, alpha=0.15, color='b')
    ax.stem([-1, 1], [1, 1], linefmt='r-', markerfmt='ro', basefmt='gray')
    ax.set_title(f'{label}\n(slide={s})', fontsize=9)

plt.tight_layout()
plt.savefig('q1_graphical_method.png', dpi=150, bbox_inches='tight')
print("Done! q1_graphical_method.png saved.")
