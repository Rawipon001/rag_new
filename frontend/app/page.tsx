'use client';

import { useState } from 'react';
import { Calculator, TrendingUp, Shield, Wallet, Gift, PiggyBank, Info } from 'lucide-react';
import {
  SimplifiedFormData,
  TaxOptimizationResponse,
  convertToApiRequest
} from '@/lib/types';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';

export default function Home() {
  const [formData, setFormData] = useState<SimplifiedFormData>({
    // รายได้
    salary: 0,
    bonus: 0,
    
    // ครอบครัว
    hasSpouse: false,
    numberOfChildren: 0,
    
    // ประกันสังคม
    hasSocialSecurity: false,
    socialSecurityAmount: 0,
    
    // ประกัน
    hasLifeInsurance: false,
    lifeInsuranceAmount: 0,
    hasHealthInsurance: false,
    healthInsuranceAmount: 0,
    hasPensionInsurance: false,
    pensionInsuranceAmount: 0,
    
    // Easy e-Receipt
    easyEReceiptAmount: 0,
    
    // เงินบริจาค
    donationAmount: 0,
    
    // การลงทุน
    hasProvidentFund: false,
    providentFundAmount: 0,
    hasRMF: false,
    rmfAmount: 0,
    hasSSF: false,
    ssfAmount: 0,
    
    risk_tolerance: 'medium'
  });

  const [result, setResult] = useState<TaxOptimizationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
  
    // แปลง SimplifiedFormData เป็น TaxCalculationRequest
    const apiRequest = convertToApiRequest(formData);
    console.log("📤 Sending request:", apiRequest);
  
    try {
      const response = await fetch('http://localhost:8000/api/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(apiRequest)
      });

      if (!response.ok) {
        throw new Error('เกิดข้อผิดพลาดในการคำนวณ');
      }

      const data: TaxOptimizationResponse = await response.json();
      setResult(data);
    } catch (err) {
      console.error("❌ Error:", err);
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

  const chartData = result ? [
    { name: 'ภาษีที่จ่าย', value: result.current_tax.tax_amount, color: '#ef4444' },
    { name: 'รายได้สุทธิ', value: result.current_tax.net_income, color: '#22c55e' }
  ] : [];

  const returnChartData = result?.recommendations.map(rec => ({
    name: rec.strategy.substring(0, 20) + '...',
    '1 ปี': rec.expected_return_1y || 0,
    '3 ปี': rec.expected_return_3y || 0,
    '5 ปี': rec.expected_return_5y || 0,
  })) || [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center gap-3">
            <Calculator className="w-8 h-8 text-blue-600" />
            <div>
              <h1 className="text-3xl font-bold text-gray-900">AI Tax Advisor</h1>
              <p className="text-sm text-gray-600">ผู้ช่วยวางแผนภาษีอัจฉริยะ - ปี 2568</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Section */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">กรอกข้อมูลรายได้และค่าลดหย่อน</h2>
            
            <form onSubmit={handleSubmit} className="space-y-8">
              {/* 1. รายได้ */}
              <div className="space-y-4 p-4 bg-orange-50 rounded-lg border-2 border-orange-200">
                <h3 className="text-lg font-bold text-orange-800 flex items-center gap-2">
                  <TrendingUp className="w-5 h-5" />
                  รายได้
                </h3>
                
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">
                    เงินเดือนรายปี (บาท)
                  </label>
                  <input
                    type="number"
                    value={formData.salary || ''}
                    onChange={(e) => setFormData({...formData, salary: parseFloat(e.target.value) || 0})}
                    placeholder="เช่น 600,000"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500"
                  />
                </div>

                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">
                    โบนัสและรายได้อื่นๆ รายปี (บาท)
                  </label>
                  <input
                    type="number"
                    value={formData.bonus || ''}
                    onChange={(e) => setFormData({...formData, bonus: parseFloat(e.target.value) || 0})}
                    placeholder="เช่น 100,000"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500"
                  />
                </div>
              </div>

              {/* 2. ค่าลดหย่อนส่วนตัว/ครอบครัว */}
              <div className="space-y-4 p-4 bg-blue-50 rounded-lg border-2 border-blue-200">
                <h3 className="text-lg font-bold text-blue-800 flex items-center gap-2">
                  <Shield className="w-5 h-5" />
                  กลุ่มลดหย่อนส่วนตัว/ครอบครัว
                </h3>

                {/* ส่วนตัว - แสดงอัตโนมัติ */}
                <div className="bg-blue-100 p-3 rounded-lg">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium text-blue-900">ค่าลดหย่อนส่วนตัว</span>
                    <span className="text-lg font-bold text-blue-900">60,000 บาท</span>
                  </div>
                  <p className="text-xs text-blue-700 mt-1">✓ คำนวณให้อัตโนมัติ</p>
                </div>

                {/* คู่สมรส */}
                <div className="space-y-2">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.hasSpouse}
                      onChange={(e) => setFormData({...formData, hasSpouse: e.target.checked})}
                      className="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                    />
                    <span className="text-sm font-medium text-gray-700">
                      มีคู่สมรส (ไม่มีรายได้)
                      {formData.hasSpouse && <span className="ml-2 text-blue-600 font-bold">+60,000 บาท</span>}
                    </span>
                  </label>
                </div>

                {/* บุตร */}
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">
                    จำนวนบุตร (คน)
                  </label>
                  <input
                    type="number"
                    min="0"
                    max="10"
                    value={formData.numberOfChildren}
                    onChange={(e) => setFormData({...formData, numberOfChildren: parseInt(e.target.value) || 0})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                  {formData.numberOfChildren > 0 && (
                    <p className="text-sm text-blue-600">
                      ลดหย่อน: <span className="font-bold">{formatCurrency(formData.numberOfChildren * 30000)}</span>
                    </p>
                  )}
                </div>

                {/* ประกันสังคม */}
                <div className="space-y-2">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.hasSocialSecurity}
                      onChange={(e) => setFormData({...formData, hasSocialSecurity: e.target.checked})}
                      className="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                    />
                    <span className="text-sm font-medium text-gray-700">จ่ายประกันสังคม</span>
                  </label>
                  {formData.hasSocialSecurity && (
                    <input
                      type="number"
                      value={formData.socialSecurityAmount || ''}
                      onChange={(e) => setFormData({...formData, socialSecurityAmount: parseFloat(e.target.value) || 0})}
                      placeholder="จำนวนเงิน (สูงสุด 9,000)"
                      max="9000"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    />
                  )}
                </div>
              </div>

              {/* 3. กลุ่มประกันชีวิตและสุขภาพ */}
              <div className="space-y-4 p-4 bg-green-50 rounded-lg border-2 border-green-200">
                <h3 className="text-lg font-bold text-green-800 flex items-center gap-2">
                  <Shield className="w-5 h-5" />
                  กลุ่มประกันชีวิตและการลงทุน
                </h3>

                {/* ประกันชีวิต */}
                <div className="space-y-2">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.hasLifeInsurance}
                      onChange={(e) => setFormData({...formData, hasLifeInsurance: e.target.checked})}
                      className="w-5 h-5 text-green-600 rounded"
                    />
                    <span className="text-sm font-medium text-gray-700">ประกันชีวิต</span>
                  </label>
                  {formData.hasLifeInsurance && (
                    <div>
                      <input
                        type="number"
                        value={formData.lifeInsuranceAmount || ''}
                        onChange={(e) => setFormData({...formData, lifeInsuranceAmount: parseFloat(e.target.value) || 0})}
                        placeholder="จำนวนเงิน (สูงสุด 100,000)"
                        max="100000"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                      />
                      <p className="text-xs text-green-600 mt-1">ลดหย่อนได้สูงสุด 100,000 บาท</p>
                    </div>
                  )}
                </div>

                {/* ประกันสุขภาพ */}
                <div className="space-y-2">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.hasHealthInsurance}
                      onChange={(e) => setFormData({...formData, hasHealthInsurance: e.target.checked})}
                      className="w-5 h-5 text-green-600 rounded"
                    />
                    <span className="text-sm font-medium text-gray-700">ประกันสุขภาพ</span>
                  </label>
                  {formData.hasHealthInsurance && (
                    <div>
                      <input
                        type="number"
                        value={formData.healthInsuranceAmount || ''}
                        onChange={(e) => setFormData({...formData, healthInsuranceAmount: parseFloat(e.target.value) || 0})}
                        placeholder="จำนวนเงิน (สูงสุด 25,000)"
                        max="25000"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                      />
                      <p className="text-xs text-green-600 mt-1">ลดหย่อนได้สูงสุด 25,000 บาท</p>
                    </div>
                  )}
                </div>

                {/* ประกันบำนาญ */}
                <div className="space-y-2">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.hasPensionInsurance}
                      onChange={(e) => setFormData({...formData, hasPensionInsurance: e.target.checked})}
                      className="w-5 h-5 text-green-600 rounded"
                    />
                    <span className="text-sm font-medium text-gray-700">ประกันบำนาญ</span>
                  </label>
                  {formData.hasPensionInsurance && (
                    <div>
                      <input
                        type="number"
                        value={formData.pensionInsuranceAmount || ''}
                        onChange={(e) => setFormData({...formData, pensionInsuranceAmount: parseFloat(e.target.value) || 0})}
                        placeholder="จำนวนเงิน (สูงสุด 15% หรือ 200,000)"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                      />
                      <p className="text-xs text-green-600 mt-1">ลดหย่อนได้สูงสุด 15% ของรายได้ หรือ 200,000 บาท</p>
                    </div>
                  )}
                </div>
              </div>

              {/* 4. กลุ่มการลงทุนระยะยาว */}
              <div className="space-y-4 p-4 bg-purple-50 rounded-lg border-2 border-purple-200">
                <h3 className="text-lg font-bold text-purple-800 flex items-center gap-2">
                  <PiggyBank className="w-5 h-5" />
                  กลุ่มการลงทุน
                </h3>

                {/* กองทุนสำรองเลี้ยงชีพ */}
                <div className="space-y-2">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.hasProvidentFund}
                      onChange={(e) => setFormData({...formData, hasProvidentFund: e.target.checked})}
                      className="w-5 h-5 text-purple-600 rounded"
                    />
                    <span className="text-sm font-medium text-gray-700">กองทุนสำรองเลี้ยงชีพ (PVD)</span>
                  </label>
                  {formData.hasProvidentFund && (
                    <div>
                      <input
                        type="number"
                        value={formData.providentFundAmount || ''}
                        onChange={(e) => setFormData({...formData, providentFundAmount: parseFloat(e.target.value) || 0})}
                        placeholder="ลงทุนไปเท่าไหร่ต่อปี"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                      />
                      <p className="text-xs text-purple-600 mt-1">ลดหย่อนได้สูงสุด 15% ของเงินเดือน หรือ 500,000 บาท</p>
                    </div>
                  )}
                </div>

                {/* RMF */}
                <div className="space-y-2">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.hasRMF}
                      onChange={(e) => setFormData({...formData, hasRMF: e.target.checked})}
                      className="w-5 h-5 text-purple-600 rounded"
                    />
                    <span className="text-sm font-medium text-gray-700">กองทุน RMF</span>
                  </label>
                  {formData.hasRMF && (
                    <div>
                      <input
                        type="number"
                        value={formData.rmfAmount || ''}
                        onChange={(e) => setFormData({...formData, rmfAmount: parseFloat(e.target.value) || 0})}
                        placeholder="ลงทุนไปเท่าไหร่ต่อปี"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                      />
                      <p className="text-xs text-purple-600 mt-1">ลดหย่อนได้สูงสุด 30% ของรายได้ หรือ 500,000 บาท</p>
                    </div>
                  )}
                </div>

                {/* SSF */}
                <div className="space-y-2">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.hasSSF}
                      onChange={(e) => setFormData({...formData, hasSSF: e.target.checked})}
                      className="w-5 h-5 text-purple-600 rounded"
                    />
                    <span className="text-sm font-medium text-gray-700">กองทุน SSF</span>
                  </label>
                  {formData.hasSSF && (
                    <div>
                      <input
                        type="number"
                        value={formData.ssfAmount || ''}
                        onChange={(e) => setFormData({...formData, ssfAmount: parseFloat(e.target.value) || 0})}
                        placeholder="ลงทุนไปเท่าไหร่ต่อปี"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                      />
                      <p className="text-xs text-purple-600 mt-1">ลดหย่อนได้สูงสุด 30% ของรายได้ หรือ 200,000 บาท</p>
                    </div>
                  )}
                </div>
              </div>

              {/* 5. กลุ่มเงินบริจาค */}
              <div className="space-y-4 p-4 bg-yellow-50 rounded-lg border-2 border-yellow-200">
                <h3 className="text-lg font-bold text-yellow-800 flex items-center gap-2">
                  <Gift className="w-5 h-5" />
                  กลุ่มเงินบริจาค
                </h3>

                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">
                    เงินบริจาค (บาท)
                  </label>
                  <input
                    type="number"
                    value={formData.donationAmount || ''}
                    onChange={(e) => setFormData({...formData, donationAmount: parseFloat(e.target.value) || 0})}
                    placeholder="บริจาคไปเท่าไหร่ต่อปี"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500"
                  />
                  <p className="text-xs text-yellow-700">ลดหย่อนได้สูงสุด 10% ของรายได้หลังหักค่าใช้จ่าย</p>
                </div>
              </div>

              {/* ระดับความเสี่ยง */}
              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">
                  ระดับความเสี่ยงที่รับได้
                </label>
                <select
                  key={`risk-${formData.risk_tolerance}`}
                  value={formData.risk_tolerance}
                  onChange={(e) => setFormData({...formData, risk_tolerance: e.target.value as 'low' | 'medium' | 'high'})}
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
                className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-4 px-6 rounded-lg transition-all disabled:bg-gray-400 disabled:cursor-not-allowed shadow-lg"
              >
                {loading ? '🔄 กำลังคำนวณ...' : '🚀 คำนวณภาษีและแนะนำ'}
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
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">💰 สรุปภาษี</h2>
                  
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

                    {/* กราฟผลตอบแทน */}
                    {returnChartData.length > 0 && (
                      <div className="mb-6">
                        <h3 className="text-lg font-semibold text-gray-900 mb-4">📈 ผลตอบแทนคาดการณ์</h3>
                        <div className="h-80">
                          <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={returnChartData}>
                              <CartesianGrid strokeDasharray="3 3" />
                              <XAxis 
                                dataKey="name" 
                                angle={-45}
                                textAnchor="end"
                                height={100}
                                fontSize={12}
                              />
                              <YAxis 
                                label={{ value: 'ผลตอบแทน (%)', angle: -90, position: 'insideLeft' }}
                              />
                              <Tooltip />
                              <Legend />
                              <Bar dataKey="1 ปี" fill="#3b82f6" />
                              <Bar dataKey="3 ปี" fill="#10b981" />
                              <Bar dataKey="5 ปี" fill="#f59e0b" />
                            </BarChart>
                          </ResponsiveContainer>
                        </div>
                      </div>
                    )}

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
                                {rec.expected_return_3y > 0 && <span className="text-xs bg-gray-100 px-2 py-1 rounded">3ปี: {rec.expected_return_3y}%</span>}
                                {rec.expected_return_5y > 0 && <span className="text-xs bg-gray-100 px-2 py-1 rounded">5ปี: {rec.expected_return_5y}%</span>}
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