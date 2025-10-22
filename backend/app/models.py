# app/models.py
from pydantic import BaseModel, Field
from typing import List, Literal

class TaxCalculationRequest(BaseModel):
    """
    ข้อมูลที่รับจาก Frontend
    """
    # รายได้
    salary: float = Field(ge=0, description="เงินเดือนรายปี")
    bonus: float = Field(ge=0, description="โบนัสรายปี")
    
    # ค่าลดหย่อนพื้นฐาน
    personal_allowance: float = Field(default=60000, description="ค่าลดหย่อนส่วนตัว")
    spouse_allowance: float = Field(default=0, description="ค่าลดหย่อนคู่สมรส")
    child_allowance: float = Field(default=0, description="ค่าลดหย่อนบุตร")
    social_security: float = Field(default=0, description="ประกันสังคม")
    
    # ค่าลดหย่อนจากการลงทุน
    life_insurance: float = Field(default=0, description="ประกันชีวิต")
    health_insurance: float = Field(default=0, description="ประกันสุขภาพ")
    provident_fund: float = Field(default=0, description="กองทุนสำรองเลี้ยงชีพ")
    rmf: float = Field(default=0, description="RMF")
    ssf: float = Field(default=0, description="SSF")
    pension_insurance: float = Field(default=0, description="ประกันบำนาญ")
    donation: float = Field(default=0, description="เงินบริจาค")
    
    # ความเสี่ยง
    risk_tolerance: Literal["low", "medium", "high"] = Field(
        default="medium",
        description="ระดับความเสี่ยงที่รับได้"
    )


class TaxCalculationResult(BaseModel):
    """
    ผลการคำนวณภาษี
    """
    gross_income: float = Field(description="รายได้รวม")
    total_deductions: float = Field(description="ค่าลดหย่อนทั้งหมด")
    taxable_income: float = Field(description="เงินได้สุทธิที่ต้องเสียภาษี")
    tax_amount: float = Field(description="ภาษีที่ต้องจ่าย")
    net_income: float = Field(description="รายได้สุทธิหลังหักภาษี")
    effective_tax_rate: float = Field(description="อัตราภาษีเฉลี่ย (%)")
    requires_optimization: bool = Field(
        description="ควรใช้ RAG เพื่อหาวิธีลดภาษีหรือไม่"
    )


class Recommendation(BaseModel):
    """
    คำแนะนำการลดภาษี 1 วิธี
    """
    strategy: str = Field(description="ชื่อกลยุทธ์")
    description: str = Field(description="คำอธิบายวิธีการ")
    investment_amount: float = Field(description="จำนวนเงินที่แนะนำให้ลงทุน")
    tax_saving: float = Field(description="ภาษีที่ประหยัดได้")
    risk_level: Literal["low", "medium", "high"] = Field(description="ระดับความเสี่ยง")
    expected_return_1y: float = Field(description="ผลตอบแทนคาดการณ์ 1 ปี (%)")
    expected_return_3y: float = Field(default=0, description="ผลตอบแทนคาดการณ์ 3 ปี (%)")
    expected_return_5y: float = Field(default=0, description="ผลตอบแทนคาดการณ์ 5 ปี (%)")
    pros: List[str] = Field(description="ข้อดี")
    cons: List[str] = Field(description="ข้อเสีย")


class TaxOptimizationResponse(BaseModel):
    """
    Response ที่ส่งกลับไปหา Frontend
    """
    current_tax: TaxCalculationResult = Field(description="ผลการคำนวณภาษีปัจจุบัน")
    recommendations: List[Recommendation] = Field(description="คำแนะนำการลดภาษี")
    summary: str = Field(description="สรุปคำแนะนำ")
    disclaimer: str = Field(
        default="⚠️ ข้อมูลนี้เป็นเพียงคำแนะนำเบื้องต้น กรุณาปรึกษาที่ปรึกษาทางการเงินมืออาชีพก่อนตัดสินใจลงทุน",
        description="คำเตือน"
    )