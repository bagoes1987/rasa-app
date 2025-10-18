# 🚀 Panduan Deployment RASA ke Hostinger

## Persiapan

### 1. Mendapatkan OpenRouter API Key
1. Kunjungi [OpenRouter.ai](https://openrouter.ai/)
2. Daftar/Login akun
3. Buka menu API Keys
4. Generate API Key baru
5. Copy dan simpan API Key dengan aman

### 2. Persiapan Files
Pastikan semua file berikut sudah ada:
- ✅ app.py
- ✅ config.py
- ✅ models.py
- ✅ requirements.txt
- ✅ templates/ (folder dengan semua HTML)
- ✅ static/ (folder dengan CSS & JS)

## Metode Deployment

### Opsi 1: Shared Hosting (Tidak Disarankan)
Kebanyakan shared hosting Hostinger tidak support Python/Flask dengan baik.

### Opsi 2: VPS Hostinger (DISARANKAN)

#### Step 1: Setup VPS
1. Login ke Hostinger VPS
2. Akses via SSH:
   ```bash
   ssh root@your-vps-ip
   ```

#### Step 2: Install Dependencies
```bash
# Update sistem
apt update && apt upgrade -y

# Install Python & pip
apt install python3 python3-pip python3-venv nginx -y

# Install Git (optional)
apt install git -y
```

#### Step 3: Upload Aplikasi
```bash
# Buat direktori aplikasi
mkdir -p /var/www/rasa
cd /var/www/rasa

# Upload files via SFTP atau Git
# Atau gunakan scp dari komputer lokal:
# scp -r RasaVer1.0/* root@your-vps-ip:/var/www/rasa/
```

#### Step 4: Setup Virtual Environment
```bash
cd /var/www/rasa
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Step 5: Setup Environment Variables
```bash
nano .env
```

Isi dengan:
```env
SECRET_KEY=your-super-secret-key-here-ganti-dengan-random-string-panjang
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
DATABASE_PATH=sqlite:////var/www/rasa/rasa.db
FLASK_ENV=production
```

Tekan `Ctrl+X`, lalu `Y`, lalu `Enter` untuk save.

#### Step 6: Initialize Database
```bash
python3 << EOF
from app import app, db
with app.app_context():
    db.create_all()
print("Database created!")
EOF
```

#### Step 7: Setup Gunicorn Systemd Service
```bash
nano /etc/systemd/system/rasa.service
```

Isi dengan:
```ini
[Unit]
Description=RASA Flask Application
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/rasa
Environment="PATH=/var/www/rasa/venv/bin"
ExecStart=/var/www/rasa/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

Enable dan start service:
```bash
systemctl daemon-reload
systemctl enable rasa
systemctl start rasa
systemctl status rasa
```

#### Step 8: Setup Nginx Reverse Proxy
```bash
nano /etc/nginx/sites-available/rasa
```

Isi dengan:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/rasa/static;
        expires 30d;
    }
}
```

Enable site:
```bash
ln -s /etc/nginx/sites-available/rasa /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### Step 9: Setup SSL (HTTPS) - Gratis dengan Let's Encrypt
```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your-domain.com -d www.your-domain.com
```

## Verifikasi

1. Akses `http://your-domain.com` atau `https://your-domain.com`
2. Coba register akun baru
3. Test semua modul chat
4. Coba download report

## Maintenance

### Melihat Logs
```bash
# Application logs
journalctl -u rasa -f

# Nginx logs
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
```

### Restart Aplikasi
```bash
systemctl restart rasa
```

### Update Aplikasi
```bash
cd /var/www/rasa
source venv/bin/activate

# Pull changes jika pakai git
git pull

# Atau upload file baru via SFTP

# Restart
systemctl restart rasa
```

### Backup Database
```bash
# Backup manual
cp /var/www/rasa/rasa.db /var/www/rasa/backup/rasa_$(date +%Y%m%d).db

# Setup auto backup (crontab)
crontab -e

# Tambahkan line ini untuk backup setiap hari jam 2 pagi:
0 2 * * * cp /var/www/rasa/rasa.db /var/www/rasa/backup/rasa_$(date +\%Y\%m\%d).db
```

## Troubleshooting

### Error: "502 Bad Gateway"
```bash
# Check Gunicorn status
systemctl status rasa

# Restart Gunicorn
systemctl restart rasa
```

### Error: Database locked
```bash
# Check file permissions
chown -R www-data:www-data /var/www/rasa
chmod 755 /var/www/rasa
chmod 644 /var/www/rasa/rasa.db
```

### Error: "Module not found"
```bash
cd /var/www/rasa
source venv/bin/activate
pip install -r requirements.txt
systemctl restart rasa
```

## Optimasi Performance

### 1. Increase Gunicorn Workers
Edit `/etc/systemd/system/rasa.service`:
```ini
# Ganti -w 4 dengan jumlah: (2 x CPU cores) + 1
ExecStart=/var/www/rasa/venv/bin/gunicorn -w 8 -b 127.0.0.1:8000 app:app
```

### 2. Enable Nginx Caching
Edit nginx config dan tambahkan:
```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=rasa_cache:10m max_size=100m inactive=60m;

location / {
    proxy_cache rasa_cache;
    proxy_cache_valid 200 10m;
    # ... proxy_pass config lainnya
}
```

### 3. Monitor Resource Usage
```bash
# CPU & Memory
htop

# Disk usage
df -h
```

## Security Checklist

- ✅ Ganti SECRET_KEY dengan random string yang kuat
- ✅ Enable HTTPS/SSL
- ✅ Setup firewall (UFW):
  ```bash
  ufw allow 22
  ufw allow 80
  ufw allow 443
  ufw enable
  ```
- ✅ Disable root SSH login (edit `/etc/ssh/sshd_config`)
- ✅ Setup fail2ban untuk proteksi brute force
- ✅ Regular update sistem: `apt update && apt upgrade`

## Support

Jika ada masalah, cek:
1. Application logs: `journalctl -u rasa -f`
2. Nginx error log: `tail -f /var/log/nginx/error.log`
3. File permissions: `ls -la /var/www/rasa/`

---

**Good luck dengan deployment! 🚀**

