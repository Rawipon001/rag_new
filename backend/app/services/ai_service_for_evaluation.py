"""
AI Service สำหรับ Evaluation เท่านั้น
แยกออกจากระบบหลัก เพื่อแสดง raw response จาก OpenAI

ไฟล์นี้จะถูกใช้โดย run_evaluation.py เท่านั้น
ไม่กระทบกับ ai_service.py ในระบบหลัก
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import os
from typing import Dict, List, Any

# Import models จากระบบหลัก
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.models import TaxCalculationRequest, TaxCalculationResult
from app.config import settings


class AIServiceForEvaluation:
    """
    AI Service แยกสำหรับ Evaluation
    
    ความแตกต่างจาก ai_service.py ในระบบหลัก:
    1. แสดง raw response จาก OpenAI
    2. บันทึก raw response ลงไฟล์
    3. แสดง prompt ที่ส่งไป
    4. มี verbose logging เพื่อ debug
    """
    
    def __init__(self, verbose: bool = True, save_to_file: bool = True):
        """
        Args:
            verbose: แสดงข้อความ debug หรือไม่
            save_to_file: บันทึก raw response ลงไฟล์หรือไม่
        """
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=settings.openai_temperature,
            openai_api_key=settings.openai_api_key
        )
        self.verbose = verbose
        self.save_to_file = save_to_file
        
        # สร้างโฟลเดอร์สำหรับเก็บ logs
        if self.save_to_file:
            self.log_dir = Path(__file__).parent.parent.parent / "evaluation_logs"
            self.log_dir.mkdir(exist_ok=True)
    
    def generate_tax_optimization_prompt(
        self, 
        request: TaxCalculationRequest,
        tax_result: TaxCalculationResult,
        retrieved_context: str
    ) -> str:
        """
        สร้าง Prompt (เหมือนกับระบบหลัก หรือปรับแต่งได้)
        
        **สามารถแก้ prompt ตรงนี้ได้เลย โดยไม่กระทบระบบหลัก**
        """
        gross = tax_result.gross_income
        max_rmf = min(gross * 0.30, 500000)
        max_ssf = min(gross * 0.30, 200000)
        max_pension = min(gross * 0.15, 200000)
        
        remaining_rmf = max_rmf - request.rmf
        remaining_ssf = max_ssf - request.ssf
        remaining_pension = max_pension - request.pension_insurance
        
        # คำนวณอัตราภาษีส่วนเพิ่ม
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

===========================================
📊 สถานการณ์ของลูกค้า
===========================================
รายได้รวม: {tax_result.gross_income:,.0f} บาท
เงินได้สุทธิ: {tax_result.taxable_income:,.0f} บาท
ภาษีที่ต้องจ่าย: {tax_result.tax_amount:,.0f} บาท
อัตราภาษีเฉลี่ย: {tax_result.effective_tax_rate}%
อัตราภาษีส่วนเพิ่ม: {marginal_rate}%
ระดับความเสี่ยง: {request.risk_tolerance}

===========================================
💰 ค่าลดหย่อนที่ใช้แล้ว
===========================================
RMF: {request.rmf:,.0f} / {max_rmf:,.0f} บาท (เหลือ {remaining_rmf:,.0f})
SSF: {request.ssf:,.0f} / {max_ssf:,.0f} บาท (เหลือ {remaining_ssf:,.0f})
ประกันบำนาญ: {request.pension_insurance:,.0f} / {max_pension:,.0f} บาท (เหลือ {remaining_pension:,.0f})
ประกันชีวิต: {request.life_insurance:,.0f} / 100,000 บาท
ประกันสุขภาพ: {request.health_insurance:,.0f} / 25,000 บาท
กองทุน PVD: {request.provident_fund:,.0f} บาท
เงินบริจาค: {request.donation:,.0f} บาท

===========================================
📚 ข้อมูลจาก Knowledge Base
===========================================
{retrieved_context}

===========================================
🎯 คำสั่ง
===========================================

**วิธีคำนวณภาษีที่ประหยัดได้:**
ภาษีที่ประหยัด = investment_amount × {marginal_rate}%

**กฎสำคัญ:**
1. แนะนำเฉพาะที่มีเหลือในวงเงิน
2. คำนวณภาษีให้ถูกต้อง
3. พิจารณาความเสี่ยงที่ลูกค้าต้องการ
4. ใช้ข้อมูลจาก Knowledge Base เท่านั้น

===========================================
📝 รูปแบบการตอบ (JSON Array เท่านั้น)
===========================================

ตอบเป็น JSON Array เท่านั้น ห้ามมีข้อความอื่น:

[
  {{
    "strategy": "ลงทุน RMF เพิ่ม 150,000 บาท (กองทุนผสม)",
    "description": "ลงทุนในกองทุน RMF ประเภทผสม...",
    "investment_amount": 150000,
    "tax_saving": {int(150000 * marginal_rate / 100)},
    "risk_level": "medium",
    "expected_return_1y": 5.5,
    "expected_return_3y": 6.8,
    "expected_return_5y": 8.0,
    "pros": ["ลดหย่อนภาษีได้สูง", "ผลตอบแทนดี"],
    "cons": ["ต้องถือจนอายุ 55 ปี", "มีความเสี่ยง"]
  }}
]

เริ่มตอบเลย:"""
    
    async def generate_recommendations(
        self,
        request: TaxCalculationRequest,
        tax_result: TaxCalculationResult,
        retrieved_context: str,
        test_case_id: int = 0
    ) -> tuple[list[dict], str]:
        """
        เรียก OpenAI เพื่อสร้างคำแนะนำ
        
        Returns:
            (recommendations, raw_response)
        """
        try:
            # สร้าง Prompt
            prompt = self.generate_tax_optimization_prompt(
                request, tax_result, retrieved_context
            )
            
            # แสดง Prompt (ถ้า verbose)
            if self.verbose:
                print("\n" + "=" * 80)
                print("📤 PROMPT SENT TO OPENAI:")
                print("=" * 80)
                print(prompt[:1000] + "...[truncated]" if len(prompt) > 1000 else prompt)
                print("=" * 80 + "\n")
            
            # บันทึก Prompt ลงไฟล์
            if self.save_to_file:
                prompt_file = self.log_dir / f"prompt_test_case_{test_case_id}.txt"
                with open(prompt_file, 'w', encoding='utf-8') as f:
                    f.write(prompt)
                if self.verbose:
                    print(f"💾 Saved prompt to: {prompt_file}\n")
            
            # เรียก OpenAI
            if self.verbose:
                print("🤖 Calling OpenAI API...")
            
            response = await self.llm.ainvoke(prompt)
            raw_response = response.content
            
            # แสดง Raw Response
            if self.verbose:
                print("\n" + "=" * 80)
                print("📥 RAW RESPONSE FROM OPENAI:")
                print("=" * 80)
                print(raw_response)
                print("=" * 80 + "\n")
            
            # บันทึก Raw Response ลงไฟล์
            if self.save_to_file:
                response_file = self.log_dir / f"raw_response_test_case_{test_case_id}.txt"
                with open(response_file, 'w', encoding='utf-8') as f:
                    f.write(raw_response)
                if self.verbose:
                    print(f"💾 Saved raw response to: {response_file}\n")
            
            # Parse JSON
            recommendations_text = raw_response.strip()
            
            # ลบ markdown code blocks ถ้ามี
            if recommendations_text.startswith("```json"):
                recommendations_text = recommendations_text[7:]
                if self.verbose:
                    print("🔧 Removed ```json prefix")
            if recommendations_text.startswith("```"):
                recommendations_text = recommendations_text[3:]
                if self.verbose:
                    print("🔧 Removed ``` prefix")
            if recommendations_text.endswith("```"):
                recommendations_text = recommendations_text[:-3]
                if self.verbose:
                    print("🔧 Removed ``` suffix")
            
            recommendations = json.loads(recommendations_text.strip())
            
            # แสดง Parsed Result
            if self.verbose:
                print("\n" + "=" * 80)
                print("📊 PARSED RECOMMENDATIONS:")
                print("=" * 80)
                print(json.dumps(recommendations, indent=2, ensure_ascii=False))
                print("=" * 80 + "\n")
                print(f"✅ Successfully parsed {len(recommendations)} recommendations\n")
            
            # บันทึก Parsed Result ลงไฟล์
            if self.save_to_file:
                parsed_file = self.log_dir / f"parsed_recommendations_test_case_{test_case_id}.json"
                with open(parsed_file, 'w', encoding='utf-8') as f:
                    json.dump(recommendations, f, indent=2, ensure_ascii=False)
                if self.verbose:
                    print(f"💾 Saved parsed recommendations to: {parsed_file}\n")
            
            return recommendations, raw_response
            
        except json.JSONDecodeError as e:
            print(f"\n❌ JSON Parse Error: {e}")
            print(f"\n📄 Raw Response was:")
            print("=" * 80)
            print(raw_response)
            print("=" * 80)
            
            # บันทึก error
            if self.save_to_file:
                error_file = self.log_dir / f"error_test_case_{test_case_id}.txt"
                with open(error_file, 'w', encoding='utf-8') as f:
                    f.write(f"JSON Parse Error: {e}\n\n")
                    f.write("Raw Response:\n")
                    f.write(raw_response)
                print(f"\n💾 Saved error to: {error_file}\n")
            
            # Return fallback
            return self._get_fallback_recommendations(request, tax_result), raw_response
            
        except Exception as e:
            print(f"\n❌ AI Service Error: {e}")
            import traceback
            traceback.print_exc()
            
            # บันทึก error
            if self.save_to_file:
                error_file = self.log_dir / f"error_test_case_{test_case_id}.txt"
                with open(error_file, 'w', encoding='utf-8') as f:
                    f.write(f"Error: {e}\n\n")
                    f.write(traceback.format_exc())
                print(f"\n💾 Saved error to: {error_file}\n")
            
            return self._get_fallback_recommendations(request, tax_result), ""
    
    def _get_fallback_recommendations(
        self,
        request: TaxCalculationRequest,
        tax_result: TaxCalculationResult
    ) -> list[dict]:
        """
        คำแนะนำสำรองกรณี AI ล้มเหลว
        """
        if self.verbose:
            print("\n⚠️  Using fallback recommendations...\n")
        
        gross = tax_result.gross_income
        max_rmf = min(gross * 0.30, 500000)
        remaining_rmf = max_rmf - request.rmf
        
        marginal_rate = 20  # ประมาณ
        
        recommendations = []
        
        if remaining_rmf > 0:
            amount = min(remaining_rmf, 100000)
            recommendations.append({
                "strategy": f"ลงทุน RMF เพิ่ม {amount:,.0f} บาท",
                "description": "คำแนะนำสำรอง: ลงทุนในกองทุน RMF",
                "investment_amount": amount,
                "tax_saving": int(amount * marginal_rate / 100),
                "risk_level": "medium",
                "expected_return_1y": 5.0,
                "expected_return_3y": 6.5,
                "expected_return_5y": 8.0,
                "pros": ["ลดหย่อนภาษี", "ผลตอบแทนดี"],
                "cons": ["ต้องถือจนอายุ 55 ปี"]
            })
        
        return recommendations


# ==========================================
# ตัวอย่างการใช้งาน
# ==========================================

if __name__ == "__main__":
    import asyncio
    from app.services.tax_service import TaxService
    
    print("🧪 Testing AIServiceForEvaluation\n")
    
    # สร้าง service
    ai_service = AIServiceForEvaluation(verbose=True, save_to_file=True)
    tax_service = TaxService()
    
    # สร้าง test request
    request = TaxCalculationRequest(
        gross_income=600000,
        personal_deduction=60000,
        life_insurance=50000,
        health_insurance=15000,
        provident_fund=50000,
        rmf=0,
        ssf=0,
        pension_insurance=0,
        donation=0,
        risk_tolerance="medium"
    )
    
    # คำนวณภาษี
    tax_result = tax_service.calculate_tax(request)
    
    # Mock context
    context = """
    RMF สามารถลดหย่อนภาษีได้สูงสุด 30% ของรายได้
    ต้องถือจนอายุ 55 ปี
    ผลตอบแทนประมาณ 5-8% ต่อปี
    """
    
    # เรียก AI
    async def test():
        recommendations, raw_response = await ai_service.generate_recommendations(
            request, tax_result, context, test_case_id=999
        )
        
        print("\n" + "=" * 80)
        print("✅ TEST COMPLETED!")
        print("=" * 80)
        print(f"📊 Got {len(recommendations)} recommendations")
        print(f"📝 Raw response length: {len(raw_response)} characters")
        print(f"💾 Files saved to: {ai_service.log_dir}")
        print("=" * 80 + "\n")
    
    asyncio.run(test())