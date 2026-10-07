"""Check family 160's digit product and the stronger interface required by our wildcard recursion."""

import argparse
import json
from pathlib import Path

from cosetprobe import divisors, safe_coset


SOURCE = "https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/07-transfers.tex"


def monochromatic(word, k, cyclic=False):
    n = len(word)
    if k < 2 or not word:
        raise ValueError("A nonempty word and k >= 2 are required")
    count = tested = 0
    for a in range(n):
        differences = range(1, n) if cyclic else range(1, (n-1-a)//(k-1) + 1)
        for d in differences:
            tested += 1
            count += len({word[(a+j*d) % n] for j in range(k)}) == 1
    return {"progressions_tested": tested, "monochromatic": count}


def digit_product(base, digits):
    if not base or digits < 1:
        raise ValueError("A nonempty base and positive digit count are required")
    n = len(base)
    return [tuple(base[(value // n**place) % n] for place in range(digits))
            for value in range(n**digits)]


def check(plant=None):
    base, k = [0, 0, 1, 1], 3
    if plant == "coloring":
        base[2] = 0
    cyclic = monochromatic(base, k, cyclic=True)
    cosets = []
    for size in divisors(len(base)):
        if size == len(base):
            continue
        step = len(base)//size
        for residue in range(step):
            free = {residue + step*j for j in range(size)}
            safe, dangerous = safe_coset(base, k, free)
            if plant == "interface":
                safe = True
            cosets.append({"free_coset": sorted(free), "safe": safe, "dangerous_progressions": dangerous})

    products = []
    for digits in (1, 2, 3):
        word = digit_product(base, digits)
        products.append({"digits": digits, "length": len(word), "colors": len(set(word)),
                         **monochromatic(word, k)})

    qr = [int(pow(x, 5, 11) == 1) for x in range(11)]
    qr_cyclic = monochromatic(qr, 4, cyclic=True)
    qr_safe, qr_dangerous = safe_coset(qr, 4, {0})
    checks = [
        {"name": "small base is cyclic AP-free", "passed": cyclic["monochromatic"] == 0},
        {"name": "digit products are interval AP-free", "passed": all(item["monochromatic"] == 0 for item in products)},
        {"name": "cyclic AP-freeness does not imply a safe proper wildcard coset",
         "passed": cyclic["monochromatic"] == 0 and not any(item["safe"] for item in cosets)},
        {"name": "known quadratic-residue wildcard base still passes",
         "passed": qr_cyclic["monochromatic"] == 0 and qr_safe},
    ]
    return {
        "source": SOURCE,
        "scope": "Finite checks of the digit-product interface and a counterexample to an automatic wildcard transfer. No new asymptotic bound or improvement of delta_k.",
        "plant": plant,
        "base": base,
        "k": k,
        "cyclic": cyclic,
        "proper_cosets": cosets,
        "digit_products": products,
        "positive_control": {"base": qr, "k": 4, "free_coset": [0], "cyclic": qr_cyclic,
                             "safe": qr_safe, "dangerous_progressions": qr_dangerous},
        "checks": checks,
        "passed": all(item["passed"] for item in checks),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--plant", choices=("coloring", "interface"))
    args = parser.parse_args()
    report = check(args.plant)
    for item in report["checks"]:
        print(f"{'PASS' if item['passed'] else 'FAIL'} {item['name']}")
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
