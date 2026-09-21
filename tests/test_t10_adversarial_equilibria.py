from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Fontes"))

from search_t10_positive_equilibrium_hypertrees import (
    attachment_trees,
    catalogue_positive_vertex_equilibria,
    certificate_if_positive_equilibrium,
    counterexample_delta_exact,
    counterexample_leaf_velocity_exact,
    gauge_sign_patterns,
    is_linear_acyclic_attachment_tree,
    phi_grad_exact,
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
