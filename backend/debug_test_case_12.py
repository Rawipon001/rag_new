import json

# Load the latest detailed results
with open("evaluation_output/results/detailed_results_20251029_043328.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Find test case 12 (it's the 12th element in the list, index 11)
# Or search by test case name
test_12_results = None
for test_case in data:
    if "ร้านอาหาร" in test_case.get("test_case_name", ""):
        test_12_results = test_case
        break

if not test_12_results:
    print("ERROR: Could not find Test Case 12")
    exit(1)

print("=" * 80)
print("TEST CASE 12: ร้านอาหาร 1.5M - ความเสี่ยงกลาง")
print("=" * 80)

# Check each plan from evaluation_results
eval_results = test_12_results.get("evaluation_results", {})
plan_results = eval_results.get("plan_results", [])

for plan in plan_results:
    plan_num = plan["plan_number"]
    print(f"\n{'='*60}")
    print(f"Plan {plan_num}")
    print('='*60)

    ai_desc = plan["ai_description"]
    exp_desc = plan["expected_description"]

    print("\nACTUAL AI DESCRIPTION:")
    print(f'  "{ai_desc}"')

    print("\nEXPECTED DESCRIPTION:")
    print(f'  "{exp_desc}"')

    bleu = plan.get("description_bleu4", 0)
    bert = plan.get("description_bertscore", 0)

    print("\nSCORES:")
    print(f"  Description BLEU-4: {bleu:.4f} ({bleu*100:.1f}%)")
    print(f"  Description BERTScore: {bert:.4f} ({bert*100:.1f}%)")

    if ai_desc != exp_desc:
        print("\n⚠️  MISMATCH DETECTED!")
        print(f"\nDifference Analysis:")
        print(f"  AI length: {len(ai_desc)} chars")
        print(f"  Expected length: {len(exp_desc)} chars")

        # Character by character comparison
        print("\n  Character-by-character comparison:")
        for i, (a, e) in enumerate(zip(ai_desc, exp_desc)):
            if a != e:
                print(f"    Position {i}: AI='{a}' ({ord(a)}) vs Expected='{e}' ({ord(e)})")
    else:
        print("\n✅ PERFECT MATCH!")
