# Campus-Navigate-3D — Backend (Django)

[![Project Status](https://img.shields.io/badge/Status-In_Development-yellow)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Українська](https://img.shields.io/badge/Мова-Українська-brightgreen)](README.md)

[![Fullstack](https://img.shields.io/badge/Integration-Fullstack-blueviolet)]()
[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-yellowgreen?logo=django)](https://www.django-rest-framework.org/)

REST-API для керування 3D-навігацією по університетському комплексу:  
- Автоматичні маршрути (обліт точок)  
- Вільний політ  
- Адмін-панель для додавання та редагування локацій  
- Ендпоінт для завантаження актуальної 3D-моделі

---

## ✨ Основні можливості
- 📍 **FlightLocation API**  
  - Список точок (`GET /api/locations/`)  
  - Деталі точки (`GET /api/locations/{id}/`)

- 🗺 **Active Model File Endpoint**  
  - Повертає актуальний `.glb` файл моделі (`GET /api/active-model-file/`)

- 🔐 **Адмін-панель**  
  - Універсальна модель `FlightType`, `FlightPath`, `FlightPoint`  
  - Відмітка активної 3D-моделі (`is_active`)  
  - Інлайн-редагування точок обльоту

---

## 🤝 Взаємодія з фронтендом
Цей бекенд розроблений для роботи разом з [фронтенд-додатком на React](https://github.com/Zebaro24/Campus-Navigate-3D-FE).
Ключові точки інтеграції:
- Фронтенд використовує `/api/locations/` для отримання точок навігації
- 3D-модель завантажується через `/api/active-model-file/`

---

## 🛠 Технології
- **Python 3.10+**  
- **Django 4.2**  
- **Django REST Framework**  
- **django-cors-headers** (CORS)  
- **SQLite / PostgreSQL**  
- **FileResponse** для доставки `.glb` файлу

---

## 🚀 Установка та запуск

1. **Клонування репозиторію**  
   ```bash
   git clone https://github.com/Zebaro24/Campus-Navigate-3D-BE.git backend
   cd backend
   ```

2. **Віртуальне оточення та залежності**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   pip install -r requirements.txt
   ```

3. **Міграції та створення суперкористувача**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Запуск сервера**

   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

---

## 🔍 Тестування API

* **Список локацій**
  `GET http://localhost:8000/api/locations/`

* **Деталі локації**
  `GET http://localhost:8000/api/locations/1/`

* **Отримати активну модель**
  `GET http://localhost:8000/api/active-model-file/`
  — повертає `.glb` файл з кеш-заголовками

---

## 📧 Контакти
- **Автор**: Денис Щербатий
- **Пошта**: zebaro.work@gmail.com