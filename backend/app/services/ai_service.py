from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import settings
from app.models import TaxCalculationRequest, TaxCalculationResult
import json

class AIService:
    """
    จัดการการเรียกใช้ OpenAI API
    ปรับปรุง Prompt Engineering ให้ตอบตรงประเด็นมากขึ้น
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
        สร้าง Prompt สำหรับ AI ให้วิเคราะห์และแนะนำ (ปรับปรุงใหม่)
        
        เทคนิค Prompt Engineering ที่ใช้:
        1. ให้ Context ชัดเจน (สถานการณ์ลูกค้า)
        2. ให้ข้อจำกัด (วงเงินที่เหลือ, กฎภาษี)
        3. ให้ตัวอย่างการคำนวณ
        4. ระบุห้ามทำอะไร
        5. กำหนด Output Format ชัดเจน
        """
        # คำนวณว่ามีที่ว่างในค่าลดหย่อนเท่าไหร่
        gross = tax_result.gross_income
        max_rmf = min(gross * 0.30, 500000)
        max_ssf = min(gross * 0.30, 200000)
        max_pension = min(gross * 0.15, 200000)
        max_life = 100000
        max_health = 25000
        
        remaining_rmf = max_rmf - request.rmf
        remaining_ssf = max_ssf - request.ssf
        remaining_pension = max_pension - request.pension_insurance
        remaining_life = max_life - request.life_insurance
        remaining_health = max_health - request.health_insurance
        
        # คำนวณอัตราภาษีส่วนเพิ่ม (Marginal Tax Rate) สำหรับคำนวณภาษีที่ประหยัดได้
        taxable = tax_result.taxable_income
        if taxable <= 150000:
            marginal_rate = 0
        elif taxable <= 300000:
            marginal_rate = 5
        elif taxable <= 500000:
            marginal_rate = 10
        elif taxable <= 750000:
            marginal_rate = 15
        elif taxable <= 1000000:
            marginal_rate = 20
        elif taxable <= 2000000:
            marginal_rate = 25
        elif taxable <= 5000000:
            marginal_rate = 30
        else:
            marginal_rate = 35
        
        return f"""คุณเป็นที่ปรึกษาภาษีมืออาชีพในประเทศไทย ปี 2568 
คุณให้คำแนะนำตามข้อมูลจริงจาก Knowledge Base เท่านั้น

===========================================
📊 สถานการณ์ปัจจุบันของลูกค้า
===========================================
รายได้รวม: {tax_result.gross_income:,.0f} บาท
เงินได้สุทธิ (หลังหักค่าลดหย่อน): {tax_result.taxable_income:,.0f} บาท
ภาษีที่ต้องจ่าย: {tax_result.tax_amount:,.0f} บาท
อัตราภาษีเฉลี่ย: {tax_result.effective_tax_rate}%
อัตราภาษีส่วนเพิ่ม (Marginal): {marginal_rate}%
ระดับความเสี่ยงที่ลูกค้าต้องการ: {request.risk_tolerance}

===========================================
💰 ค่าลดหย่อนที่ใช้แล้ว (และที่ว่างอยู่)
===========================================
1. RMF: {request.rmf:,.0f} / {max_rmf:,.0f} บาท 
   → เหลือที่ว่าง: {remaining_rmf:,.0f} บาท

2. SSF: {request.ssf:,.0f} / {max_ssf:,.0f} บาท
   → เหลือที่ว่าง: {remaining_ssf:,.0f} บาท

3. ประกันบำนาญ: {request.pension_insurance:,.0f} / {max_pension:,.0f} บาท
   → เหลือที่ว่าง: {remaining_pension:,.0f} บาท

4. ประกันชีวิต: {request.life_insurance:,.0f} / 100,000 บาท
   → เหลือที่ว่าง: {remaining_life:,.0f} บาท

5. ประกันสุขภาพ: {request.health_insurance:,.0f} / 25,000 บาท
   → เหลือที่ว่าง: {remaining_health:,.0f} บาท

6. กองทุนสำรองเลี้ยงชีพ: {request.provident_fund:,.0f} บาท
7. เงินบริจาค: {request.donation:,.0f} บาท

===========================================
📚 ข้อมูลอ้างอิงจาก Knowledge Base
===========================================
{retrieved_context}

===========================================
🎯 คำสั่งสำหรับ AI (อ่านให้ครบทุกข้อ!)
===========================================

**วิธีคำนวณภาษีที่ประหยัดได้อย่างถูกต้อง:**
ใช้ "อัตราภาษีส่วนเพิ่ม" ({marginal_rate}%) ในการคำนวณ

ตัวอย่าง:
- ลงทุน RMF 100,000 บาท
- ภาษีที่ประหยัดได้ = 100,000 × {marginal_rate}% = {int(100000 * marginal_rate / 100):,} บาท

**กฎการแนะนำ (สำคัญมาก!):**

1. ✅ แนะนำเฉพาะที่มี "เหลือที่ว่าง" เท่านั้น
   - ถ้า RMF เหลือ 0 บาท → ห้ามแนะนำ RMF
   - ถ้า RMF เหลือ 150,000 → แนะนำได้สูงสุด 150,000

2. ✅ จัดลำดับความสำคัญตาม:
   ก. ภาษีที่ประหยัดได้ (มากที่สุดก่อน)
   ข. ความเสี่ยงที่เหมาะกับลูกค้า
   ค. ผลตอบแทน

3. ✅ พิจารณาความเสี่ยงที่ลูกค้าต้องการ:
   - "low" → แนะนำประกันบำนาญ, กองทุนตราสารหนี้
   - "medium" → แนะนำ RMF ผสม, ประกันบำนาญ
   - "high" → แนะนำ RMF หุ้น, SSF

4. ✅ ใช้ข้อมูลจาก Knowledge Base เท่านั้น
   - ผลตอบแทนต้องตรงกับที่ระบุใน Knowledge Base
   - ข้อดี/ข้อเสียต้องตรงกับความจริง

5. ❌ ห้ามทำ:
   - ห้ามแนะนำเกินวงเงินที่เหลือ
   - ห้ามแต่งตัวเลขผลตอบแทน
   - ห้ามคำนวณภาษีผิด
   - ห้ามแนะนำสิ่งที่ลูกค้าทำครบแล้ว

**ตัวอย่างการแนะนำที่ถูกต้อง:**

สถานการณ์: RMF เหลือ 200,000 บาท, อัตราภาษี {marginal_rate}%
✅ ถูก:
{{
  "strategy": "ลงทุน RMF เพิ่ม 200,000 บาท",
  "investment_amount": 200000,
  "tax_saving": {int(200000 * marginal_rate / 100)},
  ...
}}

❌ ผิด: investment_amount: 300000 (เกินที่เหลือ!)
❌ ผิด: tax_saving: 50000 (คำนวณผิด!)

===========================================
📝 รูปแบบการตอบ (JSON Array เท่านั้น)
===========================================

แนะนำ 3-5 วิธีที่เหมาะสมที่สุด เรียงจากดีที่สุด ตามรูปแบบนี้:

[
  {{
    "strategy": "ลงทุน RMF เพิ่ม 150,000 บาท (กองทุนผสม)",
    "description": "ลงทุนในกองทุน RMF ประเภทผสมระหว่างหุ้นและตราสารหนี้ เพื่อเติมเต็มวงเงินที่เหลือและลดภาษีได้สูงสุด ต้องถือจนอายุ 55 ปี หรือถือครบ 5 ปีภาษี ผลตอบแทนคาดว่าจะได้ 5-8% ต่อปี",
    "investment_amount": 150000,
    "tax_saving": {int(150000 * marginal_rate / 100)},
    "risk_level": "medium",
    "expected_return_1y": 5.5,
    "expected_return_3y": 6.8,
    "expected_return_5y": 8.0,
    "pros": ["ลดหย่อนภาษีได้สูงสุด 30% ของรายได้", "ผลตอบแทนดีกว่าเงินฝาก", "บังคับออมระยะยาว", "เหมาะกับการเกษียณ"],
    "cons": ["ต้องถือจนอายุ 55 ปี หรือ 5 ปี", "มีความเสี่ยงตามตลาด", "ถอนก่อนเวลามีภาษีเพิ่ม", "ขาดสภาพคล่อง"]
  }},
  {{
    "strategy": "เปิดประกันบำนาญ 100,000 บาท",
    "description": "ซื้อประกันบำนาญเพื่อรับผลตอบแทนที่รับประกันและลดภาษี เหมาะกับคนที่ไม่ชอบความเสี่ยงและต้องการรายได้ที่แน่นอนหลังเกษียณ ผลตอบแทนรับประกันประมาณ 3-4% ต่อปี",
    "investment_amount": 100000,
    "tax_saving": {int(100000 * marginal_rate / 100)},
    "risk_level": "low",
    "expected_return_1y": 3.0,
    "expected_return_3y": 3.5,
    "expected_return_5y": 4.0,
    "pros": ["รับประกันผลตอบแทน", "ความเสี่ยงต่ำมาก", "มีรายได้ประจำหลังเกษียณ", "เหมาะกับคนอายุ 40+"],
    "cons": ["ผลตอบแทนต่ำกว่ากองทุน", "ต้องผูกพันระยะยาว", "ขาดสภาพคล่องสูง", "ค่าธรรมเนียมอาจสูง"]
  }}
]

⚠️ **สำคัญมาก:**
- ตอบเป็น JSON Array เท่านั้น
- ห้ามมี ```json หรือข้อความอื่นใดๆ
- เริ่มด้วย [ และจบด้วย ]
- ตรวจสอบให้แน่ใจว่า:
  * investment_amount ≤ วงเงินที่เหลือ
  * tax_saving = investment_amount × {marginal_rate}%
  * risk_level ตรงกับ risk_tolerance ของลูกค้า
  * ผลตอบแทนตรงกับข้อมูลจริง

เริ่มตอบเลย:"""
    
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
            
            print("=" * 60)
            print("📤 SENDING PROMPT TO AI:")
            print("=" * 60)
            print(prompt[:500] + "...[truncated]")
            print("=" * 60)
            
            # เรียก LLM
            response = await self.llm.ainvoke(prompt)
            
            print("=" * 60)
            print("📥 RAW AI RESPONSE:")
            print("=" * 60)
            print(response.content)
            print("=" * 60)
            
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
            
            print("=" * 60)
            print(f"✅ PARSED {len(recommendations)} RECOMMENDATIONS")
            print("=" * 60)
            
            return recommendations
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON Parse Error: {e}")
            print(f"Response was: {response.content}")
            # Fallback: ส่งคำแนะนำพื้นฐาน
            return self._get_fallback_recommendations(request, tax_result)
        except Exception as e:
            print(f"❌ AI Service Error: {e}")
            import traceback
            traceback.print_exc()
            return self._get_fallback_recommendations(request, tax_result)
    
    def _get_fallback_recommendations(
        self,
        request: TaxCalculationRequest,
        tax_result: TaxCalculationResult
    ) -> list[dict]:
        """
        คำแนะนำสำรองกรณี AI ล้มเหลว
        """
        gross = tax_result.gross_income
        max_rmf = min(gross * 0.30, 500000)
        remaining_rmf = max_rmf - request.rmf
        
        marginal_rate = 20  # ประมาณ
        
        recommendations = []
        
        # แนะนำ RMF ถ้ามีที่ว่าง
        if remaining_rmf > 0:
            amount = min(remaining_rmf, 100000)
            recommendations.append({
                "strategy": f"ลงทุน RMF เพิ่ม {amount:,.0f} บาท",
                "description": "ลงทุนในกองทุนรวมเพื่อการเลี้ยงชีพ (RMF) สามารถลดหย่อนภาษีได้สูงสุด 30% ของรายได้ ต้องถือจนอายุ 55 ปี หรือถือครบ 5 ปีภาษี",
                "investment_amount": amount,
                "tax_saving": int(amount * marginal_rate / 100),
                "risk_level": "medium",
                "expected_return_1y": 5.0,
                "expected_return_3y": 6.5,
                "expected_return_5y": 8.0,
                "pros": ["ลดหย่อนภาษีได้สูง", "มีผลตอบแทนดี", "บังคับออม"],
                "cons": ["ต้องถือจนอายุ 55 ปี", "มีความเสี่ยงตามตลาด"]
            })
        
        # แนะนำประกันบำนาญ
        max_pension = min(gross * 0.15, 200000)
        remaining_pension = max_pension - request.pension_insurance
        if remaining_pension > 0:
            amount = min(remaining_pension, 100000)
            recommendations.append({
                "strategy": f"เปิดประกันบำนาญ {amount:,.0f} บาท",
                "description": "ซื้อประกันบำนาญเพื่อลดหย่อนภาษี สูงสุด 15% ของรายได้ หรือไม่เกิน 200,000 บาท",
                "investment_amount": amount,
                "tax_saving": int(amount * marginal_rate / 100),
                "risk_level": "low",
                "expected_return_1y": 3.0,
                "expected_return_3y": 3.5,
                "expected_return_5y": 4.0,
                "pros": ["ความเสี่ยงต่ำ", "รับประกันผลตอบแทน", "มีรายได้หลังเกษียณ"],
                "cons": ["ผลตอบแทนต่ำกว่ากองทุน", "ผูกพันระยะยาว"]
            })
        
        return recommendations