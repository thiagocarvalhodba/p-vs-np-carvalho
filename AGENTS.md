# AGENTS.md — CLG-R Mathematical Research Lab

## Mission

This repository contains an active mathematical research program. The agent's job is not to preserve a preferred theorem. The job is to determine what is true.

The automated research loop is under `research_lab/`. Before working on the current claim, read:

1. `research_lab/CURRENT_CLAIM.md`
2. `research_lab/CERTIFIED_FACTS.md`
3. `research_lab/OPEN_OBLIGATIONS.md`
4. `research_lab/REJECTED_ARGUMENTS.md`
5. `research_lab/runtime/WORKING_STATE.md` if it exists.

## Epistemic rules

Use only these statuses:

- **PROVED** — complete mathematical chain, including every external theorem hypothesis or an exact internal proof.
- **REFUTED** — exact counterexample/certificate or a rigorous contradiction.
- **CONDITIONAL** — conclusion follows only if explicitly named unresolved hypotheses hold.
- **COMPUTATIONAL_ONLY** — finite/numerical computation supports the claim but does not prove the universal statement.
- **OPEN** — neither proof nor refutation is complete.

Never promote a claim because multiple agents agree. Agreement is evidence, not proof.

Never infer a universal theorem from a finite search. Floating-point optimization, eigenvalues, Monte Carlo, L-BFGS-B, IVP solvers, SMT without a certificate, and bounded enumeration are discovery/evidence unless the searched domain is itself proved exhaustive and arithmetic is certified.

## Adversarial standard

For every proposed proof:

1. Identify the weakest implication.
2. Try to build the smallest counterexample.
3. Check feasibility of every direction used in constrained second-order reasoning.
4. On a box boundary, use the tangent cone and the **critical cone**, not the unrestricted Hessian.
5. Distinguish:
   - existence of equilibrium,
   - local minimum,
   - Lyapunov stability,
   - asymptotic stability,
   - positive-measure basin,
   - open basin,
   - almost-everywhere convergence.
6. If a face is involved, separate tangential dynamics from normal attraction.
7. If a probabilistic limit is claimed, separate expectation, convergence in probability, w.h.p./a.a.s., and almost-sure statements.
8. If literature is used, name the exact theorem and map every hypothesis.

## Current mathematical safety checks

Do not repeat any of these known invalid moves:

- “negative unrestricted Hessian eigenvalue => feasible escape at a box boundary”;
- “C1 impact map => null preimages are null” without rank/nondegeneracy;
- “semialgebraic critical set of low dimension => basin has measure zero”;
- “no local minimum => no positive-measure basin”;
- “finite length => active face is reached in finite time”;
- “lower bound Omega(alpha^k) => function tends to zero”;
- “overlapping embeddings have negative covariance => total variance is O(N)” without treating disjoint pairs.

See `research_lab/REJECTED_ARGUMENTS.md`.

## Agent roles

### Constructor
Find the strongest rigorous proof, exact family, or exact counterexample. Prefer symbolic identities and explicit invariant regions.

### Adversarial referee
Try to destroy the claim. Do not repair the proof until the failure mode is explicit.

### Computation auditor
Use computation only to discover candidates or to certify a finite exhaustive domain. Prefer rational/exact arithmetic, symbolic elimination, interval certificates, and reproducible scripts.

### Literature verifier
Verify primary sources, exact theorem numbers, definitions, and hypothesis translation.

### Adjudicator
Consolidate only claims that survived adversarial review. Unresolved obligations remain OPEN.

## Repository safety

Automated research agents must not:

- push,
- merge,
- rewrite `main`,
- change theorem status in the official manuscripts,
- delete files,
- modify existing publication files.

The automated loop runs Codex read-only and Gemini in Plan/read-only mode. It may write only its own local runtime artifacts under `research_lab/rounds/` and `research_lab/runtime/` through the orchestrator process.

Human review is required before promoting any result into `Publicacoes/`.

## Output discipline

Every research report should contain:

- exact claim audited;
- verdict;
- proof/counterexample chain;
- assumptions;
- exact certificates;
- computational evidence separated from proof;
- surviving obligations;
- next cheapest decisive test.

If the theorem is false, refuting it is success.
