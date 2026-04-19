# 🎓 Student Data Management System

> A desktop ERP application for managing student records, marks, attendance, and fees — built with Python, tkinter, and SQLite.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)
![tkinter](https://img.shields.io/badge/GUI-tkinter-informational)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📸 Overview

Student ERP is a fully offline desktop application designed to help educational institutions manage student data through a clean, dark-themed GUI. It supports multi-module operations including student records, academic marks, daily attendance, and fee tracking — all backed by a local SQLite database.

---

## ✨ Features

- 🔐 **Login system** — role-based access (`admin`, `teacher`)
- 📊 **Dashboard** — live student count and system stats
- 👤 **Students module** — full CRUD with search, CSV import/export
- 📝 **Marks module** — subject-wise marks with auto grade & percentage calculation
- 📅 **Attendance module** — daily tracking with Present / Absent / Late statuses
- 💰 **Fees module** — semester-wise fee tracking with payment updates and balance summary
- 📄 **Activity log** — timestamped audit trail of all actions (`activity.log`)
- 💾 **File handling** — JSON, TXT, and CSV backup/restore via `FileHandler`

---

## 🗂️ Project Structure

```
student-erp/
│
├── main.py           # Multi-screen tkinter GUI (Login, Dashboard, 4 modules)
├── database.py       # Database class — all SQLite CRUD operations
├── models.py         # OOP models: Student, Marks, Attendance, Fee, FileHandler
│                     # + custom exceptions
├── students.db       # SQLite database (auto-created on first run)
├── activity.log      # Timestamped audit log
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8+**
- No third-party packages required — uses only the Python standard library (`tkinter`, `sqlite3`, `csv`, `json`)



### Default Credentials

| Role    | Username  | Password   |
|---------|-----------|------------|
| Admin   | `admin`   | `admin123` |
| Teacher | `teacher` | `teach456` |

---

## 🏗️ Architecture

```
main.py (GUI Layer)
    │
    ├── LoginPage
    ├── DashboardPage
    ├── StudentsPage      ─── CSV Import / Export
    ├── MarksPage
    ├── AttendancePage
    └── FeesPage
          │
          ▼
    database.py (Data Access Layer)
          │
    SQLite (students.db)
          │
    models.py (Domain Models)
    Student | Marks | Attendance | Fee | FileHandler
```

---

## 🧩 Module Details

### `models.py`
| Class | Description |
|---|---|
| `Student` | Core student record with validation and serialisation (dict, JSON, TXT, CSV) |
| `Marks` | Subject marks with auto-computed `percentage` and `grade` properties |
| `Attendance` | Daily attendance with Present / Absent / Late statuses |
| `Fee` | Semester fee records with `balance` property |
| `FileHandler` | Static methods for `.json`, `.txt`, `.csv` I/O and activity logging |
| Custom Exceptions | `DuplicateStudentError`, `StudentNotFoundError`, `ValidationError`, `FileHandlingError` |

### `database.py`
| Method group | Operations |
|---|---|
| Student CRUD | `add_student`, `get_all_students`, `get_student_by_id`, `update_student`, `delete_student` |
| Marks | `add_marks`, `get_marks`, `get_marks_summary`, `delete_marks` |
| Attendance | `add_attendance`, `get_attendance`, `get_attendance_summary`, `delete_attendance` |
| Fees | `add_fee`, `get_fees`, `update_fee_payment`, `get_fee_summary` |
| Import / Export | `export_csv`, `import_csv` |

### Database Schema
```sql
students   — id, student_id (UNIQUE), name, department, year, email, phone, gpa
marks      — id, student_id (FK), subject, marks_obtained, max_marks, exam_type
attendance — id, student_id (FK), date, subject, status
fees       — id, student_id (FK), semester, amount_due, amount_paid, status, due_date
```
Foreign keys are enforced with `ON DELETE CASCADE`.

---

## 📊 Grading Scale

| Grade | Percentage |
|-------|-----------|
| O     | ≥ 90%     |
| A+    | ≥ 80%     |
| A     | ≥ 70%     |
| B+    | ≥ 60%     |
| B     | ≥ 50%     |
| C     | ≥ 40%     |
| F     | < 40%     |

---

## 📁 File Handling

The system supports multiple file formats for data persistence and backup:

| Format | Purpose |
|--------|---------|
| `.db` (SQLite) | Primary storage — all live data |
| `.csv` | Import/export student records in bulk |
| `.json` | Full backup and restore of student data |
| `.txt` | Pipe-delimited plain text backup |
| `activity.log` | Append-only audit trail |

---

## 🎨 UI Theme

The GUI uses a custom dark theme built entirely with `tkinter`:

| Token | Colour |
|-------|--------|
| Background | `#0f1117` |
| Panel | `#1a1d27` |
| Accent | `#e8c547` (gold) |
| Teal | `#4ecdc4` |
| Success | `#4caf78` |
| Danger | `#e05252` |

---

## 📚 Academic Scope (Micro Project-01)

| Course Outcome | Implementation |
|---|---|
| **CO1** — Data structures & control statements | `Student.to_dict()`, lists, tuples; `validate()` methods, loops, `try/except` |
| **CO2** — File handling | `FileHandler`: `.json`, `.txt`, `.csv`, `activity.log` |
| **CO4** — Database operations | `Database` class: schema creation, parameterised CRUD, foreign keys |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.