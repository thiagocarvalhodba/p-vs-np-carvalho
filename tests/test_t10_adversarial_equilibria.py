from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Fontes"))

from search_t10_positive_equilibrium_hypertrees import (
    attachment_trees,
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
