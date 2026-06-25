"""
概率论教程配套图表生成脚本
所有图用 matplotlib + numpy 生成，中文字体支持
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.font_manager as fm
from matplotlib.patches import Circle, Rectangle
import os

# 字体设置：优先用 Noto Sans SC（Google 出品，同时完美支持中文和拉丁字符）
# 其次 Microsoft YaHei，再 SimHei
_fonts_available = [f.name for f in fm.fontManager.ttflist]
if 'Noto Sans SC' in _fonts_available:
    matplotlib.rcParams['font.sans-serif'] = ['Noto Sans SC']
elif 'Microsoft YaHei' in _fonts_available:
    matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
elif 'SimHei' in _fonts_available:
    matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
else:
    matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
# 禁用 monospace 字体回退到 DejaVu Sans Mono（它没有中文），统一用 sans-serif
matplotlib.rcParams['font.monospace'] = matplotlib.rcParams['font.sans-serif']

print(f"Using font: {matplotlib.rcParams['font.sans-serif']}")

output_dir = 'images'
os.makedirs(output_dir, exist_ok=True)

# ============================================================
# 图1: 集合关系图 — 事件运算的文氏图
# ============================================================
def draw_venn_diagrams():
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    axes = axes.flatten()

    titles = [
        '(a) A ⊂ B (A 包含于 B)',
        '(b) A 与 B 互不相容',
        '(c) A ∪ B (A 与 B 的并)',
        '(d) A ∩ B (A 与 B 的交)',
        '(e) A − B (A 与 B 的差)',
        '(f) Ā (A 的对立事件)'
    ]

    # 统一画布参数
    for i, (ax, title) in enumerate(zip(axes, titles)):
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontsize=11, pad=5)

        # 样本空间 Ω 用浅灰大矩形
        rect = Rectangle((-1.8, -1.8), 3.6, 3.6, fill=True,
                         facecolor='#f0f0f0', edgecolor='gray',
                         linewidth=1, linestyle='--')
        ax.add_patch(rect)
        ax.text(1.5, 1.5, 'Ω', fontsize=9, color='gray')

        if i == 0:  # A ⊂ B
            circle_B = Circle((0, 0), 1.2, fill=True, facecolor='lightblue', edgecolor='blue', linewidth=2, alpha=0.5)
            circle_A = Circle((0, 0), 0.6, fill=True, facecolor='lightcoral', edgecolor='red', linewidth=2, alpha=0.6)
            ax.add_patch(circle_B)
            ax.add_patch(circle_A)
            ax.text(0, 0, 'A', fontsize=11, fontweight='bold')
            ax.text(0, 1.05, 'B', fontsize=11, fontweight='bold', color='blue')

        elif i == 1:  # 互不相容
            circle_A = Circle((-0.6, 0), 0.8, fill=True, facecolor='lightcoral', edgecolor='red', linewidth=2, alpha=0.6)
            circle_B = Circle((0.6, 0), 0.8, fill=True, facecolor='lightblue', edgecolor='blue', linewidth=2, alpha=0.5)
            ax.add_patch(circle_A)
            ax.add_patch(circle_B)
            ax.text(-0.6, 0, 'A', fontsize=11, fontweight='bold')
            ax.text(0.6, 0, 'B', fontsize=11, fontweight='bold')

        elif i == 2:  # A ∪ B
            circle_A = Circle((-0.4, 0), 0.9, fill=True, facecolor='lightcoral', edgecolor='red', linewidth=2, alpha=0.5)
            circle_B = Circle((0.4, 0), 0.9, fill=True, facecolor='lightblue', edgecolor='blue', linewidth=2, alpha=0.5)
            ax.add_patch(circle_A)
            ax.add_patch(circle_B)
            ax.text(-0.55, 0.3, 'A', fontsize=11, fontweight='bold')
            ax.text(0.55, 0.3, 'B', fontsize=11, fontweight='bold')

        elif i == 3:  # A ∩ B
            circle_A = Circle((-0.4, 0), 0.9, fill=True, facecolor='lightcoral', edgecolor='red', linewidth=2, alpha=0.3)
            circle_B = Circle((0.4, 0), 0.9, fill=True, facecolor='lightblue', edgecolor='blue', linewidth=2, alpha=0.3)
            ax.add_patch(circle_A)
            ax.add_patch(circle_B)
            # 交集区域高亮
            intersection = Circle((-0.4, 0), 0.9, fill=False, edgecolor='none')
            ax.text(0, 0, 'A∩B', fontsize=9, fontweight='bold', ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8))
            ax.text(-0.6, 0.3, 'A', fontsize=11, fontweight='bold')
            ax.text(0.6, 0.3, 'B', fontsize=11, fontweight='bold')

        elif i == 4:  # A - B
            circle_A = Circle((-0.3, 0), 0.9, fill=True, facecolor='lightcoral', edgecolor='red', linewidth=2, alpha=0.4)
            circle_B = Circle((0.3, 0), 0.9, fill=True, facecolor='lightblue', edgecolor='blue', linewidth=2, alpha=0.3)
            ax.add_patch(circle_A)
            ax.add_patch(circle_B)
            ax.text(-0.55, 0, 'A−B', fontsize=9, fontweight='bold', ha='center',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8))
            ax.text(0.55, 0.35, 'B', fontsize=11, fontweight='bold')

        elif i == 5:  # 对立事件
            circle_A = Circle((0, 0), 0.9, fill=True, facecolor='lightcoral', edgecolor='red', linewidth=2, alpha=0.5)
            ax.add_patch(circle_A)
            ax.text(0, 0, 'A', fontsize=11, fontweight='bold')
            ax.text(1.4, 0, 'Ā', fontsize=11, fontweight='bold', color='darkgreen')
            ax.annotate('', xy=(1.3, -0.2), xytext=(0.7, -0.5),
                       arrowprops=dict(arrowstyle='->', color='darkgreen', lw=1.5))

    plt.tight_layout()
    plt.savefig(f'{output_dir}/01_venn_diagrams.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Done: 01_venn_diagrams.png")


# ============================================================
# 图2: 生日悖论可视化
# ============================================================
def draw_birthday_paradox():
    n_vals = np.arange(1, 101)
    probs = np.ones(100)
    for i in range(2, 101):
        prod = 1.0
        for k in range(i):
            prod *= (365 - k) / 365
        probs[i-1] = 1 - prod

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(n_vals, probs, 'b-', linewidth=2)
    ax.axhline(y=0.5, color='red', linestyle='--', linewidth=1, alpha=0.7)
    ax.axvline(x=23, color='red', linestyle='--', linewidth=1, alpha=0.7)
    ax.plot(23, probs[22], 'ro', markersize=8)
    ax.annotate(f'n=23, P≈{probs[22]:.3f}', xy=(23, probs[22]),
                xytext=(35, 0.35), fontsize=10, color='red',
                arrowprops=dict(arrowstyle='->', color='red'))

    ax.axvline(x=60, color='green', linestyle='--', linewidth=1, alpha=0.7)
    ax.plot(60, probs[59], 'go', markersize=6)
    ax.annotate(f'n=60, P≈{probs[59]:.4f}', xy=(60, probs[59]),
                xytext=(70, 0.8), fontsize=10, color='green',
                arrowprops=dict(arrowstyle='->', color='green'))

    ax.set_xlabel('人数 n', fontsize=12)
    ax.set_ylabel('至少两人生日相同的概率 P(A)', fontsize=12)
    ax.set_title('生日问题：n 个人中至少两人生日相同的概率', fontsize=14)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/02_birthday_paradox.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Done: 02_birthday_paradox.png")


# ============================================================
# 图3: 全概率公式与贝叶斯公式 — 树状图
# ============================================================
def draw_probability_tree():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(-1, 11)
    ax.set_ylim(-4, 4)
    ax.axis('off')
    ax.set_title('全概率公式与贝叶斯公式 — 原因→结果 树状图\n(手机生产质检问题)', fontsize=14, pad=20)

    # 根节点
    ax.plot(0, 0, 'ko', markersize=8)
    ax.text(-0.6, 0.2, '开始', fontsize=11, fontweight='bold')

    # 第一层：两个生产基地
    # S市
    ax.plot([0, 4], [0, 2], 'b-', linewidth=2)
    ax.plot(4, 2, 'bo', markersize=10)
    ax.text(4.2, 2.2, 'S市生产 (A)', fontsize=11, fontweight='bold', color='blue')
    ax.text(4.2, 1.7, 'P(A)=0.6', fontsize=10, color='blue')

    # T市
    ax.plot([0, 4], [0, -2], 'g-', linewidth=2)
    ax.plot(4, -2, 'go', markersize=10)
    ax.text(4.2, -1.8, 'T市生产 (Ā)', fontsize=11, fontweight='bold', color='green')
    ax.text(4.2, -2.3, 'P(Ā)=0.4', fontsize=10, color='green')

    # 第二层：质检结果
    # S市 → 合格/不合格
    ax.plot([4, 8], [2, 2.8], 'b-', linewidth=1.5)
    ax.plot(8, 2.8, 'ro', markersize=8)
    ax.text(8.2, 3.0, '不合格 (B)', fontsize=10, color='red')
    ax.text(8.2, 2.5, 'P(B|A)=0.05', fontsize=9, color='red')

    ax.plot([4, 8], [2, 1.2], 'b-', linewidth=1.5)
    ax.plot(8, 1.2, 'go', markersize=8)
    ax.text(8.2, 1.4, '合格 (B̄)', fontsize=10, color='darkgreen')
    ax.text(8.2, 0.9, 'P(B̄|A)=0.95', fontsize=9, color='darkgreen')

    # T市 → 合格/不合格
    ax.plot([4, 8], [-2, -1.2], 'g-', linewidth=1.5)
    ax.plot(8, -1.2, 'ro', markersize=8)
    ax.text(8.2, -1.0, '不合格 (B)', fontsize=10, color='red')
    ax.text(8.2, -1.5, 'P(B|Ā)=0.10', fontsize=9, color='red')

    ax.plot([4, 8], [-2, -2.8], 'g-', linewidth=1.5)
    ax.plot(8, -2.8, 'go', markersize=8)
    ax.text(8.2, -2.6, '合格 (B̄)', fontsize=10, color='darkgreen')
    ax.text(8.2, -3.1, 'P(B̄|Ā)=0.90', fontsize=9, color='darkgreen')

    # 注释框
    ax.text(9.5, 0, '全概率公式:\nP(B) = P(A)P(B|A) + P(Ā)P(B|Ā)\n      = 0.6×0.05 + 0.4×0.10\n      = 0.07\n\n贝叶斯公式:\nP(A|B) = P(A)P(B|A)/P(B)\n      = 0.6×0.05/0.07\n      = 3/7 ≈ 0.429',
           fontsize=9, family='monospace',
           bbox=dict(boxstyle='round,pad=0.8', facecolor='lightyellow', edgecolor='orange', alpha=0.9))

    plt.tight_layout()
    plt.savefig(f'{output_dir}/03_probability_tree.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Done: 03_probability_tree.png")


# ============================================================
# 图4: 常见离散分布对比 (二项/泊松/几何)
# ============================================================
def draw_discrete_distributions():
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

    # 二项分布 B(20, 0.3)
    from math import comb as _comb
    def binom_pmf(k, n, p):
        """二项分布 B(n,p) 的概率质量函数"""
        return np.array([_comb(n, ki) * p**ki * (1-p)**(n-ki) for ki in k])
    def poisson_pmf(k, lam):
        """泊松分布 P(λ) 的概率质量函数"""
        from math import exp, factorial
        return np.array([exp(-lam) * lam**ki / factorial(ki) for ki in k])
    def geom_pmf(k, p):
        """几何分布 Ge(p) 的概率质量函数"""
        return p * (1-p)**(np.array(k)-1)

    n, p = 20, 0.3
    k_vals = np.arange(0, n+1)
    binom_pmf_arr = binom_pmf(k_vals, n, p)
    axes[0].bar(k_vals, binom_pmf_arr, color='steelblue', alpha=0.8, edgecolor='navy')
    axes[0].set_title(f'二项分布 B(n={n}, p={p})', fontsize=12)
    axes[0].set_xlabel('k (成功次数)', fontsize=10)
    axes[0].set_ylabel('P(X=k)', fontsize=10)
    axes[0].axvline(x=n*p, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    axes[0].text(n*p+0.5, max(binom_pmf_arr)*0.9, f'E(X)={n*p}', fontsize=9, color='red')

    # 泊松分布 P(λ=4)
    lam = 4
    k_vals2 = np.arange(0, 15)
    poisson_pmf_arr = poisson_pmf(k_vals2, lam)
    axes[1].bar(k_vals2, poisson_pmf_arr, color='darkorange', alpha=0.8, edgecolor='brown')
    axes[1].set_title(f'泊松分布 P(λ={lam})', fontsize=12)
    axes[1].set_xlabel('k', fontsize=10)
    axes[1].set_ylabel('P(X=k)', fontsize=10)
    axes[1].axvline(x=lam, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    axes[1].text(lam+0.3, max(poisson_pmf_arr)*0.9, f'E(X)={lam}', fontsize=9, color='red')

    # 几何分布 Ge(p=0.3)
    p_geom = 0.3
    k_vals3 = np.arange(1, 16)
    geom_pmf_arr = geom_pmf(k_vals3, p_geom)
    axes[2].bar(k_vals3, geom_pmf_arr, color='seagreen', alpha=0.8, edgecolor='darkgreen')
    axes[2].set_title(f'几何分布 Ge(p={p_geom})', fontsize=12)
    axes[2].set_xlabel('k (首次成功的试验次数)', fontsize=10)
    axes[2].set_ylabel('P(X=k)', fontsize=10)
    axes[2].axvline(x=1/p_geom, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    axes[2].text(1/p_geom+0.3, max(geom_pmf_arr)*0.9, f'E(X)≈{1/p_geom:.1f}', fontsize=9, color='red')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/04_discrete_distributions.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Done: 04_discrete_distributions.png")


# ============================================================
# 图5: 常见连续分布对比 (均匀/指数/正态)
# ============================================================
def draw_continuous_distributions():
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

    # 均匀分布 U(0, 1) 和 U(2, 5)
    x1 = np.linspace(-0.5, 6.5, 1000)
    u1 = np.where((x1 >= 0) & (x1 <= 1), 1.0, 0)
    u2 = np.where((x1 >= 2) & (x1 <= 5), 1/3, 0)
    axes[0].plot(x1, u1, 'b-', linewidth=2, label='U(0,1)')
    axes[0].plot(x1, u2, 'r-', linewidth=2, label='U(2,5)')
    axes[0].fill_between(x1, u1, alpha=0.3, color='blue')
    axes[0].fill_between(x1, u2, alpha=0.3, color='red')
    axes[0].set_title('均匀分布', fontsize=12)
    axes[0].set_xlabel('x', fontsize=10)
    axes[0].set_ylabel('f(x)', fontsize=10)
    axes[0].legend(fontsize=9)
    axes[0].set_ylim(0, 1.3)

    # 指数分布 Exp(λ)
    x2 = np.linspace(0, 8, 1000)
    for lam, color, label in [(0.5, 'blue', 'λ=0.5'), (1.0, 'red', 'λ=1.0'), (2.0, 'green', 'λ=2.0')]:
        axes[1].plot(x2, lam * np.exp(-lam * x2), linewidth=2, color=color, label=label)
    axes[1].set_title('指数分布 Exp(λ)', fontsize=12)
    axes[1].set_xlabel('x', fontsize=10)
    axes[1].set_ylabel('f(x)', fontsize=10)
    axes[1].legend(fontsize=9)

    # 正态分布 N(μ, σ²)
    x3 = np.linspace(-5, 8, 1000)
    for mu, sigma, color, label in [(0, 1, 'blue', 'N(0,1)'), (1, 1.5, 'red', 'N(1,1.5²)'), (-2, 0.5, 'green', 'N(-2,0.5²)')]:
        axes[2].plot(x3, 1/(sigma*np.sqrt(2*np.pi)) * np.exp(-(x3-mu)**2/(2*sigma**2)),
                    linewidth=2, color=color, label=label)
    axes[2].set_title('正态分布 N(μ, σ²)', fontsize=12)
    axes[2].set_xlabel('x', fontsize=10)
    axes[2].set_ylabel('f(x)', fontsize=10)
    axes[2].legend(fontsize=9)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/05_continuous_distributions.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Done: 05_continuous_distributions.png")


# ============================================================
# 图6: 正态分布的 1σ/2σ/3σ 规则
# ============================================================
def draw_normal_sigma():
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.linspace(-4, 4, 1000)
    y = 1/np.sqrt(2*np.pi) * np.exp(-x**2/2)

    ax.plot(x, y, 'b-', linewidth=2)
    ax.fill_between(x, y, alpha=0.15, color='blue')

    # 标出 1σ, 2σ, 3σ 区域
    for sigma, color, alpha_val in [(1, 'lightgreen', 0.35), (2, 'lightblue', 0.25), (3, 'lightcoral', 0.15)]:
        mask = (x >= -sigma) & (x <= sigma)
        ax.fill_between(x[mask], y[mask], alpha=alpha_val, color=color)

    # 标注概率
    from math import erf as _erf
    def std_norm_cdf(x):
        """标准正态分布的累积分布函数 (用误差函数 erfc)"""
        return 0.5 * (1 + _erf(x / np.sqrt(2)))
    for sigma, y_pos in [(1, 0.32), (2, 0.22), (3, 0.10)]:
        prob = std_norm_cdf(sigma) - std_norm_cdf(-sigma)
        ax.annotate(f'{sigma}σ: {prob*100:.1f}%', xy=(0, y_pos), fontsize=11, ha='center',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9))

    ax.set_xlabel('x (以 σ 为单位)', fontsize=12)
    ax.set_ylabel('φ(x)', fontsize=12)
    ax.set_title('标准正态分布 N(0,1) — 1σ/2σ/3σ 规则', fontsize=14)
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_xticklabels(['-3σ', '-2σ', '-1σ', '0', '1σ', '2σ', '3σ'])
    ax.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/06_normal_sigma.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Done: 06_normal_sigma.png")


# ============================================================
# 图7: 中心极限定理演示
# ============================================================
def draw_clt_demo():
    np.random.seed(42)
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))

    sample_sizes = [1, 2, 5, 10, 30, 100]
    n_samples = 10000

    for idx, (ax, size) in enumerate(zip(axes.flatten(), sample_sizes)):
        # 从均匀分布 U(0,1) 中取 size 个样本，求和/平均
        if size == 1:
            data = np.random.uniform(0, 1, n_samples)
        else:
            data = np.sum(np.random.uniform(0, 1, (n_samples, size)), axis=1) / size

        ax.hist(data, bins=50, density=True, color='steelblue', alpha=0.7, edgecolor='white')

        # 叠加理论正态曲线
        mu_theory = 0.5  # U(0,1) 的均值
        sigma_theory = np.sqrt(1/12 / size)  # Var = (b-a)²/12 / n
        x_curve = np.linspace(mu_theory - 4*sigma_theory, mu_theory + 4*sigma_theory, 200)
        y_curve = 1/(sigma_theory*np.sqrt(2*np.pi)) * np.exp(-(x_curve-mu_theory)**2/(2*sigma_theory**2))
        ax.plot(x_curve, y_curve, 'r-', linewidth=2, label='正态近似')

        ax.set_title(f'n = {size}', fontsize=12)
        ax.set_xlabel('样本均值', fontsize=9)
        if idx % 3 == 0:
            ax.set_ylabel('频率密度', fontsize=9)
        ax.legend(fontsize=8)

    fig.suptitle('中心极限定理演示：从 U(0,1) 中抽取不同样本量的均值分布', fontsize=14)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/07_clt_demo.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Done: 07_clt_demo.png")


# ============================================================
# 图8: 贝叶斯更新 — 疾病检测的先后验概率
# ============================================================
def draw_bayes_update():
    fig, ax = plt.subplots(figsize=(10, 5))

    stages = ['初始\n(先验)', '血液检查\n阳性后', '核磁共振\n确认后']
    probs = [0.001, 0.09, 0.98989]
    colors = ['gray', 'steelblue', 'darkgreen']

    bars = ax.bar(stages, probs, color=colors, alpha=0.8, edgecolor='black', width=0.5)

    # 在柱子上标注概率
    for bar, prob in zip(bars, probs):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03,
                f'{prob*100:.2f}%', ha='center', fontsize=13, fontweight='bold')

    ax.set_ylabel('患病的概率', fontsize=12)
    ax.set_title('贝叶斯更新：疾病检测中"患病概率"的逐步修正', fontsize=14)
    ax.set_ylim(0, 1.15)
    ax.grid(axis='y', alpha=0.3)

    # 添加连接箭头和说明
    ax.annotate('', xy=(1, 0.15), xytext=(0.3, 0.1),
               arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.text(0.65, 0.13, '贝叶斯\n更新', fontsize=9, color='red', ha='center')

    ax.annotate('', xy=(2, 1.05), xytext=(1.3, 0.2),
               arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.text(1.65, 0.6, '再次贝叶斯\n更新', fontsize=9, color='red', ha='center')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/08_bayes_update.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Done: 08_bayes_update.png")


# ============================================================
# 图9: 大数定律 — 抛硬币频率收敛
# ============================================================
def draw_law_of_large_numbers():
    np.random.seed(123)
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

    for idx, (ax, n_trials) in enumerate(zip(axes, [100, 1000, 10000])):
        flips = np.random.binomial(1, 0.5, n_trials)
        cumulative_avg = np.cumsum(flips) / np.arange(1, n_trials+1)

        ax.plot(range(1, n_trials+1), cumulative_avg, 'b-', linewidth=0.8, alpha=0.8)
        ax.axhline(y=0.5, color='red', linestyle='--', linewidth=1.5, alpha=0.8)
        ax.set_title(f'抛硬币 {n_trials} 次', fontsize=12)
        ax.set_xlabel('试验次数', fontsize=10)
        ax.set_ylabel('正面朝上的频率', fontsize=10)
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.2)

    fig.suptitle('大数定律演示：抛硬币频率收敛到真实概率 0.5', fontsize=14)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/09_lln_demo.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Done: 09_lln_demo.png")


# ============================================================
# 图10: 置信区间示意
# ============================================================
def draw_confidence_interval():
    np.random.seed(42)
    fig, ax = plt.subplots(figsize=(10, 8))

    # 生成100个样本，每个样本量为30，来自N(5, 1)
    n_intervals = 100
    n_sample = 30
    true_mean = 5.0
    alpha = 0.05

    means = []
    cis = []
    for _ in range(n_intervals):
        sample = np.random.normal(true_mean, 1, n_sample)
        xbar = np.mean(sample)
        se = 1 / np.sqrt(n_sample)  # σ=1 known
        z = 1.96  # 95% CI
        ci_low = xbar - z * se
        ci_high = xbar + z * se
        means.append(xbar)
        cis.append((ci_low, ci_high))

    # 绘制置信区间
    for i, (ci_low, ci_high) in enumerate(cis):
        if ci_low <= true_mean <= ci_high:
            color = 'steelblue'
            alpha_val = 0.6
        else:
            color = 'red'
            alpha_val = 0.9
        ax.plot([ci_low, ci_high], [i, i], color=color, linewidth=1.5, alpha=alpha_val)
        ax.plot(means[i], i, 'o', color=color, markersize=2, alpha=alpha_val)

    ax.axvline(x=true_mean, color='darkgreen', linestyle='--', linewidth=2, alpha=0.8)
    ax.text(true_mean + 0.02, n_intervals + 1, f'真实均值 μ={true_mean}', fontsize=11, color='darkgreen')

    # 统计覆盖比例
    coverage = sum(1 for ci_low, ci_high in cis if ci_low <= true_mean <= ci_high)
    ax.set_title(f'95% 置信区间模拟 (N=100个样本, 每个n=30)\n覆盖真实均值的区间: {coverage}/{n_intervals} ≈ {coverage/n_intervals*100:.0f}%',
                fontsize=13)
    ax.set_xlabel('μ 的估计值', fontsize=11)
    ax.set_ylabel('样本编号', fontsize=11)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/10_confidence_intervals.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Done: 10_confidence_intervals.png")


# ============================================================
# 图11: 假设检验 — 拒绝域示意
# ============================================================
def draw_hypothesis_test():
    fig, ax = plt.subplots(figsize=(10, 5))

    x = np.linspace(-4, 4, 1000)
    y = 1/np.sqrt(2*np.pi) * np.exp(-x**2/2)

    ax.plot(x, y, 'b-', linewidth=2)
    ax.fill_between(x, y, alpha=0.15, color='blue')

    # 拒绝域 (双侧, α=0.05)
    z_crit = 1.96
    mask_reject_left = x <= -z_crit
    mask_reject_right = x >= z_crit
    ax.fill_between(x[mask_reject_left], y[mask_reject_left], alpha=0.4, color='red')
    ax.fill_between(x[mask_reject_right], y[mask_reject_right], alpha=0.4, color='red')

    ax.text(-2.5, 0.15, '拒绝域\nα/2=2.5%', fontsize=10, color='red', ha='center')
    ax.text(2.5, 0.15, '拒绝域\nα/2=2.5%', fontsize=10, color='red', ha='center')
    ax.text(0, 0.25, '接受域\n95%', fontsize=11, ha='center', fontweight='bold')

    ax.set_xlabel('检验统计量 Z', fontsize=12)
    ax.set_ylabel('φ(z)', fontsize=12)
    ax.set_title('假设检验：双侧检验的拒绝域 (alpha=0.05, Z_crit=±1.96)', fontsize=14)
    ax.set_xticks([-1.96, 0, 1.96])
    ax.set_xticklabels(['-1.96', '0', '1.96'])
    ax.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/11_hypothesis_test.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Done: 11_hypothesis_test.png")


# ============================================================
# 图12: 二维正态分布 3D 曲面 + 等高线
# ============================================================
def draw_bivariate_normal():
    from matplotlib import cm

    fig = plt.figure(figsize=(14, 5))

    # 3D 曲面
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    x = np.linspace(-3, 3, 80)
    y = np.linspace(-3, 3, 80)
    X, Y = np.meshgrid(x, y)

    rho = 0.5
    Z = 1/(2*np.pi*np.sqrt(1-rho**2)) * np.exp(-(X**2 - 2*rho*X*Y + Y**2)/(2*(1-rho**2)))

    surf = ax1.plot_surface(X, Y, Z, cmap=cm.viridis, alpha=0.85, linewidth=0, antialiased=True)
    ax1.set_xlabel('X', fontsize=10)
    ax1.set_ylabel('Y', fontsize=10)
    ax1.set_zlabel('f(x,y)', fontsize=10)
    ax1.set_title('二维正态分布联合密度 N(0,0,1,1,0.5)', fontsize=11)

    # 等高线
    ax2 = fig.add_subplot(1, 2, 2)
    contour = ax2.contour(X, Y, Z, levels=12, cmap='viridis')
    ax2.clabel(contour, inline=True, fontsize=7)
    ax2.set_xlabel('X', fontsize=10)
    ax2.set_ylabel('Y', fontsize=10)
    ax2.set_title('等高线图 (ρ=0.5)', fontsize=11)
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/12_bivariate_normal.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Done: 12_bivariate_normal.png")


# ============================================================
# 图13: 相关系数示意 (正相关/负相关/不相关)
# ============================================================
def draw_correlation():
    np.random.seed(123)
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

    # 正相关
    mean = [0, 0]
    cov_pos = [[1, 0.8], [0.8, 1]]
    X_pos, Y_pos = np.random.multivariate_normal(mean, cov_pos, 200).T
    axes[0].scatter(X_pos, Y_pos, alpha=0.5, s=15, color='steelblue')
    axes[0].set_title(f'正相关 (ρ=0.8)\n协方差>0，同向变化', fontsize=11)
    axes[0].set_xlabel('X')
    axes[0].set_ylabel('Y')
    axes[0].axhline(y=0, color='gray', linestyle='--', alpha=0.3)
    axes[0].axvline(x=0, color='gray', linestyle='--', alpha=0.3)
    axes[0].set_aspect('equal')

    # 负相关
    cov_neg = [[1, -0.8], [-0.8, 1]]
    X_neg, Y_neg = np.random.multivariate_normal(mean, cov_neg, 200).T
    axes[1].scatter(X_neg, Y_neg, alpha=0.5, s=15, color='darkorange')
    axes[1].set_title(f'负相关 (ρ=-0.8)\n协方差<0，反向变化', fontsize=11)
    axes[1].set_xlabel('X')
    axes[1].set_ylabel('Y')
    axes[1].axhline(y=0, color='gray', linestyle='--', alpha=0.3)
    axes[1].axvline(x=0, color='gray', linestyle='--', alpha=0.3)
    axes[1].set_aspect('equal')

    # 不相关
    cov_zero = [[1, 0.0], [0.0, 1]]
    X_zero, Y_zero = np.random.multivariate_normal(mean, cov_zero, 200).T
    axes[2].scatter(X_zero, Y_zero, alpha=0.5, s=15, color='seagreen')
    axes[2].set_title(f'不相关 (ρ≈0)\n协方差≈0，没有线性关系', fontsize=11)
    axes[2].set_xlabel('X')
    axes[2].set_ylabel('Y')
    axes[2].axhline(y=0, color='gray', linestyle='--', alpha=0.3)
    axes[2].axvline(x=0, color='gray', linestyle='--', alpha=0.3)
    axes[2].set_aspect('equal')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/13_correlation.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Done: 13_correlation.png")


# ============================================================
# 运行所有
# ============================================================
if __name__ == '__main__':
    print("Generating probability theory diagrams...")
    draw_venn_diagrams()
    draw_birthday_paradox()
    draw_probability_tree()
    draw_discrete_distributions()
    draw_continuous_distributions()
    draw_normal_sigma()
    draw_clt_demo()
    draw_bayes_update()
    draw_law_of_large_numbers()
    draw_confidence_interval()
    draw_hypothesis_test()
    draw_bivariate_normal()
    draw_correlation()
    print("\n=== All diagrams generated! ===")
