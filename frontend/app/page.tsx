'use client';

import { useState } from 'react';
import { Calculator, TrendingUp, Shield, Info } from 'lucide-react';
import {
  TaxCalculationRequest,
  TaxOptimizationResponse,
  INCOME_FIELDS,
  BASIC_DEDUCTION_FIELDS,
  INVESTMENT_DEDUCTION_FIELDS,
  FormField
} from '@/lib/types';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

export default function Home() {
  const [formData, setFormData] = useState<TaxCalculationRequest>({
    salary: 0,
    bonus: 0,
    personal_allowance: 60000,
    spouse_allowance: 0,
    child_allowance: 0,
    social_security: 0,
    life_insurance: 0,
    health_insurance: 0,
    provident_fund: 0,
    rmf: 0,
    ssf: 0,
    pension_insurance: 0,
    donation: 0,
    risk_tolerance: 'medium'
  });

  const [result, setResult] = useState<TaxOptimizationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (name: keyof TaxCalculationRequest, value: string | number) => {
    setFormData(prev => ({
      ...prev,
      [name]: typeof value === 'string' ? parseFloat(value) || 0 : value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
  
    console.log("📤 Sending request:", formData); // เพิ่มบรรทัดนี้
  
  try {
    const response = await fetch('http://localhost:8000/api/calculate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData)
    });

    console.log("📡 Response status:", response.status); // เพิ่มบรรทัดนี้

    if (!response.ok) {
      throw new Error('เกิดข้อผิดพลาดในการคำนวณ');
    }

    const data: TaxOptimizationResponse = await response.json();
    console.log("📊 Response data:", data); // เพิ่มบรรทัดนี้
    console.log("📊 Recommendations length:", data.recommendations.length); // เพิ่มบรรทัดนี้
    
    setResult(data);
    console.log("✅ Result state updated"); // เพิ่มบรรทัดนี้
  } catch (err) {
    console.error("❌ Error:", err); // เพิ่มบรรทัดนี้
    setError(err instanceof Error ? err.message : 'เกิดข้อผิดพลาด');
  } finally {
    setLoading(false);
  }
};

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('th-TH', {
      style: 'currency',
      currency: 'THB',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  const renderInputField = (field: FormField) => (
    <div key={field.name} className="space-y-2">
      <label className="block text-sm font-medium text-gray-700">
        {field.label}
        {field.info && (
          <span className="ml-2 text-xs text-gray-500">({field.info})</span>
        )}
      </label>
      <input
        type="number"
        value={formData[field.name] || ''}
        onChange={(e) => handleInputChange(field.name, e.target.value)}
        placeholder={field.placeholder}
        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        max={field.max}
      />
    </div>
  );

  const chartData = result ? [
    { name: 'ภาษีที่จ่าย', value: result.current_tax.tax_amount, color: '#ef4444' },
    { name: 'รายได้สุทธิ', value: result.current_tax.net_income, color: '#22c55e' }
  ] : [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center gap-3">
            <Calculator className="w-8 h-8 text-blue-600" />
            <div>
              <h1 className="text-3xl font-bold text-gray-900">AI Tax Advisor</h1>
              <p className="text-sm text-gray-600">ผู้ช่วยวางแผนภาษีอัจฉริยะ</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Section */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">กรอกข้อมูลรายได้</h2>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* รายได้ */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-green-600" />
                  รายได้
                </h3>
                {INCOME_FIELDS.map(renderInputField)}
              </div>

              {/* ค่าลดหย่อนพื้นฐาน */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
                  <Shield className="w-5 h-5 text-blue-600" />
                  ค่าลดหย่อนพื้นฐาน
                </h3>
                {BASIC_DEDUCTION_FIELDS.map(renderInputField)}
              </div>

              {/* ค่าลดหย่อนจากการลงทุน */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
                  <Info className="w-5 h-5 text-purple-600" />
                  ค่าลดหย่อนจากการลงทุน
                </h3>
                {INVESTMENT_DEDUCTION_FIELDS.map(renderInputField)}
              </div>

              {/* ระดับความเสี่ยง */}
              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">
                  ระดับความเสี่ยงที่รับได้
                </label>
                <select
                  value={formData.risk_tolerance}
                  onChange={(e) => handleInputChange('risk_tolerance', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="low">ต่ำ - ต้องการความปลอดภัย</option>
                  <option value="medium">กลาง - สมดุลระหว่างความเสี่ยงและผลตอบแทน</option>
                  <option value="high">สูง - ต้องการผลตอบแทนสูง</option>
                </select>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                {loading ? 'กำลังคำนวณ...' : 'คำนวณภาษีและแนะนำ'}
              </button>
            </form>
          </div>

          {/* Results Section */}
          <div className="space-y-6">
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-red-800">{error}</p>
              </div>
            )}
            {result && (
              <>
                {/* Tax Summary */}
                <div className="bg-white rounded-xl shadow-lg p-6">
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">สรุปภาษี</h2>
                  
                  <div className="space-y-3">
                    <div className="flex justify-between items-center pb-2 border-b">
                      <span className="text-gray-600">รายได้รวม</span>
                      <span className="font-semibold">{formatCurrency(result.current_tax.gross_income)}</span>
                    </div>
                    <div className="flex justify-between items-center pb-2 border-b">
                      <span className="text-gray-600">ค่าลดหย่อนทั้งหมด</span>
                      <span className="font-semibold text-green-600">-{formatCurrency(result.current_tax.total_deductions)}</span>
                    </div>
                    <div className="flex justify-between items-center pb-2 border-b">
                      <span className="text-gray-600">เงินได้สุทธิ</span>
                      <span className="font-semibold">{formatCurrency(result.current_tax.taxable_income)}</span>
                    </div>
                    <div className="flex justify-between items-center pb-2 border-b border-red-200 bg-red-50 p-3 rounded-lg">
                      <span className="text-red-600 font-semibold">ภาษีที่ต้องจ่าย</span>
                      <span className="text-2xl font-bold text-red-600">{formatCurrency(result.current_tax.tax_amount)}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">อัตราภาษีเฉลี่ย</span>
                      <span className="font-semibold text-blue-600">{result.current_tax.effective_tax_rate}%</span>
                    </div>
                  </div>

                  {/* Pie Chart */}
                  {chartData.length > 0 && (
                    <div className="mt-6 h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={chartData}
                            cx="50%"
                            cy="50%"
                            labelLine={false}
                            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                            outerRadius={80}
                            fill="#8884d8"
                            dataKey="value"
                          >
                            {chartData.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                          </Pie>
                          <Tooltip formatter={(value: number) => formatCurrency(value)} />
                          <Legend />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  )}
                </div>

                {/* AI Recommendations */}
                {result.recommendations.length > 0 && (
                  <div className="bg-white rounded-xl shadow-lg p-6">
                    <h2 className="text-2xl font-bold text-gray-900 mb-4">💡 คำแนะนำจาก AI</h2>
                    
                    <div className="bg-blue-50 rounded-lg p-4 mb-6">
                      <p className="text-gray-700 whitespace-pre-line">{result.summary}</p>
                    </div>

                    <div className="space-y-4">
                      {result.recommendations.map((rec, index) => (
                        <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                          <div className="flex items-start justify-between mb-3">
                            <h3 className="text-lg font-semibold text-gray-900">{rec.strategy}</h3>
                            <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                              rec.risk_level === 'low' ? 'bg-green-100 text-green-800' :
                              rec.risk_level === 'high' ? 'bg-red-100 text-red-800' :
                              'bg-yellow-100 text-yellow-800'
                            }`}>
                              {rec.risk_level === 'low' ? 'ความเสี่ยงต่ำ' :
                               rec.risk_level === 'high' ? 'ความเสี่ยงสูง' : 'ความเสี่ยงกลาง'}
                            </span>
                          </div>

                          <p className="text-gray-600 mb-4">{rec.description}</p>

                          <div className="grid grid-cols-2 gap-4 mb-4">
                            <div className="bg-green-50 rounded-lg p-3">
                              <p className="text-xs text-gray-600">ลงทุน</p>
                              <p className="text-lg font-bold text-green-600">{formatCurrency(rec.investment_amount)}</p>
                            </div>
                            <div className="bg-blue-50 rounded-lg p-3">
                              <p className="text-xs text-gray-600">ประหยัดภาษี</p>
                              <p className="text-lg font-bold text-blue-600">{formatCurrency(rec.tax_saving)}</p>
                            </div>
                          </div>

                          {rec.expected_return_1y && (
                            <div className="mb-4">
                              <p className="text-sm font-medium text-gray-700 mb-2">ผลตอบแทนคาดการณ์:</p>
                              <div className="flex gap-2">
                                <span className="text-xs bg-gray-100 px-2 py-1 rounded">1ปี: {rec.expected_return_1y}%</span>
                                {rec.expected_return_3y && <span className="text-xs bg-gray-100 px-2 py-1 rounded">3ปี: {rec.expected_return_3y}%</span>}
                                {rec.expected_return_5y && <span className="text-xs bg-gray-100 px-2 py-1 rounded">5ปี: {rec.expected_return_5y}%</span>}
                              </div>
                            </div>
                          )}

                          <div className="grid grid-cols-2 gap-4 text-sm">
                            <div>
                              <p className="font-medium text-green-600 mb-1">✓ ข้อดี</p>
                              <ul className="list-disc list-inside space-y-1 text-gray-600">
                                {rec.pros.map((pro, i) => <li key={i}>{pro}</li>)}
                              </ul>
                            </div>
                            <div>
                              <p className="font-medium text-red-600 mb-1">✗ ข้อเสีย</p>
                              <ul className="list-disc list-inside space-y-1 text-gray-600">
                                {rec.cons.map((con, i) => <li key={i}>{con}</li>)}
                              </ul>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>

                    <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                      <p className="text-sm text-yellow-800">{result.disclaimer}</p>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}