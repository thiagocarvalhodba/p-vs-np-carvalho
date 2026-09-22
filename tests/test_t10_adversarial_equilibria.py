from fractions import Fraction
from math import comb, factorial
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Fontes"))

from search_t10_positive_equilibrium_hypertrees import (
    DOUBLE_CORE_AUTOMORPHISM_ORDER,
    DOUBLE_CORE_EDGES,
    DOUBLE_CORE_GAUGE_ORBIT_SIZE,
    DOUBLE_CORE_SIGNS,
    POSITIVE_BASIN_EDGES,
    POSITIVE_BASIN_SIGNS,
    attachment_trees,
    branch_sizes_around_edge,
    catalogue_positive_vertex_equilibria,
    certificate_if_positive_equilibrium,
    counterexample_delta_exact,
    counterexample_leaf_velocity_exact,
    double_core_delta_exact,
    double_core_asymptotic_component_coefficient,
    double_core_asymptotic_expected_residual_coefficient,
    double_core_expected_isolated_gauge_components,
    double_core_expected_isolated_gauge_components_iid,
    double_core_leaf_products_exact,
    double_core_open_box_measure,
    double_core_phi_exact,
    double_core_projected_velocity_exact,
    double_core_x_from_factors,
    gauge_sign_patterns,
    is_linear_acyclic_attachment_tree,
    leafless_edges,
    phi_grad_exact,
    positive_basin_branch_sums_exact,
    positive_basin_delta_exact,
    positive_basin_open_box_measure,
    positive_basin_phi_zq_exact,
    positive_basin_projected_velocity_zq_exact,
    positive_basin_x_from_zq,
    projected_equilibrium_exact,
    projected_velocity_box_exact,
)


def test_projected_kkt_signs_at_each_box_boundary():
    assert projected_equilibrium_exact((Fraction(1),), (Fraction(-1),))
    assert not projected_equilibrium_exact((Fraction(1),), (Fraction(1),))
    assert projected_equilibrium_exact((Fraction(-1),), (Fraction(1),))
    assert not projected_equilibrium_exact((Fraction(-1),), (Fraction(-1),))
    assert projected_equilibrium_exact((Fraction(0),), (Fraction(0),))


def test_tangent_projection_and_kkt_zero_condition_agree_coordinatewise():
    x = (Fraction(1), Fraction(-1), Fraction(0))
    gradient = (Fraction(-2), Fraction(3), Fraction(0))
    assert projected_velocity_box_exact(x, gradient) == (Fraction(0), Fraction(0), Fraction(0))
    assert projected_equilibrium_exact(x, gradient)


def test_attachment_generator_is_linear_connected_and_acyclic():
    trees = list(attachment_trees(4))
    assert trees
    assert all(is_linear_acyclic_attachment_tree(tree) for tree in trees)


def test_gauge_reduction_has_two_to_m_minus_one_representatives():
    tree = next(attachment_trees(4))
    assert len(list(gauge_sign_patterns(tree))) == 8


def test_exact_phi_gradient_for_one_clause():
    edges = ((0, 1, 2),)
    signs = ((1, 1, 1),)
    x = (Fraction(-1), Fraction(-1), Fraction(-1))
    phi, grad = phi_grad_exact(edges, signs, x)
    assert phi == 1
    assert grad == (Fraction(-1, 2), Fraction(-1, 2), Fraction(-1, 2))
    assert not projected_equilibrium_exact(x, grad)


def test_non_tree_detector_rejects_two_edge_overlap():
    assert not is_linear_acyclic_attachment_tree(((0, 1, 2), (0, 1, 3)))


def test_exact_certificate_requires_positive_energy_and_kkt():
    edges = ((0, 1, 2),)
    signs = ((1, 1, 1),)
    assert certificate_if_positive_equilibrium(edges, signs, (Fraction(-1),) * 3) is None


def test_four_clause_hypertree_counterexample_has_an_exact_certificate():
    # Central edge has no leaf; each of its three variables continues into a
    # leaf edge.  This is linear, connected and Berge-acyclic.
    edges = ((0, 1, 2), (0, 3, 4), (1, 5, 6), (2, 7, 8))
    signs = ((1, 1, 1), (-1, 1, 1), (-1, 1, 1), (-1, 1, 1))
    candidate = certificate_if_positive_equilibrium(edges, signs, (Fraction(-1),) * 9)
    assert is_linear_acyclic_attachment_tree(edges)
    assert candidate is not None
    assert candidate.phi == 1
    assert candidate.gradient == (Fraction(0),) * 9


def test_counterexample_exact_boundary_expansion_has_both_signs():
    zero = (Fraction(0),) * 9
    assert counterexample_delta_exact(zero) == 0
    # Feasible directions u>=0: one raises and one lowers Phi exactly.
    raise_direction = (Fraction(1), Fraction(1)) + (Fraction(0),) * 7
    lower_direction = (Fraction(1), Fraction(0), Fraction(0), Fraction(1)) + (Fraction(0),) * 5
    assert counterexample_delta_exact(raise_direction) == Fraction(1, 4)
    assert counterexample_delta_exact(lower_direction) == Fraction(-1, 4)


def test_counterexample_leaf_velocities_are_nonnegative_on_the_box():
    u = (Fraction(1), Fraction(3, 2), Fraction(1, 2), Fraction(1), Fraction(1, 2), Fraction(0), Fraction(1), Fraction(3, 2), Fraction(0))
    assert all(counterexample_leaf_velocity_exact(u, leaf) >= 0 for leaf in range(3, 9))
    # A positive central displacement immediately forces its leaf outward.
    u_center_only = (Fraction(1),) + (Fraction(0),) * 8
    assert counterexample_leaf_velocity_exact(u_center_only, 3) == Fraction(1, 4)


def test_non_tree_control_has_a_positive_exact_equilibrium():
    # Same triple twice is non-linear; opposite polarities cancel at the origin.
    edges = ((0, 1, 2), (0, 1, 2))
    signs = ((1, 1, 1), (-1, -1, -1))
    candidate = certificate_if_positive_equilibrium(edges, signs, (Fraction(0),) * 3)
    assert not is_linear_acyclic_attachment_tree(edges)
    assert candidate is not None
    assert candidate.phi == Fraction(1, 4)


def test_vertex_catalogue_is_empty_through_three_clauses():
    certificates, counts = catalogue_positive_vertex_equilibria(3)
    assert certificates == []
    assert counts == {1: 8, 2: 192, 3: 7680}


def test_zero_clause_energy_does_not_imply_zero_clause_gradient():
    # This is the obstruction to a naive peeling induction: a satisfied leaf
    # clause may still exert force through the variable carrying its zero factor.
    edges = ((0, 1, 2),)
    signs = ((1, 1, 1),)
    phi, gradient = phi_grad_exact(edges, signs, (Fraction(1), Fraction(-1), Fraction(-1)))
    assert phi == 0
    assert gradient == (Fraction(-1, 2), Fraction(0), Fraction(0))


def test_seven_clause_hypertree_has_open_positive_basin_certificate():
    edges = (
        (0, 1, 2),
        (0, 3, 4), (0, 5, 6),
        (1, 7, 8), (1, 9, 10),
        (2, 11, 12), (2, 13, 14),
    )
    signs = (
        (1, 1, 1),
        (-1, 1, 1), (-1, 1, 1),
        (-1, 1, 1), (-1, 1, 1),
        (-1, 1, 1), (-1, 1, 1),
    )
    x = (Fraction(-1),) * 15
    phi, grad = phi_grad_exact(edges, signs, x)

    assert is_linear_acyclic_attachment_tree(edges)
    assert phi == 1
    assert grad[:3] == (Fraction(1, 2),) * 3
    assert grad[3:] == (Fraction(0),) * 12
    assert projected_equilibrium_exact(x, grad)

    # Exact bootstrap used in the analytic open-basin proof:
    # leaves below 1/4 imply each peripheral leaf-product >= 49/64,
    # hence each central gradient is >= 17/64.
    leaf_factor_min = Fraction(7, 8)
    branch_product_min = leaf_factor_min * leaf_factor_min
    two_branch_sum_min = 2 * branch_product_min
    central_grad_min = (two_branch_sum_min - 1) / 2
    assert branch_product_min == Fraction(49, 64)
    assert two_branch_sum_min == Fraction(49, 32)
    assert central_grad_min == Fraction(17, 64)

    # With initial central displacement <1/4, hitting time is <16/17.
    hit_time_max = Fraction(1, 4) / central_grad_min
    assert hit_time_max == Fraction(16, 17)

    # A leaf moves at speed <=u_center/4<=1/16, so from an initial
    # displacement <1/8 it remains below 1/4 before the center hits.
    leaf_displacement_max = Fraction(1, 16) * hit_time_max
    assert leaf_displacement_max == Fraction(1, 17)
    assert Fraction(1, 8) + leaf_displacement_max == Fraction(25, 136)
    assert Fraction(25, 136) < Fraction(1, 4)


def test_m16_core_trap_survives_degree_two_and_mixed_polarities():
    # Clause nodes V_k cycle through centers a,b,c five times.
    groups = tuple(i % 3 for i in range(15))
    edges = [(0, 1, 2)]
    signs = [(1, 1, 1)]
    # leaf ell_k = variable 3+k; V_k contains incoming ell_{k-1}
    # negatively and outgoing ell_k positively.
    for k, center in enumerate(groups):
        incoming = 3 + ((k - 1) % 15)
        outgoing = 3 + k
        edges.append((center, incoming, outgoing))
        signs.append((-1, -1, 1))

    x = (Fraction(-1),) * 3 + (Fraction(0),) * 15
    phi, grad = phi_grad_exact(tuple(edges), tuple(signs), x)

    # Linear hypergraph: no pair of clauses shares more than one variable.
    assert all(
        len(set(edges[i]).intersection(edges[j])) <= 1
        for i in range(len(edges))
        for j in range(i)
    )

    degrees = [0] * 18
    polarity_sets = [set() for _ in range(18)]
    for edge, sign in zip(edges, signs):
        for v, s in zip(edge, sign):
            degrees[v] += 1
            polarity_sets[v].add(s)

    assert min(degrees) >= 2
    assert degrees[:3] == [6, 6, 6]
    assert degrees[3:] == [2] * 15
    assert all(polarity_sets[v] == {-1, 1} for v in range(18))

    assert phi == 1
    assert grad[:3] == (Fraction(1, 8),) * 3
    assert grad[3:] == (Fraction(0),) * 15
    assert projected_equilibrium_exact(x, grad)

    # Exact open-basin bootstrap constants.
    eta = Fraction(1, 16)
    epsilon = Fraction(1, 32)
    factor_min = (1 - eta) / 2
    five_branch_sum_min = 5 * factor_min * factor_min
    center_grad_min = (five_branch_sum_min - 1) / 2
    assert factor_min == Fraction(15, 32)
    assert five_branch_sum_min == Fraction(1125, 1024)
    assert center_grad_min == Fraction(101, 2048)

    hit_time_max = epsilon / center_grad_min
    assert hit_time_max == Fraction(64, 101)

    leaf_speed_max = epsilon / 2
    leaf_drift_max = leaf_speed_max * hit_time_max
    assert leaf_drift_max == Fraction(1, 101)
    assert Fraction(1, 32) + leaf_drift_max < eta


def test_shared_leaf_m7_is_a_positive_trap_inside_the_degree_two_core():
    edges = (
        (0, 1, 2),
        (0, 8, 3),
        (1, 3, 4),
        (2, 4, 5),
        (0, 5, 6),
        (1, 6, 7),
        (2, 7, 8),
    )
    signs = (
        (1, 1, 1),
        (-1, 1, 1),
        (-1, 1, 1),
        (-1, 1, 1),
        (-1, 1, 1),
        (-1, 1, 1),
        (-1, 1, 1),
    )
    x = (Fraction(-1),) * 9
    phi, grad = phi_grad_exact(edges, signs, x)

    degrees = [0] * 9
    for edge in edges:
        for v in edge:
            degrees[v] += 1

    assert degrees[:3] == [3, 3, 3]
    assert degrees[3:] == [2] * 6
    assert min(degrees) == 2
    assert all(
        len(set(edges[i]).intersection(edges[j])) <= 1
        for i in range(len(edges))
        for j in range(i)
    )

    assert phi == 1
    assert grad[:3] == (Fraction(1, 2),) * 3
    assert grad[3:] == (Fraction(0),) * 6
    assert projected_equilibrium_exact(x, grad)

    center_grad_min = Fraction(17, 64)
    hit_time_max = Fraction(16, 17)
    shared_leaf_speed_max = Fraction(1, 8)
    shared_leaf_drift_max = shared_leaf_speed_max * hit_time_max
    assert shared_leaf_drift_max == Fraction(2, 17)
    assert Fraction(1, 8) + shared_leaf_drift_max == Fraction(33, 136)
    assert Fraction(33, 136) < Fraction(1, 4)
def test_leafless_edge_obstruction_classifies_all_attachment_trees_through_m4():
    # A positive clause at a projected equilibrium cannot contain a degree-one
    # variable.  Up to m=3 every edge has a leaf.  With m=4, a leafless edge
    # forces the unique central-edge/three-leaf-branches architecture.
    for m in range(1, 4):
        assert all(not leafless_edges(tree) for tree in attachment_trees(m))

    for tree in attachment_trees(4):
        cores = leafless_edges(tree)
        for core in cores:
            outer = [edge for edge in tree if tuple(edge) != core]
            assert len(cores) == 1
            assert sorted(len(set(core) & set(edge)) for edge in outer) == [1, 1, 1]
            assert {next(iter(set(core) & set(edge))) for edge in outer} == set(core)


def test_every_leafless_core_through_m5_has_singleton_branches():
    for tree in attachment_trees(4):
        for core in leafless_edges(tree):
            assert branch_sizes_around_edge(tree, core) == (1, 1, 1)
    for tree in attachment_trees(5):
        for core in leafless_edges(tree):
            assert branch_sizes_around_edge(tree, core) == (1, 1, 2)


def test_seven_clause_hypertree_has_positive_projected_vertex_minimum():
    x_star = (Fraction(-1),) * 15
    certificate = certificate_if_positive_equilibrium(
        POSITIVE_BASIN_EDGES, POSITIVE_BASIN_SIGNS, x_star
    )
    assert is_linear_acyclic_attachment_tree(POSITIVE_BASIN_EDGES)
    assert certificate is not None
    assert certificate.phi == 1
    assert certificate.gradient == (Fraction(1, 2),) * 3 + (Fraction(0),) * 12


def test_positive_basin_adapted_formula_matches_original_polynomial_exactly():
    z = (Fraction(1, 16), Fraction(1, 32), Fraction(1, 64))
    q = tuple(Fraction(7 + (i % 3), 10) for i in range(12))
    x = positive_basin_x_from_zq(z, q)
    phi, _ = phi_grad_exact(POSITIVE_BASIN_EDGES, POSITIVE_BASIN_SIGNS, x)
    assert positive_basin_phi_zq_exact(z, q) == phi
    assert positive_basin_delta_exact(z, q) == phi - 1


def test_positive_equilibrium_continuum_is_exact_and_twelve_dimensional():
    z = (Fraction(0),) * 3
    # This is an interior point of the open 12-dimensional set S_i>1.
    q = (Fraction(3, 4),) * 12
    assert positive_basin_branch_sums_exact(q) == (Fraction(9, 8),) * 3
    x = positive_basin_x_from_zq(z, q)
    certificate = certificate_if_positive_equilibrium(
        POSITIVE_BASIN_EDGES, POSITIVE_BASIN_SIGNS, x
    )
    assert certificate is not None
    assert certificate.phi == 1
    assert positive_basin_projected_velocity_zq_exact(z, q) == (
        (Fraction(0),) * 3,
        (Fraction(0),) * 12,
    )


def test_positive_continuum_has_a_certified_relative_minimum_neighborhood():
    # If every S_i>=1, the exact identity is a sum of nonnegative terms:
    # sum z_i(S_i-1) + sum_{i<j} z_i z_j - z_0 z_1 z_2.
    q = (Fraction(3, 4),) * 12
    for z in (
        (Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(1, 10), Fraction(0), Fraction(0)),
        (Fraction(1, 10), Fraction(1, 5), Fraction(1, 4)),
        (Fraction(1), Fraction(1), Fraction(1)),
    ):
        assert positive_basin_delta_exact(z, q) >= 0


def test_open_basin_box_has_exact_inward_rates_and_positive_measure():
    z = (Fraction(1, 32),) * 3
    q = (Fraction(15, 16),) * 12
    dz, dq = positive_basin_projected_velocity_zq_exact(z, q)
    assert all(value <= Fraction(-1, 16) for value in dz)
    assert all(value < 0 for value in dq)

    # Bootstrap constants used in the finite-time capture proof.  Starting
    # above 49/32, S_i cannot fall to 5/4 before z_i hits zero.
    assert 2 * Fraction(7, 8) ** 2 == Fraction(49, 32)
    assert Fraction(49, 32) - Fraction(1, 16) > Fraction(5, 4)
    assert positive_basin_open_box_measure() == Fraction(1, 2**48)


def test_vertex_catalogue_m4_regression_still_has_twelve_known_saddles():
    certificates, counts = catalogue_positive_vertex_equilibria(4)
    assert len(certificates) == 12
    assert counts[4] == 430080
    assert all(certificate.phi == 1 for certificate in certificates)


def test_six_clause_double_core_has_a_nine_dimensional_positive_continuum():
    y = Fraction(1, 2)
    u = v = (Fraction(1), Fraction(1))
    leaves = (Fraction(3, 4),) * 8
    x = double_core_x_from_factors(y, u, v, leaves)
    certificate = certificate_if_positive_equilibrium(DOUBLE_CORE_EDGES, DOUBLE_CORE_SIGNS, x)
    assert is_linear_acyclic_attachment_tree(DOUBLE_CORE_EDGES)
    assert double_core_leaf_products_exact(leaves) == (Fraction(9, 16),) * 4
    assert certificate is not None
    assert certificate.phi == 1
    assert certificate.gradient == (
        (Fraction(0),) + (Fraction(1, 32),) * 4 + (Fraction(0),) * 8
    )
    assert double_core_projected_velocity_exact(y, u, v, leaves) == (
        Fraction(0),
        (Fraction(0),) * 2,
        (Fraction(0),) * 2,
        (Fraction(0),) * 8,
    )


def test_double_core_adapted_formula_and_minimum_identity_are_exact():
    y = Fraction(17, 32)
    u = (Fraction(15, 16), Fraction(31, 32))
    v = (Fraction(7, 8), Fraction(29, 32))
    leaves = tuple(Fraction(3 + (i % 2), 5) for i in range(8))
    x = double_core_x_from_factors(y, u, v, leaves)
    phi, _ = phi_grad_exact(DOUBLE_CORE_EDGES, DOUBLE_CORE_SIGNS, x)
    assert double_core_phi_exact(y, u, v, leaves) == phi
    assert double_core_delta_exact(y, u, v, leaves) == phi - 1

    # In the equilibrium valley the four leaf products dominate their core
    # weights, so the exact decomposition is nonnegative for every feasible
    # one-sided displacement of u and v.
    valley_leaves = (Fraction(3, 4),) * 8
    assert double_core_delta_exact(
        Fraction(1, 2),
        (Fraction(9, 10), Fraction(4, 5)),
        (Fraction(7, 8), Fraction(3, 4)),
        valley_leaves,
    ) >= 0


def test_double_core_open_box_has_finite_time_capture_bounds():
    y = Fraction(1, 2)
    u = v = (Fraction(31, 32), Fraction(31, 32))
    leaves = (Fraction(31, 32),) * 8
    dy, du, dv, dleaves = double_core_projected_velocity_exact(y, u, v, leaves)
    assert dy == 0
    assert all(value >= Fraction(13, 256) for value in du + dv)
    assert all(value < 0 for value in dleaves)

    # Exact bootstrap for U: y in (31/64,33/64), u,v,leaves in (15/16,1).
    # In the larger envelope y in (7/16,9/16), leaves>7/8, capture takes
    # <16/13; the possible y/leaf drifts stay strictly within the envelope.
    assert (Fraction(7, 8) ** 2 - Fraction(9, 16)) / 4 == Fraction(13, 256)
    assert Fraction(31, 64) - Fraction(31, 832) > Fraction(7, 16)
    assert Fraction(33, 64) + Fraction(31, 832) < Fraction(9, 16)
    assert Fraction(15, 16) - Fraction(1, 52) > Fraction(7, 8)
    assert double_core_open_box_measure() == Fraction(1, 2**53)


def test_double_core_random_ensemble_lower_bound_constants_are_exact():
    assert DOUBLE_CORE_AUTOMORPHISM_ORDER == 2 * 2**2 * 2**4 == 128
    assert DOUBLE_CORE_GAUGE_ORBIT_SIZE == 2**13
    assert (
        Fraction(DOUBLE_CORE_GAUGE_ORBIT_SIZE, DOUBLE_CORE_AUTOMORPHISM_ORDER)
        * Fraction(3, 4) ** 6
        == Fraction(729, 64)
    )
    assert double_core_asymptotic_component_coefficient() == Fraction(729, 64)
    assert double_core_asymptotic_expected_residual_coefficient() == Fraction(729, 2**59)
    assert double_core_expected_isolated_gauge_components(12, 6) == 0
    assert double_core_expected_isolated_gauge_components(13, 5) == 0
    signed_clause_count = 8 * comb(13, 3)
    expected_without_replacement = (
        Fraction(factorial(13), DOUBLE_CORE_AUTOMORPHISM_ORDER)
        * DOUBLE_CORE_GAUGE_ORBIT_SIZE
        / comb(signed_clause_count, 6)
    )
    expected_iid = (
        Fraction(factorial(13), DOUBLE_CORE_AUTOMORPHISM_ORDER)
        * DOUBLE_CORE_GAUGE_ORBIT_SIZE
        * factorial(6)
        / signed_clause_count**6
    )
    assert (
        double_core_expected_isolated_gauge_components(13, 6)
        == expected_without_replacement
    )
    assert double_core_expected_isolated_gauge_components_iid(12, 6) == 0
    assert double_core_expected_isolated_gauge_components_iid(13, 5) == 0
    assert (
        double_core_expected_isolated_gauge_components_iid(13, 6)
        == expected_iid
    )
