'use client';

import React, { useState } from 'react';
import MultiplePlansView from './components/MultiplePlansView';
import { TaxCalculationResponse } from '../lib/types';

export default function Home() {
  const [formData, setFormData] = useState({
    // รายได้
    gross_income: 600000,

    // ประเภทเงินได้และวิธีคำนวณ (ใหม่ปี 2568 - ตาม backend)
    income_type: "40(8)", // ประเภทเงินได้ตามมาตรา 40(8) - ธุรกิจ
    business_type: "general_trade", // ประเภทธุรกิจ
    expense_method: "standard", // วิธีหักค่าใช้จ่าย (เหมา)
    actual_expenses: 0, // ค่าใช้จ่ายจริง (ถ้าเลือก expense_method = actual)

    // กลุ่มส่วนตัว/ครอบครัว
    personal_deduction: 60000, // ค่าคงที่ ไม่ให้แก้
    has_spouse: false, // มีคู่สมรสไม่มีรายได้หรือไม่
    number_of_children: 0, // จำนวนบุตร (ไม่จำกัด x 30,000)
    number_of_parents: 0, // จำนวนบิดามารดา (สูงสุด 4 คน x 30,000)
    number_of_disabled: 0, // จำนวนคนพิการ/ทุพพลภาพ (ไม่จำกัด x 60,000)

    // กลุ่มประกันและการลงทุน
    life_insurance: 0, // สูงสุด 100,000
    life_insurance_pension: 0, // ประกันชีวิตแบบบำนาญ สูงสุด 10,000
    life_insurance_parents: 0, // สูงสุด 15,000/คน
    health_insurance: 0, // สูงสุด 25,000
    health_insurance_parents: 0, // สูงสุด 15,000/คน (สูงสุด 4 คน = 60,000)
    pension_insurance: 0, // ประกันบำนาญ สูงสุด 15% หรือ 200,000
    social_security: 0, // ประกันสังคม สูงสุด 9,000
    provident_fund: 0, // PVD สูงสุด 15% หรือ 500,000
    gpf: 0, // กบข. สูงสุด 30% หรือ 500,000
    pvd_teacher: 0, // กองทุนสงเคราะห์ครูฯ สูงสุด 15% หรือ 500,000

    // กลุ่มกองทุน (เปลี่ยนแปลงปี 2568 - ไม่มี SSF แล้ว!)
    rmf: 0, // RMF สูงสุด 30% หรือ 500,000
    thai_esg: 0, // ThaiESG สูงสุด 300,000 (ยกเว้น 30%)
    thai_esgx_new: 0, // ThaiESGX เงินใหม่ สูงสุด 300,000 (ยกเว้น 30%)
    thai_esgx_ltf: 0, // ThaiESGX จาก LTF สูงสุด 300,000

    // กลุ่มอื่นๆ (ใหม่ปี 2568)
    stock_investment: 0, // ลงทุนหุ้นจดทะเบียนใหม่ สูงสุด 100,000 (ถือ 2 ปี)
    easy_e_receipt: 0, // Easy e-Receipt สูงสุด 50,000
    home_loan_interest: 0, // ดอกเบี้ยสร้างบ้าน (2567-2568) สูงสุด 100,000
    nsf: 0, // กองทุนการออมแห่งชาติ (กอช.) สูงสุด 30,000

    // กลุ่มเงินบริจาค
    donation_general: 0, // บริจาคทั่วไป 10% ของรายได้
    donation_education: 0, // บริจาคการศึกษา (นับ 2 เท่า)
    donation_social_enterprise: 0, // บริจาค Social Enterprise สูงสุด 100,000
    donation_political: 0, // บริจาคพรรคการเมือง สูงสุด 10,000

    risk_tolerance: 'medium' as 'low' | 'medium' | 'high',
  });

  const [result, setResult] = useState<TaxCalculationResponse & { no_tax_required?: boolean } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showInfo, setShowInfo] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;

    if (name === 'risk_tolerance') {
      setFormData((prev) => ({
        ...prev,
        [name]: value,
      }));
    } else if (type === 'checkbox') {
      // Handle checkbox
      const checked = (e.target as HTMLInputElement).checked;
      setFormData((prev) => ({
        ...prev,
        [name]: checked,
      }));
    } else {
      // ถ้าเป็นช่องตัวเลข
      if (value === '') {
        // ถ้าลบหมดให้เป็น 0
        setFormData((prev) => ({
          ...prev,
          [name]: 0,
        }));
      } else {
        // แปลงเป็นตัวเลข
        const numValue = parseInt(value);
        setFormData((prev) => ({
          ...prev,
          [name]: isNaN(numValue) ? 0 : numValue,
        }));
      }
    }
  };

  const handleCalculate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // ✅ คำนวณเบื้องต้นว่าต้องจ่ายภาษีหรือไม่
      // คำนวณค่าลดหย่อนตามจำนวนคนจริง
      const spouse_deduction = formData.has_spouse ? 60000 : 0;
      const child_deduction = formData.number_of_children * 30000; // ไม่จำกัดจำนวน
      const parent_support = Math.min(formData.number_of_parents, 4) * 30000; // สูงสุด 4 คน x 30,000
      const disabled_support = formData.number_of_disabled * 60000; // ไม่จำกัดจำนวน x 60,000

      const totalDeductions =
        formData.personal_deduction +
        spouse_deduction +
        child_deduction +
        parent_support +
        disabled_support +
        formData.life_insurance +
        formData.life_insurance_pension +
        formData.life_insurance_parents +
        formData.health_insurance +
        formData.health_insurance_parents +
        formData.pension_insurance +
        formData.social_security +
        formData.provident_fund +
        formData.gpf +
        formData.pvd_teacher +
        formData.rmf +
        formData.thai_esg +
        formData.thai_esgx_new +
        formData.thai_esgx_ltf +
        formData.stock_investment +
        formData.easy_e_receipt +
        formData.home_loan_interest +
        formData.nsf +
        formData.donation_general +
        (formData.donation_education * 2) +
        formData.donation_social_enterprise +
        formData.donation_political;

      const taxableIncome = Math.max(0, formData.gross_income - totalDeductions);
      const requiresTax = taxableIncome > 150000; // เกินขั้นแรกที่ยกเว้นภาษี (0-150,000 บาท)

      console.log('📊 Quick Tax Check (ปี 2568):');
      console.log(`   รายได้รวม: ${formData.gross_income.toLocaleString()} บาท`);
      console.log(`   ค่าลดหย่อนรวม: ${totalDeductions.toLocaleString()} บาท`);
      console.log(`   เงินได้สุทธิ: ${taxableIncome.toLocaleString()} บาท`);
      console.log(`   ต้องจ่ายภาษี: ${requiresTax ? 'ใช่' : 'ไม่ต้อง'}`);

      // ✅ ถ้าไม่ต้องจ่ายภาษี แสดงผลทันที ไม่ต้องเรียก API
      if (!requiresTax) {
        console.log('✅ ไม่ต้องจ่ายภาษี - ไม่เรียก API');
        setResult({
          tax_result: {
            gross_income: formData.gross_income,
            taxable_income: taxableIncome,
            tax_amount: 0,
            effective_tax_rate: 0,
            total_deductions: totalDeductions,
            requires_optimization: false
          },
          investment_plans: { plans: [] },
          no_tax_required: true
        });
        setLoading(false);
        return;
      }

      // ✅ ถ้าต้องจ่ายภาษี เรียก API เพื่อคำนวณและรับคำแนะนำ
      console.log('⏳ ต้องจ่ายภาษี - กำลังเรียก API...');

      // เตรียมข้อมูลส่ง API โดยแปลงเป็นค่าลดหย่อนที่คำนวณแล้ว
      // สร้าง object ใหม่โดยไม่รวม has_spouse, number_of_children, etc.
      const apiPayload = {
        // ข้อมูลพื้นฐานและประเภทเงินได้
        gross_income: formData.gross_income,
        income_type: formData.income_type,
        business_type: formData.business_type,
        expense_method: formData.expense_method,
        actual_expenses: formData.actual_expenses,

        // ค่าลดหย่อนที่คำนวณแล้ว
        personal_deduction: formData.personal_deduction,
        spouse_deduction: spouse_deduction,
        child_deduction: child_deduction,
        parent_support: parent_support,
        disabled_support: disabled_support,

        // ประกันและการลงทุน (copy จาก formData)
        life_insurance: formData.life_insurance,
        life_insurance_pension: formData.life_insurance_pension,
        life_insurance_parents: formData.life_insurance_parents,
        health_insurance: formData.health_insurance,
        health_insurance_parents: formData.health_insurance_parents,
        pension_insurance: formData.pension_insurance,
        social_security: formData.social_security,
        provident_fund: formData.provident_fund,
        gpf: formData.gpf,
        pvd_teacher: formData.pvd_teacher,
        rmf: formData.rmf,
        thai_esg: formData.thai_esg,
        thai_esgx_new: formData.thai_esgx_new,
        thai_esgx_ltf: formData.thai_esgx_ltf,
        stock_investment: formData.stock_investment,
        easy_e_receipt: formData.easy_e_receipt,
        home_loan_interest: formData.home_loan_interest,
        nsf: formData.nsf,
        donation_general: formData.donation_general,
        donation_education: formData.donation_education,
        donation_social_enterprise: formData.donation_social_enterprise,
        donation_political: formData.donation_political,

        // ระดับความเสี่ยง
        risk_tolerance: formData.risk_tolerance
      };

      const response = await fetch('http://localhost:8000/api/calculate-tax', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(apiPayload),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ API Response:', data);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'เกิดข้อผิดพลาด');
      console.error('❌ Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white py-16 px-4 shadow-2xl">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            <div className="inline-block bg-white/20 backdrop-blur-sm px-6 py-2 rounded-full mb-4">
              <span className="text-sm font-semibold">อัปเดตล่าสุด: พ.ศ. 2568 (2025)</span>
            </div>
            <h1 className="text-5xl md:text-6xl font-bold mb-4 drop-shadow-lg">
              AI Tax Advisor
            </h1>
            <p className="text-xl md:text-2xl mb-6 text-blue-100">
              ที่ปรึกษาภาษีอัจฉริยะ - วางแผนภาษีให้คุณได้รับสิทธิประโยชน์สูงสุด
            </p>
            <div className="flex flex-wrap justify-center gap-4 text-sm">
              <div className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-lg">
                ✅ ใช้กฎหมายภาษี พ.ศ. 2568
              </div>
              <div className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-lg">
                💰 คำนวณภาษีแม่นยำ 100%
              </div>
              <div className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-lg">
                🤖 AI แนะนำ 3 แผนการลงทุน
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Tax Year 2568 Info Banner */}
        <div className="mb-8 bg-gradient-to-r from-orange-50 to-red-50 border-l-4 border-orange-500 rounded-lg p-6 shadow-lg">
          <div className="flex items-start gap-4">
            <div className="text-3xl">📢</div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-orange-900 mb-2">
                การเปลี่ยนแปลงสำคัญในปี 2568
              </h3>
              <ul className="space-y-2 text-sm text-orange-800">
                <li className="flex items-start gap-2">
                  <span className="text-orange-600">•</span>
                  <span><strong>ยกเลิก SSF</strong> → ใช้ <strong>ThaiESG/ThaiESGX</strong> แทน (วงเงินสูงสุด 300,000 บาท/กองทุน)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-orange-600">•</span>
                  <span><strong>Easy e-Receipt เพิ่มเป็น 50,000 บาท</strong> (จากเดิม 30,000 บาท)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-orange-600">•</span>
                  <span><strong>ค่าอุปการะบิดามารดาเพิ่ม</strong> สูงสุด 120,000 บาท (4 คน × 30,000 บาท)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-orange-600">•</span>
                  <span><strong>ลงทุนหุ้นจดทะเบียนใหม่</strong> ลดหย่อนได้ 100,000 บาท (ถือครบ 2 ปี)</span>
                </li>
              </ul>
              <button
                onClick={() => setShowInfo(!showInfo)}
                className="mt-4 text-sm text-orange-700 hover:text-orange-900 font-semibold underline"
              >
                {showInfo ? '▲ ซ่อนข้อมูลเพิ่มเติม' : '▼ ดูข้อมูลค่าลดหย่อนทั้งหมด'}
              </button>
            </div>
          </div>
        </div>

        {/* Deductions Info Panel */}
        {showInfo && (
          <div className="mb-8 bg-white rounded-2xl shadow-xl p-8 border-2 border-indigo-200">
            <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
              📋 ตารางค่าลดหย่อนภาษี พ.ศ. 2568
            </h3>

            <div className="grid md:grid-cols-2 gap-6">
              {/* กลุ่มการลงทุนระยะยาว */}
              <div className="bg-purple-50 rounded-xl p-5 border-2 border-purple-200">
                <h4 className="font-bold text-purple-900 mb-3 text-lg">💼 กลุ่มการลงทุนระยะยาว</h4>
                <table className="w-full text-sm">
                  <tbody className="space-y-1">
                    <tr className="border-b border-purple-200">
                      <td className="py-2 text-gray-700">RMF</td>
                      <td className="py-2 text-right font-semibold text-purple-800">500,000 บาท (30%)</td>
                    </tr>
                    <tr className="border-b border-purple-200">
                      <td className="py-2 text-gray-700">ThaiESG</td>
                      <td className="py-2 text-right font-semibold text-purple-800">300,000 บาท (ถือ 8 ปี)</td>
                    </tr>
                    <tr className="border-b border-purple-200">
                      <td className="py-2 text-gray-700">ThaiESGX</td>
                      <td className="py-2 text-right font-semibold text-purple-800">300,000 บาท (เงินใหม่)</td>
                    </tr>
                    <tr>
                      <td className="py-2 text-gray-700">กองทุนสำรองเลี้ยงชีพ</td>
                      <td className="py-2 text-right font-semibold text-purple-800">500,000 บาท (15%)</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              {/* กลุ่มประกัน */}
              <div className="bg-green-50 rounded-xl p-5 border-2 border-green-200">
                <h4 className="font-bold text-green-900 mb-3 text-lg">🏥 กลุ่มประกัน</h4>
                <table className="w-full text-sm">
                  <tbody>
                    <tr className="border-b border-green-200">
                      <td className="py-2 text-gray-700">ประกันบำนาญ</td>
                      <td className="py-2 text-right font-semibold text-green-800">200,000 บาท (15%)</td>
                    </tr>
                    <tr className="border-b border-green-200">
                      <td className="py-2 text-gray-700">ประกันชีวิต</td>
                      <td className="py-2 text-right font-semibold text-green-800">100,000 บาท</td>
                    </tr>
                    <tr className="border-b border-green-200">
                      <td className="py-2 text-gray-700">ประกันสุขภาพ</td>
                      <td className="py-2 text-right font-semibold text-green-800">25,000 บาท</td>
                    </tr>
                    <tr>
                      <td className="py-2 text-gray-700">ประกันบิดามารดา</td>
                      <td className="py-2 text-right font-semibold text-green-800">60,000 บาท (4 คน)</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              {/* กลุ่มครอบครัว */}
              <div className="bg-blue-50 rounded-xl p-5 border-2 border-blue-200">
                <h4 className="font-bold text-blue-900 mb-3 text-lg">👨‍👩‍👧‍👦 กลุ่มครอบครัว</h4>
                <table className="w-full text-sm">
                  <tbody>
                    <tr className="border-b border-blue-200">
                      <td className="py-2 text-gray-700">ส่วนตัว</td>
                      <td className="py-2 text-right font-semibold text-blue-800">60,000 บาท</td>
                    </tr>
                    <tr className="border-b border-blue-200">
                      <td className="py-2 text-gray-700">คู่สมรส</td>
                      <td className="py-2 text-right font-semibold text-blue-800">60,000 บาท</td>
                    </tr>
                    <tr className="border-b border-blue-200">
                      <td className="py-2 text-gray-700">บุตร</td>
                      <td className="py-2 text-right font-semibold text-blue-800">30,000 บาท/คน</td>
                    </tr>
                    <tr className="border-b border-blue-200">
                      <td className="py-2 text-gray-700">อุปการะบิดามารดา</td>
                      <td className="py-2 text-right font-semibold text-blue-800">120,000 บาท (4 คน)</td>
                    </tr>
                    <tr>
                      <td className="py-2 text-gray-700">คนพิการ</td>
                      <td className="py-2 text-right font-semibold text-blue-800">60,000 บาท/คน</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              {/* กลุ่มอื่นๆ */}
              <div className="bg-yellow-50 rounded-xl p-5 border-2 border-yellow-200">
                <h4 className="font-bold text-yellow-900 mb-3 text-lg">✨ กลุ่มอื่นๆ (ใหม่ 2568)</h4>
                <table className="w-full text-sm">
                  <tbody>
                    <tr className="border-b border-yellow-200">
                      <td className="py-2 text-gray-700">หุ้นจดทะเบียนใหม่</td>
                      <td className="py-2 text-right font-semibold text-yellow-800">100,000 บาท</td>
                    </tr>
                    <tr className="border-b border-yellow-200">
                      <td className="py-2 text-gray-700">Easy e-Receipt</td>
                      <td className="py-2 text-right font-semibold text-yellow-800">50,000 บาท</td>
                    </tr>
                    <tr className="border-b border-yellow-200">
                      <td className="py-2 text-gray-700">ดอกเบี้ยบ้าน</td>
                      <td className="py-2 text-right font-semibold text-yellow-800">100,000 บาท</td>
                    </tr>
                    <tr>
                      <td className="py-2 text-gray-700">บริจาคการศึกษา</td>
                      <td className="py-2 text-right font-semibold text-yellow-800">นับ 2 เท่า</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Main Form */}
        <div className="bg-white rounded-2xl shadow-2xl p-8 mb-8 border-t-4 border-indigo-500">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-3xl font-bold text-gray-800 flex items-center gap-3">
              <span className="text-4xl">📝</span>
              กรอกข้อมูลของคุณ
            </h2>
            <div className="text-right">
              <p className="text-sm text-gray-500">ใช้เวลาเพียง 2-3 นาที</p>
              <p className="text-xs text-gray-400">ข้อมูลของคุณปลอดภัย 100%</p>
            </div>
          </div>

          <form onSubmit={handleCalculate} className="space-y-6">
            {/* รายได้ */}
            <div className="bg-gradient-to-r from-orange-50 to-red-50 rounded-xl p-6 border-2 border-orange-300 shadow-md">
              <h3 className="text-xl font-bold text-orange-800 mb-4 flex items-center gap-2">
                <span className="text-2xl">💰</span>
                รายได้ต่อปี
              </h3>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  รายได้รวมต่อปี (บาท) <span className="text-red-500">*</span>
                </label>
                <input
                  type="number"
                  name="gross_income"
                  value={formData.gross_income === 0 ? '' : formData.gross_income}
                  onChange={handleInputChange}
                  placeholder="ตัวอย่าง: 600000"
                  className="w-full px-6 py-4 text-lg border-2 border-gray-300 rounded-xl focus:border-orange-500 focus:ring-2 focus:ring-orange-200 focus:outline-none transition-all"
                  required
                />
                <p className="text-xs text-gray-500 mt-2">
                  💡 รวมเงินเดือน โบนัส และรายได้อื่นๆ ทั้งหมดในปี
                </p>
              </div>

              {/* Expense Method Selection - NEW */}
              <div className="mt-6">
                <h4 className="text-lg font-bold text-orange-800 mb-3 flex items-center gap-2">
                  <span className="text-xl">📊</span>
                  วิธีการหักค่าใช้จ่าย
                </h4>
                <div className="space-y-3">
                  {/* Standard Method */}
                  <label className="flex items-start gap-3 p-4 border-2 rounded-lg cursor-pointer transition-all hover:bg-orange-50 hover:border-orange-400"
                    style={{
                      borderColor: formData.expense_method === 'standard' ? '#fb923c' : '#d1d5db',
                      backgroundColor: formData.expense_method === 'standard' ? '#fff7ed' : 'white'
                    }}>
                    <input
                      type="radio"
                      name="expense_method"
                      value="standard"
                      checked={formData.expense_method === 'standard'}
                      onChange={handleInputChange}
                      className="w-5 h-5 mt-1 text-orange-600 border-gray-300 focus:ring-orange-500 cursor-pointer"
                    />
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-gray-800">หักค่าใช้จ่ายเหมา (Standard)</span>
                        <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full font-semibold">แนะนำ</span>
                      </div>
                      <p className="text-sm text-gray-600 mt-1">
                        หักตามเปอร์เซ็นต์ที่กฎหมายกำหนด (30% หรือ 60% ตามประเภทเงินได้)
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        ✅ ไม่ต้องเก็บใบเสร็จ | ✅ คำนวณง่าย | ✅ เหมาะกับคนทำงาน
                      </p>
                    </div>
                  </label>

                  {/* Actual Method */}
                  <label className="flex items-start gap-3 p-4 border-2 rounded-lg cursor-pointer transition-all hover:bg-orange-50 hover:border-orange-400"
                    style={{
                      borderColor: formData.expense_method === 'actual' ? '#fb923c' : '#d1d5db',
                      backgroundColor: formData.expense_method === 'actual' ? '#fff7ed' : 'white'
                    }}>
                    <input
                      type="radio"
                      name="expense_method"
                      value="actual"
                      checked={formData.expense_method === 'actual'}
                      onChange={handleInputChange}
                      className="w-5 h-5 mt-1 text-orange-600 border-gray-300 focus:ring-orange-500 cursor-pointer"
                    />
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-gray-800">หักค่าใช้จ่ายตามจริง (Actual)</span>
                        <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full font-semibold">SME/Freelance</span>
                      </div>
                      <p className="text-sm text-gray-600 mt-1">
                        หักค่าใช้จ่ายจริงทั้งหมดตามใบเสร็จ (วัตถุดิบ, ค่าเช่า, ค่าจ้าง, ฯลฯ)
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        📄 ต้องมีใบเสร็จครบ | 📊 ต้องทำบัญชี | 💰 เหมาะกับธุรกิจต้นทุนสูง
                      </p>
                    </div>
                  </label>
                </div>

                {/* Actual Expenses Input - Conditional */}
                {formData.expense_method === 'actual' && (
                  <div className="mt-4 p-4 bg-yellow-50 border-2 border-yellow-300 rounded-lg">
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      ค่าใช้จ่ายจริงทั้งหมด (บาท) <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="number"
                      name="actual_expenses"
                      value={formData.actual_expenses === 0 ? '' : formData.actual_expenses}
                      onChange={handleInputChange}
                      placeholder="ตัวอย่าง: 400000"
                      className="w-full px-6 py-4 text-lg border-2 border-yellow-400 rounded-xl focus:border-yellow-600 focus:ring-2 focus:ring-yellow-200 focus:outline-none transition-all"
                      required={formData.expense_method === 'actual'}
                    />
                    <div className="mt-3 p-3 bg-white rounded-lg border border-yellow-300">
                      <p className="text-sm font-semibold text-yellow-900 mb-2">⚠️ ข้อกำหนดสำคัญ:</p>
                      <ul className="text-xs text-gray-700 space-y-1">
                        <li>• ต้องมีใบเสร็จ/ใบกำกับภาษีครบถ้วน</li>
                        <li>• ต้องจัดทำบัญชีรายรับ-รายจ่าย</li>
                        <li>• อาจถูกตรวจสอบจากกรมสรรพากร</li>
                        <li>• รวม: วัตถุดิบ, ค่าเช่า, ค่าจ้าง, ค่าน้ำไฟ, ค่าเสื่อมราคา ฯลฯ</li>
                      </ul>
                    </div>
                    {formData.actual_expenses > 0 && formData.gross_income > 0 && (
                      <div className="mt-2 p-2 bg-blue-50 rounded border border-blue-300">
                        <p className="text-sm text-blue-800">
                          <span className="font-semibold">เปอร์เซ็นต์ค่าใช้จ่าย:</span> {((formData.actual_expenses / formData.gross_income) * 100).toFixed(2)}%
                          {(formData.actual_expenses / formData.gross_income) > 0.60 && (
                            <span className="ml-2 text-green-700 font-semibold">✓ สูงกว่าหักเหมา - คุ้มค่า!</span>
                          )}
                          {(formData.actual_expenses / formData.gross_income) <= 0.60 && (
                            <span className="ml-2 text-orange-700 font-semibold">⚠️ ต่ำกว่าหักเหมา - ควรพิจารณาใหม่</span>
                          )}
                        </p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>

            {/* กลุ่มครอบครัว */}
            <div className="bg-blue-50 rounded-xl p-6 border-2 border-blue-200 shadow-md">
              <h3 className="text-xl font-bold text-blue-800 mb-4 flex items-center gap-2">
                <span className="text-2xl">👨‍👩‍👧‍👦</span>
                ข้อมูลครอบครัว
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* ส่วนตัว - Disabled */}
                <div className="md:col-span-2">
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    ค่าลดหย่อนส่วนตัว
                  </label>
                  <div className="relative">
                    <input
                      type="text"
                      value="60,000 บาท"
                      disabled
                      className="w-full px-6 py-4 border-2 border-gray-200 rounded-xl bg-gray-50 text-gray-600 cursor-not-allowed"
                    />
                    <span className="absolute right-4 top-1/2 -translate-y-1/2 text-green-600 font-bold">
                      ✓ คงที่
                    </span>
                  </div>
                </div>

                {/* คู่สมรส */}
                <div className="md:col-span-2 bg-white rounded-lg p-4 border border-blue-200">
                  <label className="flex items-center gap-3 cursor-pointer">
                    <input
                      type="checkbox"
                      name="has_spouse"
                      checked={formData.has_spouse}
                      onChange={handleInputChange}
                      className="w-6 h-6 text-blue-600 border-gray-300 rounded focus:ring-blue-500 cursor-pointer"
                    />
                    <div>
                      <span className="text-base font-semibold text-gray-800">
                        มีคู่สมรสที่ไม่มีรายได้
                      </span>
                      <p className="text-sm text-gray-500">ลดหย่อนเพิ่ม 60,000 บาท</p>
                    </div>
                  </label>
                </div>

                {/* บุตร */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    จำนวนบุตร (คน)
                  </label>
                  <input
                    type="number"
                    name="number_of_children"
                    value={formData.number_of_children === 0 ? '' : formData.number_of_children}
                    onChange={handleInputChange}
                    placeholder="0"
                    min="0"
                    max="20"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    30,000 บาท/คน (ไม่จำกัดจำนวน)
                  </p>
                  {formData.number_of_children > 0 && (
                    <p className="text-sm text-blue-600 font-semibold mt-1">
                      = {(formData.number_of_children * 30000).toLocaleString()} บาท
                    </p>
                  )}
                </div>

                {/* บิดามารดา */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    จำนวนบิดามารดา (คน)
                  </label>
                  <input
                    type="number"
                    name="number_of_parents"
                    value={formData.number_of_parents === 0 ? '' : formData.number_of_parents}
                    onChange={handleInputChange}
                    placeholder="0"
                    min="0"
                    max="4"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    30,000 บาท/คน (สูงสุด 4 คน) <span className="bg-orange-200 px-1 rounded">ใหม่ 2568</span>
                  </p>
                  {formData.number_of_parents > 0 && (
                    <p className="text-sm text-blue-600 font-semibold mt-1">
                      = {(Math.min(formData.number_of_parents, 4) * 30000).toLocaleString()} บาท
                    </p>
                  )}
                </div>

                {/* คนพิการ */}
                <div className="md:col-span-2">
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    จำนวนคนพิการ/ทุพพลภาพที่อุปการะ (คน)
                  </label>
                  <input
                    type="number"
                    name="number_of_disabled"
                    value={formData.number_of_disabled === 0 ? '' : formData.number_of_disabled}
                    onChange={handleInputChange}
                    placeholder="0"
                    min="0"
                    max="10"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    60,000 บาท/คน (ไม่จำกัดจำนวน)
                  </p>
                  {formData.number_of_disabled > 0 && (
                    <p className="text-sm text-blue-600 font-semibold mt-1">
                      = {(formData.number_of_disabled * 60000).toLocaleString()} บาท
                    </p>
                  )}
                </div>
              </div>
            </div>

            {/* ประกันชีวิตและสุขภาพ */}
            <details className="bg-green-50 rounded-xl border-2 border-green-200 shadow-md group">
              <summary className="cursor-pointer p-6 font-bold text-xl text-green-800 flex items-center justify-between hover:bg-green-100 rounded-xl transition-colors">
                <span className="flex items-center gap-2">
                  <span className="text-2xl">🏥</span>
                  ประกันชีวิตและสุขภาพ
                </span>
                <span className="text-sm text-green-600 group-open:rotate-180 transition-transform">▼</span>
              </summary>
              <div className="p-6 pt-0 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    เบี้ยประกันชีวิต (บาท)
                  </label>
                  <input
                    type="number"
                    name="life_insurance"
                    value={formData.life_insurance === 0 ? '' : formData.life_insurance}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 100,000 บาท</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    ประกันชีวิตแบบบำนาญ (บาท)
                  </label>
                  <input
                    type="number"
                    name="life_insurance_pension"
                    value={formData.life_insurance_pension === 0 ? '' : formData.life_insurance_pension}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 10,000 บาท</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    เบี้ยประกันสุขภาพ (บาท)
                  </label>
                  <input
                    type="number"
                    name="health_insurance"
                    value={formData.health_insurance === 0 ? '' : formData.health_insurance}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 25,000 บาท</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    ประกันชีวิตบิดามารดา (บาท)
                  </label>
                  <input
                    type="number"
                    name="life_insurance_parents"
                    value={formData.life_insurance_parents === 0 ? '' : formData.life_insurance_parents}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 15,000 บาท/คน (รวม 60,000)</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    ประกันสุขภาพบิดามารดา (บาท)
                  </label>
                  <input
                    type="number"
                    name="health_insurance_parents"
                    value={formData.health_insurance_parents === 0 ? '' : formData.health_insurance_parents}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 15,000 บาท/คน (รวม 60,000)</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    ประกันบำนาญ (บาท)
                  </label>
                  <input
                    type="number"
                    name="pension_insurance"
                    value={formData.pension_insurance === 0 ? '' : formData.pension_insurance}
                    onChange={handleInputChange}
                    placeholder="0"
                    max={Math.min(Math.floor(formData.gross_income * 0.15), 200000)}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    สูงสุด 15% หรือ 200,000 บาท
                    {formData.gross_income > 0 && (
                      <span className="font-semibold text-orange-600">
                        {' '}(รายได้ของคุณ: สูงสุด {Math.min(Math.floor(formData.gross_income * 0.15), 200000).toLocaleString()} บาท)
                      </span>
                    )}
                  </p>
                  {formData.pension_insurance > Math.min(Math.floor(formData.gross_income * 0.15), 200000) && formData.gross_income > 0 && (
                    <p className="text-xs text-red-600 font-semibold mt-1">
                      ⚠️ เกินขีดจำกัดตามกฎหมาย! จะถูกปรับลงเป็น {Math.min(Math.floor(formData.gross_income * 0.15), 200000).toLocaleString()} บาท
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    ประกันสังคม (มาตรา 40) (บาท)
                  </label>
                  <input
                    type="number"
                    name="social_security"
                    value={formData.social_security === 0 ? '' : formData.social_security}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 9,000 บาท (หักอัตโนมัติ)</p>
                </div>
              </div>
            </details>

            {/* กองทุนและการลงทุน */}
            <details className="bg-purple-50 rounded-xl border-2 border-purple-200 shadow-md group">
              <summary className="cursor-pointer p-6 font-bold text-xl text-purple-800 flex items-center justify-between hover:bg-purple-100 rounded-xl transition-colors">
                <span className="flex items-center gap-2">
                  <span className="text-2xl">💼</span>
                  กองทุนและการลงทุนระยะยาว
                </span>
                <span className="text-sm text-purple-600 group-open:rotate-180 transition-transform">▼</span>
              </summary>
              <div className="p-6 pt-0 space-y-4">
                {/* PVD/GPF/Teacher Fund */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      กองทุนสำรองเลี้ยงชีพ (PVD)
                    </label>
                    <input
                      type="number"
                      name="provident_fund"
                      value={formData.provident_fund === 0 ? '' : formData.provident_fund}
                      onChange={handleInputChange}
                      placeholder="0"
                      className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-purple-500 focus:outline-none"
                    />
                    <p className="text-xs text-gray-500 mt-1">สูงสุด 15% หรือ 500,000</p>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      กบข. (ข้าราชการ)
                    </label>
                    <input
                      type="number"
                      name="gpf"
                      value={formData.gpf === 0 ? '' : formData.gpf}
                      onChange={handleInputChange}
                      placeholder="0"
                      className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-purple-500 focus:outline-none"
                    />
                    <p className="text-xs text-gray-500 mt-1">สูงสุด 30% หรือ 500,000</p>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      กองทุนสงเคราะห์ครูฯ
                    </label>
                    <input
                      type="number"
                      name="pvd_teacher"
                      value={formData.pvd_teacher === 0 ? '' : formData.pvd_teacher}
                      onChange={handleInputChange}
                      placeholder="0"
                      className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-purple-500 focus:outline-none"
                    />
                    <p className="text-xs text-gray-500 mt-1">สูงสุด 15% หรือ 500,000</p>
                  </div>
                </div>

                {/* RMF */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    RMF (กองทุนรวมเพื่อการเลี้ยงชีพ)
                  </label>
                  <input
                    type="number"
                    name="rmf"
                    value={formData.rmf === 0 ? '' : formData.rmf}
                    onChange={handleInputChange}
                    placeholder="0"
                    max={Math.min(Math.floor(formData.gross_income * 0.30), 500000)}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-purple-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    สูงสุด 30% หรือ 500,000 บาท (ยกเว้นภาษี 30%)
                    {formData.gross_income > 0 && (
                      <span className="font-semibold text-orange-600">
                        {' '}(รายได้ของคุณ: สูงสุด {Math.min(Math.floor(formData.gross_income * 0.30), 500000).toLocaleString()} บาท)
                      </span>
                    )}
                  </p>
                  {formData.rmf > Math.min(Math.floor(formData.gross_income * 0.30), 500000) && formData.gross_income > 0 && (
                    <p className="text-xs text-red-600 font-semibold mt-1">
                      ⚠️ เกินขีดจำกัดตามกฎหมาย! จะถูกปรับลงเป็น {Math.min(Math.floor(formData.gross_income * 0.30), 500000).toLocaleString()} บาท
                    </p>
                  )}
                </div>

                {/* ThaiESG กลุ่ม - ใหม่ 2568 */}
                <div className="bg-orange-50 border-2 border-orange-300 rounded-lg p-4">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="bg-orange-500 text-white text-xs font-bold px-3 py-1 rounded-full">
                      ใหม่ ปี 2568
                    </span>
                    <span className="font-bold text-orange-900">กลุ่ม ThaiESG (แทน SSF)</span>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-2">
                        ThaiESG
                      </label>
                      <input
                        type="number"
                        name="thai_esg"
                        value={formData.thai_esg === 0 ? '' : formData.thai_esg}
                        onChange={handleInputChange}
                        placeholder="0"
                        className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-orange-500 focus:outline-none"
                      />
                      <p className="text-xs text-gray-500 mt-1">สูงสุด 300,000 (ถือ 8 ปี)</p>
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-2">
                        ThaiESGX (เงินใหม่)
                      </label>
                      <input
                        type="number"
                        name="thai_esgx_new"
                        value={formData.thai_esgx_new === 0 ? '' : formData.thai_esgx_new}
                        onChange={handleInputChange}
                        placeholder="0"
                        className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-orange-500 focus:outline-none"
                      />
                      <p className="text-xs text-gray-500 mt-1">สูงสุด 300,000</p>
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-2">
                        ThaiESGX (จาก LTF)
                      </label>
                      <input
                        type="number"
                        name="thai_esgx_ltf"
                        value={formData.thai_esgx_ltf === 0 ? '' : formData.thai_esgx_ltf}
                        onChange={handleInputChange}
                        placeholder="0"
                        className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-orange-500 focus:outline-none"
                      />
                      <p className="text-xs text-gray-500 mt-1">สูงสุด 300,000</p>
                    </div>
                  </div>
                  <p className="text-sm text-orange-800 mt-3 bg-orange-100 p-2 rounded">
                    ⚠️ <strong>สำคัญ:</strong> SSF ยกเลิกแล้วในปี 2568 → ใช้ ThaiESG/ThaiESGX แทน
                  </p>
                </div>
              </div>
            </details>

            {/* อื่นๆ ปี 2568 */}
            <details className="bg-yellow-50 rounded-xl border-2 border-yellow-200 shadow-md group">
              <summary className="cursor-pointer p-6 font-bold text-xl text-yellow-800 flex items-center justify-between hover:bg-yellow-100 rounded-xl transition-colors">
                <span className="flex items-center gap-2">
                  <span className="text-2xl">✨</span>
                  สิทธิประโยชน์อื่นๆ (ใหม่ ปี 2568)
                </span>
                <span className="text-sm text-yellow-600 group-open:rotate-180 transition-transform">▼</span>
              </summary>
              <div className="p-6 pt-0 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    <span className="bg-green-200 px-2 py-1 rounded text-xs mr-1">ใหม่</span>
                    ลงทุนหุ้นจดทะเบียนใหม่
                  </label>
                  <input
                    type="number"
                    name="stock_investment"
                    value={formData.stock_investment === 0 ? '' : formData.stock_investment}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-yellow-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 100,000 บาท (ถือครบ 2 ปี)</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    <span className="bg-blue-200 px-2 py-1 rounded text-xs mr-1">เพิ่ม</span>
                    Easy e-Receipt
                  </label>
                  <input
                    type="number"
                    name="easy_e_receipt"
                    value={formData.easy_e_receipt === 0 ? '' : formData.easy_e_receipt}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-yellow-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    สูงสุด <strong className="text-blue-600">50,000 บาท</strong> (เพิ่มจาก 30,000)
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    ดอกเบี้ยสร้างบ้าน (2567-2568)
                  </label>
                  <input
                    type="number"
                    name="home_loan_interest"
                    value={formData.home_loan_interest === 0 ? '' : formData.home_loan_interest}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-yellow-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 100,000 บาท</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    กองทุนการออมแห่งชาติ (กอช.)
                  </label>
                  <input
                    type="number"
                    name="nsf"
                    value={formData.nsf === 0 ? '' : formData.nsf}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-yellow-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 30,000 บาท</p>
                </div>
              </div>
            </details>

            {/* เงินบริจาค */}
            <details className="bg-pink-50 rounded-xl border-2 border-pink-200 shadow-md group">
              <summary className="cursor-pointer p-6 font-bold text-xl text-pink-800 flex items-center justify-between hover:bg-pink-100 rounded-xl transition-colors">
                <span className="flex items-center gap-2">
                  <span className="text-2xl">🎁</span>
                  เงินบริจาค
                </span>
                <span className="text-sm text-pink-600 group-open:rotate-180 transition-transform">▼</span>
              </summary>
              <div className="p-6 pt-0 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    บริจาคทั่วไป
                  </label>
                  <input
                    type="number"
                    name="donation_general"
                    value={formData.donation_general === 0 ? '' : formData.donation_general}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">ลดหย่อนได้ 10% ของรายได้</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    <span className="bg-yellow-300 px-2 py-1 rounded text-xs mr-1">⭐ คุ้มสุด</span>
                    บริจาคการศึกษา
                  </label>
                  <input
                    type="number"
                    name="donation_education"
                    value={formData.donation_education === 0 ? '' : formData.donation_education}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none"
                  />
                  <p className="text-xs text-pink-600 font-semibold mt-1">
                    นับ 2 เท่า! ลดหย่อนได้ไม่จำกัด
                  </p>
                  {formData.donation_education > 0 && (
                    <p className="text-sm text-pink-600 font-semibold mt-1">
                      = ลดหย่อนได้ {(formData.donation_education * 2).toLocaleString()} บาท
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    บริจาค Social Enterprise
                  </label>
                  <input
                    type="number"
                    name="donation_social_enterprise"
                    value={formData.donation_social_enterprise === 0 ? '' : formData.donation_social_enterprise}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 100,000 บาท</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    บริจาคพรรคการเมือง
                  </label>
                  <input
                    type="number"
                    name="donation_political"
                    value={formData.donation_political === 0 ? '' : formData.donation_political}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 10,000 บาท</p>
                </div>
              </div>
            </details>

            {/* ระดับความเสี่ยง */}
            <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-6 border-2 border-indigo-300 shadow-md">
              <label className="block text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
                <span className="text-2xl">📊</span>
                ระดับความเสี่ยงที่ยอมรับได้ <span className="text-red-500">*</span>
              </label>
              <select
                name="risk_tolerance"
                value={formData.risk_tolerance}
                onChange={handleInputChange}
                className="w-full px-6 py-4 text-lg border-2 border-gray-300 rounded-xl focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none cursor-pointer"
              >
                <option value="low">🛡️ ต่ำ - ไม่ชอบเสี่ยง (เน้นประกัน, เงินฝาก)</option>
                <option value="medium">⚖️ กลาง - สมดุล (กระจายความเสี่ยง)</option>
                <option value="high">🚀 สูง - ชอบลงทุน (เน้นกองทุน, หุ้น)</option>
              </select>
              <p className="text-sm text-gray-600 mt-3 bg-white p-3 rounded-lg border border-indigo-200">
                💡 <strong>AI จะแนะนำ 3 แผนการลงทุน</strong>ตามระดับความเสี่ยงที่คุณเลือก
                เพื่อช่วยให้คุณประหยัดภาษีได้สูงสุด
              </p>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white font-bold py-6 px-8 rounded-2xl hover:from-blue-700 hover:via-indigo-700 hover:to-purple-700 transform hover:scale-[1.02] transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none shadow-2xl text-xl relative overflow-hidden group"
            >
              <span className="relative z-10 flex items-center justify-center gap-3">
                {loading ? (
                  <>
                    <svg className="animate-spin h-6 w-6" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    กำลังวิเคราะห์และสร้างแผน...
                  </>
                ) : (
                  <>
                    <span className="text-2xl">🚀</span>
                    คำนวณภาษีและรับคำแนะนำ 3 แผน (พ.ศ. 2568)
                  </>
                )}
              </span>
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent transform -skew-x-12 translate-x-[-200%] group-hover:translate-x-[200%] transition-transform duration-1000" />
            </button>
          </form>
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 text-red-700 px-6 py-4 rounded-lg mb-8 shadow-lg">
            <div className="flex items-center gap-3">
              <span className="text-2xl">❌</span>
              <div>
                <p className="font-bold">เกิดข้อผิดพลาด</p>
                <p className="text-sm">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="space-y-8">
            {/* Tax Result */}
            <div className="bg-white rounded-2xl shadow-2xl p-8 border-t-4 border-green-500">
              <h2 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-3">
                <span className="text-4xl">💰</span>
                ผลการคำนวณภาษี (พ.ศ. 2568)
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-6 border-2 border-blue-200 shadow-md">
                  <p className="text-sm text-gray-600 mb-2 font-semibold">รายได้รวม</p>
                  <p className="text-3xl font-bold text-blue-600">
                    {result.tax_result.gross_income.toLocaleString()}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">บาท/ปี</p>
                </div>
                <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-6 border-2 border-purple-200 shadow-md">
                  <p className="text-sm text-gray-600 mb-2 font-semibold">เงินได้สุทธิ</p>
                  <p className="text-3xl font-bold text-purple-600">
                    {result.tax_result.taxable_income.toLocaleString()}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">หลังหักค่าลดหย่อน</p>
                </div>
                <div className="bg-gradient-to-br from-red-50 to-red-100 rounded-xl p-6 border-2 border-red-200 shadow-md">
                  <p className="text-sm text-gray-600 mb-2 font-semibold">ภาษีที่ต้องจ่าย</p>
                  <p className="text-3xl font-bold text-red-600">
                    {result.tax_result.tax_amount.toLocaleString()}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">บาท</p>
                </div>
                <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-6 border-2 border-green-200 shadow-md">
                  <p className="text-sm text-gray-600 mb-2 font-semibold">อัตราภาษีเฉลี่ย</p>
                  <p className="text-3xl font-bold text-green-600">
                    {result.tax_result.effective_tax_rate.toFixed(2)}%
                  </p>
                  <p className="text-xs text-gray-500 mt-1">ของรายได้</p>
                </div>
              </div>
            </div>

            {/* ✅ กรณีไม่ต้องจ่ายภาษี */}
            {result.no_tax_required && (
              <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-2xl shadow-2xl p-12 border-4 border-green-400">
                <div className="text-center">
                  <div className="text-8xl mb-6">🎉</div>
                  <h2 className="text-4xl font-bold text-green-800 mb-4">
                    ยินดีด้วย! คุณไม่ต้องจ่ายภาษี
                  </h2>
                  <p className="text-xl text-gray-700 mb-8">
                    เงินได้สุทธิของคุณอยู่ในเกณฑ์ยกเว้นภาษี (ไม่เกิน 150,000 บาท)
                  </p>
                  <div className="bg-white rounded-2xl p-8 inline-block shadow-lg">
                    <div className="grid grid-cols-2 gap-8 text-left">
                      <div>
                        <p className="text-sm text-gray-600 mb-1">รายได้รวม</p>
                        <p className="text-2xl font-bold text-gray-800">
                          {result.tax_result.gross_income.toLocaleString()} บาท
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600 mb-1">เงินได้สุทธิ</p>
                        <p className="text-2xl font-bold text-gray-800">
                          {result.tax_result.taxable_income.toLocaleString()} บาท
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="mt-8 p-6 bg-blue-50 rounded-xl border-2 border-blue-200">
                    <p className="text-gray-700">
                      💡 <strong>หมายเหตุ:</strong> หากต้องการวางแผนภาษีเพิ่มเติม
                      คุณสามารถเพิ่มรายได้หรือลดค่าลดหย่อนเพื่อดูแผนการลงทุนจาก AI
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* ✅ กรณีต้องจ่ายภาษี - แสดงแผนการลงทุน */}
            {!result.no_tax_required && result.investment_plans && result.investment_plans.plans.length > 0 && (
              <MultiplePlansView plans={result.investment_plans.plans} />
            )}
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-16 pb-8">
          <div className="bg-gradient-to-r from-gray-100 to-gray-200 rounded-2xl p-8 shadow-lg">
            <p className="text-gray-700 font-semibold text-lg mb-2">
              AI Tax Advisor - Version 5.0
            </p>
            <p className="text-gray-600 mb-4">
              ระบบที่ปรึกษาภาษีอัจฉริยะ | อัปเดตตามกฎหมายภาษี พ.ศ. 2568
            </p>
            <div className="flex flex-wrap justify-center gap-3 text-sm text-gray-600">
              <div className="flex items-center gap-1">
                <span>✅</span>
                <span>ยกเลิก SSF</span>
              </div>
              <div className="flex items-center gap-1">
                <span>✅</span>
                <span>เพิ่ม ThaiESG/ThaiESGX</span>
              </div>
              <div className="flex items-center gap-1">
                <span>✅</span>
                <span>Easy e-Receipt 50,000</span>
              </div>
              <div className="flex items-center gap-1">
                <span>✅</span>
                <span>ค่าอุปการะบิดามารดา 120,000</span>
              </div>
              <div className="flex items-center gap-1">
                <span>✅</span>
                <span>ลงทุนหุ้นใหม่ 100,000</span>
              </div>
            </div>
            <p className="text-xs text-gray-500 mt-4">
              💡 ข้อมูลทั้งหมดอ้างอิงจากกฎหมายภาษีเงินได้บุคคลธรรมดา พ.ศ. 2568
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
