# ⚡ Quick Start Guide - RASA

## 🎯 Cara Tercepat Menjalankan RASA

### 1️⃣ Setup Environment (5 menit)

#### Windows:
```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Linux/Mac:
```bash
# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Setup API Key (2 menit)

1. Buka [OpenRouter.ai](https://openrouter.ai/)
2. Login/Register
3. Generate API Key
4. Copy file `.env.example` menjadi `.env`
5. Buka `.env` dan ganti `<YOUR_OPENROUTER_API_KEY>` dengan API Key yang sudah di-copy

**Contoh isi `.env`:**
```env
SECRET_KEY=rasa-secret-key-2025
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxx
DATABASE_PATH=sqlite:///rasa.db
FLASK_ENV=development
```

### 3️⃣ Jalankan Aplikasi (1 menit)

```bash
python run.py
```

atau

```bash
python app.py
```

### 4️⃣ Akses Aplikasi

Buka browser dan kunjungi:
```
http://localhost:5000
```

## 🎉 Selesai!

Sekarang kamu bisa:
1. **Register** akun baru
2. **Login** dengan NIS dan password
3. **Mulai eksplorasi** dengan berbagai modul chat
4. **Download laporan** setelah menyelesaikan semua modul

## 🐛 Troubleshooting Cepat

### ❌ Error: "No module named 'flask'"
**Solusi:** Install dependencies
```bash
pip install -r requirements.txt
```

### ❌ Error: "OPENROUTER_API_KEY not found"
**Solusi:** Pastikan file `.env` sudah dibuat dan diisi dengan benar

### ❌ Error: "Port 5000 already in use"
**Solusi:** Ganti port di `app.py` atau matikan aplikasi yang menggunakan port 5000

### ❌ Error: "Database is locked"
**Solusi:** Hapus file `rasa.db` dan jalankan ulang aplikasi

## 📱 Test Fitur

### Test Registrasi:
1. Klik "Daftar Sekarang"
2. Isi form:
   - Nama Lengkap: **Test User**
   - NIS: **12345**
   - Kelas: **XII**
   - Password: **test123**
3. Klik "Daftar"

### Test Chat:
1. Login dengan akun yang sudah dibuat
2. Pilih modul "Analisator Jati Diri"
3. Jawab pertanyaan dari RASA
4. Setelah cukup, klik "Selesai & Analisis"
5. Lihat hasil analisis

## 🎨 Customization

### Ganti Warna Theme:
Edit `templates/base.html` bagian:
```javascript
colors: {
    'primary': '#6366f1',    // 👈 Ganti ini
    'secondary': '#8b5cf6',  // 👈 Ganti ini
}
```

### Ganti Nama Sekolah:
Edit `templates/base.html` dan `templates/index.html`

## 📚 Dokumentasi Lengkap

Lihat `README.md` untuk dokumentasi lengkap.

## 🚀 Deployment

Lihat `DEPLOYMENT_GUIDE.md` untuk panduan deploy ke Hostinger.

---

**Selamat mencoba! 🌟**

