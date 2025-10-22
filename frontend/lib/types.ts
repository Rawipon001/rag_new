export interface TaxCalculationRequest {
  salary: number;
  bonus: number;
  personal_allowance: number;
  spouse_allowance: number;
  child_allowance: number;
  social_security: number;
  life_insurance: number;
  health_insurance: number;
  provident_fund: number;
  rmf: number;
  ssf: number;
  pension_insurance: number;
  donation: number;
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

export interface FormField {
  label: string;
  name: keyof TaxCalculationRequest;
  placeholder: string;
  max?: number;
  info?: string;
}

export const INCOME_FIELDS: FormField[] = [
  { label: 'เงินเดือนต่อปี', name: 'salary', placeholder: '600,000', info: 'รายได้จากเงินเดือนทั้งปี' },
  { label: 'โบนัสและรายได้อื่นๆ', name: 'bonus', placeholder: '100,000', info: 'โบนัส, ค่าคอมมิชชั่น' }
];

export const BASIC_DEDUCTION_FIELDS: FormField[] = [
  { label: 'ค่าลดหย่อนตัวเอง', name: 'personal_allowance', placeholder: '60,000', info: 'ค่าลดหย่อนพื้นฐาน 60,000 บาท' },
  { label: 'ค่าลดหย่อนคู่สมรส', name: 'spouse_allowance', placeholder: '0', max: 60000, info: 'สูงสุด 60,000 บาท' },
  { label: 'ค่าลดหย่อนบุตร', name: 'child_allowance', placeholder: '0', info: 'บุตรคนละ 30,000 บาท' }
];

export const INVESTMENT_DEDUCTION_FIELDS: FormField[] = [
  { label: 'ประกันสังคม', name: 'social_security', placeholder: '0', max: 9000, info: 'สูงสุด 9,000 บาท/ปี' },
  { label: 'ประกันชีวิต', name: 'life_insurance', placeholder: '0', max: 100000, info: 'สูงสุด 100,000 บาท/ปี' },
  { label: 'ประกันสุขภาพ', name: 'health_insurance', placeholder: '0', max: 25000, info: 'สูงสุด 25,000 บาท/ปี' },
  { label: 'กองทุนสำรองเลี้ยงชีพ', name: 'provident_fund', placeholder: '0', info: 'สูงสุด 15% ของเงินเดือน' },
  { label: 'กองทุน RMF', name: 'rmf', placeholder: '0', info: 'สูงสุด 30% ของรายได้ ไม่เกิน 500,000 บาท' },
  { label: 'กองทุน SSF', name: 'ssf', placeholder: '0', info: 'สูงสุด 30% ของรายได้ ไม่เกิน 200,000 บาท' },
  { label: 'ประกันบำนาญ', name: 'pension_insurance', placeholder: '0', info: 'สูงสุด 15% ของรายได้' },
  { label: 'เงินบริจาค', name: 'donation', placeholder: '0', info: 'สูงสุด 10% ของรายได้หลังหักค่าใช้จ่าย' }
];