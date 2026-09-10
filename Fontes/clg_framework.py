"""
Computational Landscape Geometry (CLG) Framework - Version 2.0 (CLG-02)
Author: Thiago Carvalho (2026)
Project: CLG-02 (Degree-Controlled Complexity Benchmark)

Formal Enhancements:
- Rigorous complexity classification: problem_family and language_class (e.g., P vs NP-Complete)
- Geometric Descriptor Vector G(I) replacing premature invariance terminology
- Exact calculation of Third-Order Variation Tensor T_ijk = nabla^3 Phi and norm Gamma(I)
- Inclusion of 4 controlled problem families:
    1. 2-SAT (Language: P, Degree: 2)
    2. Horn-3-SAT (Language: P, Degree: 3)
    3. Equisatisfiable 3-SAT from 2-SAT (Language: P, Degree: 3)
    4. Critical Random 3-SAT (Language: NP-Complete, Degree: 3)
    5. Max-Cut Continuous Quadratic Relaxation (Language: NP-Hard, Degree: 2)
"""

import time
import math
import random
from dataclasses import dataclass, asdict
from typing import List, Tuple, Dict, Any, Optional

import numpy as np
import torch
from torch.autograd.functional import hessian


@dataclass
class GeometricDescriptor:
    problem_family: str        # e.g., '2-SAT', 'Horn-3-SAT', 'Equi-3-SAT', 'Random-3-SAT', 'Max-Cut'
    language_class: str        # 'P', 'NP-Complete', 'NP-Hard'
    algebraic_degree: int      # 2 (quadratic), 3 (cubic)
    num_vars: int              # N
    num_clauses: int           # M (or edges)
    clause_ratio: float        # M / N
    
    # Spectral Hessian Invariants (Second-Order Geometry)
    mean_lambda_min: float
    mean_lambda_max: float
    mean_spectral_range: float   # Delta lambda = lambda_max - lambda_min
    mean_spectral_trace: float   # Tr(H)
    mean_morse_index: float      # Fraction of negative eigenvalues (saddle density)
    mean_condition_number: float # kappa(H)
    
    # Differential Curvature Dispersion
    curvature_dispersion: float  # Omega_curv = sqrt(E[||H(x) - H_bar||_F^2])
    is_state_independent: bool   # Exactly True if Omega_curv == 0
    
    # Third-Order Tensor of Variation: T_ijk = nabla^3 Phi
    third_order_norm: float      # Gamma(I) = ||T||_F
    
    # Rigidity & Ruggedness Descriptors
    rigidity_index: float        # R(I) = (Omega_curv / (Delta_lambda + eps)) * Morse_Index
    langevin_escape_rate: float  # Empirical escape frequency under thermal noise
    computation_time_sec: float


class CNFInstance:
    """Represents a general k-CNF formula and its continuous relaxation on [-1, 1]^N."""
    
    def __init__(
        self,
        num_vars: int,
        k_sat: int,
        clauses: List[Tuple[List[int], List[int]]],
        problem_family: str,
        language_class: str
    ):
        self.num_vars = num_vars
        self.k_sat = k_sat
        self.clauses = clauses
        self.num_clauses = len(clauses)
        self.clause_ratio = self.num_clauses / self.num_vars
        self.problem_family = problem_family
        self.language_class = language_class
        self.algebraic_degree = k_sat
        
        # Pre-convert to tensors for fast vectorized evaluation
        self.clause_indices = torch.tensor([c[0] for c in clauses], dtype=torch.long)
        self.clause_signs = torch.tensor([c[1] for c in clauses], dtype=torch.float32)

    def potential(self, x: torch.Tensor) -> torch.Tensor:
        """
        Computes continuous potential energy Phi(x) in [0, M].
        Phi(x) = sum_c prod_{j=1}^k (1 - sigma_{c,j} * x_{c,j}) / 2
        """
        selected_vars = x[self.clause_indices] # [M, k]
        factors = (1.0 - self.clause_signs * selected_vars) * 0.5
        clause_energies = torch.prod(factors, dim=-1) # [M]
        return torch.sum(clause_energies)

    def gradient(self, x: torch.Tensor) -> torch.Tensor:
        x_req = x.detach().clone().requires_grad_(True)
        energy = self.potential(x_req)
        energy.backward()
        return x_req.grad.detach()

    def compute_hessian(self, x: torch.Tensor) -> torch.Tensor:
        return hessian(self.potential, x)

    def compute_third_order_tensor_norm(self) -> float:
        """
        Computes exact Frobenius norm Gamma(I) = ||nabla^3 Phi||_F of the third derivative tensor.
        For k=2: nabla^3 Phi is identically 0.
        For k=3: for each clause c = (i, j, k), the third derivative is -1/8 * sigma_i * sigma_j * sigma_k.
        """
        if self.k_sat < 3:
            return 0.0
        
        # Aggregate symmetric 3rd-derivative entries across all permutations of variables in each clause
        n = self.num_vars
        # Create sparse dictionary of triplets (i, j, k) with i <= j <= k
        triplet_weights: Dict[Tuple[int, int, int], float] = {}
        
        for (v_idx, s_sign) in self.clauses:
            if len(v_idx) == 3:
                # Sort indices to form canonical unordered triplet
                order = np.argsort(v_idx)
                i, j, k = v_idx[order[0]], v_idx[order[1]], v_idx[order[2]]
                # Derivative contribution: -1/8 * prod(signs)
                contrib = -0.125 * (s_sign[0] * s_sign[1] * s_sign[2])
                key = (i, j, k)
                triplet_weights[key] = triplet_weights.get(key, 0.0) + contrib

        # Total Frobenius norm squared accounts for permutations:
        frobenius_sq = 0.0
        for (i, j, k), val in triplet_weights.items():
            if i != j and j != k and i != k:
                # 3 distinct indices: 3! = 6 equal tensor entries
                frobenius_sq += 6.0 * (val ** 2)
            elif (i == j and j != k) or (j == k and i != j) or (i == k and j != i):
                # 2 distinct indices: 3! / 2! = 3 entries
                frobenius_sq += 3.0 * (val ** 2)
            else:
                # 3 identical indices: 1 entry
                frobenius_sq += 1.0 * (val ** 2)
                
        return float(math.sqrt(frobenius_sq))

    def discrete_energy(self, spin_state: np.ndarray) -> int:
        """Evaluates number of unsatisfied clauses for discrete spin configuration {-1, +1}^N."""
        unsatisfied = 0
        for indices, signs in self.clauses:
            sat = any(signs[j] * spin_state[indices[j]] > 0 for j in range(self.k_sat))
            if not sat:
                unsatisfied += 1
        return unsatisfied



class LandscapeAnalyzer:
    """Extracts geometric descriptors from the continuous energy landscape."""

    @staticmethod
    def extract_descriptor(instance: CNFInstance, num_samples: int = 25) -> GeometricDescriptor:
        start_time = time.time()
        n = instance.num_vars
        
        samples = [torch.empty(n).uniform_(-1.0, 1.0) for _ in range(num_samples)]
        
        hessians: List[torch.Tensor] = []
        eigenvalues_list: List[np.ndarray] = []
        condition_numbers: List[float] = []
        morse_indices: List[float] = []
        traces: List[float] = []
        
        for s in samples:
            h = instance.compute_hessian(s)
            hessians.append(h)
            
            h_np = h.numpy()
            eigvals = np.linalg.eigvalsh(h_np)
            eigenvalues_list.append(eigvals)
            
            traces.append(float(np.trace(h_np)))
            neg_count = np.sum(eigvals < -1e-6)
            morse_indices.append(float(neg_count / n))
            
            abs_eigs = np.abs(eigvals)
            cond = float(abs_eigs.max() / (abs_eigs.min() + 1e-6))
            condition_numbers.append(cond)

        # 1. Curvature Dispersion: Omega_curv = sqrt(E[||H(x) - H_bar||_F^2])
        mean_h = torch.stack(hessians, dim=0).mean(dim=0)
        frobenius_diffs = [torch.norm(h - mean_h, p='fro').item() for h in hessians]
        curvature_dispersion = float(np.sqrt(np.mean(np.square(frobenius_diffs))))
        is_state_independent = bool(curvature_dispersion < 1e-4)

        # 2. Spectral statistics
        eig_matrix = np.array(eigenvalues_list)
        mean_lambda_min = float(np.mean(eig_matrix[:, 0]))
        mean_lambda_max = float(np.mean(eig_matrix[:, -1]))
        spectral_range = float(np.mean(eig_matrix[:, -1] - eig_matrix[:, 0]))
        mean_morse = float(np.mean(morse_indices))
        mean_trace = float(np.mean(traces))
        mean_cond = float(np.mean(condition_numbers))

        # 3. Third-Order Tensor Norm: Gamma(I) = ||nabla^3 Phi||_F
        third_order_norm = instance.compute_third_order_tensor_norm()

        # 4. Rigidity / Ruggedness Descriptor: R(I)
        rigidity_index = float((curvature_dispersion / (spectral_range + 1e-6)) * mean_morse)

        # 5. Langevin Escape Rate Simulation
        escape_count = 0
        for _ in range(8):
            x_traj = torch.empty(n).uniform_(-0.5, 0.5)
            init_energy = instance.potential(x_traj).item()
            dt = 0.05
            temp = 0.15
            for _ in range(40):
                grad = instance.gradient(x_traj)
                noise = torch.randn(n) * math.sqrt(2.0 * temp * dt)
                x_traj = torch.clamp(x_traj - dt * grad + noise, -1.0, 1.0)
            final_energy = instance.potential(x_traj).item()
            if abs(final_energy - init_energy) > 0.5:
                escape_count += 1
        langevin_escape_rate = escape_count / 8.0

        return GeometricDescriptor(
            problem_family=instance.problem_family,
            language_class=instance.language_class,
            algebraic_degree=instance.algebraic_degree,
            num_vars=n,
            num_clauses=instance.num_clauses,
            clause_ratio=instance.clause_ratio,
            mean_lambda_min=mean_lambda_min,
            mean_lambda_max=mean_lambda_max,
            mean_spectral_range=spectral_range,
            mean_spectral_trace=mean_trace,
            mean_morse_index=mean_morse,
            mean_condition_number=mean_cond,
            curvature_dispersion=curvature_dispersion,
            is_state_independent=is_state_independent,
            third_order_norm=third_order_norm,
            rigidity_index=rigidity_index,
            langevin_escape_rate=langevin_escape_rate,
            computation_time_sec=time.time() - start_time
        )


# ==============================================================================
# PROBLEM FAMILY GENERATORS FOR CLG-02
# ==============================================================================

def generate_random_2sat(n: int, alpha: float, seed: Optional[int] = None) -> CNFInstance:
    """Group 1: 2-SAT (Language: Class P, Degree: 2)"""
    if seed is not None:
        random.seed(seed)
        torch.manual_seed(seed)
    num_clauses = max(1, int(round(alpha * n)))
    clauses = []
    for _ in range(num_clauses):
        vars_chosen = random.sample(range(n), 2)
        signs = [random.choice([-1.0, 1.0]) for _ in range(2)]
        clauses.append((vars_chosen, signs))
    return CNFInstance(n, 2, clauses, problem_family="2-SAT", language_class="P")


def generate_horn_3sat(n: int, alpha: float, seed: Optional[int] = None) -> CNFInstance:
    """
    Group 2A: Horn-3-SAT (Language: Class P, Degree: 3)
    Each clause has 3 literals, but AT MOST 1 literal is positive.
    Horn formulas are solvable in deterministic linear time O(M) via Unit Propagation,
    yet possess algebraic degree 3 in the continuous relaxation!
    """
    if seed is not None:
        random.seed(seed)
        torch.manual_seed(seed)
    num_clauses = max(1, int(round(alpha * n)))
    clauses = []
    for _ in range(num_clauses):
        vars_chosen = random.sample(range(n), 3)
        # Horn constraint: at most 1 positive literal
        # 50% chance of all negative, 50% chance of exactly 1 positive
        if random.random() < 0.5:
            signs = [-1.0, -1.0, -1.0]
        else:
            pos_idx = random.randint(0, 2)
            signs = [-1.0, -1.0, -1.0]
            signs[pos_idx] = 1.0
        clauses.append((vars_chosen, signs))
    return CNFInstance(n, 3, clauses, problem_family="Horn-3-SAT", language_class="P")


def generate_equisatisfiable_3sat_from_2sat(n_base: int, alpha: float, seed: Optional[int] = None) -> CNFInstance:
    """
    Group 2B: Equisatisfiable 3-SAT derived from 2-SAT (Language: Class P, Degree: 3)
    Converts 2-SAT clause (u v) into (u v z) and (u v not z), introducing auxiliary variable z.
    The resulting formula is purely degree 3, but computationally solvable in Class P!
    """
    if seed is not None:
        random.seed(seed)
        torch.manual_seed(seed)
    num_base_clauses = max(1, int(round(alpha * n_base)))
    # Add auxiliary variables
    total_vars = n_base + num_base_clauses
    clauses = []
    for c_idx in range(num_base_clauses):
        u, v = random.sample(range(n_base), 2)
        su, sv = random.choice([-1.0, 1.0]), random.choice([-1.0, 1.0])
        z = n_base + c_idx
        # (u v z) and (u v not z)
        clauses.append(([u, v, z], [su, sv, 1.0]))
        clauses.append(([u, v, z], [su, sv, -1.0]))
    return CNFInstance(total_vars, 3, clauses, problem_family="Equi-3-SAT", language_class="P")


def generate_random_3sat(n: int, alpha: float, seed: Optional[int] = None) -> CNFInstance:
    """Group 3: Random 3-SAT at critical threshold alpha_c = 4.267 (Language: NP-Complete, Degree: 3)"""
    if seed is not None:
        random.seed(seed)
        torch.manual_seed(seed)
    num_clauses = max(1, int(round(alpha * n)))
    clauses = []
    for _ in range(num_clauses):
        vars_chosen = random.sample(range(n), 3)
        signs = [random.choice([-1.0, 1.0]) for _ in range(3)]
        clauses.append((vars_chosen, signs))
    return CNFInstance(n, 3, clauses, problem_family="Random-3-SAT", language_class="NP-Complete")
