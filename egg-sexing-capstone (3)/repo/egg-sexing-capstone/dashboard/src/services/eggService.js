// Service untuk berlangganan data telur secara real-time dari Firebase Realtime Database.
// Referensi: Buku Capstone Design, Bab 4.2.4 (Implementasi Web Dashboard).

import { ref, onValue } from "firebase/database";
import { db } from "./firebaseConfig";

function mapItemToEgg(item) {
  // TODO: sesuaikan mapping ini kalau struktur field di Firebase berubah.
  return {
    id: item.id || item.egg_id || item.kode,
    status: item.status || item.gender,
    confidence: item.confidence ?? 50,
    weight: item.weight_grams,
    width: item.width_cm,
    height: item.height_cm,
    shapeIndex: item.shape_index,
    glcmContrast: item.glcm_contrast,
    timestamp: item.timestamp,
  };
}

function sortByTimestamp(eggs) {
  return [...eggs].sort(
    (a, b) => new Date(b.timestamp) - new Date(a.timestamp)
  );
}

export const eggService = {
  subscribeToEggs(callback) {
    // Referensi ke root database Firebase
    const eggsRef = ref(db, "/");

    // Listener realtime Firebase
    const unsubscribe = onValue(
      eggsRef,
      (snapshot) => {
        try {
          if (!snapshot.exists()) {
            callback([]);
            return;
          }
          // Ambil seluruh data dari Firebase
          const data = snapshot.val();
          const eggs = sortByTimestamp(Object.values(data).map(mapItemToEgg));
          callback(eggs);
        } catch (error) {
          console.error("Realtime Firebase processing error:", error);
          callback([]);
        }
      },
      // Error handler listener
      (error) => {
        console.error("Realtime Firebase listener error:", error);
        callback([]);
      }
    );

    return () => unsubscribe();
  },
};
