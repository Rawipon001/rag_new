"""
Script to calculate CORRECT ground truth tax saving values
Based on Thai tax law and marginal tax rates
"""

import sys
sys.path.append('/Users/atikun/Desktop/Rag/rag_new/backend')

from app.services.tax_calculator import TaxCalculatorService
from app.models import TaxCalculationRequest

def calculate_correct_tax_savings():
    """Calculate correct tax savings for all test cases"""

    calculator = TaxCalculatorService()

    print("=" * 80)
    print("CALCULATING CORRECT TAX SAVINGS FOR TEST CASES")
    print("=" * 80)

    # Test Case 1: 600K income
    print("\n" + "=" * 80)
    print("TEST CASE 1: รายได้ 600K")
    print("=" * 80)

    request1 = TaxCalculationRequest(
        gross_income=600000,
        personal_deduction=60000,
        life_insurance=50000,
        health_insurance=15000,
        social_security=9000,
        provident_fund=50000,
        risk_tolerance="medium"
    )

    tax_result1 = calculator.calculate_tax(request1)
    print(f"\nTaxable Income: {tax_result1.taxable_income:,} บาท")
    print(f"Current Tax: {tax_result1.tax_amount:,} บาท")

    # Calculate for 3 investment tiers
    tiers = [60000, 100000, 150000]
    print(f"\nInvestment Tiers: {tiers}")
    print("\nCalculating tax savings:\n")

    for tier in tiers:
        taxable_without = tax_result1.taxable_income + tier
        marginal_rate = calculator.get_marginal_tax_rate(taxable_without)
        tax_saving = int(tier * (marginal_rate / 100))

        print(f"Investment: {tier:>7,} บาท")
        print(f"  → Taxable without investment: {taxable_without:,} บาท")
        print(f"  → Marginal rate at that level: {marginal_rate}%")
        print(f"  → Tax saving: {tax_saving:,} บาท")
        print()

    # Test Case 2: 1.5M income
    print("=" * 80)
    print("TEST CASE 2: รายได้ 1.5M")
    print("=" * 80)

    request2 = TaxCalculationRequest(
        gross_income=1500000,
        personal_deduction=60000,
        spouse_deduction=60000,
        child_deduction=60000,
        parent_support=60000,
        life_insurance=100000,
        health_insurance=25000,
        social_security=9000,
        provident_fund=75000,
        risk_tolerance="high"
    )

    tax_result2 = calculator.calculate_tax(request2)
    print(f"\nTaxable Income: {tax_result2.taxable_income:,} บาท")
    print(f"Current Tax: {tax_result2.tax_amount:,} บาท")

    tiers2 = [300000, 500000, 800000]
    print(f"\nInvestment Tiers: {tiers2}")
    print("\nCalculating tax savings:\n")

    for tier in tiers2:
        taxable_without = tax_result2.taxable_income + tier
        marginal_rate = calculator.get_marginal_tax_rate(taxable_without)
        tax_saving = int(tier * (marginal_rate / 100))

        print(f"Investment: {tier:>7,} บาท")
        print(f"  → Taxable without investment: {taxable_without:,} บาท")
        print(f"  → Marginal rate at that level: {marginal_rate}%")
        print(f"  → Tax saving: {tax_saving:,} บาท")
        print()

    # Test Case 3: 360K income
    print("=" * 80)
    print("TEST CASE 3: รายได้ 360K")
    print("=" * 80)

    request3 = TaxCalculationRequest(
        gross_income=360000,
        personal_deduction=60000,
        child_deduction=30000,
        life_insurance=20000,
        health_insurance=10000,
        social_security=9000,
        risk_tolerance="low"
    )

    tax_result3 = calculator.calculate_tax(request3)
    print(f"\nTaxable Income: {tax_result3.taxable_income:,} บาท")
    print(f"Current Tax: {tax_result3.tax_amount:,} บาท")

    tiers3 = [40000, 60000, 80000]
    print(f"\nInvestment Tiers: {tiers3}")
    print("\nCalculating tax savings:\n")

    for tier in tiers3:
        taxable_without = tax_result3.taxable_income + tier
        marginal_rate = calculator.get_marginal_tax_rate(taxable_without)
        tax_saving = int(tier * (marginal_rate / 100))

        print(f"Investment: {tier:>7,} บาท")
        print(f"  → Taxable without investment: {taxable_without:,} บาท")
        print(f"  → Marginal rate at that level: {marginal_rate}%")
        print(f"  → Tax saving: {tax_saving:,} บาท")
        print()

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("\nThe ground truth in evaluation_test_data.py needs to be updated")
    print("with these CORRECT tax saving values based on Thai tax law.")
    print("\nKey principle:")
    print("  Tax Saving = Investment × Marginal Rate at (Current Taxable + Investment)")
    print()


if __name__ == "__main__":
    calculate_correct_tax_savings()
