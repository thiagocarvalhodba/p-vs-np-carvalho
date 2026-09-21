"""Adversarial search for positive projected equilibria of CLG multilinear Phi.

This is a *falsification* tool.  It enumerates rooted linear 3-uniform
hypertrees built by attaching a new clause through one old vertex, quotients
literal polarities by vertex-sign gauge, and checks the KKT conditions of the
box exactly whenever a rational candidate is considered.  Numerical root
finding is discovery only; a reported hit is always rechecked with ``Fraction``.

The search is exhaustive only for the finite families printed by the command
line report.  In particular it does not prove a universal statement when no
hit is found.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Iterable, Iterator, Sequence

import numpy as np


RATIONAL_GRID = (Fraction(-1), Fraction(-1, 2), Fraction(0), Fraction(1, 2), Fraction(1))

# The first exact counterexample, in the u=x+1 coordinates of the box.
COUNTEREXAMPLE_EDGES = ((0, 1, 2), (0, 3, 4), (1, 5, 6), (2, 7, 8))
COUNTEREXAMPLE_SIGNS = ((1, 1, 1), (-1, 1, 1), (-1, 1, 1), (-1, 1, 1))


@dataclass(frozen=True)
class Certificate:
    edges: tuple[tuple[int, int, int], ...]
    signs: tuple[tuple[int, int, int], ...]
    x: tuple[Fraction, ...]
    phi: Fraction
    gradient: tuple[Fraction, ...]


def counterexample_delta_exact(u: Sequence[Fraction]) -> Fraction:
    """Exact Phi(-1+u)-Phi(-1) for the four-clause counterexample.

    The expression is the complete Taylor polynomial (degree three), not an
    asymptotic truncation.  Its degree-two part is indefinite on u >= 0.
    """
    if len(u) != 9:
        raise ValueError("the counterexample has nine variables")
    q = (u[0] * u[1] + u[0] * u[2] + u[1] * u[2]) / 4
    q -= (u[0] * (u[3] + u[4]) + u[1] * (u[5] + u[6]) + u[2] * (u[7] + u[8])) / 4
    cubic = -u[0] * u[1] * u[2] / 8
    cubic += (u[0] * u[3] * u[4] + u[1] * u[5] * u[6] + u[2] * u[7] * u[8]) / 8
    return q + cubic


def counterexample_leaf_velocity_exact(u: Sequence[Fraction], leaf: int) -> Fraction:
    """Exact PDS velocity of one of the six leaves in u=x+1 coordinates.

    Leaves are 3,...,8.  Their gradient is nonpositive everywhere on the
    orthant, so the tangent-cone projection does not change -grad Phi.
    """
    branches = {3: (0, 4), 4: (0, 3), 5: (1, 6), 6: (1, 5), 7: (2, 8), 8: (2, 7)}
    if leaf not in branches:
        raise ValueError("leaf must be one of 3,...,8")
    center, sibling = branches[leaf]
    return u[center] * (1 - u[sibling] / 2) / 4


def attachment_trees(num_clauses: int) -> Iterator[tuple[tuple[int, int, int], ...]]:
    """Generate labelled rooted attachment trees (duplicates are intentional).

    Each new edge shares exactly one existing vertex and introduces two new
    vertices.  Thus every output is connected, linear and Berge-acyclic.
    """
    if num_clauses < 1:
        return

    def rec(edges: tuple[tuple[int, int, int], ...], next_vertex: int):
        if len(edges) == num_clauses:
            yield edges
            return
        vertices = sorted({v for edge in edges for v in edge})
        for attachment in vertices:
            yield from rec(edges + ((attachment, next_vertex, next_vertex + 1),), next_vertex + 2)

    yield from rec(((0, 1, 2),), 3)


def gauge_sign_patterns(edges: Sequence[Sequence[int]]) -> Iterator[tuple[tuple[int, int, int], ...]]:
    """One representative of every literal-sign orbit under x_i -> eps_i x_i.

    Make the sign at a variable's first occurrence positive.  In an attachment
    tree only the shared variable of every later edge remains free, leaving
    exactly 2^(m-1) representatives for m clauses.
    """
    shared_positions = [(edge_index, 0) for edge_index in range(1, len(edges))]
    for choices in product((-1, 1), repeat=len(shared_positions)):
        signs = [[1, 1, 1] for _ in edges]
        for (edge_index, position), value in zip(shared_positions, choices):
            signs[edge_index][position] = value
        yield tuple(tuple(row) for row in signs)


def phi_grad_exact(
    edges: Sequence[Sequence[int]], signs: Sequence[Sequence[int]], x: Sequence[Fraction]
) -> tuple[Fraction, tuple[Fraction, ...]]:
    n = max(v for edge in edges for v in edge) + 1
    phi = Fraction(0)
    gradient = [Fraction(0) for _ in range(n)]
    for edge, edge_signs in zip(edges, signs):
        factors = [(1 - sign * x[v]) / 2 for v, sign in zip(edge, edge_signs)]
        phi += factors[0] * factors[1] * factors[2]
        for position, (vertex, sign) in enumerate(zip(edge, edge_signs)):
            other = Fraction(1)
            for other_position, factor in enumerate(factors):
                if other_position != position:
                    other *= factor
            gradient[vertex] -= Fraction(sign, 2) * other
    return phi, tuple(gradient)


def projected_equilibrium_exact(x: Sequence[Fraction], gradient: Sequence[Fraction]) -> bool:
    """Exact KKT test for Proj_{T_[-1,1]^n}(-grad Phi)=0.

    At +1, allowed velocity is <=0, hence -grad<=0 and grad>=0 is NOT
    correct: projection is zero iff -grad>=0 (outward), i.e. grad<=0.
    At -1 the corresponding condition is grad>=0.
    """
    for xi, gi in zip(x, gradient):
        if -1 < xi < 1:
            if gi != 0:
                return False
        elif xi == 1:
            if gi > 0:
                return False
        elif xi == -1:
            if gi < 0:
                return False
        else:
            raise ValueError("candidate is outside the box")
    return True


def projected_velocity_box_exact(x: Sequence[Fraction], gradient: Sequence[Fraction]) -> tuple[Fraction, ...]:
    """Coordinate projection of -gradient onto the tangent cone of the box."""
    velocity: list[Fraction] = []
    for xi, gi in zip(x, gradient):
        raw = -gi
        if xi == 1:
            velocity.append(min(raw, Fraction(0)))
        elif xi == -1:
            velocity.append(max(raw, Fraction(0)))
        elif -1 < xi < 1:
            velocity.append(raw)
        else:
            raise ValueError("candidate is outside the box")
    return tuple(velocity)


def certificate_if_positive_equilibrium(
    edges: Sequence[Sequence[int]], signs: Sequence[Sequence[int]], x: Sequence[Fraction]
) -> Certificate | None:
    phi, gradient = phi_grad_exact(edges, signs, x)
    if phi > 0 and projected_equilibrium_exact(x, gradient):
        return Certificate(tuple(map(tuple, edges)), tuple(map(tuple, signs)), tuple(x), phi, gradient)
    return None


def exhaustive_vertex_search(max_clauses: int = 5) -> tuple[Certificate | None, dict[int, int]]:
    """Exact exhaustive search of all vertices and gauge polarity orbits."""
    counts: dict[int, int] = {}
    for m in range(1, max_clauses + 1):
        checked = 0
        for edges in attachment_trees(m):
            n = 2 * m + 1
            for signs in gauge_sign_patterns(edges):
                for x in product((Fraction(-1), Fraction(1)), repeat=n):
                    checked += 1
                    hit = certificate_if_positive_equilibrium(edges, signs, x)
                    if hit is not None:
                        return hit, counts | {m: checked}
        counts[m] = checked
    return None, counts


def rational_grid_search(max_clauses: int = 3) -> tuple[Certificate | None, dict[int, int]]:
    """Exhaustive rational-grid search, deliberately bounded to small trees."""
    counts: dict[int, int] = {}
    for m in range(1, max_clauses + 1):
        checked = 0
        for edges in attachment_trees(m):
            n = 2 * m + 1
            for signs in gauge_sign_patterns(edges):
                for x in product(RATIONAL_GRID, repeat=n):
                    checked += 1
                    hit = certificate_if_positive_equilibrium(edges, signs, x)
                    if hit is not None:
                        return hit, counts | {m: checked}
        counts[m] = checked
    return None, counts


def is_linear_acyclic_attachment_tree(edges: Sequence[Sequence[int]]) -> bool:
    """Independent structural validator for the attachment-tree family."""
    if not edges or len(set(edges[0])) != 3:
        return False
    seen_vertices = set(edges[0])
    for edge in edges[1:]:
        if len(set(edge)) != 3 or len(set(edge) & seen_vertices) != 1:
            return False
        seen_vertices.update(edge)
    return True


def format_certificate(certificate: Certificate) -> str:
    return "\n".join(
        [
            "EXACT COUNTEREXAMPLE CERTIFICATE",
            f"edges = {certificate.edges}",
            f"signs = {certificate.signs}",
            f"x = {certificate.x}",
            f"Phi(x) = {certificate.phi} > 0",
            f"grad Phi(x) = {certificate.gradient}",
            "KKT / tangent-cone projection: verified exactly.",
        ]
    )


def main() -> int:
    vertex_hit, vertex_counts = exhaustive_vertex_search(5)
    print("exact vertex search through 5 clauses:", vertex_counts)
    if vertex_hit:
        print(format_certificate(vertex_hit))
        return 1
    grid_hit, grid_counts = rational_grid_search(3)
    print("exact five-point rational-grid search through 3 clauses:", grid_counts)
    if grid_hit:
        print(format_certificate(grid_hit))
        return 1
    print("NO HIT in the stated finite searches; this is not a proof for all hypertrees.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
