import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

t = np.linspace(-4, 4, 2000)
dt = t[1] - t[0]

# === 信号 f1(t)：矩形脉冲 u(t+1) - u(t-1) ===
f1 = np.where((t >= -1) & (t < 1), 1.0, 0.0)

# === 信号 f2(t)：两根冲激 delta(t+1) + delta(t-1) ===
f2 = np.zeros_like(t)
idx_neg1 = np.argmin(np.abs(t - (-1)))
idx_pos1 = np.argmin(np.abs(t - 1))
f2[idx_neg1] = 1.0 / dt  # 面积=1
f2[idx_pos1] = 1.0 / dt

# === 卷积 ===
conv = np.convolve(f1, f2, mode='same') * dt

# === 理论结果 y(t) = u(t+2) - u(t-2) ===
y_theory = np.where((t >= -2) & (t < 2), 1.0, 0.0)

# ==================== 画图 ====================
fig, axes = plt.subplots(2, 2, figsize=(13, 8))

# (a) f1(t)
ax = axes[0, 0]
ax.plot(t, f1, 'b', linewidth=1.5)
ax.fill_between(t, 0, f1, alpha=0.15, color='b')
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.axvline(x=0, color='gray', linewidth=0.5)
ax.set_xlim(-4, 4); ax.set_ylim(-0.3, 1.5)
ax.set_xlabel('t')
ax.set_title('f1(t) = u(t+1) - u(t-1)   (矩形脉冲, 宽=2)', fontsize=12)
ax.grid(True, alpha=0.3)

# (b) f2(t) — stem 冲激
ax = axes[0, 1]
ax.stem([-1, 1], [1, 1], linefmt='r-', markerfmt='ro', basefmt='gray')
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.set_xlim(-4, 4); ax.set_ylim(-0.3, 1.5)
ax.set_xlabel('t')
ax.set_title('f2(t) = delta(t+1) + delta(t-1)   (两根冲激)', fontsize=12)
ax.grid(True, alpha=0.3)

# (c) 卷积结果
ax = axes[1, 0]
ax.plot(t, conv, 'b', linewidth=1.5, label='f1 * f2 (数值卷积)')
ax.plot(t, y_theory, 'r--', linewidth=2, label='u(t+2)-u(t-2) (理论)')
ax.fill_between(t, 0, y_theory, alpha=0.1, color='r')
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.axvline(x=0, color='gray', linewidth=0.5)
ax.set_xlim(-4, 4); ax.set_ylim(-0.3, 1.5)
ax.set_xlabel('t')
ax.set_title('卷积结果  y(t) = f1(t) * f2(t)', fontsize=12)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

# (d) 分解：f1(t+1) + f1(t-1)
ax = axes[1, 1]
ax.plot(t, np.where((t >= -2) & (t < 0), 1.0, 0.0), 'orange', linewidth=1,
        label='f1(t+1)  <- 左移')
ax.plot(t, np.where((t >= 0) & (t < 2), 1.0, 0.0), 'green', linewidth=1,
        label='f1(t-1)  -> 右移')
ax.plot(t, y_theory, 'r--', linewidth=2, label='两者叠加')
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.axvline(x=0, color='gray', linewidth=0.5)
ax.set_xlim(-4, 4); ax.set_ylim(-0.3, 1.5)
ax.set_xlabel('t')
ax.set_title('分解: f1(t+1) + f1(t-1) = u(t+2)-u(t-2)', fontsize=12)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('q1_convolution.png', dpi=150, bbox_inches='tight')
print("Done! Image saved as q1_convolution.png")
print()
print("=== 推导 ===")
print("f1(t) = u(t+1) - u(t-1)        <-- 矩形脉冲 [-1, 1]")
print("f2(t) = delta(t+1) + delta(t-1) <-- 两根冲激")
print()
print("f1 * f2 = f1 * delta(t+1) + f1 * delta(t-1)")
print("        = f1(t+1) + f1(t-1)                    <-- delta 卷积性质")
print()
print("f1(t+1) = u(t+2) - u(t)          <-- 矩形移至 [-2, 0]")
print("f1(t-1) = u(t)   - u(t-2)        <-- 矩形移至 [ 0, 2]")
print("        + -------------------")
print("        = u(t+2) - u(t-2)         <-- 矩形 [-2, 2], 宽=4")
