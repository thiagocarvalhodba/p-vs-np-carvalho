# Contraexemplo determinístico ao escudo 2-core / Pure Literal Elimination

**Data:** 21 de setembro de 2026  
**Status:** certificado analítico candidato verificado por aritmética exata; mostra que remover grau-1/literais puros não exclui armadilhas PDS positivas em fórmulas arbitrárias.

## Construção M16-core

Centros (a,b,c). Cláusula central:
[
C_0=(alor blor c).
]

Crie 15 cláusulas periféricas (V_k), (k=0,ldots,14), em ordem cíclica de centros
[
a,b,c,a,b,c,ldots,a,b,c
]
(cinco ocorrências de cada centro). Crie folhas compartilhadas
(ell_0,ldots,ell_{14}), índices módulo 15, e defina
[
V_k=(
eg r_klor 
eg ell_{k-1}lor ell_k).
]

Cada centro tem grau 6 (uma ocorrência positiva central e cinco negativas).
Cada (ell_k) tem grau 2, uma ocorrência positiva e uma negativa.
Logo a fórmula é seu próprio 2-core e nenhuma variável é literal puro.
Além disso, quaisquer duas cláusulas compartilham no máximo uma variável.

## Equilíbrio positivo

Use
[
a=b=c=-1,qquad ell_k=0.
]
Escreva (r=-1+u_r). A cláusula central tem energia 1.
Cada periférica tem energia zero por causa de (
eg r_k).

Para um centro (r), cada uma das cinco periféricas contribui (+1/8)
à derivada em (u_r), enquanto a cláusula central contribui (-1/2).
Portanto
[
partial_{u_r}Phi=-rac12+5rac18=rac18>0.
]
A velocidade não projetada aponta para fora de (u_rge0), de modo que o PDS
prende (u_r=0). Nas folhas, as duas contribuições são multiplicadas por
(u_r) ou (u_s), logo se anulam quando todos os centros estão no bordo.
Assim o ponto é um equilíbrio projetado de energia 1.

## Bacia aberta explícita

Considere inicialmente
[
0<u_a,u_b,u_c<arepsilon:=rac1{32},
qquad
|ell_k|<rac1{32}.
]
Use como envelope de bootstrap (|ell_k|<eta:=1/16).
Então todo fator foliar de qualquer polaridade satisfaz
[
rac{1pmell_k}{2}gerac{15}{32}.
]
Cada produto de dois fatores numa periférica é pelo menos (225/1024), e
cinco periféricas dão pelo menos (1125/1024). Logo
[
partial_{u_r}Phi
ge
-rac12+rac12rac{1125}{1024}
=
rac{101}{2048}
=:delta>0.
]
Consequentemente
[
dot u_rle-delta,
qquad
T_{m hit}lerac{arepsilon}{delta}
=rac{64}{101}.
]

Cada folha aparece em duas periféricas de polaridades opostas. Enquanto
(u_r,u_slearepsilon), sua velocidade satisfaz
[
|dotell_k|lerac{u_r+u_s}{4}lerac1{64}.
]
Portanto, até todos os centros atingirem o bordo,
[
|Deltaell_k|
lerac1{64}rac{64}{101}
=rac1{101}.
]
Assim
[
|ell_k(t)|<rac1{32}+rac1{101}<rac1{16},
]
fechando o bootstrap.

Quando um centro chega a (u_r=0), a margem
(partial_{u_r}Phige101/2048) o mantém preso pelo PDS. Depois que os três
centros atingem zero, todas as velocidades foliares também zeram.
A energia permanece (Phi=1), e a cláusula central permanece violada após
rounding.

Logo existe uma bacia aberta de energia positiva mesmo numa fórmula sem
variáveis de grau 1 e sem literais puros.

Sob inicialização uniforme no hipercubo de dimensão 18, o subcaixote acima já
tem probabilidade
[
left(rac{1/32}{2}ight)^3
left(rac{2/32}{2}ight)^{15}
=2^{-93}>0.
]

## Consequência

O simples pré-processamento por 2-core ou Pure Literal Elimination não pode
sustentar um teorema determinístico universal de convergência do PDS para
energia zero.

Este exemplo, porém, é um núcleo cíclico de excesso positivo. Por isso ele não
implica automaticamente densidade residual positiva no ensemble subcrítico:
a questão probabilística de ocorrência macroscópica no random 3-SAT deve ser
tratada separadamente.
