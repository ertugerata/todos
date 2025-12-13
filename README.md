# Flask + PocketBase To-Do Uygulaması 📝

Bu proje, **Python Flask** ve **PocketBase** kullanılarak geliştirilmiş; kullanıcı kaydı, girişi ve kişiye özel veri saklama (CRUD) işlemlerini içeren örnek bir uygulamadır.

## 🚀 Özellikler

* **Kullanıcı Yönetimi:** Giriş (Login) ve Oturum (Session) yönetimi.
* **CRUD İşlemleri:** Görev Ekleme, Listeleme, Güncelleme (Tamamlandı/Devam) ve Silme.
* **Veri Güvenliği:** Her kullanıcı sadece kendi oluşturduğu görevleri görebilir, düzenleyebilir ve silebilir.
* **İlişkisel Veri:** Kullanıcılar ve Görevler arasında ilişki (Relation) kurulmuştur.

## 🛠️ Kurulum

### 1. Gereksinimler
* Python 3.x
* PocketBase (Tek dosya executable)

### 2. Bağımlılıkların Yüklenmesi
Proje dizininde terminali açın ve gerekli Python kütüphanelerini yükleyin:

```bash
pip install -r requirements.txt
