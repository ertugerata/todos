# 1. Python'un hafif (slim) sürümünü baz al
FROM python:3.9-slim

# 2. Çalışma dizinini ayarla
WORKDIR /app

# 3. Önce gereksinimleri kopyala (Docker cache mantığı için önemli)
COPY requirements.txt .

# 4. Kütüphaneleri yükle
RUN pip install --no-cache-dir -r requirements.txt

# 5. Tüm proje dosyalarını kopyala
COPY . .

# 6. Flask'ın varsayılan portunu dışarı aç
EXPOSE 5000

# 7. Uygulamayı başlat
CMD ["python", "app.py"]
