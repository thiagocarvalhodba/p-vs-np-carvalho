# Open obligations

The automated loop should prioritize the smallest decisive obligation.

## O1 — Global reduction theorem

Prove or refute:

> If an open positive-Lebesgue-measure set of initial conditions for the multilinear PDS on a box converges to positive-energy equilibria, then some positive-relative-measure part of the dynamics is captured by either a positive attracting vertex or a tangentially flat, normally attracting face.

The latest proposed proof uses an Egorov–Liouville “volumetric cascade”. Audit all transitions carefully.

Required subcases:

- trajectories remaining in the full interior forever;
- finite-time boundary hitting;
- asymptotic approach to a face without finite-time hitting;
- tangential hitting;
- leaving a face after hitting it;
- repeated or infinitely many face switches;
- normal velocity tending to zero;
- loss of injectivity/volume when dimension drops.

Do not reuse the previously rejected C1 impact-map null-preimage argument.

## O2 — Static exclusion for m <= 5

Conditional on a valid reduction theorem, exclude all positive attracting vertices and all positive tangentially flat normally attracting faces on linear 3-uniform hypertrees with at most five clauses.

A promising counting structure is:

- an active clause on a flat face contains at most one free coordinate;
- active clauses containing a free coordinate need cancellation by another active clause sharing that free coordinate;
- an inactive clause can provide nonzero normal restoring derivative to at most one active boundary variable;
- acyclicity/linearity constrain sharing.

Every combinatorial step must be formal and must cover arbitrary topology/polarity.

## O3 — Search for M5 or smaller

Try to refute minimality constructively.

Search exact face patterns, especially:

- two or more active clauses with shared free coordinates;
- faces of dimension at least 2;
- partially active clauses;
- non-1/2 normal forces;
- normally attracting continua;
- asymptotic rather than finite-time capture.

Numerics are candidate discovery only; exact certification is required.

## O4 — Exact M6 component count

Audit the candidate

[
rac{mathbb E X_{M6}}{N}
sim
rac{729}{64}alpha^6e^{-39alpha}.
]

Verify:

- automorphism group of the **signed** motif;
- gauge orbit counting under the exact ensemble convention;
- isolation factor;
- difference between (H_3(N,p)) and (H_3(N,M)).

## O5 — M6 second moment

Prove or refute

[
operatorname{Var}(X_{M6})=O(N)
]

in the exact random model.

Treat separately:

- identical embeddings;
- overlapping distinct embeddings;
- disjoint embeddings.

Do not assume disjoint isolated-component events are independent.

## O6 — PDS convergence source

If the deterministic minimality proof requires convergence of every bounded PDS trajectory to a point, verify an exact primary theorem applicable to

[
F=Phi+delta_{[-1,1]^N}.
]

Map every hypothesis. If an external theorem is unnecessary, prefer a direct proof.
