"""
Tax Calculator Service
Version: Support All Deduction Categories - ปี 2568
"""

from typing import Dict
from app.models import TaxCalculationRequest, TaxCalculationResult


class TaxCalculatorService:
    """Service สำหรับคำนวณภาษีเงินได้บุคคลธรรมดา ปี 2568"""
    
    TAX_BRACKETS = [
        (150000, 0),
        (300000, 5),
        (500000, 10),
        (750000, 15),
        (1000000, 20),
        (2000000, 25),
        (5000000, 30),
        (float('inf'), 35)
    ]
    
    def calculate_tax(self, request: TaxCalculationRequest) -> TaxCalculationResult:
        """คำนวณภาษีเงินได้ ปี 2568"""
        
        gross_income = request.gross_income
        
        # รวมค่าลดหย่อนทั้งหมด ปี 2568
        total_deductions = (
            # กลุ่มส่วนตัว/ครอบครัว
            request.personal_deduction +
            request.spouse_deduction +
            request.child_deduction +
            request.parent_support +
            request.disabled_support +
            
            # กลุ่มประกันชีวิตและสุขภาพ
            request.life_insurance +
            request.life_insurance_pension +
            request.life_insurance_parents +
            request.health_insurance +
            request.health_insurance_parents +
            request.social_security +
            
            # กลุ่มกองทุนและการลงทุน
            request.pension_insurance +
            request.provident_fund +
            request.gpf +
            request.pvd_teacher +
            request.rmf +
            
            # กลุ่มกองทุน ESG (ใหม่ปี 2568 - แทน SSF)
            request.thai_esg +
            request.thai_esgx_new +
            request.thai_esgx_ltf +
            
            # กลุ่มอื่นๆ (ใหม่ปี 2568)
            request.stock_investment +
            request.easy_e_receipt +
            request.home_loan_interest +
            request.nsf +
            
            # กลุ่มเงินบริจาค
            request.donation_general +
            (request.donation_education * 2) +  # นับ 2 เท่า
            request.donation_social_enterprise +
            request.donation_political
        )
        
        # เงินได้สุทธิ
        taxable_income = max(0, gross_income - total_deductions)
        
        # คำนวณภาษี
        tax_amount = self._calculate_progressive_tax(taxable_income)
        
        # อัตราภาษีเฉลี่ย
        effective_tax_rate = (tax_amount / gross_income * 100) if gross_income > 0 else 0
        
        return TaxCalculationResult(
            gross_income=gross_income,
            taxable_income=taxable_income,
            tax_amount=tax_amount,
            effective_tax_rate=round(effective_tax_rate, 2)
        )
    
    def _calculate_progressive_tax(self, taxable_income: int) -> int:
        """คำนวณภาษีแบบขั้นบันได"""
        if taxable_income <= 0:
            return 0
        
        tax = 0
        previous_bracket = 0
        
        for bracket_limit, rate in self.TAX_BRACKETS:
            if taxable_income <= bracket_limit:
                taxable_in_bracket = taxable_income - previous_bracket
                tax += taxable_in_bracket * rate / 100
                break
            else:
                taxable_in_bracket = bracket_limit - previous_bracket
                tax += taxable_in_bracket * rate / 100
                previous_bracket = bracket_limit
        
        return int(tax)
    
    def get_marginal_tax_rate(self, taxable_income: int) -> int:
        """หาอัตราภาษีส่วนเพิ่ม"""
        for bracket_limit, rate in self.TAX_BRACKETS:
            if taxable_income <= bracket_limit:
                return rate
        return 35


# Export singleton
tax_calculator_service = TaxCalculatorService()