import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

omega = np.linspace(-300, 300, 5000)
omega_c = 120 * np.pi   # 截止频率 ≈ 377 rad/s

# ===== 理想低通滤波器 =====
H_mag = np.where(np.abs(omega) <= omega_c, 2.0, 0.0)

# ===== 输入信号的两个分量 =====
# x1: 20cos(100pi t),  omega1 = 100pi ≈ 314
# x2:  5cos(200pi t),  omega2 = 200pi ≈ 628
omega_1 = 100 * np.pi
omega_2 = 200 * np.pi

# ==================== 画图 ====================
fig, axes = plt.subplots(2, 2, figsize=(14, 9))

# ---- (a) 理想低通滤波器频率响应 ----
ax = axes[0, 0]
ax.plot(omega, H_mag, 'b', linewidth=2)
ax.fill_between(omega, 0, H_mag, alpha=0.1, color='b')
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.axvline(x=0, color='gray', linewidth=0.5)
ax.axvline(x=-omega_c, color='blue', linewidth=0.8, linestyle='--', alpha=0.5)
ax.axvline(x=omega_c, color='blue', linewidth=0.8, linestyle='--', alpha=0.5)
ax.set_xlim(-300, 300); ax.set_ylim(-0.3, 2.5)
ax.set_xlabel('omega (rad/s)')
ax.set_title('理想低通: |H(jomega)|=2 (|omega|<=120pi), 0 (|omega|>120pi)', fontsize=12)
ax.grid(True, alpha=0.25)

# 标注截止频率
ax.annotate('-120pi', xy=(-omega_c, 2), xytext=(-280, 2.2),
            fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))
ax.annotate('+120pi', xy=(omega_c, 2), xytext=(280, 2.2),
            fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))
ax.axhline(y=2, color='blue', linewidth=0.5, linestyle=':', alpha=0.3)
ax.text(0, 2.15, '通带增益 = 2', ha='center', fontsize=10, color='blue')

# ---- (b) 输入信号频谱 ----
ax = axes[0, 1]
# 输入频谱: 20cos(100pi t) + 5cos(200pi t)
# = 20*pi[delta(w-100pi)+delta(w+100pi)] + 5*pi[delta(w-200pi)+delta(w+200pi)]
ax.stem([-omega_2, -omega_1, omega_1, omega_2],
        [5*np.pi, 20*np.pi, 20*np.pi, 5*np.pi],
        linefmt='darkgreen', markerfmt='go', basefmt='gray')
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.axvline(x=0, color='gray', linewidth=0.3)
ax.set_xlim(-300, 300); ax.set_ylim(-5, 75)
ax.set_xlabel('omega (rad/s)')
ax.set_title('输入频谱: 20cos(100pi*t) + 5cos(200pi*t)', fontsize=12)
ax.grid(True, alpha=0.25)

# 标注每根谱线
ax.annotate('20cos(100pi*t)\n幅度=20, w=100pi',
            xy=(omega_1, 20*np.pi), xytext=(omega_1+30, 60),
            fontsize=9, ha='center',
            arrowprops=dict(arrowstyle='->', color='green', lw=1.2))
ax.annotate('5cos(200pi*t)\n幅度=5, w=200pi',
            xy=(omega_2, 5*np.pi), xytext=(omega_2+30, 30),
            fontsize=9, ha='center',
            arrowprops=dict(arrowstyle='->', color='green', lw=1.2))
ax.annotate('(共轭对称)', xy=(-omega_1, 20*np.pi), xytext=(-omega_1-50, 60),
            fontsize=8, ha='center', color='gray',
            arrowprops=dict(arrowstyle='->', color='gray', lw=0.8))

# ---- (c) 输入频谱 vs 滤波器叠加 ----
ax = axes[1, 0]
# 画滤波器掩模
ax.fill_between(omega, 0, H_mag*25, alpha=0.08, color='blue')
ax.plot(omega, H_mag*25, 'b--', linewidth=1, alpha=0.4, label='|H(w)| (通带边界)')
# 输入谱线
ax.stem([-omega_2, -omega_1, omega_1, omega_2],
        [5*np.pi, 20*np.pi, 20*np.pi, 5*np.pi],
        linefmt='darkgreen', markerfmt='go', basefmt='gray', label='输入频谱')
# 标注通过/被滤
ax.annotate('PASS\n(100pi < 120pi)', xy=(omega_1, 20*np.pi),
            xytext=(omega_1+60, 50), fontsize=10, ha='center', color='darkgreen',
            fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5),
            arrowprops=dict(arrowstyle='->', color='darkgreen', lw=2))
ax.annotate('CUT!\n(200pi > 120pi)', xy=(omega_2, 5*np.pi),
            xytext=(omega_2+60, 30), fontsize=10, ha='center', color='darkred',
            fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5),
            arrowprops=dict(arrowstyle='->', color='darkred', lw=2))

ax.axhline(y=0, color='gray', linewidth=0.5)
ax.set_xlim(-300, 300); ax.set_ylim(-5, 85)
ax.set_xlabel('omega (rad/s)')
ax.set_title('滤波器 x 输入频谱: 100pi通过, 200pi被滤除', fontsize=12)
ax.legend(fontsize=8, loc='upper left')
ax.grid(True, alpha=0.25)

# ---- (d) 输出信号 ----
ax = axes[1, 1]
t_demo = np.linspace(0, 0.06, 1000)
x_in = 20 * np.cos(100*np.pi*t_demo) + 5 * np.cos(200*np.pi*t_demo)
x_out_passband = 20 * np.cos(100*np.pi*t_demo)  # 仅100pi分量通过
# 如果增益=2: x_out_gain2 = 40 * np.cos(100*np.pi*t_demo)

ax.plot(t_demo, x_in, 'gray', linewidth=1, alpha=0.6, label='输入 x(t)')
ax.plot(t_demo, x_out_passband, 'b', linewidth=2.5, label='输出 y(t)=20cos(100pi*t)')
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.set_xlim(0, 0.06); ax.set_ylim(-28, 28)
ax.set_xlabel('t (s)'); ax.set_ylabel('')
ax.set_title('波形对比: 输入(灰) vs 输出(蓝)', fontsize=12)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.25)

# 标注
ax.annotate('输入含高频毛刺\n(200pi分量)', xy=(0.02, 15), xytext=(0.035, 20),
            fontsize=9, color='gray',
            arrowprops=dict(arrowstyle='->', color='gray', lw=1))
ax.annotate('输出光滑\n只剩100pi分量', xy=(0.03, 10), xytext=(0.04, -15),
            fontsize=9, color='blue',
            arrowprops=dict(arrowstyle='->', color='blue', lw=1))

fig.suptitle('期中 Q19: 理想低通滤波器 — 频率选择', fontsize=15, fontweight='bold')

plt.tight_layout()
plt.savefig('q19_filter.png', dpi=150, bbox_inches='tight')
print("Done! q19_filter.png saved.")
print()
print("=== Q19 详解 ===")
print("滤波器: |H(jw)| = 2 (|w|<=120pi),  0 (|w|>120pi)")
print("截止角频率: w_c = 120*pi = 377 rad/s")
print("截止频率:   f_c = 60 Hz")
print()
print("输入 x(t) = 20cos(100pi*t) + 5cos(200pi*t)")
print("  分量1: w1 = 100*pi = 314 rad/s  (f=50 Hz)")
print("  分量2: w2 = 200*pi = 628 rad/s  (f=100 Hz)")
print()
print("判断:")
print("  w1=100pi < 120pi -> 在通带内 -> 通过!")
print("  w2=200pi > 120pi -> 在通带外 -> 被滤除!")
print()
print("输出 y(t) = 20cos(100pi*t)  -> 答案 A")
print()
print("注意: 本题系统答案忽略了增益2,")
print("严格按 H=2 的话输出应为 40cos(100pi*t)")
print("实际考试按系统答案 A 即可")
