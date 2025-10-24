"""
Test Data สำหรับ Evaluation - ปี 2568 (Extended Version)
มี ground truth ที่ครอบคลุมสำหรับเทียบกับคำตอบของ AI
อัปเดตให้ตรงกับระบบหลัก: ไม่มี SSF, มี ThaiESG/ThaiESGX

ครอบคลุม 20 test cases:
- ทุกกลุ่มอาชีพ (พนักงาน, ข้าราชการ, ครู, ฟรีแลนซ์)
- ทุกระดับรายได้ (300K - 4.5M+)
- ทุกช่วงอายุ (25-60+ ปี)
- สถานการณ์พิเศษ (ครอบครัวใหญ่, มีคนพิการ, ใกล้เกษียณ)
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
        }
    }
    
    # ===================================
    # Test Case 2: รายได้ 1,500,000 - ความเสี่ยงสูง
    # ===================================
    TEST_CASE_2 = {
        "name": "รายได้ 1.5M - ความเสี่ยงสูง",
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
        }
    }
    
    # ===================================
    # Test Case 3: รายได้ 360,000 - ความเสี่ยงต่ำ
    # ===================================
    TEST_CASE_3 = {
        "name": "รายได้ 360K - ความเสี่ยงต่ำ",
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
        }
    }
    
    # ===================================
    # Test Case 4: พนักงานใหม่จบ 25 ปี
    # ===================================
    TEST_CASE_4 = {
        "name": "พนักงานใหม่จบ 25 ปี - รายได้ 420K",
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
        }
    }
    
    # ===================================
    # Test Case 5: ข้าราชการ 35 ปี
    # ===================================
    TEST_CASE_5 = {
        "name": "ข้าราชการ 35 ปี - รายได้ 900K, มีลูก 2 คน",
        "input": {
            "gross_income": 900000,
            "personal_deduction": 60000,
            "spouse_deduction": 60000,
            "child_deduction": 60000,
            "parent_support": 120000,
            "disabled_support": 0,
            "life_insurance": 80000,
            "life_insurance_pension": 10000,
            "life_insurance_parents": 30000,
            "health_insurance": 25000,
            "health_insurance_parents": 30000,
            "social_security": 0,
            "pension_insurance": 80000,
            "provident_fund": 0,
            "gpf": 270000,
            "pvd_teacher": 0,
            "rmf": 0,
            "thai_esg": 0,
            "thai_esgx_new": 0,
            "thai_esgx_ltf": 0,
            "stock_investment": 0,
            "easy_e_receipt": 30000,
            "home_loan_interest": 80000,
            "nsf": 0,
            "donation_general": 20000,
            "donation_education": 10000,
            "donation_social_enterprise": 0,
            "donation_political": 0,
            "risk_tolerance": "medium"
        }
    }
    
    # ===================================
    # Test Case 6: ครู 40 ปี
    # ===================================
    TEST_CASE_6 = {
        "name": "ครู 40 ปี - รายได้ 720K, มีลูก 3 คน",
        "input": {
            "gross_income": 720000,
            "personal_deduction": 60000,
            "spouse_deduction": 60000,
            "child_deduction": 90000,
            "parent_support": 240000,
            "disabled_support": 0,
            "life_insurance": 70000,
            "life_insurance_pension": 10000,
            "life_insurance_parents": 60000,
            "health_insurance": 25000,
            "health_insurance_parents": 60000,
            "social_security": 0,
            "pension_insurance": 60000,
            "provident_fund": 0,
            "gpf": 0,
            "pvd_teacher": 108000,
            "rmf": 0,
            "thai_esg": 0,
            "thai_esgx_new": 0,
            "thai_esgx_ltf": 0,
            "stock_investment": 0,
            "easy_e_receipt": 25000,
            "home_loan_interest": 60000,
            "nsf": 20000,
            "donation_general": 15000,
            "donation_education": 20000,
            "donation_social_enterprise": 0,
            "donation_political": 0,
            "risk_tolerance": "low"
        }
    }
    
    # ===================================
    # Test Case 7: ฟรีแลนซ์/SME Owner
    # ===================================
    TEST_CASE_7 = {
        "name": "ฟรีแลนซ์/เจ้าของธุรกิจ - รายได้ 1.8M",
        "input": {
            "gross_income": 1800000,
            "personal_deduction": 60000,
            "spouse_deduction": 0,
            "child_deduction": 30000,
            "parent_support": 120000,
            "disabled_support": 0,
            "life_insurance": 100000,
            "life_insurance_pension": 10000,
            "life_insurance_parents": 30000,
            "health_insurance": 25000,
            "health_insurance_parents": 30000,
            "social_security": 0,
            "pension_insurance": 150000,
            "provident_fund": 0,
            "gpf": 0,
            "pvd_teacher": 0,
            "rmf": 0,
            "thai_esg": 0,
            "thai_esgx_new": 0,
            "thai_esgx_ltf": 0,
            "stock_investment": 100000,
            "easy_e_receipt": 50000,
            "home_loan_interest": 0,
            "nsf": 30000,
            "donation_general": 50000,
            "donation_education": 0,
            "donation_social_enterprise": 50000,
            "donation_political": 10000,
            "risk_tolerance": "high"
        }
    }
    
    # ===================================
    # Test Case 8: ผู้บริหารระดับสูง
    # ===================================
    TEST_CASE_8 = {
        "name": "ผู้บริหารระดับสูง - รายได้ 4.5M",
        "input": {
            "gross_income": 4500000,
            "personal_deduction": 60000,
            "spouse_deduction": 60000,
            "child_deduction": 60000,
            "parent_support": 240000,
            "disabled_support": 0,
            "life_insurance": 100000,
            "life_insurance_pension": 10000,
            "life_insurance_parents": 60000,
            "health_insurance": 25000,
            "health_insurance_parents": 60000,
            "social_security": 0,
            "pension_insurance": 200000,
            "provident_fund": 500000,
            "gpf": 0,
            "pvd_teacher": 0,
            "rmf": 0,
            "thai_esg": 0,
            "thai_esgx_new": 0,
            "thai_esgx_ltf": 0,
            "stock_investment": 100000,
            "easy_e_receipt": 50000,
            "home_loan_interest": 100000,
            "nsf": 30000,
            "donation_general": 200000,
            "donation_education": 300000,
            "donation_social_enterprise": 100000,
            "donation_political": 10000,
            "risk_tolerance": "high"
        }
    }
    
    # ===================================
    # Test Case 9: มีคนพิการในครอบครัว
    # ===================================
    TEST_CASE_9 = {
        "name": "พนักงาน 38 ปี - มีพี่พิการ + ดูแลบิดามารดา",
        "input": {
            "gross_income": 840000,
            "personal_deduction": 60000,
            "spouse_deduction": 0,
            "child_deduction": 30000,
            "parent_support": 120000,
            "disabled_support": 60000,
            "life_insurance": 60000,
            "life_insurance_pension": 10000,
            "life_insurance_parents": 30000,
            "health_insurance": 25000,
            "health_insurance_parents": 30000,
            "social_security": 9000,
            "pension_insurance": 80000,
            "provident_fund": 126000,
            "gpf": 0,
            "pvd_teacher": 0,
            "rmf": 0,
            "thai_esg": 0,
            "thai_esgx_new": 0,
            "thai_esgx_ltf": 0,
            "stock_investment": 0,
            "easy_e_receipt": 30000,
            "home_loan_interest": 50000,
            "nsf": 20000,
            "donation_general": 20000,
            "donation_education": 15000,
            "donation_social_enterprise": 0,
            "donation_political": 0,
            "risk_tolerance": "medium"
        }
    }
    
    # ===================================
    # Test Case 10: ใกล้เกษียณ 55 ปี
    # ===================================
    TEST_CASE_10 = {
        "name": "ใกล้เกษียณ 55 ปี - รายได้ 1.2M",
        "input": {
            "gross_income": 1200000,
            "personal_deduction": 60000,
            "spouse_deduction": 60000,
            "child_deduction": 0,
            "parent_support": 0,
            "disabled_support": 0,
            "life_insurance": 100000,
            "life_insurance_pension": 10000,
            "life_insurance_parents": 0,
            "health_insurance": 25000,
            "health_insurance_parents": 0,
            "social_security": 0,
            "pension_insurance": 180000,
            "provident_fund": 180000,
            "gpf": 0,
            "pvd_teacher": 0,
            "rmf": 0,
            "thai_esg": 0,
            "thai_esgx_new": 0,
            "thai_esgx_ltf": 0,
            "stock_investment": 0,
            "easy_e_receipt": 40000,
            "home_loan_interest": 0,
            "nsf": 30000,
            "donation_general": 30000,
            "donation_education": 50000,
            "donation_social_enterprise": 0,
            "donation_political": 0,
            "risk_tolerance": "low"
        }
    }
    
    # ===================================
    # Test Case 11: คู่รักใหม่แต่งงาน
    # ===================================
    TEST_CASE_11 = {
        "name": "คู่รักใหม่แต่งงาน 30 ปี - รวมรายได้ 1.4M",
        "input": {
            "gross_income": 1400000,
            "personal_deduction": 60000,
            "spouse_deduction": 0,
            "child_deduction": 0,
            "parent_support": 120000,
            "disabled_support": 0,
            "life_insurance": 80000,
            "life_insurance_pension": 10000,
            "life_insurance_parents": 30000,
            "health_insurance": 25000,
            "health_insurance_parents": 30000,
            "social_security": 9000,
            "pension_insurance": 100000,
            "provident_fund": 210000,
            "gpf": 0,
            "pvd_teacher": 0,
            "rmf": 0,
            "thai_esg": 0,
            "thai_esgx_new": 0,
            "thai_esgx_ltf": 0,
            "stock_investment": 0,
            "easy_e_receipt": 50000,
            "home_loan_interest": 100000,
            "nsf": 0,
            "donation_general": 20000,
            "donation_education": 0,
            "donation_social_enterprise": 0,
            "donation_political": 0,
            "risk_tolerance": "medium"
        }
    }
    
    # ===================================
    # Test Case 12: หมอ/วิศวกร
    # ===================================
    TEST_CASE_12 = {
        "name": "หมอ/วิศวกรอาวุโส - รายได้ 2.8M",
        "input": {
            "gross_income": 2800000,
            "personal_deduction": 60000,
            "spouse_deduction": 60000,
            "child_deduction": 90000,
            "parent_support": 240000,
            "disabled_support": 0,
            "life_insurance": 100000,
            "life_insurance_pension": 10000,
            "life_insurance_parents": 60000,
            "health_insurance": 25000,
            "health_insurance_parents": 60000,
            "social_security": 0,
            "pension_insurance": 200000,
            "provident_fund": 420000,
            "gpf": 0,
            "pvd_teacher": 0,
            "rmf": 0,
            "thai_esg": 0,
            "thai_esgx_new": 0,
            "thai_esgx_ltf": 0,
            "stock_investment": 100000,
            "easy_e_receipt": 50000,
            "home_loan_interest": 100000,
            "nsf": 30000,
            "donation_general": 100000,
            "donation_education": 200000,
            "donation_social_enterprise": 100000,
            "donation_political": 10000,
            "risk_tolerance": "high"
        }
    }
    
    # ===================================
    # Test Case 13: พนักงาน SME ไม่มี PVD
    # ===================================
    TEST_CASE_13 = {
        "name": "พนักงาน SME - รายได้ 540K, ไม่มี PVD",
        "input": {
            "gross_income": 540000,
            "personal_deduction": 60000,
            "spouse_deduction": 0,
            "child_deduction": 0,
            "parent_support": 60000,
            "disabled_support": 0,
            "life_insurance": 40000,
            "life_insurance_pension": 0,
            "life_insurance_parents": 15000,
            "health_insurance": 15000,
            "health_insurance_parents": 15000,
            "social_security": 9000,
            "pension_insurance": 50000,
            "provident_fund": 0,
            "gpf": 0,
            "pvd_teacher": 0,
            "rmf": 0,
            "thai_esg": 0,
            "thai_esgx_new": 0,
            "thai_esgx_ltf": 0,
            "stock_investment": 0,
            "easy_e_receipt": 20000,
            "home_loan_interest": 0,
            "nsf": 15000,
            "donation_general": 10000,
            "donation_education": 0,
            "donation_social_enterprise": 0,
            "donation_political": 0,
            "risk_tolerance": "medium"
        }
    }
    
    # ===================================
    # Test Case 14: ครอบครัวใหญ่ลูก 5 คน
    # ===================================
    TEST_CASE_14 = {
        "name": "ครอบครัวใหญ่ - ลูก 5 คน, รายได้ 1.1M",
        "input": {
            "gross_income": 1100000,
            "personal_deduction": 60000,
            "spouse_deduction": 60000,
            "child_deduction": 150000,
            "parent_support": 120000,
            "disabled_support": 0,
            "life_insurance": 80000,
            "life_insurance_pension": 10000,
            "life_insurance_parents": 30000,
            "health_insurance": 25000,
            "health_insurance_parents": 30000,
            "social_security": 9000,
            "pension_insurance": 100000,
            "provident_fund": 165000,
            "gpf": 0,
            "pvd_teacher": 0,
            "rmf": 0,
            "thai_esg": 0,
            "thai_esgx_new": 0,
            "thai_esgx_ltf": 0,
            "stock_investment": 0,
            "easy_e_receipt": 40000,
            "home_loan_interest": 80000,
            "nsf": 0,
            "donation_general": 20000,
            "donation_education": 30000,
            "donation_social_enterprise": 0,
            "donation_political": 0,
            "risk_tolerance": "low"
        }
    }
    
    # ===================================
    # Test Case 15: นักลงทุนรุ่นเยาว์
    # ===================================
    TEST_CASE_15 = {
        "name": "นักลงทุนรุ่นเยาว์ 28 ปี - รายได้ 780K",
        "input": {
            "gross_income": 780000,
            "personal_deduction": 60000,
            "spouse_deduction": 0,
            "child_deduction": 0,
            "parent_support": 0,
            "disabled_support": 0,
            "life_insurance": 30000,
            "life_insurance_pension": 0,
            "life_insurance_parents": 0,
            "health_insurance": 15000,
            "health_insurance_parents": 0,
            "social_security": 9000,
            "pension_insurance": 0,
            "provident_fund": 117000,
            "gpf": 0,
            "pvd_teacher": 0,
            "rmf": 0,
            "thai_esg": 0,
            "thai_esgx_new": 0,
            "thai_esgx_ltf": 0,
            "stock_investment": 50000,
            "easy_e_receipt": 30000,
            "home_loan_interest": 0,
            "nsf": 20000,
            "donation_general": 0,
            "donation_education": 0,
            "donation_social_enterprise": 0,
            "donation_political": 0,
            "risk_tolerance": "high"
        }
    }
    
    # ===================================
    # Test Case 16: อาจารย์มหาวิทยาลัย
    # ===================================
    TEST_CASE_16 = {
        "name": "อาจารย์มหาวิทยาลัย - รายได้ 960K",
        "input": {
            "gross_income": 960000,
            "personal_deduction": 60000,
            "spouse_deduction": 60000,
            "child_deduction": 60000,
            "parent_support": 60000,
            "disabled_support": 0,
            "life_insurance": 70000,
            "life_insurance_pension": 10000,
            "life_insurance_parents": 15000,
            "health_insurance": 25000,
            "health_insurance_parents": 15000,
            "social_security": 0,
            "pension_insurance": 80000,
            "provident_fund": 0,
            "gpf": 288000,
            "pvd_teacher": 0,
            "rmf": 0,
            "thai_esg": 0,
            "thai_esgx_new": 0,
            "thai_esgx_ltf": 0,
            "stock_investment": 0,
            "easy_e_receipt": 35000,
            "home_loan_interest": 70000,
            "nsf": 25000,
            "donation_general": 30000,
            "donation_education": 100000,
            "donation_social_enterprise": 0,
            "donation_political": 0,
            "risk_tolerance": "medium"
        }
    }
    
    # ===================================
    # Test Case 17: Startup Founder
    # ===================================
    TEST_CASE_17 = {
        "name": "Startup Founder - รายได้ 2.2M",
        "input": {
            "gross_income": 2200000,
            "personal_deduction": 60000,
            "spouse_deduction": 0,
            "child_deduction": 30000,
            "parent_support": 120000,
            "disabled_support": 0,
            "life_insurance": 100000,
            "life_insurance_pension": 10000,
            "life_insurance_parents": 30000,
            "health_insurance": 25000,
            "health_insurance_parents": 30000,
            "social_security": 0,
            "pension_insurance": 180000,
            "provident_fund": 0,
            "gpf": 0,
            "pvd_teacher": 0,
            "rmf": 0,
            "thai_esg": 0,
            "thai_esgx_new": 0,
            "thai_esgx_ltf": 0,
            "stock_investment": 100000,
            "easy_e_receipt": 50000,
            "home_loan_interest": 90000,
            "nsf": 30000,
            "donation_general": 80000,
            "donation_education": 150000,
            "donation_social_enterprise": 100000,
            "donation_political": 0,
            "risk_tolerance": "high"
        }
    }
    
    # ===================================
    # Test Case 18: พยาบาล
    # ===================================
    TEST_CASE_18 = {
        "name": "พยาบาล 33 ปี - รายได้ 660K",
        "input": {
            "gross_income": 660000,
            "personal_deduction": 60000,
            "spouse_deduction": 0,
            "child_deduction": 30000,
            "parent_support": 120000,
            "disabled_support": 0,
            "life_insurance": 50000,
            "life_insurance_pension": 5000,
            "life_insurance_parents": 30000,
            "health_insurance": 20000,
            "health_insurance_parents": 30000,
            "social_security": 9000,
            "pension_insurance": 60000,
            "provident_fund": 99000,
            "gpf": 0,
            "pvd_teacher": 0,
            "rmf": 0,
            "thai_esg": 0,
            "thai_esgx_new": 0,
            "thai_esgx_ltf": 0,
            "stock_investment": 0,
            "easy_e_receipt": 25000,
            "home_loan_interest": 0,
            "nsf": 15000,
            "donation_general": 15000,
            "donation_education": 10000,
            "donation_social_enterprise": 0,
            "donation_political": 0,
            "risk_tolerance": "low"
        }
    }
    
    # ===================================
    # Test Case 19: นักการเมืองท้องถิ่น
    # ===================================
    TEST_CASE_19 = {
        "name": "นักการเมืองท้องถิ่น - รายได้ 1.5M",
        "input": {
            "gross_income": 1500000,
            "personal_deduction": 60000,
            "spouse_deduction": 60000,
            "child_deduction": 60000,
            "parent_support": 120000,
            "disabled_support": 0,
            "life_insurance": 100000,
            "life_insurance_pension": 10000,
            "life_insurance_parents": 30000,
            "health_insurance": 25000,
            "health_insurance_parents": 30000,
            "social_security": 0,
            "pension_insurance": 150000,
            "provident_fund": 0,
            "gpf": 0,
            "pvd_teacher": 0,
            "rmf": 0,
            "thai_esg": 0,
            "thai_esgx_new": 0,
            "thai_esgx_ltf": 0,
            "stock_investment": 100000,
            "easy_e_receipt": 50000,
            "home_loan_interest": 80000,
            "nsf": 0,
            "donation_general": 150000,
            "donation_education": 100000,
            "donation_social_enterprise": 80000,
            "donation_political": 10000,
            "risk_tolerance": "medium"
        }
    }
    
    # ===================================
    # Test Case 20: Digital Nomad
    # ===================================
    TEST_CASE_20 = {
        "name": "Digital Nomad - รายได้ 1.3M",
        "input": {
            "gross_income": 1300000,
            "personal_deduction": 60000,
            "spouse_deduction": 0,
            "child_deduction": 0,
            "parent_support": 60000,
            "disabled_support": 0,
            "life_insurance": 80000,
            "life_insurance_pension": 10000,
            "life_insurance_parents": 15000,
            "health_insurance": 25000,
            "health_insurance_parents": 15000,
            "social_security": 0,
            "pension_insurance": 120000,
            "provident_fund": 0,
            "gpf": 0,
            "pvd_teacher": 0,
            "rmf": 0,
            "thai_esg": 0,
            "thai_esgx_new": 0,
            "thai_esgx_ltf": 0,
            "stock_investment": 100000,
            "easy_e_receipt": 50000,
            "home_loan_interest": 0,
            "nsf": 30000,
            "donation_general": 30000,
            "donation_education": 0,
            "donation_social_enterprise": 50000,
            "donation_political": 0,
            "risk_tolerance": "high"
        }
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
            cls.TEST_CASE_3,
            cls.TEST_CASE_4,
            cls.TEST_CASE_5,
            cls.TEST_CASE_6,
            cls.TEST_CASE_7,
            cls.TEST_CASE_8,
            cls.TEST_CASE_9,
            cls.TEST_CASE_10,
            cls.TEST_CASE_11,
            cls.TEST_CASE_12,
            cls.TEST_CASE_13,
            cls.TEST_CASE_14,
            cls.TEST_CASE_15,
            cls.TEST_CASE_16,
            cls.TEST_CASE_17,
            cls.TEST_CASE_18,
            cls.TEST_CASE_19,
            cls.TEST_CASE_20,
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