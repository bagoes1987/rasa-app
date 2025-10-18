# 🚀 Panduan Setup GitHub untuk RASA

## ✅ Step 1: Buat Repository di GitHub

1. **Login ke GitHub**
   - Buka [github.com](https://github.com)
   - Login dengan akun Anda (atau buat akun baru jika belum punya)

2. **Buat Repository Baru**
   - Klik tombol **"+"** di kanan atas → **"New repository"**
   - Isi form:
     - **Repository name**: `rasa-app` (atau nama lain yang Anda suka)
     - **Description**: `RASA - Platform Konseling AI untuk Siswa SMA`
     - **Public** atau **Private**: Pilih sesuai kebutuhan
     - **JANGAN** centang "Initialize this repository with a README"
   - Klik **"Create repository"**

3. **Copy URL Repository**
   - Setelah repository dibuat, copy URL yang muncul
   - Contoh: `https://github.com/username/rasa-app.git`

---

## 📤 Step 2: Push Code ke GitHub

Jalankan command berikut di terminal (di folder project):

```bash
# Tambahkan remote repository
git remote add origin https://github.com/USERNAME/NAMA-REPO.git

# Push code ke GitHub
git branch -M main
git push -u origin main
```

**Ganti `USERNAME` dan `NAMA-REPO` dengan URL repository Anda!**

**Contoh:**
```bash
git remote add origin https://github.com/johndoe/rasa-app.git
git branch -M main
git push -u origin main
```

---

## 🔄 Step 3: Update Code di Masa Depan

Setiap kali ada perubahan code, jalankan:

```bash
# Stage semua perubahan
git add .

# Commit dengan pesan yang jelas
git commit -m "Deskripsi perubahan yang dilakukan"

# Push ke GitHub
git push origin main
```

**Contoh:**
```bash
git add .
git commit -m "Update logo dan fix bug survey completion"
git push origin main
```

---

## 🌐 Step 4: Deploy ke Hosting (Opsional)

### Option A: Deploy ke Railway (Recommended - Mudah)

1. **Login ke Railway**
   - Buka [railway.app](https://railway.app)
   - Login dengan GitHub

2. **Deploy dari GitHub**
   - Klik **"New Project"**
   - Pilih **"Deploy from GitHub repo"**
   - Pilih repository `rasa-app`
   - Railway akan auto-deploy

3. **Setup Environment Variables**
   - Di Railway dashboard, buka **"Variables"**
   - Tambahkan:
     ```
     SECRET_KEY=random-secret-key-ganti-ini
     OPENROUTER_API_KEY=your-openrouter-api-key
     FLASK_ENV=production
     ```

4. **Domain**
   - Railway akan generate domain otomatis: `rasa-app.up.railway.app`
   - Atau bisa custom domain

**DONE! ✅** Aplikasi sudah online dan bisa diakses!

---

### Option B: Deploy ke Render (Alternative)

1. **Login ke Render**
   - Buka [render.com](https://render.com)
   - Login dengan GitHub

2. **Create New Web Service**
   - Klik **"New +"** → **"Web Service"**
   - Connect repository `rasa-app`
   - Settings:
     - **Name**: `rasa-app`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn wsgi:app`

3. **Environment Variables**
   - Tambahkan di **"Environment"** tab:
     ```
     SECRET_KEY=random-secret-key-ganti-ini
     OPENROUTER_API_KEY=your-openrouter-api-key
     FLASK_ENV=production
     ```

4. **Deploy**
   - Klik **"Create Web Service"**
   - Tunggu proses deploy selesai

**DONE! ✅** Aplikasi sudah online!

---

### Option C: Deploy ke VPS (Manual - Full Control)

Jika Anda punya VPS (DigitalOcean, Vultr, dll):

1. **SSH ke VPS**
   ```bash
   ssh root@your-vps-ip
   ```

2. **Install Dependencies**
   ```bash
   apt update
   apt install python3 python3-pip nginx git -y
   ```

3. **Clone Repository**
   ```bash
   cd /var/www
   git clone https://github.com/USERNAME/rasa-app.git
   cd rasa-app
   ```

4. **Setup Python Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Setup Environment Variables**
   ```bash
   nano .env
   # Isi dengan:
   # SECRET_KEY=your-secret-key
   # OPENROUTER_API_KEY=your-api-key
   # FLASK_ENV=production
   ```

6. **Setup Gunicorn Service**
   ```bash
   nano /etc/systemd/system/rasa.service
   ```
   
   Isi dengan:
   ```ini
   [Unit]
   Description=RASA Gunicorn Service
   After=network.target

   [Service]
   User=root
   WorkingDirectory=/var/www/rasa-app
   Environment="PATH=/var/www/rasa-app/venv/bin"
   ExecStart=/var/www/rasa-app/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 wsgi:app

   [Install]
   WantedBy=multi-user.target
   ```

7. **Setup Nginx**
   ```bash
   nano /etc/nginx/sites-available/rasa
   ```
   
   Isi dengan:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static {
           alias /var/www/rasa-app/static;
       }
   }
   ```

8. **Enable & Start Services**
   ```bash
   ln -s /etc/nginx/sites-available/rasa /etc/nginx/sites-enabled/
   systemctl enable rasa
   systemctl start rasa
   systemctl restart nginx
   ```

**DONE! ✅** Aplikasi sudah online di VPS!

---

## 🔐 Important Notes

1. **JANGAN commit file `.env`** - File ini sudah di-ignore oleh `.gitignore`
2. **JANGAN commit database (`*.db`)** - Sudah di-ignore
3. **SELALU ganti `SECRET_KEY`** di production dengan random string
4. **API Key OpenRouter** harus valid untuk AI chat berfungsi

---

## 🆘 Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/USERNAME/NAMA-REPO.git
```

### Error: Authentication failed
- Gunakan **Personal Access Token** sebagai password
- Generate di GitHub: Settings → Developer settings → Personal access tokens

### Error: Port already in use
```bash
# Matikan aplikasi yang sedang running
# Di Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Di Linux:
sudo lsof -ti:5000 | xargs sudo kill -9
```

---

## 📞 Support

Jika ada masalah, silakan:
1. Cek GitHub Issues
2. Hubungi developer
3. Baca dokumentasi lengkap di README.md

---

**Good luck! 🚀**

