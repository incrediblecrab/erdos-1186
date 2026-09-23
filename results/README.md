# `results/` — certified artifacts

Everything here is an input to `src/final_check.py`, which re-derives each bound from the stored colouring in exact arithmetic. Stored `phi`/`psi` fields are **recomputed, never trusted**: corrupting one bit of a word makes the check exit 1.

## The claims

`claims.json` is the machine-checked statement of what this repo asserts. Each entry is `{problem, k, bound, beats, beats_random, note}` with `problem` either `"n"` ($\delta_k$, over $\{1,\dots,n\}$) or `"zp"` ($\tilde\delta_k$, over $\mathbb{F}_p$). `beats` is a published value and is `null` where nothing was improved — set for $\delta_5$, $\tilde\delta_4$ and $\tilde\delta_5$ only.

## Colourings

| file | contents |
|---|---|
| `zm_k{3..6}.json` | periodic colourings of $\mathbb{Z}_m$, keyed by $m$ |
| `zm_k5_big.json`, `zm_k4_big.json` | tiling-seeded results at large $m$ |
| `wildcard_k5.json`, `wildcard_k5_deep.json` | the $k=5$ chain, incl. $m=484$ and $m=5324$ |
| `wildcard_k6_deep.json` | the $k=6$ chain, $m=3698$ |
| `n_k{3,4,5}.json` | block colourings of $\{1,\dots,n\}$ |
| `two_k{3,4,5}*.json` | two-scale colourings (the $\delta_4$ record) |
| `apfree_k5.json` | moduli admitting a $k$-AP-free 2-colouring |
| `weights/` | cached exact AP-weight tables |

Record schema: `k`, `m`, `phi`, `psi`, `psi_float`, `word` (the colouring, as a 0/1 string of length `m`), `ap_free`, and `seeded_from`/`b`/`f`/`r` where relevant. Files are dicts keyed by `m` as a string. Concurrent searches shard by filename and are merged on read, so several files may hold the same $m$; the minimum wins.

## Logs

`*.log` are raw search and verification transcripts, kept for provenance. `cosetprobe_k6.log` contains the positive control — the probe rediscovering the known $k=5$ structure ($b=44$, $f=4$, $r=3$) before being applied to $b=86$, since a search too weak to find what is already known is not evidence about what is not. `verify_two_k6_3698.log` holds the $\{1,\dots,n\}$ residual measurements. `final_check_full.log` is the complete validation run.

Nothing here is redistributed source material; see `refs/fetch.sh`.
