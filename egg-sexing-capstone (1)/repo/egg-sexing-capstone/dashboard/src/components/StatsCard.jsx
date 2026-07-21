// Kartu statistik reusable (total telur, betina, jantan, model accuracy).
// Referensi: Buku Capstone Design, Bab 4.2.4 (Kartu Statistik).

import React from "react";

const StatsCard = ({ icon: Icon, label, value, iconColor, loading }) => {
  if (loading) {
    return (
      <div className="bg-white dark:bg-[#121214] border border-[#E5E7EB] dark:border-[#27272A] rounded-lg p-6 shadow-[0_2px_8px_rgba(0,0,0,0.04)] dark:shadow-[0_2px_8px_rgba(0,0,0,0.2)]">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-20 mb-3"></div>
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-16"></div>
        </div>
      </div>
    );
  }

  return (
    <div
      className="bg-white dark:bg-[#121214] border border-[#E5E7EB] dark:border-[#27272A] rounded-lg p-6 shadow-[0_2px_8px_rgba(0,0,0,0.04)] dark:shadow-[0_2px_8px_rgba(0,0,0,0.2)]"
      data-testid={`stats-card-${label.toLowerCase().replace(/\s+/g, "-")}`}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[#52525B] dark:text-[#A1A1AA] mb-2 font-['IBM_Plex_Sans']">
            {label}
          </p>
          <p className="text-2xl sm:text-3xl font-semibold tracking-tight text-[#0A0A0A] dark:text-[#FAFAFA] font-['Manrope']">
            {value}
          </p>
        </div>
        {Icon && (
          <div className="p-2 rounded-lg" style={{ backgroundColor: iconColor + "20" }}>
            <Icon size={24} style={{ color: iconColor }} />
          </div>
        )}
      </div>
    </div>
  );
};

export default StatsCard;
