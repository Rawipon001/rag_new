'use client';

import React, { useState } from 'react';
import MultiplePlansView from './components/MultiplePlansView';

export default function Home() {
  const [formData, setFormData] = useState({
    // รายได้
    gross_income: 600000,
    
    // กลุ่มส่วนตัว/ครอบครัว
    personal_deduction: 60000, // ค่าคงที่ ไม่ให้แก้
    spouse_deduction: 0,
    child_deduction: 0,
    parent_support: 0,
    disabled_support: 0,
    
    // กลุ่มประกันและการลงทุน
    life_insurance: 0,
    life_insurance_parents: 0,
    health_insurance: 0,
    health_insurance_parents: 0,
    pension_insurance: 0,
    provident_fund: 0,
    gpf: 0,
    pvd: 0,
    rmf: 0,
    ssf: 0,
    
    // กลุ่มกระตุ้นเศรษฐกิจ
    shopping_deduction: 0,
    otop_deduction: 0,
    travel_deduction: 0,
    
    // กลุ่มเงินบริจาค
    donation_general: 0,
    donation_education: 0,
    donation_political: 0,
    
    risk_tolerance: 'medium',
  });

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    
    if (name === 'risk_tolerance') {
      setFormData((prev) => ({
        ...prev,
        [name]: value,
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

    try {
      const response = await fetch('http://localhost:8000/api/calculate-tax', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'เกิดข้อผิดพลาด');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            🏦 AI Tax Advisor
          </h1>
          <p className="text-lg text-gray-600">
            ระบบแนะนำการวางแผนภาษี - ได้หลายแผนการลงทุนพร้อมเปรียบเทียบ
          </p>
        </div>

        {/* Form */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            📝 กรอกข้อมูลรายได้และค่าลดหย่อน
          </h2>

          <form onSubmit={handleCalculate} className="space-y-8">
            {/* รายได้ */}
            <div className="bg-orange-50 rounded-xl p-6 border-2 border-orange-200">
              <h3 className="text-xl font-bold text-orange-800 mb-4">รายได้</h3>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  รายได้รวมต่อปี (บาท) *
                </label>
                <input
                  type="number"
                  name="gross_income"
                  value={formData.gross_income === 0 ? '' : formData.gross_income}
                  onChange={handleInputChange}
                  placeholder="กรอกรายได้"
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-orange-500 focus:outline-none"
                  required
                />
              </div>
            </div>

            {/* กลุ่มลดหย่อนส่วนตัว/ครอบครัว */}
            <div className="bg-blue-50 rounded-xl p-6 border-2 border-blue-200">
              <h3 className="text-xl font-bold text-blue-800 mb-4">
                👨‍👩‍👧‍👦 กลุ่มลดหย่อนส่วนตัว/ครอบครัว
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* ค่าลดหย่อนส่วนตัว - DISABLED */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    ค่าลดหย่อนส่วนตัว (บาท)
                  </label>
                  <input
                    type="number"
                    name="personal_deduction"
                    value={formData.personal_deduction}
                    disabled
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg bg-gray-100 cursor-not-allowed"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    ⚠️ ค่าคงที่ 60,000 บาท (ไม่สามารถแก้ไขได้)
                  </p>
                </div>
                
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    ค่าลดหย่อนคู่สมรส (บาท)
                  </label>
                  <input
                    type="number"
                    name="spouse_deduction"
                    value={formData.spouse_deduction === 0 ? '' : formData.spouse_deduction}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">คู่สมรสไม่มีรายได้ 60,000 บาท</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    ค่าเลี้ยงดูบุตร (บาท)
                  </label>
                  <input
                    type="number"
                    name="child_deduction"
                    value={formData.child_deduction === 0 ? '' : formData.child_deduction}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">คนละ 30,000 บาท (สูงสุด 3 คน)</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    ค่าอุปการะบิดามารดา (บาท)
                  </label>
                  <input
                    type="number"
                    name="parent_support"
                    value={formData.parent_support === 0 ? '' : formData.parent_support}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">คนละ 30,000 บาท (สูงสุด 2 คน)</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    ค่าอุปการะคนพิการ (บาท)
                  </label>
                  <input
                    type="number"
                    name="disabled_support"
                    value={formData.disabled_support === 0 ? '' : formData.disabled_support}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">คนละ 60,000 บาท</p>
                </div>
              </div>
            </div>

            {/* กลุ่มประกันชีวิตและการลงทุน */}
            <div className="bg-green-50 rounded-xl p-6 border-2 border-green-200">
              <h3 className="text-xl font-bold text-green-800 mb-4">
                🏦 กลุ่มประกันชีวิตและการลงทุน
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 15,000 บาท</p>
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
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 15,000 บาท</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    กองทุนสำรองเลี้ยงชีพ (บาท)
                  </label>
                  <input
                    type="number"
                    name="provident_fund"
                    value={formData.provident_fund === 0 ? '' : formData.provident_fund}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 15% หรือ 500,000 บาท</p>
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
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 15% หรือ 200,000 บาท</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    RMF (บาท)
                  </label>
                  <input
                    type="number"
                    name="rmf"
                    value={formData.rmf === 0 ? '' : formData.rmf}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 30% หรือ 500,000 บาท</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    SSF (บาท)
                  </label>
                  <input
                    type="number"
                    name="ssf"
                    value={formData.ssf === 0 ? '' : formData.ssf}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 30% หรือ 200,000 บาท</p>
                </div>
              </div>
            </div>

            {/* กลุ่มกระตุ้นเศรษฐกิจ */}
            <div className="bg-purple-50 rounded-xl p-6 border-2 border-purple-200">
              <h3 className="text-xl font-bold text-purple-800 mb-4">
                💳 กลุ่มกระตุ้นเศรษฐกิจ
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    ช้อปช่วยชาติ (บาท)
                  </label>
                  <input
                    type="number"
                    name="shopping_deduction"
                    value={formData.shopping_deduction === 0 ? '' : formData.shopping_deduction}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-purple-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 30,000 บาท</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    ซื้อ OTOP (บาท)
                  </label>
                  <input
                    type="number"
                    name="otop_deduction"
                    value={formData.otop_deduction === 0 ? '' : formData.otop_deduction}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-purple-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 50,000 บาท</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    ท่องเที่ยวในประเทศ (บาท)
                  </label>
                  <input
                    type="number"
                    name="travel_deduction"
                    value={formData.travel_deduction === 0 ? '' : formData.travel_deduction}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-purple-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">สูงสุด 30,000 บาท</p>
                </div>
              </div>
            </div>

            {/* กลุ่มเงินบริจาค */}
            <div className="bg-pink-50 rounded-xl p-6 border-2 border-pink-200">
              <h3 className="text-xl font-bold text-pink-800 mb-4">
                🎁 กลุ่มเงินบริจาค
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    บริจาคทั่วไป (บาท)
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
                    บริจาคการศึกษา (บาท)
                  </label>
                  <input
                    type="number"
                    name="donation_education"
                    value={formData.donation_education === 0 ? '' : formData.donation_education}
                    onChange={handleInputChange}
                    placeholder="0"
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">นับ 2 เท่า</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    บริจาคพรรคการเมือง (บาท)
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
            </div>

            {/* ระดับความเสี่ยง */}
            <div className="bg-yellow-50 rounded-xl p-6 border-2 border-yellow-200">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                📊 ระดับความเสี่ยงที่ยอมรับได้ *
              </label>
              <select
                name="risk_tolerance"
                value={formData.risk_tolerance}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-yellow-500 focus:outline-none text-lg"
              >
                <option value="low">🛡️ ต่ำ - ไม่ชอบเสี่ยง (เน้นประกัน)</option>
                <option value="medium">⚖️ กลาง - สมดุล (กระจายความเสี่ยง)</option>
                <option value="high">🚀 สูง - ชอบลงทุน (เน้นกองทุน)</option>
              </select>
              <p className="text-xs text-gray-600 mt-2">
                ⚠️ AI จะแนะนำแผนการลงทุนตามระดับความเสี่ยงที่คุณเลือก
              </p>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold py-4 rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all disabled:opacity-50 shadow-lg text-lg"
            >
              {loading ? '⏳ กำลังวิเคราะห์และสร้างแผน...' : '🚀 คำนวณภาษีและรับคำแนะนำ 3 แผน'}
            </button>
          </form>
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-50 border-2 border-red-500 text-red-700 px-6 py-4 rounded-lg mb-8">
            <p className="font-semibold">❌ เกิดข้อผิดพลาด:</p>
            <p>{error}</p>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="space-y-8">
            {/* Tax Result */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">
                💰 ผลการคำนวณภาษี
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="bg-blue-50 rounded-lg p-4">
                  <p className="text-sm text-gray-600 mb-1">รายได้รวม</p>
                  <p className="text-2xl font-bold text-blue-600">
                    {result.tax_result.gross_income.toLocaleString()} ฿
                  </p>
                </div>
                <div className="bg-purple-50 rounded-lg p-4">
                  <p className="text-sm text-gray-600 mb-1">เงินได้สุทธิ</p>
                  <p className="text-2xl font-bold text-purple-600">
                    {result.tax_result.taxable_income.toLocaleString()} ฿
                  </p>
                </div>
                <div className="bg-red-50 rounded-lg p-4">
                  <p className="text-sm text-gray-600 mb-1">ภาษีที่ต้องจ่าย</p>
                  <p className="text-2xl font-bold text-red-600">
                    {result.tax_result.tax_amount.toLocaleString()} ฿
                  </p>
                </div>
                <div className="bg-green-50 rounded-lg p-4">
                  <p className="text-sm text-gray-600 mb-1">อัตราภาษีเฉลี่ย</p>
                  <p className="text-2xl font-bold text-green-600">
                    {result.tax_result.effective_tax_rate.toFixed(2)}%
                  </p>
                </div>
              </div>
            </div>

            {/* Multiple Plans */}
            <MultiplePlansView plans={result.investment_plans.plans} />
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 text-gray-600">
          <p>Powered by AI Tax Advisor | Version 3.0 Risk-Aware + Insurance Required</p>
        </div>
      </div>
    </main>
  );
}