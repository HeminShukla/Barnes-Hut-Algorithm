# Barnes–Hut Algorithm

A Python implementation of the **Barnes–Hut Algorithm** for efficiently solving the **N-body problem** using a hierarchical quadtree data structure.

## Overview

The Barnes–Hut algorithm is a recursive approximation algorithm commonly used in computational physics, astrophysics, and molecular dynamics to simulate interactions between a large number of bodies.

Instead of calculating the force between every pair of particles (which requires **O(N²)** computations), the Barnes–Hut algorithm groups distant bodies together and approximates them as a single body located at their **centre of mass**. This reduces the computational complexity to approximately **O(N log N)** while maintaining high accuracy.

---

## How the Algorithm Works

### 1. Constructing the Quadtree

The simulation space is recursively divided into four equally sized regions, forming a **quadtree**.

- Every node represents a region of space.
- If a region contains more than one body, it is subdivided into four child nodes.
- This subdivision continues until each leaf node contains at most one body.

Each internal node stores:

- Total mass of all bodies within the region
- Centre of mass of those bodies
- References to its four child nodes

---

### 2. Force Calculation

To compute the gravitational force acting on a particle, the quadtree is traversed recursively.

For each node encountered:

- If the node is sufficiently far away, the entire region is treated as a **single body** located at its centre of mass.
- Otherwise, the node is opened and its children are examined individually.

This dramatically reduces the number of force calculations compared to evaluating every particle individually.

---

## Barnes–Hut Criterion

Whether a node can be approximated as a single body is determined using the ratio

***s / d***

where

- **s** = width of the region represented by the node
- **d** = distance from the particle to the node's centre of mass

This value is compared against a threshold parameter **θ (theta)**.

If

***s / d < θ***

the node is considered sufficiently far away and its entire mass is approximated by a single force calculation.

Otherwise, the algorithm recursively examines the node's children.

---

## Choosing θ

The parameter **θ** controls the balance between simulation accuracy and computational speed.

| θ | Behaviour |
|---|-----------|
| 0 | Equivalent to brute-force N-body calculation (highest accuracy, slowest) |
| Small | High accuracy with moderate speed-up |
| Large | Faster computation with reduced accuracy |

Typical values range between **0.5 and 1.0** depending on the required precision.

---

## Time Complexity

| Method | Complexity |
|---------|------------|
| Brute-force N-body | O(N²) |
| Barnes–Hut | O(N log N) (average case) |

The Barnes–Hut algorithm becomes significantly more efficient as the number of bodies increases.
---

## References

Barnes, J., & Hut, P. (1986). *A Hierarchical O(N log N) Force-Calculation Algorithm*. Nature, 324, 446–449.
