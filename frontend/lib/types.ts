export interface TaxCalculationRequest {
  // รายได้
  salary: number;
  bonus: number;
  
  // ค่าลดหย่อนพื้นฐาน (คำนวณอัตโนมัติ)
  personal_allowance: number; // ระบบกำหนดให้ 60,000
  spouse_allowance: number;   // คำนวณจาก hasSpouse
  child_allowance: number;    // คำนวณจาก numberOfChildren
  social_security: number;    // คำนวณจาก hasSocialSecurity + จำนวนเงิน
  
  // ค่าลดหย่อนจากการลงทุน
  life_insurance: number;
  health_insurance: number;
  provident_fund: number;
  rmf: number;
  ssf: number;
  pension_insurance: number;
  donation: number;
  
  risk_tolerance: 'low' | 'medium' | 'high';
}

// Form State ที่ใช้จริงใน Frontend (ง่ายต่อการใช้งาน)
export interface SimplifiedFormData {
  // รายได้
  salary: number;
  bonus: number;
  
  // ค่าลดหย่อนส่วนตัว/ครอบครัว
  hasSpouse: boolean;
  numberOfChildren: number;
  
  // ประกันสังคม
  hasSocialSecurity: boolean;
  socialSecurityAmount: number; // สูงสุด 9,000
  
  // กลุ่มประกันชีวิต
  hasLifeInsurance: boolean;
  lifeInsuranceAmount: number; // สูงสุด 100,000
  
  hasHealthInsurance: boolean;
  healthInsuranceAmount: number; // สูงสุด 25,000
  
  hasPensionInsurance: boolean;
  pensionInsuranceAmount: number; // สูงสุด 200,000 หรือ 15% ของรายได้
  
  // กลุ่มกระตุ้นเศรษฐกิจ
  easyEReceiptAmount: number; // สูงสุด 50,000
  
  // กลุ่มเงินบริจาค
  donationAmount: number; // สูงสุด 10% ของรายได้
  
  // กลุ่มการลงทุน
  hasProvidentFund: boolean;
  providentFundAmount: number; // สูงสุด 15% ของเงินเดือน, ไม่เกิน 500,000
  
  hasRMF: boolean;
  rmfAmount: number; // สูงสุด 30% ของรายได้, ไม่เกิน 500,000
  
  hasSSF: boolean;
  ssfAmount: number; // สูงสุด 30% ของรายได้, ไม่เกิน 200,000
  
  // ความเสี่ยง
  risk_tolerance: 'low' | 'medium' | 'high';
}

export interface TaxCalculationResult {
  gross_income: number;
  total_deductions: number;
  taxable_income: number;
  tax_amount: number;
  net_income: number;
  effective_tax_rate: number;
  requires_optimization: boolean;
}

export interface Recommendation {
  strategy: string;
  description: string;
  investment_amount: number;
  tax_saving: number;
  risk_level: string;
  expected_return_1y: number | null;
  expected_return_3y: number | null;
  expected_return_5y: number | null;
  pros: string[];
  cons: string[];
}

export interface TaxOptimizationResponse {
  current_tax: TaxCalculationResult;
  recommendations: Recommendation[];
  summary: string;
  disclaimer: string;
}

// Helper function สำหรับแปลง SimplifiedFormData เป็น TaxCalculationRequest
export function convertToApiRequest(formData: SimplifiedFormData): TaxCalculationRequest {
  return {
    salary: formData.salary,
    bonus: formData.bonus,
    
    // ค่าลดหย่อนพื้นฐาน
    personal_allowance: 60000, // กำหนดให้อัตโนมัติ
    spouse_allowance: formData.hasSpouse ? 60000 : 0,
    child_allowance: formData.numberOfChildren * 30000, // 30,000 บาท/คน
    social_security: formData.hasSocialSecurity ? Math.min(formData.socialSecurityAmount, 9000) : 0,
    
    // ประกัน
    life_insurance: formData.hasLifeInsurance ? Math.min(formData.lifeInsuranceAmount, 100000) : 0,
    health_insurance: formData.hasHealthInsurance ? Math.min(formData.healthInsuranceAmount, 25000) : 0,
    pension_insurance: formData.hasPensionInsurance 
      ? Math.min(formData.pensionInsuranceAmount, Math.min(200000, (formData.salary + formData.bonus) * 0.15))
      : 0,
    
    // การลงทุน
    provident_fund: formData.hasProvidentFund 
      ? Math.min(formData.providentFundAmount, Math.min(500000, formData.salary * 0.15))
      : 0,
    rmf: formData.hasRMF 
      ? Math.min(formData.rmfAmount, Math.min(500000, (formData.salary + formData.bonus) * 0.30))
      : 0,
    ssf: formData.hasSSF 
      ? Math.min(formData.ssfAmount, Math.min(200000, (formData.salary + formData.bonus) * 0.30))
      : 0,
    
    // เงินบริจาค
    donation: Math.min(formData.donationAmount, (formData.salary + formData.bonus) * 0.10),
    
    risk_tolerance: formData.risk_tolerance
  };
}