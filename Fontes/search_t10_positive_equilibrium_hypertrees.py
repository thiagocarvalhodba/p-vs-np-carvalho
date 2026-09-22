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
from math import comb
import sys
from typing import Iterable, Iterator, Sequence

import numpy as np


RATIONAL_GRID = (Fraction(-1), Fraction(-1, 2), Fraction(0), Fraction(1, 2), Fraction(1))

# The first exact counterexample, in the u=x+1 coordinates of the box.
COUNTEREXAMPLE_EDGES = ((0, 1, 2), (0, 3, 4), (1, 5, 6), (2, 7, 8))
COUNTEREXAMPLE_SIGNS = ((1, 1, 1), (-1, 1, 1), (-1, 1, 1), (-1, 1, 1))

# A seven-clause hypertree with an open basin converging in finite time to a
# positive, twelve-dimensional equilibrium family.  Each central variable has
# two leaf branches with the opposite polarity at the attachment vertex.
POSITIVE_BASIN_EDGES = (
    (0, 1, 2),
    (0, 3, 4),
    (0, 5, 6),
    (1, 7, 8),
    (1, 9, 10),
    (2, 11, 12),
    (2, 13, 14),
)
POSITIVE_BASIN_SIGNS = ((1, 1, 1),) + ((-1, 1, 1),) * 6

# A smaller six-clause "double core" counterexample.  In the adapted factor
# coordinates its potential is
#   y*u1*u2 + (1-y)*v1*v2
#   + (1-u1)*a1*b1 + (1-u2)*a2*b2
#   + (1-v1)*c1*d1 + (1-v2)*c2*d2.
DOUBLE_CORE_EDGES = (
    (0, 1, 2),
    (0, 3, 4),
    (1, 5, 6),
    (2, 7, 8),
    (3, 9, 10),
    (4, 11, 12),
)
DOUBLE_CORE_SIGNS = ((1, 1, 1),) + ((-1, 1, 1),) * 5
DOUBLE_CORE_AUTOMORPHISM_ORDER = 2 * 2**2 * 2**4
DOUBLE_CORE_GAUGE_ORBIT_SIZE = 2**13


@dataclass(frozen=True)
class Certificate:
    edges: tuple[tuple[int, int, int], ...]
    signs: tuple[tuple[int, int, int], ...]
    x: tuple[Fraction, ...]
    phi: Fraction
    gradient: tuple[Fraction, ...]


def vertex_degrees(edges: Sequence[Sequence[int]]) -> dict[int, int]:
    """Return incidence degrees in a finite hypergraph."""
    degrees: dict[int, int] = {}
    for edge in edges:
        for vertex in edge:
            degrees[vertex] = degrees.get(vertex, 0) + 1
    return degrees


def leafless_edges(edges: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    """Edges all of whose vertices have incidence degree at least two."""
    degrees = vertex_degrees(edges)
    return tuple(tuple(edge) for edge in edges if all(degrees[vertex] >= 2 for vertex in edge))


def branch_sizes_around_edge(
    edges: Sequence[Sequence[int]], core: Sequence[int]
) -> tuple[int, ...]:
    """Clause counts of components left after deleting ``core``.

    For a linear Berge tree and a leafless core, these are the nonempty branch
    sizes attached to the three distinct core vertices.
    """
    core_tuple = tuple(core)
    try:
        core_index = [tuple(edge) for edge in edges].index(core_tuple)
    except ValueError as exc:
        raise ValueError("core is not an edge") from exc
    remaining = [tuple(edge) for index, edge in enumerate(edges) if index != core_index]
    unseen = set(range(len(remaining)))
    sizes: list[int] = []
    while unseen:
        frontier = [unseen.pop()]
        component: set[int] = set()
        while frontier:
            index = frontier.pop()
            component.add(index)
            neighbours = {
                other
                for other in unseen
                if set(remaining[index]) & set(remaining[other])
            }
            unseen.difference_update(neighbours)
            frontier.extend(neighbours)
        touched = set(core_tuple) & {
            vertex for index in component for vertex in remaining[index]
        }
        if len(touched) != 1:
            raise ValueError("edges do not form branches of a linear Berge tree around core")
        sizes.append(len(component))
    return tuple(sorted(sizes))


def positive_basin_x_from_zq(
    z: Sequence[Fraction], q: Sequence[Fraction]
) -> tuple[Fraction, ...]:
    """Map the adapted coordinates of the seven-clause example back to x.

    The three central coordinates are ``z_i=(1+x_i)/2`` and the twelve
    leaves are ``q_l=(1-x_l)/2``.
    """
    if len(z) != 3 or len(q) != 12:
        raise ValueError("the positive-basin example has 3 central and 12 leaf coordinates")
    return tuple(2 * value - 1 for value in z) + tuple(1 - 2 * value for value in q)


def positive_basin_branch_sums_exact(q: Sequence[Fraction]) -> tuple[Fraction, ...]:
    """Return S_i=q_1 q_2+q_3 q_4 for each central branch pair."""
    if len(q) != 12:
        raise ValueError("the positive-basin example has 12 leaf coordinates")
    return tuple(q[4 * i] * q[4 * i + 1] + q[4 * i + 2] * q[4 * i + 3] for i in range(3))


def positive_basin_phi_zq_exact(z: Sequence[Fraction], q: Sequence[Fraction]) -> Fraction:
    """Exact potential of the seven-clause example in adapted coordinates."""
    if len(z) != 3:
        raise ValueError("the positive-basin example has 3 central coordinates")
    branch_sums = positive_basin_branch_sums_exact(q)
    central = (1 - z[0]) * (1 - z[1]) * (1 - z[2])
    return central + sum((z[i] * branch_sums[i] for i in range(3)), Fraction(0))


def positive_basin_delta_exact(z: Sequence[Fraction], q: Sequence[Fraction]) -> Fraction:
    """Exact ``Phi(z,q)-1`` identity used for the relative-minimum proof."""
    branch_sums = positive_basin_branch_sums_exact(q)
    linear = sum((z[i] * (branch_sums[i] - 1) for i in range(3)), Fraction(0))
    quadratic = z[0] * z[1] + z[0] * z[2] + z[1] * z[2]
    return linear + quadratic - z[0] * z[1] * z[2]


def positive_basin_projected_velocity_zq_exact(
    z: Sequence[Fraction], q: Sequence[Fraction]
) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    """Exact projected PDS field in the adapted unit-cube coordinates.

    The coordinate change from x contributes the common factor 1/4.  The
    result includes tangent-cone clipping at 0 and 1 in both z and q.
    """
    if len(z) != 3 or len(q) != 12:
        raise ValueError("the positive-basin example has 3 central and 12 leaf coordinates")
    branch_sums = positive_basin_branch_sums_exact(q)
    raw_z = []
    for i in range(3):
        others = [j for j in range(3) if j != i]
        raw_z.append(((1 - z[others[0]]) * (1 - z[others[1]]) - branch_sums[i]) / 4)

    raw_q: list[Fraction] = []
    for i in range(3):
        block = q[4 * i : 4 * i + 4]
        raw_q.extend(
            (
                -z[i] * block[1] / 4,
                -z[i] * block[0] / 4,
                -z[i] * block[3] / 4,
                -z[i] * block[2] / 4,
            )
        )

    def project_unit(value: Fraction, raw: Fraction) -> Fraction:
        if value == 0:
            return max(raw, Fraction(0))
        if value == 1:
            return min(raw, Fraction(0))
        if 0 < value < 1:
            return raw
        raise ValueError("adapted coordinate is outside [0,1]")

    return (
        tuple(project_unit(value, raw) for value, raw in zip(z, raw_z)),
        tuple(project_unit(value, raw) for value, raw in zip(q, raw_q)),
    )


def positive_basin_open_box_measure() -> Fraction:
    """Normalized Lebesgue measure of z_i in (0,1/16), q_l in (7/8,1)."""
    return Fraction(1, 16) ** 3 * Fraction(1, 8) ** 12


def double_core_x_from_factors(
    y: Fraction,
    u: Sequence[Fraction],
    v: Sequence[Fraction],
    leaves: Sequence[Fraction],
) -> tuple[Fraction, ...]:
    """Map the 13 adapted factors r=(1-x)/2 back to x coordinates."""
    if len(u) != 2 or len(v) != 2 or len(leaves) != 8:
        raise ValueError("the double-core example has 2 u, 2 v, and 8 leaf factors")
    factors = (y,) + tuple(u) + tuple(v) + tuple(leaves)
    return tuple(1 - 2 * factor for factor in factors)


def double_core_leaf_products_exact(leaves: Sequence[Fraction]) -> tuple[Fraction, ...]:
    """Products (a1*b1,a2*b2,c1*d1,c2*d2) in the double core."""
    if len(leaves) != 8:
        raise ValueError("the double-core example has 8 leaf factors")
    return tuple(leaves[2 * i] * leaves[2 * i + 1] for i in range(4))


def double_core_phi_exact(
    y: Fraction,
    u: Sequence[Fraction],
    v: Sequence[Fraction],
    leaves: Sequence[Fraction],
) -> Fraction:
    """Exact six-clause potential in double-core factor coordinates."""
    if len(u) != 2 or len(v) != 2:
        raise ValueError("the double-core example has 2 u and 2 v factors")
    a1, a2, c1, c2 = double_core_leaf_products_exact(leaves)
    return (
        y * u[0] * u[1]
        + (1 - y) * v[0] * v[1]
        + (1 - u[0]) * a1
        + (1 - u[1]) * a2
        + (1 - v[0]) * c1
        + (1 - v[1]) * c2
    )


def double_core_delta_exact(
    y: Fraction,
    u: Sequence[Fraction],
    v: Sequence[Fraction],
    leaves: Sequence[Fraction],
) -> Fraction:
    """Exact ``Phi-1`` decomposition proving a relative minimum valley."""
    a1, a2, c1, c2 = double_core_leaf_products_exact(leaves)
    pu = (1 - u[0], 1 - u[1])
    pv = (1 - v[0], 1 - v[1])
    return (
        pu[0] * (a1 - y)
        + pu[1] * (a2 - y)
        + y * pu[0] * pu[1]
        + pv[0] * (c1 - (1 - y))
        + pv[1] * (c2 - (1 - y))
        + (1 - y) * pv[0] * pv[1]
    )


def double_core_projected_velocity_exact(
    y: Fraction,
    u: Sequence[Fraction],
    v: Sequence[Fraction],
    leaves: Sequence[Fraction],
) -> tuple[Fraction, tuple[Fraction, ...], tuple[Fraction, ...], tuple[Fraction, ...]]:
    """Exact PDS field in the 13 adapted unit-cube factor coordinates."""
    if len(u) != 2 or len(v) != 2 or len(leaves) != 8:
        raise ValueError("the double-core example has 2 u, 2 v, and 8 leaf factors")
    a1, a2, c1, c2 = double_core_leaf_products_exact(leaves)
    raw_y = (v[0] * v[1] - u[0] * u[1]) / 4
    raw_u = ((a1 - y * u[1]) / 4, (a2 - y * u[0]) / 4)
    raw_v = (
        (c1 - (1 - y) * v[1]) / 4,
        (c2 - (1 - y) * v[0]) / 4,
    )
    raw_leaves: list[Fraction] = []
    deficits = (1 - u[0], 1 - u[1], 1 - v[0], 1 - v[1])
    for i, deficit in enumerate(deficits):
        left, right = leaves[2 * i : 2 * i + 2]
        raw_leaves.extend((-deficit * right / 4, -deficit * left / 4))

    def project_unit(value: Fraction, raw: Fraction) -> Fraction:
        if value == 0:
            return max(raw, Fraction(0))
        if value == 1:
            return min(raw, Fraction(0))
        if 0 < value < 1:
            return raw
        raise ValueError("adapted coordinate is outside [0,1]")

    factor_values = (y,) + tuple(u) + tuple(v) + tuple(leaves)
    raw_values = (raw_y,) + raw_u + raw_v + tuple(raw_leaves)
    projected = tuple(project_unit(value, raw) for value, raw in zip(factor_values, raw_values))
    return projected[0], projected[1:3], projected[3:5], projected[5:]


def double_core_open_box_measure() -> Fraction:
    """Measure of the certified capture box used for the six-clause example."""
    # y in (31/64,33/64); all other 12 factors in (15/16,1).
    return Fraction(1, 32) * Fraction(1, 16) ** 12


def double_core_expected_isolated_gauge_components(
    num_variables: int, num_clauses: int
) -> Fraction:
    """Exact expectation in the uniform distinct-signed-clause model.

    The sample space consists of ``num_clauses`` distinct clauses chosen from
    the ``8*C(N,3)`` signed 3-clauses.  We count isolated copies of the
    six-clause underlying hypergraph with any of its ``2^13`` variable-gauge
    signings.  Its unsigned automorphism group has order 128.
    """
    if num_variables < 13 or num_clauses < 6:
        return Fraction(0)
    total_signed = 8 * comb(num_variables, 3)
    outside_signed = 8 * comb(num_variables - 13, 3)
    if num_clauses > total_signed or num_clauses - 6 > outside_signed:
        return Fraction(0)
    falling_vertices = 1
    for value in range(num_variables - 12, num_variables + 1):
        falling_vertices *= value
    embeddings = Fraction(falling_vertices, DOUBLE_CORE_AUTOMORPHISM_ORDER)
    isolation_probability = Fraction(
        comb(outside_signed, num_clauses - 6), comb(total_signed, num_clauses)
    )
    return embeddings * DOUBLE_CORE_GAUGE_ORBIT_SIZE * isolation_probability


def double_core_expected_isolated_gauge_components_iid(
    num_variables: int, num_clauses: int
) -> Fraction:
    """Exact expectation in the iid signed-clause model.

    The six prescribed motif clauses occupy an ordered injection into the
    ``num_clauses`` sampling slots, and every remaining draw must avoid all
    thirteen motif variables.  Thus duplicate clauses are allowed globally,
    but not inside a counted isolated motif.
    """
    if num_variables < 13 or num_clauses < 6:
        return Fraction(0)
    total_signed = 8 * comb(num_variables, 3)
    outside_signed = 8 * comb(num_variables - 13, 3)
    falling_vertices = 1
    for value in range(num_variables - 12, num_variables + 1):
        falling_vertices *= value
    falling_slots = 1
    for value in range(num_clauses - 5, num_clauses + 1):
        falling_slots *= value
    embeddings = Fraction(falling_vertices, DOUBLE_CORE_AUTOMORPHISM_ORDER)
    sampling_probability = Fraction(
        falling_slots * outside_signed ** (num_clauses - 6),
        total_signed**num_clauses,
    )
    return embeddings * DOUBLE_CORE_GAUGE_ORBIT_SIZE * sampling_probability


def double_core_asymptotic_component_coefficient() -> Fraction:
    """Coefficient of ``alpha^6 exp(-39 alpha) N`` for gauge copies."""
    signed_embeddings = Fraction(
        DOUBLE_CORE_GAUGE_ORBIT_SIZE, DOUBLE_CORE_AUTOMORPHISM_ORDER
    )
    clause_density_scale = Fraction(3, 4) ** 6
    return signed_embeddings * clause_density_scale


def double_core_asymptotic_expected_residual_coefficient() -> Fraction:
    """Coefficient of the certified ``alpha^5 exp(-39 alpha)`` rho bound."""
    return double_core_asymptotic_component_coefficient() * double_core_open_box_measure()


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


def catalogue_positive_vertex_equilibria(
    max_clauses: int = 4,
    limit: int | None = None,
) -> tuple[list[Certificate], dict[int, int]]:
    """Catalogue exact positive *vertex* equilibria in the generated family.

    This is exhaustive over labelled attachment constructions and the stated
    gauge representatives, not an isomorphism quotient and not a catalogue of
    positive equilibria on higher-dimensional faces.
    """
    certificates: list[Certificate] = []
    counts: dict[int, int] = {}
    for m in range(1, max_clauses + 1):
        checked = 0
        for edges in attachment_trees(m):
            n = 2 * m + 1
            for signs in gauge_sign_patterns(edges):
                for x in product((Fraction(-1), Fraction(1)), repeat=n):
                    checked += 1
                    certificate = certificate_if_positive_equilibrium(edges, signs, x)
                    if certificate is not None:
                        certificates.append(certificate)
                        if limit is not None and len(certificates) >= limit:
                            counts[m] = checked
                            return certificates, counts
        counts[m] = checked
    return certificates, counts


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
    if len(sys.argv) == 2 and sys.argv[1] == "--catalogue-vertices-m4":
        certificates, counts = catalogue_positive_vertex_equilibria(4)
        print("exact positive-vertex catalogue through 4 clauses:", counts)
        print("number of certificates:", len(certificates))
        for certificate in certificates:
            print(format_certificate(certificate))
        return 0
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
