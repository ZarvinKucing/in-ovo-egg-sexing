# Dashboard Monitoring — Egg Sexing System

React + Vite + Firebase Realtime Database.

## Setup

```bash
npm install
```

Buat file `.env` di folder ini (jangan commit ke git):

```
VITE_FIREBASE_API_KEY=xxx
VITE_FIREBASE_AUTH_DOMAIN=xxx
VITE_FIREBASE_DATABASE_URL=xxx
VITE_FIREBASE_PROJECT_ID=xxx
```

Jalankan:

```bash
npm run dev
```

## Struktur

```
src/
├── App.jsx                    # halaman utama
├── components/
│   ├── StatsCard.jsx          # kartu statistik (total, betina, jantan, accuracy)
│   ├── EggCard.jsx            # kartu data telur terbaru
│   └── GenderChart.jsx        # pie chart distribusi gender
└── services/
    ├── firebaseConfig.js      # init Firebase + auth anonymous
    └── eggService.js          # subscribeToEggs (realtime listener)
```

> ⚠️ Ini kerangka dashboard berdasarkan potongan kode di Buku Capstone Design.
> Beberapa bagian (search & filter, pagination) disebutkan sudah ada di dashboard asli
> tapi belum ada snippet-nya di buku — tambahkan sendiri sesuai implementasi final kamu.
