// Pie chart distribusi status gender telur (Recharts).
// Referensi: Buku Capstone Design, Bab 4.2.4 (Grafik Distribusi Status Gender).

import React from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const GenderChart = ({ stats }) => {
  const chartData = [
    { name: "Betina", value: stats.betina, color: "#10B981" },
    { name: "Jantan", value: stats.jantan, color: "#EF4444" },
  ];

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={chartData}
          labelLine={false}
          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
          outerRadius={80}
          dataKey="value"
        >
          {chartData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            backgroundColor: "#FFFFFF",
            border: "1px solid #E5E7EB",
            borderRadius: "8px",
          }}
        />
        <Legend wrapperStyle={{ fontSize: "12px", fontFamily: "IBM Plex Sans" }} />
      </PieChart>
    </ResponsiveContainer>
  );
};

export default GenderChart;
