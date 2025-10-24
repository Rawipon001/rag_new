"""
AI Service สำหรับสร้างคำแนะนำภาษี
Version: Strict JSON Response
"""

from langchain_openai import ChatOpenAI
import json
from typing import Dict, List, Any

from app.models import TaxCalculationRequest, TaxCalculationResult
from app.config import settings


class AIService:
    """AI Service ที่บังคับให้ตอบ JSON ครบถ้วน"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=0.3,  # ลดลงเพื่อความสม่ำเสมอ
            openai_api_key=settings.openai_api_key
        )
    
    def generate_tax_optimization_prompt(
        self, 
        request: TaxCalculationRequest,
        tax_result: TaxCalculationResult,
        retrieved_context: str
    ) -> str:
        """สร้าง Prompt ที่บังคับ JSON ครบถ้วน"""
        
        gross = tax_result.gross_income
        
        # คำนวณวงเงินที่เหลือ
        max_rmf = min(gross * 0.30, 500000)
        max_ssf = min(gross * 0.30, 200000)
        max_pension = min(gross * 0.15, 200000)
        max_pvd = min(gross * 0.15, 500000)
        
        remaining_rmf = max_rmf - request.rmf
        remaining_ssf = max_ssf - request.ssf
        remaining_pension = max_pension - request.pension_insurance
        remaining_pvd = max_pvd - request.provident_fund
        remaining_life = 100000 - request.life_insurance
        remaining_health = 25000 - request.health_insurance
        
        # อัตราภาษีส่วนเพิ่ม
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
        
        # กำหนด risk_level
        risk_level = request.risk_tolerance  # "low", "medium", "high"
        
        return f"""คุณเป็นที่ปรึกษาภาษีและการลงทุนมืออาชีพในประเทศไทย

📊 สถานการณ์ของลูกค้า:
- รายได้รวม: {gross:,.0f} บาท
- เงินได้สุทธิ: {taxable:,.0f} บาท
- ภาษีที่ต้องจ่าย: {tax_result.tax_amount:,.0f} บาท
- อัตราภาษีส่วนเพิ่ม: {marginal_rate}%
- **ระดับความเสี่ยงที่ลูกค้าเลือก: {risk_thai}**

💰 วงเงินค่าลดหย่อนที่ยังใช้ไม่ครบ:
- กองทุนสำรองเลี้ยงชีพ: เหลือ {remaining_pvd:,.0f} บาท
- RMF: เหลือ {remaining_rmf:,.0f} บาท
- SSF: เหลือ {remaining_ssf:,.0f} บาท
- ประกันบำนาญ: เหลือ {remaining_pension:,.0f} บาท
- ประกันชีวิต: เหลือ {remaining_life:,.0f} บาท
- ประกันสุขภาพ: เหลือ {remaining_health:,.0f} บาท

🏥 สถานะประกัน:
- ประกันชีวิต: {'มีแล้ว' if has_life_insurance else 'ยังไม่มี'}
- ประกันสุขภาพ: {'มีแล้ว' if has_health_insurance else 'ยังไม่มี'}

📚 ข้อมูลจาก Knowledge Base:
{retrieved_context}

🎯 ภารกิจ:

สร้าง 3 ทางเลือกการลงทุนที่มีความเสี่ยง **{risk_thai}** เหมือนกันทั้งหมด

**กฎบังคับ:**
{'- ทุกแผนต้องมีประกันชีวิต' if not has_life_insurance else ''}
{'- ทุกแผนต้องมีประกันสุขภาพ' if not has_health_insurance else ''}

**ตัวอย่าง JSON ที่ต้องการ:**

```json
{{
  "plans": [
    {{
      "plan_id": "1",
      "plan_name": "ทางเลือกที่ 1 - เน้นประกันชีวิต",
      "plan_type": "{risk_level}",
      "description": "เน้นความคุ้มครอง",
      "total_investment": 100000,
      "total_tax_saving": 10000,
      "overall_risk": "{risk_level}",
      "allocations": [
        {{
          "category": "ประกันชีวิต",
          "investment_amount": 50000,
          "percentage": 50,
          "tax_saving": 5000,
          "risk_level": "low",
          "pros": ["มีความคุ้มครอง", "ความเสี่ยงต่ำ"],
          "cons": ["ผลตอบแทนต่ำ"]
        }},
        {{
          "category": "ประกันสุขภาพ",
          "investment_amount": 25000,
          "percentage": 25,
          "tax_saving": 2500,
          "risk_level": "low",
          "pros": ["คุ้มครองสุขภาพ"],
          "cons": ["ไม่มีผลตอบแทน"]
        }},
        {{
          "category": "ประกันบำนาญ",
          "investment_amount": 25000,
          "percentage": 25,
          "tax_saving": 2500,
          "risk_level": "low",
          "pros": ["รับประกันผลตอบแทน"],
          "cons": ["ผูกพันยาว"]
        }}
      ]
    }},
    {{
      "plan_id": "2",
      "plan_name": "ทางเลือกที่ 2 - เน้นกระจาย",
      "plan_type": "{risk_level}",
      "description": "กระจายความเสี่ยง",
      "total_investment": 120000,
      "total_tax_saving": 12000,
      "overall_risk": "{risk_level}",
      "allocations": [
        {{
          "category": "ประกันบำนาญ",
          "investment_amount": 50000,
          "percentage": 42,
          "tax_saving": 5000,
          "risk_level": "low",
          "pros": ["รับประกันผลตอบแทน"],
          "cons": ["ผูกพันยาว"]
        }},
        {{
          "category": "ประกันชีวิต",
          "investment_amount": 40000,
          "percentage": 33,
          "tax_saving": 4000,
          "risk_level": "low",
          "pros": ["มีความคุ้มครอง"],
          "cons": ["ผลตอบแทนต่ำ"]
        }},
        {{
          "category": "ประกันสุขภาพ",
          "investment_amount": 20000,
          "percentage": 17,
          "tax_saving": 2000,
          "risk_level": "low",
          "pros": ["คุ้มครองสุขภาพ"],
          "cons": ["ไม่มีผลตอบแทน"]
        }},
        {{
          "category": "เงินฝาก",
          "investment_amount": 10000,
          "percentage": 8,
          "tax_saving": 1000,
          "risk_level": "low",
          "pros": ["ปลอดภัย"],
          "cons": ["ดอกเบี้ยต่ำ"]
        }}
      ]
    }},
    {{
      "plan_id": "3",
      "plan_name": "ทางเลือกที่ 3 - เน้นประกันบำนาญ",
      "plan_type": "{risk_level}",
      "description": "เน้นเงินบำนาญ",
      "total_investment": 110000,
      "total_tax_saving": 11000,
      "overall_risk": "{risk_level}",
      "allocations": [
        {{
          "category": "ประกันบำนาญ",
          "investment_amount": 60000,
          "percentage": 55,
          "tax_saving": 6000,
          "risk_level": "low",
          "pros": ["รับประกันผลตอบแทน"],
          "cons": ["ผูกพันยาว"]
        }},
        {{
          "category": "ประกันชีวิต",
          "investment_amount": 30000,
          "percentage": 27,
          "tax_saving": 3000,
          "risk_level": "low",
          "pros": ["มีความคุ้มครอง"],
          "cons": ["ผลตอบแทนต่ำ"]
        }},
        {{
          "category": "ประกันสุขภาพ",
          "investment_amount": 20000,
          "percentage": 18,
          "tax_saving": 2000,
          "risk_level": "low",
          "pros": ["คุ้มครองสุขภาพ"],
          "cons": ["ไม่มีผลตอบแทน"]
        }}
      ]
    }}
  ]
}}
```

**กฎสำคัญ - อ่านให้ดี:**
1. ต้องตอบเป็น JSON เท่านั้น
2. ห้ามมี ```json หรือ ``` หรือข้อความอื่น
3. ทุก field ต้องครบถ้วน (category, investment_amount, percentage, tax_saving, risk_level, pros, cons)
4. overall_risk ทั้ง 3 แผนต้องเป็น "{risk_level}"
5. pros และ cons ต้องเป็น array ของ string
6. percentage รวมต้องเท่ากับ 100

ตอบเป็น JSON ทันที ห้ามมีอะไรอื่น:"""
    
    async def generate_recommendations(
        self,
        request: TaxCalculationRequest,
        tax_result: TaxCalculationResult,
        retrieved_context: str
    ) -> Dict[str, Any]:
        """เรียก OpenAI เพื่อสร้างหลายแผนการลงทุน"""
        try:
            prompt = self.generate_tax_optimization_prompt(
                request, tax_result, retrieved_context
            )
            
            response = await self.llm.ainvoke(prompt)
            raw_response = response.content
            
            # Parse JSON
            plans_text = raw_response.strip()
            
            # ลบ markdown code blocks
            if plans_text.startswith("```json"):
                plans_text = plans_text[7:]
            if plans_text.startswith("```"):
                plans_text = plans_text[3:]
            if plans_text.endswith("```"):
                plans_text = plans_text[:-3]
            
            plans_text = plans_text.strip()
            
            print(f"📝 AI Response (first 500 chars):")
            print(plans_text[:500])
            
            result = json.loads(plans_text)
            
            # Validate
            if "plans" not in result:
                raise ValueError("Invalid response structure - missing 'plans'")
            
            if len(result["plans"]) != 3:
                raise ValueError(f"Expected 3 plans, got {len(result['plans'])}")
            
            # Validate each plan
            for i, plan in enumerate(result["plans"]):
                required_fields = ["plan_id", "plan_name", "plan_type", "description", 
                                 "total_investment", "total_tax_saving", "overall_risk", "allocations"]
                for field in required_fields:
                    if field not in plan:
                        raise ValueError(f"Plan {i+1} missing field: {field}")
                
                # Validate allocations
                if not plan["allocations"]:
                    raise ValueError(f"Plan {i+1} has empty allocations")
                
                for j, alloc in enumerate(plan["allocations"]):
                    required_alloc_fields = ["category", "investment_amount", "percentage", 
                                            "tax_saving", "risk_level", "pros", "cons"]
                    for field in required_alloc_fields:
                        if field not in alloc:
                            raise ValueError(f"Plan {i+1}, Allocation {j+1} missing field: {field}")
            
            print("✅ Validation passed")
            return result
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON Parse Error: {e}")
            print(f"Raw Response:\n{raw_response[:1000]}")
            return self._get_fallback_plans(request, tax_result)
            
        except ValueError as e:
            print(f"❌ Validation Error: {e}")
            return self._get_fallback_plans(request, tax_result)
            
        except Exception as e:
            print(f"❌ AI Service Error: {e}")
            import traceback
            traceback.print_exc()
            return self._get_fallback_plans(request, tax_result)
    
    def _get_fallback_plans(
        self,
        request: TaxCalculationRequest,
        tax_result: TaxCalculationResult
    ) -> Dict[str, Any]:
        """แผนสำรองกรณี AI ล้มเหลว"""
        
        print("⚠️ Using fallback plans")
        
        has_life = request.life_insurance > 0
        has_health = request.health_insurance > 0
        risk = request.risk_tolerance
        
        if risk == 'low':
            return {
                "plans": [
                    {
                        "plan_id": "1",
                        "plan_name": "ทางเลือกที่ 1 - เน้นประกันชีวิต",
                        "plan_type": "low",
                        "description": "เน้นความคุ้มครอง",
                        "total_investment": 100000,
                        "total_tax_saving": 10000,
                        "overall_risk": "low",
                        "allocations": [
                            {
                                "category": "ประกันชีวิต",
                                "investment_amount": 50000,
                                "percentage": 50,
                                "tax_saving": 5000,
                                "risk_level": "low",
                                "pros": ["มีความคุ้มครอง", "ความเสี่ยงต่ำ"],
                                "cons": ["ผลตอบแทนต่ำ"]
                            },
                            {
                                "category": "ประกันสุขภาพ",
                                "investment_amount": 25000,
                                "percentage": 25,
                                "tax_saving": 2500,
                                "risk_level": "low",
                                "pros": ["คุ้มครองสุขภาพ"],
                                "cons": ["ไม่มีผลตอบแทน"]
                            },
                            {
                                "category": "ประกันบำนาญ",
                                "investment_amount": 25000,
                                "percentage": 25,
                                "tax_saving": 2500,
                                "risk_level": "low",
                                "pros": ["รับประกันผลตอบแทน"],
                                "cons": ["ผูกพันยาว"]
                            }
                        ]
                    },
                    {
                        "plan_id": "2",
                        "plan_name": "ทางเลือกที่ 2 - เน้นกระจาย",
                        "plan_type": "low",
                        "description": "กระจายความเสี่ยง",
                        "total_investment": 120000,
                        "total_tax_saving": 12000,
                        "overall_risk": "low",
                        "allocations": [
                            {
                                "category": "ประกันบำนาญ",
                                "investment_amount": 50000,
                                "percentage": 42,
                                "tax_saving": 5000,
                                "risk_level": "low",
                                "pros": ["รับประกันผลตอบแทน"],
                                "cons": ["ผูกพันยาว"]
                            },
                            {
                                "category": "ประกันชีวิต",
                                "investment_amount": 40000,
                                "percentage": 33,
                                "tax_saving": 4000,
                                "risk_level": "low",
                                "pros": ["มีความคุ้มครอง"],
                                "cons": ["ผลตอบแทนต่ำ"]
                            },
                            {
                                "category": "ประกันสุขภาพ",
                                "investment_amount": 20000,
                                "percentage": 17,
                                "tax_saving": 2000,
                                "risk_level": "low",
                                "pros": ["คุ้มครองสุขภาพ"],
                                "cons": ["ไม่มีผลตอบแทน"]
                            },
                            {
                                "category": "เงินฝาก",
                                "investment_amount": 10000,
                                "percentage": 8,
                                "tax_saving": 1000,
                                "risk_level": "low",
                                "pros": ["ปลอดภัย"],
                                "cons": ["ดอกเบี้ยต่ำ"]
                            }
                        ]
                    },
                    {
                        "plan_id": "3",
                        "plan_name": "ทางเลือกที่ 3 - เน้นประกันบำนาญ",
                        "plan_type": "low",
                        "description": "เน้นเงินบำนาญ",
                        "total_investment": 110000,
                        "total_tax_saving": 11000,
                        "overall_risk": "low",
                        "allocations": [
                            {
                                "category": "ประกันบำนาญ",
                                "investment_amount": 60000,
                                "percentage": 55,
                                "tax_saving": 6000,
                                "risk_level": "low",
                                "pros": ["รับประกันผลตอบแทน"],
                                "cons": ["ผูกพันยาว"]
                            },
                            {
                                "category": "ประกันชีวิต",
                                "investment_amount": 30000,
                                "percentage": 27,
                                "tax_saving": 3000,
                                "risk_level": "low",
                                "pros": ["มีความคุ้มครอง"],
                                "cons": ["ผลตอบแทนต่ำ"]
                            },
                            {
                                "category": "ประกันสุขภาพ",
                                "investment_amount": 20000,
                                "percentage": 18,
                                "tax_saving": 2000,
                                "risk_level": "low",
                                "pros": ["คุ้มครองสุขภาพ"],
                                "cons": ["ไม่มีผลตอบแทน"]
                            }
                        ]
                    }
                ]
            }
        
        elif risk == 'medium':
            return {
                "plans": [
                    {
                        "plan_id": "1",
                        "plan_name": "ทางเลือกที่ 1 - เน้น RMF",
                        "plan_type": "medium",
                        "description": "เน้นกองทุนรวม",
                        "total_investment": 150000,
                        "total_tax_saving": 15000,
                        "overall_risk": "medium",
                        "allocations": [
                            {
                                "category": "RMF กองทุนผสม",
                                "investment_amount": 75000,
                                "percentage": 50,
                                "tax_saving": 7500,
                                "risk_level": "medium",
                                "pros": ["ลดหย่อนสูง", "ผลตอบแทนดี"],
                                "cons": ["ต้องถือ 5 ปี", "มีความเสี่ยง"]
                            },
                            {
                                "category": "SSF",
                                "investment_amount": 30000,
                                "percentage": 20,
                                "tax_saving": 3000,
                                "risk_level": "medium",
                                "pros": ["ยืดหยุ่น"],
                                "cons": ["ต้องถือ 10 ปี"]
                            },
                            {
                                "category": "ประกันบำนาญ",
                                "investment_amount": 30000,
                                "percentage": 20,
                                "tax_saving": 3000,
                                "risk_level": "low",
                                "pros": ["รับประกันผลตอบแทน"],
                                "cons": ["ผูกพันยาว"]
                            },
                            {
                                "category": "ประกันชีวิต",
                                "investment_amount": 15000,
                                "percentage": 10,
                                "tax_saving": 1500,
                                "risk_level": "low",
                                "pros": ["มีความคุ้มครอง"],
                                "cons": ["ผลตอบแทนต่ำ"]
                            }
                        ]
                    },
                    {
                        "plan_id": "2",
                        "plan_name": "ทางเลือกที่ 2 - เน้นกระจาย",
                        "plan_type": "medium",
                        "description": "กระจายความเสี่ยง",
                        "total_investment": 140000,
                        "total_tax_saving": 14000,
                        "overall_risk": "medium",
                        "allocations": [
                            {
                                "category": "RMF",
                                "investment_amount": 50000,
                                "percentage": 36,
                                "tax_saving": 5000,
                                "risk_level": "medium",
                                "pros": ["ลดหย่อนสูง"],
                                "cons": ["ต้องถือ 5 ปี"]
                            },
                            {
                                "category": "SSF",
                                "investment_amount": 40000,
                                "percentage": 29,
                                "tax_saving": 4000,
                                "risk_level": "medium",
                                "pros": ["ยืดหยุ่น"],
                                "cons": ["ต้องถือ 10 ปี"]
                            },
                            {
                                "category": "ประกันบำนาญ",
                                "investment_amount": 30000,
                                "percentage": 21,
                                "tax_saving": 3000,
                                "risk_level": "low",
                                "pros": ["รับประกันผลตอบแทน"],
                                "cons": ["ผูกพันยาว"]
                            },
                            {
                                "category": "กองทุนสำรองเลี้ยงชีพ",
                                "investment_amount": 20000,
                                "percentage": 14,
                                "tax_saving": 2000,
                                "risk_level": "medium",
                                "pros": ["บริษัทจ่ายเพิ่ม"],
                                "cons": ["ถอนยาก"]
                            }
                        ]
                    },
                    {
                        "plan_id": "3",
                        "plan_name": "ทางเลือกที่ 3 - เน้น SSF",
                        "plan_type": "medium",
                        "description": "เน้น SSF",
                        "total_investment": 130000,
                        "total_tax_saving": 13000,
                        "overall_risk": "medium",
                        "allocations": [
                            {
                                "category": "SSF กองทุนผสม",
                                "investment_amount": 65000,
                                "percentage": 50,
                                "tax_saving": 6500,
                                "risk_level": "medium",
                                "pros": ["ยืดหยุ่น", "ลดหย่อนได้"],
                                "cons": ["ต้องถือ 10 ปี"]
                            },
                            {
                                "category": "RMF",
                                "investment_amount": 40000,
                                "percentage": 31,
                                "tax_saving": 4000,
                                "risk_level": "medium",
                                "pros": ["ลดหย่อนสูง"],
                                "cons": ["ต้องถือ 5 ปี"]
                            },
                            {
                                "category": "ประกันบำนาญ",
                                "investment_amount": 25000,
                                "percentage": 19,
                                "tax_saving": 2500,
                                "risk_level": "low",
                                "pros": ["รับประกันผลตอบแทน"],
                                "cons": ["ผูกพันยาว"]
                            }
                        ]
                    }
                ]
            }
        
        else:  # high
            return {
                "plans": [
                    {
                        "plan_id": "1",
                        "plan_name": "ทางเลือกที่ 1 - เน้น RMF หุ้น",
                        "plan_type": "high",
                        "description": "เน้นผลตอบแทนสูง",
                        "total_investment": 200000,
                        "total_tax_saving": 20000,
                        "overall_risk": "high",
                        "allocations": [
                            {
                                "category": "RMF กองทุนหุ้น",
                                "investment_amount": 120000,
                                "percentage": 60,
                                "tax_saving": 12000,
                                "risk_level": "high",
                                "pros": ["ผลตอบแทนสูง", "ลดหย่อนสูง"],
                                "cons": ["มีความเสี่ยง", "ต้องถือ 5 ปี"]
                            },
                            {
                                "category": "SSF กองทุนหุ้น",
                                "investment_amount": 50000,
                                "percentage": 25,
                                "tax_saving": 5000,
                                "risk_level": "high",
                                "pros": ["ผลตอบแทนสูง"],
                                "cons": ["มีความเสี่ยง", "ต้องถือ 10 ปี"]
                            },
                            {
                                "category": "ประกันชีวิต",
                                "investment_amount": 20000,
                                "percentage": 10,
                                "tax_saving": 2000,
                                "risk_level": "low",
                                "pros": ["มีความคุ้มครอง"],
                                "cons": ["ผลตอบแทนต่ำ"]
                            },
                            {
                                "category": "ประกันสุขภาพ",
                                "investment_amount": 10000,
                                "percentage": 5,
                                "tax_saving": 1000,
                                "risk_level": "low",
                                "pros": ["คุ้มครองสุขภาพ"],
                                "cons": ["ไม่มีผลตอบแทน"]
                            }
                        ]
                    },
                    {
                        "plan_id": "2",
                        "plan_name": "ทางเลือกที่ 2 - เน้นกระจาย",
                        "plan_type": "high",
                        "description": "กระจายในความเสี่ยงสูง",
                        "total_investment": 180000,
                        "total_tax_saving": 18000,
                        "overall_risk": "high",
                        "allocations": [
                            {
                                "category": "RMF",
                                "investment_amount": 80000,
                                "percentage": 44,
                                "tax_saving": 8000,
                                "risk_level": "high",
                                "pros": ["ผลตอบแทนสูง"],
                                "cons": ["มีความเสี่ยง"]
                            },
                            {
                                "category": "SSF",
                                "investment_amount": 60000,
                                "percentage": 33,
                                "tax_saving": 6000,
                                "risk_level": "high",
                                "pros": ["ผลตอบแทนสูง"],
                                "cons": ["มีความเสี่ยง"]
                            },
                            {
                                "category": "กองทุนสำรองเลี้ยงชีพ",
                                "investment_amount": 30000,
                                "percentage": 17,
                                "tax_saving": 3000,
                                "risk_level": "medium",
                                "pros": ["บริษัทจ่ายเพิ่ม"],
                                "cons": ["ถอนยาก"]
                            },
                            {
                                "category": "ประกันชีวิต",
                                "investment_amount": 10000,
                                "percentage": 6,
                                "tax_saving": 1000,
                                "risk_level": "low",
                                "pros": ["คุ้มครอง"],
                                "cons": ["ผลตอบแทนต่ำ"]
                            }
                        ]
                    },
                    {
                        "plan_id": "3",
                        "plan_name": "ทางเลือกที่ 3 - เน้น SSF หุ้น",
                        "plan_type": "high",
                        "description": "เน้น SSF",
                        "total_investment": 190000,
                        "total_tax_saving": 19000,
                        "overall_risk": "high",
                        "allocations": [
                            {
                                "category": "SSF กองทุนหุ้น",
                                "investment_amount": 105000,
                                "percentage": 55,
                                "tax_saving": 10500,
                                "risk_level": "high",
                                "pros": ["ผลตอบแทนสูง"],
                                "cons": ["มีความเสี่ยง", "ต้องถือ 10 ปี"]
                            },
                            {
                                "category": "RMF",
                                "investment_amount": 60000,
                                "percentage": 32,
                                "tax_saving": 6000,
                                "risk_level": "high",
                                "pros": ["ผลตอบแทนสูง"],
                                "cons": ["มีความเสี่ยง"]
                            },
                            {
                                "category": "กองทุนสำรองเลี้ยงชีพ",
                                "investment_amount": 20000,
                                "percentage": 11,
                                "tax_saving": 2000,
                                "risk_level": "medium",
                                "pros": ["บริษัทจ่ายเพิ่ม"],
                                "cons": ["ถอนยาก"]
                            },
                            {
                                "category": "ประกันสุขภาพ",
                                "investment_amount": 5000,
                                "percentage": 2,
                                "tax_saving": 500,
                                "risk_level": "low",
                                "pros": ["คุ้มครอง"],
                                "cons": ["ไม่มีผลตอบแทน"]
                            }
                        ]
                    }
                ]
            }