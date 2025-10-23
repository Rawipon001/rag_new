"""
Test Data สำหรับ Evaluation
มี ground truth สำหรับเทียบกับคำตอบของ AI
"""

from typing import List, Dict, Any


class EvaluationTestData:
    """
    ข้อมูลสำหรับ test evaluation
    """
    
    # Test Case 1: รายได้ปานกลาง
    TEST_CASE_1 = {
        "input": {
            "gross_income": 600000,
            "personal_deduction": 60000,
            "life_insurance": 50000,
            "health_insurance": 15000,
            "provident_fund": 50000,
            "rmf": 0,
            "ssf": 0,
            "pension_insurance": 0,
            "donation": 0,
            "risk_tolerance": "medium"
        },
        "expected_recommendations": [
            {
                "strategy": "ลงทุน RMF 150,000 บาท (กองทุนผสม)",
                "description": "ลงทุนในกองทุน RMF ประเภทผสมระหว่างหุ้นและตราสารหนี้ เพื่อลดหย่อนภาษีได้สูงสุด 25% ของรายได้ ต้องถือจนอายุ 55 ปี หรือถือครบ 5 ปีภาษี",
                "investment_amount": 150000,
                "tax_saving": 15000,  # 150,000 × 10% (อัตราภาษีส่วนเพิ่ม)
                "risk_level": "medium",
                "expected_return_1y": 5.5,
                "expected_return_3y": 6.8,
                "expected_return_5y": 8.0,
                "pros": ["ลดหย่อนภาษีได้สูง", "ผลตอบแทนดี", "บังคับออม"],
                "cons": ["ต้องถือจนอายุ 55 ปี", "มีความเสี่ยงตามตลาด"]
            },
            {
                "strategy": "เปิดประกันบำนาญ 90,000 บาท",
                "description": "ซื้อประกันบำนาญเพื่อรับผลตอบแทนที่รับประกันและลดภาษี สูงสุด 15% ของรายได้",
                "investment_amount": 90000,
                "tax_saving": 9000,
                "risk_level": "low",
                "expected_return_1y": 3.0,
                "expected_return_3y": 3.5,
                "expected_return_5y": 4.0,
                "pros": ["รับประกันผลตอบแทน", "ความเสี่ยงต่ำ"],
                "cons": ["ผลตอบแทนต่ำกว่ากองทุน", "ผูกพันระยะยาว"]
            },
            {
                "strategy": "เพิ่มประกันชีวิตอีก 50,000 บาท",
                "description": "ซื้อประกันชีวิตแบบสะสมทรัพย์เพิ่มเติม เพื่อเติมเต็มวงเงินลดหย่อน 100,000 บาท",
                "investment_amount": 50000,
                "tax_saving": 5000,
                "risk_level": "low",
                "expected_return_1y": 2.0,
                "expected_return_3y": 2.5,
                "expected_return_5y": 3.0,
                "pros": ["มีความคุ้มครอง", "ลดภาษีได้"],
                "cons": ["ผลตอบแทนต่ำ", "ค่าธรรมเนียมสูง"]
            }
        ]
    }
    
    # Test Case 2: รายได้สูง
    TEST_CASE_2 = {
        "input": {
            "gross_income": 1500000,
            "personal_deduction": 60000,
            "life_insurance": 100000,
            "health_insurance": 25000,
            "provident_fund": 150000,
            "rmf": 0,
            "ssf": 0,
            "pension_insurance": 0,
            "donation": 0,
            "risk_tolerance": "high"
        },
        "expected_recommendations": [
            {
                "strategy": "ลงทุน RMF เต็มวงเงิน 450,000 บาท (กองทุนหุ้น)",
                "description": "ลงทุนในกองทุน RMF ประเภทหุ้น เพื่อลดหย่อนภาษีได้สูงสุด 30% ของรายได้ และได้ผลตอบแทนสูง เหมาะกับคนที่รับความเสี่ยงได้",
                "investment_amount": 450000,
                "tax_saving": 112500,  # 450,000 × 25%
                "risk_level": "high",
                "expected_return_1y": 10.0,
                "expected_return_3y": 12.0,
                "expected_return_5y": 15.0,
                "pros": ["ลดหย่อนภาษีได้สูงสุด", "ผลตอบแทนสูง"],
                "cons": ["ความเสี่ยงสูง", "ต้องถือจนอายุ 55 ปี"]
            },
            {
                "strategy": "ลงทุน SSF 200,000 บาท",
                "description": "ลงทุนในกองทุน SSF เพิ่มเติม ถือครบ 10 ปี",
                "investment_amount": 200000,
                "tax_saving": 50000,
                "risk_level": "medium",
                "expected_return_1y": 6.0,
                "expected_return_3y": 7.0,
                "expected_return_5y": 8.5,
                "pros": ["ยืดหยุ่นกว่า RMF", "ผลตอบแทนดี"],
                "cons": ["ถือครบ 10 ปี", "วงเงินจำกัด"]
            },
            {
                "strategy": "เปิดประกันบำนาญ 200,000 บาท",
                "description": "ซื้อประกันบำนาญเพื่อสร้างความมั่นคงหลังเกษียณ",
                "investment_amount": 200000,
                "tax_saving": 50000,
                "risk_level": "low",
                "expected_return_1y": 3.0,
                "expected_return_3y": 3.5,
                "expected_return_5y": 4.0,
                "pros": ["รับประกันผลตอบแทน", "มีรายได้หลังเกษียณ"],
                "cons": ["ผลตอบแทนต่ำ", "ผูกพันระยะยาว"]
            }
        ]
    }
    
    # Test Case 3: รายได้ต่ำ ความเสี่ยงต่ำ
    TEST_CASE_3 = {
        "input": {
            "gross_income": 360000,
            "personal_deduction": 60000,
            "life_insurance": 20000,
            "health_insurance": 10000,
            "provident_fund": 30000,
            "rmf": 0,
            "ssf": 0,
            "pension_insurance": 0,
            "donation": 0,
            "risk_tolerance": "low"
        },
        "expected_recommendations": [
            {
                "strategy": "เปิดประกันบำนาญ 54,000 บาท",
                "description": "ซื้อประกันบำนาญ 15% ของรายได้ เพื่อลดภาษีและสร้างความมั่นคง",
                "investment_amount": 54000,
                "tax_saving": 2700,  # 54,000 × 5%
                "risk_level": "low",
                "expected_return_1y": 3.0,
                "expected_return_3y": 3.5,
                "expected_return_5y": 4.0,
                "pros": ["ความเสี่ยงต่ำ", "รับประกันผลตอบแทน"],
                "cons": ["ผลตอบแทนต่ำ", "ผูกพันระยะยาว"]
            },
            {
                "strategy": "ลงทุน RMF ตราสารหนี้ 50,000 บาท",
                "description": "ลงทุนในกองทุน RMF ประเภทตราสารหนี้ ความเสี่ยงต่ำ",
                "investment_amount": 50000,
                "tax_saving": 2500,
                "risk_level": "low",
                "expected_return_1y": 3.5,
                "expected_return_3y": 4.0,
                "expected_return_5y": 5.0,
                "pros": ["ความเสี่ยงต่ำ", "ลดภาษีได้"],
                "cons": ["ต้องถือจนอายุ 55 ปี"]
            },
            {
                "strategy": "เพิ่มประกันชีวิต 30,000 บาท",
                "description": "ซื้อประกันชีวิตเพิ่มเติม",
                "investment_amount": 30000,
                "tax_saving": 1500,
                "risk_level": "low",
                "expected_return_1y": 2.0,
                "expected_return_3y": 2.5,
                "expected_return_5y": 3.0,
                "pros": ["มีความคุ้มครอง", "ลดภาษีได้"],
                "cons": ["ผลตอบแทนต่ำมาก"]
            }
        ]
    }
    
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
            cls.TEST_CASE_3
        ]
    
    @classmethod
    def get_test_case_by_id(cls, case_id: int) -> Dict[str, Any]:
        """
        ดึง test case ตาม ID
        
        Args:
            case_id: 1, 2, หรือ 3
            
        Returns:
            Test case dict
        """
        cases = {
            1: cls.TEST_CASE_1,
            2: cls.TEST_CASE_2,
            3: cls.TEST_CASE_3
        }
        return cases.get(case_id, cls.TEST_CASE_1)