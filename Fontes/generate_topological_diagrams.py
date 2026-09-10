# -*- coding: utf-8 -*-
"""
generate_topological_diagrams.py
Generates publication-quality SVG and PNG topological figures for Project CLG-R:
Figure 1: Central Fractional Box Theorem & LP Integrality Gap (Håstad 7/8)
Figure 2: Harmonic Multilinear Landscape, Interior Saddles & Vertex Confinement
Figure 3: Softplus Global Convexity vs Thermodynamic Bifurcation (beta -> inf)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import Rectangle, FancyArrowPatch
import mpl_toolkits.mplot3d.art3d as art3d

output_dir = r"C:\MathDoCarvalho\P_NP\Publicacoes"
os.makedirs(output_dir, exist_ok=True)

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'cm'

# ==============================================================================
# FIGURE 1: Central Fractional Box Theorem & LP Integrality Gap
# ==============================================================================
print("Generating Figure 1: Central Fractional Box Theorem...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

# Panel A: 2D Section of Hypercube [-1, 1]^2 and Central Box (-1/3, 1/3)^2
ax1.set_xlim(-1.15, 1.15)
ax1.set_ylim(-1.15, 1.15)
ax1.set_aspect('equal')

# Domain boundary [-1, 1]^2
cube = Rectangle((-1, -1), 2, 2, fill=False, edgecolor='#1E293B', linewidth=2, linestyle='-', label=r'Hypercube $\mathcal{X} = [-1, 1]^2$')
ax1.add_patch(cube)

# Central Fractional Box U_N = (-1/3, 1/3)^2
box = Rectangle((-1/3, -1/3), 2/3, 2/3, fill=True, facecolor='#10B981', alpha=0.35, edgecolor='#059669', linewidth=2, linestyle='--', label=r'Central Box $\mathcal{U}_N = (-1/3, 1/3)^N$ ($\nabla \Phi_{\rm quad} \equiv \mathbf{0}$)')
ax1.add_patch(box)

# Origin and Slack
ax1.plot(0, 0, 'o', color='#0F172A', markersize=8, label=r'Origin $x=\mathbf{0}$ (LP Slack $= 0.5$)')
ax1.annotate(r'$\mathbf{x=0}$' + '\n' + r'Slack $= 0.5$' + '\n' + r'(LP 7/8 Gap)', 
             xy=(0, 0), xytext=(0.08, 0.08),
             fontsize=10, fontweight='bold', color='#0F172A',
             arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.5))

# Negative Orthant where sign(x) = (-1, -1) violates clause (x1 or x2)
violated_orthant = Rectangle((-1/3, -1/3), 1/3, 1/3, fill=True, facecolor='#EF4444', alpha=0.45, edgecolor='#DC2626', linewidth=1.5, hatch='//', label=r'Spurious Plateau $\mathcal{C}_0$ ($E_{\rm disc} \geq 1, \nabla\Phi \equiv \mathbf{0}$)')
ax1.add_patch(violated_orthant)

# Clause Inactivity Boundary Plane x1 + x2 = -1
x_line = np.linspace(-1, 0, 100)
y_line = -1 - x_line
ax1.plot(x_line, y_line, color='#D97706', linewidth=2.5, linestyle='-', label=r'Clause Boundary $g_c(x) = 0 \Leftrightarrow x_1+x_2 = -1$')
ax1.fill_between(x_line, y_line, -1, color='#F59E0B', alpha=0.15, label=r'Active Clause Zone ($g_c(x) > 0$)')

# Vector Field (Drift Flow towards LP polytope)
Y, X = np.mgrid[-1:1:15j, -1:1:15j]
U = np.zeros_like(X)
V = np.zeros_like(Y)
mask_active = (X + Y < -1)
U[mask_active] = -0.5 * (X[mask_active] + Y[mask_active] + 1)
V[mask_active] = -0.5 * (X[mask_active] + Y[mask_active] + 1)
ax1.quiver(X, Y, U, V, color='#2563EB', alpha=0.65, width=0.005, scale=5.0, label=r'Drift Flow $-\nabla\Phi_{\rm quad}$')

ax1.axhline(0, color='#94A3B8', linestyle=':', lw=1)
ax1.axvline(0, color='#94A3B8', linestyle=':', lw=1)
ax1.set_xlabel(r'Coordinate $x_1$', fontsize=11, fontweight='bold')
ax1.set_ylabel(r'Coordinate $x_2$', fontsize=11, fontweight='bold')
ax1.set_title(r'(A) Geometry of Central Fractional Box $\mathcal{U}_N$' + '\n' + r'and Spurious Plateau $\mathcal{C}_0(\Phi_{\rm quad})$', fontsize=12, fontweight='bold', pad=10)
ax1.legend(loc='upper right', fontsize=8, framealpha=0.95)
ax1.grid(True, linestyle='--', alpha=0.3)

# Panel B: Volume Scaling of Central Box vs Dimension N
N_vals = np.arange(1, 21)
vol_box_norm = (1/3)**N_vals
vol_unsat_norm = (2/3)**N_vals
lp_gap = np.full_like(N_vals, 7/8, dtype=float)

ax2.semilogy(N_vals, vol_unsat_norm, 'o-', color='#059669', lw=2.5, label=r'UNSAT Plateau Volume: $\mu(\mathcal{C}_0) / 2^N \geq (2/3)^N$')
ax2.semilogy(N_vals, vol_box_norm, 's--', color='#DC2626', lw=2.5, label=r'Single-Orthant Universal Bound: $(1/3)^N$')
ax2.axhline(0.04, color='#7C3AED', linestyle='-.', lw=2, label=r'Empirical $R_{\rm dyn}$ at $N=60$ ($4.0\%$)')


ax2.set_xlabel(r'Dimension $N$ (Number of Variables)', fontsize=11, fontweight='bold')
ax2.set_ylabel(r'Normalized Measure / Volume Fraction', fontsize=11, fontweight='bold')
ax2.set_title(r'(B) Exponential Volume Scaling and Drift Retention' + '\n' + r'Connecting $\mu(\mathcal{C}_0)$ to Empirical Stagnation', fontsize=12, fontweight='bold', pad=10)
ax2.grid(True, which="both", ls="--", alpha=0.4)
ax2.legend(loc='upper right', fontsize=9, framealpha=0.95)

plt.tight_layout()
fig1_png = os.path.join(output_dir, "fig_clg_teorema1_caixa_fracionaria.png")
fig1_svg = os.path.join(output_dir, "fig_clg_teorema1_caixa_fracionaria.svg")
plt.savefig(fig1_png, dpi=300)
plt.savefig(fig1_svg)
plt.close()
print(f"Figure 1 saved: {fig1_png}")

# ==============================================================================
# FIGURE 2: Harmonic Multilinear Landscape & Vertex Confinement
# ==============================================================================
print("Generating Figure 2: Harmonic Landscape & Vertex Confinement...")
fig = plt.figure(figsize=(15, 6), dpi=300)

# Panel A: 3D Surface of Multilinear Harmonic Saddle
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
x1 = np.linspace(-1, 1, 40)
x2 = np.linspace(-1, 1, 40)
X1, X2 = np.meshgrid(x1, x2)
# Canonical multilinear saddle for (x1 or x2): Phi = (1 - x1)(1 - x2)/4
Z = (1 - X1) * (1 - X2) / 4.0

surf = ax1.plot_surface(X1, X2, Z, cmap=cm.coolwarm, alpha=0.85, edgecolor='none')
ax1.plot([0], [0], [0.25], 'ro', markersize=8, label=r'Interior Critical Saddle ($\Delta\Phi \equiv 0$)')

# Draw hypercube boundary lines on 3D
ax1.plot([-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1], [1, 0, 0, 0, 1], color='#0F172A', lw=2)

ax1.set_xlabel(r'$x_1$', fontsize=10, fontweight='bold')
ax1.set_ylabel(r'$x_2$', fontsize=10, fontweight='bold')
ax1.set_zlabel(r'$\Phi_{\rm mult}(x)$', fontsize=10, fontweight='bold')
ax1.set_title(r'(A) Harmonic Multilinear Saddle' + '\n' + r'$\Delta\Phi = \frac{\partial^2\Phi}{\partial x_1^2} + \frac{\partial^2\Phi}{\partial x_2^2} \equiv 0$ (No Interior Minima)', fontsize=11, fontweight='bold')
ax1.view_init(elev=28, azim=-125)

# Panel B: Projected Gradient Flow and Vertex Confinement on Hypercube
ax2 = fig.add_subplot(1, 2, 2)
ax2.set_xlim(-1.2, 1.2)
ax2.set_ylim(-1.2, 1.2)
ax2.set_aspect('equal')

# Cube boundary
cube2 = Rectangle((-1, -1), 2, 2, fill=False, edgecolor='#1E293B', linewidth=2.5)
ax2.add_patch(cube2)

# Vector Field of Multilinear Gradient Flow
Y2, X2 = np.mgrid[-0.95:0.95:18j, -0.95:0.95:18j]
U2 = -( -(1 - Y2)/4.0 ) # -dPhi/dx1 = (1-x2)/4
V2 = -( -(1 - X2)/4.0 ) # -dPhi/dx2 = (1-x1)/4
ax2.quiver(X2, Y2, U2, V2, color='#3B82F6', alpha=0.7, width=0.004, scale=3.5, label=r'Interior Hyperbolic Flow $\dot{x} = -\nabla\Phi_{\rm mult}$')

# Projected Flow on Boundaries (Arrows along edges pointing to vertices)
ax2.annotate('', xy=(1, 0.95), xytext=(1, 0), arrowprops=dict(arrowstyle="->", color="#DC2626", lw=2.5))
ax2.annotate('', xy=(0.95, 1), xytext=(0, 1), arrowprops=dict(arrowstyle="->", color="#DC2626", lw=2.5))
ax2.annotate('', xy=(-0.95, 1), xytext=(0, 1), arrowprops=dict(arrowstyle="->", color="#DC2626", lw=2.5))
ax2.annotate('', xy=(-1, 0.95), xytext=(-1, 0), arrowprops=dict(arrowstyle="->", color="#DC2626", lw=2.5))

# Vertices (Attractors of Projected Flow)
vertices = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
for vx, vy in vertices:
    if (vx, vy) == (1, 1):
        ax2.plot(vx, vy, 'o', color='#059669', markersize=12, label=r'True Satisfying Vertex $(+1, +1)$')
    else:
        ax2.plot(vx, vy, 's', color='#DC2626', markersize=10)

ax2.plot([], [], 's', color='#DC2626', label=r'Spurious Vertex Attractors $\{-1, 1\}^2$')
ax2.plot(0, 0, 'rX', markersize=10, label=r'Interior Saddle ($m=1$, Unstable)')

ax2.axhline(0, color='#94A3B8', linestyle=':', lw=1)
ax2.axvline(0, color='#94A3B8', linestyle=':', lw=1)
ax2.set_xlabel(r'Coordinate $x_1$', fontsize=11, fontweight='bold')
ax2.set_ylabel(r'Coordinate $x_2$', fontsize=11, fontweight='bold')
ax2.set_title(r'(B) Teorema da Localização Estrita nos Vértices' + '\n' + r'All Projected Minima Confined to $\{-1, +1\}^N$ (Theorem 4)', fontsize=11, fontweight='bold')
ax2.legend(loc='lower left', fontsize=8.5, framealpha=0.95)
ax2.grid(True, linestyle='--', alpha=0.3)

plt.tight_layout()
fig2_png = os.path.join(output_dir, "fig_clg_teorema3_4_harmonic_saddles_vertices.png")
fig2_svg = os.path.join(output_dir, "fig_clg_teorema3_4_harmonic_saddles_vertices.svg")
plt.savefig(fig2_png, dpi=300)
plt.savefig(fig2_svg)
plt.close()
print(f"Figure 2 saved: {fig2_png}")

# ==============================================================================
# FIGURE 3: Softplus Convexity vs Thermodynamic Bifurcation (beta -> inf)
# ==============================================================================
print("Generating Figure 3: Softplus Convexity and Bifurcation...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

# Panel A: 1D Energy Slice along Coordinate Trajectory
u = np.linspace(-2, 2, 400)
g_u = -0.5 * (1 + u) # Violation function

hinge_linear = np.maximum(0, g_u)
hinge_quad = hinge_linear**2

ax1.plot(u, hinge_quad, 'k-', lw=3, label=r'Quadratic Hinge $\Phi_{\rm quad} = [\max(0, g_c)]^2$ (Zero Plateau for $u \geq -1$)')

betas = [1.0, 3.0, 8.0, 20.0]
colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444']

for b, c in zip(betas, colors):
    softplus_val = (1.0 / b) * np.log(1.0 + np.exp(b * g_u))
    ax1.plot(u, softplus_val, lw=2, color=c, label=rf'Softplus $\Phi_{{\rm soft}}$ ($\beta = {b}$)')

ax1.axvline(-1, color='#64748B', linestyle='--', lw=1.5, label=r'Clause Boundary $g_c(u) = 0$ ($u = -1$)')
ax1.set_xlabel(r'Coordinate Projection $u = \sum \sigma_j x_j$', fontsize=11, fontweight='bold')
ax1.set_ylabel(r'Relaxation Potential Energy Value', fontsize=11, fontweight='bold')
ax1.set_title(r'(A) Homotopy from Global Convex Funnel to Flat Plateau' + '\n' + r'$\lim_{\beta \to \infty} \Phi_{\rm soft,\beta}(x) = \Phi_{\rm hinge}(x)$ (Theorem 6)', fontsize=11, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.4)
ax1.legend(loc='upper right', fontsize=8.5, framealpha=0.95)

# Panel B: Hessian Curvature Collapse & Lipschitz Growth
b_range = np.linspace(0.5, 30, 200)
# Curvature in central box (u = 0, g = -0.5)
g_center = -0.5
sigma_val = 1.0 / (1.0 + np.exp(-b_range * g_center))
# Curvature = beta/4 * sigma * (1 - sigma)
curvature_center = (b_range / 4.0) * sigma_val * (1.0 - sigma_val)
lipschitz_const = (3.0 / 16.0) * b_range * 13 # d_max approx 13

ax2_twin = ax2.twinx()

line1 = ax2.plot(b_range, curvature_center, 'g-', lw=2.5, label=r'Center Curvature $\frac{\partial^2\Phi}{\partial x_i^2}(\mathbf{0}) \sim \beta e^{-\beta \delta} \to 0$')
line2 = ax2_twin.plot(b_range, lipschitz_const, 'r--', lw=2.5, label=r'Lipschitz Constant $L_\beta = \Theta(\beta)$ (Stiffness)')

# Optimal Operating Window [2, 10]
ax2.axvspan(2.0, 10.0, color='#10B981', alpha=0.15, label=r'Optimal Navigability Window $\beta \in [2.0, 10.0]$')

ax2.set_xlabel(r'Inverse Temperature Smoothing Parameter $\beta$', fontsize=11, fontweight='bold')
ax2.set_ylabel(r'Central Hessian Curvature $\nabla^2_{ii} \Phi(\mathbf{0})$', color='#059669', fontsize=11, fontweight='bold')
ax2_twin.set_ylabel(r'Gradient Lipschitz Bound $L_\beta$', color='#DC2626', fontsize=11, fontweight='bold')
ax2.set_title(r'(B) Curvature Collapse vs Lipschitz Stiffness' + '\n' + r'Thermodynamic Phase Transition and Machine Underflow', fontsize=11, fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.4)

# Combine legends
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax2.legend(lines, labels, loc='center right', fontsize=8.5, framealpha=0.95)

plt.tight_layout()
fig3_png = os.path.join(output_dir, "fig_clg_teorema5_6_softplus_convexity_bifurcation.png")
fig3_svg = os.path.join(output_dir, "fig_clg_teorema5_6_softplus_convexity_bifurcation.svg")
plt.savefig(fig3_png, dpi=300)
plt.savefig(fig3_svg)
plt.close()
print(f"Figure 3 saved: {fig3_png}")

print("All 3 topological diagrams successfully generated in PNG and SVG!")
