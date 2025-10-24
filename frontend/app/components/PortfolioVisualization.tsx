import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

interface AllocationItem {
  name: string;
  investment_amount: number;
  percentage: number;
  tax_saving: number;
  risk_level: string;
  expected_return_1y: number;
  expected_return_3y: number;
  expected_return_5y: number;
  pros: string[];
  cons: string[];
  description: string;
}

interface PortfolioSummary {
  total_investment: number;
  total_tax_saving: number;
  overall_risk: string;
  overall_expected_return_1y: number;
  overall_expected_return_3y: number;
  overall_expected_return_5y: number;
}

interface PortfolioVisualizationProps {
  portfolioSummary: PortfolioSummary;
  allocations: AllocationItem[];
  summaryText: string;
}

// สีสำหรับแต่ละประเภท
const COLORS = [
  '#3B82F6', // Blue - RMF
  '#10B981', // Green - SSF
  '#F59E0B', // Amber - ประกันบำนาญ
  '#EF4444', // Red - ประกันชีวิต
  '#8B5CF6', // Purple - ประกันสุขภาพ
  '#EC4899', // Pink
  '#14B8A6', // Teal
];

// แปลง risk level เป็นภาษาไทย
const getRiskLevelText = (level: string): string => {
  const riskMap: Record<string, string> = {
    low: 'ต่ำ',
    medium: 'กลาง',
    high: 'สูง',
  };
  return riskMap[level] || level;
};

// แปลง risk level เป็นสี
const getRiskColor = (level: string): string => {
  const colorMap: Record<string, string> = {
    low: 'text-green-600 bg-green-100',
    medium: 'text-yellow-600 bg-yellow-100',
    high: 'text-red-600 bg-red-100',
  };
  return colorMap[level] || 'text-gray-600 bg-gray-100';
};

const PortfolioVisualization: React.FC<PortfolioVisualizationProps> = ({
  portfolioSummary,
  allocations,
  summaryText,
}) => {
  // เตรียมข้อมูลสำหรับ Pie Chart
  const chartData = allocations.map((item) => ({
    name: item.name,
    value: item.percentage,
    amount: item.investment_amount,
  }));

  // Custom label สำหรับ Pie Chart
  const renderCustomizedLabel = ({
    cx,
    cy,
    midAngle,
    innerRadius,
    outerRadius,
    percent,
  }: any) => {
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text
        x={x}
        y={y}
        fill="white"
        textAnchor={x > cx ? 'start' : 'end'}
        dominantBaseline="central"
        className="text-sm font-bold"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  return (
    <div className="space-y-8">
      {/* สรุปภาพรวม */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg shadow-lg p-6 text-white">
        <h2 className="text-2xl font-bold mb-4">📊 สรุปพอร์ตการลงทุน</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white bg-opacity-20 rounded-lg p-4">
            <p className="text-sm opacity-90">เงินลงทุนรวม</p>
            <p className="text-3xl font-bold">
              {portfolioSummary.total_investment.toLocaleString()} ฿
            </p>
          </div>
          <div className="bg-white bg-opacity-20 rounded-lg p-4">
            <p className="text-sm opacity-90">ประหยัดภาษี</p>
            <p className="text-3xl font-bold text-green-300">
              {portfolioSummary.total_tax_saving.toLocaleString()} ฿
            </p>
          </div>
          <div className="bg-white bg-opacity-20 rounded-lg p-4">
            <p className="text-sm opacity-90">ความเสี่ยงโดยรวม</p>
            <p className="text-3xl font-bold">
              {getRiskLevelText(portfolioSummary.overall_risk)}
            </p>
          </div>
        </div>
        <div className="mt-4 pt-4 border-t border-white border-opacity-30">
          <p className="text-sm opacity-90 mb-2">ผลตอบแทนคาดหวัง:</p>
          <div className="flex gap-6">
            <div>
              <span className="text-sm opacity-75">1 ปี: </span>
              <span className="font-bold">
                {portfolioSummary.overall_expected_return_1y.toFixed(1)}%
              </span>
            </div>
            <div>
              <span className="text-sm opacity-75">3 ปี: </span>
              <span className="font-bold">
                {portfolioSummary.overall_expected_return_3y.toFixed(1)}%
              </span>
            </div>
            <div>
              <span className="text-sm opacity-75">5 ปี: </span>
              <span className="font-bold">
                {portfolioSummary.overall_expected_return_5y.toFixed(1)}%
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* สรุปเป็นข้อความ */}
      <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
        <p className="text-gray-700">{summaryText}</p>
      </div>

      {/* Pie Chart */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold mb-4">🥧 การกระจายการลงทุน</h3>
        <ResponsiveContainer width="100%" height={400}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={renderCustomizedLabel}
              outerRadius={150}
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              formatter={(value: number, name: string, props: any) => [
                `${value.toFixed(1)}% (${props.payload.amount.toLocaleString()} บาท)`,
                name,
              ]}
            />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* รายละเอียดแต่ละประเภท */}
      <div className="space-y-4">
        <h3 className="text-xl font-bold">📋 รายละเอียดแต่ละประเภท</h3>
        {allocations.map((item, index) => (
          <div
            key={index}
            className="border-2 rounded-lg p-6 hover:shadow-lg transition-shadow"
            style={{ borderColor: COLORS[index % COLORS.length] }}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div
                  className="w-4 h-4 rounded-full"
                  style={{ backgroundColor: COLORS[index % COLORS.length] }}
                />
                <div>
                  <h4 className="text-lg font-bold">{item.name}</h4>
                  <p className="text-sm text-gray-600">{item.description}</p>
                </div>
              </div>
              <span
                className={`px-3 py-1 rounded-full text-xs font-semibold ${getRiskColor(
                  item.risk_level
                )}`}
              >
                ความเสี่ยง: {getRiskLevelText(item.risk_level)}
              </span>
            </div>

            {/* จำนวนเงินและเปอร์เซ็นต์ */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
              <div className="bg-gray-50 rounded p-3">
                <p className="text-xs text-gray-600">จำนวนเงิน</p>
                <p className="text-xl font-bold text-gray-800">
                  {item.investment_amount.toLocaleString()} ฿
                </p>
              </div>
              <div className="bg-gray-50 rounded p-3">
                <p className="text-xs text-gray-600">สัดส่วน</p>
                <p className="text-xl font-bold text-gray-800">
                  {item.percentage.toFixed(1)}%
                </p>
              </div>
              <div className="bg-green-50 rounded p-3">
                <p className="text-xs text-gray-600">ประหยัดภาษี</p>
                <p className="text-xl font-bold text-green-600">
                  {item.tax_saving.toLocaleString()} ฿
                </p>
              </div>
              <div className="bg-blue-50 rounded p-3">
                <p className="text-xs text-gray-600">ผลตอบแทน 5 ปี</p>
                <p className="text-xl font-bold text-blue-600">
                  {item.expected_return_5y.toFixed(1)}%
                </p>
              </div>
            </div>

            {/* ข้อดีข้อเสีย */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h5 className="font-semibold text-green-700 mb-2">✅ ข้อดี</h5>
                <ul className="space-y-1">
                  {item.pros.map((pro, i) => (
                    <li key={i} className="text-sm text-gray-700 flex items-start">
                      <span className="text-green-500 mr-2">•</span>
                      {pro}
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <h5 className="font-semibold text-red-700 mb-2">❌ ข้อเสีย</h5>
                <ul className="space-y-1">
                  {item.cons.map((con, i) => (
                    <li key={i} className="text-sm text-gray-700 flex items-start">
                      <span className="text-red-500 mr-2">•</span>
                      {con}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* ผลตอบแทนคาดหวัง */}
            <div className="mt-4 pt-4 border-t">
              <p className="text-sm font-semibold text-gray-600 mb-2">
                📈 ผลตอบแทนคาดหวัง:
              </p>
              <div className="flex gap-4 text-sm">
                <span>
                  1 ปี: <strong>{item.expected_return_1y.toFixed(1)}%</strong>
                </span>
                <span>
                  3 ปี: <strong>{item.expected_return_3y.toFixed(1)}%</strong>
                </span>
                <span>
                  5 ปี: <strong>{item.expected_return_5y.toFixed(1)}%</strong>
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PortfolioVisualization;