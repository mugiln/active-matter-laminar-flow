"""
High-quality visualization utilities for active matter flows and phase space dynamics.
Supports clean publication styling (white background) and 3Blue1Brown-inspired electric dark aesthetics.
"""

import matplotlib.pyplot as plt
import numpy as np


def set_visual_style(dark_mode=False):
    """
    Configures Matplotlib styling parameters for publication or electric presentation figures.
    """
    if dark_mode:
        plt.style.use("dark_background")
        plt.rcParams.update({
            "figure.facecolor": "black",
            "axes.facecolor": "black",
            "axes.edgecolor": "white",
            "axes.labelcolor": "white",
            "xtick.color": "white",
            "ytick.color": "white",
            "grid.color": "#333333",
            "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
        })
    else:
        plt.style.use("default")
        plt.rcParams.update({
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#333333",
            "axes.labelcolor": "#111111",
            "xtick.color": "#222222",
            "ytick.color": "#222222",
            "grid.color": "#e0e0e0",
            "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
        })


def plot_particles_2d(X, L=2.0 * np.pi, title="Particle Distribution", save_path=None, dark_mode=False):
    """
    Renders 2D particle positions with domain boundaries and separatrix dividers at pi.
    Highlights spatial clustering near vortex separatrices.
    """
    set_visual_style(dark_mode)
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Wrap coordinates into domain [0, L]
    x_wrapped = np.mod(X[:, 0], L)
    y_wrapped = np.mod(X[:, 1], L)
    
    color = "#08F7FE" if dark_mode else "#1f77b4"
    ax.scatter(x_wrapped, y_wrapped, s=2.5, alpha=0.8, color=color, edgecolors="none")
    
    # Draw separatrix lines dividing counter-rotating vortex cells
    vortex_boundary = L / 2.0
    line_color = "#555555" if dark_mode else "#cccccc"
    ax.axvline(vortex_boundary, color=line_color, linestyle="--", linewidth=1.0)
    ax.axhline(vortex_boundary, color=line_color, linestyle="--", linewidth=1.0)
    
    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")
    ax.set_title(title, fontsize=12, pad=10)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
        plt.close()
    else:
        plt.show()


def plot_quiver_field(U0=1.0, L=2.0 * np.pi, grid_points=20, save_path=None, dark_mode=False):
    """
    Plots velocity vector arrows across the cellular vortex grid showing alternating circulation.
    """
    from .flow import cellular_velocity
    set_visual_style(dark_mode)
    
    x = np.linspace(0, L, grid_points)
    y = np.linspace(0, L, grid_points)
    X_grid, Y_grid = np.meshgrid(x, y)
    
    vel = cellular_velocity(X_grid.ravel(), Y_grid.ravel(), U0=U0, L=L)
    u = vel[:, 0].reshape(grid_points, grid_points)
    v = vel[:, 1].reshape(grid_points, grid_points)
    
    fig, ax = plt.subplots(figsize=(6, 6))
    arrow_color = "#08F7FE" if dark_mode else "#2b5c8f"
    ax.quiver(X_grid, Y_grid, u, v, color=arrow_color, alpha=0.85, scale=25.0)
    
    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("2D Cellular Flow Field", fontsize=12)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
        plt.close()
    else:
        plt.show()


def plot_msd_scaling(time, msd_dict, title="Mean Squared Displacement vs Time", save_path=None, dark_mode=False):
    """
    Plots ensemble MSD curves on log-log axes to distinguish ballistic, diffusive, and trapped regimes.
    """
    set_visual_style(dark_mode)
    fig, ax = plt.subplots(figsize=(7, 5))
    
    palette = ["#ff595e", "#1982c4", "#6a4c93", "#ffca3a", "#8ac926"]
    for i, (label, msd) in enumerate(msd_dict.items()):
        c = palette[i % len(palette)]
        ax.loglog(time, msd, label=label, color=c, linewidth=2.0)
        
    ax.set_xlabel("Time (t)")
    ax.set_ylabel("Mean Squared Displacement <|r(t) - r(0)|^2>")
    ax.set_title(title, fontsize=12)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(frameon=True)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
        plt.close()
    else:
        plt.show()
