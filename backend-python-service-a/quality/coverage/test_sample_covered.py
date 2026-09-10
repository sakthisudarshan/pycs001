import pytest
from sample_covered import calculate_tax, evaluate_risk

def test_tax_zero_or_negative():
    assert calculate_tax(0) == 0.0
    assert calculate_tax(-500) == 0.0

def test_tax_single_brackets():
    assert calculate_tax(15000, "single") > 0.0
    assert calculate_tax(60000, "single") > 0.0
    assert calculate_tax(120000, "single") > 0.0

def test_tax_married_brackets():
    assert calculate_tax(50000, "married") > 0.0
    assert calculate_tax(90000, "married") > 0.0
    assert calculate_tax(200000, "married") > 0.0

def test_evaluate_risk():
    assert evaluate_risk(800) == "EXCELLENT"
    assert evaluate_risk(700) == "GOOD"
    assert evaluate_risk(600) == "FAIR"
    assert evaluate_risk(400) == "POOR"
