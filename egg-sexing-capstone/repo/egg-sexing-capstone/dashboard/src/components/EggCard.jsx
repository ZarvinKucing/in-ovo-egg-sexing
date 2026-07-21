// Kartu data telur terbaru dengan badge status gender dinamis.
// Referensi: Buku Capstone Design, Bab 4.2.4 (Card Data Terbaru).

import React from "react";
import { format } from "date-fns";
import { id as idLocale } from "date-fns/locale";

const EggCard = ({ egg }) => {
  const isBetina = egg.status === "betina";
  const statusColor = isBetina ? "#10B981" : "#EF4444";
  const statusBgColor = isBetina ? "#D1FAE5" : "#FEE2E2";

  return (
    <div className="bg-white dark:bg-[#121214] border border-[#E5E7EB] dark:border-[#27272A] rounded-lg p-6">
      <div className="flex items-center justify-between mb-2">
        <p className="font-semibold">{egg.id}</p>
        <div
          className="px-3 py-1 rounded-full text-sm font-medium"
          style={{ backgroundColor: statusBgColor, color: statusColor }}
        >
          {isBetina ? "Betina" : "Jantan"}
        </div>
      </div>

      <p className="text-sm text-[#52525B]">{egg.confidence}% confidence</p>
      <p className="text-sm text-[#52525B]">
        {egg.timestamp &&
          format(new Date(egg.timestamp), "dd MMMM yyyy, HH:mm", {
            locale: idLocale,
          })}
      </p>
    </div>
  );
};

export default EggCard;
