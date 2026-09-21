# Current claim under audit

## Primary claim

For the projected gradient flow of the natural multilinear 3-SAT extension on **linear 3-uniform hypertrees**,

[
m_{*,HT}^{mathrm{mult}} = 6,
]

where (m_{*,HT}^{mathrm{mult}}) is the minimum number of clauses in a finite connected linear 3-uniform hypertree that admits an **open bad basin**: an open set of initial conditions of positive Lebesgue measure whose omega-limit rounds to a Boolean assignment with positive residual clause error.

## What is already enough to prove the upper bound

The six-clause construction M6 is a candidate exact certificate with:

- two active clauses sharing one free central variable (v);
- four boundary variables (b_{ij});
- four anchoring clauses;
- eight leaf variables;
- a positive tangentially flat face;
- strict normal attraction on an explicit open bootstrap region.

The research loop must re-audit the M6 certificate but should treat the explicit algebra in `CERTIFIED_FACTS.md` as the current baseline.

## Equality still requires a lower bound

To prove equality, exclude **every** open bad basin on every linear 3-uniform hypertree with (mle5).

A valid proof must not be restricted to:

- vertices;
- one free variable;
- one “central” violated clause;
- forces of magnitude exactly (1/2);
- isolated point attractors;
- finite-time identification of the final face.

## Latest claims that require independent audit

Gemini has proposed:

1. an Egorov–Liouville “volumetric cascade” intended to reduce any positive-volume basin to a vertex or a tangentially flat normally attracting face;
2. a combinatorial exclusion of such vertices/faces for (mle5);
3. a second-moment argument for the density of isolated M6 components.

These are **not certified merely because they were proposed**. In particular, audit:

- whether positive volume in the ambient cube necessarily produces positive relative measure on a single invariant face;
- hitting-time maps, tangencies, trajectories that approach a face only asymptotically, and repeated face switching;
- whether the Liouville argument applies on the required measurable sets;
- the full covariance contribution of disjoint M6 embeddings in (H_3(N,M)).

## Secondary probabilistic target

Under the candidate M6 count,

[
rac{mathbb E X_{M6}}{N}
sim
rac{729}{64}alpha^6 e^{-39alpha},
]

and an explicit certified sub-basin gives (p_{M6}ge 2^{-96}). If the count is correct, the expected residual-density lower bound is

[
liminf_{N	oinfty}mathbb E[ho_{mathrm{mult},N}(alpha)]
ge
rac{729}{2^{102}}alpha^5e^{-39alpha}.
]

The second-moment/concentration upgrade is separate from the deterministic minimality theorem.

## Success criteria

The round succeeds if it does at least one of the following:

- constructs an exact M5 (or smaller) open bad basin;
- proves a rigorous reduction theorem covering all PDS trajectories relevant to a positive-volume basin;
- proves the static (mle5) exclusion after the reduction;
- gives an exact flaw/counterexample to the proposed global reduction;
- closes the M6 component count and second moment rigorously.

Do not optimize for preserving (m_*=6). Optimize for truth.
