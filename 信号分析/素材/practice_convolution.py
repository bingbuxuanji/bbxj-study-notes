import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

t = np.linspace(-1, 7, 2000)
dt = t[1] - t[0]

# === 信号 ===
# f1(t) = u(t) - u(t-3)  矩形 [0, 3], 宽=3
f1 = np.where((t >= 0) & (t < 3), 1.0, 0.0)
# f2(t) = delta(t) + delta(t-3)  冲激在 0 和 3
f2 = np.zeros_like(t)
f2[np.argmin(np.abs(t - 0))] = 1.0 / dt
f2[np.argmin(np.abs(t - 3))] = 1.0 / dt

# === f1 的两份平移拷贝 ===
f1_copy0 = np.where((t >= 0) & (t < 3), 1.0, 0.0)     # f1(t)   = u(t)-u(t-3)
f1_copy3 = np.where((t >= 3) & (t < 6), 1.0, 0.0)     # f1(t-3) = u(t-3)-u(t-6)

# === 卷积结果 (理论) ===
y_theory = np.where((t >= 0) & (t < 6), 1.0, 0.0)     # u(t) - u(t-6)

# ==================== 画图 ====================
fig, axes = plt.subplots(2, 2, figsize=(13, 8))

# (a) f1
ax = axes[0, 0]
ax.plot(t, f1, 'b', linewidth=1.5)
ax.fill_between(t, 0, f1, alpha=0.15, color='b')
ax.axhline(y=0, color='gray', linewidth=0.5); ax.axvline(x=0, color='gray', linewidth=0.5)
ax.set_xlim(-1, 7); ax.set_ylim(-0.3, 1.5)
ax.set_xlabel('t')
ax.set_title('f1(t) = u(t) - u(t-3)   矩形 [0, 3], 宽=3', fontsize=12)
ax.grid(True, alpha=0.3)

# (b) f2
ax = axes[0, 1]
ax.stem([0, 3], [1, 1], linefmt='r-', markerfmt='ro', basefmt='gray')
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.set_xlim(-1, 7); ax.set_ylim(-0.3, 1.5)
ax.set_xlabel('t')
ax.set_title('f2(t) = delta(t) + delta(t-3)', fontsize=12)
ax.grid(True, alpha=0.3)

# (c) 卷积 + 理论
conv = np.convolve(f1, f2, mode='same') * dt
ax = axes[1, 0]
ax.plot(t, conv, 'b', linewidth=1.5, label='数值卷积')
ax.plot(t, y_theory, 'r--', linewidth=2, label='u(t)-u(t-6) (理论)')
ax.fill_between(t, 0, y_theory, alpha=0.1, color='r')
ax.axhline(y=0, color='gray', linewidth=0.5); ax.axvline(x=0, color='gray', linewidth=0.5)
ax.set_xlim(-1, 7); ax.set_ylim(-0.3, 1.5)
ax.set_xlabel('t'); ax.set_title('f1 * f2 = u(t) - u(t-6)   矩形 [0, 6], 宽=6', fontsize=12)
ax.legend(fontsize=10); ax.grid(True, alpha=0.3)

# (d) 分解: 两份平移拷贝首尾相接
ax = axes[1, 1]
ax.plot(t, f1_copy0, 'orange', linewidth=1.5, label='f1(t)     [0, 3]')
ax.plot(t, f1_copy3, 'green', linewidth=1.5, label='f1(t-3)  [3, 6]')
ax.plot(t, y_theory, 'r--', linewidth=2, label='叠加 = [0, 6]')
ax.axhline(y=0, color='gray', linewidth=0.5); ax.axvline(x=0, color='gray', linewidth=0.5)
ax.set_xlim(-1, 7); ax.set_ylim(-0.3, 1.5)
ax.set_xlabel('t')
ax.set_title('分解: f1(t) + f1(t-3), 首尾相接拼成宽矩形', fontsize=12)
ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('practice_convolution.png', dpi=150, bbox_inches='tight')
print("Done! practice_convolution.png saved.")
print()
print("=== 新题 ===")
print("f1(t) = u(t) - u(t-3)          矩形 [0, 3], 宽=3")
print("f2(t) = delta(t) + delta(t-3)   冲激在 0 和 3")
print()
print("f1 * f2 = f1(t) + f1(t-3)")
print("        = [u(t)-u(t-3)] + [u(t-3)-u(t-6)]")
print("        = u(t) - u(t-6)         矩形 [0, 6], 宽=6")
print()
print("关键: 冲激间隔 = 矩形宽度, 拷贝刚好首尾相接不重叠")
