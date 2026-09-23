# Erdős #1186 — monochromatic $k$-APs in 2-colourings

> Let $\delta_k$ be such that in any $2$-colouring of $\{1,\ldots,n\}$ there exist at least $(\delta_k+o(1))n^2$ many monochromatic $k$-term arithmetic progressions. Give reasonable bounds (or even an asymptotic formula) for $\delta_k$.
>
> […] It is easier to study this quantity if we replace $\{1,\ldots,n\}$ with a finite field $\mathbb{F}_p$; let this analogue be denoted by $\tilde{\delta}_k$.

**Status: open** — "this is open, and cannot be resolved with a finite computation." Not solved here. Erdős [Er80, p. 93]; quoted from [erdosproblems.com/1186](https://www.erdosproblems.com/1186) (see [Attribution](#attribution)).

**Objective.** Push the *upper* bounds down by explicit construction, certify every value in exact arithmetic, and reproduce the published numbers before claiming to beat them. No lower-bound work was attempted.

**Inputs.** [LuPe12] ([arXiv:1107.2888](https://arxiv.org/abs/1107.2888)), [PRS08], [CCS07], and the erdosproblems.com entry for #1186. Run `refs/fetch.sh` — none are redistributed here. [Wo10] and [BCG10] are paywalled and were **not read**; their numbers appear only as quoted by [LuPe12].

**Findings.** Comparing the optimal periodic colourings at $m=88$ and $m=132$ showed both reduce to one 44-bit base with a free coset of size 4. Generalising gives a **wildcard recursion**: if $\mathbb{Z}_b$ is coloured so every monochromatic $k$-AP lies inside one coset $F$ of size $f$, then

$$m_k(\mathbb{Z}_{bt}) \le \frac{(b-f)+f^2 m_k(\mathbb{Z}_{ft})}{b^2},
\qquad \delta_k \le \frac{1}{2(k-1)(b+f)} .$$

This reproduces **both** published constants exactly — $b=11,f=1\Rightarrow c_4\le1/72$ and $b=37,f=1\Rightarrow c_5\le1/304$ — which is the evidence that it measures the published quantity. Lu and Peng used $b=37$; the largest 5-AP-free modulus is actually **44**, and it carries a free coset of size **4**, not 1. That gives

$$\boxed{\ \delta_5 \le 13421/5153632 = 0.00260418\ }$$

certified at $m=5324$ — a **20.8 % improvement** on $1/304$. The same method on a 6-AP-free $\mathbb{Z}_{86}$ base ($f=2$) gives $\delta_6\le1807/1590140$. Over $\mathbb{F}_p$, block colourings improve $\tilde\delta_4$ by 2.8 % and $\tilde\delta_5$ by 10.6 %.

**$\delta_3$ and $\delta_4$ were not improved.** $\delta_3$ reproduces [PRS08] exactly. $\delta_4$ falls 0.45 % short of $1/72$, and §4 of [`NOTES.md`](NOTES.md) shows this family *provably cannot* reach it: the chain converges to $1/12$ strictly from above, matching [LuPe12, Conjecture 1].

## Certified bounds

All exact rationals, re-derived by `src/final_check.py` from the stored colourings.

| | bound | decimal | where | vs. random | vs. published |
|---|---|---|---|---|---|
| $\delta_3$ | $117/2192$ | 0.05337591 | blocks, $m=548$ | 0.854× | $=117/2192$ [PRS08] — **not improved** |
| $\delta_4$ | $2917/209088$ | 0.01395106 | two-scale, $m=66,B=4$ | 0.670× | $1/72$ [LuPe12] — **0.45 % short** |
| $\delta_5$ | $\mathbf{13421/5153632}$ | 0.00260418 | wildcard chain, $m=5324$ | 0.333× | **beats $1/304$ by 20.83 %** |
| $\delta_6$ | $\mathbf{1807/1590140}$ | 0.00113638 | wildcard chain, $m=3698$ | 0.364× | no published bound found |
| $\tilde\delta_4$ | $\mathbf{159/2888}$ | 0.05505540 | $\mathbb{F}_p$ blocks, $m=152$ | 0.881× | **beats $17/300$ by 2.84 %** |
| $\tilde\delta_5$ | $\mathbf{1283/51984}$ | 0.02468067 | $\mathbb{F}_p$ blocks, $m=114$ | 0.790× | **beats $3629/131424$ by 10.62 %** |
| $\tilde\delta_6$ | $2821/216000$ | 0.01306019 | $\mathbb{F}_p$ blocks, $m=60$ | 0.836× | no published bound found |
| $\tilde\delta_7$ | $1517/230640$ | 0.00657735 | $\mathbb{F}_p$ blocks, $m=62$ | 0.842× | no published bound found |

The recursion's fixed points give $\delta_5\le1/384$ and $\delta_6\le1/880$, but the recursion is **verified at many levels, not proved in general**, so those limits are *conjectural* and the table reports only the finite certified values. For $k=5$ the two differ by $1.6\times10^{-8}$, so nothing rests on the conjectural form.

## How the numbers are trusted

Certification is separated from search, and no self-reported score is accepted.

- Every bound is recomputed from the colouring in exact `Fraction` arithmetic (`src/exact.py`). A stored value is never read as a result.
- Each headline value is confirmed by code sharing nothing with the search: `src/verify_zm.c` (direct double loop over $\mathbb{Z}_m$, no weight table) and `src/verify_two.c` (brute force over $\{1,\dots,n\}$).
- The periodic-to-integer step is measured, not assumed: the boundary term is $1/(2n)$, so (measured $-$ claimed) $\times n$ must stay flat at $\approx0.50$. For the $k=6$ record at $n=20000,60000,120000$ it is **0.504, 0.502, 0.502**.
- Published values are reproduced first — five of them, including Lu–Peng's $B_{74}$ with its exact $d$-breakdown (74 APs at $d=0$, 72 at $d=37$).
- The gate is tested against planted defects, not merely observed to pass. An unsupported claim and a one-bit-corrupted stored word both make it exit 1.

## Reproduce

```bash
bash scripts/reproduce.sh          # full pipeline
FAST=1 bash scripts/reproduce.sh   # skip the long searches
python src/final_check.py          # re-derive every claim; exit 0 = pass
```

| path | contents |
|---|---|
| `src/exact.py` | exact rational evaluator — the certification path |
| `src/periodic.py`, `src/blocks.py`, `src/twoscale.py` | the three colouring families |
| `src/bigm.py` | tiling-seeded search at large $m$ |
| `src/cosetprobe.py` | finds the wildcard coset; exact safety test + positive control |
| `src/chain.py` | builds and certifies one level of the recursion |
| `src/wildcard.py` | the $k=5$ restricted search |
| `src/apfree.py` | AP-free moduli |
| `src/verify_zm.c`, `src/verify_two.c`, `src/verify_zp.c` | independent C cross-checks |
| `src/final_check.py` | re-derives every claim; exit 0 = pass |
| `results/claims.json` | the asserted bounds, machine-checked |
| `results/` | certified colourings and search logs |
| `NOTES.md` | normalisation, reproductions, the recursion, negative results |

Read [`NOTES.md`](NOTES.md) for the derivation, the failure of the $k=4$ family, and the provenance caveats.

## Attribution

The question quoted at the top is from [erdosproblems.com/1186](https://www.erdosproblems.com/1186), maintained by Thomas Bloom, whose companion repository [teorth/erdosproblems](https://github.com/teorth/erdosproblems) is licensed Apache 2.0. The attribution there is to Erdős, *A survey of problems in combinatorial number theory*, Ann. Discrete Math. **6** (1980), 89–115, at p. 93 [Er80].

Short quotations from [LuPe12] in `NOTES.md` are cited in place and used to fix the normalisation and to record which published values were reproduced. No third-party paper or web page is redistributed here: `refs/fetch.sh` retrieves them and `refs/README.md` records which claim each one supports.

The code, data, and prose in this repository are MIT licensed — see [`LICENSE`](LICENSE). That covers this work only; the quoted question and anything `refs/fetch.sh` downloads remain under their own terms.
