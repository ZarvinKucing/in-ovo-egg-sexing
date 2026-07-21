// Konfigurasi koneksi Firebase untuk dashboard web.
// Referensi: Buku Capstone Design, Bab 4.2.3 (Rules Firebase - akses baca butuh autentikasi).
//
// TODO: isi konfigurasi ini dari Firebase Console (Project Settings > Web App)
// Simpan sebagai environment variables (.env), JANGAN hardcode & JANGAN commit ke git.

import { initializeApp } from "firebase/app";
import { getDatabase } from "firebase/database";
import { getAuth, signInAnonymously } from "firebase/auth";

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  databaseURL: import.meta.env.VITE_FIREBASE_DATABASE_URL,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
};

const app = initializeApp(firebaseConfig);
export const db = getDatabase(app);
export const auth = getAuth(app);

// Dashboard hanya boleh membaca data setelah berhasil autentikasi anonymous,
// sesuai Firebase Security Rules: { ".read": "auth != null", ".write": false }
signInAnonymously(auth).catch((error) => {
  console.error("Firebase anonymous auth error:", error);
});
