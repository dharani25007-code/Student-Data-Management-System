<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f1117,50:4ecdc4,100:0f1117&height=200&section=header&text=Student%20ERP&fontSize=50&fontColor=ffffff&fontAlignY=40&desc=Desktop%20Student%20Data%20Management%20System&descAlignY=60&descSize=18&animation=fadeIn"/>
</div>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![tkinter](https://img.shields.io/badge/GUI-tkinter-4ecdc4?style=for-the-badge)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> 🎓 A fully offline desktop ERP for managing student records, marks, attendance, and fees — dark-themed, role-based, and built entirely on the Python standard library.

</div>

---

## 📌 Overview

Student ERP is a multi-screen desktop application with a clean dark-themed GUI. It supports full CRUD operations across four modules — Students, Marks, Attendance, and Fees — all backed by a local SQLite database with foreign key enforcement.

---

## ✨ Features

| Module | What it does |
|---|---|
| 🔐 **Login** | Role-based access — `admin` and `teacher` |
| 📊 **Dashboard** | Live student count and system overview |
| 👤 **Students** | Full CRUD — add, edit, delete, search, CSV import/export |
| 📝 **Marks** | Subject-wise marks with auto grade & percentage calculation |
| 📅 **Attendance** | Daily tracking — Present / Absent / Late |
| 💰 **Fees** | Semester-wise fee records with payment updates & balance summary |
| 📄 **Activity Log** | Timestamped audit trail of every action |
| 💾 **File Handling** | JSON, TXT, and CSV backup/restore |

---

## 🗂️ Project Structure

```
Student-Data-Management-System/
├── main.py        # Multi-screen tkinter GUI (Login, Dashboard, 4 modules)
├── database.py    # Database class — all SQLite CRUD operations
├── models.py      # OOP models: Student, Marks, Attendance, Fee, FileHandler
│                  # + custom exceptions
├── students.db    # SQLite database (auto-created on first run)
├── activity.log   # Timestamped audit log
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python **3.8+**
- No third-party packages — uses only standard library (`tkinter`, `sqlite3`, `csv`, `json`)

### Run
```bash
git clone https://github.com/dharani25007-code/Student-Data-Management-System.git
cd Student-Data-Management-System
python main.py
```

### Default Credentials

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| Teacher | `teacher` | `teach456` |

---

## 🏗️ Architecture

```
main.py (GUI Layer)
    ├── LoginPage
    ├── DashboardPage
    ├── StudentsPage  ── CSV Import/Export
    ├── MarksPage
    ├── AttendancePage
    └── FeesPage
          ↓
    database.py (Data Access Layer)
          ↓
    SQLite — students.db
          ↓
    models.py (Domain Models)
    Student | Marks | Attendance | Fee | FileHandler
```

---

## 📊 Grading Scale

| Grade | Percentage |
|---|---|
| O | ≥ 90% |
| A+ | ≥ 80% |
| A | ≥ 70% |
| B+ | ≥ 60% |
| B | ≥ 50% |
| C | ≥ 40% |
| F | < 40% |

---

## 🎨 UI Theme (Dark)

| Token | Colour |
|---|---|
| Background | `#0f1117` |
| Panel | `#1a1d27` |
| Accent | `#e8c547` (gold) |
| Teal | `#4ecdc4` |
| Success | `#4caf78` |
| Danger | `#e05252` |

---

## 📚 Academic Scope

| Course Outcome | Implementation |
|---|---|
| **CO1** Data structures | `Student.to_dict()`, lists, tuples, validate loops |
| **CO2** File handling | `FileHandler` — `.json`, `.txt`, `.csv`, `activity.log` |
| **CO4** Database ops | Schema creation, parameterised CRUD, foreign keys |

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:4ecdc4,100:0f1117&height=120&section=footer"/>

**Built by [Dharanidharan M](https://github.com/dharani25007-code)
</div>
