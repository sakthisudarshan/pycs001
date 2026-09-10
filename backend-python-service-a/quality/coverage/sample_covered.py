# sample_covered.py - Target file for coverage.py analysis
def calculate_tax(income: float, status: str = "single") -> float:
    """Calculate tax based on income brackets and filing status."""
    if income <= 0:
        return 0.0
    
    rate = 0.10
    if status == "single":
        if income > 100000:
            rate = 0.28
        elif income > 50000:
            rate = 0.22
        elif income > 20000:
            rate = 0.15
    elif status == "married":
        if income > 150000:
            rate = 0.24
        elif income > 80000:
            rate = 0.18
        else:
            rate = 0.12
    else:
        rate = 0.20
        
    deduction = 2000.0 if status == "married" else 1000.0
    taxable = max(0.0, income - deduction)
    return round(taxable * rate, 2)


def evaluate_risk(score: int) -> str:
    """Evaluate credit risk score."""
    if score >= 750:
        return "EXCELLENT"
    if score >= 650:
        return "GOOD"
    if score >= 550:
        return "FAIR"
    return "POOR"
