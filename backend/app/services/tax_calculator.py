from app.models import TaxCalculationRequest, TaxCalculationResult

# อัตราภาษีไทย 2025 (Progressive Tax Rate)
TAX_BRACKETS = [
    (0, 150000, 0.0),           # 0-150,000 = 0%
    (150001, 300000, 0.05),     # 150,001-300,000 = 5%
    (300001, 500000, 0.10),     # 300,001-500,000 = 10%
    (500001, 750000, 0.15),     # 500,001-750,000 = 15%
    (750001, 1000000, 0.20),    # 750,001-1,000,000 = 20%
    (1000001, 2000000, 0.25),   # 1,000,001-2,000,000 = 25%
    (2000001, 5000000, 0.30),   # 2,000,001-5,000,000 = 30%
    (5000001, float('inf'), 0.35)  # 5,000,001+ = 35%
]

class TaxCalculator:
    """
    คำนวณภาษีเงินได้บุคคลธรรมดาตามกฎหมายไทย
    """
    
    @staticmethod
    def calculate_progressive_tax(taxable_income: float) -> float:
        """
        คำนวณภาษีแบบ Progressive
        
        Args:
            taxable_income: เงินได้สุทธิที่ต้องเสียภาษี
            
        Returns:
            จำนวนภาษีที่ต้องจ่าย
        """
        if taxable_income <= 0:
            return 0.0
        
        tax = 0.0
        remaining = taxable_income
        
        for min_income, max_income, rate in TAX_BRACKETS:
            if remaining <= 0:
                break
                
            # คำนวณรายได้ที่อยู่ใน bracket นี้
            if max_income == float('inf'):
                taxable_in_bracket = remaining
            else:
                bracket_width = max_income - min_income + 1
                taxable_in_bracket = min(remaining, bracket_width)
            
            # คำนวณภาษีใน bracket นี้
            tax += taxable_in_bracket * rate
            remaining -= taxable_in_bracket
        
        return tax
    
    @staticmethod
    def calculate_total_deductions(request: TaxCalculationRequest) -> float:
        """
        คำนวณค่าลดหย่อนทั้งหมด
        
        ข้อจำกัดตามกฎหมาย:
        - ประกันชีวิต: สูงสุด 100,000 บาท
        - ประกันสุขภาพ: สูงสุด 25,000 บาท
        - กองทุนสำรองเลี้ยงชีพ: สูงสุด 15% ของเงินเดือน และไม่เกิน 500,000 บาท
        - RMF: สูงสุด 30% ของรายได้ และไม่เกิน 500,000 บาท
        - SSF: สูงสุด 30% ของรายได้ และไม่เกิน 200,000 บาท
        - ประกันบำนาญ: สูงสุด 15% ของรายได้ และไม่เกิน 200,000 บาท
        - เงินบริจาค: สูงสุด 10% ของรายได้หลังหักค่าใช้จ่าย
        """
        gross_income = request.salary + request.bonus
        
        # ค่าลดหย่อนพื้นฐาน
        deductions = (
            request.personal_allowance +
            request.spouse_allowance +
            request.child_allowance +
            request.social_security
        )
        
        # ประกันชีวิต (สูงสุด 100,000)
        deductions += min(request.life_insurance, 100000)
        
        # ประกันสุขภาพ (สูงสุด 25,000)
        deductions += min(request.health_insurance, 25000)
        
        # กองทุนสำรองเลี้ยงชีพ (สูงสุด 15% ของเงินเดือน, ไม่เกิน 500,000)
        max_provident = min(gross_income * 0.15, 500000)
        deductions += min(request.provident_fund, max_provident)
        
        # RMF (สูงสุด 30% ของรายได้, ไม่เกิน 500,000)
        max_rmf = min(gross_income * 0.30, 500000)
        deductions += min(request.rmf, max_rmf)
        
        # SSF (สูงสุด 30% ของรายได้, ไม่เกิน 200,000)
        max_ssf = min(gross_income * 0.30, 200000)
        deductions += min(request.ssf, max_ssf)
        
        # ประกันบำนาญ (สูงสุด 15% ของรายได้, ไม่เกิน 200,000)
        max_pension = min(gross_income * 0.15, 200000)
        deductions += min(request.pension_insurance, max_pension)
        
        # เงินบริจาค (สูงสุด 10% ของรายได้หลังหักค่าใช้จ่าย)
        taxable_before_donation = max(0, gross_income - deductions)
        max_donation = taxable_before_donation * 0.10
        deductions += min(request.donation, max_donation)
        
        return deductions
    
    @staticmethod
    def calculate(request: TaxCalculationRequest) -> TaxCalculationResult:
        """
        คำนวณภาษีทั้งหมด
        
        Args:
            request: ข้อมูลรายได้และค่าลดหย่อน
            
        Returns:
            ผลลัพธ์การคำนวณภาษี
        """
        # คำนวณรายได้รวม
        gross_income = request.salary + request.bonus
        
        # คำนวณค่าลดหย่อนทั้งหมด
        total_deductions = TaxCalculator.calculate_total_deductions(request)
        
        # คำนวณเงินได้สุทธิที่ต้องเสียภาษี
        taxable_income = max(0, gross_income - total_deductions)
        
        # คำนวณภาษี
        tax_amount = TaxCalculator.calculate_progressive_tax(taxable_income)
        
        # คำนวณรายได้สุทธิหลังหักภาษี
        net_income = gross_income - tax_amount
        
        # คำนวณอัตราภาษีเฉลี่ย
        effective_tax_rate = (tax_amount / gross_income * 100) if gross_income > 0 else 0.0
        
        # ตรวจสอบว่าควรใช้ RAG เพื่อหาวิธีลดภาษีหรือไม่
        # ถ้าเสียภาษีมากกว่า 10,000 บาท ให้แนะนำการลดภาษี
        requires_optimization = tax_amount > 10000
        
        return TaxCalculationResult(
            gross_income=gross_income,
            total_deductions=total_deductions,
            taxable_income=taxable_income,
            tax_amount=tax_amount,
            net_income=net_income,
            effective_tax_rate=round(effective_tax_rate, 2),
            requires_optimization=requires_optimization
        )