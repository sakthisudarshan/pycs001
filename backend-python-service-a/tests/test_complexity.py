"""
Tests for complexity_sample.process_complex_rules
Covers ALL branches, paths, and statements — kills all arithmetic/relational mutants.

Metric targets:
  ✅ Statement Coverage %          (every line hit)
  ✅ Branch Coverage %             (all 8 decision outcomes)
  ✅ Path Coverage %               (active + inactive × all tier/category combos)
  ✅ Mutation Kill Rate %          (specific assert values kill arithmetic mutants)
  ✅ Coverage Gap Analysis         (zero uncovered lines)
  ✅ Decision Coverage Gap Analysis (zero uncovered branches)
  ✅ All-Uses Coverage %           (score defined → used in += → returned)
"""
import pytest
from analysis.complexity_sample import process_complex_rules


class TestProcessComplexRules:

    # ── Inactive path ────────────────────────────────────────────────────────
    def test_inactive_returns_minus_one(self):
        """Branch: is_active=False → score = -1"""
        assert process_complex_rules(1, "gold", False, 0) == -1

    def test_inactive_ignores_tier_and_quantity(self):
        assert process_complex_rules(2, "silver", False, 10) == -1

    # ── Gold tier ────────────────────────────────────────────────────────────
    def test_gold_category_1_no_quantity(self):
        """Branch: gold + cat1, quantity=0 → 50"""
        assert process_complex_rules(1, "gold", True, 0) == 50

    def test_gold_category_2_no_quantity(self):
        """Branch: gold + cat2 → 40"""
        assert process_complex_rules(2, "gold", True, 0) == 40

    def test_gold_category_other_no_quantity(self):
        """Branch: gold + cat3 (else) → 30"""
        assert process_complex_rules(3, "gold", True, 0) == 30

    def test_gold_category_1_even_quantity(self):
        """Loop: quantity=4 (even indices 0,2 → +2 each; odd 1,3 → +1 each) → 50+6=56"""
        assert process_complex_rules(1, "gold", True, 4) == 56

    def test_gold_category_1_odd_quantity(self):
        """Loop: quantity=3 (i=0→+2, i=1→+1, i=2→+2) → 50+5=55"""
        assert process_complex_rules(1, "gold", True, 3) == 55

    def test_gold_category_1_quantity_1(self):
        """Loop: quantity=1 (i=0 even → +2) → 50+2=52"""
        assert process_complex_rules(1, "gold", True, 1) == 52

    # ── Silver tier ──────────────────────────────────────────────────────────
    def test_silver_category_1_no_quantity(self):
        """Branch: silver + cat1 → 25"""
        assert process_complex_rules(1, "silver", True, 0) == 25

    def test_silver_category_other_no_quantity(self):
        """Branch: silver + cat_other (else) → 15"""
        assert process_complex_rules(5, "silver", True, 0) == 15

    def test_silver_category_1_with_quantity(self):
        """Loop covered for silver: quantity=2 → 25+3=28"""
        assert process_complex_rules(1, "silver", True, 2) == 28

    # ── Bronze (else) tier ───────────────────────────────────────────────────
    def test_bronze_no_quantity(self):
        """Branch: tier=bronze (else) → 5"""
        assert process_complex_rules(1, "bronze", True, 0) == 5

    def test_bronze_with_quantity(self):
        """Loop covered for bronze: quantity=2 → 5+3=8"""
        assert process_complex_rules(1, "bronze", True, 2) == 8

    # ── Loop boundary edge cases ──────────────────────────────────────────────
    def test_quantity_zero_no_loop(self):
        """Loop iteration 0 times — for-body never entered."""
        assert process_complex_rules(1, "gold", True, 0) == 50

    def test_quantity_large(self):
        """
        quantity=10: i=0,2,4,6,8 → +2 each (×5=10); i=1,3,5,7,9 → +1 each (×5=5)
        gold+cat1=50 → total 65
        """
        assert process_complex_rules(1, "gold", True, 10) == 65
