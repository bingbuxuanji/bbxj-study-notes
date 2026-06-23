"""
Generate all rectifier circuit waveform diagrams for the power electronics tutorial.
Each figure is saved as a separate PNG in the images/ folder.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

# Configure matplotlib for Chinese text
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['savefig.bbox'] = 'tight'

IMG_DIR = os.path.join(os.path.dirname(__file__), 'images')
os.makedirs(IMG_DIR, exist_ok=True)

# Common parameters
ω = 2 * np.pi * 50  # 50Hz
T = 1 / 50
Um = 311  # 220V * sqrt(2)

# ============================================================
# Figure 1: 单相半波不可控整流——电阻负载
# ============================================================
def fig_halfwave_uncontrolled():
    t = np.linspace(0, 2*T, 2000)
    u_in = Um * np.sin(ω * t)
    # Diode conducts only when u_in > 0
    u_out = np.where(u_in > 0, u_in, 0)
    i_out = u_out / 10  # R = 10Ω

    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    # Input voltage
    axes[0].plot(t*1000, u_in, 'b', linewidth=1.2)
    axes[0].axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    axes[0].set_ylabel('输入电压 $u_2$ (V)')
    axes[0].set_title('单相半波不可控整流——电阻负载', fontsize=13, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim(-350, 350)

    # Output voltage
    axes[1].fill_between(t*1000, 0, u_out, alpha=0.3, color='red')
    axes[1].plot(t*1000, u_out, 'r', linewidth=1.5)
    axes[1].axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    axes[1].set_ylabel('输出电压 $u_d$ (V)')
    axes[1].grid(True, alpha=0.3)
    axes[1].set_ylim(-10, 350)
    # Annotate
    for n in [0, 1]:
        axes[1].annotate('导通', xy=(n*20+5, 200), fontsize=10, color='red',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
        axes[1].annotate('截止', xy=(n*20+15, 30), fontsize=10, color='gray',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgray', alpha=0.7))

    # Output current
    axes[2].fill_between(t*1000, 0, i_out, alpha=0.3, color='green')
    axes[2].plot(t*1000, i_out, 'g', linewidth=1.5)
    axes[2].axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    axes[2].set_ylabel('输出电流 $i_d$ (A)')
    axes[2].set_xlabel('时间 (ms) — 两个周期')
    axes[2].grid(True, alpha=0.3)
    axes[2].set_ylim(-2, 33)

    # x-axis ticks
    for ax in axes:
        ax.set_xticks(np.arange(0, 41, 5))
        ax.axvline(x=10, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
        ax.axvline(x=30, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

    # Add Ud annotation
    Ud = Um / np.pi
    axes[1].axhline(y=Ud, color='orange', linestyle='--', linewidth=1, alpha=0.7)
    axes[1].annotate(f'$U_d = U_m/\\pi \\approx {Ud:.0f}$V', xy=(30, Ud+10), fontsize=9, color='orange')

    plt.tight_layout()
    fig.savefig(os.path.join(IMG_DIR, '01_halfwave_uncontrolled.png'))
    plt.close(fig)
    print("[OK] Fig 1: 半波不可控整流")


# ============================================================
# Figure 2: 单相半波可控整流——电阻负载，不同α
# ============================================================
def fig_halfwave_controlled_resistive():
    t = np.linspace(0, 2*T, 2000)
    u_in = Um * np.sin(ω * t)
    R = 10
    alphas = [30, 60, 90, 120]

    fig, axes = plt.subplots(4, 1, figsize=(10, 10), sharex=True)

    for idx, α in enumerate(alphas):
        α_rad = np.deg2rad(α)
        # Time when α occurs
        t_alpha = α_rad / ω
        u_out = np.where((u_in > 0) & (t % T >= t_alpha), u_in, 0)
        i_out = u_out / R
        Ud = Um / (2*np.pi) * (1 + np.cos(α_rad))

        ax = axes[idx]
        ax.plot(t*1000, u_in, 'lightblue', linewidth=0.8, alpha=0.5)
        ax.fill_between(t*1000, 0, u_out, alpha=0.35, color='red')
        ax.plot(t*1000, u_out, 'r', linewidth=1.5)
        ax.axhline(y=0, color='gray', linewidth=0.5)
        ax.set_ylabel('$u_d$ (V)')
        ax.set_title(f'α = {α}°　　　$U_d = \\frac{{U_m}}{{2\\pi}}(1+\\cos{α}°) \\approx {Ud:.1f}$V', fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-350, 350)

        # Mark α position
        for n in [0, 1]:
            x_α = (n * T + t_alpha) * 1000
            ax.axvline(x=x_α, color='blue', linestyle='--', linewidth=1, alpha=0.7)
            ax.annotate(f'α', xy=(x_α+0.5, 280), fontsize=9, color='blue')
            # Mark conduction interval
            x_end = (n * T + T/2) * 1000
            ax.annotate('', xy=(x_α, 200), xytext=(x_end, 200),
                       arrowprops=dict(arrowstyle='<->', color='darkred', lw=1.5))
            ax.text((x_α + x_end)/2, 215, f'导通\n{180-α}°', ha='center', fontsize=8, color='darkred')

    axes[-1].set_xlabel('时间 (ms)')
    for ax in axes:
        ax.set_xticks(np.arange(0, 41, 5))

    plt.tight_layout()
    fig.savefig(os.path.join(IMG_DIR, '02_halfwave_controlled_resistive.png'))
    plt.close(fig)
    print("[OK] Fig 2: 半波可控整流（电阻，不同α）")


# ============================================================
# Figure 3: 单相半波可控整流——电感负载，无续流二极管
# ============================================================
def fig_halfwave_inductive_no_fwd():
    """Simulate R-L load without freewheeling diode — proper physics"""
    t = np.linspace(0, 2*T, 8000)  # High resolution for accurate zero-crossing
    dt = t[1] - t[0]
    u_in = Um * np.sin(ω * t)

    α = 60  # degrees
    α_rad = np.deg2rad(α)
    R = 5.0        # Lower R → larger τ → clearer negative voltage area
    L = 0.06       # H → τ = L/R = 12ms ≈ half cycle

    i = np.zeros(len(t))
    scr_on = np.zeros(len(t), dtype=bool)

    for k in range(1, len(t)):
        ωt_curr = (ω * t[k]) % (2 * np.pi)
        ωt_prev = (ω * t[k-1]) % (2 * np.pi)

        # --- Detect α-crossing (handles 2π→0 wrap correctly) ---
        if ωt_prev < ωt_curr:
            # No wrap within this step
            crossed_alpha = (ωt_prev < α_rad <= ωt_curr)
        else:
            # Wrapped around 2π → 0
            crossed_alpha = (ωt_prev < α_rad) or (α_rad <= ωt_curr)

        # --- SCR state machine ---
        if crossed_alpha and ωt_curr < np.pi and u_in[k] > 0:
            # Gate pulse at α — turn SCR on
            scr_on[k] = True
        elif scr_on[k-1]:
            # SCR stays on as long as current flows (> 1 mA)
            if i[k-1] > 1e-3:
                scr_on[k] = True
            else:
                scr_on[k] = False  # current reached zero → natural turn-off
        else:
            scr_on[k] = False

        # --- Circuit: u_in = L·di/dt + R·i  (when SCR on) ---
        if scr_on[k]:
            di = (u_in[k] - R * i[k-1]) / L * dt
            i[k] = max(0.0, i[k-1] + di)
        else:
            i[k] = 0.0

    u_out = np.where(scr_on, u_in, 0.0)

    # --- Plot ---
    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

    # (1) Input voltage
    axes[0].plot(t*1000, u_in, 'b', linewidth=1)
    axes[0].axhline(y=0, color='gray', linewidth=0.5)
    axes[0].set_ylabel('$u_2$ (V)')
    axes[0].set_title(f'单相半波可控整流——电感性负载（无续流二极管）  α={α}°, R={R}Ω, L={int(L*1000)}mH, τ={L/R*1000:.0f}ms', fontsize=13, fontweight='bold')
    axes[0].grid(True, alpha=0.3)

    # (2) Output voltage — show positive & negative areas clearly
    axes[1].plot(t*1000, u_in, 'lightblue', linewidth=0.5, alpha=0.4)
    axes[1].fill_between(t*1000, 0, u_out, where=(u_out>=0), alpha=0.35, color='#e74c3c', label='正向面积')
    axes[1].fill_between(t*1000, 0, u_out, where=(u_out<0), alpha=0.45, color='#3498db', label='负向面积！')
    axes[1].plot(t*1000, u_out, 'darkred', linewidth=1.5)
    axes[1].axhline(y=0, color='gray', linewidth=0.5)
    axes[1].set_ylabel('$u_d$ (V)')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(loc='upper right', fontsize=9)

    # Mark π (voltage zero-crossing) and θ_off
    for n in [0, 1]:
        x_pi = (n*T + T/2) * 1000
        axes[1].axvline(x=x_pi, color='green', linestyle=':', linewidth=1.2, alpha=0.8)
        axes[1].annotate('π\n(电压过零)', xy=(x_pi-1.2, -80), fontsize=8, color='green',
                        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

    # Find and mark θ_off (where SCR turns off)
    for n in [0, 1]:
        cycle_mask = (t >= n*T) & (t < (n+1)*T)
        cycle_idx = np.where(cycle_mask)[0]
        # Find last point where scr is on in this cycle
        scr_in_cycle = scr_on[cycle_idx]
        if np.any(scr_in_cycle):
            last_on = cycle_idx[np.where(scr_in_cycle)[0][-1]]
            x_off = t[last_on] * 1000
            if x_off > (n*T + T/2)*1000:  # Only mark if extends past π
                axes[1].axvline(x=x_off, color='purple', linestyle='--', linewidth=1, alpha=0.8)
                axes[1].annotate(r'$\theta_{off}$', xy=(x_off+0.3, 30), fontsize=9, color='purple')

    # (3) Output current
    axes[2].fill_between(t*1000, 0, i, alpha=0.3, color='green')
    axes[2].plot(t*1000, i, 'darkgreen', linewidth=1.5)
    axes[2].axhline(y=0, color='gray', linewidth=0.5)
    axes[2].set_ylabel('$i_d$ (A)')
    axes[2].set_xlabel('时间 (ms)')
    axes[2].grid(True, alpha=0.3)

    for n in [0, 1]:
        x_pi = (n*T + T/2) * 1000
        axes[2].axvline(x=x_pi, color='green', linestyle=':', linewidth=1.2, alpha=0.8)
        # Annotate: current continues past π
        axes[2].annotate('电流继续！', xy=(x_pi+1.5, max(i)*0.5), fontsize=9, color='darkgreen',
                        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

    for ax in axes:
        ax.set_xticks(np.arange(0, 41, 5))
        ax.set_xlim(0, 40)
        ax.set_ylim(auto=True)

    axes[0].set_ylim(-350, 350)
    axes[1].set_ylim(-350, 350)

    plt.tight_layout()
    fig.savefig(os.path.join(IMG_DIR, '03_halfwave_inductive_no_fwd.png'))
    plt.close(fig)
    print("[OK] Fig 3: 半波可控整流（电感，无续流二极管）")


# ============================================================
# Figure 4: 单相半波可控整流——电感负载，带续流二极管
# ============================================================
def fig_halfwave_inductive_with_fwd():
    t = np.linspace(0, 2*T, 8000)
    dt = t[1] - t[0]
    u_in = Um * np.sin(ω * t)
    α = 60
    α_rad = np.deg2rad(α)
    R = 5.0       # Match Fig 3 parameters for consistency
    L = 0.08       # Large L for nearly constant current, τ = 16ms

    i_load = np.zeros(len(t))
    i_scr = np.zeros(len(t))
    i_fwd = np.zeros(len(t))
    scr_on = np.zeros(len(t), dtype=bool)
    fwd_on = np.zeros(len(t), dtype=bool)

    for k in range(1, len(t)):
        ωt_curr = (ω * t[k]) % (2 * np.pi)
        ωt_prev = (ω * t[k-1]) % (2 * np.pi)

        # Detect α-crossing (handles 2π→0 wrap)
        if ωt_prev < ωt_curr:
            crossed_alpha = (ωt_prev < α_rad <= ωt_curr)
        else:
            crossed_alpha = (ωt_prev < α_rad) or (α_rad <= ωt_curr)

        # Detect π-crossing (voltage zero-crossing, handles wrap)
        if ωt_prev < ωt_curr:
            crossed_pi = (ωt_prev < np.pi <= ωt_curr)
        else:
            crossed_pi = (ωt_prev < np.pi) or (np.pi <= ωt_curr)

        # --- State machine ---
        # SCR triggers at α in positive half-cycle
        if crossed_alpha and ωt_curr < np.pi:
            scr_on[k] = True
            fwd_on[k] = False
        # SCR turns off at π (voltage zero-crossing), FWD takes over
        elif scr_on[k-1] and crossed_pi:
            scr_on[k] = False
            fwd_on[k] = True
        # FWD stays on until next SCR trigger
        elif fwd_on[k-1] and crossed_alpha and ωt_curr < np.pi:
            scr_on[k] = True
            fwd_on[k] = False
        else:
            scr_on[k] = scr_on[k-1]
            fwd_on[k] = fwd_on[k-1]

        # --- Circuit equations ---
        if scr_on[k]:
            di = (u_in[k] - R * i_load[k-1]) / L * dt
            i_load[k] = max(0.0, i_load[k-1] + di)
            i_scr[k] = i_load[k]
            i_fwd[k] = 0.0
        elif fwd_on[k]:
            di = (-R * i_load[k-1]) / L * dt  # FWD shorts load, voltage ≈ 0
            i_load[k] = max(0.0, i_load[k-1] + di)
            i_scr[k] = 0.0
            i_fwd[k] = i_load[k]
        else:
            i_load[k] = 0.0
            i_scr[k] = 0.0
            i_fwd[k] = 0.0

    u_out = np.where(scr_on, np.maximum(u_in, 0), 0.0)

    # --- Plot ---
    fig, axes = plt.subplots(4, 1, figsize=(10, 11), sharex=True)

    axes[0].plot(t*1000, u_in, 'b', linewidth=1)
    axes[0].axhline(y=0, color='gray', linewidth=0.5)
    axes[0].set_ylabel('$u_2$ (V)')
    axes[0].set_title(f'单相半波可控整流——电感性负载（带续流二极管）  α={α}°, R={R}Ω, L={int(L*1000)}mH', fontsize=13, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim(-350, 350)

    axes[1].fill_between(t*1000, 0, u_out, alpha=0.35, color='#e74c3c')
    axes[1].plot(t*1000, u_out, 'darkred', linewidth=1.5)
    axes[1].axhline(y=0, color='gray', linewidth=0.5)
    axes[1].set_ylabel('$u_d$ (V)')
    axes[1].grid(True, alpha=0.3)
    axes[1].annotate('无负向面积！', xy=(22, 250), fontsize=11, color='darkred',
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    axes[1].set_ylim(-10, 350)

    axes[2].plot(t*1000, i_load, 'darkgreen', linewidth=1.5)
    axes[2].axhline(y=0, color='gray', linewidth=0.5)
    axes[2].set_ylabel('负载电流 $i_d$ (A)')
    axes[2].grid(True, alpha=0.3)
    axes[2].annotate('电流近似恒定\n（大电感续流）', xy=(22, np.mean(i_load)*0.7), fontsize=10,
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

    axes[3].fill_between(t*1000, 0, i_scr, alpha=0.4, color='#e74c3c', label='晶闸管电流 $i_T$')
    axes[3].fill_between(t*1000, 0, i_fwd, alpha=0.4, color='#3498db', label='续流二极管电流 $i_{FWD}$')
    axes[3].plot(t*1000, i_scr, 'darkred', linewidth=0.8)
    axes[3].plot(t*1000, i_fwd, 'darkblue', linewidth=0.8)
    axes[3].axhline(y=0, color='gray', linewidth=0.5)
    axes[3].set_ylabel('器件电流 (A)')
    axes[3].set_xlabel('时间 (ms)')
    axes[3].grid(True, alpha=0.3)
    axes[3].legend(loc='upper right', fontsize=9)
    axes[3].annotate(f'SCR导通\n{180-α}°', xy=(6, max(i_scr)*0.55), fontsize=9, color='darkred')
    axes[3].annotate(f'FWD导通\n{180+α}°', xy=(26, max(i_fwd)*0.55), fontsize=9, color='darkblue')

    for ax in axes:
        ax.set_xticks(np.arange(0, 41, 5))
        ax.set_xlim(0, 40)

    plt.tight_layout()
    fig.savefig(os.path.join(IMG_DIR, '04_halfwave_inductive_with_fwd.png'))
    plt.close(fig)
    print("[OK] Fig 4: 半波可控整流（电感，带续流二极管）")


# ============================================================
# Figure 5: 单相桥式全控整流——电阻负载
# ============================================================
def fig_bridge_full_resistive():
    t = np.linspace(0, 2*T, 2000)
    u_in = Um * np.sin(ω * t)
    α = 45
    α_rad = np.deg2rad(α)

    # Bridge: output is abs(u_in) when conducting, 0 otherwise
    u_out = np.zeros(len(t))
    i_out = np.zeros(len(t))
    R = 10

    for k in range(len(t)):
        ωt_mod = (ω * t[k]) % (2 * np.pi)
        # Bridge conducts in both half-cycles after α
        if α_rad <= ωt_mod < np.pi:
            u_out[k] = u_in[k]   # Positive half-cycle
        elif np.pi + α_rad <= ωt_mod < 2*np.pi:
            u_out[k] = -u_in[k]  # Negative half-cycle
        else:
            u_out[k] = 0
    i_out = u_out / R

    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

    axes[0].plot(t*1000, u_in, 'b', linewidth=1)
    axes[0].axhline(y=0, color='gray', linewidth=0.5)
    axes[0].set_ylabel('$u_2$ (V)')
    axes[0].set_title(f'单相桥式全控整流——电阻负载  α={α}°', fontsize=13, fontweight='bold')
    axes[0].grid(True, alpha=0.3)

    axes[1].fill_between(t*1000, 0, u_out, alpha=0.35, color='red')
    axes[1].plot(t*1000, u_out, 'r', linewidth=1.5)
    axes[1].axhline(y=0, color='gray', linewidth=0.5)
    axes[1].set_ylabel('$u_d$ (V)')
    axes[1].grid(True, alpha=0.3)
    # Mark each pulse
    for n in range(4):
        axes[1].annotate(f'VT{n%2+1}&VT{(n%2)+4 if n%2==0 else (n%2)+2}',
                        xy=(n*5+2, 200), fontsize=7, rotation=90, color='darkred')

    axes[2].fill_between(t*1000, 0, i_out, alpha=0.3, color='green')
    axes[2].plot(t*1000, i_out, 'g', linewidth=1.5)
    axes[2].axhline(y=0, color='gray', linewidth=0.5)
    axes[2].set_ylabel('$i_d$ (A)')
    axes[2].set_xlabel('时间 (ms)')
    axes[2].grid(True, alpha=0.3)

    # Ud line
    Ud = Um / np.pi * (1 + np.cos(α_rad))
    axes[1].axhline(y=Ud, color='orange', linestyle='--', linewidth=1, alpha=0.7)
    axes[1].annotate(f'$U_d \\approx {Ud:.0f}$V', xy=(30, Ud+10), fontsize=9, color='orange')

    for ax in axes:
        ax.set_xticks(np.arange(0, 41, 5))
        ax.set_xlim(0, 40)

    plt.tight_layout()
    fig.savefig(os.path.join(IMG_DIR, '05_bridge_full_resistive.png'))
    plt.close(fig)
    print("[OK] Fig 5: 桥式全控整流（电阻负载）")


# ============================================================
# Figure 6: 单相桥式全控整流——大电感负载
# ============================================================
def fig_bridge_full_inductive():
    """Correct bridge full-controlled with large inductive load.
    Key points:
    - Each thyristor conducts exactly 180° (π), independent of α
    - u_d follows u_in during VT1&4, follows -u_in during VT2&3
    - u_d has BOTH positive and negative portions (for α>0)
    - i_d ≈ constant (large L)
    - i_in (AC side) = ±Id square wave, 180° wide, shifted by α
    """
    t = np.linspace(0, 2*T, 8000)
    dt = t[1] - t[0]
    u_in = Um * np.sin(ω * t)
    α = 45
    α_rad = np.deg2rad(α)
    R = 2.0       # Small R, large L → nearly constant current
    L = 0.2       # τ = 100ms >> 20ms period → i_d ≈ constant

    # -- Build thyristor conduction states --
    # Each pair conducts 180° starting from its trigger angle
    vt14_on = np.zeros(len(t), dtype=bool)  # VT1 & VT4
    vt23_on = np.zeros(len(t), dtype=bool)  # VT2 & VT3

    for k in range(len(t)):
        ωt_mod = (ω * t[k]) % (2 * np.pi)
        # VT1&VT4: conduct from α to α+π
        if α_rad <= ωt_mod < α_rad + np.pi:
            vt14_on[k] = True
        # VT2&VT3: conduct from α+π to α+2π (= α mod 2π)
        if (ωt_mod >= α_rad + np.pi) or (ωt_mod < α_rad):
            vt23_on[k] = True

    # -- Output voltage: u_d = u_in when VT14 on, u_d = -u_in when VT23 on --
    u_out = np.where(vt14_on, u_in, -u_in)

    # -- Load current: simulate large L (nearly constant) --
    i_load = np.zeros(len(t))
    for k in range(1, len(t)):
        di = (abs(u_out[k]) - R * i_load[k-1]) / L * dt
        i_load[k] = i_load[k-1] + di
    Id = np.mean(i_load[len(t)//4:])  # steady-state average

    # -- AC input current: ±Id square wave (180° wide) --
    i_in = np.where(vt14_on, Id, -Id)

    # -- Thyristor voltage stress (across VT1) --
    # VT1 blocks when VT23 conduct → sees u_in (reverse) or forward voltage
    v_vt1 = np.where(vt23_on, u_in, 0.0)  # simplified: reverse voltage across VT1

    # ===== PLOT =====
    fig, axes = plt.subplots(5, 1, figsize=(12, 13), sharex=True)

    # (1) Input AC voltage
    axes[0].plot(t*1000, u_in, 'b', linewidth=1)
    axes[0].axhline(y=0, color='gray', linewidth=0.5)
    axes[0].set_ylabel('$u_2$ (V)')
    axes[0].set_title(f'单相桥式全控整流——阻感负载（大电感，电流连续）  α={α}°', fontsize=14, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim(-350, 350)

    # Mark trigger instants
    for n in [0, 1]:
        t_a1 = (n*T + α_rad/ω) * 1000
        t_a2 = (n*T + T/2 + α_rad/ω) * 1000
        axes[0].axvline(x=t_a1, color='red', linestyle='--', linewidth=0.8, alpha=0.6)
        axes[0].axvline(x=t_a2, color='blue', linestyle='--', linewidth=0.8, alpha=0.6)
    axes[0].annotate('VT1,4\n触发', xy=(t_a1+0.3, 280), fontsize=7, color='red')
    axes[0].annotate('VT2,3\n触发', xy=(t_a2+0.3, 280), fontsize=7, color='blue')

    # (2) Output voltage — show positive & negative areas
    axes[1].plot(t*1000, u_in, 'lightgray', linewidth=0.4, alpha=0.3)
    axes[1].fill_between(t*1000, 0, u_out, where=(u_out>=0), alpha=0.35, color='#e74c3c', label='正向面积')
    axes[1].fill_between(t*1000, 0, u_out, where=(u_out<0), alpha=0.4, color='#3498db', label='负向面积')
    axes[1].plot(t*1000, u_out, 'darkred', linewidth=1.2)
    axes[1].axhline(y=0, color='gray', linewidth=0.5)
    axes[1].set_ylabel('$u_d$ (V)')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(loc='upper right', fontsize=8)
    Ud = 2*Um/np.pi * np.cos(α_rad)
    axes[1].axhline(y=Ud, color='orange', linestyle='--', linewidth=1.2, alpha=0.8)
    axes[1].annotate(f'$U_d = {Ud:.0f}$V', xy=(30, Ud+15), fontsize=10, color='orange',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Mark π (voltage zero crossing)
    for n in [0, 1]:
        x_pi = (n*T + T/2) * 1000
        axes[1].axvline(x=x_pi, color='green', linestyle=':', linewidth=1, alpha=0.5)

    # (3) Output current (nearly constant)
    axes[2].plot(t*1000, i_load, 'darkgreen', linewidth=1.5)
    axes[2].axhline(y=Id, color='green', linestyle='--', linewidth=0.8, alpha=0.6)
    axes[2].axhline(y=0, color='gray', linewidth=0.5)
    axes[2].set_ylabel('$i_d$ (A)')
    axes[2].grid(True, alpha=0.3)
    axes[2].annotate(f'$I_d \\approx {Id:.1f}$A (近似恒定)', xy=(20, Id*1.02), fontsize=10,
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

    # (4) AC input current — ±180° square wave!
    axes[3].fill_between(t*1000, 0, i_in, where=(i_in>0), alpha=0.35, color='#e74c3c')
    axes[3].fill_between(t*1000, 0, i_in, where=(i_in<0), alpha=0.35, color='#3498db')
    axes[3].plot(t*1000, i_in, 'purple', linewidth=1.5)
    axes[3].axhline(y=0, color='gray', linewidth=0.5)
    axes[3].set_ylabel('$i_2$ (A)')
    axes[3].grid(True, alpha=0.3)
    axes[3].set_ylim(-Id*1.5, Id*1.5)
    axes[3].annotate('±180° 矩形波\n(无直流分量)', xy=(5, Id*0.6), fontsize=10, color='purple',
                    bbox=dict(boxstyle='round', facecolor='plum', alpha=0.8))
    axes[3].annotate(f'宽度恒为 180°\n相位由 α 决定', xy=(22, -Id*0.6), fontsize=9, color='darkblue',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

    # (5) Thyristor conduction — mark 180° per device
    axes[4].fill_between(t*1000, 0, np.where(vt14_on, 1, 0), alpha=0.4, color='#e74c3c', label='VT1&VT4 导通')
    axes[4].fill_between(t*1000, 0, np.where(vt23_on, 1, 0), alpha=0.4, color='#3498db', label='VT2&VT3 导通')
    axes[4].set_ylabel('导通状态')
    axes[4].set_xlabel('时间 (ms)')
    axes[4].grid(True, alpha=0.3)
    axes[4].legend(loc='upper right', fontsize=9)
    axes[4].set_ylim(0, 1.5)
    axes[4].annotate('180°', xy=(8, 0.5), fontsize=14, fontweight='bold', color='darkred')
    axes[4].annotate('180°', xy=(18, 0.5), fontsize=14, fontweight='bold', color='darkblue')
    axes[4].annotate('导通角 = 180°\n与 α 无关！', xy=(30, 0.8), fontsize=10,
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

    for ax in axes:
        ax.set_xticks(np.arange(0, 41, 5))
        ax.set_xlim(0, 40)

    plt.tight_layout()
    fig.savefig(os.path.join(IMG_DIR, '06_bridge_full_inductive.png'))
    plt.close(fig)
    print("[OK] Fig 6: 桥式全控整流（大电感负载）——含输入电流方波、导通状态")


# ============================================================
# Figure 7: 单相桥式全控整流——α=30° vs α=90° 对比
# ============================================================
def fig_bridge_alpha_comparison():
    """Compare α=30° (rectifier mode) vs α=90° (Ud=0 boundary)"""
    t = np.linspace(0, 2*T, 8000)
    u_in = Um * np.sin(ω * t)

    fig, axes = plt.subplots(2, 2, figsize=(13, 9), sharex=True)

    for col, α_deg in enumerate([30, 90]):
        α_rad = np.deg2rad(α_deg)

        # --- Build bridge output ---
        vt14_on = np.zeros(len(t), dtype=bool)
        vt23_on = np.zeros(len(t), dtype=bool)
        for k in range(len(t)):
            ωt_mod = (ω * t[k]) % (2 * np.pi)
            if α_rad <= ωt_mod < α_rad + np.pi:
                vt14_on[k] = True
            if (ωt_mod >= α_rad + np.pi) or (ωt_mod < α_rad):
                vt23_on[k] = True

        u_out = np.where(vt14_on, u_in, -u_in)
        Ud_val = 2*Um/np.pi * np.cos(α_rad)

        # (Top row) Output voltage with area shading
        ax_v = axes[0, col]
        ax_v.plot(t*1000, u_in, 'lightgray', linewidth=0.3, alpha=0.3)
        ax_v.fill_between(t*1000, 0, u_out, where=(u_out>=0), alpha=0.35, color='#e74c3c')
        ax_v.fill_between(t*1000, 0, u_out, where=(u_out<0), alpha=0.45, color='#3498db')
        ax_v.plot(t*1000, u_out, 'darkred', linewidth=1.2)
        ax_v.axhline(y=0, color='gray', linewidth=0.5)
        ax_v.set_ylabel('$u_d$ (V)')
        ax_v.set_ylim(-350, 350)
        ax_v.grid(True, alpha=0.3)
        ax_v.set_title(f'α = {α_deg}°　　　$U_d = {Ud_val:.0f}$V', fontsize=13, fontweight='bold')

        # Mark α and π
        for n in [0, 1]:
            ax_v.axvline(x=(n*T + α_rad/ω)*1000, color='orange', linestyle='--', linewidth=0.8, alpha=0.7)
            ax_v.axvline(x=(n*T + T/2)*1000, color='green', linestyle=':', linewidth=0.8, alpha=0.5)
        if α_deg == 90:
            ax_v.annotate('正=负\nUd=0!', xy=(25, 50), fontsize=11, fontweight='bold',
                        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))

        # (Bottom row) Thyristor conduction — 180° each
        ax_c = axes[1, col]
        ax_c.fill_between(t*1000, 0, np.where(vt14_on, 1, 0), alpha=0.5, color='#e74c3c', label='VT1&4')
        ax_c.fill_between(t*1000, 0, np.where(vt23_on, 1, 0), alpha=0.5, color='#3498db', label='VT2&3')
        ax_c.set_ylabel('导通')
        ax_c.set_xlabel('时间 (ms)')
        ax_c.grid(True, alpha=0.3)
        ax_c.legend(loc='upper right', fontsize=9)
        ax_c.set_ylim(0, 1.5)
        ax_c.annotate(f'每组导通恒为 180°\n与 α={α_deg}° 无关', xy=(10, 0.7), fontsize=10,
                     bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

    fig.suptitle('单相桥式全控整流——阻感负载 α=30° vs α=90° 波形对比', fontsize=14, fontweight='bold')
    for ax in axes.flat:
        ax.set_xticks(np.arange(0, 41, 5))
        ax.set_xlim(0, 40)

    plt.tight_layout()
    fig.savefig(os.path.join(IMG_DIR, '07_bridge_alpha_comparison.png'))
    plt.close(fig)
    print("[OK] Fig 7: 桥式全控 α=30° vs 90° 对比")


# ============================================================
# Figure 8: 单相桥式半控整流——电感负载
# ============================================================
def fig_bridge_half_inductive():
    t = np.linspace(0, 2*T, 4000)
    dt = t[1] - t[0]
    u_in = Um * np.sin(ω * t)
    α = 45
    α_rad = np.deg2rad(α)
    R = 10
    L = 0.06

    # --- Without FWD (runaway/failure) ---
    i_no_fwd = np.zeros(len(t))
    for k in range(1, len(t)):
        ωt_mod = (ω * t[k]) % (2 * np.pi)
        # Half-controlled bridge without FWD: SCR can't turn off!
        if α_rad <= ωt_mod < np.pi:
            u_bridge = u_in[k] if u_in[k] > 0 else 0
        elif np.pi + α_rad <= ωt_mod < 2*np.pi:
            u_bridge = -u_in[k] if -u_in[k] > 0 else 0
        else:
            # During gap, diode + SCR forms freewheeling path — SCR stays on!
            u_bridge = 0
        di = (u_bridge - R * i_no_fwd[k-1]) / L * dt
        i_no_fwd[k] = max(0, i_no_fwd[k-1] + di)

    # --- With FWD (normal operation) ---
    i_with_fwd = np.zeros(len(t))
    fwd_on = False
    scr_on = False
    for k in range(1, len(t)):
        ωt_mod = (ω * t[k]) % (2 * np.pi)
        if not scr_on and α_rad <= ωt_mod < np.pi and u_in[k] > 0:
            scr_on = True
            fwd_on = False
        if scr_on and ωt_mod >= np.pi:
            scr_on = False
            fwd_on = True
        if fwd_on and α_rad <= ωt_mod < np.pi:
            scr_on = True
            fwd_on = False
        if scr_on:
            u_bridge = abs(u_in[k])
        elif fwd_on:
            u_bridge = 0
        else:
            u_bridge = 0
        di = (u_bridge - R * i_with_fwd[k-1]) / L * dt
        i_with_fwd[k] = max(0, i_with_fwd[k-1] + di)

    u_out_no = np.zeros(len(t))
    u_out_with = np.zeros(len(t))
    for k in range(len(t)):
        ωt_mod = (ω * t[k]) % (2 * np.pi)
        if α_rad <= ωt_mod < np.pi:
            u_out_with[k] = abs(u_in[k])
        # Without FWD — runaway, SCR can't turn off, output stuck
        # Simplified: SCR stays on permanently
        u_out_no[k] = abs(u_in[k]) if np.sin(ωt_mod) > 0 or (np.pi <= ωt_mod < np.pi+α_rad) else abs(u_in[k])

    fig, axes = plt.subplots(2, 2, figsize=(12, 9), sharex=True)

    # Left: Without FWD
    axes[0,0].plot(t*1000, u_in, 'lightblue', linewidth=0.5, alpha=0.4)
    axes[0,0].fill_between(t*1000, 0, u_out_no, alpha=0.3, color='red')
    axes[0,0].plot(t*1000, u_out_no, 'r', linewidth=1.2)
    axes[0,0].axhline(y=0, color='gray', linewidth=0.5)
    axes[0,0].set_ylabel('$u_d$ (V)')
    axes[0,0].set_title('[X] 无续流二极管——失控！', fontsize=12, color='red')
    axes[0,0].grid(True, alpha=0.3)
    axes[0,0].annotate('晶闸管无法关断\n输出电压不可控', xy=(20, 200), fontsize=10, color='red',
                      bbox=dict(boxstyle='round', facecolor='pink', alpha=0.9))

    axes[1,0].plot(t*1000, i_no_fwd, 'r', linewidth=1.5)
    axes[1,0].axhline(y=0, color='gray', linewidth=0.5)
    axes[1,0].set_ylabel('$i_d$ (A)')
    axes[1,0].set_xlabel('时间 (ms)')
    axes[1,0].grid(True, alpha=0.3)
    axes[1,0].annotate('电流失控上升！', xy=(20, max(i_no_fwd)*0.7), fontsize=10, color='red',
                      bbox=dict(boxstyle='round', facecolor='pink', alpha=0.9))

    # Right: With FWD
    axes[0,1].plot(t*1000, u_in, 'lightblue', linewidth=0.5, alpha=0.4)
    axes[0,1].fill_between(t*1000, 0, u_out_with, alpha=0.3, color='green')
    axes[0,1].plot(t*1000, u_out_with, 'g', linewidth=1.2)
    axes[0,1].axhline(y=0, color='gray', linewidth=0.5)
    axes[0,1].set_ylabel('$u_d$ (V)')
    axes[0,1].set_title('[OK] 有续流二极管——正常', fontsize=12, color='green')
    axes[0,1].grid(True, alpha=0.3)
    axes[0,1].annotate('输出正常，\n无负向面积', xy=(20, 200), fontsize=10, color='darkgreen',
                      bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9))

    axes[1,1].plot(t*1000, i_with_fwd, 'g', linewidth=1.5)
    axes[1,1].axhline(y=0, color='gray', linewidth=0.5)
    axes[1,1].set_ylabel('$i_d$ (A)')
    axes[1,1].set_xlabel('时间 (ms)')
    axes[1,1].grid(True, alpha=0.3)
    axes[1,1].annotate('电流稳定可控', xy=(20, np.mean(i_with_fwd)*0.8), fontsize=10, color='darkgreen',
                      bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9))

    fig.suptitle(f'单相桥式半控整流——电感性负载对比  α={α}°', fontsize=14, fontweight='bold')
    for ax_row in axes:
        for ax in ax_row:
            ax.set_xticks(np.arange(0, 41, 5))
            ax.set_xlim(0, 40)

    plt.tight_layout()
    fig.savefig(os.path.join(IMG_DIR, '08_bridge_half_inductive_comparison.png'))
    plt.close(fig)
    print("[OK] Fig 8: 桥式半控整流（电感负载，有无续流对比）")


# ============================================================
# Figure 9: 三相桥式整流
# ============================================================
def fig_threephase_bridge():
    t = np.linspace(0, T, 2000)
    # Three phase voltages
    ua = Um * np.sin(ω * t)
    ub = Um * np.sin(ω * t - 2*np.pi/3)
    uc = Um * np.sin(ω * t + 2*np.pi/3)

    # Line-to-line voltages
    uab = ua - ub
    ubc = ub - uc
    uca = uc - ua

    # Three-phase bridge output (uncontrolled): max of line-to-line at any instant
    u_out = np.maximum(np.maximum(uab, ubc), uca)

    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

    # Phase voltages
    axes[0].plot(t*1000, ua, 'r', linewidth=1, label='$u_a$')
    axes[0].plot(t*1000, ub, 'g', linewidth=1, label='$u_b$')
    axes[0].plot(t*1000, uc, 'b', linewidth=1, label='$u_c$')
    axes[0].axhline(y=0, color='gray', linewidth=0.5)
    axes[0].set_ylabel('相电压 (V)')
    axes[0].set_title('三相桥式整流——相电压与输出电压', fontsize=13, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(loc='upper right', fontsize=8, ncol=3)

    # Output voltage (6-pulse)
    axes[1].fill_between(t*1000, 0, u_out, alpha=0.35, color='red')
    axes[1].plot(t*1000, u_out, 'r', linewidth=1.2)
    # Also show envelope lines
    axes[1].plot(t*1000, uab, 'gray', linewidth=0.4, alpha=0.3)
    axes[1].plot(t*1000, ubc, 'gray', linewidth=0.4, alpha=0.3)
    axes[1].plot(t*1000, uca, 'gray', linewidth=0.4, alpha=0.3)
    axes[1].axhline(y=0, color='gray', linewidth=0.5)
    axes[1].set_ylabel('$u_d$ (V)')
    axes[1].grid(True, alpha=0.3)
    axes[1].annotate('6脉波输出\n(300Hz纹波)', xy=(3, 450), fontsize=10,
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

    # Zoom: show the ripple
    axes[2].fill_between(t*1000, 0, u_out, alpha=0.35, color='red')
    axes[2].plot(t*1000, u_out, 'r', linewidth=1.2)
    axes[2].axhline(y=0, color='gray', linewidth=0.5)
    axes[2].set_ylabel('$u_d$ (V)')
    axes[2].set_xlabel('时间 (ms)')
    axes[2].grid(True, alpha=0.3)
    Ud_avg = 2.34 * (Um/np.sqrt(2))
    axes[2].axhline(y=Ud_avg, color='orange', linestyle='--', linewidth=1, alpha=0.7)
    axes[2].annotate(f'$U_d \\approx 2.34U_2 \\approx {Ud_avg:.0f}$V', xy=(3, Ud_avg+10), fontsize=10, color='orange')
    axes[2].annotate('纹波很小\n（±14%）', xy=(8, 470), fontsize=9,
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    axes[2].set_ylim(350, 550)

    for ax in axes:
        ax.set_xticks(np.arange(0, 21, 2))
        ax.set_xlim(0, 20)

    plt.tight_layout()
    fig.savefig(os.path.join(IMG_DIR, '09_threephase_bridge.png'))
    plt.close(fig)
    print("[OK] Fig 9: 三相桥式整流")


# ============================================================
# Figure 10: 波形对比汇总——四种典型情况
# ============================================================
def fig_waveform_comparison():
    t = np.linspace(0, 2*T, 5000)
    u_in = Um * np.sin(ω * t)
    α = 45
    α_rad = np.deg2rad(α)
    t_alpha = α_rad / ω

    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

    # (a) Half-wave, resistive
    u_a = np.where((u_in > 0) & (t % T >= t_alpha), u_in, 0)
    axes[0].fill_between(t*1000, 0, u_a, alpha=0.35, color='#e74c3c')
    axes[0].plot(t*1000, u_a, '#c0392b', linewidth=1.3)
    axes[0].plot(t*1000, u_in, 'lightblue', linewidth=0.5, alpha=0.4)
    axes[0].axhline(y=0, color='gray', linewidth=0.5)
    axes[0].set_ylabel('$u_d$')
    axes[0].set_title(f'(a) 单相半波 + 电阻负载　　导通角=π−α，断续', fontsize=11)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim(-350, 350)

    # (b) Half-wave, inductive with FWD (same voltage, but current is continuous)
    u_b = np.where((u_in > 0) & (t % T >= t_alpha), u_in, 0)
    axes[1].fill_between(t*1000, 0, u_b, alpha=0.35, color='#27ae60')
    axes[1].plot(t*1000, u_b, '#1e8449', linewidth=1.3)
    axes[1].plot(t*1000, u_in, 'lightblue', linewidth=0.5, alpha=0.4)
    axes[1].axhline(y=0, color='gray', linewidth=0.5)
    axes[1].set_ylabel('$u_d$')
    axes[1].set_title(f'(b) 单相半波 + 电感负载（带续流二极管）　电压同上，电流连续', fontsize=11)
    axes[1].grid(True, alpha=0.3)
    axes[1].set_ylim(-350, 350)

    # (c) Bridge full-controlled, resistive
    u_c = np.zeros(len(t))
    for k in range(len(t)):
        ωt_mod = (ω * t[k]) % (2 * np.pi)
        # VT1&4: α→π (conducts only while u_in>0, stops at π for resistive)
        if α_rad <= ωt_mod < np.pi:
            u_c[k] = u_in[k]
        # VT2&3: π+α→2π
        elif np.pi + α_rad <= ωt_mod < 2*np.pi:
            u_c[k] = -u_in[k]
    axes[2].fill_between(t*1000, 0, u_c, alpha=0.35, color='#2980b9')
    axes[2].plot(t*1000, u_c, '#1a5276', linewidth=1.3)
    axes[2].axhline(y=0, color='gray', linewidth=0.5)
    axes[2].set_ylabel('$u_d$')
    axes[2].set_title(f'(c) 单相桥式全控 + 电阻负载　　导通角=π−α，断续，两脉冲/周期', fontsize=11)
    axes[2].grid(True, alpha=0.3)
    axes[2].set_ylim(-10, 350)

    # (d) Bridge full-controlled, large inductive — CORRECTED
    # Each thyristor pair conducts 180° starting from its trigger angle
    vt14_on = np.zeros(len(t), dtype=bool)
    vt23_on = np.zeros(len(t), dtype=bool)
    for k in range(len(t)):
        ωt_mod = (ω * t[k]) % (2 * np.pi)
        if α_rad <= ωt_mod < α_rad + np.pi:
            vt14_on[k] = True
        if (ωt_mod >= α_rad + np.pi) or (ωt_mod < α_rad):
            vt23_on[k] = True
    u_d = np.where(vt14_on, u_in, -u_in)

    axes[3].fill_between(t*1000, 0, u_d, where=(u_d>=0), alpha=0.35, color='#8e44ad')
    axes[3].fill_between(t*1000, 0, u_d, where=(u_d<0), alpha=0.4, color='#3498db')
    axes[3].plot(t*1000, u_d, '#6c3483', linewidth=1.3)
    axes[3].axhline(y=0, color='gray', linewidth=0.5)
    axes[3].set_ylabel('$u_d$')
    axes[3].set_xlabel('时间 (ms)')
    axes[3].set_title(f'(d) 单相桥式全控 + 阻感负载　　导通角恒180°，含负向面积，α=90°时Ud=0', fontsize=11)
    axes[3].grid(True, alpha=0.3)
    axes[3].set_ylim(-350, 350)

    # Mark π and α
    for ax in axes:
        for n in [0, 1]:
            ax.axvline(x=(n*T + T/2)*1000, color='green', linestyle=':', linewidth=0.8, alpha=0.5)

    fig.suptitle(f'四种典型整流电路输出电压波形对比 (α={α}°)', fontsize=14, fontweight='bold', y=1.01)

    for ax in axes:
        ax.set_xticks(np.arange(0, 41, 5))
        ax.set_xlim(0, 40)

    plt.tight_layout()
    fig.savefig(os.path.join(IMG_DIR, '10_waveform_comparison.png'))
    plt.close(fig)
    print("[OK] Fig 10: 四种波形对比汇总")


# ============================================================
# Figure 11: α变化对Ud的影响曲线
# ============================================================
def fig_ud_vs_alpha():
    α = np.linspace(0, 180, 200)
    α_rad = np.deg2rad(α)

    # Half-wave resistive (and with FWD)
    ud_hw_r = Um / (2*np.pi) * (1 + np.cos(α_rad))
    # Bridge resistive
    ud_br_r = Um / np.pi * (1 + np.cos(α_rad))
    # Bridge large inductive
    ud_br_l = np.where(α <= 90, 2*Um/np.pi * np.cos(α_rad), 0)

    fig, ax = plt.subplots(1, 1, figsize=(9, 6))

    ax.plot(α, ud_hw_r, 'r', linewidth=2, label='单相半波（电阻/带续流二极管电感）')
    ax.plot(α, ud_br_r, 'b', linewidth=2, label='单相桥式全控（电阻负载）')
    ax.plot(α, ud_br_l, 'g', linewidth=2.5, label='单相桥式全控（大电感负载）')

    ax.axhline(y=0, color='gray', linewidth=0.8)
    ax.axvline(x=90, color='orange', linestyle='--', linewidth=1, alpha=0.7)
    ax.annotate('α=90°\n大电感 Ud=0\n>90° 逆变区', xy=(90, 5), fontsize=10, color='orange',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
                xytext=(105, 30), arrowprops=dict(arrowstyle='->', color='orange'))

    ax.set_xlabel('控制角 α (度)', fontsize=12)
    ax.set_ylabel('平均输出电压 $U_d$ (V)', fontsize=12)
    ax.set_title('控制角 α 对平均输出电压 $U_d$ 的影响', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=10)
    ax.set_xlim(0, 180)
    ax.set_ylim(-20, 350)

    # Shade the inverter region
    ax.axvspan(90, 180, alpha=0.08, color='red')
    ax.text(135, 180, '逆变区\n(桥式全控)', ha='center', fontsize=11, color='red', alpha=0.6)

    plt.tight_layout()
    fig.savefig(os.path.join(IMG_DIR, '11_ud_vs_alpha.png'))
    plt.close(fig)
    print("[OK] Fig 11: α-Ud 关系曲线")


# ============================================================
# Figure 12: 电感大小对半波整流波形的影响
# ============================================================
def fig_inductance_effect():
    """Show how different L values affect the output waveform"""
    t = np.linspace(0, 2*T, 8000)  # High resolution
    dt = t[1] - t[0]
    u_in = Um * np.sin(ω * t)
    α = 60
    α_rad = np.deg2rad(α)
    R = 5.0        # Consistent with fixed Fig 3

    L_values = [0.005, 0.03, 0.08]  # H — small, medium, large
    labels = ['小电感 (L=5mH, τ=1ms)', '中等电感 (L=30mH, τ=6ms)', '大电感 (L=80mH, τ=16ms)']
    colors = ['#2e86c1', '#e67e22', '#c0392b']

    fig, axes = plt.subplots(len(L_values), 2, figsize=(13, 10), sharex=True)

    for idx, (L, label, color) in enumerate(zip(L_values, labels, colors)):
        # --- Fixed simulation (same logic as Fig 3) ---
        i = np.zeros(len(t))
        scr_on = np.zeros(len(t), dtype=bool)

        for k in range(1, len(t)):
            ωt_curr = (ω * t[k]) % (2 * np.pi)
            ωt_prev = (ω * t[k-1]) % (2 * np.pi)

            if ωt_prev < ωt_curr:
                crossed_alpha = (ωt_prev < α_rad <= ωt_curr)
            else:
                crossed_alpha = (ωt_prev < α_rad) or (α_rad <= ωt_curr)

            if crossed_alpha and ωt_curr < np.pi and u_in[k] > 0:
                scr_on[k] = True
            elif scr_on[k-1]:
                if i[k-1] > 1e-3:
                    scr_on[k] = True
                else:
                    scr_on[k] = False
            else:
                scr_on[k] = False

            if scr_on[k]:
                di = (u_in[k] - R * i[k-1]) / L * dt
                i[k] = max(0.0, i[k-1] + di)
            else:
                i[k] = 0.0

        u_out = np.where(scr_on, u_in, 0.0)

        # Voltage (left column)
        axes[idx, 0].plot(t*1000, u_in, 'lightgray', linewidth=0.4, alpha=0.4)
        axes[idx, 0].fill_between(t*1000, 0, u_out, where=(u_out>=0), alpha=0.3, color='#e74c3c')
        axes[idx, 0].fill_between(t*1000, 0, u_out, where=(u_out<0), alpha=0.4, color='#3498db')
        axes[idx, 0].plot(t*1000, u_out, color, linewidth=1.3)
        axes[idx, 0].axhline(y=0, color='gray', linewidth=0.5)
        axes[idx, 0].set_ylabel('$u_d$ (V)')
        axes[idx, 0].set_title(f'{label} —— 输出电压', fontsize=11)
        axes[idx, 0].grid(True, alpha=0.3)
        axes[idx, 0].set_ylim(-350, 350)

        # Mark π
        for n in [0, 1]:
            axes[idx, 0].axvline(x=(n*T + T/2)*1000, color='green', linestyle=':', linewidth=1, alpha=0.6)

        # Find θ_off for annotation
        for n in [0, 1]:
            cycle_mask = (t >= n*T) & (t < (n+1)*T)
            cycle_idx_ = np.where(cycle_mask)[0]
            scr_in_cycle = scr_on[cycle_idx_]
            if np.any(scr_in_cycle):
                last_on = cycle_idx_[np.where(scr_in_cycle)[0][-1]]
                cutoff_ms = t[last_on] * 1000
                if cutoff_ms > (n*T + T/2)*1000 + 0.5:
                    axes[idx, 0].axvline(x=cutoff_ms, color='purple', linestyle='--', linewidth=0.8, alpha=0.7)

        # Current (right column)
        axes[idx, 1].fill_between(t*1000, 0, i, alpha=0.3, color=color)
        axes[idx, 1].plot(t*1000, i, color, linewidth=1.5)
        axes[idx, 1].axhline(y=0, color='gray', linewidth=0.5)
        axes[idx, 1].set_ylabel('$i_d$ (A)')
        axes[idx, 1].set_title(f'{label} —— 输出电流', fontsize=11)
        axes[idx, 1].grid(True, alpha=0.3)

        # Mark π on current plots too
        for n in [0, 1]:
            axes[idx, 1].axvline(x=(n*T + T/2)*1000, color='green', linestyle=':', linewidth=1, alpha=0.6)

        # Annotate peak current
        if max(i) > 1:
            axes[idx, 1].annotate(f'峰值 {max(i):.1f}A', xy=(t[np.argmax(i)]*1000, max(i)),
                                fontsize=8, color=color,
                                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

    axes[-1, 0].set_xlabel('时间 (ms)')
    axes[-1, 1].set_xlabel('时间 (ms)')

    fig.suptitle(f'电感大小对单相半波可控整流波形的影响（无续流二极管，α={α}°）', fontsize=14, fontweight='bold')
    for ax_row in axes:
        for ax in ax_row:
            ax.set_xticks(np.arange(0, 41, 5))
            ax.set_xlim(0, 40)

    plt.tight_layout()
    fig.savefig(os.path.join(IMG_DIR, '12_inductance_effect.png'))
    plt.close(fig)
    print("[OK] Fig 12: 电感大小影响")


# ============================================================
if __name__ == '__main__':
    print("Generating waveform diagrams...")
    print("=" * 50)
    fig_halfwave_uncontrolled()
    fig_halfwave_controlled_resistive()
    fig_halfwave_inductive_no_fwd()
    fig_halfwave_inductive_with_fwd()
    fig_bridge_full_resistive()
    fig_bridge_full_inductive()
    fig_bridge_alpha_comparison()
    fig_bridge_half_inductive()
    fig_threephase_bridge()
    fig_waveform_comparison()
    fig_ud_vs_alpha()
    fig_inductance_effect()
    print("=" * 50)
    print(f"\nAll {12} figures saved to: {IMG_DIR}")
