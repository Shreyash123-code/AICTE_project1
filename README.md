# 🛡️ Stud Safe

> **Share & Discover Student Notes** — A web platform where students can upload, browse, download, and bookmark study notes organized by engineering branch and subject.

Built as part of the **AICTE Project**.

---

## ✨ Features

- **📤 Upload Notes** — Upload PDFs, docs, images with title, description, branch & subject tagging
- **🔍 Search & Filter** — Search by title, subject, or branch; filter by branch and subject with dropdown menus
- **⬇️ Download Notes** — One-click download for any shared note
- **🔖 Bookmarks** — Save favorite notes for quick access later
- **👁️ Preview** — Preview notes in-browser before downloading
- **📊 Dashboard** — Personal dashboard showing your uploads, downloads, and bookmarks
- **🔐 Authentication** — Sign up, log in, log out, password reset via email
- **📱 Responsive** — Works on desktop, tablet, and mobile
- **🎓 Branch-wise Organization** — Notes organized by engineering branches (FE, CSE, ME, IT, Civil)

---

## 🛠️ Tech Stack

| Layer     | Technology       |
|-----------|------------------|
| Backend   | Django 5.2       |
| Database  | SQLite           |
| Frontend  | HTML, CSS, JS    |
| Fonts     | Google Fonts (Inter) |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/Shreyash123-code/AICTE_project1.git
cd AICTE_project1

# 2. Create a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
cd studproject
python manage.py migrate

# 5. Populate branches & subjects
python manage.py populate_subjects

# 6. Create a superuser (optional)
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 📁 Project Structure

```
AICTE_project1/
├── studproject/
│   ├── studproject/        # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── studapp/            # Main application
│   │   ├── models.py       # Branch, Subject, Note, Bookmark models
│   │   ├── views.py        # All views (home, browse, upload, dashboard, etc.)
│   │   ├── forms.py        # Upload & auth forms
│   │   ├── urls.py         # App URL routes
│   │   ├── admin.py        # Admin configuration
│   │   ├── templates/      # HTML templates
│   │   ├── static/         # CSS & static assets
│   │   └── management/     # Custom management commands
│   ├── media/              # Uploaded files
│   └── db.sqlite3          # SQLite database
├── requirements.txt
└── README.md
```

---

## 📌 Engineering Branches & Subjects

The app comes pre-loaded with **5 branches** and **88 subjects**:

- **First Year (FE)** — Engg. Math, Mechanics, Chemistry, Physics, etc.
- **Computer Engineering** — Data Structures, OS, DBMS, ML, Web Dev, etc.
- **Mechanical Engineering** — Thermodynamics, Fluid Mechanics, CAD/CAM, etc.
- **Information Technology** — Networking, Cyber Security, Cloud Computing, etc.
- **Civil Engineering** — Structural Analysis, Surveying, Concrete Tech, etc.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available for educational purposes.

---

Made with ❤️ by students, for students.
