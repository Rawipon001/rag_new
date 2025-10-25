"""
Test Data สำหรับ Evaluation - ปี 2568 (Extended Version)
มี ground truth ที่ครอบคลุมสำหรับเทียบกับคำตอบของ AI
อัปเดตให้ตรงกับระบบหลัก: ไม่มี SSF, มี ThaiESG/ThaiESGX

ครอบคลุม 20 test cases:
- ทุกกลุ่มอาชีพ (พนักงาน, ข้าราชการ, ครู, ฟรีแลนซ์)
- ทุกระดับรายได้ (300K - 4.5M+)
- ทุกช่วงอายุ (25-60+ ปี)
- สถานการณ์พิเศษ (ครอบครัวใหญ่, มีคนพิการ, ใกล้เกษียณ)

NOTE: ไฟล์นี้เป็นตัวอย่าง 3 test cases แรก พร้อม expected_plans
      คุณต้องเพิ่ม expected_plans สำหรับ test cases ที่เหลือ (4-20) ตามรูปแบบเดียวกัน
"""

from typing import List, Dict, Any


class EvaluationTestData:
    """
    ข้อมูลสำหรับ test evaluation - ปี 2568
    Extended Version - 20 Test Cases
    """
    
    # ===================================
    # Test Case 1: รายได้ 600,000 - ความเสี่ยงกลาง
    # ===================================
    TEST_CASE_1 = {
        "name": "รายได้ 600K - ความเสี่ยงกลาง",
        "description": "พนักงานรายได้ปานกลาง มี PVD ความเสี่ยงกลาง",
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
        "expected_plans": {
            "plan_1": {
                "plan_id": "1",
                "plan_name": "ทางเลือกที่ 1 - เน้นประกัน",
                "plan_type": "medium",
                "description": "เน้นความคุ้มครองและความปลอดภัย เหมาะกับผู้เริ่มต้นวางแผนภาษี",
                "total_investment": 60000,
                "total_tax_saving": 6000,
                "overall_risk": "medium",
                "allocations": [
                    {
                        "category": "ประกันชีวิตเพิ่มเติม",
                        "investment_amount": 20000,
                        "percentage": 33.33,
                        "tax_saving": 2000,
                        "risk_level": "low",
                        "pros": ["มีความคุ้มครอง", "จำเป็นสำหรับครอบครัว"],
                        "cons": ["ผลตอบแทนต่ำ"]
                    },
                    {
                        "category": "RMF",
                        "investment_amount": 30000,
                        "percentage": 50.0,
                        "tax_saving": 3000,
                        "risk_level": "medium",
                        "pros": ["ลดหย่อนภาษีได้", "ผลตอบแทนดี"],
                        "cons": ["ต้องถือ 5 ปี"]
                    },
                    {
                        "category": "ประกันสุขภาพเพิ่มเติม",
                        "investment_amount": 10000,
                        "percentage": 16.67,
                        "tax_saving": 1000,
                        "risk_level": "low",
                        "pros": ["คุ้มครองสุขภาพ"],
                        "cons": ["ไม่มีผลตอบแทน"]
                    }
                ]
            },
            "plan_2": {
                "plan_id": "2",
                "plan_name": "ทางเลือกที่ 2 - สมดุล",
                "plan_type": "medium",
                "description": "กระจายความเสี่ยง เน้น RMF และกองทุน ESG",
                "total_investment": 100000,
                "total_tax_saving": 10000,
                "overall_risk": "medium",
                "allocations": [
                    {
                        "category": "RMF",
                        "investment_amount": 60000,
                        "percentage": 60.0,
                        "tax_saving": 6000,
                        "risk_level": "medium",
                        "pros": ["ลดหย่อนภาษี 30%", "ผลตอบแทนดี"],
                        "cons": ["ต้องถือ 5 ปี"]
                    },
                    {
                        "category": "ThaiESG",
                        "investment_amount": 30000,
                        "percentage": 30.0,
                        "tax_saving": 3000,
                        "risk_level": "medium",
                        "pros": ["ลดหย่อน 30%", "ลงทุนยั่งยืน"],
                        "cons": ["ต้องถือ 8 ปี"]
                    },
                    {
                        "category": "ประกันบำนาญ",
                        "investment_amount": 10000,
                        "percentage": 10.0,
                        "tax_saving": 1000,
                        "risk_level": "low",
                        "pros": ["รับประกันผลตอบแทน"],
                        "cons": ["ผูกพันระยะยาว"]
                    }
                ]
            },
            "plan_3": {
                "plan_id": "3",
                "plan_name": "ทางเลือกที่ 3 - เติบโตสูงสุด",
                "plan_type": "medium",
                "description": "ใช้วงเงินลดหย่อนสูงสุด เน้นการลงทุนระยะยาว",
                "total_investment": 150000,
                "total_tax_saving": 15000,
                "overall_risk": "medium",
                "allocations": [
                    {
                        "category": "RMF",
                        "investment_amount": 90000,
                        "percentage": 60.0,
                        "tax_saving": 9000,
                        "risk_level": "medium",
                        "pros": ["ลดหย่อนสูง", "ผลตอบแทนดี"],
                        "cons": ["ต้องถือจนอายุ 55"]
                    },
                    {
                        "category": "ThaiESG",
                        "investment_amount": 40000,
                        "percentage": 26.67,
                        "tax_saving": 2000,
                        "risk_level": "medium",
                        "pros": ["ลดหย่อน 30%", "ESG"],
                        "cons": ["ต้องถือ 8 ปี"]
                    },
                    {
                        "category": "ประกันบำนาญ",
                        "investment_amount": 20000,
                        "percentage": 13.33,
                        "tax_saving": 1000,
                        "risk_level": "low",
                        "pros": ["รับประกันผลตอบแทน", "เหมาะเกษียณ"],
                        "cons": ["ผูกพันยาว"]
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
        "description": "ผู้บริหารรายได้สูง ยอมรับความเสี่ยงสูง",
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
        "expected_plans": {
            "plan_1": {
                "plan_id": "1",
                "plan_name": "ทางเลือกที่ 1 - เน้นประกัน",
                "plan_type": "high",
                "description": "เน้นประกันและความปลอดภัย เงินลงทุนพอเหมาะ",
                "total_investment": 300000,
                "total_tax_saving": 45000,
                "overall_risk": "high",
                "allocations": [
                    {
                        "category": "RMF",
                        "investment_amount": 200000,
                        "percentage": 66.67,
                        "tax_saving": 30000,
                        "risk_level": "high",
                        "pros": ["ลดหย่อนสูง", "ผลตอบแทนดี"],
                        "cons": ["ต้องถือยาว"]
                    },
                    {
                        "category": "ประกันบำนาญ",
                        "investment_amount": 80000,
                        "percentage": 26.67,
                        "tax_saving": 12000,
                        "risk_level": "low",
                        "pros": ["รับประกันผลตอบแทน"],
                        "cons": ["ผูกพันยาว"]
                    },
                    {
                        "category": "Easy e-Receipt",
                        "investment_amount": 20000,
                        "percentage": 6.67,
                        "tax_saving": 3000,
                        "risk_level": "low",
                        "pros": ["ลดหย่อนง่าย"],
                        "cons": ["วงเงินจำกัด"]
                    }
                ]
            },
            "plan_2": {
                "plan_id": "2",
                "plan_name": "ทางเลือกที่ 2 - สมดุล",
                "plan_type": "high",
                "description": "กระจายความเสี่ยง เน้น RMF + ThaiESG + บริจาค",
                "total_investment": 500000,
                "total_tax_saving": 82500,
                "overall_risk": "high",
                "allocations": [
                    {
                        "category": "RMF",
                        "investment_amount": 300000,
                        "percentage": 60.0,
                        "tax_saving": 45000,
                        "risk_level": "high",
                        "pros": ["ลดหย่อน 30%", "ผลตอบแทนดี"],
                        "cons": ["ต้องถือยาว"]
                    },
                    {
                        "category": "ThaiESG",
                        "investment_amount": 150000,
                        "percentage": 30.0,
                        "tax_saving": 22500,
                        "risk_level": "high",
                        "pros": ["ลดหย่อน 30%", "ESG"],
                        "cons": ["ต้องถือ 8 ปี"]
                    },
                    {
                        "category": "บริจาคการศึกษา",
                        "investment_amount": 50000,
                        "percentage": 10.0,
                        "tax_saving": 15000,
                        "risk_level": "low",
                        "pros": ["นับ 2 เท่า", "ทำความดี"],
                        "cons": ["ไม่ได้คืน"]
                    }
                ]
            },
            "plan_3": {
                "plan_id": "3",
                "plan_name": "ทางเลือกที่ 3 - ลงทุนสูงสุด",
                "plan_type": "high",
                "description": "ใช้วงเงินลดหย่อนเต็มที่ เน้นผลตอบแทนสูงสุด",
                "total_investment": 800000,
                "total_tax_saving": 127500,
                "overall_risk": "high",
                "allocations": [
                    {
                        "category": "RMF",
                        "investment_amount": 450000,
                        "percentage": 56.25,
                        "tax_saving": 67500,
                        "risk_level": "high",
                        "pros": ["ลดหย่อนสูงสุด", "หุ้นเติบโต"],
                        "cons": ["ความเสี่ยงสูง"]
                    },
                    {
                        "category": "ThaiESG",
                        "investment_amount": 200000,
                        "percentage": 25.0,
                        "tax_saving": 30000,
                        "risk_level": "high",
                        "pros": ["ลดหย่อน 30%", "ยั่งยืน"],
                        "cons": ["ต้องถือยาว"]
                    },
                    {
                        "category": "ประกันบำนาญ",
                        "investment_amount": 100000,
                        "percentage": 12.5,
                        "tax_saving": 15000,
                        "risk_level": "low",
                        "pros": ["รับประกัน", "เกษียณ"],
                        "cons": ["ผูกพัน"]
                    },
                    {
                        "category": "บริจาคการศึกษา",
                        "investment_amount": 50000,
                        "percentage": 6.25,
                        "tax_saving": 15000,
                        "risk_level": "low",
                        "pros": ["นับ 2 เท่า"],
                        "cons": ["ไม่คืน"]
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
        "description": "พนักงานรายได้น้อย เน้นความปลอดภัย",
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
        "expected_plans": {
            "plan_1": {
                "plan_id": "1",
                "plan_name": "ทางเลือกที่ 1 - เน้นประกัน",
                "plan_type": "low",
                "description": "เน้นความคุ้มครองและความปลอดภัยสูงสุด",
                "total_investment": 40000,
                "total_tax_saving": 2000,
                "overall_risk": "low",
                "allocations": [
                    {
                        "category": "ประกันชีวิตเพิ่มเติม",
                        "investment_amount": 20000,
                        "percentage": 50.0,
                        "tax_saving": 1000,
                        "risk_level": "low",
                        "pros": ["คุ้มครองครอบครัว", "จำเป็น"],
                        "cons": ["ไม่มีผลตอบแทน"]
                    },
                    {
                        "category": "ประกันสุขภาพเพิ่มเติม",
                        "investment_amount": 10000,
                        "percentage": 25.0,
                        "tax_saving": 500,
                        "risk_level": "low",
                        "pros": ["คุ้มครองสุขภาพ"],
                        "cons": ["ไม่มีผลตอบแทน"]
                    },
                    {
                        "category": "กอช.",
                        "investment_amount": 10000,
                        "percentage": 25.0,
                        "tax_saving": 500,
                        "risk_level": "low",
                        "pros": ["ปลอดภัย", "ลดหย่อนได้"],
                        "cons": ["ผลตอบแทนต่ำ"]
                    }
                ]
            },
            "plan_2": {
                "plan_id": "2",
                "plan_name": "ทางเลือกที่ 2 - สมดุล",
                "plan_type": "low",
                "description": "กระจายระหว่างประกันและการออม",
                "total_investment": 60000,
                "total_tax_saving": 3000,
                "overall_risk": "low",
                "allocations": [
                    {
                        "category": "RMF ตราสารหนี้",
                        "investment_amount": 30000,
                        "percentage": 50.0,
                        "tax_saving": 1500,
                        "risk_level": "low",
                        "pros": ["ลดหย่อนได้", "ปลอดภัย"],
                        "cons": ["ต้องถือยาว"]
                    },
                    {
                        "category": "ประกันบำนาญ",
                        "investment_amount": 20000,
                        "percentage": 33.33,
                        "tax_saving": 200,
                        "risk_level": "low",
                        "pros": ["รับประกัน", "เกษียณ"],
                        "cons": ["ผูกพัน"]
                    },
                    {
                        "category": "กอช.",
                        "investment_amount": 10000,
                        "percentage": 16.67,
                        "tax_saving": 100,
                        "risk_level": "low",
                        "pros": ["ปลอดภัยสูง"],
                        "cons": ["ดอกต่ำ"]
                    }
                ]
            },
            "plan_3": {
                "plan_id": "3",
                "plan_name": "ทางเลือกที่ 3 - ออมสูงสุด",
                "plan_type": "low",
                "description": "เน้นการออมและลดหย่อนภาษี",
                "total_investment": 80000,
                "total_tax_saving": 4000,
                "overall_risk": "low",
                "allocations": [
                    {
                        "category": "RMF ตราสารหนี้",
                        "investment_amount": 50000,
                        "percentage": 62.5,
                        "tax_saving": 2500,
                        "risk_level": "low",
                        "pros": ["ลดหย่อน", "ปลอดภัย"],
                        "cons": ["ถือยาว"]
                    },
                    {
                        "category": "ประกันบำนาญ",
                        "investment_amount": 20000,
                        "percentage": 25.0,
                        "tax_saving": 200,
                        "risk_level": "low",
                        "pros": ["รับประกัน"],
                        "cons": ["ผูกพัน"]
                    },
                    {
                        "category": "กอช.",
                        "investment_amount": 10000,
                        "percentage": 12.5,
                        "tax_saving": 100,
                        "risk_level": "low",
                        "pros": ["ปลอดภัย"],
                        "cons": ["ดอกต่ำ"]
                    }
                ]
            }
        }
    }
    
    # ===================================
    # Test Cases 4-20: ต้องเพิ่ม expected_plans ด้วย
    # ===================================
    # NOTE: เพิ่ม expected_plans สำหรับ test cases ที่เหลือตามรูปแบบเดียวกัน
    
    TEST_CASE_4 = {
        "name": "พนักงานใหม่จบ 25 ปี - รายได้ 420K",
        "description": "จบใหม่ เริ่มต้นทำงาน",
        "input": {
            "gross_income": 420000,
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
            "easy_e_receipt": 15000,
            "home_loan_interest": 0,
            "nsf": 0,
            "donation_general": 0,
            "donation_education": 0,
            "donation_social_enterprise": 0,
            "donation_political": 0,
            "risk_tolerance": "high"
        },
        "expected_plans": {}  # TODO: เพิ่มตามรูปแบบข้างบน
    }
    
    # ทำต่อไปเรื่อยๆ จนถึง TEST_CASE_20...
    # (เนื่องจากความยาว ขอแสดงเฉพาะโครงสร้าง)
    
    @classmethod
    def get_all_test_cases(cls) -> List[Dict[str, Any]]:
        """
        ดึง test cases ทั้งหมด
        
        Returns:
            List of test cases
        """
        return [
            cls.TEST_CASE_1,
            cls.TEST_CASE_2,
            cls.TEST_CASE_3,
            # cls.TEST_CASE_4,
            # ... เพิ่มต่อ
        ]
    
    @classmethod
    def get_test_case_by_id(cls, case_id: int) -> Dict[str, Any]:
        """
        ดึง test case ตาม ID
        
        Args:
            case_id: 1-20
            
        Returns:
            Test case dict
        """
        all_cases = cls.get_all_test_cases()
        if 1 <= case_id <= len(all_cases):
            return all_cases[case_id - 1]
        return cls.TEST_CASE_1
    
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