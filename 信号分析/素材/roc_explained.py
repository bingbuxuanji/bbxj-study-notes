import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(2, 2, figsize=(14, 11))

# ===== (a) 什么是 ROC: 因果信号 e^{-2t}u(t) =====
ax = axes[0, 0]
ax.set_xlim(-5, 5); ax.set_ylim(-5, 5)
ax.axhline(y=0, color='gray', linewidth=1)
ax.axvline(x=0, color='gray', linewidth=1)
ax.set_xlabel('sigma (实部)'); ax.set_ylabel('j*omega (虚部)')
ax.set_title('因果信号 e^{-2t}u(t) 的 ROC: sigma > -2', fontsize=12)

# s-plane
ax.fill_between([-2, 5], [-5, -5], [5, 5], alpha=0.15, color='green')
# 极点标记
ax.plot(-2, 0, 'rx', markersize=12, markeredgewidth=2)
ax.annotate('极点 s=-2', xy=(-2, 0), xytext=(-3.5, 1.5), fontsize=10, color='red',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

# jω 轴标注
ax.plot([0, 0], [-5, 5], 'b--', linewidth=0.8, alpha=0.5)
ax.text(0.3, 4.5, 'jw轴', fontsize=9, color='blue')

# ROC 标注
ax.annotate('ROC:\nsigma > -2\n(极点以右的半平面)', xy=(2, 3), fontsize=10, ha='center',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.6))

# 在被排除的区域画斜线示意
for y_val in np.linspace(-4.5, 4.5, 7):
    ax.plot([-5, -2], [y_val, y_val], 'r-', linewidth=0.3, alpha=0.3)

# 小图: 时域波形
ax_inset = ax.inset_axes([0.55, 0.08, 0.4, 0.3])
t_inset = np.linspace(-1, 4, 200)
ax_inset.plot(t_inset, np.exp(-2*t_inset) * (t_inset >= 0), 'b', linewidth=1.5)
ax_inset.axhline(y=0, color='gray', linewidth=0.5)
ax_inset.set_title('e^{-2t}u(t)', fontsize=8)
ax_inset.set_xlim(-1, 4); ax_inset.set_ylim(-0.2, 1.2)

# ===== (b) 为什么需要 ROC: 不同信号可能对应相同 F(s) =====
ax = axes[0, 1]
# 同一 F(s) = 1/(s+2)(s-1), 极点 s=-2, s=1
# 因果: ROC sigma>1
# 反因果: ROC sigma<-2
# 双边: ROC -2<sigma<1

# 画三个不同区域的框
# 因果 ROC
from matplotlib.patches import Rectangle
ax.add_patch(Rectangle((1, -5.2), 5, 10.4, alpha=0.12, color='blue', zorder=0))
# 双边 ROC (带状)
ax.add_patch(Rectangle((-2, -5.2), 3, 10.4, alpha=0.12, color='orange', zorder=0))
# 反因果 ROC
ax.add_patch(Rectangle((-5.5, -5.2), 3.5, 10.4, alpha=0.12, color='purple', zorder=0))

ax.set_xlim(-5.5, 6); ax.set_ylim(-5, 5)
ax.axhline(y=0, color='gray', linewidth=1)
ax.axvline(x=0, color='gray', linewidth=1, linestyle='--', alpha=0.5)
ax.set_xlabel('sigma'); ax.set_ylabel('j*omega')
ax.set_title('F(s)=1/[(s+2)(s-1)]  不同 ROC -> 不同 f(t)!', fontsize=12)

# 极点
ax.plot(-2, 0, 'rx', markersize=10, markeredgewidth=2)
ax.plot(1, 0, 'rx', markersize=10, markeredgewidth=2)
ax.annotate('p=-2', xy=(-2, 0), xytext=(-2, -1.5), fontsize=9, ha='center', color='red')
ax.annotate('p=1', xy=(1, 0), xytext=(1, -1.5), fontsize=9, ha='center', color='red')

# 标注三个可能的 f(t)
ax.text(3.5, 3.5, 'ROC sigma>1\n-> 因果信号\n(e^{t}+e^{-2t})u(t)\n发散!', fontsize=8, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
ax.text(0.5, 3.5, 'ROC -2<sigma<1\n-> 双边信号\n-e^{t}u(-t)+e^{-2t}u(t)', fontsize=8, ha='center',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6))
ax.text(-3.5, 3.5, 'ROC sigma<-2\n-> 反因果信号\n-(e^{t}+e^{-2t})u(-t)', fontsize=8, ha='center',
        bbox=dict(boxstyle='round', facecolor='plum', alpha=0.6))

# ===== (c) ROC 与傅里叶变换的关系 =====
ax = axes[1, 0]
ax.set_xlim(-5, 5); ax.set_ylim(-5, 5)
ax.axhline(y=0, color='gray', linewidth=1)
ax.axvline(x=0, color='b', linewidth=2, linestyle='--', alpha=0.7)
ax.set_xlabel('sigma'); ax.set_ylabel('j*omega')
ax.set_title('ROC 包含 jw 轴 <-> 傅里叶变换存在', fontsize=12)

# 信号 e^{-t}u(t) 极点 s=-1, ROC sigma>-1 (包含 jw 轴)
ax.fill_between([-1, 5], [-5, -5], [5, 5], alpha=0.18, color='green')
ax.plot(-1, 0, 'rx', markersize=10, markeredgewidth=2)
ax.annotate('极点 s=-1', xy=(-1, 0), xytext=(-2.5, 2), fontsize=9, color='red',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.2))
ax.text(2, 4, 'ROC: sigma > -1\n包含 jw 轴\n-> FT 存在!', fontsize=9, ha='center', color='darkgreen',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.6))
ax.annotate('jw 轴 (sigma=0)\nFT = LT|_{s=jw}', xy=(0, 0), xytext=(1.5, -2.5),
            fontsize=9, color='blue',
            arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))

# 信号 e^{2t}u(t) 极点 s=2, ROC sigma>2 (不包含 jw 轴)
ax.fill_between([2, 5], [-5, -5], [5, 5], alpha=0.1, color='red', hatch='///')
ax.plot(2, 0, 'rx', markersize=10, markeredgewidth=2)
ax.text(3.5, -4, 'e^{2t}u(t):\nROC sigma>2\n不含 jw 轴\n-> FT 不存在!', fontsize=8, ha='center', color='darkred',
        bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))

# ===== (d) ROC 形状总览 =====
ax = axes[1, 1]
ax.set_xlim(-6, 6); ax.set_ylim(-5, 5)
ax.axhline(y=0, color='gray', linewidth=1); ax.axvline(x=0, color='gray', linewidth=1)
ax.set_xlabel('sigma'); ax.set_ylabel('j*omega')
ax.set_title('四种信号类型的 ROC 形状', fontsize=12)
ax.text(0, -5.5, '因果: sigma > a   |   反因果: sigma < b   |   双边: a<sigma<b   |   有限长: 全平面(除0,inf)',
        ha='center', fontsize=8, transform=ax.transData)

# 因果信号 ROC (右半平面)
ax.fill_between([1, 6], [-5, -5], [5, 5], alpha=0.15, color='blue')
ax.plot(1, 0, 'bx', markersize=10)
ax.text(3.5, 3, '因果\nsigma>a', fontsize=9, ha='center', color='blue')

# 反因果信号 ROC (左半平面)
ax.fill_between([-6, -1], [-5, -5], [5, 5], alpha=0.15, color='purple')
ax.plot(-1, 0, 'x', color='purple', markersize=10)
ax.text(-3.5, 3, '反因果\nsigma<b', fontsize=9, ha='center', color='purple')

# 双边信号 ROC (带状)
ax.fill_between([-2, 1], [-5, -5], [5, 5], alpha=0.25, color='orange')
ax.plot(-2, 0, 'x', color='darkorange', markersize=10)
ax.plot(1, 0, 'x', color='darkorange', markersize=10)
ax.text(-0.5, 1.5, '双边\na<sigma<b', fontsize=9, ha='center', color='darkorange')

# 有限长 (全平面)
ax.text(0, -3, '有限长: 全平面', fontsize=9, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

fig.suptitle('ROC (收敛域) 详解: 什么是 ROC? 为什么需要它?', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('roc_explained.png', dpi=150, bbox_inches='tight')
print("Done! roc_explained.png saved.")
