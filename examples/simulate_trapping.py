"""
Demonstration: Shape-Driven Aggregation and Separatrix Clustering.
Compares spherical microswimmers (alpha = 0) with elongated ellipsoidal swimmers (alpha = 0.99).
"""

import sys
import os
import numpy as np

# Ensure parent directory is in Python path for local package import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from active_matter import simulate_ensemble, plot_particles_2d


def run_trapping_comparison(num_particles=2000, timesteps=3000, dt=0.01, output_dir="output"):
    """
    Simulates spherical vs elongated particles to demonstrate phase space contraction.
    Spheres remain uniform (Liouville theorem); ellipsoids cluster along vortex separatrices.
    """
    os.makedirs(output_dir, exist_ok=True)
    np.random.seed(42)
    
    # Initialize random positions uniformly across [0, 2pi] domain with random heading angles
    X0 = np.random.uniform(0.0, 2.0 * np.pi, size=(num_particles, 3))
    
    # 1. Spherical particles (alpha = 0.0): Phase space divergence is identically zero
    print("Simulating spherical particles (alpha = 0.0)...")
    traj_sphere, _ = simulate_ensemble(
        X0, dt=dt, nt=timesteps, nsave=timesteps, U0=1.0, vp=0.05, alpha=0.0, wrap_pbc=True
    )
    plot_particles_2d(
        traj_sphere[-1],
        title="Spherical Particles (alpha = 0.0) - Uniform Distribution",
        save_path=os.path.join(output_dir, "spherical_distribution.png"),
    )
    
    # 2. Ellipsoidal particles (alpha = 0.99): Jeffrey alignment contracts phase space
    print("Simulating elongated ellipsoidal particles (alpha = 0.99)...")
    traj_ellipsoid, _ = simulate_ensemble(
        X0, dt=dt, nt=timesteps, nsave=timesteps, U0=1.0, vp=0.05, alpha=0.99, wrap_pbc=True
    )
    plot_particles_2d(
        traj_ellipsoid[-1],
        title="Ellipsoidal Particles (alpha = 0.99) - Separatrix Aggregation",
        save_path=os.path.join(output_dir, "ellipsoid_aggregation.png"),
    )
    
    print(f"Trapping comparison complete! Plots saved in '{output_dir}/'.")


if __name__ == "__main__":
    run_trapping_comparison()
