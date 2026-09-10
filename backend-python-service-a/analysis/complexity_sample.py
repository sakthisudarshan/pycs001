"""
Analysis fixture — mirrors ComplexitySample.cs
Provides rich branch/path/statement coverage and mutation testing targets.

Techniques unlocked:
  - Statement Coverage     (every line exercised)
  - Branch Coverage        (8 decision outcomes: tier × category × active)
  - Path Coverage          (nested conditions + loop = multiple distinct paths)
  - Mutation Score         (arithmetic / relational mutants are killable)
  - All Uses Coverage      (score variable: defined, used in conditions + returned)
"""


def process_complex_rules(
    category: int, tier: str, is_active: bool, quantity: int
) -> int:
    """
    Compute a scoring rule identical in logic to ProcessComplexRules in C#.
    All branch pairs are covered by the test suite.
    """
    score: int = 0

    if is_active:
        if tier == "gold":
            if category == 1:
                score += 50
            elif category == 2:
                score += 40
            else:
                score += 30
        elif tier == "silver":
            if category == 1:
                score += 25
            else:
                score += 15
        else:
            score += 5

        for i in range(quantity):
            if i % 2 == 0:
                score += 2
            else:
                score += 1
    else:
        score = -1

    return score
