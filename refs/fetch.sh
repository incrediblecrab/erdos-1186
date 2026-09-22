#!/bin/sh
# Re-download the primary sources cited in NOTES.md.
#
# Nothing fetched here is redistributed in this repository: all of it is
# copyright its authors/publishers.  Run this to populate refs/ locally.  The
# repository .gitignore excludes everything in refs/ except this script and
# refs/README.md.
#
# Two of the load-bearing sources are paywalled and cannot be fetched:
#   [Wo10]  Wolf, J. Combin. 1 (2010) 53-68.  No arXiv version exists; the only
#           copy is behind International Press.  DOI 10.4310/JOC.2010.v1.n1.a4
#   [BCG10] Butler-Costello-Graham, Exp. Math. 19 (2010) 399-411.  No preprint
#           was found on any author page.  DOI 10.1080/10586458.2010.10390631
# Their numbers are quoted in NOTES.md with that provenance stated explicitly.
set -e
cd "$(dirname "$0")"

# [PRS08] Parrilo, Robertson, Saracino, "On the asymptotic minimum number of
# monochromatic 3-term arithmetic progressions", JCTA 115 (2008) 185-192.
# Theorem 5 is the delta_3 <= 117/2192 upper bound; section 4 displays the
# 12-block word that src/final_check.py re-certifies exactly.
curl -sL "https://arxiv.org/pdf/math/0609532" -o prs08.pdf

# [LuPe12] Lu, Peng, "Monochromatic 4-term arithmetic progressions in
# 2-colorings of Z_n", JCTA 119 (2012) 1048-1065.  Theorem 1 is the
# m_4(Z_p) <= 17/150 bound this project beats; B_20 is the bit string that
# src/final_check.py re-derives independently as the m = 20 block optimum.
curl -sL "https://arxiv.org/pdf/1107.2888" -o lupe12.pdf

# [GKW24] Greenwood, Kariv, Williams, "From discrete to continuous:
# monochromatic 3-term arithmetic progressions", Math. Comp. (2024).
# Proves PRS08's word is optimal among antisymmetric <= 12-block colourings.
curl -sL "https://arxiv.org/pdf/2301.00336" -o gkw24.pdf

# [Ve21] Versteegen, "Linear configurations containing 4-term arithmetic
# progressions are uncommon".  Qualitative delta~_4 < 1/16 for Z_p; no constant.
curl -sL "https://arxiv.org/pdf/2106.06846" -o versteegen21.pdf

# [RS26] Rue, Spiegel, "The Rado multiplicity problem in vector spaces over
# finite fields", FFA 111 (2026) 102782.  Flag algebras, but over F_p^n, not Z_p.
curl -sL "https://arxiv.org/pdf/2304.00400" -o rue_spiegel.pdf

# [YM26] Yang, Mao, resolution of the Butler-Costello-Graham conjecture.
# Existence of a beats-random colouring for every rational pattern; no constant.
curl -sL "https://arxiv.org/pdf/2604.02115" -o yang_mao26.pdf

# [CCS07] Cameron, Cilleruelo, Serra, "On monochromatic solutions of equations
# in groups", Rev. Mat. Iberoam. 23 (2007) 385-395.  Author-hosted preprint.
# Note: the typeset Theorem 4.4 reads "4-coloring"; the proof uses two colour
# classes throughout.  See NOTES.md.
curl -sL "https://webspace.maths.qmul.ac.uk/p.j.cameron/preprints/mono.pdf" \
  -o ccs07.pdf || echo "ccs07: author copy moved; see DOI 10.4171/RMI/499"

# The problem statement itself.
curl -sL "https://www.erdosproblems.com/1186" -o erdos1186.html

echo "fetched into $(pwd)"
