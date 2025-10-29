"""
Verification Script: Why 274,920 baht in ประกันบำนาญ is ILLEGAL

This script demonstrates the legal violation clearly.
"""

def calculate_pension_insurance_limit(gross_income: int) -> dict:
    """Calculate legal limit for pension insurance according to Thai law"""

    # Thai Tax Law: ประกันบำนาญ maximum is 15% of income OR 200,000 (whichever is lower)
    percentage_limit = int(gross_income * 0.15)
    absolute_limit = 200000
    legal_maximum = min(percentage_limit, absolute_limit)

    return {
        "gross_income": gross_income,
        "15_percent": percentage_limit,
        "absolute_limit": absolute_limit,
        "legal_maximum": legal_maximum
    }


def check_if_legal(gross_income: int, claimed_amount: int) -> dict:
    """Check if the claimed amount is legal"""

    limits = calculate_pension_insurance_limit(gross_income)
    is_legal = claimed_amount <= limits["legal_maximum"]

    violation_amount = 0 if is_legal else claimed_amount - limits["legal_maximum"]
    violation_percentage = 0 if is_legal else (violation_amount / limits["legal_maximum"] * 100)

    return {
        **limits,
        "claimed_amount": claimed_amount,
        "is_legal": is_legal,
        "violation_amount": violation_amount,
        "violation_percentage": violation_percentage
    }


print("=" * 80)
print("VERIFICATION: Is 274,920 baht in ประกันบำนาญ LEGAL?")
print("=" * 80)
print()

# Test Case 1: What income would make 274,920 legal?
print("❓ Question: At what income level would 274,920 baht be legal?")
print()
required_income_for_legal = 274920 / 0.15
print(f"   Answer: You need income of at least {required_income_for_legal:,.0f} baht")
print(f"   Because: {required_income_for_legal:,.0f} × 15% = 274,920")
print(f"   BUT: This exceeds the absolute limit of 200,000 baht!")
print(f"   Conclusion: 274,920 is NEVER legal, even with infinite income! ❌")
print()

print("-" * 80)
print()

# Test Case 2: Common income scenarios
print("📊 Testing 274,920 baht across different income levels:")
print()

test_incomes = [
    600000,   # Low income
    1000000,  # Medium income
    1500000,  # High income
    2000000,  # Very high income
    5000000   # Extremely high income
]

for income in test_incomes:
    result = check_if_legal(income, 274920)

    print(f"Income: {income:,} baht")
    print(f"  • 15% limit: {result['15_percent']:,} baht")
    print(f"  • Absolute limit: {result['absolute_limit']:,} baht")
    print(f"  • Legal maximum: {result['legal_maximum']:,} baht")
    print(f"  • Claimed: {result['claimed_amount']:,} baht")

    if result['is_legal']:
        print(f"  • Status: ✅ LEGAL")
    else:
        print(f"  • Status: ❌ ILLEGAL")
        print(f"  • Violation: {result['violation_amount']:,} baht over limit")
        print(f"  • Percentage over: {result['violation_percentage']:.1f}%")
    print()

print("-" * 80)
print()

# Test Case 3: What's the ACTUAL maximum anyone can claim?
print("💡 What is the ACTUAL maximum ประกันบำนาญ anyone can claim?")
print()
print("   Answer: 200,000 baht")
print("   Reason: Even though the rule is '15% or 200,000 (whichever is lower)',")
print("           the absolute cap is 200,000 baht for ALL income levels.")
print()
print("   To reach 200,000 legally:")
required_income = 200000 / 0.15
print(f"   • Minimum income needed: {required_income:,.0f} baht")
print(f"   • Because: {required_income:,.0f} × 15% = 200,000")
print()

print("-" * 80)
print()

# Test Case 4: Specific example from the webpage
print("🚨 WEBPAGE VIOLATION ANALYSIS")
print()
print("The webpage shows:")
print("  • ประกันบำนาญ: 274,920 baht")
print("  • สัดส่วน: 22.9%")
print("  • ประหยัดภาษี: 82,476 baht")
print()

# Calculate what income would give 22.9% allocation
implied_investment_total = 274920 / 0.229
print(f"Implied total investment: {implied_investment_total:,.0f} baht (from 22.9%)")
print()

# Test with likely income scenarios
print("Testing possible income levels that might generate this:")
print()

likely_incomes = [1200000, 1500000, 1833200]
for income in likely_incomes:
    result = check_if_legal(income, 274920)
    tax_saving = result['legal_maximum'] * 0.30  # Assume 30% marginal rate

    print(f"If income = {income:,} baht:")
    print(f"  • Legal max: {result['legal_maximum']:,} baht")
    print(f"  • Claimed: 274,920 baht")
    print(f"  • Status: ❌ ILLEGAL - exceeds by {result['violation_amount']:,} baht")
    print(f"  • Real tax saving: {tax_saving:,.0f} baht (not 82,476!)")
    print()

print("=" * 80)
print("CONCLUSION")
print("=" * 80)
print()
print("❌ 274,920 baht in ประกันบำนาญ is ILLEGAL for ALL income levels")
print()
print("Legal maximums:")
print("  • Income 600,000: max 90,000 baht (15%)")
print("  • Income 1,000,000: max 150,000 baht (15%)")
print("  • Income 1,333,334+: max 200,000 baht (absolute cap)")
print()
print("⚠️  This webpage recommendation violates Thai Tax Law 2568!")
print("⚠️  Users following this advice could face legal consequences!")
print()
print("=" * 80)
