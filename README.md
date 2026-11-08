# Active Matter in Laminar Flow

When tiny organisms like bacteria (*E. coli*) or sperm cells swim in water, they don't just drift around like dust. They consume internal energy to move forward. In nature, fluids rarely stay still—they form whirlpools (vortices) and shear currents. This project is a Python simulation studying how self-propelled particles move, get trapped, and disperse through a 2D grid of vortices.

Instead of treating swimmers as simple points, this model investigates the impact of realistic shapes and biological behaviors.

### Project Outline

1. **Particle Shape**: Most bacteria are rod-shaped (ellipsoids) rather than spheres. Under fluid shear, elongated swimmers align with the flow, gradually moving out of vortex centers to cluster along the boundaries between neighboring vortices. Spherical particles do not aggregate—they remain uniformly spread.

2. **Vortex Trapping and Escape**: Vortices act as hydrodynamic cages. A swimmer needs a threshold speed to cross into an adjacent cell. Rod-shaped particles escape at much lower speeds than spheres because their elongation allows them to catch boundary shear and slingshot across.

3. **Chirality (Natural Turning)**: Many microswimmers have asymmetrical bodies or flagella that make them turn constantly in circles. Swimmers whose turning matches the vortex rotation stay trapped longer, while those turning against it escape quickly. This enables passive cell sorting in microfluidic channels using flow alone.

4. **Noise and Flow Fluctuations**: Collisions with fluid molecules (rotational diffusion) and time-dependent flow oscillations shake swimmers loose from vortex cages, allowing them to explore wider territory.

Simulations are implemented with a vectorized second-order Runge-Kutta scheme in Python.

### References

1. G. B. Jeffery, *The Motion of Ellipsoidal Particles Immersed in a Viscous Fluid*, Proc. R. Soc. Lond. A **102**, 161–179 (1922).
2. C. Torney and Z. Neufeld, *Transport and Aggregation of Self-Propelled Particles in Fluid Flows*, Phys. Rev. Lett. **99**, 078101 (2007).
3. C. Bechinger et al., *Active Particles in Complex and Crowded Environments*, Rev. Mod. Phys. **88**, 045006 (2016).
4. T. J. Whitney and K. A. Mitchell, *Ballistic to Diffusive Transition for Swimmers in a Periodic Vortex Array*, Phys. Rev. E **110**, 034203 (2024).
