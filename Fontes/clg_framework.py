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


def generate_random_3xorsat(n: int, alpha: float, seed: Optional[int] = None) -> CNFInstance:
    """
    Group 4: Random 3-XOR-SAT / Parity Equations (Language: Class P, Degree: 3)
    Each equation is x_i1 (+) x_i2 (+) x_i3 = b (mod 2).
    In Boolean CNF, each parity equation expands into exactly 4 clauses of degree 3.
    Theoretical Complexity: Solvable in O(N^3) by Gaussian Elimination over GF(2) (strictly in Class P).
    Continuous Landscape: Forms a dense 3-spin Sherrington-Kirkpatrick spin glass with 
    exponential proliferation of metastable local minima (Kac-Rice), demonstrating that
    continuous gradient descent cannot emulate global algebraic Gaussian elimination!
    """
    if seed is not None:
        random.seed(seed)
        torch.manual_seed(seed)
    num_equations = max(1, int(round(alpha * n)))
    clauses = []
    for _ in range(num_equations):
        vars_chosen = random.sample(range(n), 3)
        b = random.choice([0, 1])
        # A parity equation x1 (+) x2 (+) x3 = b expands to 4 CNF clauses
        # Truth table: parity is violated when sum(vars) = 1 - b (mod 2)
        # Signs in CNFInstance: +1 means literal is positive (x_i), -1 means negative (not x_i)
        # An assignment s in {-1, 1}^3 satisfies a clause if exists j with s_j == sign_j.
        for s1 in [-1.0, 1.0]:
            for s2 in [-1.0, 1.0]:
                for s3 in [-1.0, 1.0]:
                    # Map sign {-1, 1} to boolean {0, 1}: +1 -> True (1), -1 -> False (0)
                    b1 = 1 if s1 > 0 else 0
                    b2 = 1 if s2 > 0 else 0
                    b3 = 1 if s3 > 0 else 0
                    # If this boolean combination violates the equation, add the rejecting clause
                    if (b1 ^ b2 ^ b3) != b:
                        # Rejecting clause has opposite signs
                        clauses.append((vars_chosen, [-s1, -s2, -s3]))
    return CNFInstance(n, 3, clauses, problem_family="3-XOR-SAT", language_class="P")


# ==============================================================================
# RIGOROUS CLG-R RELAXATION AND CONTINUOUS FLOW ENGINE
# ==============================================================================

class Relaxation:
    """
    Implements the three canonical continuous relaxations of 3-SAT on [-1, 1]^N:
      1. Quadratic Hinge: Phi_quad(x) = sum_c max(0, g_c(x))^2
      2. Multilinear Harmonics: Phi_mult(x) = sum_c prod_{j in c} (1 - sigma_{c,j} * x_j)/2
      3. Softplus Convex: Phi_soft(x) = (1/beta) * sum_c ln(1 + exp(beta * g_c(x)))
    
    Includes closed-form gradients, Hessians, and pure projected Euler gradient flow.
    """
    def __init__(self, num_vars: int, clauses: List[Tuple[List[int], List[float]]]):
        self.num_vars = num_vars
        self.num_clauses = len(clauses)
        self.clauses = clauses
        
        # Build dense polarity matrix S of shape (M, N)
        self.S = np.zeros((self.num_clauses, self.num_vars), dtype=np.float64)
        for c, (vs, ss) in enumerate(clauses):
            for v, s in zip(vs, ss):
                self.S[c, v] = float(s)
                
        # Incidence matrix V = -0.5 * S
        self.V = -0.5 * self.S
        
        # Fast vectorized indexing for 3-SAT instances
        self.is_3sat = (self.num_clauses > 0) and all(len(c[0]) == 3 for c in clauses)
        if self.is_3sat:
            self.V0 = np.array([c[0][0] for c in clauses], dtype=np.int64)
            self.V1 = np.array([c[0][1] for c in clauses], dtype=np.int64)
            self.V2 = np.array([c[0][2] for c in clauses], dtype=np.int64)
            self.S0 = np.array([c[1][0] for c in clauses], dtype=np.float64)
            self.S1 = np.array([c[1][1] for c in clauses], dtype=np.float64)
            self.S2 = np.array([c[1][2] for c in clauses], dtype=np.float64)

    def g(self, x: np.ndarray) -> np.ndarray:
        """Affine clause violation function: g_c(x) = -0.5 * (1 + S_c . x)."""
        return -0.5 * (1.0 + self.S @ x)

    # 1. Quadratic Hinge
    def phi_quad(self, x: np.ndarray) -> float:
        gc = self.g(x)
        return float(np.sum(np.maximum(0.0, gc) ** 2))

    def grad_quad(self, x: np.ndarray) -> np.ndarray:
        if self.is_3sat:
            gc = -0.5 * (1.0 + x[self.V0] * self.S0 + x[self.V1] * self.S1 + x[self.V2] * self.S2)
            act = gc > 0
            out = np.zeros_like(x, dtype=np.float64)
            if np.any(act):
                np.add.at(out, self.V0[act], -gc[act] * self.S0[act])
                np.add.at(out, self.V1[act], -gc[act] * self.S1[act])
                np.add.at(out, self.V2[act], -gc[act] * self.S2[act])
            return out
        gc = self.g(x)
        act = gc > 0
        if not np.any(act):
            return np.zeros_like(x)
        return (2.0 * gc[act]) @ (-0.5 * self.S[act])

    # 2. Multilinear Harmonics
    def phi_mult(self, x: np.ndarray) -> float:
        if self.is_3sat:
            u0 = (1.0 - self.S0 * x[self.V0]) * 0.5
            u1 = (1.0 - self.S1 * x[self.V1]) * 0.5
            u2 = (1.0 - self.S2 * x[self.V2]) * 0.5
            return float(np.sum(u0 * u1 * u2))
        factors = np.where(self.S != 0, (1.0 - self.S * x) / 2.0, 1.0)
        return float(np.sum(np.prod(factors, axis=1)))

    def grad_mult(self, x: np.ndarray) -> np.ndarray:
        if self.is_3sat:
            u0 = (1.0 - self.S0 * x[self.V0]) * 0.5
            u1 = (1.0 - self.S1 * x[self.V1]) * 0.5
            u2 = (1.0 - self.S2 * x[self.V2]) * 0.5
            out = np.zeros_like(x, dtype=np.float64)
            np.add.at(out, self.V0, (-self.S0 * 0.5) * (u1 * u2))
            np.add.at(out, self.V1, (-self.S1 * 0.5) * (u0 * u2))
            np.add.at(out, self.V2, (-self.S2 * 0.5) * (u0 * u1))
            return out
        out = np.zeros_like(x, dtype=np.float64)
        for c in range(self.num_clauses):
            vs = np.nonzero(self.S[c])[0]
            for i in vs:
                others = [j for j in vs if j != i]
                term = (-self.S[c, i] / 2.0) * np.prod([(1.0 - self.S[c, j] * x[j]) / 2.0 for j in others])
                out[i] += term
        return out

    # 3. Softplus Convex
    def phi_soft(self, x: np.ndarray, beta: float = 5.0) -> float:
        gc = self.g(x)
        return float(np.sum(np.logaddexp(0.0, beta * gc)) / beta)

    def grad_soft(self, x: np.ndarray, beta: float = 5.0) -> np.ndarray:
        gc = self.g(x)
        s = 1.0 / (1.0 + np.exp(-np.clip(beta * gc, -500.0, 500.0)))
        return s @ self.V

    def hess_soft(self, x: np.ndarray, beta: float = 5.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        gc = self.g(x)
        s = 1.0 / (1.0 + np.exp(-np.clip(beta * gc, -500.0, 500.0)))
        W = beta * s * (1.0 - s)
        H = self.V.T @ (W[:, None] * self.V)
        return H, self.V, W

    # Discrete Energy Evaluation
    def discrete_energy(self, spin_state: np.ndarray) -> int:
        """Vectorized discrete clause violation count for spin configuration s in {-1, +1}^N."""
        s = np.asarray(spin_state, dtype=np.float64)
        if self.is_3sat:
            violated = (s[self.V0] * self.S0 < 0) & (s[self.V1] * self.S1 < 0) & (s[self.V2] * self.S2 < 0)
            return int(np.sum(violated))
        violated = np.all(self.S * s < 0, axis=1)
        return int(np.sum(violated))

    # Pure Projected Gradient Descent (No box penalty, no Adam)
    def projected_gradient_descent(
        self,
        x0: np.ndarray,
        representation: str = "mult",
        eta: float = 0.01,
        T: float = 40.0,
        beta: float = 5.0,
        tol: float = 1e-10
    ) -> Tuple[np.ndarray, float, int]:
        """
        Pure projected Euler flow on [-1, 1]^N:
          x_{t+1} = clip(x_t - eta * grad_Phi(x_t), -1.0, 1.0)
        """
        x = np.clip(x0.copy().astype(np.float64), -1.0, 1.0)
        steps = int(round(T / eta))
        
        for step in range(steps):
            if representation == "quad":
                grad = self.grad_quad(x)
            elif representation == "mult":
                grad = self.grad_mult(x)
            elif representation == "soft":
                grad = self.grad_soft(x, beta=beta)
            else:
                raise ValueError(f"Unknown representation: {representation}")
                
            x_new = np.clip(x - eta * grad, -1.0, 1.0)
            if np.linalg.norm(grad) < tol or np.max(np.abs(x_new - x)) < 1e-8:
                x = x_new
                break
            x = x_new
            
        final_energy = self.phi_mult(x) if representation == "mult" else (
            self.phi_quad(x) if representation == "quad" else self.phi_soft(x, beta=beta)
        )
        return x, final_energy, step + 1


class ErcseyRavaszToroczkaiDynamics:
    """
    Deterministic Continuous-Time SAT Solver with Auxiliary Variables.
    Reference: Ercsey-Ravasz & Toroczkai, Nature Physics 7, 966-970 (2011).
    
    Equations:
      s_i in [-1, 1],  a_m >= 1
      K_m(s) = prod_{j in m} (1 - S_{mj} * s_j) / 2
      ds_i/dt = - sum_m 2 * a_m * K_m * (dK_m / ds_i)
      da_m/dt = a_m * K_m
    """
    def __init__(self, num_vars: int, clauses: List[Tuple[List[int], List[float]]]):
        self.num_vars = num_vars
        self.num_clauses = len(clauses)
        self.clauses = clauses
        self.S = np.zeros((self.num_clauses, self.num_vars), dtype=np.float64)
        for c, (vs, ss) in enumerate(clauses):
            for v, s in zip(vs, ss):
                self.S[c, v] = float(s)
                
        self.is_3sat = (self.num_clauses > 0) and all(len(c[0]) == 3 for c in clauses)
        if self.is_3sat:
            self.V0 = np.array([c[0][0] for c in clauses], dtype=np.int64)
            self.V1 = np.array([c[0][1] for c in clauses], dtype=np.int64)
            self.V2 = np.array([c[0][2] for c in clauses], dtype=np.int64)
            self.S0 = np.array([c[1][0] for c in clauses], dtype=np.float64)
            self.S1 = np.array([c[1][1] for c in clauses], dtype=np.float64)
            self.S2 = np.array([c[1][2] for c in clauses], dtype=np.float64)

    def solve(
        self,
        s0: Optional[np.ndarray] = None,
        dt: float = 0.02,
        max_time: float = 30.0,
        tol: float = 1e-4
    ) -> Tuple[np.ndarray, bool, float]:
        n, m = self.num_vars, self.num_clauses
        if s0 is None:
            s = np.random.uniform(-0.9, 0.9, n)
        else:
            s = np.clip(s0.copy(), -1.0, 1.0)
            
        a = np.ones(m, dtype=np.float64)
        t = 0.0
        
        while t < max_time:
            if self.is_3sat:
                u0 = (1.0 - self.S0 * s[self.V0]) * 0.5
                u1 = (1.0 - self.S1 * s[self.V1]) * 0.5
                u2 = (1.0 - self.S2 * s[self.V2]) * 0.5
                K = u0 * u1 * u2
                if np.all(K < tol):
                    return s, True, t
                w = -2.0 * a * K
                ds = np.zeros(n, dtype=np.float64)
                np.add.at(ds, self.V0, w * ((-self.S0 * 0.5) * (u1 * u2)))
                np.add.at(ds, self.V1, w * ((-self.S1 * 0.5) * (u0 * u2)))
                np.add.at(ds, self.V2, w * ((-self.S2 * 0.5) * (u0 * u1)))
            else:
                factors = np.where(self.S != 0, (1.0 - self.S * s) / 2.0, 1.0)
                K = np.prod(factors, axis=1)
                if np.all(K < tol):
                    return s, True, t
                ds = np.zeros(n, dtype=np.float64)
                for c in range(m):
                    if K[c] > 1e-12:
                        vs = np.nonzero(self.S[c])[0]
                        for i in vs:
                            others = [j for j in vs if j != i]
                            dK_dsi = (-self.S[c, i] / 2.0) * np.prod([(1.0 - self.S[c, j] * s[j]) / 2.0 for j in others])
                            ds[i] += -2.0 * a[c] * K[c] * dK_dsi
                        
            s = np.clip(s + dt * ds, -1.0, 1.0)
            a = np.clip(a + dt * (a * K), 1.0, 1e7)
            t += dt
            
        return s, False, t


# ==============================================================================
# STATISTICAL ROBUSTNESS AND CONFIDENCE INTERVAL UTILITIES
# ==============================================================================

def wilson_score_interval(successes: int, total: int, confidence: float = 0.95) -> Tuple[float, float]:
    """Computes exact Wilson score confidence interval for binomial proportion."""
    if total == 0:
        return 0.0, 1.0
    z = 1.95996  # 95% confidence
    p_hat = successes / total
    denom = 1.0 + (z ** 2) / total
    center = (p_hat + (z ** 2) / (2.0 * total)) / denom
    margin = (z / denom) * math.sqrt((p_hat * (1.0 - p_hat) / total) + (z ** 2) / (4.0 * (total ** 2)))
    lower = max(0.0, center - margin)
    upper = min(1.0, center + margin)
    return lower, upper


def bootstrap_instance_ci(
    values: List[float],
    num_resamples: int = 2000,
    confidence: float = 0.95,
    seed: int = 42
) -> Tuple[float, float, float]:
    """Computes non-parametric bootstrap confidence interval across instances."""
    arr = np.asarray(values, dtype=np.float64)
    if len(arr) == 0:
        return 0.0, 0.0, 0.0
    rng = np.random.default_rng(seed)
    n = len(arr)
    mean_val = float(np.mean(arr))
    boot_means = np.empty(num_resamples)
    for b in range(num_resamples):
        sample = rng.choice(arr, size=n, replace=True)
        boot_means[b] = np.mean(sample)
    alpha = (1.0 - confidence) / 2.0
    lower = float(np.percentile(boot_means, 100.0 * alpha))
    upper = float(np.percentile(boot_means, 100.0 * (1.0 - alpha)))
    return mean_val, lower, upper


