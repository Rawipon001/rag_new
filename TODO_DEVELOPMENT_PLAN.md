# 📋 TODO: สิ่งที่ต้องพัฒนาเพิ่มเติม
**Updated:** 2025-10-29
**Status:** หลังแก้ไข Critical Bugs เสร็จแล้ว

---

## ✅ **สิ่งที่แก้ไขเสร็จแล้ว**

### 1. Backend Validation ✅
- [x] เพิ่มการตรวจสอบ 15% limit สำหรับ ประกันบำนาญ
- [x] เพิ่มการตรวจสอบ 30% limit สำหรับ RMF, ThaiESG
- [x] เพิ่มการตรวจสอบ 15% limit สำหรับ PVD, กบข.
- [x] สร้าง error messages ที่ชัดเจน

### 2. AI Service Auto-Correction ✅
- [x] ตรวจจับเมื่อ AI แนะนำเกินขีดจำกัด
- [x] Auto-correct ให้เป็นจำนวนที่ถูกกฎหมาย
- [x] คำนวณ tax saving ใหม่ให้ถูกต้อง

### 3. Frontend Dynamic Limits ✅
- [x] แสดงขีดจำกัดตามรายได้ของผู้ใช้
- [x] แสดง warning เมื่อกรอกเกิน
- [x] เพิ่ม max attribute ในช่อง input

### 4. Documentation ✅
- [x] TAX_VALIDATION_FIX_REPORT.md
- [x] ILLEGAL_AMOUNT_ANALYSIS.md
- [x] Test scripts (test_validation_fixes.py, verify_illegal_amount.py)

---

## 🚧 **สิ่งที่ต้องพัฒนาต่อ (Priority สูง)**

### 1. 🔴 **CRITICAL: ปรับปรุง Evaluation System**

#### ปัญหา
```
❌ ตอนนี้ Numerical Accuracy = 100% แต่จริงๆ มี AI แนะนำเกินกฎหมาย!
```

#### สิ่งที่ต้องทำ
```python
# เพิ่มใน evaluation_service.py

def validate_legal_compliance(
    self,
    plan: Dict,
    gross_income: int
) -> Dict[str, Any]:
    """
    ตรวจสอบว่าแผนการลงทุนถูกกฎหมายหรือไม่

    Returns:
        {
            "is_legal": True/False,
            "violations": [
                {
                    "category": "ประกันบำนาญ",
                    "recommended": 274920,
                    "legal_max": 200000,
                    "excess": 74920,
                    "violation_percentage": 37.5
                }
            ]
        }
    """
    violations = []

    # เช็ค ประกันบำนาญ (15% or 200,000)
    for allocation in plan["allocations"]:
        if "ประกันบำนาญ" in allocation["category"]:
            amount = allocation.get("investment_amount", 0)
            max_pension = min(int(gross_income * 0.15), 200000)

            if amount > max_pension:
                violations.append({
                    "category": "ประกันบำนาญ",
                    "recommended": amount,
                    "legal_max": max_pension,
                    "excess": amount - max_pension,
                    "violation_percentage": ((amount - max_pension) / max_pension) * 100
                })

    # เช็ค RMF (30% or 500,000)
    # เช็ค ThaiESG (30% or 300,000)
    # ... ต่อไป

    return {
        "is_legal": len(violations) == 0,
        "violations": violations,
        "legal_compliance_score": 0 if violations else 100
    }
```

#### Integration กับ Evaluation
```python
# ใน run_evaluation_complete.py

async def run_single_test_case(self, test_case, test_id):
    # ... existing code ...

    # 🆕 เพิ่มการตรวจสอบกฎหมาย
    for plan in ai_plans:
        legal_check = self.evaluator.validate_legal_compliance(
            plan=plan,
            gross_income=request.gross_income
        )

        if not legal_check["is_legal"]:
            # ลดคะแนน Numerical Accuracy เป็น 0
            scores["numerical_accuracy"] = 0
            scores["legal_compliance"] = 0

            # บันทึก violations
            scores["violations"] = legal_check["violations"]

            print(f"❌ Legal Violation Detected in Plan {plan['plan_id']}:")
            for v in legal_check["violations"]:
                print(f"   {v['category']}: {v['recommended']:,} > {v['legal_max']:,}")
```

#### Expected Output
```
📊 Test Case 1: รายได้ 1,000,000 บาท

Plan A:
  ✅ Legal Compliance: PASS
  ✅ Numerical Accuracy: 100%

Plan B:
  ❌ Legal Compliance: FAILED
  ❌ Numerical Accuracy: 0% (มี Legal Violations)

  Violations:
    • ประกันบำนาญ: แนะนำ 274,920 บาท
      → Legal Max: 150,000 บาท (15% of 1,000,000)
      → เกิน: 124,920 บาท (83.3%)
      → Tax Saving Miscalculation: 37,476 บาท (overstated)

Overall Score: 50% (Plan A pass, Plan B fail)
```

**Timeline:** 2-3 วัน
**Priority:** 🔴 CRITICAL

---

### 2. 🟠 **HIGH: ตรวจสอบ Test Data ทั้งหมด**

#### ปัญหา
```
Test data อาจมีจำนวนที่ใกล้เคียงขีดจำกัด แต่ไม่ได้ test edge cases
```

#### สิ่งที่ต้องทำ

**A. เพิ่ม Edge Case Tests**
```python
# ใน evaluation_test_data.py

# Test Case 8: รายได้ต่ำ - ประกันบำนาญเกิน 15%
TEST_CASE_8 = {
    "name": "Edge Case: รายได้ต่ำ ประกันบำนาญเกิน 15%",
    "input": {
        "gross_income": 600000,
        "pension_insurance": 100000,  # เกิน! (15% = 90,000)
    },
    "expected_behavior": {
        "should_reject": True,
        "error_message": "ประกันบำนาญเกินขีดจำกัด",
        "max_allowed": 90000
    }
}

# Test Case 9: รายได้สูง - ประกันบำนาญถึง absolute limit
TEST_CASE_9 = {
    "name": "Edge Case: รายได้สูงมาก ประกันบำนาญ 200K",
    "input": {
        "gross_income": 2000000,
        "pension_insurance": 200000,  # ถูกต้อง (15% = 300K แต่ติด absolute 200K)
    },
    "expected_behavior": {
        "should_accept": True
    }
}

# Test Case 10: รายได้สูง - ประกันบำนาญเกิน absolute limit
TEST_CASE_10 = {
    "name": "Edge Case: ประกันบำนาญ 274,920 (เกิน absolute)",
    "input": {
        "gross_income": 2000000,
        "pension_insurance": 274920,  # เกิน absolute limit!
    },
    "expected_behavior": {
        "should_reject": True,
        "error_message": "ประกันบำนาญเกินขีดจำกัด",
        "max_allowed": 200000
    }
}
```

**B. เพิ่ม Combined Limit Tests**
```python
# Test Case 11: รวม RMF + PVD + GPF ต้องไม่เกิน 500K
TEST_CASE_11 = {
    "name": "Combined Limit: RMF + PVD + GPF",
    "input": {
        "gross_income": 2000000,
        "rmf": 300000,
        "provident_fund": 200000,
        "gpf": 100000,  # รวม = 600K (เกิน 500K!)
    },
    "expected_behavior": {
        "should_reject": True,
        "error_message": "รวม RMF + PVD + GPF เกิน 500,000",
        "combined_max": 500000
    }
}
```

**Timeline:** 1-2 วัน
**Priority:** 🟠 HIGH

---

### 3. 🟠 **HIGH: เพิ่ม Combined Limits Validation**

#### ปัญหา
```
ตอนนี้เช็คแยกรายการ แต่ยังไม่เช็ครวม
เช่น: RMF + PVD + GPF + Pension ≤ 500,000 (ตามกฎหมาย)
```

#### สิ่งที่ต้องทำ
```python
# ใน tax_calculator.py

def _validate_combined_limits(self, request: TaxCalculationRequest) -> None:
    """
    ตรวจสอบขีดจำกัดรวม (Combined Limits)

    ตาม tax_deductions_update280168.pdf:
    1. RMF + PVD + GPF + Pension + Teacher Fund ≤ 500,000 บาท
    2. Life Insurance + Health Insurance ≤ 125,000 บาท (100K + 25K)
    3. เงินบริจาคทั่วไป ≤ 10% ของรายได้หลังหักค่าใช้จ่าย
    """

    # 1. กลุ่มกองทุนระยะยาว (Long-term Savings)
    long_term_total = (
        request.rmf +
        request.provident_fund +
        request.gpf +
        request.pvd_teacher +
        request.pension_insurance
    )

    if long_term_total > 500000:
        raise ValueError(
            f"รวมกองทุนระยะยาวเกินขีดจำกัด: {long_term_total:,} บาท "
            f"แต่สูงสุดได้ 500,000 บาท\n"
            f"  - RMF: {request.rmf:,}\n"
            f"  - PVD: {request.provident_fund:,}\n"
            f"  - GPF: {request.gpf:,}\n"
            f"  - ครู: {request.pvd_teacher:,}\n"
            f"  - ประกันบำนาญ: {request.pension_insurance:,}"
        )

    # 2. กลุ่มประกันชีวิต + สุขภาพ
    insurance_total = request.life_insurance + request.health_insurance
    if insurance_total > 125000:
        raise ValueError(
            f"รวมประกันชีวิต + สุขภาพ เกิน: {insurance_total:,} บาท "
            f"(ชีวิต {request.life_insurance:,} + สุขภาพ {request.health_insurance:,}) "
            f"สูงสุดได้ 125,000 บาท"
        )

    # 3. เงินบริจาคทั่วไป (ต้องคำนวณหลังหักค่าใช้จ่าย)
    # จะเช็คในขั้นตอน calculate_tax
```

**ใน calculate_tax เพิ่ม:**
```python
# หลังคำนวณ expense_deduction แล้ว
net_income = gross_income - expense_deduction

# เช็คเงินบริจาคทั่วไป
max_donation = int(net_income * 0.10)
if request.donation_general > max_donation:
    raise ValueError(
        f"เงินบริจาคทั่วไปเกิน: {request.donation_general:,} บาท "
        f"สูงสุดได้ 10% ของเงินได้สุทธิ = {max_donation:,} บาท"
    )
```

**Timeline:** 1 วัน
**Priority:** 🟠 HIGH

---

### 4. 🟡 **MEDIUM: ปรับปรุง Frontend UX**

#### A. Real-time Combined Limit Display
```typescript
// ใน page.tsx

// แสดงยอดรวมกองทุนระยะยาว
const totalLongTerm = formData.rmf + formData.provident_fund +
                      formData.gpf + formData.pension_insurance;

{totalLongTerm > 0 && (
  <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-300">
    <p className="text-sm font-semibold text-blue-900">
      📊 รวมกองทุนระยะยาว: {totalLongTerm.toLocaleString()} บาท
    </p>
    <p className="text-xs text-blue-700">
      ขีดจำกัดรวม: 500,000 บาท
      {totalLongTerm > 500000 && (
        <span className="text-red-600 font-bold">
          ⚠️ เกิน {(totalLongTerm - 500000).toLocaleString()} บาท!
        </span>
      )}
    </p>
  </div>
)}
```

#### B. Interactive Tax Calculator
```typescript
// แสดงการคำนวณภาษีแบบ step-by-step

<div className="tax-breakdown">
  <h3>การคำนวณภาษีของคุณ</h3>

  <div className="step">
    <span>1. รายได้รวม:</span>
    <span>{gross_income.toLocaleString()} บาท</span>
  </div>

  <div className="step">
    <span>2. หักค่าใช้จ่าย (50%):</span>
    <span>-{expense.toLocaleString()} บาท</span>
  </div>

  <div className="step">
    <span>3. หักค่าลดหย่อน:</span>
    <span>-{deductions.toLocaleString()} บาท</span>
  </div>

  <div className="step total">
    <span>4. เงินได้สุทธิ:</span>
    <span>{taxable.toLocaleString()} บาท</span>
  </div>

  <div className="step tax">
    <span>5. ภาษีที่ต้องจ่าย:</span>
    <span className="text-red-600 font-bold">
      {tax.toLocaleString()} บาท
    </span>
  </div>
</div>
```

**Timeline:** 2-3 วัน
**Priority:** 🟡 MEDIUM

---

### 5. 🟡 **MEDIUM: Audit Existing User Data**

#### สิ่งที่ต้องทำ
```python
# scripts/audit_user_data.py

"""
ตรวจสอบว่ามีผู้ใช้คนไหนบ้างที่:
1. บันทึกจำนวนเงินที่เกินกฎหมาย
2. ได้รับคำแนะนำที่ผิดพลาด
"""

async def audit_all_users():
    # ถ้ามี database
    users = await get_all_users_from_db()

    violations = []

    for user in users:
        # เช็คประกันบำนาญ
        max_pension = min(user.income * 0.15, 200000)
        if user.pension_insurance > max_pension:
            violations.append({
                "user_id": user.id,
                "email": user.email,
                "category": "pension_insurance",
                "amount": user.pension_insurance,
                "legal_max": max_pension,
                "excess": user.pension_insurance - max_pension
            })

        # เช็ค RMF
        max_rmf = min(user.income * 0.30, 500000)
        if user.rmf > max_rmf:
            violations.append({
                "user_id": user.id,
                "email": user.email,
                "category": "rmf",
                "amount": user.rmf,
                "legal_max": max_rmf,
                "excess": user.rmf - max_rmf
            })

    # สร้างรายงาน
    create_audit_report(violations)

    # ส่งอีเมลแจ้งเตือนผู้ใช้ที่มีปัญหา
    send_correction_emails(violations)
```

**Timeline:** 1 วัน (ถ้ามี database)
**Priority:** 🟡 MEDIUM

---

### 6. 🟢 **LOW: Enhanced Error Messages**

#### สิ่งที่ต้องทำ
```python
# แทนที่ error แบบนี้
raise ValueError("ประกันบำนาญเกินขีดจำกัด")

# เป็นแบบนี้
raise ValidationError(
    category="pension_insurance",
    amount=274920,
    legal_max=150000,
    reason="percentage_limit",  # or "absolute_limit"
    suggestion="ลดจำนวนเป็น 150,000 บาท (15% ของรายได้ 1,000,000)",
    law_reference="tax_deductions_update280168.pdf, Page 2, Item 13"
)
```

**Frontend แสดง:**
```typescript
<div className="error-message">
  <h3>❌ ข้อมูลไม่ถูกต้อง</h3>

  <p className="category">ประกันบำนาญ</p>
  <p className="issue">
    คุณกรอก: <span className="wrong">274,920 บาท</span>
    แต่สูงสุดได้: <span className="correct">150,000 บาท</span>
  </p>

  <p className="reason">
    เหตุผล: รายได้ 1,000,000 × 15% = 150,000 บาท
  </p>

  <button onClick={autoFix}>
    🔧 แก้ไขอัตโนมัติเป็น 150,000 บาท
  </button>

  <a href="/help/pension-insurance">
    📚 เรียนรู้เพิ่มเติมเกี่ยวกับประกันบำนาญ
  </a>
</div>
```

**Timeline:** 2 วัน
**Priority:** 🟢 LOW

---

### 7. 🟢 **LOW: Monitoring & Alerts**

#### สิ่งที่ต้องทำ
```python
# monitoring/alert_system.py

"""
ระบบแจ้งเตือนเมื่อ AI สร้างคำแนะนำที่ใกล้เคียงหรือเกินขีดจำกัด
"""

async def monitor_ai_recommendations(plan: Dict):
    alerts = []

    # เช็คว่าใกล้ขีดจำกัดหรือไม่
    for allocation in plan["allocations"]:
        if "ประกันบำนาญ" in allocation["category"]:
            amount = allocation["investment_amount"]
            legal_max = get_legal_max_pension(user_income)

            percentage_used = (amount / legal_max) * 100

            if percentage_used > 90:  # ใกล้ขีดจำกัด 90%
                alerts.append({
                    "level": "warning",
                    "message": f"ประกันบำนาญใกล้ขีดจำกัด: {percentage_used:.1f}%",
                    "amount": amount,
                    "max": legal_max
                })

            if amount > legal_max:  # เกินขีดจำกัด
                alerts.append({
                    "level": "critical",
                    "message": "ประกันบำนาญเกินขีดจำกัด!",
                    "amount": amount,
                    "max": legal_max,
                    "auto_corrected": True
                })

                # ส่ง alert ไป Slack/Email
                await send_alert_to_team(alerts[-1])

    return alerts
```

**Timeline:** 1 วัน
**Priority:** 🟢 LOW

---

## 📊 **สรุปแผนงานทั้งหมด**

| ลำดับ | งาน | Priority | Timeline | Status |
|-------|-----|----------|----------|--------|
| 1 | เพิ่ม Legal Compliance Check ใน Evaluation | 🔴 CRITICAL | 2-3 วัน | 📋 TODO |
| 2 | เพิ่ม Edge Case Tests | 🟠 HIGH | 1-2 วัน | 📋 TODO |
| 3 | เพิ่ม Combined Limits Validation | 🟠 HIGH | 1 วัน | 📋 TODO |
| 4 | ปรับปรุง Frontend UX | 🟡 MEDIUM | 2-3 วัน | 📋 TODO |
| 5 | Audit User Data | 🟡 MEDIUM | 1 วัน | 📋 TODO |
| 6 | Enhanced Error Messages | 🟢 LOW | 2 วัน | 📋 TODO |
| 7 | Monitoring & Alerts | 🟢 LOW | 1 วัน | 📋 TODO |

**Total Estimate:** 10-13 วันทำงาน

---

## 🎯 **Recommended Priority Order**

### Week 1 (ลำดับความสำคัญสูง)
1. ✅ แก้ไข Critical Bugs (DONE)
2. 🔴 เพิ่ม Legal Compliance Check ใน Evaluation (2-3 วัน)
3. 🟠 เพิ่ม Combined Limits Validation (1 วัน)
4. 🟠 เพิ่ม Edge Case Tests (1-2 วัน)

### Week 2 (ปรับปรุงประสบการณ์ผู้ใช้)
5. 🟡 ปรับปรุง Frontend UX (2-3 วัน)
6. 🟡 Audit User Data (1 วัน)

### Week 3 (เสริมความมั่นคง)
7. 🟢 Enhanced Error Messages (2 วัน)
8. 🟢 Monitoring & Alerts (1 วัน)

---

## 📝 **Notes สำคัญ**

### ข้อควรระวัง
1. ⚠️ ทุกครั้งที่แก้ไข validation logic ต้อง:
   - Update test cases
   - Update documentation
   - Run full evaluation suite
   - Check backward compatibility

2. ⚠️ Combined Limits ต้องตรวจสอบตามกฎหมายให้ละเอียด:
   - บางอย่างรวมกันได้ไม่เกิน 500K
   - บางอย่างมีขีดจำกัดแยก

3. ⚠️ Frontend validation ควรเป็น "helper" เท่านั้น:
   - Backend ต้องเป็น single source of truth
   - Frontend แค่ช่วยผู้ใช้ก่อนส่ง request

### การทดสอบ
- [ ] Unit tests สำหรับทุก validation function
- [ ] Integration tests สำหรับ end-to-end flow
- [ ] Edge case tests สำหรับ boundary values
- [ ] Regression tests เพื่อให้แน่ใจว่าไม่พัง existing features

---

**สรุป:** มีงาน 7 รายการที่ต้องพัฒนาเพิ่มเติม โดยสำคัญที่สุดคือ **Legal Compliance Check ใน Evaluation** เพื่อให้มั่นใจว่าระบบไม่แนะนำสิ่งที่ผิดกฎหมาย
