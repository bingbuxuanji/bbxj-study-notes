import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

omega = np.linspace(-15, 15, 3000)

# ===== 幅频 |H(jω)| = u(ω+10) - u(ω-10) =====
H_mag = np.where(np.abs(omega) <= 10, 1.0, 0.0)

# ===== 相频 φ(ω) =====
phi = np.zeros_like(omega)
for i, w in enumerate(omega):
    if w < -5:
        phi[i] = 5
    elif w <= 5:   # -5 <= w <= 5
        phi[i] = -w
    else:          # w > 5
        phi[i] = -5

# ===== 四个候选信号的频率分量 =====
# A: sin(2t)+sin(4t)   -> ω = 2, 4        (都在 (-5,5) 内)
# B: cos²(4t)=½+½cos8t -> ω = 0, 8        (8 在 (5,10) 被相位失真)
# C: cos t + cos 8t    -> ω = 1, 8        (8 失真)
# D: sin(2t)sin(4t)=½[cos2t-cos6t] -> 2,6 (6 失真)

signals = {
    'A': {'freqs': [2, 4],   'color': 'green',  'label': 'A: sin2t+sin4t  (2,4)',    'distortionless': True},
    'B': {'freqs': [0, 8],   'color': 'orange', 'label': 'B: cos²4t  (0,8)',          'distortionless': False},
    'C': {'freqs': [1, 8],   'color': 'purple', 'label': 'C: cost+cos8t  (1,8)',      'distortionless': False},
    'D': {'freqs': [2, 6],   'color': 'brown',  'label': 'D: sin2t sin4t  (2,6)',     'distortionless': False},
}

# ==================== 画图 ====================
fig, axes = plt.subplots(2, 2, figsize=(15, 9))

# ---- (a) 幅频特性 |H(jω)| ----
ax = axes[0, 0]
ax.plot(omega, H_mag, 'b', linewidth=2)
ax.fill_between(omega, 0, H_mag, alpha=0.1, color='b')
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.axvline(x=0, color='gray', linewidth=0.3)
ax.axvline(x=-10, color='blue', linewidth=0.8, linestyle='--', alpha=0.5)
ax.axvline(x=10, color='blue', linewidth=0.8, linestyle='--', alpha=0.5)
ax.set_xlim(-15, 15); ax.set_ylim(-0.3, 1.5)
ax.set_xlabel('omega (rad/s)')
ax.set_title('|H(jomega)| = u(omega+10) - u(omega-10)   通带 [-10, 10]', fontsize=12)
ax.grid(True, alpha=0.25)
ax.text(-10, -0.15, '-10', ha='center', fontsize=9, color='blue')
ax.text(10, -0.15, '10', ha='center', fontsize=9, color='blue')

# 标注: 通带全为1
ax.annotate('通带: |H|=1\n(幅度不失真)', xy=(0, 1), xytext=(3, 1.3),
            fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))

# ---- (b) 相频特性 φ(ω) ----
ax = axes[0, 1]
ax.plot(omega, phi, 'r', linewidth=2)
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.axvline(x=0, color='gray', linewidth=0.3)
ax.axvline(x=-5, color='red', linewidth=0.8, linestyle='--', alpha=0.5)
ax.axvline(x=5, color='red', linewidth=0.8, linestyle='--', alpha=0.5)
ax.set_xlim(-15, 15); ax.set_ylim(-8, 8)
ax.set_xlabel('omega (rad/s)')
ax.set_title('phi(omega): 仅 (-5,5) 内为过原点直线', fontsize=12)
ax.grid(True, alpha=0.25)

# 标注三个区域
ax.annotate('phi=-omega\n(线性! 无失真)', xy=(0, 0), xytext=(-2, -4),
            fontsize=9, ha='center', color='darkgreen',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.3),
            arrowprops=dict(arrowstyle='->', color='darkgreen', lw=1.2))
ax.annotate('phi=5\n(常数≠直线\n相位失真!)', xy=(-10, 5), xytext=(-13, 6),
            fontsize=8, ha='center', color='darkred',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightcoral', alpha=0.3),
            arrowprops=dict(arrowstyle='->', color='darkred', lw=1))
ax.annotate('phi=-5\n(常数≠直线\n相位失真!)', xy=(10, -5), xytext=(13, -6),
            fontsize=8, ha='center', color='darkred',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightcoral', alpha=0.3),
            arrowprops=dict(arrowstyle='->', color='darkred', lw=1))

# 标注分界线
ax.text(-5, 7.5, 'ω=-5', ha='center', fontsize=9, color='red')
ax.text(5, -7, 'ω=5', ha='center', fontsize=9, color='red')

# ---- (c) 无失真区域示意 ----
ax = axes[1, 0]
# 画一个简化版，把通带分成三个区
ax.fill_between([-10, -5], [0, 0], [2, 2], alpha=0.15, color='red')
ax.fill_between([-5, 5], [0, 0], [2, 2], alpha=0.25, color='green')
ax.fill_between([5, 10], [0, 0], [2, 2], alpha=0.15, color='red')
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.set_xlim(-14, 14); ax.set_ylim(-0.5, 2.5)
ax.set_xlabel('omega (rad/s)')
ax.set_title('通带分区: 绿色=无失真, 红色=相位失真, 白色=截止', fontsize=12)
ax.grid(True, alpha=0.25)

# 标注
ax.text(-7.5, 1, '|H|=1\nφ=常数\n→ 相位失真', ha='center', fontsize=8, color='darkred')
ax.text(0, 1.3, '|H|=1 且 φ=-ω\n→ 无失真!', ha='center', fontsize=10, color='darkgreen',
        fontweight='bold')
ax.text(7.5, 1, '|H|=1\nφ=常数\n→ 相位失真', ha='center', fontsize=8, color='darkred')
ax.text(-12, 0.5, '|H|=0\n截止', ha='center', fontsize=8, color='gray')
ax.text(12, 0.5, '|H|=0\n截止', ha='center', fontsize=8, color='gray')

# 画频率分量标记
y_offset = 2.1
for key, sig in signals.items():
    for f in sig['freqs']:
        if abs(f) <= 10:
            marker = 'o' if sig['distortionless'] and abs(f) <= 5 else 'x'
            mcolor = 'green' if (sig['distortionless'] and abs(f) <= 5) else 'red'
            ax.plot(f, y_offset, marker=marker, color=mcolor, markersize=10, markeredgewidth=1.5)
            y_offset -= 0.25

# 图例
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='频率在 (-5,5) 内: 无失真'),
    Line2D([0], [0], marker='x', color='w', markeredgecolor='red', markersize=10, label='频率在 (±5,±10): 相位失真'),
]
ax.legend(handles=legend_elements, fontsize=8, loc='lower right')

# ---- (d) 四个选项的频谱分析 ----
ax = axes[1, 1]
ax.axis('off')

text = (
    "四个候选信号的频率分量:\n\n"
    "A. sin(2t) + sin(4t)\n"
    "    w = 2, 4  ->  都在 (-5,5) 内\n"
    "    |H|=1, phi=-w  ->  无失真 [OK]\n\n"
    "B. cos^2(4t) = 1/2 + 1/2*cos(8t)\n"
    "    w = 0, 8  ->  8 在 (5,10) 相位失真 [X]\n\n"
    "C. cos(t) + cos(8t)\n"
    "    w = 1, 8  ->  8 相位失真 [X]\n\n"
    "D. sin(2t)sin(4t) = 1/2[cos(2t)-cos(6t)]\n"
    "    w = 2, 6  ->  6 相位失真 [X]\n\n"
    "==============================\n"
    "无失真条件回顾:\n"
    "|H(jw)| = 常数  +  phi(w) = -w*t0\n"
    "本系统中仅 (-5, 5) 内满足!\n"
    "因此选 A"
)

ax.text(0.05, 0.95, text, transform=ax.transAxes,
        fontsize=9.5, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

fig.suptitle('期中 Q9: 无失真传输条件 | 系统 H(jω) 特性分析', fontsize=15, fontweight='bold')

plt.tight_layout()
plt.savefig('q9_system.png', dpi=150, bbox_inches='tight')
print("Done! q9_system.png saved.")
