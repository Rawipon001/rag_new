"""
Pydantic Models
Version: ปี 2568 - อัปเดตตามกฎหมายใหม่
"""

from pydantic import BaseModel, Field
from typing import List, Optional


# ===================================
# Request Models (จัดหมวดหมู่ปี 2568)
# ===================================

class TaxCalculationRequest(BaseModel):
    """ข้อมูลรายได้และค่าลดหย่อน ปี 2568"""
    
    # รายได้
    gross_income: int = Field(..., description="รายได้รวม", ge=0)
    
    # กลุ่มลดหย่อนส่วนตัว/ครอบครัว
    personal_deduction: int = Field(60000, description="ค่าลดหย่อนส่วนตัว", ge=0)
    spouse_deduction: int = Field(0, description="ค่าลดหย่อนคู่สมรส (ไม่มีรายได้)", ge=0, le=60000)
    child_deduction: int = Field(0, description="ค่าเลี้ยงดูบุตร (คนละ 30,000 ไม่จำกัดจำนวน)", ge=0)
    parent_support: int = Field(0, description="ค่าอุปการะเลี้ยงดูบิดามารดา (คนละ 60,000 สูงสุด 4 คน)", ge=0, le=240000)
    disabled_support: int = Field(0, description="ค่าอุปการะคนพิการ/ทุพพลภาพ (คนละ 60,000 ไม่จำกัด)", ge=0)
    
    # กลุ่มประกันชีวิตและสุขภาพ
    life_insurance: int = Field(0, description="เบี้ยประกันชีวิต", ge=0, le=100000)
    life_insurance_pension: int = Field(0, description="ประกันชีวิตแบบบำนาญ", ge=0, le=10000)
    life_insurance_parents: int = Field(0, description="เบี้ยประกันชีวิตบิดามารดา", ge=0, le=60000)
    health_insurance: int = Field(0, description="เบี้ยประกันสุขภาพ", ge=0, le=25000)
    health_insurance_parents: int = Field(0, description="เบี้ยประกันสุขภาพบิดามารดา (สูงสุด 4 คน)", ge=0, le=60000)
    social_security: int = Field(0, description="ประกันสังคม", ge=0, le=9000)
    
    # กลุ่มกองทุนและการลงทุน
    pension_insurance: int = Field(0, description="เบี้ยประกันบำนาญ", ge=0, le=200000)
    provident_fund: int = Field(0, description="กองทุนสำรองเลี้ยงชีพ (PVD)", ge=0, le=500000)
    gpf: int = Field(0, description="กองทุนบำเหน็จบำนาญข้าราชการ (กบข.)", ge=0, le=500000)
    pvd_teacher: int = Field(0, description="กองทุนสงเคราะห์ครูโรงเรียนเอกชน", ge=0, le=500000)
    rmf: int = Field(0, description="RMF", ge=0, le=500000)
    
    # กลุ่มกองทุน ESG (ใหม่ปี 2568 - แทน SSF)
    thai_esg: int = Field(0, description="กองทุน ThaiESG", ge=0, le=300000)
    thai_esgx_new: int = Field(0, description="กองทุน ThaiESGX (เงินใหม่)", ge=0, le=300000)
    thai_esgx_ltf: int = Field(0, description="กองทุน ThaiESGX (สะสมจาก LTF)", ge=0, le=300000)
    
    # กลุ่มอื่นๆ (ใหม่ปี 2568)
    stock_investment: int = Field(0, description="ลงทุนหุ้นจดทะเบียนที่ออกใหม่", ge=0, le=100000)
    easy_e_receipt: int = Field(0, description="Easy e-Receipt", ge=0, le=50000)
    home_loan_interest: int = Field(0, description="ดอกเบี้ยเงินกู้ซื้อ/สร้างบ้าน (2567-2568)", ge=0, le=100000)
    nsf: int = Field(0, description="กองทุนการออมแห่งชาติ (กอช.)", ge=0, le=30000)
    
    # กลุ่มเงินบริจาค
    donation_general: int = Field(0, description="เงินบริจาคทั่วไป", ge=0)
    donation_education: int = Field(0, description="เงินบริจาคเพื่อการศึกษา (นับ 2 เท่า)", ge=0)
    donation_social_enterprise: int = Field(0, description="บริจาค Social Enterprise", ge=0, le=100000)
    donation_political: int = Field(0, description="บริจาคพรรคการเมือง", ge=0, le=10000)
    
    # ระดับความเสี่ยง
    risk_tolerance: str = Field("medium", description="ระดับความเสี่ยง: low, medium, high")


# ===================================
# Response Models
# ===================================

class TaxCalculationResult(BaseModel):
    """ผลการคำนวณภาษี"""
    gross_income: int
    taxable_income: int
    tax_amount: int
    effective_tax_rate: float


class AllocationItem(BaseModel):
    """รายการการจัดสรรในแต่ละแผน"""
    category: str = Field(..., description="ประเภทการลงทุน")
    investment_amount: int = Field(..., description="จำนวนเงิน")
    percentage: float = Field(..., description="สัดส่วน %")
    tax_saving: int = Field(..., description="ภาษีที่ประหยัด")
    risk_level: str = Field(..., description="ระดับความเสี่ยง")
    pros: List[str] = Field(..., description="ข้อดี")
    cons: List[str] = Field(..., description="ข้อเสีย")


class InvestmentPlan(BaseModel):
    """แผนการลงทุนแต่ละแผน"""
    plan_id: str = Field(..., description="รหัสแผน A, B, C")
    plan_name: str = Field(..., description="ชื่อแผน")
    plan_type: str = Field(..., description="ประเภทแผน: conservative, moderate, aggressive")
    description: str = Field(..., description="คำอธิบายแผน")
    total_investment: int = Field(..., description="เงินลงทุนรวม")
    total_tax_saving: int = Field(..., description="ภาษีที่ประหยัดรวม")
    overall_risk: str = Field(..., description="ความเสี่ยงโดยรวม")
    allocations: List[AllocationItem] = Field(..., description="รายการการจัดสรร")


class MultiplePlansResponse(BaseModel):
    """Response ที่มีหลายแผนการลงทุน"""
    plans: List[InvestmentPlan] = Field(..., description="แผนการลงทุนทั้งหมด")


class TaxCalculationResponse(BaseModel):
    """Response สำหรับ API"""
    tax_result: TaxCalculationResult = Field(..., description="ผลการคำนวณภาษี")
    investment_plans: MultiplePlansResponse = Field(..., description="แผนการลงทุนทั้งหมด")