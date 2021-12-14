"""
The example sequence shows exponential growth so lets try and
work out a better solution under the assumption AoC will ask for the nth iteration later on.

Firstly, inserting in the middle of a pair means that insertions will never interact with the pair to the left or right of the current one. i.e. we can apply the same growing function to each pair individually and then stich them all back together if required.

Secondly, we don't actually care about the order.

The result being that we can just keep a count of the current pairings and apply the map to create a new set of counts.
"""
import argparse
import re
from collections import Counter
from typing import Dict
from typing import Iterable
from typing import Tuple


def parse_input(data: Iterable[str]) -> Tuple[str, Dict]:
    r"""Returns the polymer template and pair insertion rules.

    Example:

        >>> data = '''NNCB
        ... 
        ... CH -> B
        ... HH -> N
        ... CB -> H'''.split('\n')
        >>> template, rules = parse_input(iter(data))
        >>> template
        'NNCB'
        >>> rules
        {'CH': 'B', 'HH': 'N', 'CB': 'H'}
    """
    pattern = re.compile("([A-Z][A-Z]) -> ([A-Z])")
    template = next(data).rstrip()
    rules = {}
    next(data)
    for line in data:
        match = pattern.fullmatch(line.rstrip())
        if not match:
            raise ValueError(f"failed match {line}")
        rules[match[1]] = match[2]
    return template, rules


def pair_insertion(template: str, rules: Dict[str, str], iterations: int) -> Dict[str, int]:
    r"""Returns a map of (pair, count) after iterations.
    
    Example:

        >>> template, rules = parse_input(iter('''NNCB
        ... 
        ... CH -> B
        ... HH -> N
        ... CB -> H
        ... NH -> C
        ... HB -> C
        ... HC -> B
        ... HN -> C
        ... NN -> C
        ... BH -> H
        ... NC -> B
        ... NB -> B
        ... BN -> B
        ... BB -> N
        ... BC -> B
        ... CC -> N
        ... CN -> C'''.split('\n')))
        >>> exp_pair = sorted([('NC', 1), ('CN', 1), ('NB', 1), ('BC', 1), ('CH', 1), ('HB', 1)])
        >>> exp_chr = sorted(list(Counter("NCNBCHB").items()))
        >>> pair, chr = pair_insertion(template, rules, 1)
        >>> exp_pair == sorted(list(pair.items()))
        True
        >>> exp_chr == sorted(list(chr.items()))
        True
    """
    pair_cnts = Counter([a + b for a, b in zip(template, template[1:])])
    chr_cnts = Counter(template)
    
    for i in range(iterations):
        new_pair_cnts = Counter()
        for pair, count in pair_cnts.items():
            new_chr = rules[pair]
            chr_cnts[new_chr] += count
            new_pair_cnts[pair[0] + new_chr] += count
            new_pair_cnts[new_chr + pair[1]] += count
        pair_cnts = new_pair_cnts
            
    return dict(pair_cnts), dict(chr_cnts)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--iters", default=10, type=int)
    args = parser.parse_args()

    with open(args.path, 'r') as f:
        template, rules = parse_input(f)

    pair_cnts, chr_cnts = pair_insertion(template, rules, args.iters)
    
    most = max(chr_cnts.items(), key=lambda c: c[1])
    least = min(chr_cnts.items(), key=lambda c: c[1])

    print(most[1] - least[1])