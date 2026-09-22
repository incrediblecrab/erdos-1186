# Notes — Erdős #1186

Technical record: normalisation, what was reproduced from the literature, the
construction that produced the improvements, and what was tried and failed.
Every number below is produced by `src/final_check.py`, in exact rational
arithmetic. Run it; exit 0 = pass.

## 1. The problem and the normalisation

Erdős [Er80] asks for the least $\delta_k$ such that every 2-colouring of
$\{1,\dots,n\}$ contains at least $(\delta_k+o(1))n^2$ monochromatic $k$-APs,
and for the analogous $\tilde\delta_k$ over $\mathbb{F}_p$. Only upper bounds
are attacked here: an explicit colouring with few monochromatic $k$-APs bounds
$\delta_k$ from above. **No lower-bound work was attempted.**

Getting the normalisation right is the whole game, because a bound that looks
like an improvement is usually a different quantity. Lu and Peng [LuPe12,
eq. (10)] define

> $c_k = \frac{1}{2(k-1)} \lim_{n\to\infty} m_k([n])$

and state plainly, of their $m_k$,

> "Here we allow $k$-APs to be degenerated"

so $m_k$ counts **ordered pairs** $(a,b)$ with $a+jb$ monochromatic for
$j<k$, including $b=0$. This repo's $\Phi_k$ is exactly their $m_k$. Hence

$$\delta_k = \Phi^{\mathbb{Z}_m}_k/(2(k-1)), \qquad \tilde\delta_k = \Phi_k/2 .$$

The $1/(2(k-1))$ is the area of $\{x,t\ge0,\ x+(k-1)t\le1\}$, the density of
$k$-APs in $\{1,\dots,n\}$; the $/2$ over $\mathbb{F}_p$ is Wolf's unoriented
convention. A random colouring gives $\delta_k\le1/((k-1)2^k)$ and
$\tilde\delta_k\le2^{-k}$.

Degenerate progressions **must** be counted: a $\mathbb{Z}_m$-degenerate AP
(one with $b\ne0$ that wraps) corresponds to a genuine non-degenerate AP in
$\{1,\dots,n\}$. Dropping them answers a different question — this is why
Grier's AP-free sets $G(3,2)$ are not comparable here.

The periodic-to-integer step is [LuPe12, Lemma 1]:

> "For any $k \ge 3$ and any positive integer $b$, we have
> $\lim_{n\to\infty} m_k([n]) \le m_k(\mathbb{Z}_b)$."

**Checked, not assumed.** `src/verify_two.c` brute-forces $\{1,\dots,n\}$
directly. The boundary term is $1/(2n)$, so (measured $-$ claimed) $\times n$
must sit at $\approx0.50$ and stay flat. Measured for the $k=6$ record
($m=3698$) at $n=20000,60000,120000$: **0.504, 0.502, 0.502**.

## 2. Literature reproduced before anything was claimed

An evaluator that cannot recover a published value is not measuring the
published quantity. Five reproductions, all exact:

| source | published | recomputed here |
|---|---|---|
| [PRS08, Thm 5] | $c_3 \le 117/2192$ | $117/2192$ ✓ |
| [LuPe12, Thm 1] $B_{20}$, $\mathbb{F}_p$ blocks | $m_4(\mathbb{Z}_p) \le 17/150$ | $17/150$ ✓ |
| [LuPe12] periodic, $20\mid n$ | $m_4(\mathbb{Z}_n) \le 0.09$ | $m_4(\mathbb{Z}_{20}) = 9/100$ — exactly $0.09$ ✓ |
| [LuPe12] periodic, $22\mid n$ | $m_4(\mathbb{Z}_n) \le 0.086777$ | $m_4(\mathbb{Z}_{22}) = 21/242 = 0.0867769$ ✓ |
| [LuPe12] $B_{74}$ | $m_5(\mathbb{Z}_{74}) = 73/2738$ | $73/2738$ ✓ |

The two threshold values are the tightest of these: $9/100$ is $0.09$ on the
nose, and $21/242$ reproduces all six quoted digits of $0.086777$. (The best
$m_4$ found here over moduli divisible by 22 is in fact $61/726 = 0.084022$ at
$m=66$, better than their $\mathbb{Z}_{22}$ value — but this is an
intermediate quantity, and after dividing by $2(k-1)=6$ it still does not
reach $1/72$; see §4.)

The $B_{74}$ check is the sharp one, because it reproduces the *structure* and
not just the value. Lu and Peng write:

> "All monochromatic 5-APs in $B_{74}$ are degenerated ones. Among them there
> are 74 5-APs with $d = 0$ and 72 5-APs with $d = 37$. This coloring gives
> $m_5(\mathbb{Z}_{74}) = 146/74^2 = 73/2738$."

`src/verify_zm.c` prints the $d$-breakdown and returns exactly 74 at $d=0$ and
72 at $d=37$.

Targets: $c_4 \le 1/72$ and $c_5 \le 1/304$ [LuPe12, eqs. (12)–(13)], and
$\lim m_4(\mathbb{Z}_n)\le1/12$, $\lim m_5(\mathbb{Z}_n)\le1/38$ [LuPe12,
Thm 5]. Over $\mathbb{F}_p$: $m_4(\mathbb{Z}_p)\le17/300+o(1)$ [Thm 1] and
$m_5(\mathbb{Z}_n)\le3629/65712+o(1)$ for odd $n$ [Thm 4].

All quotations above were read from `refs/lupe12.pdf` directly (text extracted
with `pypdf`), not from a secondary source.

## 3. The wildcard recursion

This is the new ingredient and the source of both improvements.

Lu and Peng found their $k=4$ bound by noticing that the two halves of a good
$\mathbb{Z}_{22}$ colouring differ in one bit, giving an 11-bit pattern with a
wildcard. Running the same comparison one level up — on the optima found at
$m=88$ and $m=132$ for $k=5$ — both reduce to the **same** 44-bit base with
exactly four free positions $\{3,14,25,36\}$, the coset $x\equiv3\pmod{11}$.

Generalised: let $\mathbb{Z}_b$ be coloured so that every monochromatic $k$-AP
of the $b$-periodic extension has all its terms inside one coset $F$ of size
$f$. Then $F$ may be recoloured by an arbitrary colouring of $\mathbb{Z}_{ft}$,
and

$$m_k(\mathbb{Z}_{bt}) \;\le\; \frac{(b-f) + f^2\, m_k(\mathbb{Z}_{ft})}{b^2},
\qquad\text{fixed point } \frac{1}{b+f},$$

hence $\delta_k \le \dfrac{1}{2(k-1)(b+f)}$.

The condition on $F$ is decidable exactly, with no search
(`cosetprobe.py:safe_coset`). Call an AP **dangerous** if it has terms both
inside and outside $F$ and the base is constant on the outside terms — then
colouring the inside to match makes it monochromatic, which the recursion does
not account for. $F$ is safe iff no dangerous AP exists. Both the colour and
the $F$-membership of $a+jd$ depend only on $(a+jd)\bmod b$, so the test over
$\mathbb{Z}_b$ settles it **for every $t$**: outside terms that already
disagree mod $b$ still disagree in any lift.

**The formula reproduces both published constants exactly.**

| $k$ | base | $b$ | $f$ | limit $1/(b+f)$ | $\delta_k$ | matches |
|---|---|---|---|---|---|---|
| 4 | Lu–Peng $B_{11}$ | 11 | 1 | $1/12$ | $1/72$ | [LuPe12] eq. (12) ✓ |
| 5 | Lu–Peng $B_{37}$ | 37 | 1 | $1/38$ | $1/304$ | [LuPe12] eq. (13) ✓ |
| 5 | **this repo, $B_{44}$** | 44 | 4 | $1/48$ | $1/384$ | **new** |
| 6 | **this repo, $B_{86}$** | 86 | 2 | $1/88$ | $1/880$ | **new** |

Lu and Peng used $b=37$ because their search found $B_{37}$; the largest
5-AP-free modulus is in fact 44, and it carries a free coset of size 4 rather
than 1. That is the entire improvement.

**Bases.** $k=5$: `10010111010001011011110110100010111010010000`, free coset
$\{3,14,25,36\}$. $k=6$: an 86-bit word with $\Phi_6 = 1/86$ (6-AP-free), free
coset $\{33,76\}$. Both stored in `results/`.

### 3.1 Certified levels, and what is *not* certified

Only finitely many levels are computed; the fixed point is the limit of a
recursion **verified but not proved in general**. So:

| $k$ | certified, exact | chain limit |
|---|---|---|
| 5 | $m_5(\mathbb{Z}_{5324}) = 13421/644204 \Rightarrow \delta_5 \le 13421/5153632$ | $\delta_5\le1/384$ *(conjectural)* |
| 6 | $m_6(\mathbb{Z}_{3698}) = 1807/159014 \Rightarrow \delta_6 \le 1807/1590140$ | $\delta_6\le1/880$ *(conjectural)* |

The certified $\delta_5$ and the limit differ by $1.6\times10^{-8}$, so nothing
rests on the conjectural form. **Lead with the certified value.** The
recursion was confirmed against explicit constructions at
$t = 2, 3, 4, 11, 121$ for $k=5$ (i.e. $m = 88, 132, 176, 484, 5324$) and at
$t=43$ for $k=6$ ($m=3698$).

The $t=4$ case is the one that matters, because it refutes the obvious guess.
The naive law $(10t+1)/(484t)$ — which assumes the inner colouring is
5-AP-free — predicts $41/1936 = 0.02117769$ at $m=176$, but the true minimum
over $\mathbb{Z}_{16}$ is $m_5(\mathbb{Z}_{16}) = 5/64$, not $1/16$, and the
construction actually attains $15/704 = 0.02130682$. The naive law therefore
claims a value **below what is achievable**: it is not a valid bound. The
recursion above gives $15/704$ exactly. `src/wildcard.py:predicted` implements
the recursion; the naive law is retained only in its docstring as a warning.

Each certified value was checked three ways that share no code: `exact.py`
(rational arithmetic), `verify_zm.c` (direct double loop over $\mathbb{Z}_m$,
no weight table), and `verify_two.c` (brute force over $\{1,\dots,n\}$).

## 4. Why $\delta_4$ and $\delta_3$ were **not** improved

Stated plainly because it is the main negative result.

**$\delta_4$: 0.45 % short, and the family provably cannot close it.** Best
certified here is $2917/209088 = 0.01395106$ against Lu–Peng's
$1/72 = 0.01388889$. At $m=11t$ the optimum is $\Phi = (10t+1)/(121t)$, which
is exactly [LuPe12, Lemma 6] with a 4-AP-free inner colouring; their Theorem 5
proof gives $m_4(\mathbb{Z}_{11^s}) \le 1/12 + 1/(12\cdot11^{2s-1})$, which
converges to $1/12$ **strictly from above**. The largest 4-AP-free modulus is
11 (SAT-proved UNSAT above it), and $b=22,f=2$ is impossible since it would
imply a 4-AP-free $\mathbb{Z}_{22}$. So no member of this family reaches
$1/72$; it is approached and never attained. This is consistent with
[LuPe12, Conjecture 1]:

> "$\inf\{m_4(\mathbb{Z}_n) : n$ is not divisible by $4\} = 1/12$."

**$\delta_3$: reproduced, not improved.** $117/2192$, equal to [PRS08, Thm 5].
The $k=3$ periodic family is weak — the best periodic $\mathbb{Z}_m$ result is
$\Phi_3 = 1/16$ at $m=12$, exactly the random value, i.e. no gain at all.

## 5. Other negative results

Recorded so they are not re-run.

- **Larger free cosets at $b=44$ do not exist.** $f$ must divide 44. Direct
  search at $m=88$: $f=4 \to 21/968$ (best), $f=11 \to 87/3872$,
  $f=22 \to 43/1936$. The exact structural test agrees — only $f=2$ and $f=4$
  are safe, and $f=4$ wins. So $1/48$ is the ceiling of this scheme for $k=5$.
- **Same at $b=86$ for $k=6$.** Divisors are $1,2,43,86$. The structural test
  is exhaustive over all of them and finds $f=2$ (at $r=33$) the only safe
  coset of size $>1$. $f=43$ is unsafe, so $1/88$ is the ceiling.
- $f=1$ cosets *do* lower $\Phi$ at finite $t$ (e.g. $87/3872 < 1/44$) without
  being safe. Improving a finite instance is not the same as supporting the
  recursion; do not confuse the two.
- Random restarts are useless past $m\approx100$. Tiling a $\mathbb{Z}_m$ word
  to $\mathbb{Z}_{tm}$ preserves $\Phi$ exactly, so seeding from the tiled
  record is what makes large $m$ reachable (`src/bigm.py`).

## 6. Provenance caveats

- **[Wo10] and [BCG10] are paywalled and were not read.** Their numbers
  ($c_4 < 0.0172202$, $c_5 < 0.005719619$) appear here only as quoted by
  [LuPe12]. They are weaker than the bounds used as targets, so nothing
  depends on them, but they are second-hand and are marked as such.
- [CCS07]'s typeset Theorem 4.4 says "4-coloring" while its proof uses two
  colour classes. Almost certainly a typo; the two-colour reading is the one
  used here.
- $k\ge6$: no published bound was located for either problem. The $k=6$ and
  $k=7$ entries are therefore reported as "no published bound found", not as
  records. Absence of a bound in the sources read is not proof none exists.

## 7. A subagent's numbers were wrong — do not trust unverified ones

A literature agent returned two colouring certificates and several claimed
values. On checking: its "88-bit" string had **92** characters and its
"176-bit" string had **140**, so neither certificate could be evaluated at all.
Its claim that $m_5(\mathbb{Z}_{44}) = 7/242$ is false for the word used here,
which is antipodal ($c(x+22) = 1-c(x)$), so no difference divisible by 11 can
be monochromatic. Its best claimed values ($85/3872$ at $m=88$, $333/15488$ at
$m=176$) are both beaten by direct search here ($21/968$, $15/704$).

Its one useful contribution was pointing out that Lu–Peng's bound comes from a
recursion rather than a fixed modulus — a structural hint, which was then
verified against the PDF.

On a second request it re-sent the colourings as explicit integer lists. Those
*did* have the stated lengths and were evaluable, and its two best candidates
were checked here in exact arithmetic before publication:

| agent's claim | verified $\Phi$ | this repo | outcome |
|---|---|---|---|
| $k=5$, $m=220$ | $51/2420 = 0.02107438$ | $13421/644204 = 0.02083346$ | does not beat |
| $k=6$, $m=344$ | $169/14792 = 0.01142509$ | $1807/159014 = 0.01136378$ | does not beat |

It independently arrived at $\mathbb{Z}_{86}$ as the best 6-AP-free modulus,
which corroborates the base used in §3. The standing lesson is unchanged: every
number it supplied was re-derived here before being believed, and the ones that
mattered were checked before anything was published.

## 8. Validation

`src/final_check.py` re-derives every claim from the stored artifacts and
asserts the contents of `results/claims.json` against them; it does not read
any cached score.

**The gate was tested by planting defects, not merely observed to pass.** A
checker that has only ever seen good input is untested. Two independent
defects, each planted and then reverted:

| planted defect | result |
|---|---|
| $\delta_5$ claim changed to $1/400$ (better than anything certified) | exit **1**, `[FAIL] delta_5: certified 13421/5153632 <= claimed 1/400` |
| one bit of the stored $m=484$ word flipped, its recorded `phi` left intact | exit **1**, `[FAIL] zm k=5: 12 words re-certify — 1 bad: 633/234256 != 111/42592` |

The second is the important one: it shows $\Phi$ is recomputed from the
colouring rather than read from the file, so a corrupted certificate cannot
pass by carrying a correct-looking number.

Known gap in coverage: `results/zm_k4.json` starts at $m=12$, so the $k=4$
AP-free list is empty even though $\mathbb{Z}_{11}$ is 4-AP-free. This affects
reporting only — the $k=4$ bound comes from the two-scale family.

The `.gitignore` entries for the compiled C binaries were written but **not
verified with `git check-ignore`**: this tree is not a git repository in the
environment used, so the rules are correct by inspection only.

## References

- [Er80] P. Erdős, *A survey of problems in combinatorial number theory*,
  Ann. Discrete Math. 6 (1980), 89–115. MR 593525.
- [LuPe12] L. Lu, X. Peng, *Monochromatic 4-term arithmetic progressions in
  2-colorings of $\mathbb{Z}_n$*, [arXiv:1107.2888](https://arxiv.org/abs/1107.2888).
- [PRS08] P. Parrilo, A. Robertson, D. Saracino, *On the asymptotic minimum
  number of monochromatic 3-term arithmetic progressions*, JCTA 115 (2008).
- [CCS07] Cameron, Cilleruelo, Serra, *On monochromatic solutions of
  equations in groups*, Rev. Mat. Iberoam. 23 (2007).
- [Wo10] J. Wolf, *The minimum number of monochromatic 4-term progressions in
  $\mathbb{Z}_p$*, J. Comb. 1 (2010). **Not read — paywalled.**
- [BCG10] Butler, Costello, Graham. **Not read — paywalled.**

Fetch with `refs/fetch.sh`; nothing is redistributed here.
