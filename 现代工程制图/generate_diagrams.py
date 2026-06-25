"""
现代工程制图 — 第一章配套图表生成脚本
生成所有教程中使用的示意图
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Arc, FancyArrowPatch, Circle, Wedge
import numpy as np
import os
import sys

# 解决 Windows GBK 编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============ 中文字体设置 ============
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
# 图1: A系列图纸幅面对折关系
# ============================================================
def draw_paper_sizes():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # --- 左图: 嵌套矩形展示对折关系 ---
    ax = axes[0]
    ax.set_xlim(-5, 130)
    ax.set_ylim(-5, 100)
    ax.set_aspect('equal')
    ax.axis('off')

    papers = [
        ('A0', 0, 0, 118.9, 84.1, '#E3F2FD', '#1565C0'),
        ('A1', 0, 0, 84.1, 59.4, '#BBDEFB', '#1976D2'),
        ('A2', 0, 0, 59.4, 42.0, '#90CAF9', '#1E88E5'),
        ('A3', 0, 0, 42.0, 29.7, '#64B5F6', '#2196F3'),
        ('A4', 0, 0, 29.7, 21.0, '#42A5F5', '#1E88E5'),
    ]

    offset_x, offset_y = 2, 2
    for name, ox, oy, w, h, fc, ec in papers:
        rect = FancyBboxPatch((offset_x + ox, offset_y + oy), w, h,
                              boxstyle="round,pad=0.02", facecolor=fc, edgecolor=ec,
                              linewidth=2, alpha=0.7)
        ax.add_patch(rect)
        # 标注尺寸
        ax.text(offset_x + ox + w/2, offset_y + oy - 3.5, f'{name}  {h*10:.0f}×{w*10:.0f}',
                ha='center', va='top', fontsize=10, fontweight='bold', color=ec)

    # 对折箭头
    arrows = [
        (offset_x + 120, offset_y + 42, '对折 1 次', '#D32F2F'),
        (offset_x + 120, offset_y + 30, '对折 2 次', '#E64A19'),
        (offset_x + 120, offset_y + 21, '对折 3 次', '#F57C00'),
        (offset_x + 120, offset_y + 14, '对折 4 次', '#FFA000'),
    ]
    for x, y, txt, color in arrows:
        ax.annotate(txt, xy=(offset_x + 86, y), xytext=(x + 5, y + 5),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.5),
                    fontsize=9, color=color, fontweight='bold')

    ax.set_title('A系列幅面嵌套关系（等比例）', fontsize=14, fontweight='bold', pad=15)

    # --- 右图: 裁切次数与张数关系 ---
    ax2 = axes[1]
    cuts = [0, 1, 2, 3, 4]
    sheets = [2**n for n in cuts]  # [1, 2, 4, 8, 16]
    labels = ['A0\n(0次)', 'A1\n(1次)', 'A2\n(2次)', 'A3\n(3次)', 'A4\n(4次)']
    colors = ['#1565C0', '#1976D2', '#1E88E5', '#2196F3', '#42A5F5']

    bars = ax2.bar(labels, sheets, color=colors, edgecolor='white', linewidth=1.5, width=0.6)
    for bar, s in zip(bars, sheets):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{s} 张',
                ha='center', fontsize=12, fontweight='bold', color='#333')

    ax2.set_ylabel('张数', fontsize=12)
    ax2.set_title('裁切次数与张数：每裁 1 次翻 1 倍\n张数 = 2^n (n = 裁切次数)',
                   fontsize=13, fontweight='bold', pad=10)
    ax2.set_ylim(0, 20)
    ax2.grid(axis='y', alpha=0.3)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    fig.suptitle('图纸幅面的对折规律', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    save(fig, '01_paper_sizes.png')

# ============================================================
# 图2: 比例概念可视化
# ============================================================
def draw_scale_concept():
    fig, axes = plt.subplots(1, 4, figsize=(15, 4.5))

    # 实物参考: φ40 的圆
    real_diameter = 40  # mm

    scales = [
        ('1∶1\n原值比例', 1.0, '#4CAF50'),
        ('2∶1\n放大比例', 2.0, '#F44336'),
        ('1∶2\n缩小比例', 0.5, '#2196F3'),
        ('1∶5\n缩小比例', 0.2, '#FF9800'),
    ]

    for ax, (title, ratio, color) in zip(axes, scales):
        draw_diameter = real_diameter * ratio
        r = draw_diameter / 2

        # 画"图纸"背景
        ax.set_xlim(-30, 30)
        ax.set_ylim(-30, 30)
        ax.set_aspect('equal')

        # 实物淡色参考圈
        real_r = real_diameter / 2
        real_circle = Circle((0, 0), real_r, fill=False, edgecolor='#CCC',
                            linewidth=1.5, linestyle='--', alpha=0.6)
        ax.add_patch(real_circle)
        if ratio != 1.0:
            ax.text(real_r + 0.5, real_r + 0.5, '实物\nφ40', fontsize=7, color='#999', alpha=0.7)

        # 绘图尺寸的圆
        circle = Circle((0, 0), r, fill=True, facecolor=color, edgecolor='#333',
                       linewidth=2.5, alpha=0.35)
        ax.add_patch(circle)

        # 标注
        if draw_diameter > 0.5:
            ax.annotate('', xy=(r, 0), xytext=(-r, 0),
                       arrowprops=dict(arrowstyle='<->', color='#333', lw=2))
            ax.text(0, r + 2, f'绘图 φ{draw_diameter:.0f}', ha='center', fontsize=10,
                   fontweight='bold', color='#333')

        ax.set_xlim(-max(30, r+8), max(30, r+8))
        ax.set_ylim(-max(30, r+8), max(30, r+8))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title, fontsize=12, fontweight='bold', color=color, pad=8)
        for spine in ax.spines.values():
            spine.set_edgecolor('#DDD')
            spine.set_linewidth(1)

    # 最右侧添加说明
    axes[-1].text(0, -22, '绘图=实物×比例\n如 1∶5 时：\n40×1/5=8mm',
                 ha='center', fontsize=9, color='#666', style='italic')

    fig.suptitle('比例的含义：图形尺寸 vs 实物尺寸', fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    save(fig, '02_scale_concept.png')

# ============================================================
# 图3: 字体规范
# ============================================================
def draw_font_specs():
    fig = plt.figure(figsize=(14, 8))

    # --- 左: 长仿宋体 vs 普通宋体 ---
    ax1 = fig.add_subplot(2, 3, (1, 2))
    ax1.set_xlim(0, 8)
    ax1.set_ylim(0, 6)
    ax1.axis('off')
    ax1.set_title('长仿宋体 特征', fontsize=13, fontweight='bold', pad=10)

    # 字宽比例示意图
    for i, (label, w, h_val, fc) in enumerate([
        ('正方形\n(参考)', 1.0, 1.0, '#E0E0E0'),
        ('长仿宋体\n字宽=0.7h', 0.7, 1.0, '#64B5F6'),
    ]):
        x = 1 + i * 3.5
        y = 1.5
        rect = FancyBboxPatch((x, y), w * 2.5, h_val * 2.5,
                              boxstyle="round,pad=0.05", facecolor=fc, edgecolor='#333',
                              linewidth=2, alpha=0.6)
        ax1.add_patch(rect)
        ax1.text(x + w * 1.25, y - 0.5, label, ha='center', fontsize=9, color='#555')
        if i == 1:
            ax1.annotate('', xy=(x, y - 0.15), xytext=(x + w * 2.5, y - 0.15),
                        arrowprops=dict(arrowstyle='<->', color='#D32F2F', lw=2))
            ax1.text(x + w * 1.25, y - 1.0, '字宽 = 0.7 x 字高', ha='center',
                    fontsize=10, color='#D32F2F', fontweight='bold')

    # 长仿宋体示例文字
    ax1.text(4, 4.8, '工 程 制 图', fontsize=22,
            ha='center', fontweight='bold', color='#333',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F5E9', edgecolor='#4CAF50', lw=1.5))
    ax1.text(4, 4.2, '横平竖直 · 起落有顿 · 结构匀称', fontsize=9, ha='center', color='#777')

    # --- 中: 斜体75° ---
    ax2 = fig.add_subplot(2, 3, 3)
    ax2.set_xlim(-1, 5)
    ax2.set_ylim(-1, 5)
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.set_title('斜体字母 75° 倾斜', fontsize=13, fontweight='bold', pad=10)

    # 水平基准线
    ax2.axhline(y=0, xmin=0.1, xmax=0.9, color='#333', linewidth=2)
    ax2.text(4.5, -0.15, '水平基准', fontsize=8, color='#333', ha='right')

    # 75°线
    angle_rad = np.radians(75)
    ax2.annotate('', xy=(4 * np.cos(angle_rad), 4 * np.sin(angle_rad)), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='#D32F2F', lw=2.5))
    ax2.text(2.5, 2.8, '75°', fontsize=14, color='#D32F2F', fontweight='bold')

    # 角度弧线
    arc = Arc((0, 0), 2, 2, angle=0, theta1=0, theta2=75, color='#FF5722', lw=2)
    ax2.add_patch(arc)

    # 示例倾斜字母
    ax2.text(2.5, 1.5, 'ABCD', fontsize=24, fontstyle='italic', color='#1565C0',
            fontweight='bold', rotation=15, ha='center')

    # --- 右下: 字号系列柱状图 ---
    ax3 = fig.add_subplot(2, 1, 2)
    sizes = [1.8, 2.5, 3.5, 5, 7, 10, 14, 20]
    labels = [f'{s}' for s in sizes]
    colors_bar = plt.cm.Blues(np.linspace(0.35, 0.9, len(sizes)))

    bars = ax3.bar(range(len(sizes)), sizes, color=colors_bar, edgecolor='#333', linewidth=1.2, width=0.6)

    for i, (bar, s) in enumerate(zip(bars, sizes)):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f'{s}mm', ha='center', fontsize=10, fontweight='bold', color='#333')

    # 标注√2比率
    for i in range(len(sizes) - 1):
        ratio = sizes[i+1] / sizes[i]
        mid_x = i + 0.5
        ax3.annotate(f'×{ratio:.2f}', xy=(mid_x, max(sizes[i], sizes[i+1]) + 1.2),
                    fontsize=7, color='#E65100', ha='center')

    ax3.set_xticks(range(len(sizes)))
    ax3.set_xticklabels(labels)
    ax3.set_xlabel('字号', fontsize=12)
    ax3.set_ylabel('字高 (mm)', fontsize=12)
    ax3.set_title('字号系列（8种）— 按 √2 比率递增', fontsize=14, fontweight='bold', pad=8)
    ax3.grid(axis='y', alpha=0.3)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)

    # 标记"不是4号"
    ax3.annotate('注意："4"号不在标准系列中！', xy=(0.5, 4), xytext=(2.5, 2.5),
                arrowprops=dict(arrowstyle='->', color='#D32F2F', lw=1.5),
                fontsize=9, color='#D32F2F', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFEBEE', edgecolor='#D32F2F'))

    fig.suptitle('字体规范', fontsize=16, fontweight='bold', y=1.01)
    plt.tight_layout()
    save(fig, '03_font_specs.png')

# ============================================================
# 图4: 常用图线类型
# ============================================================
def draw_line_types():
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 14)
    ax.axis('off')

    lines_data = [
        ('粗实线', '可见轮廓线', '粗 (d)', '#333', 3.5, 'solid'),
        ('细实线', '尺寸线、尺寸界线、剖面线', '细 (d/2)', '#333', 1.5, 'solid'),
        ('细虚线', '不可见轮廓线', '细 (d/2)', '#555', 1.5, (0, (6, 3))),
        ('细点画线', '轴线、对称中心线', '细 (d/2)', '#333', 1.5, (0, (12, 4, 2, 4))),
        ('波浪线', '断裂处分界线', '细 (d/2)', '#333', 1.5, 'solid'),
        ('细双点画线', '轨迹线、相邻辅助零件', '细 (d/2)', '#333', 1.5, (0, (14, 4, 2, 4, 2, 4))),
    ]

    y_start = 12
    for i, (name, usage, width_label, color, lw, ls) in enumerate(lines_data):
        y = y_start - i * 2.2

        # 标签
        ax.text(0.5, y, name, fontsize=12, fontweight='bold', color='#333', va='center')
        ax.text(6.5, y, usage, fontsize=10, color='#666', va='center')
        ax.text(17.5, y, width_label, fontsize=9, color='#999', va='center')

        # 画线
        if name == '波浪线':
            # 手绘波浪效果
            xs = np.linspace(19, 28, 120)
            ys = y + 0.25 * np.sin(xs * 3.5) * np.exp(-0.02 * (xs - 19))
            ax.plot(xs, ys, color=color, linewidth=lw)
        else:
            ax.plot([19, 28], [y, y], color=color, linewidth=lw, linestyle=ls,
                   solid_capstyle='round')

        # 示例小图
        if name == '粗实线':
            rect = FancyBboxPatch((27, y-0.35), 2, 0.7,
                                  boxstyle="round,pad=0.02", facecolor='none',
                                  edgecolor=color, linewidth=lw)
            ax.add_patch(rect)
        elif name == '细虚线':
            rect = FancyBboxPatch((27, y-0.35), 2, 0.7,
                                  boxstyle="round,pad=0.02", facecolor='none',
                                  edgecolor=color, linewidth=lw, linestyle=ls)
            ax.add_patch(rect)
        elif name == '细点画线':
            ax.plot([27, 29], [y, y], color=color, linewidth=lw, linestyle=ls)
            ax.plot([27, 29], [y+0.3, y+0.3], color=color, linewidth=lw, linestyle=ls)
            # 十字中心标记
            ax.plot([28, 28], [y-0.3, y+0.6], color=color, linewidth=lw, linestyle=ls)

    ax.set_title('常用图线类型与用途', fontsize=16, fontweight='bold', pad=15)

    # 图例：线宽对比
    ax.text(0.5, -0.3, f'粗线宽度 d = 0.5~2mm | 细线宽度 = d/2 | 粗∶细 = 2∶1',
            fontsize=11, color='#E65100', fontweight='bold', ha='left', transform=ax.transAxes)

    plt.tight_layout()
    save(fig, '04_line_types.png')

# ============================================================
# 图5: 尺寸标注四要素
# ============================================================
def draw_dimension_elements():
    fig, ax = plt.subplots(figsize=(12, 6))

    # 画一个"零件"矩形
    rect = FancyBboxPatch((3, 2.5), 8, 3.5, boxstyle="round,pad=0.1",
                          facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=2.5)
    ax.add_patch(rect)
    ax.text(7, 4.25, '零 件', fontsize=16, ha='center', va='center',
           color='#1565C0', fontweight='bold')

    # 尺寸界线（细实线）
    ax.plot([3, 3], [1.2, 2.5], color='#333', linewidth=1.2)
    ax.plot([11, 11], [1.2, 2.5], color='#333', linewidth=1.2)

    # 尺寸线（细实线 + 箭头）
    ax.plot([2.3, 11.7], [1.2, 1.2], color='#333', linewidth=1.2)
    # 箭头
    ax.annotate('', xy=(11.7, 1.2), xytext=(10.7, 1.2),
               arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
    ax.annotate('', xy=(2.3, 1.2), xytext=(3.3, 1.2),
               arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))

    # 尺寸数字
    ax.text(7, 1.7, '80', fontsize=18, ha='center', va='bottom',
           fontweight='bold', color='#333')

    # 标注四个要素
    annotations = [
        (1.5, 1.85, '尺寸界线\n(细实线)', '#D32F2F', 'left'),
        (7, 0.5, '尺寸线 (细实线)', '#1976D2', 'center'),
        (7, 2.3, '尺寸数字\n(真实大小)', '#388E3C', 'center'),
        (11.3, 1.85, '尺寸终端\n(箭头)', '#F57C00', 'right'),
    ]

    for x, y, txt, color, align in annotations:
        ax.annotate(txt, xy=(x, y), fontsize=11, color=color, fontweight='bold',
                   ha=align if align != 'right' else 'left',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                            edgecolor=color, alpha=0.9, lw=1.2))

        # 连线
        if '尺寸界线' in txt:
            ax.plot([1.5, 2.5], [1.85, 1.7], color=color, lw=1, linestyle='--')
        elif '尺寸线' in txt:
            ax.plot([7, 7], [0.9, 1.15], color=color, lw=1, linestyle='--')
        elif '尺寸数字' in txt:
            ax.plot([7, 7], [2.3, 1.9], color=color, lw=1, linestyle='--')
        elif '尺寸终端' in txt:
            ax.plot([12, 11.5], [1.85, 1.4], color=color, lw=1, linestyle='--')

    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('尺寸标注的四要素', fontsize=16, fontweight='bold', pad=15)

    plt.tight_layout()
    save(fig, '05_dimension_elements.png')

# ============================================================
# 图6: 线性尺寸标注详解
# ============================================================
def draw_linear_dimension():
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # --- (a) 水平标注：数字在尺寸线上方，头朝上 ---
    ax = axes[0, 0]
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.set_aspect('equal')

    rect = FancyBboxPatch((2, 2.5), 8, 2, boxstyle="round,pad=0.08",
                          facecolor='#E8F5E9', edgecolor='#388E3C', linewidth=2)
    ax.add_patch(rect)

    # 尺寸界线
    ax.plot([2, 2], [1, 2.5], 'k-', lw=1)
    ax.plot([10, 10], [1, 2.5], 'k-', lw=1)
    # 尺寸线+箭头
    ax.annotate('', xy=(10, 1), xytext=(2, 1), arrowprops=dict(arrowstyle='<->', lw=1.5, color='#333'))
    ax.text(6, 1.5, '80', fontsize=18, ha='center', va='bottom', fontweight='bold')
    ax.text(6, 0.3, '数字在尺寸线上方，头朝上↑', fontsize=10, ha='center', color='#D32F2F', fontweight='bold')

    ax.axis('off')
    ax.set_title('水平标注', fontsize=13, fontweight='bold', color='#388E3C')

    # --- (b) 竖直标注：数字头朝左 ---
    ax = axes[0, 1]
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.set_aspect('equal')

    rect = FancyBboxPatch((3, 1), 2, 4, boxstyle="round,pad=0.08",
                          facecolor='#FFF3E0', edgecolor='#E65100', linewidth=2)
    ax.add_patch(rect)

    ax.plot([6, 6], [1, 5], 'k-', lw=1)  # 尺寸线
    ax.plot([5.5, 7.5], [1, 1], 'k-', lw=1)  # 尺寸界线
    ax.plot([5.5, 7.5], [5, 5], 'k-', lw=1)
    ax.annotate('', xy=(6, 5), xytext=(6, 1), arrowprops=dict(arrowstyle='<->', lw=1.5, color='#333'))
    ax.text(6.8, 3, '50', fontsize=18, ha='left', va='center', fontweight='bold', rotation=90)
    ax.text(6.8, 0.3, '数字头朝左←\n(旋转后仍可读)', fontsize=9, ha='center', color='#D32F2F', fontweight='bold')

    ax.axis('off')
    ax.set_title('竖直标注', fontsize=13, fontweight='bold', color='#E65100')

    # --- (c) 尺寸数字中断处注写 ---
    ax = axes[1, 0]
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')

    rect = FancyBboxPatch((1.5, 2), 9, 1.5, boxstyle="round,pad=0.08",
                          facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=2)
    ax.add_patch(rect)

    ax.plot([1.5, 1.5], [0.8, 2], 'k-', lw=1)
    ax.plot([10.5, 10.5], [0.8, 2], 'k-', lw=1)
    # 尺寸线分两段
    ax.annotate('', xy=(5.2, 0.8), xytext=(1.5, 0.8), arrowprops=dict(arrowstyle='<->', lw=1.5, color='#333'))
    ax.annotate('', xy=(10.5, 0.8), xytext=(7.3, 0.8), arrowprops=dict(arrowstyle='<->', lw=1.5, color='#333'))
    ax.text(6.25, 0.8, '90', fontsize=18, ha='center', va='center', fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none'))
    ax.text(6, 0.1, '数字写在尺寸线中断处', fontsize=10, ha='center', color='#D32F2F', fontweight='bold')

    ax.axis('off')
    ax.set_title('中断处注写（也允许）', fontsize=13, fontweight='bold', color='#1565C0')

    # --- (d) 图线通过数字→断开图线 ---
    ax = axes[1, 1]
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')

    # 中心线在数字处断开
    ax.plot([1, 4.8], [2.5, 2.5], color='k', lw=1, linestyle=(0, (12, 4, 2, 4)))  # 点画线
    ax.plot([7.2, 11], [2.5, 2.5], color='k', lw=1, linestyle=(0, (12, 4, 2, 4)))
    ax.text(6, 2.5, '30', fontsize=18, ha='center', va='center', fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#333', lw=1))

    ax.annotate('图线在此断开', xy=(4, 3), xytext=(2.5, 4),
               arrowprops=dict(arrowstyle='->', color='#D32F2F', lw=2),
               fontsize=10, color='#D32F2F', fontweight='bold')
    ax.annotate('图线在此断开', xy=(8.5, 3), xytext=(9.5, 4),
               arrowprops=dict(arrowstyle='->', color='#D32F2F', lw=2),
               fontsize=10, color='#D32F2F', fontweight='bold', ha='right')

    ax.axis('off')
    ax.set_title('数字不可被图线通过 → 断开图线', fontsize=13, fontweight='bold', color='#C62828')

    fig.suptitle('线性尺寸标注规则', fontsize=16, fontweight='bold', y=1.01)
    plt.tight_layout()
    save(fig, '06_linear_dimension.png')

# ============================================================
# 图7: 角度、直径、半径、弧长标注
# ============================================================
def draw_special_dimensions():
    fig, axes = plt.subplots(1, 4, figsize=(16, 5))

    # --- (a) 角度标注 ---
    ax = axes[0]
    # 画角度
    ax.plot([0, 4], [0, 0], 'k-', lw=2)
    ax.plot([0, 2.83], [0, 2.83], 'k-', lw=2)

    # 圆弧尺寸线
    arc = Arc((0, 0), 3, 3, angle=0, theta1=0, theta2=45, color='#D32F2F', lw=2)
    ax.add_patch(arc)

    # 箭头
    ax.annotate('', xy=(2.12, 2.12), xytext=(2.6, 1.08),
               arrowprops=dict(arrowstyle='->', color='#D32F2F', lw=1.5))

    ax.text(1.5, 1.0, '45°', fontsize=18, ha='center', fontweight='bold', color='#D32F2F')
    ax.text(1.5, 0.5, '数字永远水平！', fontsize=9, ha='center', color='#D32F2F', fontweight='bold')

    ax.set_xlim(-0.5, 5)
    ax.set_ylim(-0.5, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('① 角度标注', fontsize=13, fontweight='bold', color='#D32F2F')

    # --- (b) 直径标注 ---
    ax = axes[1]
    circle = Circle((2, 2.25), 1.8, fill=False, edgecolor='#1565C0', linewidth=2.5)
    ax.add_patch(circle)

    # 直径尺寸线通过圆心
    ax.annotate('', xy=(3.8, 2.25), xytext=(0.2, 2.25),
               arrowprops=dict(arrowstyle='<->', color='#1565C0', lw=2))
    ax.plot([2, 2], [2.25, 2.25], 'o', color='#1565C0', markersize=4)  # 圆心

    ax.text(2, 2.9, 'φ36', fontsize=18, ha='center', fontweight='bold', color='#1565C0')
    ax.text(2, 3.5, '尺寸线通过圆心', fontsize=9, ha='center', color='#1565C0', fontweight='bold')

    ax.set_xlim(-1, 5)
    ax.set_ylim(-1, 5.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('② 直径标注 φ', fontsize=13, fontweight='bold', color='#1565C0')

    # --- (c) 半径标注 ---
    ax = axes[2]
    # 半圆/圆弧
    theta = np.linspace(0, np.pi, 100)
    ax.plot(0.5 + 1.8 * np.cos(theta), 2.25 + 1.8 * np.sin(theta), 'k-', lw=2.5)
    ax.plot([0.5, 0.5], [2.25, 4.05], 'k-', lw=2.5)

    # 圆心
    ax.plot(0.5, 2.25, 'o', color='#333', markersize=5)
    # 半径线
    ax.plot([0.5, 2.3], [2.25, 2.25], color='#E65100', lw=2)
    ax.annotate('', xy=(2.3, 2.25), xytext=(0.5, 2.25),
               arrowprops=dict(arrowstyle='->', color='#E65100', lw=2))

    ax.text(1.4, 2.7, 'R18', fontsize=18, ha='center', fontweight='bold', color='#E65100')
    ax.text(1.4, 3.3, '从圆心出发\n箭头指到圆弧', fontsize=8, ha='center', color='#E65100', fontweight='bold')

    ax.set_xlim(-1, 5)
    ax.set_ylim(-1, 5.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('③ 半径标注 R', fontsize=13, fontweight='bold', color='#E65100')

    # --- (d) 弧长标注 ---
    ax = axes[3]
    theta = np.linspace(np.pi/4, 3*np.pi/4, 100)
    arc_x = 2 + 2.5 * np.cos(theta)
    arc_y = 1 + 2.5 * np.sin(theta)
    ax.plot(arc_x, arc_y, 'k-', lw=2.5)

    # 弧长符号和数字
    mid_idx = len(theta) // 2
    ax.text(arc_x[mid_idx], arc_y[mid_idx] + 0.7, '⌒\n120', fontsize=16, ha='center',
           fontweight='bold', color='#7B1FA2')
    ax.text(arc_x[mid_idx], arc_y[mid_idx] + 2.0, '⌒加在数字上方', fontsize=9, ha='center',
           color='#7B1FA2', fontweight='bold')

    # 端点标记
    ax.plot(arc_x[0], arc_y[0], 'o', color='#333', markersize=4)
    ax.plot(arc_x[-1], arc_y[-1], 'o', color='#333', markersize=4)

    ax.set_xlim(-1, 5.5)
    ax.set_ylim(-1, 5.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('④ 弧长标注 ⌒', fontsize=13, fontweight='bold', color='#7B1FA2')

    fig.suptitle('角度 · 直径 · 半径 · 弧长 — 标注规则', fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    save(fig, '07_special_dimensions.png')

# ============================================================
# 图8: 本章知识体系总览
# ============================================================
def draw_overview():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # 中心标题
    ax.text(10, 11, '第一章  制图的基本知识和技能', fontsize=18, fontweight='bold',
           ha='center', color='#1A237E',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#E8EAF6', edgecolor='#1A237E', lw=2))

    # 五个知识板块
    blocks = [
        (2, 8, '图纸幅面\n与格式', '#1565C0', '#E3F2FD',
         'A0~A4 (5种)\n对折规律 2^n\n加长沿短边\n标题栏右下角'),
        (7.5, 8, '比例', '#2E7D32', '#E8F5E9',
         '2∶1 = 放大\n1∶2 = 缩小\n绘图尺寸=实物×比例\n标注格式: 数字∶数字'),
        (12.5, 8, '字体', '#E65100', '#FFF3E0',
         '汉字: 长仿宋体\n字宽≈0.7h\n8种字号(√2递增)\n斜体75°'),
        (4.5, 3.5, '图线', '#6A1B9A', '#F3E5F5',
         '9种图线\n粗实线→可见轮廓\n细虚线→不可见轮廓\n粗∶细 = 2∶1'),
        (12, 3.5, '尺寸标注', '#C62828', '#FFEBEE',
         '四要素: 界线/线/数字/终端\n线性: 头朝上/头朝左\n角度: 水平注写\nφ/R/Sφ/SR/⌒'),
    ]

    for x, y, title, color, bg, content in blocks:
        # 圆角矩形
        rect = FancyBboxPatch((x - 2.2, y - 1.5), 4.4, 3.0,
                              boxstyle="round,pad=0.15", facecolor=bg,
                              edgecolor=color, linewidth=2.5, alpha=0.95)
        ax.add_patch(rect)
        ax.text(x, y + 1.0, title, fontsize=14, fontweight='bold', ha='center', color=color)
        ax.text(x, y - 0.3, content, fontsize=9, ha='center', va='top', color='#555', linespacing=1.5)

    # 底部连接线
    for x in [2, 7.5, 12.5]:
        ax.plot([x, x], [6.5, 7.3], color='#999', lw=1, linestyle='--')
    for x in [4.5, 12]:
        ax.plot([x, x], [2, 3.3], color='#999', lw=1, linestyle='--')

    ax.text(10, 0.5, '全部 30 道课后习题答案及解析见附录：第一章_习题答案.md',
           fontsize=11, ha='center', color='#888', style='italic')

    plt.tight_layout()
    save(fig, '08_chapter_overview.png')

# ============================================================
# 主程序
# ============================================================
if __name__ == '__main__':
    print("生成现代工程制图第一章配套图表...")
    draw_paper_sizes()
    draw_scale_concept()
    draw_font_specs()
    draw_line_types()
    draw_dimension_elements()
    draw_linear_dimension()
    draw_special_dimensions()
    draw_overview()
    print(f"\n全部图表已保存到: {OUTPUT_DIR}")
