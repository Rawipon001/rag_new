# Fix: Insurance Deduction Limit Violations

## Problem Identified

The AI Tax Advisor was recommending investment amounts that **violate Thai tax law limits**:

### Example Violation:
- **ประกันชีวิตและสุขภาพ (Life & Health Insurance):** Recommended 320,000 บาท
- **Legal Limit:**
  - ประกันชีวิต (Life Insurance): Maximum **100,000 บาท**
  - ประกันสุขภาพ (Health Insurance): Maximum **25,000 บาท**
  - Combined Maximum: **125,000 บาท**

**The system was recommending 320,000 บาท - which is 2.56x over the legal limit!**

## Root Cause

1. The AI prompt did not emphasize the legal limits strongly enough
2. No validation was performed on the generated recommendations
3. The prompt template showed examples without clear warnings about limits

## Solution Implemented

### 1. Enhanced AI Prompt (ai_service.py:152-162)

Added a dedicated section with clear warnings:

```
🚨 **วงเงินลดหย่อนสูงสุดตามกฎหมายที่ต้องปฏิบัติตาม (ห้ามเกิน!):**
- ประกันชีวิต: สูงสุด 100,000 บาท
- ประกันชีวิตแบบบำนาญ: สูงสุด 10,000 บาท
- ประกันสุขภาพ: สูงสุด 25,000 บาท
- ประกันบำนาญ: สูงสุด 200,000 บาท หรือ 15% ของรายได้ (เลือกน้อยกว่า)
- RMF: สูงสุด 500,000 บาท หรือ 30% ของรายได้ (เลือกน้อยกว่า)
- ThaiESG/ThaiESGX: สูงสุด 300,000 บาท แต่ละประเภท, ยกเว้น 30% ของรายได้
- กองทุนสำรองเลี้ยงชีพ (PVD): สูงสุด 500,000 บาท หรือ 15% ของรายได้
- Easy e-Receipt: สูงสุด 50,000 บาท

⚠️ **คำเตือนสำคัญ:** หากแนะนำเกินวงเงินที่กฎหมายกำหนด จะถือว่าผิดกฎหมายและทำให้ลูกค้าเสียหาย!
```

### 2. Updated Rules Section (ai_service.py:174-184)

Added explicit rule #5 with calculations:

```
5. 🚨 **ห้ามเกินวงเงินตามกฎหมาย:**
   - ประกันชีวิต ≤ 100,000 บาท (รวมทุกประเภท)
   - ประกันสุขภาพ ≤ 25,000 บาท
   - ประกันชีวิต + สุขภาพ รวม ≤ 125,000 บาท
   - ถ้าแนะนำ "ประกันชีวิตและสุขภาพ" ต้องแยกชัดเจนว่าเป็นประกันชีวิตเท่าไร สุขภาพเท่าไร
```

### 3. Added Calculation Examples (ai_service.py:328-333)

Provided concrete examples to guide the AI:

```
- 🚨 **วงเงินตามกฎหมายที่ห้ามเกิน:**
  * ประกันชีวิต: สูงสุด 100,000 บาท
  * ประกันสุขภาพ: สูงสุด 25,000 บาท
  * เมื่อคำนวณเป็นเงิน (total_investment × percentage) ต้องไม่เกินวงเงินที่กฎหมายกำหนด
  * ตัวอย่าง: ถ้า total_investment = 800,000 และแนะนำประกันชีวิต 40% = 320,000 (ผิด! เกิน 100,000)
  * ต้องปรับ: ประกันชีวิต ≤ 12.5% ของ 800,000 = 100,000 บาท
```

### 4. Post-Generation Validation (ai_service.py:391-433)

Added validation logic that:
- Calculates actual investment amounts from percentages
- Tracks total life insurance and health insurance across allocations
- Prints warnings when limits are exceeded
- Helps identify problematic recommendations

```python
# Check legal limits for insurance
if "ประกันชีวิต" in alloc["category"] and "สุขภาพ" not in alloc["category"]:
    life_insurance_total += amount
    if amount > 100000:
        print(f"⚠️ Warning: Plan {i+1} allocation '{alloc['category']}' recommends {amount:,} บาท (exceeds 100,000 legal limit)")

if "สุขภาพ" in alloc["category"]:
    health_insurance_total += amount
    if amount > 25000:
        print(f"⚠️ Warning: Plan {i+1} allocation '{alloc['category']}' recommends {amount:,} บาท (exceeds 25,000 legal limit)")
```

## Expected Outcome

After this fix:

1. **AI will be more aware** of legal limits when generating recommendations
2. **Percentages will be adjusted** to ensure calculated amounts don't exceed limits
3. **Validation warnings** will appear in logs if limits are still violated
4. **User recommendations will be legal and compliant** with Thai tax law

## Testing

To verify the fix works:

```bash
cd /Users/atikun/Desktop/Rag/rag_new/backend
python3 scripts/run_evaluation_complete.py
```

Look for:
- ✅ No warnings about exceeding insurance limits
- ✅ All insurance recommendations ≤ 100,000 (life) and ≤ 25,000 (health)
- ✅ BLEU-4 and BERTScore remain high (showing quality is maintained)

## Legal Reference

According to Thai tax law (ปี 2568):
- **ประกันชีวิต (Life Insurance):** Maximum deduction 100,000 บาท
- **ประกันสุขภาพ (Health Insurance):** Maximum deduction 25,000 บาท
- **ประกันบำนาญ (Pension Insurance):** Maximum 200,000 บาท or 15% of income
- **RMF:** Maximum 500,000 บาท or 30% of income
- **ThaiESG/ThaiESGX:** Maximum 300,000 บาท each, exempt 30% of income

Source: `/Users/atikun/Desktop/Rag/rag_new/backend/data/tax_knowledge/tax_deductions_2025.txt` (lines 84-118)
