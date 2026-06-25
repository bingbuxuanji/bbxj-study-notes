import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ===== 参数 =====
tau = 2.0          # 矩形脉冲宽度
omega_0 = 20.0     # 载波频率 (调制目标)
t = np.linspace(-4, 4, 4000)
omega = np.linspace(-50, 50, 4000)

# ===== 基带信号: 矩形脉冲 =====
x = np.where(np.abs(t) < tau/2, 1.0, 0.0)

# ===== 载波 =====
carrier_cos = np.cos(omega_0 * t)

# ===== 已调信号 =====
x_mod_cos = x * carrier_cos   # 基带 x 余弦载波 (实际调制)

# ===== 频谱 =====
# X(omega) = tau * Sa(omega*tau/2)
X_base = tau * np.sinc(omega * tau / (2 * np.pi))   # numpy sinc(x) = sin(pi x)/(pi x)
# 已调信号的频谱: 1/2 [X(omega-omega_0) + X(omega+omega_0)]
X_mod = 0.5 * tau * np.sinc((omega - omega_0) * tau / (2 * np.pi)) \
      + 0.5 * tau * np.sinc((omega + omega_0) * tau / (2 * np.pi))

# ==================== 画图 ====================
fig, axes = plt.subplots(2, 2, figsize=(14, 9))

# ---- (a) 基带信号 x(t) ----
ax = axes[0, 0]
ax.plot(t, x, 'b', linewidth=2)
ax.fill_between(t, 0, x, alpha=0.12, color='b')
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.axvline(x=0, color='gray', linewidth=0.3)
ax.set_xlim(-4, 4); ax.set_ylim(-0.3, 1.5)
ax.set_xlabel('t'); ax.set_ylabel('x(t)')
ax.set_title('基带信号  x(t) = 矩形脉冲 (宽=2)', fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.25)

# 标注: 时域宽度
ax.annotate('', xy=(-1, 1.25), xytext=(1, 1.25),
            arrowprops=dict(arrowstyle='<->', color='darkblue', lw=2))
ax.text(0, 1.35, 'tau = 2', ha='center', fontsize=11, color='darkblue', fontweight='bold')

# ---- (b) 基带频谱 X(omega) ----
ax = axes[0, 1]
ax.plot(omega, X_base, 'b', linewidth=2)
ax.fill_between(omega, 0, X_base, alpha=0.12, color='b')
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.axvline(x=0, color='gray', linewidth=0.3, linestyle='--')
ax.set_xlim(-50, 50); ax.set_ylim(-0.5, 2.3)
ax.set_xlabel('omega (rad/s)'); ax.set_ylabel('X(omega)')
ax.set_title('基带频谱  X(omega) = tau * Sa(omega*tau/2)', fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.25)

# 标注: 频谱集中在 0 附近
ax.annotate('频谱集中\n在 omega=0', xy=(0, 2), xytext=(15, 2.2),
            fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='->', color='darkblue', lw=2))

# ---- (c) 已调信号 x(t)*cos(omega_0 t) ----
ax = axes[1, 0]
ax.plot(t, x_mod_cos, 'r', linewidth=0.8)
ax.plot(t, x, 'b', linewidth=1.5, alpha=0.3, label='x(t) 包络')
ax.plot(t, -x, 'b', linewidth=1.5, alpha=0.3)
ax.plot(t, carrier_cos * 0.5, 'gray', linewidth=0.4, alpha=0.5, label='载波(缩小)')
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.axvline(x=0, color='gray', linewidth=0.3)
ax.set_xlim(-4, 4); ax.set_ylim(-1.3, 1.3)
ax.set_xlabel('t'); ax.set_ylabel('')
ax.set_title('已调信号  x(t) * cos(omega_0 t)', fontsize=13, fontweight='bold')
ax.legend(fontsize=8, loc='upper right')
ax.grid(True, alpha=0.25)

# 标注: 时域包络不变, 内部填满载波
ax.annotate('包络 = x(t)', xy=(-1.8, 0.95), xytext=(-3.5, 1.1),
            fontsize=10, color='blue',
            arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))
ax.annotate('载波振荡', xy=(0.5, 0.7), xytext=(2, 1.1),
            fontsize=10, color='red',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

# ---- (d) 已调频谱 (频移!) ----
ax = axes[1, 1]
ax.plot(omega, X_mod, 'r', linewidth=2)
ax.fill_between(omega, 0, X_mod, alpha=0.12, color='r')
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.axvline(x=0, color='gray', linewidth=0.3, linestyle='--')
# 标注载频位置
ax.axvline(x=omega_0, color='darkred', linewidth=0.8, linestyle='--', alpha=0.6)
ax.axvline(x=-omega_0, color='darkred', linewidth=0.8, linestyle='--', alpha=0.6)
ax.set_xlim(-50, 50); ax.set_ylim(-0.3, 1.3)
ax.set_xlabel('omega (rad/s)'); ax.set_ylabel('')
ax.set_title('已调频谱 = 1/2 [X(omega-omega_0) + X(omega+omega_0)]', fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.25)

# 标注: 频谱搬到了 ±omega_0
ax.annotate('搬到 -omega_0', xy=(-omega_0, 1.0), xytext=(-38, 1.2),
            fontsize=10, ha='center', color='darkred',
            arrowprops=dict(arrowstyle='->', color='darkred', lw=2))
ax.annotate('搬到 +omega_0', xy=(omega_0, 1.0), xytext=(38, 1.2),
            fontsize=10, ha='center', color='darkred',
            arrowprops=dict(arrowstyle='->', color='darkred', lw=2))
ax.annotate('原来在 omega=0\n的频谱', xy=(0, 0.05), xytext=(10, 0.5),
            fontsize=9, color='gray',
            arrowprops=dict(arrowstyle='->', color='gray', lw=1.2))

# 总标题
fig.suptitle('频移性质:  x(t) * cos(omega_0 t)  <-->  1/2 [X(omega-omega_0) + X(omega+omega_0)]',
             fontsize=15, fontweight='bold', y=0.99)

plt.tight_layout()
plt.savefig('frequency_shift.png', dpi=150, bbox_inches='tight')
print("Done! frequency_shift.png saved.")
print()
print("=== 频移性质 (调制定理) ===")
print("数学形式: x(t) * e^(j*omega_0*t)  <-->  X(omega - omega_0)")
print("实数形式: x(t) * cos(omega_0*t)  <-->  1/2[X(omega-omega_0) + X(omega+omega_0)]")
print()
print("物理含义: 时域乘以高频载波 = 频域整体搬到载频处")
print("应用:     AM/FM 调制、变频、通信发射机")
