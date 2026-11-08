"""
Demonstration: Chiral Symmetry Breaking and Microfluidic Vorticity Sorting.
Quantifies how intrinsic turning torque (chirality C) breaks spatial symmetry and biases vortex residence.
"""

import sys
import os
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from active_matter import (
    simulate_ensemble,
    compute_vorticity,
    compute_vorticity_pdf_ratio,
    set_visual_style,
)


def run_chirality_analysis(num_particles=5000, timesteps=4000, dt=0.01, output_dir="output"):
    """
    Computes sampled fluid vorticity for non-chiral (C = 0) vs chiral (C = 0.3) microswimmers.
    Plots normalized probability ratio P(omega) / P0(omega) demonstrating co-rotating vortex preference.
    """
    os.makedirs(output_dir, exist_ok=True)
    np.random.seed(42)
    L = 2.0 * np.pi
    
    # Generate uniform spatial reference sample to establish geometric baseline P0(omega)
    X_uniform = np.random.uniform(0.0, L, size=(num_particles, 2))
    vorticity_uniform = compute_vorticity(X_uniform[:, 0], X_uniform[:, 1], L=L)
    
    # 1. Non-chiral particles (C = 0.0): Symmetrical sampling of clockwise and counter-clockwise cells
    print("Simulating non-chiral particles (C = 0.0)...")
    X0 = np.random.uniform(0.0, L, size=(num_particles, 3))
    traj_nonchiral, _ = simulate_ensemble(
        X0, dt=dt, nt=timesteps, nsave=timesteps, U0=1.0, vp=0.15, alpha=0.99, chirality=0.0, wrap_pbc=True
    )
    vort_nonchiral = compute_vorticity(traj_nonchiral[-1, :, 0], traj_nonchiral[-1, :, 1], L=L)
    
    # 2. Chiral particles (C = 0.3): Intrinsic turning rate aligns with co-rotating vortex flow
    print("Simulating chiral particles (C = 0.3)...")
    traj_chiral, _ = simulate_ensemble(
        X0, dt=dt, nt=timesteps, nsave=timesteps, U0=1.0, vp=0.15, alpha=0.99, chirality=0.3, wrap_pbc=True
    )
    vort_chiral = compute_vorticity(traj_chiral[-1, :, 0], traj_chiral[-1, :, 1], L=L)
    
    # Compute normalized probability density ratios
    bins_nc, ratio_nc, _, _ = compute_vorticity_pdf_ratio(vort_nonchiral, vorticity_uniform, nbins=25)
    bins_c, ratio_c, _, _ = compute_vorticity_pdf_ratio(vort_chiral, vorticity_uniform, nbins=25)
    
    # Render comparative ratio plot
    set_visual_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), sharey=True)
    
    # Non-chiral ratio remains centered and symmetric around zero vorticity
    ax1.plot(bins_nc, ratio_nc, color="#2b2d42", linewidth=2.0)
    ax1.fill_between(bins_nc, ratio_nc, color="#8d99ae", alpha=0.4)
    ax1.set_xlabel(r"Vorticity ($\omega$)")
    ax1.set_ylabel(r"Ratio $P(\omega) / P_0(\omega)$")
    ax1.set_title("Non-Chiral (C = 0.0) - Symmetric", fontsize=11)
    ax1.grid(True, linestyle=":", alpha=0.5)
    
    # Chiral ratio shows clear bias toward co-rotating vortex sign
    ax2.plot(bins_c, ratio_c, color="#d90429", linewidth=2.0)
    ax2.fill_between(bins_c, ratio_c, color="#ef233c", alpha=0.4)
    ax2.set_xlabel(r"Vorticity ($\omega$)")
    ax2.set_title("Chiral (C = 0.3) - Vorticity Selective", fontsize=11)
    ax2.grid(True, linestyle=":", alpha=0.5)
    
    plt.tight_layout()
    save_path = os.path.join(output_dir, "chirality_vorticity_sorting.png")
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Chirality analysis complete! Saved to '{save_path}'.")


if __name__ == "__main__":
    run_chirality_analysis()
