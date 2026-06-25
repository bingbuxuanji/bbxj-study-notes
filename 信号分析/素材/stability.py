import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# ===== (a) s-plane 三分区 =====
ax = axes[0, 0]
ax.set_xlim(-5, 5); ax.set_ylim(-5, 5)
ax.axhline(y=0, color='gray', linewidth=1)
ax.axvline(x=0, color='black', linewidth=2, linestyle='-', alpha=0.8)
ax.set_xlabel('sigma (实部)'); ax.set_ylabel('j*omega (虚部)')
ax.set_title('s 平面三分区: 左半稳定 / 虚轴临界 / 右半不稳定', fontsize=12)

# 左半平面 (稳定) - 绿色
ax.fill_between([-5, 0], [-5, -5], [5, 5], alpha=0.12, color='green')
ax.text(-2.5, 4, '左半平面\nsigma<0\n稳定区', fontsize=11, ha='center', color='darkgreen',
        fontweight='bold', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

# 右半平面 (不稳定) - 红色
ax.fill_between([0, 5], [-5, -5], [5, 5], alpha=0.12, color='red')
ax.text(2.5, 4, '右半平面\nsigma>0\n不稳定区', fontsize=11, ha='center', color='darkred',
        fontweight='bold', bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))

# 虚轴
ax.annotate('虚轴 (jw轴)\nsigma=0  临界', xy=(0, 3), xytext=(1.5, 0),
            fontsize=9, color='darkorange',
            arrowprops=dict(arrowstyle='->', color='darkorange', lw=1.5),
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.6))

# 示例极点
poles_stable = [(-1, 2), (-2, -1.5), (-3, 0)]
poles_critical = [(0, 3), (0, -2)]
poles_unstable = [(1.5, 1.5), (3, -0.5)]

for p in poles_stable:
    ax.plot(p[0], p[1], 'go', markersize=10, markeredgecolor='darkgreen')
for p in poles_critical:
    ax.plot(p[0], p[1], 'o', color='orange', markersize=10, markeredgecolor='darkorange')
for p in poles_unstable:
    ax.plot(p[0], p[1], 'ro', markersize=10, markeredgecolor='darkred')

ax.annotate('s=-2\n稳定', xy=(-2, -1.5), xytext=(-4, -3.5),
            fontsize=8, color='darkgreen',
            arrowprops=dict(arrowstyle='->', color='darkgreen', lw=1))
ax.annotate('s=0\n临界', xy=(0, -2), xytext=(1.5, -3.5),
            fontsize=8, color='darkorange',
            arrowprops=dict(arrowstyle='->', color='darkorange', lw=1))
ax.annotate('s=1.5\n不稳定', xy=(1.5, 1.5), xytext=(3.5, 3.5),
            fontsize=8, color='darkred',
            arrowprops=dict(arrowstyle='->', color='darkred', lw=1))

# ===== (b) 极点位置 vs 时域行为 =====
ax = axes[0, 1]
t = np.linspace(0, 5, 300)

# 左半平面: 衰减
ax.plot(t, np.exp(-1*t), 'g', linewidth=2, label='e^{-1t} (s=-1, 稳定)')
ax.plot(t, np.exp(-2*t), 'darkgreen', linewidth=2, label='e^{-2t} (s=-2, 更快衰减)')

# 虚轴: 等幅
ax.plot(t, np.ones_like(t), 'orange', linewidth=2, label='1 (s=0, 临界)')

# 右半平面: 增长
ax.plot(t, np.exp(0.5*t), 'r', linewidth=2, label='e^{0.5t} (s=0.5, 不稳定)')
ax.plot(t, np.exp(1.0*t), 'darkred', linewidth=2, label='e^{1.0t} (s=1, 更快发散)')

ax.axhline(y=0, color='gray', linewidth=0.5)
ax.set_xlim(0, 5); ax.set_ylim(-0.5, 5)
ax.set_xlabel('t'); ax.set_title('极点位置 -> 时域行为', fontsize=12)
ax.legend(fontsize=7, loc='upper left')
ax.grid(True, alpha=0.25)

# ===== (c) 具体例题: 期中 Q27 和 Q28 =====
ax = axes[1, 0]
ax.set_xlim(-4, 1); ax.set_ylim(-3, 3)
ax.axhline(y=0, color='gray', linewidth=1)
ax.axvline(x=0, color='black', linewidth=2, linestyle='-', alpha=0.5)
ax.set_xlabel('sigma'); ax.set_ylabel('j*omega')
ax.set_title('例题: Q27(不稳定) vs Q28(稳定)', fontsize=12)
ax.fill_between([-4, 0], [-3, -3], [3, 3], alpha=0.08, color='green')
ax.fill_between([0, 1], [-3, -3], [3, 3], alpha=0.08, color='red')

# Q27: H(s)=1/[s(s+1)], 极点 0, -1
ax.plot(0, 0, 'rx', markersize=14, markeredgewidth=2.5)
ax.annotate('s1=0 (在虚轴!)\n积分器 -> 不稳定', xy=(0, 0), xytext=(-2.5, 2),
            fontsize=9, ha='center', color='darkred',
            fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5),
            arrowprops=dict(arrowstyle='->', color='darkred', lw=2))
ax.plot(-1, 0, 'x', color='darkorange', markersize=12, markeredgewidth=2)
ax.annotate('s2=-1 (稳定)', xy=(-1, 0), xytext=(-3, -2),
            fontsize=9, color='darkorange',
            arrowprops=dict(arrowstyle='->', color='darkorange', lw=1))

# Q28: H(s)=(2s+1)/(s^2+5s+6), 极点 -2, -3
ax.plot(-2, 1.5, 'go', markersize=14, markeredgecolor='darkgreen')
ax.plot(-3, -1.5, 'go', markersize=14, markeredgecolor='darkgreen')
ax.annotate('s1=-2, s2=-3\n都在左半平面\n-> 稳定!', xy=(-2.5, 0),
            xytext=(-1.5, -1.5),
            fontsize=10, ha='center', color='darkgreen', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.6))

# 标注 Q27/Q28
ax.text(-3.5, 2.8, 'Q27: H(s)=1/s(s+1)', fontsize=9, color='darkred', fontweight='bold')
ax.text(-3.5, -2.8, 'Q28: H(s)=(2s+1)/(s^2+5s+6)', fontsize=9, color='darkgreen', fontweight='bold')

ax.grid(True, alpha=0.25)

# ===== (d) 为什么虚轴极点导致不稳定 =====
ax = axes[1, 1]
t_long = np.linspace(0, 10, 500)
ax.plot(t_long, np.ones_like(t_long), 'orange', linewidth=2, label='s=0: 阶跃响应 -> 斜坡 (无界!)')
ax.plot(t_long, t_long * 0.3, 'orange', linewidth=1.5, linestyle='--', alpha=0.6,
        label='u(t)输入积分器 -> 输出 t*u(t)')
ax.plot(t_long, np.exp(-2*t_long), 'g', linewidth=2, label='s=-2: 冲激响应 -> 衰减到0')
ax.plot(t_long, np.sin(2*t_long), 'purple', linewidth=1.5,
        label='s=+-j2: 等幅振荡 (临界)')
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.set_xlim(0, 10); ax.set_ylim(-2, 3)
ax.set_xlabel('t'); ax.set_title('为什么 s=0 不稳定? — 积分器效应', fontsize=12)
ax.legend(fontsize=8, loc='upper right')
ax.grid(True, alpha=0.25)

# 标注
ax.annotate('输入常数 -> 输出斜坡\n随时间无限增长!', xy=(7, 2.1), xytext=(3, 2.5),
            fontsize=9, color='darkred',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.3),
            arrowprops=dict(arrowstyle='->', color='darkred', lw=1.5))
ax.annotate('左半平面极点:\n永远衰减到0', xy=(3, 0.3), xytext=(6, 1.5),
            fontsize=9, color='darkgreen',
            arrowprops=dict(arrowstyle='->', color='darkgreen', lw=1.5))

fig.suptitle('稳定性判据: 极点位置决定系统命运', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('stability.png', dpi=150, bbox_inches='tight')
print("Done! stability.png saved.")
