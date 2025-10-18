# 🧠 ANALISATOR JATI DIRI SISWA SMA

## 📋 Deskripsi

Analisator Jati Diri adalah sistem chatbot interaktif yang membantu siswa SMA mengenal dan memahami jati diri mereka melalui 24 pertanyaan komprehensif berdasarkan teori James Marcia (1966).

## 🎯 Tujuan

- Membantu siswa SMA mengenal diri lebih dalam
- Memberikan analisis komprehensif tentang identitas diri
- Memberikan rekomendasi pengembangan diri
- Menyediakan referensi untuk perencanaan masa depan

## 📊 Struktur Analisis

### 4 Dimensi Identitas:

1. **Eksplorasi Diri** (6 pertanyaan)
   - Keterbukaan terhadap pengalaman baru
   - Pencarian informasi tentang masa depan
   - Refleksi diri dan potensi

2. **Komitmen Diri** (6 pertanyaan)
   - Kekuatan tujuan hidup
   - Konsistensi dalam bertindak
   - Keyakinan terhadap keputusan

3. **Reconsideration** (6 pertanyaan)
   - Refleksi terhadap keputusan
   - Keterbukaan terhadap perubahan
   - Evaluasi konsekuensi

4. **Gaya Identitas** (6 pertanyaan)
   - Cara mengambil keputusan
   - Kemerdekaan dari pengaruh luar
   - Kepercayaan diri dalam bertindak

## 🔢 Sistem Scoring

- **A** = 1 poin (Rendah)
- **B** = 2 poin (Sedang)
- **C** = 3 poin (Tinggi)

**Total Maksimal:** 72 poin

## 📈 Interpretasi Hasil

### Berdasarkan Total Skor:

- **24-36**: Identity Diffusion — belum memiliki arah hidup atau kesadaran nilai diri
- **37-48**: Foreclosure — mengikuti nilai luar tanpa eksplorasi mendalam
- **49-60**: Moratorium — sedang mencari dan bereksperimen dengan identitas diri
- **61-72**: Identity Achievement — sudah mengenal, mengeksplorasi, dan menetapkan jati diri

## 🚀 Cara Menggunakan

### 1. Menjalankan Chatbot
```bash
python analisator_jati_diri.py
```

### 2. Langkah-langkah:
1. Baca intro dan penjelasan
2. Masukkan nama
3. Konfirmasi kesiapan
4. Jawab 24 pertanyaan dengan jujur
5. Dapatkan analisis komprehensif
6. Simpan hasil untuk referensi

### 3. Demo dan Informasi
```bash
python demo_analisator.py
```

## ✨ Fitur Chatbot

- ✅ **Intro yang menarik** - Penjelasan lengkap tentang tujuan analisis
- ✅ **24 pertanyaan komprehensif** - Mencakup semua aspek identitas diri
- ✅ **Analisis real-time** - Feedback langsung untuk setiap jawaban
- ✅ **Interpretasi ilmiah** - Berdasarkan teori James Marcia (1966)
- ✅ **Analisis per dimensi** - Evaluasi mendalam setiap aspek
- ✅ **Rekomendasi pengembangan** - Saran konkret untuk perbaikan
- ✅ **Penyimpanan hasil** - Data tersimpan dalam format JSON
- ✅ **Interface user-friendly** - Mudah digunakan dan dipahami

## 📁 Output

### File Hasil:
```
hasil_jati_diri_[nama]_[timestamp].json
```

### Struktur Data:
```json
{
  "user_info": {
    "name": "Nama Siswa",
    "timestamp": "20251009_220000",
    "date": "2025-10-09 22:00:00"
  },
  "scores": {
    "total": 45,
    "max_possible": 72,
    "dimension_scores": {
      "Eksplorasi Diri": 12,
      "Komitmen Diri": 15,
      "Reconsideration": 9,
      "Gaya Identitas": 9
    },
    "status": "Moratorium — sedang mencari dan bereksperimen dengan identitas diri"
  },
  "answers": [...]
}
```

## 🎓 Dasar Teoritis

### James Marcia (1966) - Identity Status Theory:
- **Identity Diffusion**: Belum memiliki komitmen atau eksplorasi
- **Foreclosure**: Memiliki komitmen tanpa eksplorasi
- **Moratorium**: Sedang dalam proses eksplorasi
- **Identity Achievement**: Memiliki komitmen setelah eksplorasi

### Referensi Tambahan:
- Crocetti et al. (2008) - Model tiga dimensi identitas
- Luyckx et al. (2006) - Model lima dimensi identitas
- Berzonsky (2011) - Gaya identitas dan pengambilan keputusan

## 💡 Tips Penggunaan

1. **Jawab dengan jujur** - Hasil akan lebih akurat jika jawaban mencerminkan diri yang sebenarnya
2. **Jangan terburu-buru** - Baca setiap pertanyaan dengan teliti
3. **Simpan hasil** - Gunakan sebagai referensi untuk evaluasi diri
4. **Ulangi secara berkala** - Lakukan analisis ulang setiap 6-12 bulan
5. **Diskusikan dengan konselor** - Konsultasi dengan guru BK atau konselor jika diperlukan

## 🔧 Technical Details

### Requirements:
- Python 3.6+
- Standard library only (no external dependencies)

### File Structure:
```
analisator_jati_diri.py     # Main chatbot script
demo_analisator.py          # Demo dan informasi
ANALISATOR_JATI_DIRI_GUIDE.md  # Dokumentasi ini
hasil_jati_diri_*.json      # File hasil (auto-generated)
```

### Error Handling:
- Input validation untuk jawaban A/B/C
- Graceful handling untuk interrupt (Ctrl+C)
- File saving dengan error handling

## 📞 Support

Jika mengalami masalah atau memerlukan bantuan:
1. Periksa apakah Python terinstall dengan benar
2. Pastikan file `analisator_jati_diri.py` dapat diakses
3. Coba jalankan `demo_analisator.py` untuk melihat informasi sistem
4. Konsultasi dengan guru BK atau konselor sekolah

---

**Versi:** 2.1  
**Tanggal:** Oktober 2025  
**Author:** RASA System  
**Status:** Ready for Use ✅
