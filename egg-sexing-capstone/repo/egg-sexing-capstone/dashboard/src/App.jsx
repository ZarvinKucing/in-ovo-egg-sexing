// Halaman utama dashboard - menggabungkan StatsCard, EggCard, GenderChart.
// Referensi: Buku Capstone Design, Bab 4.2.4 (Implementasi Web Dashboard).
//
// TODO: ini kerangka integrasi berdasarkan potongan kode di buku TA.
// Lengkapi styling/layout final sesuai desain dashboard aslimu (Gambar 4.13).

import React, { useState, useEffect } from "react";
import { Database, Egg, Target, TrendingUp } from "lucide-react";
import { eggService } from "./services/eggService";
import StatsCard from "./components/StatsCard";
import EggCard from "./components/EggCard";
import GenderChart from "./components/GenderChart";

const MODEL_ACCURACY = "88%"; // Hasil akhir model SVM, lihat docs/model_results.md

function App() {
  const [featuredEgg, setFeaturedEgg] = useState(null);
  const [stats, setStats] = useState({ total: 0, betina: 0, jantan: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = eggService.subscribeToEggs((eggs) => {
      if (eggs.length > 0) {
        setFeaturedEgg(eggs[0]);
        const betina = eggs.filter((e) => e.status === "betina").length;
        const jantan = eggs.filter((e) => e.status === "jantan").length;
        setStats({ total: eggs.length, betina, jantan });
      }
      setLoading(false);
    });
    return () => unsubscribe();
  }, []);

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">Egg Sexing Dashboard</h1>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatsCard icon={Database} label="Total Telur" value={stats.total} iconColor="#0A0A0A" loading={loading} />
        <StatsCard icon={Egg} label="Betina" value={stats.betina} iconColor="#10B981" loading={loading} />
        <StatsCard icon={Target} label="Jantan" value={stats.jantan} iconColor="#EF4444" loading={loading} />
        <StatsCard icon={TrendingUp} label="Model Accuracy" value={MODEL_ACCURACY} iconColor="#0A0A0A" loading={loading} />
      </div>

      {featuredEgg && <EggCard egg={featuredEgg} />}

      <GenderChart stats={stats} />
    </div>
  );
}

export default App;
