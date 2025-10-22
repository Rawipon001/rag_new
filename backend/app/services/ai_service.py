from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import settings
from app.models import TaxCalculationRequest, TaxCalculationResult
import json

class AIService:
    """
    จัดการการเรียกใช้ OpenAI API
    """
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=settings.openai_temperature,
            openai_api_key=settings.openai_api_key
        )
    
    def generate_tax_optimization_prompt(
        self, 
        request: TaxCalculationRequest,
        tax_result: TaxCalculationResult,
        retrieved_context: str
    ) -> str:
        """
        สร้าง Prompt สำหรับ AI ให้วิเคราะห์และแนะนำ
        
        Args:
            request: ข้อมูลที่ผู้ใช้กรอก
            tax_result: ผลการคำนวณภาษี
            retrieved_context: ข้อมูลที่ดึงมาจาก Vector DB
            
        Returns:
            Prompt template
        """
        return f"""คุณเป็นที่ปรึกษาวางแผนภาษีมืออาชีพในประเทศไทย

**สถานการณ์ของลูกค้า:**
- รายได้รวม: {tax_result.gross_income:,.0f} บาท
- ภาษีที่ต้องจ่ายตอนนี้: {tax_result.tax_amount:,.0f} บาท
- อัตราภาษีเฉลี่ย: {tax_result.effective_tax_rate}%
- ระดับความเสี่ยงที่รับได้: {request.risk_tolerance}

**ค่าลดหย่อนที่ใช้แล้ว:**
- ประกันชีวิต: {request.life_insurance:,.0f} บาท
- ประกันสุขภาพ: {request.health_insurance:,.0f} บาท
- กองทุนสำรองเลี้ยงชีพ: {request.provident_fund:,.0f} บาท
- RMF: {request.rmf:,.0f} บาท
- SSF: {request.ssf:,.0f} บาท
- ประกันบำนาญ: {request.pension_insurance:,.0f} บาท
- เงินบริจาค: {request.donation:,.0f} บาท

**ข้อมูลอ้างอิงจาก Knowledge Base:**
{retrieved_context}

**คำสั่ง:**
วิเคราะห์สถานการณ์และแนะนำ 3-5 วิธีลดภาษี โดย:

1. **แต่ละวิธีต้องระบุ:**
   - strategy: ชื่อกลยุทธ์ (เช่น "ลงทุน RMF เพิ่ม", "เปิดประกันบำนาญ")
   - description: คำอธิบายว่าทำอย่างไร
   - investment_amount: จำนวนเงินที่แนะนำให้ลงทุน (บาท)
   - tax_saving: ภาษีที่ประหยัดได้ (บาท)
   - risk_level: ระดับความเสี่ยง (low/medium/high)
   - expected_return_1y, expected_return_3y, expected_return_5y: ผลตอบแทนคาดการณ์ (%)
   - pros: ข้อดี (list)
   - cons: ข้อเสีย (list)

2. **เรียงลำดับตามความเหมาะสม** (แนะนำตัวที่ดีที่สุดก่อน)

3. **พิจารณาความเสี่ยง** ตามที่ลูกค้าระบุ

4. **ใช้ข้อมูลจริง** จาก Knowledge Base ไม่แต่งตัวเลข

**ตอบเป็น JSON Array เท่านั้น** ตามรูปแบบนี้:
[
  {{
    "strategy": "ลงทุน RMF เพิ่ม 100,000 บาท",
    "description": "ลงทุนในกองทุน RMF เพิ่มเติม...",
    "investment_amount": 100000,
    "tax_saving": 30000,
    "risk_level": "medium",
    "expected_return_1y": 5.0,
    "expected_return_3y": 6.5,
    "expected_return_5y": 8.0,
    "pros": ["ลดหย่อนภาษีได้สูง", "มีผลตอบแทนดี"],
    "cons": ["ต้องถือจนอายุ 55 ปี", "มีความเสี่ยงตามตลาด"]
  }}
]

**ห้ามเขียนอะไรนอกจาก JSON Array**"""
    
    async def generate_recommendations(
        self,
        request: TaxCalculationRequest,
        tax_result: TaxCalculationResult,
        retrieved_context: str
    ) -> list[dict]:
        """
        เรียก OpenAI เพื่อสร้างคำแนะนำ
        
        Args:
            request: ข้อมูลผู้ใช้
            tax_result: ผลการคำนวณภาษี
            retrieved_context: ข้อมูลจาก Vector DB
            
        Returns:
            List ของคำแนะนำ
        """
        try:
            prompt = self.generate_tax_optimization_prompt(
                request, tax_result, retrieved_context
            )
            
            # เรียก LLM
            response = await self.llm.ainvoke(prompt)
            
            # Parse JSON
            recommendations_text = response.content.strip()
            
            # ลบ markdown code blocks ถ้ามี
            if recommendations_text.startswith("```json"):
                recommendations_text = recommendations_text[7:]
            if recommendations_text.startswith("```"):
                recommendations_text = recommendations_text[3:]
            if recommendations_text.endswith("```"):
                recommendations_text = recommendations_text[:-3]
            
            recommendations = json.loads(recommendations_text.strip())
            
            return recommendations
            
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}")
            print(f"Response: {response.content}")
            # Fallback: ส่งคำแนะนำพื้นฐาน
            return self._get_fallback_recommendations(request, tax_result)
        except Exception as e:
            print(f"AI Service Error: {e}")
            return self._get_fallback_recommendations(request, tax_result)
    
    def _get_fallback_recommendations(
        self,
        request: TaxCalculationRequest,
        tax_result: TaxCalculationResult
    ) -> list[dict]:
        """
        คำแนะนำสำรองกรณี AI ล้มเหลว
        """
        return [
            {
                "strategy": "ลงทุน RMF",
                "description": "ลงทุนในกองทุนรวมเพื่อการเลี้ยงชีพ (RMF) สามารถลดหย่อนภาษีได้สูงสุด 30% ของรายได้",
                "investment_amount": 100000,
                "tax_saving": 30000,
                "risk_level": "medium",
                "expected_return_1y": 5.0,
                "expected_return_3y": 6.5,
                "expected_return_5y": 8.0,
                "pros": ["ลดหย่อนภาษีได้สูง", "มีผลตอบแทนดี"],
                "cons": ["ต้องถือจนอายุ 55 ปี"]
            },
            {
                "strategy": "เปิดประกันบำนาญ",
                "description": "ซื้อประกันบำนาญเพื่อลดหย่อนภาษี สูงสุด 15% ของรายได้",
                "investment_amount": 50000,
                "tax_saving": 15000,
                "risk_level": "low",
                "expected_return_1y": 3.0,
                "expected_return_3y": 3.5,
                "expected_return_5y": 4.0,
                "pros": ["ความเสี่ยงต่ำ", "รับประกันผลตอบแทน"],
                "cons": ["ผลตอบแทนต่ำกว่ากองทุน"]
            }
        ]