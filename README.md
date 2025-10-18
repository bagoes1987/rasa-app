# RASA - Refleksi dan Asistensi Sosial Emosional Siswa

<div align="center">
  <h3>🌟 Platform Analisis & Konseling AI untuk Siswa SMA</h3>
  <p>Membantu siswa mengenal diri, mengelola emosi, dan merencanakan masa depan</p>
</div>

---

## 📋 Deskripsi

RASA adalah chatbot konseling berbasis AI yang dirancang khusus untuk membantu siswa SMA Negeri 1 Belitang dalam:

- 🌟 **Analisis Jati Diri** - Menggali nilai, motivasi, dan passion siswa
- 💝 **Kecerdasan Emosional** - Mengukur dan meningkatkan EQ
- 📚 **Gaya Belajar** - Menemukan metode belajar yang paling efektif
- 🎯 **Rekomendasi Jurusan SMA** - Membantu memilih jurusan yang tepat
- 🎓 **Rekomendasi Program Studi** - Panduan memilih jurusan kuliah

## 🚀 Fitur Utama

### Untuk Siswa:
- ✅ Chat interaktif dengan AI konselor (RASA)
- ✅ Analisis komprehensif 5 aspek perkembangan
- ✅ Dashboard personal dengan riwayat analisis
- ✅ Download laporan lengkap dalam format PDF
- ✅ Interface modern dan Gen Z-friendly

### Teknologi:
- ✅ Flask (Python Web Framework)
- ✅ SQLite (Database ringan)
- ✅ OpenRouter AI API (LLM Integration)
- ✅ Tailwind CSS (Modern UI)
- ✅ ReportLab (PDF Generation)

## 📦 Instalasi

### Prasyarat:
- Python 3.8 atau lebih baru
- pip (Python package manager)
- OpenRouter API Key

### Langkah Instalasi:

1. **Clone atau Download Project**
   ```bash
   cd RasaVer1.0
   ```

2. **Buat Virtual Environment (Opsional tapi Disarankan)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables**
   
   Buat file `.env` di root folder:
   ```env
   SECRET_KEY=your-secret-key-here-ganti-dengan-random-string
   OPENROUTER_API_KEY=your-openrouter-api-key-here
   DATABASE_PATH=sqlite:///rasa.db
   FLASK_ENV=development
   ```

   > **PENTING:** Dapatkan API Key dari [OpenRouter.ai](https://openrouter.ai/)

5. **Inisialisasi Database**
   ```bash
   python
   >>> from app import app, db
   >>> with app.app_context():
   ...     db.create_all()
   >>> exit()
   ```

6. **Jalankan Aplikasi**
   ```bash
   python app.py
   ```

7. **Akses Aplikasi**
   
   Buka browser dan kunjungi: `http://localhost:5000`

## 🌐 Deployment ke Hostinger

### Persiapan:

1. **Pastikan Hostinger Support Python**
   - Gunakan hosting yang support Python dan WSGI
   - Atau gunakan VPS jika shared hosting tidak support

2. **Upload Files**
   - Upload semua file kecuali `venv/`, `__pycache__/`, dan `.env`
   - Upload via FTP atau File Manager

3. **Setup di Server**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Set environment variables di hosting panel
   # Atau buat file .env
   ```

4. **Gunakan Gunicorn untuk Production**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

5. **Setup Web Server (Nginx/Apache)**
   - Configure reverse proxy ke Gunicorn
   - Setup SSL certificate (recommended)

### Environment Variables Production:
```env
SECRET_KEY=<strong-random-key>
OPENROUTER_API_KEY=<your-actual-api-key>
DATABASE_PATH=sqlite:////path/to/production/rasa.db
FLASK_ENV=production
```

## 📁 Struktur Folder

```
RasaVer1.0/
├── app.py                 # Main application file
├── config.py             # Configuration
├── models.py             # Database models
├── openrouter_service.py # OpenRouter API integration
├── chat_modules.py       # Chat module configurations
├── report_generator.py   # PDF report generation
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (BUAT SENDIRI)
├── README.md            # Documentation
│
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── modules.html
│   ├── chat.html
│   ├── result.html
│   ├── 404.html
│   ├── 500.html
│   └── results/        # Module-specific result templates
│       ├── jati_diri.html
│       ├── eq.html
│       ├── gaya_belajar.html
│       ├── jurusan_sma.html
│       └── prodi_kuliah.html
│
├── static/              # Static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│
└── reports/            # Generated PDF reports (auto-created)
```

## 🔒 Keamanan

- ✅ Password di-hash dengan Werkzeug
- ✅ Flask-Login untuk session management
- ✅ CSRF protection (Flask built-in)
- ✅ SQL Injection protection (SQLAlchemy ORM)
- ✅ Environment variables untuk sensitive data

## 🎨 Customization

### Mengubah Warna:
Edit `templates/base.html` di bagian Tailwind config:
```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                'primary': '#6366f1',    // Ganti warna utama
                'secondary': '#8b5cf6',  // Ganti warna sekunder
            }
        }
    }
}
```

### Menambah Modul Baru:
Edit `chat_modules.py` dan tambahkan konfigurasi modul baru.

## 📝 Database Schema

### Users
- id, nama_lengkap, nis (unique), kelas, password_hash, created_at

### ChatSessions
- id, user_id, module_type, started_at, completed_at, is_completed

### ChatMessages
- id, session_id, role, content, timestamp

### AnalysisResults
- id, user_id, session_id, module_type, result_data (JSON), created_at

## 🐛 Troubleshooting

### Error: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error: "OPENROUTER_API_KEY not configured"
- Pastikan file `.env` sudah dibuat
- Isi dengan API Key yang valid dari OpenRouter.ai

### Database Error
```bash
# Reset database
rm rasa.db
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
```

### Port sudah digunakan
```bash
# Ganti port di app.py atau jalankan dengan:
python app.py --port 8080
```

## 🤝 Support

Untuk pertanyaan atau issue, silakan hubungi:
- Email: [your-email@example.com]
- GitHub Issues: [Create an issue]

## 📄 License

Copyright © 2025 SMA Negeri 1 Belitang. All rights reserved.

---

<div align="center">
  <p>Made with 💜 for students</p>
  <p><strong>RASA - Temukan jati dirimu!</strong></p>
</div>

