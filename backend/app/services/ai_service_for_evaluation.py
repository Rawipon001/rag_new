"""
AI Service สำหรับ Evaluation - ปี 2568 (ฉบับสมบูรณ์)
ใช้ Prompt เหมือนกับระบบหลักทุกประการ
แยกออกจากระบบหลัก เพื่อแสดง raw response และทำ evaluation

จุดประสงค์:
1. แสดง raw response จาก OpenAI เพื่อตรวจสอบคุณภาพ
2. บันทึก logs สำหรับวิเคราะห์
3. ทำ evaluation โดยไม่กระทบระบบหลัก
"""

from langchain_openai import ChatOpenAI
import json
import os
from typing import Dict, List, Any, Tuple
from pathlib import Path

# Import models และ config
from app.models import TaxCalculationRequest, TaxCalculationResult
from app.config import settings


class AIServiceForEvaluation:
    """
    AI Service แยกสำหรับ Evaluation
    
    ความแตกต่างจากระบบหลัก:
    - แสดง raw response
    - บันทึก logs
    - Verbose logging
    - ไม่กระทบระบบหลัก
    """
    
    def __init__(self, verbose: bool = True, save_to_file: bool = True):
        """
        Args:
            verbose: แสดงข้อความ debug
            save_to_file: บันทึก logs ลงไฟล์
        """
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=0.3,  # ใช้ค่าเดียวกับระบบหลัก
            openai_api_key=settings.openai_api_key
        )
        self.verbose = verbose
        self.save_to_file = save_to_file
        
        # สร้างโฟลเดอร์สำหรับเก็บ logs
        if self.save_to_file:
            self.log_dir = Path(__file__).parent.parent.parent / "evaluation_logs"
            self.log_dir.mkdir(exist_ok=True)
            if self.verbose:
                print(f"📂 Log directory: {self.log_dir}")
    
    def generate_tax_optimization_prompt(
        self, 
        request: TaxCalculationRequest,
        tax_result: TaxCalculationResult,
        retrieved_context: str
    ) -> str:
        """
        สร้าง Prompt ที่เหมือนกับระบบหลักทุกประการ
        
        🔥 CRITICAL: Prompt นี้ต้องเหมือนกับ ai_service.py ในระบบหลัก
        """
        
        gross = tax_result.gross_income
        taxable = tax_result.taxable_income
        current_tax = tax_result.tax_amount
        
        # คำนวณวงเงินที่เหลือ - ปี 2568
        max_rmf = min(gross * 0.30, 500000)
        max_thai_esg = 300000  # ใหม่ปี 2568
        max_thai_esgx_new = 300000  # ใหม่ปี 2568
        max_thai_esgx_ltf = 300000  # ใหม่ปี 2568
        max_pension = min(gross * 0.15, 200000)
        max_pvd = min(gross * 0.15, 500000)
        
        remaining_rmf = max_rmf - request.rmf
        remaining_thai_esg = max_thai_esg - request.thai_esg
        remaining_thai_esgx_new = max_thai_esgx_new - request.thai_esgx_new
        remaining_thai_esgx_ltf = max_thai_esgx_ltf - request.thai_esgx_ltf
        remaining_pension = max_pension - request.pension_insurance
        remaining_pvd = max_pvd - request.provident_fund
        remaining_life = 100000 - request.life_insurance
        remaining_life_pension = 10000 - request.life_insurance_pension
        remaining_health = 25000 - request.health_insurance
        
        # อัตราภาษีส่วนเพิ่ม
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
        
        # ตรวจสอบว่ามีประกันหรือไม่
        has_life_insurance = request.life_insurance > 0
        has_health_insurance = request.health_insurance > 0
        
        # แปลงความเสี่ยง
        risk_map = {
            'low': 'ต่ำ',
            'medium': 'กลาง',
            'high': 'สูง'
        }
        risk_thai = risk_map.get(request.risk_tolerance, request.risk_tolerance)
        risk_level = request.risk_tolerance
        
        # คำนวณเงินลงทุนที่แนะนำตามรายได้
        if gross < 600000:
            suggested_min = 60000
            suggested_max = 150000
        elif gross < 1000000:
            suggested_min = 150000
            suggested_max = 300000
        elif gross < 1500000:
            suggested_min = 300000
            suggested_max = 500000
        elif gross < 2000000:
            suggested_min = 500000
            suggested_max = 800000
        elif gross < 3000000:
            suggested_min = 800000
            suggested_max = 1200000
        else:
            suggested_min = 1200000
            suggested_max = 1800000
        
        potential_tax_saving = int(suggested_max * (marginal_rate / 100))
        
        # 🔥 PROMPT เหมือนกับระบบหลักทุกประการ
        return f"""คุณเป็นที่ปรึกษาภาษีและการลงทุนมืออาชีพในประเทศไทย ปี 2568

📊 สถานการณ์ของลูกค้า:
- รายได้รวม: {gross:,.0f} บาท
- เงินได้สุทธิ: {taxable:,.0f} บาท
- ภาษีที่ต้องจ่ายตอนนี้: {current_tax:,.0f} บาท
- อัตราภาษีส่วนเพิ่ม: {marginal_rate}%
- ระดับความเสี่ยงที่ลูกค้าเลือก: {risk_thai}

💰 วงเงินค่าลดหย่อนที่ยังใช้ไม่ครบ (ปี 2568):
- RMF: เหลือ {remaining_rmf:,.0f} บาท (สูงสุด {max_rmf:,.0f})
- ThaiESG: เหลือ {remaining_thai_esg:,.0f} บาท (สูงสุด {max_thai_esg:,.0f})
- ThaiESGX (เงินใหม่): เหลือ {remaining_thai_esgx_new:,.0f} บาท (สูงสุด {max_thai_esgx_new:,.0f})
- ThaiESGX (จาก LTF): เหลือ {remaining_thai_esgx_ltf:,.0f} บาท (สูงสุด {max_thai_esgx_ltf:,.0f})
- กองทุนสำรองเลี้ยงชีพ: เหลือ {remaining_pvd:,.0f} บาท (สูงสุด {max_pvd:,.0f})
- ประกันบำนาญ: เหลือ {remaining_pension:,.0f} บาท (สูงสุด {max_pension:,.0f})
- ประกันชีวิต: เหลือ {remaining_life:,.0f} บาท
- ประกันชีวิตแบบบำนาญ: เหลือ {remaining_life_pension:,.0f} บาท
- ประกันสุขภาพ: เหลือ {remaining_health:,.0f} บาท

🎯 เป้าหมายการลงทุนที่แนะนำสำหรับรายได้ระดับนี้:
- เงินลงทุนแนะนำ: {suggested_min:,.0f} - {suggested_max:,.0f} บาท
- ภาษีที่อาจประหยัดได้: ประมาณ {potential_tax_saving:,.0f} บาท

🏥 สถานะประกัน:
- ประกันชีวิต: {'มีแล้ว' if has_life_insurance else 'ยังไม่มี - ควรมี'}
- ประกันสุขภาพ: {'มีแล้ว' if has_health_insurance else 'ยังไม่มี - ควรมี'}

🆕 สิ่งที่เปลี่ยนแปลงในปี 2568:
- ❌ SSF ยกเลิกแล้ว
- ✅ ThaiESG/ThaiESGX มาแทน (วงเงิน 300,000 บาท ยกเว้น 30%)
- ✅ Easy e-Receipt เพิ่มเป็น 50,000 บาท
- ✅ ค่าอุปการะบิดามารดาเพิ่มเป็น 60,000 บาท/คน

📚 ข้อมูลจาก Knowledge Base:
{retrieved_context}

🎯 ภารกิจ: สร้าง 3 แผนการลงทุนที่แตกต่างกัน

**กฎสำคัญ:**
1. แต่ละแผนต้องมีเงินลงทุนรวมอยู่ในช่วง {suggested_min:,.0f} - {suggested_max:,.0f} บาท
2. ทุกแผนต้องมีความเสี่ยงระดับ "{risk_level}"
3. แผนที่ 1: เน้นประกัน + ความปลอดภัย (เงินลงทุนใกล้ minimum)
4. แผนที่ 2: สมดุล กระจายความเสี่ยง (เงินลงทุนกลางๆ)
5. แผนที่ 3: เน้นการเติบโต + ลดหย่อนสูงสุด (เงินลงทุนใกล้ maximum)
{'6. ทุกแผนต้องมีประกันชีวิตอย่างน้อย 20,000 บาท' if not has_life_insurance else ''}
{'7. ทุกแผนต้องมีประกันสุขภาพอย่างน้อย 15,000 บาท' if not has_health_insurance else ''}
8. ควรใช้วงเงิน RMF ให้เต็มที่ (หรือใกล้เคียง) เพราะลดหย่อนได้สูง
9. **ใช้ ThaiESG/ThaiESGX แทน SSF** (SSF ยกเลิกแล้วในปี 2568)
10. สำหรับรายได้สูง (1,500,000+): ควรมีเงินบริจาคการศึกษา (นับ 2 เท่า)

**โครงสร้าง JSON ที่ต้องการ:**

```json
{{
  "plans": [
    {{
      "plan_id": "1",
      "plan_name": "ทางเลือกที่ 1 - เน้นประกัน",
      "plan_type": "{risk_level}",
      "description": "เน้นความคุ้มครอง เงินลงทุนพอเหมาะ",
      "total_investment": {suggested_min},
      "total_tax_saving": {int(suggested_min * marginal_rate / 100)},
      "overall_risk": "{risk_level}",
      "allocations": [...]
    }},
    {{
      "plan_id": "2",
      "plan_name": "ทางเลือกที่ 2 - สมดุล",
      "plan_type": "{risk_level}",
      "description": "กระจายความเสี่ยง เน้น RMF + ThaiESG",
      "total_investment": {int((suggested_min + suggested_max) / 2)},
      "total_tax_saving": {int((suggested_min + suggested_max) / 2 * marginal_rate / 100)},
      "overall_risk": "{risk_level}",
      "allocations": [...]
    }},
    {{
      "plan_id": "3",
      "plan_name": "ทางเลือกที่ 3 - ลงทุนสูงสุด",
      "plan_type": "{risk_level}",
      "description": "เน้นลดหย่อนภาษีสูงสุด ใช้วงเงินเต็มที่",
      "total_investment": {suggested_max},
      "total_tax_saving": {int(suggested_max * marginal_rate / 100)},
      "overall_risk": "{risk_level}",
      "allocations": [...]
    }}
  ]
}}
```

**หมายเหตุสำคัญ:**
- แต่ละ allocation ต้องมีครบทุก field: category, percentage, risk_level, pros, cons
- **ห้ามใส่ investment_amount และ tax_saving ใน allocations** (ระบบจะคำนวณให้อัตโนมัติ)
- pros และ cons ต้องเป็น array ของ string (อย่างน้อย 2-3 รายการ)
- **percentage รวมทั้งหมดในแต่ละแผนต้องใกล้เคียง 100** (ควรอยู่ในช่วง 99-101)
- **อย่าใช้ SSF** เพราะยกเลิกแล้วในปี 2568 ใช้ ThaiESG/ThaiESGX แทน

ตอบเป็น JSON เท่านั้น ห้ามมี markdown หรือข้อความอื่น:"""
    
    async def generate_recommendations(
        self,
        request: TaxCalculationRequest,
        tax_result: TaxCalculationResult,
        retrieved_context: str,
        test_case_id: int = 0
    ) -> Tuple[Dict[str, Any], str]:
        """
        เรียก OpenAI เพื่อสร้างคำแนะนำ
        
        Returns:
            (parsed_result, raw_response)
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
                print(prompt[:1500] + "...[truncated]" if len(prompt) > 1500 else prompt)
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
                print(raw_response[:2000] if len(raw_response) > 2000 else raw_response)
                if len(raw_response) > 2000:
                    print(f"...[truncated, total {len(raw_response)} characters]")
                print("=" * 80 + "\n")
            
            # บันทึก Raw Response ลงไฟล์
            if self.save_to_file:
                response_file = self.log_dir / f"raw_response_test_case_{test_case_id}.txt"
                with open(response_file, 'w', encoding='utf-8') as f:
                    f.write(raw_response)
                if self.verbose:
                    print(f"💾 Saved raw response to: {response_file}\n")
            
            # Parse JSON
            plans_text = raw_response.strip()
            
            # ลบ markdown code blocks ถ้ามี
            if plans_text.startswith("```json"):
                plans_text = plans_text[7:]
                if self.verbose:
                    print("🔧 Removed ```json prefix")
            if plans_text.startswith("```"):
                plans_text = plans_text[3:]
                if self.verbose:
                    print("🔧 Removed ``` prefix")
            if plans_text.endswith("```"):
                plans_text = plans_text[:-3]
                if self.verbose:
                    print("🔧 Removed ``` suffix")
            
            plans_text = plans_text.strip()
            result = json.loads(plans_text)
            
            # แสดง Parsed Result
            if self.verbose:
                print("\n" + "=" * 80)
                print("📊 PARSED RESULT:")
                print("=" * 80)
                print(json.dumps(result, indent=2, ensure_ascii=False)[:1500])
                print("=" * 80 + "\n")
                print(f"✅ Successfully parsed {len(result.get('plans', []))} plans\n")
            
            # บันทึก Parsed Result ลงไฟล์
            if self.save_to_file:
                parsed_file = self.log_dir / f"parsed_result_test_case_{test_case_id}.json"
                with open(parsed_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                if self.verbose:
                    print(f"💾 Saved parsed result to: {parsed_file}\n")
            
            # Validate
            self._validate_response(result)
            
            return result, raw_response
            
        except json.JSONDecodeError as e:
            print(f"\n❌ JSON Parse Error: {e}")
            print(f"\n📄 Raw Response was:")
            print("=" * 80)
            print(raw_response[:1000])
            print("=" * 80)
            
            if self.save_to_file:
                error_file = self.log_dir / f"error_test_case_{test_case_id}.txt"
                with open(error_file, 'w', encoding='utf-8') as f:
                    f.write(f"JSON Parse Error: {e}\n\n")
                    f.write("Raw Response:\n")
                    f.write(raw_response)
                print(f"\n💾 Saved error to: {error_file}\n")
            
            return self._get_fallback_response(request, tax_result), raw_response
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            
            if self.save_to_file:
                error_file = self.log_dir / f"error_test_case_{test_case_id}.txt"
                with open(error_file, 'w', encoding='utf-8') as f:
                    f.write(f"Error: {e}\n\n")
                    f.write(traceback.format_exc())
                print(f"\n💾 Saved error to: {error_file}\n")
            
            return self._get_fallback_response(request, tax_result), ""
    
    def _validate_response(self, result: Dict[str, Any]):
        """
        ตรวจสอบความถูกต้องของ response
        """
        if "plans" not in result:
            raise ValueError("Missing 'plans' key in response")
        
        if len(result["plans"]) != 3:
            raise ValueError(f"Expected 3 plans, got {len(result['plans'])}")
        
        required_plan_fields = ["plan_id", "plan_name", "plan_type", "description",
                               "total_investment", "total_tax_saving", "overall_risk", "allocations"]
        required_alloc_fields = ["category", "percentage", "risk_level", "pros", "cons"]
        
        for i, plan in enumerate(result["plans"]):
            for field in required_plan_fields:
                if field not in plan:
                    raise ValueError(f"Plan {i+1} missing field: {field}")
            
            if not plan["allocations"]:
                raise ValueError(f"Plan {i+1} has empty allocations")
            
            for j, alloc in enumerate(plan["allocations"]):
                for field in required_alloc_fields:
                    if field not in alloc:
                        raise ValueError(f"Plan {i+1}, Allocation {j+1} missing field: {field}")
        
        if self.verbose:
            print("✅ Response validation passed")
    
    def _get_fallback_response(
        self,
        request: TaxCalculationRequest,
        tax_result: TaxCalculationResult
    ) -> Dict[str, Any]:
        """
        คำตอบสำรองกรณี AI ล้มเหลว
        """
        if self.verbose:
            print("\n⚠️  Using fallback response...\n")
        
        gross = tax_result.gross_income
        risk = request.risk_tolerance
        
        # คำนวณเงินลงทุนแนะนำ
        if gross < 1000000:
            base_investment = 150000
        elif gross < 2000000:
            base_investment = 500000
        else:
            base_investment = 1000000
        
        return {
            "plans": [
                {
                    "plan_id": "1",
                    "plan_name": "ทางเลือกที่ 1 - เน้นประกัน (Fallback)",
                    "plan_type": risk,
                    "description": "แผนสำรอง - เน้นความคุ้มครอง",
                    "total_investment": base_investment,
                    "total_tax_saving": int(base_investment * 0.25),
                    "overall_risk": risk,
                    "allocations": [
                        {
                            "category": "ประกันชีวิต",
                            "investment_amount": int(base_investment * 0.25),
                            "percentage": 25,
                            "tax_saving": int(base_investment * 0.0625),
                            "risk_level": "low",
                            "pros": ["มีความคุ้มครอง", "จำเป็น"],
                            "cons": ["ผลตอบแทนต่ำ"]
                        },
                        {
                            "category": "RMF",
                            "investment_amount": int(base_investment * 0.50),
                            "percentage": 50,
                            "tax_saving": int(base_investment * 0.125),
                            "risk_level": risk,
                            "pros": ["ลดหย่อนภาษีสูง", "ผลตอบแทนดี"],
                            "cons": ["ต้องถือ 5 ปี"]
                        },
                        {
                            "category": "ประกันบำนาญ",
                            "investment_amount": int(base_investment * 0.25),
                            "percentage": 25,
                            "tax_saving": int(base_investment * 0.0625),
                            "risk_level": "low",
                            "pros": ["รับประกันผลตอบแทน"],
                            "cons": ["ผูกพันยาว"]
                        }
                    ]
                },
                {
                    "plan_id": "2",
                    "plan_name": "ทางเลือกที่ 2 - สมดุล (Fallback)",
                    "plan_type": risk,
                    "description": "แผนสำรอง - กระจายความเสี่ยง",
                    "total_investment": int(base_investment * 1.3),
                    "total_tax_saving": int(base_investment * 1.3 * 0.25),
                    "overall_risk": risk,
                    "allocations": []  # Simplified
                },
                {
                    "plan_id": "3",
                    "plan_name": "ทางเลือกที่ 3 - ลงทุนสูงสุด (Fallback)",
                    "plan_type": risk,
                    "description": "แผนสำรอง - ใช้วงเงินเต็มที่",
                    "total_investment": int(base_investment * 1.6),
                    "total_tax_saving": int(base_investment * 1.6 * 0.25),
                    "overall_risk": risk,
                    "allocations": []  # Simplified
                }
            ]
        }