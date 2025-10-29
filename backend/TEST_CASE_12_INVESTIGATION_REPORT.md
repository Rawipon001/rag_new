# Test Case 12 Investigation Report
## ร้านอาหาร 1.5M - ความเสี่ยงกลาง

Generated: 2025-10-29

---

## ISSUE SUMMARY

Test Case 12 has severely degraded performance compared to all other test cases:

- **Description BLEU-4**: 100% → **6.0%** (94% decrease)
- **Description BERTScore**: 100% → **77.8%** (22% decrease)
- **Status**: All other 19 test cases remain at 100% for both metrics

---

## ROOT CAUSE ANALYSIS

### PRIMARY FINDING: OpenAI API Refusal

The OpenAI API **refused to generate a response** for Test Case 12, returning:

```
"I'm sorry, I can't assist with that request."
```

### Fallback Behavior

When the AI refuses or fails to respond, the system activates fallback plans with generic descriptions:

**AI Generated Descriptions (Fallback):**
- Plan 1: "แผนสำรอง - เน้นความคุ้มครอง" (Fallback - Focus on protection)
- Plan 2: "แผนสำรอง - กระจายความเสี่ยง" (Fallback - Diversify risk)
- Plan 3: "แผนสำรอง - ใช้วงเงินเต็มที่" (Fallback - Use full budget)

**Expected Descriptions:**
- Plan 1: "เน้นความคุ้มครอง เงินลงทุนพอเหมาะสำหรับรายได้ระดับกลาง"
- Plan 2: "กระจายความเสี่ยง เน้นการลงทุนแบบสมดุลระหว่างประกันและกองทุน"
- Plan 3: "เน้นลดหย่อนภาษีสูงสุด ใช้วงเงินลงทุนเต็มที่สำหรับผลประโยชน์ทางภาษีสูงสุด"

### BLEU-4 Scores by Plan

From `evaluation_results.plan_metrics`:

- **Plan 1**: `desc_bleu4` = 0.1226 (12.3%)
- **Plan 2**: `desc_bleu4` = 0.0418 (4.2%)
- **Plan 3**: `desc_bleu4` = 0.0151 (1.5%)
- **Average**: 5.98% ≈ **6.0%**

The fallback descriptions have almost zero overlap with expected descriptions, causing catastrophic BLEU-4 failure.

---

## WHY DID OpenAI REFUSE THIS SPECIFIC REQUEST?

Possible reasons:

1. **Content Policy Trigger**: The prompt may contain words or patterns that trigger OpenAI's content policy filters
2. **Rate Limiting**: Temporary API issue during evaluation run
3. **Input Characteristics**: Test Case 12 (restaurant business with 1.5M income) may have unique input that differs from others
4. **Randomness**: OpenAI's safety filters can occasionally have false positives

### Test Case 12 Input Characteristics

```python
{
    "income_type": "รายได้จากธุรกิจ (ร้านอาหาร)",  # Business income (restaurant)
    "annual_income": 1500000,
    "investment_budget": 800000,
    "risk_tolerance": "medium"
}
```

This is a **standard business scenario** and should not trigger content policy. Most likely a **temporary API issue** or **false positive** from OpenAI's safety filters.

---

## SOLUTIONS

### Option A: Retry Test Case 12 (RECOMMENDED)

**Rationale**: Since this is likely a temporary API issue or false positive, re-running the evaluation for Test Case 12 should resolve it.

**Action**:
```bash
python3 scripts/run_evaluation_complete.py --mode full --test-case 12 --bertscore
```

**Pros**:
- Likely to succeed on retry
- No code changes needed
- Preserves data integrity

**Cons**:
- May fail again if persistent content policy issue
- Requires re-running evaluation

---

### Option B: Improve Fallback Descriptions

**Rationale**: Make fallback plans generate better default descriptions that are closer to expected patterns.

**Action**: Update fallback logic in `ai_service.py` or `ai_service_for_evaluation.py` to use more detailed descriptions.

**Pros**:
- Improves robustness when AI refuses
- Provides better user experience for edge cases

**Cons**:
- Doesn't fix the root cause (API refusal)
- More complex fallback logic
- Still won't match exact expected descriptions

---

### Option C: Investigate Prompt Engineering

**Rationale**: Modify the prompt to avoid triggering content policy filters.

**Action**: Review the prompt sent to OpenAI API for Test Case 12 and identify potential triggers.

**Pros**:
- May prevent future refusals
- Improves prompt robustness

**Cons**:
- Time-consuming investigation
- May not be the actual cause
- Other test cases work fine with same prompt structure

---

### Option D: Update Expected Data for Test Case 12

**Rationale**: Accept the fallback descriptions as valid and update test data to match.

**Action**: Change expected descriptions to match fallback text.

**Pros**:
- Quick fix
- Test would pass

**Cons**:
- **NOT RECOMMENDED** - Fallback descriptions are inferior quality
- Defeats purpose of evaluation
- Masks underlying API issue

---

## RECOMMENDED SOLUTION

**Option A: Retry Test Case 12**

This is almost certainly a temporary API issue or false positive from OpenAI's safety filters. Re-running the evaluation should resolve it.

If the retry fails again:
1. Check OpenAI API status/logs for any errors
2. Review the exact prompt being sent for Test Case 12
3. Consider temporarily using a different model or API endpoint
4. Implement Option B (better fallback descriptions) as backup

---

## VERIFICATION STEPS

After implementing the fix:

1. ✅ Run evaluation for Test Case 12 specifically
2. ✅ Verify raw response is NOT "I'm sorry, I can't assist with that request."
3. ✅ Verify Description BLEU-4 returns to 100%
4. ✅ Verify Description BERTScore returns to 100%
5. ✅ Verify all 3 plans have proper descriptions (not fallback)
6. ✅ Run full evaluation on all 20 test cases to confirm no regression

---

## ADDITIONAL NOTES

- **All other 19 test cases**: Working perfectly with 100% scores
- **Numeric accuracy**: Test Case 12 still has 100% numeric accuracy (fallback uses correct numbers)
- **Evaluation system**: Working correctly - properly detected the mismatch
- **No code bugs**: The low scores accurately reflect the AI refusal and fallback activation

This is an **AI API issue**, not an evaluation system bug.
