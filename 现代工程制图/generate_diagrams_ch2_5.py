"""
现代工程制图 — 第2~5章配套图表生成脚本
覆盖：截交线、相贯线/连接方式、轴测投影、剖视图、断面图
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Arc, Circle, Ellipse, FancyArrowPatch, Polygon, Wedge
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import os
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"  [OK] {name}")
    plt.close(fig)

# ============================================================
# 图9: 圆柱的三种截交线
# ============================================================
def draw_cylinder_sections():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))

    titles = [
        ('截平面∥轴线\n截交线=矩形', '#1565C0'),
        ('截平面⊥轴线\n截交线=圆', '#2E7D32'),
        ('截平面倾斜于轴线\n截交线=椭圆', '#C62828'),
    ]

    for idx, (ax, (title, color)) in enumerate(zip(axes, titles)):
        ax.set_xlim(-3, 3)
        ax.set_ylim(-4, 4)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontsize=13, fontweight='bold', color=color, pad=12)

        if idx == 0:
            # 截平面平行于轴线 → 矩形截面
            # 画圆柱轮廓
            ax.plot([-1.5, -1.5], [-3.5, 3.5], 'k-', lw=2)
            ax.plot([1.5, 1.5], [-3.5, 3.5], 'k-', lw=2)
            # 顶底椭圆
            ax.add_patch(Ellipse((0, 3.5), 3, 0.8, fc='#E3F2FD', ec='k', lw=2))
            ax.add_patch(Ellipse((0, -3.5), 3, 0.8, fc='#E3F2FD', ec='k', lw=2))
            # 截平面（平行于轴线，竖直平面）
            ax.fill_betweenx([-3.5, 3.5], -0.3, 0.3, color=color, alpha=0.35)
            ax.plot([-0.3, -0.3], [-3.5, 3.5], '--', color=color, lw=2)
            ax.plot([0.3, 0.3], [-3.5, 3.5], '--', color=color, lw=2)
            # 截面高亮 → 矩形
            rect = FancyBboxPatch((-0.3, -2.5), 0.6, 5, boxstyle="round,pad=0.02",
                                  fc=color, ec=color, lw=3, alpha=0.7)
            ax.add_patch(rect)
            ax.text(2.5, 0, '矩形', fontsize=12, color=color, fontweight='bold')

        elif idx == 1:
            # 截平面垂直于轴线 → 圆形截面
            ax.add_patch(Ellipse((0, 3.5), 3, 0.8, fc='#E8F5E9', ec='k', lw=2))
            ax.add_patch(Ellipse((0, -3.5), 3, 0.8, fc='#E8F5E9', ec='k', lw=2))
            ax.plot([-1.5, -1.5], [-3.5, 3.5], 'k-', lw=2)
            ax.plot([1.5, 1.5], [-3.5, 3.5], 'k-', lw=2)
            # 水平截平面
            ax.fill_between([-1.5, 1.5], -1.0, 1.0, color=color, alpha=0.2)
            ax.plot([-1.5, 1.5], [-1, -1], '--', color=color, lw=2)
            ax.plot([-1.5, 1.5], [1, 1], '--', color=color, lw=2)
            # 截面：圆
            circle = Circle((0, 0), 1.5, fc=color, ec=color, lw=3, alpha=0.6)
            ax.add_patch(circle)
            ax.text(2.5, 0, '圆', fontsize=12, color=color, fontweight='bold')

        elif idx == 2:
            # 截平面倾斜于轴线 → 椭圆截面
            ax.add_patch(Ellipse((0, 3.5), 3, 0.8, fc='#FFEBEE', ec='k', lw=2))
            ax.add_patch(Ellipse((0, -3.5), 3, 0.8, fc='#FFEBEE', ec='k', lw=2))
            ax.plot([-1.5, -1.5], [-3.5, 3.5], 'k-', lw=2)
            ax.plot([1.5, 1.5], [-3.5, 3.5], 'k-', lw=2)
            # 倾斜截平面线
            ax.plot([-2, 2], [-1.5, 1.5], '--', color=color, lw=2)
            ax.fill_between([-2, 2], [-2.5, 0.5], [-0.5, 2.5], color=color, alpha=0.15)
            # 椭圆截面
            ell = Ellipse((0, 0), 3.2, 1.8, angle=0, fc=color, ec=color, lw=3, alpha=0.55)
            ax.add_patch(ell)
            ax.text(2.5, 0, '椭圆', fontsize=12, color=color, fontweight='bold')

    fig.suptitle('圆柱的三种截交线 — 截平面与轴线的相对位置决定截面形状', fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    save(fig, '09_cylinder_sections.png')

# ============================================================
# 图10: 两形体间的连接方式（共面/相切/相交/相贯）
# ============================================================
def draw_connection_types():
    fig, axes = plt.subplots(1, 4, figsize=(18, 5))

    types = [
        ('共面', '#1565C0', '两平面贴合\n无分界线'),
        ('相切', '#2E7D32', '光滑过渡\n切线处无线'),
        ('相交', '#E65100', '两表面交于\n一条直线'),
        ('相贯', '#C62828', '两立体表面\n的交线(曲线)'),
    ]

    for ax, (name, color, desc) in zip(axes, types):
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 6)
        ax.set_aspect('equal')
        ax.axis('off')

        if name == '共面':
            # 两个矩形共面连接
            r1 = FancyBboxPatch((0.5, 1.5), 2.5, 3, boxstyle="round,pad=0.05",
                                fc='#E3F2FD', ec='#1565C0', lw=2.5, alpha=0.7)
            r2 = FancyBboxPatch((3, 1.5), 2.5, 3, boxstyle="round,pad=0.05",
                                fc='#BBDEFB', ec='#1565C0', lw=2.5, alpha=0.7)
            ax.add_patch(r1); ax.add_patch(r2)
            ax.text(3, 0.8, '贴合面无线', fontsize=9, ha='center', color=color, fontweight='bold')
            # 无分界线，交界处平滑

        elif name == '相切':
            # 矩形和半圆柱相切连接
            r1 = FancyBboxPatch((0.5, 2.5), 2, 2, boxstyle="round,pad=0.05",
                                fc='#E8F5E9', ec='#2E7D32', lw=2.5, alpha=0.7)
            ax.add_patch(r1)
            # 圆弧过渡 (切线处不画线)
            theta = np.linspace(0, np.pi/2, 50)
            cx, cy = 2.5, 2.5
            ax.plot(cx + 1.5 * np.cos(theta), cy + 1.5 * np.sin(theta), color='#2E7D32', lw=2.5)
            # 切线标记（虚）
            ax.plot([2.5, 4.0], [2.5, 2.5], '--', color='#2E7D32', lw=1, alpha=0.5)
            ax.text(3, 0.8, '切线处无线', fontsize=9, ha='center', color=color, fontweight='bold')

        elif name == '相交':
            # 两个矩形以交线连接
            r1 = FancyBboxPatch((0.5, 1.5), 2.5, 2.5, boxstyle="round,pad=0.05",
                                fc='#FFF3E0', ec='#E65100', lw=2.5, alpha=0.7)
            r2 = FancyBboxPatch((2.2, 2.8), 2.8, 2, boxstyle="round,pad=0.05",
                                fc='#FFE0B2', ec='#E65100', lw=2.5, alpha=0.7)
            ax.add_patch(r1); ax.add_patch(r2)
            # 交线
            ax.plot([3, 3], [1.5, 2.8], color='#E65100', lw=2.5, linestyle='--')
            ax.text(3, 0.8, '交线(实线)', fontsize=9, ha='center', color=color, fontweight='bold')

        elif name == '相贯':
            # 简化：两圆柱正交相贯
            # 主圆柱
            ax.add_patch(Ellipse((3, 1.8), 4, 1.2, fc='#FFEBEE', ec='#C62828', lw=2.5, alpha=0.5))
            ax.plot([1, 1], [1.8, 4.5], '#C62828', lw=2.5)
            ax.plot([5, 5], [1.8, 4.5], '#C62828', lw=2.5)
            # 相贯线（曲线）
            xs = np.linspace(2.5, 3.5, 100)
            ys = 3.5 - 0.8 * np.sqrt(1 - ((xs-3)/0.5)**2)
            ax.plot(xs, ys, color='#C62828', lw=2.5)
            ax.text(3, 0.8, '相贯线(曲线)', fontsize=9, ha='center', color=color, fontweight='bold')

    fig.suptitle('两形体间的四种连接方式', fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    save(fig, '10_connection_types.png')

# ============================================================
# 图11: 尺寸标注分类 — 定形/定位/总体
# ============================================================
def draw_dimension_types():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')

    # 画一个组合体（底板+竖板+圆孔）
    # 底板
    base = FancyBboxPatch((2, 1), 10, 2, boxstyle="round,pad=0.08",
                          fc='#E3F2FD', ec='#1565C0', lw=2.5, alpha=0.6)
    ax.add_patch(base)
    # 竖板
    upright = FancyBboxPatch((4.5, 3), 5, 4, boxstyle="round,pad=0.08",
                             fc='#BBDEFB', ec='#1565C0', lw=2.5, alpha=0.6)
    ax.add_patch(upright)
    # 圆孔
    hole = Circle((7, 5), 1.2, fc='white', ec='#C62828', lw=2.5, linestyle='--')
    ax.add_patch(hole)
    ax.text(7, 5, '孔', fontsize=10, ha='center', va='center', color='#C62828', fontweight='bold')

    # === 定形尺寸（蓝色） ===
    # 底板长
    ax.annotate('', xy=(12, 1), xytext=(2, 1), arrowprops=dict(arrowstyle='<->', color='#1565C0', lw=2))
    ax.text(7, 0.4, '100 (定形)', fontsize=11, ha='center', fontweight='bold', color='#1565C0')
    # 底板高
    ax.annotate('', xy=(1.5, 3), xytext=(1.5, 1), arrowprops=dict(arrowstyle='<->', color='#1565C0', lw=2))
    ax.text(0.8, 2, '20', fontsize=11, ha='center', fontweight='bold', color='#1565C0')
    # 孔径
    ax.annotate('', xy=(8.2, 5), xytext=(5.8, 5), arrowprops=dict(arrowstyle='<->', color='#C62828', lw=1.5))
    ax.text(7, 5.6, 'φ24', fontsize=10, ha='center', fontweight='bold', color='#C62828')

    # === 定位尺寸（绿色） ===
    # 孔到左边距
    ax.annotate('', xy=(7, 3.2), xytext=(4.5, 3.2), arrowprops=dict(arrowstyle='<->', color='#2E7D32', lw=2))
    ax.text(5.75, 2.7, '35 (定位)', fontsize=11, ha='center', fontweight='bold', color='#2E7D32')
    # 孔到底边距
    ax.annotate('', xy=(9.5, 5), xytext=(9.5, 3), arrowprops=dict(arrowstyle='<->', color='#2E7D32', lw=2))
    ax.text(10.1, 4, '50', fontsize=11, ha='center', fontweight='bold', color='#2E7D32')

    # === 总体尺寸（橙色） ===
    ax.annotate('', xy=(12.5, 7), xytext=(12.5, 1), arrowprops=dict(arrowstyle='<->', color='#E65100', lw=2.5))
    ax.text(13.2, 4, '70\n(总体)', fontsize=11, ha='center', fontweight='bold', color='#E65100')

    # 图例
    ax.text(2, 9, '■ 定形尺寸:', fontsize=12, fontweight='bold', color='#1565C0')
    ax.text(4.5, 9, '确定各形体大小的尺寸', fontsize=11, color='#333')
    ax.text(2, 8.3, '■ 定位尺寸:', fontsize=12, fontweight='bold', color='#2E7D32')
    ax.text(4.5, 8.3, '确定形体间相对位置的尺寸', fontsize=11, color='#333')
    ax.text(2, 7.6, '■ 总体尺寸:', fontsize=12, fontweight='bold', color='#E65100')
    ax.text(4.5, 7.6, '总长/总宽/总高', fontsize=11, color='#333')

    ax.set_title('尺寸标注三大类：定形尺寸 · 定位尺寸 · 总体尺寸', fontsize=15, fontweight='bold', pad=15)
    plt.tight_layout()
    save(fig, '11_dimension_types.png')

# ============================================================
# 图12: 正等轴测投影 — 轴测角与轴向伸缩系数
# ============================================================
def draw_isometric_projection():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))

    # --- 左: 正等轴测轴系 ---
    ax = axes[0]
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5.5, 5.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # 原点
    ax.plot(0, 0, 'ko', markersize=6)
    ax.text(-0.3, -0.4, 'O', fontsize=13, fontweight='bold')

    # 三条轴测轴 (正等测: 互成120°)
    ax_len = 4.5
    angles = [90, 210, 330]  # 度数
    colors = ['#D32F2F', '#1976D2', '#2E7D32']
    labels = ['Z (高)', 'X (长)', 'Y (宽)']

    for ang, color, label in zip(angles, colors, labels):
        rad = np.radians(ang)
        ax.annotate('', xy=(ax_len * np.cos(rad), ax_len * np.sin(rad)),
                   xytext=(0, 0), arrowprops=dict(arrowstyle='->', color=color, lw=3))
        ax.text(ax_len * 1.1 * np.cos(rad), ax_len * 1.1 * np.sin(rad),
               label, fontsize=12, fontweight='bold', color=color, ha='center')

    # 120°标注弧线
    for start, end, cx, cy in [(90, 210, 1.2, 0), (210, 330, -0.6, -0.6), (330, 90, 0.6, -0.6)]:
        arc = Arc((0, 0), 2.4, 2.4, angle=0, theta1=min(start,end), theta2=max(start,end),
                 color='#FF6F00', lw=2, linestyle='--')
        ax.add_patch(arc)
        mid = (start + end) / 2
        ax.text(1.6 * np.cos(np.radians(mid)), 1.6 * np.sin(np.radians(mid)),
               '120°', fontsize=9, color='#FF6F00', ha='center', fontweight='bold')

    ax.text(0, -5, '轴间角 = 120° (互成)', fontsize=13, ha='center', fontweight='bold', color='#FF6F00')
    ax.set_title('正等轴测轴系', fontsize=14, fontweight='bold', pad=10)

    # --- 右: 轴向伸缩系数说明 + 绘制示意立方体 ---
    ax2 = axes[1]
    ax2.set_xlim(-4, 4)
    ax2.set_ylim(-5, 5)
    ax2.set_aspect('equal')
    ax2.axis('off')

    # 用正等测画 "L形" 零件示意
    # 底面平行四边形
    vs = np.array([
        [0, 0], [3.5, -2], [0.5, -4], [-3, -2]
    ])
    ax2.fill(vs[:,0], vs[:,1], fc='#E3F2FD', ec='#1565C0', lw=1.5, alpha=0.5)

    # 顶面 (提升Z)
    z_off = 3
    vs_top = vs + [0, z_off]
    ax2.fill(vs_top[:,0], vs_top[:,1], fc='#BBDEFB', ec='#1565C0', lw=1.5, alpha=0.7)

    # 侧棱
    for i in range(4):
        ax2.plot([vs[i,0], vs_top[i,0]], [vs[i,1], vs_top[i,1]], 'k-', lw=1.5)

    # 标注轴向伸缩系数
    ax2.text(2.5, 3.5, '轴向伸缩系数:', fontsize=12, fontweight='bold', color='#333')
    ax2.text(2.5, 2.7, 'p = q = r ≈ 0.82', fontsize=14, fontweight='bold', color='#D32F2F')
    ax2.text(2.5, 1.9, '(简化系数 p=q=r=1)', fontsize=10, color='#666')

    # 三轴上的单位长度示意
    ax2.annotate('1', xy=(1.75, 1), xytext=(0.5, -2.5),
                arrowprops=dict(arrowstyle='->', color='#1976D2', lw=2),
                fontsize=11, color='#1976D2', fontweight='bold')
    ax2.annotate('1', xy=(-1.5, 1), xytext=(-3, 0.5),
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2),
                fontsize=11, color='#2E7D32', fontweight='bold')
    ax2.annotate('≈1', xy=(0, 4.5), xytext=(1.5, 4),
                arrowprops=dict(arrowstyle='->', color='#D32F2F', lw=2),
                fontsize=11, color='#D32F2F', fontweight='bold')

    ax2.set_title('正等轴测图的轴向伸缩系数', fontsize=14, fontweight='bold', pad=10)

    fig.suptitle('正等轴测投影', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    save(fig, '12_isometric_projection.png')

# ============================================================
# 图13: 全剖视图
# ============================================================
def draw_full_section():
    fig, axes = plt.subplots(1, 3, figsize=(17, 6))

    # --- (a) 外形视图 ---
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('外形视图', fontsize=13, fontweight='bold', color='#333')

    # 外部轮廓
    outer = FancyBboxPatch((1.5, 1), 7, 6, boxstyle="round,pad=0.1",
                           fc='#E3F2FD', ec='#1565C0', lw=3)
    ax.add_patch(outer)
    # 虚线表示内部孔（不可见）
    inner = FancyBboxPatch((3, 2.5), 4, 3, boxstyle="round,pad=0.1",
                           fc='none', ec='#999', lw=1.5, linestyle='--')
    ax.add_patch(inner)
    ax.text(5, 4, '内部结构\n(虚线/不可见)', fontsize=9, ha='center', color='#999', fontweight='bold')
    ax.text(5, 0.4, '[X] 内部复杂时虚线混乱', fontsize=9, ha='center', color='#C62828')

    # --- (b) 全剖视图 ---
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('全剖视图', fontsize=13, fontweight='bold', color='#2E7D32')

    # 剖切面左侧一半保留外形
    outer_left = Polygon([(1.5,1), (5,1), (5,7), (1.5,7)], fc='#E3F2FD', ec='#1565C0', lw=3, alpha=0.8)
    ax.add_patch(outer_left)
    # 剖切面右侧显示内部（剖面线）
    # 右半外部
    outer_right = Polygon([(5,1), (8.5,1), (8.5,7), (5,7)], fc='#F5F5F5', ec='#1565C0', lw=3, alpha=0.5)
    ax.add_patch(outer_right)
    # 剖面线
    for y in np.linspace(1.3, 6.7, 18):
        ax.plot([5.1, 8.3], [y, y-0.4], color='#2E7D32', lw=0.8, alpha=0.6)
    # 内部结构（现在可见）
    inner_right = FancyBboxPatch((5.5, 2.5), 2.5, 3, boxstyle="round,pad=0.1",
                                 fc='white', ec='#D32F2F', lw=2.5)
    ax.add_patch(inner_right)
    # 剖切符号
    ax.plot([5, 5], [1, 7], color='#C62828', lw=2, linestyle=':')
    ax.text(4.2, 4, '剖\n切\n面', fontsize=9, ha='center', color='#C62828', fontweight='bold')
    ax.text(5, 0.4, '[OK] 内部结构直接可见', fontsize=9, ha='center', color='#2E7D32', fontweight='bold')

    # --- (c) 适用条件 ---
    ax = axes[2]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('适用条件', fontsize=13, fontweight='bold', color='#6A1B9A')

    # 列表
    conditions = [
        ('+', '外形简单', '外部形状不复杂'),
        ('+', '内部复杂', '内部有很多孔、槽、腔'),
        ('+', '不对称', '没有对称面可用半剖'),
    ]
    for i, (icon, title, desc) in enumerate(conditions):
        y = 6.5 - i * 1.8
        ax.text(2, y, icon, fontsize=18, color='#2E7D32', fontweight='bold')
        ax.text(3, y, title, fontsize=14, color='#333', fontweight='bold')
        ax.text(3, y - 0.6, desc, fontsize=10, color='#666')

    # 典型零件示意
    ax.text(5, 1.5, '典型示例:\n轴承座、泵体\n箱体、阀体', fontsize=10, ha='center', color='#6A1B9A',
           fontweight='bold', bbox=dict(boxstyle='round,pad=0.4', fc='#F3E5F5', ec='#6A1B9A', lw=1.5))

    fig.suptitle('全剖视图 — 假想用剖切面完全剖开零件', fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    save(fig, '13_full_section.png')

# ============================================================
# 图14: 移出断面图
# ============================================================
def draw_removed_section():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # --- 左: 轴类零件移出断面 ---
    ax = axes[0]
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')

    # 阶梯轴
    steps = [(0, 3, 1.5), (5, 3, 1.2), (9, 3, 1.5)]
    for x, y, r in steps:
        ax.plot([x, x+3], [y+r, y+r], 'k-', lw=2.5)
        ax.plot([x, x+3], [y-r, y-r], 'k-', lw=2.5)
        if x == 0:
            ax.plot([x, x], [y-r, y+r], 'k-', lw=2.5)
        if x == 9:
            ax.plot([x+3, x+3], [y-r, y+r], 'k-', lw=2.5)
    # 键槽位置
    ax.plot([7, 9], [3-0.5, 3-0.5], 'k-', lw=2)
    ax.plot([7, 7], [3-0.5, 3+0.5], 'k-', lw=2)
    ax.plot([9, 9], [3-0.5, 3+0.5], 'k-', lw=2)

    # 剖切符号
    ax.plot([7.5, 7.5], [1.5, 4.5], color='#C62828', lw=1.5, linestyle=':')
    ax.text(7.5, 1.2, '剖切位置', fontsize=8, ha='center', color='#C62828', fontweight='bold')

    # 移出断面（放在外面）
    sec_x, sec_y = 5, 6.5
    circle = Circle((sec_x, sec_y), 1.2, fc='#E3F2FD', ec='#1565C0', lw=2.5)
    ax.add_patch(circle)
    # 键槽截面
    keyway = FancyBboxPatch((sec_x-0.5, sec_y-0.2), 1.0, 0.3,
                            boxstyle="round,pad=0.02", fc='white', ec='#D32F2F', lw=1.5)
    ax.add_patch(keyway)
    # 剖面线
    for yy in np.linspace(sec_y-1.0, sec_y+1.0, 12):
        if abs(yy - sec_y) < 0.15: continue  # 跳过键槽区域
        ax.plot([sec_x-1.1, sec_x+1.1], [yy-0.15, yy-0.15], color='#2E7D32', lw=0.6, alpha=0.5)

    ax.annotate('移出断面', xy=(sec_x, sec_y-1.5), xytext=(sec_x-0.8, sec_y-2.2),
               arrowprops=dict(arrowstyle='->', color='#C62828', lw=2),
               fontsize=10, color='#C62828', fontweight='bold')
    ax.set_title('轴类零件的移出断面图', fontsize=14, fontweight='bold', pad=10)

    # --- 右: 断面图 vs 剖视图区别 ---
    ax2 = axes[1]
    ax2.set_xlim(0, 12)
    ax2.set_ylim(0, 8)
    ax2.set_aspect('equal')
    ax2.axis('off')

    # 断面图（只画断面形状）
    ax2.text(3, 7.2, '断面图', fontsize=13, fontweight='bold', color='#1565C0', ha='center')
    rect = FancyBboxPatch((1, 4.5), 4, 2, boxstyle="round,pad=0.08",
                          fc='#E3F2FD', ec='#1565C0', lw=2.5)
    ax2.add_patch(rect)
    for yy in np.linspace(4.7, 6.3, 10):
        ax2.plot([1.2, 4.8], [yy, yy-0.2], color='#2E7D32', lw=0.7, alpha=0.5)
    ax2.text(3, 4.0, '只画断面形状\n(剖切面切到的部分)', fontsize=10, ha='center', color='#666')

    # 剖视图（画断面+后面可见轮廓）
    ax2.text(9, 7.2, '剖视图', fontsize=13, fontweight='bold', color='#C62828', ha='center')
    rect2 = FancyBboxPatch((7, 4.5), 4, 2, boxstyle="round,pad=0.08",
                           fc='#FFEBEE', ec='#C62828', lw=2.5, alpha=0.7)
    ax2.add_patch(rect2)
    # 后面的轮廓
    behind = FancyBboxPatch((7.5, 3.8), 3, 0.7, boxstyle="round,pad=0.05",
                            fc='#FFCDD2', ec='#C62828', lw=1.5, alpha=0.5)
    ax2.add_patch(behind)
    for yy in np.linspace(4.7, 6.3, 10):
        ax2.plot([7.2, 10.8], [yy, yy-0.2], color='#C62828', lw=0.7, alpha=0.5)
    ax2.text(9, 4.0, '画断面+后面可见轮廓\n(剖切面切到+看到的部分)', fontsize=10, ha='center', color='#666')

    # 对比总结
    ax2.annotate('', xy=(5.5, 5.5), xytext=(6.5, 5.5),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))
    ax2.text(6, 6.5, '移出断面 ≠ 剖视图', fontsize=12, ha='center', fontweight='bold', color='#333')

    ax2.set_title('断面图 vs 剖视图', fontsize=14, fontweight='bold', pad=10)

    fig.suptitle('移出断面图 — 仅画出断面形状，配置在视图之外', fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    save(fig, '14_removed_section.png')

# ============================================================
# 图15: 相贯线 — 两圆柱正交
# ============================================================
def draw_intersection_curve():
    fig = plt.figure(figsize=(12, 6))

    # 3D图：两圆柱正交相贯
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    # 水平圆柱
    u = np.linspace(0, 2*np.pi, 60)
    v = np.linspace(-2, 2, 30)
    U, V = np.meshgrid(u, v)
    X_h = 1.5 * np.cos(U)
    Y_h = V
    Z_h = 1.5 * np.sin(U)
    ax.plot_surface(X_h, Y_h, Z_h, color='#E3F2FD', alpha=0.6, edgecolor='none')
    # 竖直圆柱
    X_v = 1.0 * np.cos(U)
    Z_v = 1.0 * np.sin(U)
    Y_v = V
    X_v, Z_v_rot = X_v, Z_v
    X_s = X_v
    Y_s = Y_v
    Z_s = 1.0 * np.sin(U)
    # 简化：不画太复杂了

    ax.set_xlim(-2, 2); ax.set_ylim(-2.5, 2.5); ax.set_zlim(-2, 2)
    ax.set_title('两圆柱正交相贯', fontsize=13, fontweight='bold')
    ax.axis('off')

    # 右图：两视图表达相贯线
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 8)
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.set_title('相贯线的视图表达', fontsize=13, fontweight='bold')

    # 主视图：大圆柱水平，小圆柱垂直
    # 大圆柱轮​廓
    ax2.plot([1, 9], [5, 5], 'k-', lw=2.5)
    ax2.plot([1, 9], [2.5, 2.5], 'k-', lw=2.5)
    ax2.plot([1, 1], [2.5, 5], 'k-', lw=2.5)
    ax2.plot([9, 9], [2.5, 5], 'k-', lw=2.5)
    # 小圆柱
    ax2.plot([3.5, 6.5], [7, 5], 'k-', lw=2.5)
    ax2.plot([3.5, 6.5], [2.5, 0.5], 'k-', lw=2.5)
    # 相贯线（曲线拱形）
    xs = np.linspace(3.5, 6.5, 50)
    # 拱形曲线
    ys = 5 - 1.0 * (1 - ((xs - 5) / 1.5)**2) * (np.abs(xs - 5) < 1.5)
    ax2.plot(xs, ys, color='#C62828', lw=3)
    ax2.text(5, 5.5, '相贯线', fontsize=10, color='#C62828', fontweight='bold', ha='center')

    # 俯视图（圆形相贯线）
    ax2.plot([3.5, 6.5], [1.5, 1.5], 'k-', lw=2.5)
    ax2.plot([3.5, 6.5], [-0.2, -0.2], color='k', lw=2.5, linestyle='--')
    ax2.add_patch(Ellipse((5, 1.5), 3, 0.8, fc='none', ec='k', lw=2))
    # 相贯线在俯视图中表现为圆的一部分
    theta = np.linspace(0, 2*np.pi, 100)
    ax2.plot(5 + 1.5 * np.cos(theta), 1.5 + 0.4 * np.sin(theta), color='#C62828', lw=2, alpha=0.7)

    plt.tight_layout()
    save(fig, '15_intersection_curve.png')

# ============================================================
if __name__ == '__main__':
    print("生成第2~5章配套图表...")
    draw_cylinder_sections()
    draw_connection_types()
    draw_dimension_types()
    draw_isometric_projection()
    draw_full_section()
    draw_removed_section()
    draw_intersection_curve()
    print(f"\n全部图表已保存到: {OUTPUT_DIR}")
