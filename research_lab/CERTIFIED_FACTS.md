# Certified facts / baseline certificates

This file is intentionally conservative. Automated agents may challenge any item, but they must provide an exact contradiction before treating it as false. Automated adjudication does **not** edit this file.

## PDS and multilinear energy

For a 3-CNF instance,

[
Phi_{mathrm{mult}}(x)
=
sum_c
prod_{jin c}
rac{1-sigma_j^{(c)}x_j}{2},
qquad
X=[-1,1]^N.
]

The projected gradient system is

[
dot x
=
Pi_{T_X(x)}(-
ablaPhi(x)).
]

For the convex box, Moreau decomposition gives

[
-dot xin 
ablaPhi(x)+N_X(x)
]

and, almost everywhere along a solution,

[
rac{d}{dt}Phi(x(t))
=
-|dot x(t)|^2.
]

## Harmonicity on every face

The restriction of a multilinear polynomial to any face remains multilinear in the free coordinates. Hence

[
partial_{ii}^2Phi|_F=0
quad	ext{for every free coordinate},
]

so

[
Delta_FPhi=0.
]

Thus the smooth tangential field (-
abla_FPhi) is divergence-free while the trajectory remains in the relative interior of a fixed face.

## Exact positive equilibrium with four clauses

There is a linear 3-uniform four-clause hypertree

[
(0,1,2), (0,3,4), (1,5,6), (2,7,8)
]

with signs

[
(+,+,+), (-,+,+), (-,+,+), (-,+,+)
]

for which (x^*=(-1,ldots,-1)) satisfies

[
Phi(x^*)=1,qquad 
ablaPhi(x^*)=0.
]

This refutes the auxiliary claim that every projected equilibrium on a hypertree has zero energy.

The same point is a relative saddle and its basin is the singleton ({x^*}).

## Boundary second-order reasoning

At a constrained equilibrium, an unrestricted negative Hessian eigenvalue does not by itself prove feasible instability. Second-order conditions must be checked on the **critical cone**

[
C(x^*)=
{din T_X(x^*):
ablaPhi(x^*)^	op d=0}.
]

Example:

[
H=egin{pmatrix}0&1\\1&0end{pmatrix}
]

has a negative eigenvalue, but (d^	op H d=2d_1d_2ge0) on (mathbb R_+^2).

## M6 open-basin certificate

Use variables:

- free central (v);
- boundary variables (b_{11},b_{12},b_{21},b_{22});
- eight leaves (l_{ij,a},l_{ij,b}).

Clauses:

[
C_1=(vlor
eg b_{11}lor
eg b_{12}),
]

[
C_2=(
eg vlor
eg b_{21}lor
eg b_{22}),
]

and four anchors

[
A_{ij}=(b_{ij}lor
eg l_{ij,a}lor
eg l_{ij,b}).
]

Define

[
B_{ij}=rac{1+b_{ij}}2,
qquad
Y_{ijk}=rac{1+l_{ijk}}2.
]

Then exactly

[
Phi=
rac{1-v}{2}B_{11}B_{12}
+
rac{1+v}{2}B_{21}B_{22}
+
sum_{i,j}rac{1-b_{ij}}2Y_{ij,a}Y_{ij,b}.
]

On the face (b_{ij}=1),

[
Phi=1,qquad dot v=0,qquad dot l=0.
]

An explicit open initial set is

[
|v|<rac1{16},qquad
rac{63}{64}<b_{ij}<1,qquad
rac{127}{128}<l_{ijk}<1.
]

Use the bootstrap region

[
|v|<rac18,qquad
b_{ij}>rac{63}{64},qquad
l_{ijk}>rac{63}{64}.
]

Inside it,

[
dot b_{ij}
ge
rac12left(rac{127}{128}ight)^2
-rac14rac98
=
rac{6913}{32768}>0.
]

Hence all four boundary variables hit (1) within

[
T_{mathrm{hit}}lerac{512}{6913}.
]

Also,

[
|dot v|lerac{255}{32768}
]

and therefore

[
|Delta v|
le
rac{255}{64cdot6913}<rac1{16}.
]

For each leaf,

[
|dot l|lerac1{256},
qquad
|Delta l|
le
rac{2}{6913}<rac1{128}.
]

Thus the bootstrap closes. Once (b_{ij}=1), projection keeps them at the wall, and (v) and the leaves freeze. The limiting energy is exactly

[
Phi=1.
]

After Boolean rounding, (C_1) and (C_2) reduce to (v) and (
eg v), so exactly one of them remains violated for any Boolean value assigned to (v).

The displayed sub-basin has normalized uniform probability

[
p_{M6}ge2^{-96}>0.
]

Therefore

[
m_{*,HT}^{mathrm{mult}}le6.
]

This is an upper bound only; minimality still requires excluding all (mle5) bad basins.
