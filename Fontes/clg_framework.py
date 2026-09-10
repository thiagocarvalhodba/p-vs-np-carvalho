"""
Computational Landscape Geometry (CLG) Framework
Author: Thiago Carvalho (2026)
Project: CLG-01 (Negative Controls & Geometric Invariants for P vs NP)

This module implements the mathematical foundations of Computational Landscape
Geometry (CLG), enabling continuous relaxation, analytical and autograd Hessian
curvature analysis, and geometric invariant extraction across Class P (2-SAT)
and Class NP-Complete (3-SAT) instances.
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
class GeometricInvariants:
    problem_type: str        # '2-SAT' (Class P) or '3-SAT' (Class NP)
    complexity_class: str    # 'P' or 'NP-Complete'
    num_vars: int            # N
    num_clauses: int         # M
    clause_ratio: float      # M / N
    
    # Spectral Hessian Invariants
    mean_lambda_min: float
    mean_lambda_max: float
    mean_spectral_range: float   # Delta lambda
    mean_spectral_trace: float   # Tr(H)
    mean_morse_index: float      # Fraction of negative eigenvalues (saddles)
    mean_condition_number: float # kappa(H)
    
    # Differential Curvature Dispersion
    curvature_dispersion: float  # Omega_curv = ||H(x) - H_bar||_F
    is_state_independent: bool   # Exactly True for 2-SAT, False for 3-SAT
    
    # Rigidity & Ruggedness Metrics
    rigidity_index: float        # R(I)
    langevin_escape_rate: float  # Empirical escape frequency under thermal noise
    computation_time_sec: float


class CNFInstance:
    """Represents a general k-CNF formula and its continuous relaxation on [-1, 1]^N."""
    
    def __init__(self, num_vars: int, k_sat: int, clauses: List[Tuple[List[int], List[int]]]):
        """
        clauses is a list of tuples: (var_indices, literal_signs)
        where var_indices has length k_sat (0-indexed)
        and literal_signs has length k_sat (+1 for positive literal x_i, -1 for negated literal not x_i)
        """
        self.num_vars = num_vars
        self.k_sat = k_sat
        self.clauses = clauses
        self.num_clauses = len(clauses)
        self.clause_ratio = self.num_clauses / self.num_vars
        
        # Pre-convert to tensors for fast vectorized evaluation
        self.clause_indices = torch.tensor([c[0] for c in clauses], dtype=torch.long)
        self.clause_signs = torch.tensor([c[1] for c in clauses], dtype=torch.float32)

    def potential(self, x: torch.Tensor) -> torch.Tensor:
        """
        Computes continuous potential energy Phi(x) in [0, M].
        Phi(x) = sum_c prod_{j=1}^k (1 - sigma_{c,j} * x_{c,j}) / 2
        """
        # Gather variable values for each clause: [M, k]
        selected_vars = x[self.clause_indices] # [M, k]
        # Clause literal dissatisfaction factor: (1 - sigma * x) / 2 in [0, 1]
        factors = (1.0 - self.clause_signs * selected_vars) * 0.5
        # Clause energy is product of factors:
        clause_energies = torch.prod(factors, dim=-1) # [M]
        return torch.sum(clause_energies)

    def gradient(self, x: torch.Tensor) -> torch.Tensor:
        """Computes exact gradient grad Phi(x) via automatic differentiation."""
        x_req = x.detach().clone().requires_grad_(True)
        energy = self.potential(x_req)
        energy.backward()
        return x_req.grad.detach()

    def compute_hessian(self, x: torch.Tensor) -> torch.Tensor:
        """Computes exact Hessian matrix H(x) = nabla^2 Phi(x) of size [N, N]."""
        return hessian(self.potential, x)

    def discrete_energy(self, spin_state: np.ndarray) -> int:
        """Evaluates number of unsatisfied clauses for discrete spin configuration {-1, +1}^N."""
        unsatisfied = 0
        for indices, signs in self.clauses:
            # Satisfied if any literal evaluates to True (+1)
            sat = any(signs[j] * spin_state[indices[j]] > 0 for j in range(self.k_sat))
            if not sat:
                unsatisfied += 1
        return unsatisfied


class LandscapeAnalyzer:
    """Extracts geometric invariants from the continuous energy landscape."""

    @staticmethod
    def extract_invariants(instance: CNFInstance, num_samples: int = 30) -> GeometricInvariants:
        start_time = time.time()
        n = instance.num_vars
        
        # Sample random states uniformly from the continuous hypercube [-1, 1]^N
        samples = [torch.empty(n).uniform_(-1.0, 1.0) for _ in range(num_samples)]
        
        hessians: List[torch.Tensor] = []
        eigenvalues_list: List[np.ndarray] = []
        condition_numbers: List[float] = []
        morse_indices: List[float] = []
        traces: List[float] = []
        
        for s in samples:
            h = instance.compute_hessian(s)
            hessians.append(h)
            
            # Spectral decomposition of symmetric Hessian
            h_np = h.numpy()
            eigvals = np.linalg.eigvalsh(h_np) # Sorted real eigenvalues
            eigenvalues_list.append(eigvals)
            
            traces.append(float(np.trace(h_np)))
            # Morse index: fraction of negative eigenvalues
            neg_count = np.sum(eigvals < -1e-6)
            morse_indices.append(float(neg_count / n))
            
            # Condition number: |lambda_max| / (|lambda_min| + epsilon)
            abs_eigs = np.abs(eigvals)
            cond = float(abs_eigs.max() / (abs_eigs.min() + 1e-6))
            condition_numbers.append(cond)

        # 1. Curvature Dispersion: Omega_curv = sqrt(E[||H(x) - H_bar||_F^2])
        mean_h = torch.stack(hessians, dim=0).mean(dim=0)
        frobenius_diffs = [torch.norm(h - mean_h, p='fro').item() for h in hessians]
        curvature_dispersion = float(np.sqrt(np.mean(np.square(frobenius_diffs))))
        is_state_independent = bool(curvature_dispersion < 1e-4)

        # 2. Spectral statistics
        eig_matrix = np.array(eigenvalues_list) # [num_samples, N]
        mean_lambda_min = float(np.mean(eig_matrix[:, 0]))
        mean_lambda_max = float(np.mean(eig_matrix[:, -1]))
        spectral_range = float(np.mean(eig_matrix[:, -1] - eig_matrix[:, 0]))
        mean_morse = float(np.mean(morse_indices))
        mean_trace = float(np.mean(traces))
        mean_cond = float(np.mean(condition_numbers))

        # 3. Rigidity / Ruggedness Index: R(I) = (Omega_curv / (Delta_lambda + eps)) * Morse_Index
        rigidity_index = float((curvature_dispersion / (spectral_range + 1e-6)) * mean_morse)

        # 4. Langevin Escape Rate Simulation:
        # Measure empirical frequency of escaping local basins under thermal agitation T=0.15
        escape_count = 0
        for _ in range(10):
            x_traj = torch.empty(n).uniform_(-0.5, 0.5)
            init_energy = instance.potential(x_traj).item()
            dt = 0.05
            temp = 0.15
            for _ in range(50):
                grad = instance.gradient(x_traj)
                noise = torch.randn(n) * math.sqrt(2.0 * temp * dt)
                x_traj = torch.clamp(x_traj - dt * grad + noise, -1.0, 1.0)
            final_energy = instance.potential(x_traj).item()
            if abs(final_energy - init_energy) > 0.5:
                escape_count += 1
        langevin_escape_rate = escape_count / 10.0

        problem_type = "2-SAT" if instance.k_sat == 2 else "3-SAT"
        complexity_class = "P" if instance.k_sat == 2 else "NP-Complete"

        return GeometricInvariants(
            problem_type=problem_type,
            complexity_class=complexity_class,
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
            rigidity_index=rigidity_index,
            langevin_escape_rate=langevin_escape_rate,
            computation_time_sec=time.time() - start_time
        )


def generate_random_2sat(n: int, alpha: float, seed: Optional[int] = None) -> CNFInstance:
    """Generates a random 2-SAT instance (Class P) with M = round(alpha * N) clauses."""
    if seed is not None:
        random.seed(seed)
        torch.manual_seed(seed)
        
    num_clauses = max(1, int(round(alpha * n)))
    clauses = []
    for _ in range(num_clauses):
        # Pick 2 distinct variables uniformly at random
        vars_chosen = random.sample(range(n), 2)
        signs = [random.choice([-1.0, 1.0]) for _ in range(2)]
        clauses.append((vars_chosen, signs))
    return CNFInstance(n, 2, clauses)


def generate_random_3sat(n: int, alpha: float, seed: Optional[int] = None) -> CNFInstance:
    """Generates a random 3-SAT instance (Class NP-Complete) with M = round(alpha * N) clauses."""
    if seed is not None:
        random.seed(seed)
        torch.manual_seed(seed)
        
    num_clauses = max(1, int(round(alpha * n)))
    clauses = []
    for _ in range(num_clauses):
        # Pick 3 distinct variables uniformly at random
        vars_chosen = random.sample(range(n), 3)
        signs = [random.choice([-1.0, 1.0]) for _ in range(3)]
        clauses.append((vars_chosen, signs))
    return CNFInstance(n, 3, clauses)
