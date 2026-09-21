# Rejected arguments and known failure modes

This is a quarantine list. Automated agents should not resurrect these arguments without explicitly fixing the stated defect.

## R1 — Leaf in every violated clause

**Rejected:** “Every violated clause in a linear 3-uniform hypertree has a degree-1 variable.”

A linear hypertree can contain an internal clause whose three variables all continue into distinct branches.

## R2 — All positive projected equilibria have zero energy

**Refuted:** an exact four-clause hypertree has

[
Phi(x^*)=1,qquad 
ablaPhi(x^*)=0.
]

See the adversarial audit in `Publicacoes/`.

## R3 — Unrestricted negative Hessian eigenvalue proves boundary instability

**Rejected:** the negative eigenvector may be infeasible.

Second-order reasoning must be on the critical cone.

## R4 — C1 impact maps preserve null sets under inverse image

**Rejected:** a C1 map can pull a null set back to positive measure without a rank/nondegeneracy hypothesis. Projected flows also lose invertibility at the boundary.

## R5 — Semialgebraic critical set of low dimension implies null basin

**Rejected:** a point attractor can have an open basin. Geometry of the critical set alone does not control basin measure.

## R6 — No local minimum implies no open basin

**Rejected:** degenerate gradient systems can converge to a non-minimum from a one-sided open set. Dynamics must be analyzed.

## R7 — Finite trajectory length implies finite-time face identification

**Rejected:** a finite-length trajectory can approach a boundary asymptotically.

## R8 — Liouville alone eliminates normally attracting faces

**Rejected:** divergence-free tangential dynamics can coexist with strict normal attraction. M6 is the current exact example.

## R9 — Lower bound implies decay

**Rejected:** (ho(alpha)=Omega(alpha^k)) gives no upper bound and does not imply (ho(alpha)	o0).

## R10 — Overlapping embedding covariance controls the full second moment

**Rejected:** disjoint embeddings contribute covariance too, especially in (H_3(N,M)) where the total number of edges is fixed.

## R11 — Numerical non-discovery proves minimality

**Rejected:** L-BFGS-B, finite grids, Monte Carlo, and bounded searches can miss narrow/degenerate faces.

## R12 — Gemini/Codex agreement is proof

**Rejected:** cross-model agreement does not close a mathematical obligation. Exact proof or exact refutation is required.

## R13 — Automatic theorem promotion

**Rejected:** the automated lab may emit `PROVED` as an agent verdict, but only a human-reviewed update may add that claim to `CERTIFIED_FACTS.md` or the official manuscript.
