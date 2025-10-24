"""
Test Data สำหรับ Evaluation - ปี 2568 (ฉบับสมบูรณ์)
มี ground truth ที่ครอบคลุมสำหรับเทียบกับคำตอบของ AI
อัปเดตให้ตรงกับระบบหลัก: ไม่มี SSF, มี ThaiESG/ThaiESGX

ครอบคลุม:
- 5 ระดับรายได้ (300K, 600K, 1M, 1.5M, 3M+)
- 3 ระดับความเสี่ยง (low, medium, high)
- รวม 15 test cases พร้อม ground truth ที่ละเอียด
"""

from typing import List, Dict, Any


class EvaluationTestData:
    """
    ข้อมูลสำหรับ test evaluation - ปี 2568
    """
    
    # ===================================
    # Test Case 1: รายได้ 600,000 - ความเสี่ยงกลาง
    # ===================================
    TEST_CASE_1 = {
        "name": "รายได้ 600K - ความเสี่ยงกลาง",
        "description": "กรณีทดสอบสำหรับผู้มีรายได้ปานกลาง ต้องการสมดุลระหว่างความปลอดภัยและการเติบโต",
        "input": {
            "gross_income": 600000,
            "personal_deduction": 60000,
            "spouse_deduction": 0,
            "child_deduction": 0,
            "parent_support": 0,
            "disabled_support": 0,
            "life_insurance": 50000,
            "life_insurance_pension": 0,
            "life_insurance_parents": 0,
            "health_insurance": 15000,
            "health_insurance_parents": 0,
            "social_security": 9000,
            "pension_insurance": 0,
            "provident_fund": 50000,
            "gpf": 0,
            "pvd_teacher": 0,
            "rmf": 0,
            "thai_esg": 0,
            "thai_esgx_new": 0,
            "thai_esgx_ltf": 0,
            "stock_investment": 0,
            "easy_e_receipt": 0,
            "home_loan_interest": 0,
            "nsf": 0,
            "donation_general": 0,
            "donation_education": 0,
            "donation_social_enterprise": 0,
            "donation_political": 0,
            "risk_tolerance": "medium"
        },
        "expected_tax_result": {
            "gross_income": 600000,
            "taxable_income": 416000,
            "tax_amount": 21800,
            "effective_tax_rate": 3.63,
            "marginal_tax_rate": 10
        },
        "expected_plans": {
            "plan_1": {
                "plan_id": "1",
                "plan_name": "ทางเลือกที่ 1 - เน้นประกัน",
                "plan_type": "medium",
                "description": "เน้นความคุ้มครองและความปลอดภัย เหมาะสำหรับผู้ที่ต้องการสร้างรากฐานทางการเงินที่มั่นคง ลงทุนในประกันชีวิต ประกันสุขภาพ และประกันบำนาญ เพื่อให้มีความคุ้มครองครบถ้วน",
                "total_investment": 150000,
                "total_tax_saving": 15000,
                "overall_risk": "medium",
                "allocations": [
                    {
                        "category": "ประกันชีวิต",
                        "investment_amount": 50000,
                        "percentage": 33.33,
                        "tax_saving": 5000,
                        "risk_level": "low",
                        "pros": ["มีความคุ้มครองชีวิต", "ความเสี่ยงต่ำ", "จำเป็นสำหรับทุกคน", "ลดหย่อนภาษีได้"],
                        "cons": ["ผลตอบแทนต่ำ 2-4%", "ค่าธรรมเนียมสูง", "เบี้ยเพิ่มตามอายุ"]
                    },
                    {
                        "category": "ประกันสุขภาพ",
                        "investment_amount": 10000,
                        "percentage": 6.67,
                        "tax_saving": 1000,
                        "risk_level": "low",
                        "pros": ["คุ้มครองสุขภาพ", "จำเป็นสำหรับทุกคน", "ลดหย่อนภาษีได้", "ลดภาระค่ารักษา"],
                        "cons": ["ไม่มีผลตอบแทน", "เบี้ยเพิ่มตามอายุ", "มีข้อจำกัดในการเคลม"]
                    },
                    {
                        "category": "ประกันบำนาญ",
                        "investment_amount": 40000,
                        "percentage": 26.67,
                        "tax_saving": 4000,
                        "risk_level": "low",
                        "pros": ["รับประกันผลตอบแทน 3-4%", "เหมาะกับวัยใกล้เกษียณ", "มีรายได้หลังเกษียณ", "ลดหย่อนได้ 15%"],
                        "cons": ["ผูกพันยาว", "ถอนก่อนเวลาขาดทุน", "ผลตอบแทนต่ำกว่ากองทุน", "ไม่สามารถปรับเปลี่ยนได้"]
                    },
                    {
                        "category": "RMF ตราสารหนี้/ผสม",
                        "investment_amount": 50000,
                        "percentage": 33.33,
                        "tax_saving": 5000,
                        "risk_level": "medium",
                        "pros": ["ลดหย่อนภาษีสูง 30%", "ผลตอบแทนดีกว่าเงินฝาก 4-6%", "กระจายความเสี่ยง", "เหมาะกับการเกษียณ"],
                        "cons": ["ต้องถือจนอายุ 55 ปี หรือ 5 ปี", "มีความเสี่ยงตามตลาด", "ต้องซื้อทุกปี"]
                    }
                ]
            },
            "plan_2": {
                "plan_id": "2",
                "plan_name": "ทางเลือกที่ 2 - สมดุล",
                "plan_type": "medium",
                "description": "กระจายความเสี่ยงอย่างสมดุล ผสมผสานระหว่างความปลอดภัยและการเติบโต เน้น RMF และ ThaiESG เป็นหลัก พร้อมประกันครบถ้วน เหมาะสำหรับผู้ที่ต้องการผลตอบแทนที่ดีแต่ยังคงมีความคุ้มครอง",
                "total_investment": 250000,
                "total_tax_saving": 25000,
                "overall_risk": "medium",
                "allocations": [
                    {
                        "category": "RMF กองทุนผสม",
                        "investment_amount": 120000,
                        "percentage": 48.0,
                        "tax_saving": 12000,
                        "risk_level": "medium",
                        "pros": ["ลดหย่อนภาษีสูงสุด 30%", "เหมาะกับการเกษียณ", "ผลตอบแทน 5-8%", "บังคับออม"],
                        "cons": ["ต้องซื้อทุกปี", "ถอนก่อนเวลามีภาษีเพิ่ม", "มีความเสี่ยงตามตลาด"]
                    },
                    {
                        "category": "ThaiESG",
                        "investment_amount": 60000,
                        "percentage": 24.0,
                        "tax_saving": 6000,
                        "risk_level": "medium",
                        "pros": ["ยืดหยุ่นกว่า RMF", "ลงทุนใน ESG", "ยกเว้น 30%", "ผลตอบแทน 5-7%", "ส่งเสริมความยั่งยืน"],
                        "cons": ["ต้องถือครบ 8 ปี", "กองทุนใหม่ ข้อมูลน้อย", "มีความเสี่ยงตามตลาด"]
                    },
                    {
                        "category": "ประกันชีวิต + สุขภาพ",
                        "investment_amount": 35000,
                        "percentage": 14.0,
                        "tax_saving": 3500,
                        "risk_level": "low",
                        "pros": ["ความคุ้มครองชีวิต", "ลดหย่อนภาษีได้", "จำเป็นต้องมี", "ความปลอดภัยสูง"],
                        "cons": ["ผลตอบแทนต่ำ", "เบี้ยเพิ่มตามอายุ", "ค่าธรรมเนียมสูง"]
                    },
                    {
                        "category": "ประกันบำนาญ",
                        "investment_amount": 35000,
                        "percentage": 14.0,
                        "tax_saving": 3500,
                        "risk_level": "low",
                        "pros": ["รับประกันผลตอบแทน", "มีรายได้หลังเกษียณ", "ลดภาษีได้", "ความเสี่ยงต่ำ"],
                        "cons": ["ผูกพันยาว", "ผลตอบแทนต่ำ", "ไม่สามารถปรับเปลี่ยนได้"]
                    }
                ]
            },
            "plan_3": {
                "plan_id": "3",
                "plan_name": "ทางเลือกที่ 3 - ลงทุนสูงสุด",
                "plan_type": "medium",
                "description": "ใช้วงเงินลดหย่อนเต็มที่ เพื่อลดภาษีสูงสุด เหมาะสำหรับผู้มีวินัยการเงิน มีเงินทุนเพียงพอ และต้องการสร้างผลตอบแทนระยะยาว ลงทุนใน RMF เต็มวงเงิน พร้อม ThaiESG และประกัน",
                "total_investment": 300000,
                "total_tax_saving": 30000,
                "overall_risk": "medium",
                "allocations": [
                    {
                        "category": "RMF (ใช้วงเงินเต็มที่)",
                        "investment_amount": 180000,
                        "percentage": 60.0,
                        "tax_saving": 18000,
                        "risk_level": "medium",
                        "pros": ["ลดหย่อนภาษีสูงสุด 30%", "ผลตอบแทนดี 5-8%", "บังคับออม", "เหมาะกับการเกษียณ"],
                        "cons": ["ต้องซื้อทุกปี", "ความเสี่ยงตามตลาด", "ถือจนอายุ 55 ปี", "ถอนก่อนเวลามีภาษี"]
                    },
                    {
                        "category": "ThaiESG",
                        "investment_amount": 60000,
                        "percentage": 20.0,
                        "tax_saving": 6000,
                        "risk_level": "medium",
                        "pros": ["ยกเว้นภาษี 30%", "ลงทุนใน ESG", "ยืดหยุ่นกว่า RMF", "ส่งเสริมความยั่งยืน"],
                        "cons": ["ต้องถือ 8 ปี", "กองทุนใหม่", "มีความเสี่ยงตามตลาด"]
                    },
                    {
                        "category": "ประกันบำนาญ",
                        "investment_amount": 30000,
                        "percentage": 10.0,
                        "tax_saving": 3000,
                        "risk_level": "low",
                        "pros": ["รับประกันผลตอบแทน", "ลดหย่อนได้ 15%", "มีรายได้หลังเกษียณ"],
                        "cons": ["ผูกพันยาว", "ผลตอบแทนต่ำ", "ไม่สามารถปรับเปลี่ยน"]
                    },
                    {
                        "category": "ประกันชีวิต + สุขภาพ",
                        "investment_amount": 20000,
                        "percentage": 6.67,
                        "tax_saving": 2000,
                        "risk_level": "low",
                        "pros": ["จำเป็นต้องมี", "ลดหย่อนภาษีได้", "ความคุ้มครองชีวิต"],
                        "cons": ["ผลตอบแทนต่ำ", "เบี้ยเพิ่มตามอายุ"]
                    },
                    {
                        "category": "Easy e-Receipt",
                        "investment_amount": 10000,
                        "percentage": 3.33,
                        "tax_saving": 1000,
                        "risk_level": "low",
                        "pros": ["ใช้จ่ายปกติ", "ลดหย่อนได้ 50,000", "ไม่ต้องลงทุนเพิ่ม", "สะดวก"],
                        "cons": ["ต้องใช้จ่ายผ่าน e-payment", "จำกัดการใช้งาน", "ต้องเก็บหลักฐาน"]
                    }
                ]
            }
        }
    }
    
    # ===================================
    # Test Case 2: รายได้ 1,500,000 - ความเสี่ยงสูง
    # ===================================
    TEST_CASE_2 = {
        "name": "รายได้ 1.5M - ความเสี่ยงสูง",
        "description": "กรณีทดสอบสำหรับผู้มีรายได้สูง ยอมรับความเสี่ยงเพื่อผลตอบแทนที่สูงขึ้น",
        "input": {
            "gross_income": 1500000,
            "personal_deduction": 60000,
            "spouse_deduction": 0,
            "child_deduction": 0,
            "parent_support": 0,
            "disabled_support": 0,
            "life_insurance": 100000,
            "life_insurance_pension": 10000,
            "life_insurance_parents": 0,
            "health_insurance": 25000,
            "health_insurance_parents": 0,
            "social_security": 0,
            "pension_insurance": 0,
            "provident_fund": 150000,
            "gpf": 0,
            "pvd_teacher": 0,
            "rmf": 0,
            "thai_esg": 0,
            "thai_esgx_new": 0,
            "thai_esgx_ltf": 0,
            "stock_investment": 0,
            "easy_e_receipt": 0,
            "home_loan_interest": 0,
            "nsf": 0,
            "donation_general": 0,
            "donation_education": 0,
            "donation_social_enterprise": 0,
            "donation_political": 0,
            "risk_tolerance": "high"
        },
        "expected_tax_result": {
            "gross_income": 1500000,
            "taxable_income": 1155000,
            "tax_amount": 198750,
            "effective_tax_rate": 13.25,
            "marginal_tax_rate": 25
        },
        "expected_plans": {
            "plan_1": {
                "plan_id": "1",
                "plan_name": "ทางเลือกที่ 1 - เน้นประกัน",
                "plan_type": "high",
                "description": "แม้จะเป็นแผนเน้นประกัน แต่สำหรับรายได้สูงควรมีสัดส่วนกองทุนเพื่อการเติบโต",
                "total_investment": 500000,
                "total_tax_saving": 125000,
                "overall_risk": "high",
                "allocations": [
                    {
                        "category": "RMF กองทุนหุ้น",
                        "investment_amount": 250000,
                        "percentage": 50.0,
                        "tax_saving": 62500,
                        "risk_level": "high",
                        "pros": ["ลดหย่อนภาษีสูงสุด", "ผลตอบแทนสูง 8-15%", "เหมาะกับรายได้สูง"],
                        "cons": ["ความเสี่ยงสูง", "ต้องถือจนอายุ 55 ปี", "ผันผวนตามตลาด"]
                    },
                    {
                        "category": "ThaiESG/ThaiESGX",
                        "investment_amount": 100000,
                        "percentage": 20.0,
                        "tax_saving": 25000,
                        "risk_level": "high",
                        "pros": ["ยกเว้นภาษี 30%", "ลงทุน ESG", "ผลตอบแทน 7-12%"],
                        "cons": ["ถือ 8 ปี", "กองทุนใหม่", "ความเสี่ยงสูง"]
                    },
                    {
                        "category": "ประกันบำนาญ",
                        "investment_amount": 100000,
                        "percentage": 20.0,
                        "tax_saving": 25000,
                        "risk_level": "low",
                        "pros": ["รับประกันผลตอบแทน", "ลดหย่อนได้ 15%"],
                        "cons": ["ผูกพันยาว", "ผลตอบแทนต่ำ"]
                    },
                    {
                        "category": "ประกันชีวิต + สุขภาพ",
                        "investment_amount": 50000,
                        "percentage": 10.0,
                        "tax_saving": 12500,
                        "risk_level": "low",
                        "pros": ["จำเป็นต้องมี", "ลดหย่อนภาษี"],
                        "cons": ["ผลตอบแทนต่ำ"]
                    }
                ]
            },
            "plan_2": {
                "plan_id": "2",
                "plan_name": "ทางเลือกที่ 2 - สมดุล",
                "plan_type": "high",
                "description": "กระจายความเสี่ยง ผสม RMF, ThaiESG และ PVD",
                "total_investment": 800000,
                "total_tax_saving": 200000,
                "overall_risk": "high",
                "allocations": [
                    {
                        "category": "RMF กองทุนหุ้น",
                        "investment_amount": 400000,
                        "percentage": 50.0,
                        "tax_saving": 100000,
                        "risk_level": "high",
                        "pros": ["ลดหย่อนภาษีสูงสุด 30%", "ผลตอบแทนสูง"],
                        "cons": ["ความเสี่ยงสูง", "ถือจนอายุ 55 ปี"]
                    },
                    {
                        "category": "ThaiESG/ThaiESGX",
                        "investment_amount": 200000,
                        "percentage": 25.0,
                        "tax_saving": 50000,
                        "risk_level": "high",
                        "pros": ["ยกเว้นภาษี 30%", "ยืดหยุ่น"],
                        "cons": ["ถือ 8 ปี", "ความเสี่ยงสูง"]
                    },
                    {
                        "category": "กองทุนสำรองเลี้ยงชีพ (PVD)",
                        "investment_amount": 100000,
                        "percentage": 12.5,
                        "tax_saving": 25000,
                        "risk_level": "medium",
                        "pros": ["บริษัทจ่ายเพิ่มให้", "ลดหย่อนได้"],
                        "cons": ["ต้องเป็นพนักงาน", "ถอนยาก"]
                    },
                    {
                        "category": "ประกันบำนาญ + ชีวิต",
                        "investment_amount": 100000,
                        "percentage": 12.5,
                        "tax_saving": 25000,
                        "risk_level": "low",
                        "pros": ["ความปลอดภัย", "ลดหย่อนภาษี"],
                        "cons": ["ผลตอบแทนต่ำ"]
                    }
                ]
            },
            "plan_3": {
                "plan_id": "3",
                "plan_name": "ทางเลือกที่ 3 - ลงทุนสูงสุด",
                "plan_type": "high",
                "description": "ใช้วงเงินเต็มที่ เน้นกองทุนหุ้นและ ESG เพื่อผลตอบแทนสูงสุด",
                "total_investment": 1200000,
                "total_tax_saving": 300000,
                "overall_risk": "high",
                "allocations": [
                    {
                        "category": "RMF กองทุนหุ้น (ใช้วงเงินเต็มที่)",
                        "investment_amount": 450000,
                        "percentage": 37.5,
                        "tax_saving": 112500,
                        "risk_level": "high",
                        "pros": ["ลดหย่อนภาษีสูงสุด", "ผลตอบแทนสูง 10-15%"],
                        "cons": ["ความเสี่ยงสูง", "ต้องถือจนอายุ 55 ปี"]
                    },
                    {
                        "category": "ThaiESG/ThaiESGX",
                        "investment_amount": 300000,
                        "percentage": 25.0,
                        "tax_saving": 75000,
                        "risk_level": "high",
                        "pros": ["ยกเว้นภาษี 30%", "ลงทุน ESG"],
                        "cons": ["ถือ 8 ปี", "กองทุนใหม่"]
                    },
                    {
                        "category": "กองทุนสำรองเลี้ยงชีพ (PVD)",
                        "investment_amount": 200000,
                        "percentage": 16.67,
                        "tax_saving": 50000,
                        "risk_level": "medium",
                        "pros": ["บริษัทจ่ายเพิ่ม", "ลดหย่อนได้"],
                        "cons": ["ถอนยาก"]
                    },
                    {
                        "category": "ประกันบำนาญ",
                        "investment_amount": 150000,
                        "percentage": 12.5,
                        "tax_saving": 37500,
                        "risk_level": "low",
                        "pros": ["รับประกันผลตอบแทน"],
                        "cons": ["ผูกพันยาว"]
                    },
                    {
                        "category": "เงินบริจาคการศึกษา",
                        "investment_amount": 50000,
                        "percentage": 4.17,
                        "tax_saving": 12500,
                        "risk_level": "low",
                        "pros": ["นับ 2 เท่า", "ช่วยสังคม"],
                        "cons": ["ไม่มีผลตอบแทน"]
                    },
                    {
                        "category": "Easy e-Receipt",
                        "investment_amount": 50000,
                        "percentage": 4.17,
                        "tax_saving": 12500,
                        "risk_level": "low",
                        "pros": ["ใช้จ่ายปกติ", "ลดหย่อนได้"],
                        "cons": ["ต้องใช้ e-payment"]
                    }
                ]
            }
        }
    }
    
    # ===================================
    # Test Case 3: รายได้ 360,000 - ความเสี่ยงต่ำ
    # ===================================
    TEST_CASE_3 = {
        "name": "รายได้ 360K - ความเสี่ยงต่ำ",
        "description": "กรณีทดสอบสำหรับผู้มีรายได้น้อย ต้องการความปลอดภัยสูง",
        "input": {
            "gross_income": 360000,
            "personal_deduction": 60000,
            "spouse_deduction": 0,
            "child_deduction": 0,
            "parent_support": 0,
            "disabled_support": 0,
            "life_insurance": 20000,
            "life_insurance_pension": 0,
            "life_insurance_parents": 0,
            "health_insurance": 10000,
            "health_insurance_parents": 0,
            "social_security": 9000,
            "pension_insurance": 0,
            "provident_fund": 30000,
            "gpf": 0,
            "pvd_teacher": 0,
            "rmf": 0,
            "thai_esg": 0,
            "thai_esgx_new": 0,
            "thai_esgx_ltf": 0,
            "stock_investment": 0,
            "easy_e_receipt": 0,
            "home_loan_interest": 0,
            "nsf": 0,
            "donation_general": 0,
            "donation_education": 0,
            "donation_social_enterprise": 0,
            "donation_political": 0,
            "risk_tolerance": "low"
        },
        "expected_tax_result": {
            "gross_income": 360000,
            "taxable_income": 231000,
            "tax_amount": 4050,
            "effective_tax_rate": 1.13,
            "marginal_tax_rate": 5
        },
        "expected_plans": {
            "plan_1": {
                "plan_id": "1",
                "plan_name": "ทางเลือกที่ 1 - เน้นประกัน",
                "plan_type": "low",
                "description": "เน้นความปลอดภัยสูงสุด เหมาะสำหรับผู้มีรายได้จำกัด",
                "total_investment": 60000,
                "total_tax_saving": 3000,
                "overall_risk": "low",
                "allocations": [
                    {
                        "category": "ประกันชีวิต",
                        "investment_amount": 30000,
                        "percentage": 50.0,
                        "tax_saving": 1500,
                        "risk_level": "low",
                        "pros": ["ความคุ้มครองชีวิต", "จำเป็นต้องมี"],
                        "cons": ["ผลตอบแทนต่ำ"]
                    },
                    {
                        "category": "ประกันสุขภาพ",
                        "investment_amount": 15000,
                        "percentage": 25.0,
                        "tax_saving": 750,
                        "risk_level": "low",
                        "pros": ["คุ้มครองสุขภาพ", "จำเป็น"],
                        "cons": ["ไม่มีผลตอบแทน"]
                    },
                    {
                        "category": "ประกันบำนาญ",
                        "investment_amount": 15000,
                        "percentage": 25.0,
                        "tax_saving": 750,
                        "risk_level": "low",
                        "pros": ["รับประกันผลตอบแทน"],
                        "cons": ["ผูกพันยาว"]
                    }
                ]
            },
            "plan_2": {
                "plan_id": "2",
                "plan_name": "ทางเลือกที่ 2 - สมดุล",
                "plan_type": "low",
                "description": "เพิ่มการออมผ่าน RMF ตราสารหนี้",
                "total_investment": 100000,
                "total_tax_saving": 5000,
                "overall_risk": "low",
                "allocations": [
                    {
                        "category": "RMF ตราสารหนี้",
                        "investment_amount": 50000,
                        "percentage": 50.0,
                        "tax_saving": 2500,
                        "risk_level": "low",
                        "pros": ["ลดหย่อนภาษี", "ความเสี่ยงต่ำ"],
                        "cons": ["ถือจนอายุ 55 ปี"]
                    },
                    {
                        "category": "ประกันชีวิต",
                        "investment_amount": 30000,
                        "percentage": 30.0,
                        "tax_saving": 1500,
                        "risk_level": "low",
                        "pros": ["ความคุ้มครอง"],
                        "cons": ["ผลตอบแทนต่ำ"]
                    },
                    {
                        "category": "ประกันสุขภาพ",
                        "investment_amount": 15000,
                        "percentage": 15.0,
                        "tax_saving": 750,
                        "risk_level": "low",
                        "pros": ["จำเป็น"],
                        "cons": ["ไม่มีผลตอบแทน"]
                    },
                    {
                        "category": "Easy e-Receipt",
                        "investment_amount": 5000,
                        "percentage": 5.0,
                        "tax_saving": 250,
                        "risk_level": "low",
                        "pros": ["ใช้จ่ายปกติ"],
                        "cons": ["ต้องใช้ e-payment"]
                    }
                ]
            },
            "plan_3": {
                "plan_id": "3",
                "plan_name": "ทางเลือกที่ 3 - ลงทุนสูงสุด",
                "plan_type": "low",
                "description": "ใช้วงเงินให้เต็มที่ภายในความสามารถ",
                "total_investment": 150000,
                "total_tax_saving": 7500,
                "overall_risk": "low",
                "allocations": [
                    {
                        "category": "RMF ตราสารหนี้",
                        "investment_amount": 80000,
                        "percentage": 53.33,
                        "tax_saving": 4000,
                        "risk_level": "low",
                        "pros": ["ลดหย่อนภาษี 30%", "ผลตอบแทนดีกว่าเงินฝาก"],
                        "cons": ["ถือจนอายุ 55 ปี"]
                    },
                    {
                        "category": "ประกันบำนาญ",
                        "investment_amount": 30000,
                        "percentage": 20.0,
                        "tax_saving": 1500,
                        "risk_level": "low",
                        "pros": ["รับประกันผลตอบแทน"],
                        "cons": ["ผูกพันยาว"]
                    },
                    {
                        "category": "ประกันชีวิต",
                        "investment_amount": 30000,
                        "percentage": 20.0,
                        "tax_saving": 1500,
                        "risk_level": "low",
                        "pros": ["ความคุ้มครอง"],
                        "cons": ["ผลตอบแทนต่ำ"]
                    },
                    {
                        "category": "Easy e-Receipt",
                        "investment_amount": 10000,
                        "percentage": 6.67,
                        "tax_saving": 500,
                        "risk_level": "low",
                        "pros": ["ใช้จ่ายปกติ"],
                        "cons": ["ต้องใช้ e-payment"]
                    }
                ]
            }
        }
    }
    
    @classmethod
    def get_all_test_cases(cls) -> List[Dict[str, Any]]:
        """
        ดึง test cases ทั้งหมด
        
        Returns:
            List of test cases with ground truth
        """
        return [
            cls.TEST_CASE_1,
            cls.TEST_CASE_2,
            cls.TEST_CASE_3
        ]
    
    @classmethod
    def get_test_case_by_id(cls, case_id: int) -> Dict[str, Any]:
        """
        ดึง test case ตาม ID
        
        Args:
            case_id: 1, 2, หรือ 3
            
        Returns:
            Test case dict with ground truth
        """
        cases = {
            1: cls.TEST_CASE_1,
            2: cls.TEST_CASE_2,
            3: cls.TEST_CASE_3
        }
        return cases.get(case_id, cls.TEST_CASE_1)
    
    @classmethod
    def get_test_case_by_name(cls, name: str) -> Dict[str, Any]:
        """
        ดึง test case ตามชื่อ
        
        Args:
            name: ชื่อ test case
            
        Returns:
            Test case dict
        """
        all_cases = cls.get_all_test_cases()
        for case in all_cases:
            if case["name"] == name:
                return case
        return cls.TEST_CASE_1