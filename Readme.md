<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=Student%20Data%20Management%20System&fontSize=38&fontColor=fff&animation=twinkling&fontAlignY=35&desc=Desktop%20ERP%20for%20Educational%20Institutions&descAlignY=58&descSize=18" width="100%"/>
<br/>
[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3000&pause=800&color=E8C547&center=true&vCenter=true&multiline=false&width=700&lines=🎓+Student+Records+Management;📝+Marks+%26+Grade+Tracking;📅+Daily+Attendance+Monitoring;💰+Fee+%26+Payment+Management;🔐+Role-Based+Login+System;📊+CSV+Import+%2F+Export;🌙+Dark-Themed+Desktop+GUI)](https://git.io/typing-svg)

<br/>

<p>
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/GUI-tkinter-informational?style=for-the-badge&logo=python&logoColor=white&color=0d7377" alt="tkinter"/>
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"/>
  <img src="https://img.shields.io/badge/License-MIT-4caf78?style=for-the-badge" alt="MIT License"/>
  <img src="https://img.shields.io/badge/Platform-Desktop-e8c547?style=for-the-badge&logo=windows&logoColor=black" alt="Desktop"/>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" alt="Status"/>
</p>

<p>
  <img src="https://img.shields.io/badge/Modules-4%20Core%20Modules-4ecdc4?style=flat-square" alt="Modules"/>
  <img src="https://img.shields.io/badge/Roles-Admin%20%7C%20Teacher-e8c547?style=flat-square" alt="Roles"/>
  <img src="https://img.shields.io/badge/Storage-100%25%20Offline-4caf78?style=flat-square" alt="Offline"/>
  <img src="https://img.shields.io/badge/Dependencies-Zero%20External-e05252?style=flat-square" alt="Dependencies"/>
</p>

</div>

---

<div align="center">

## 🌟 What is Student ERP?

</div>

**Student Data Management System** is a fully offline desktop ERP application designed to help educational institutions manage student data through a clean, dark-themed GUI. Built entirely with Python's standard library — no external dependencies required — it delivers a complete suite of administrative tools for managing student records, academic performance, daily attendance, and fee collection.

> 💡 **Zero setup friction** — install Python 3.8+, run `main.py`, and you're ready to go.

<div align="center">

```
🏫 Designed for Educational Institutions · Administrators · Teachers
```

</div>

---

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=6,11,20&height=3&section=header" width="100%"/>

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🔐 Role-Based Login
- Secure credential validation
- **Admin** — full access to all modules
- **Teacher** — read + attendance/marks entry
- Session-aware navigation sidebar

### 👤 Student Records Management
- Full **CRUD** operations
- Unique Student ID system
- Department, Year, GPA tracking
- Real-time search & filter
- **CSV bulk import/export**

### 📝 Marks & Grade Tracking
- Subject-wise marks entry
- **Auto-calculated** percentage & grade
- Multiple exam types (Mid, Final, Internal)
- Performance summary view

</td>
<td width="50%">

### 📅 Attendance Management
- Daily per-subject tracking
- Three statuses: **Present / Absent / Late**
- Date-range attendance summary
- Attendance percentage calculation

### 💰 Fee Management
- Semester-wise fee records
- Payment updates with balance tracking
- Fee status: **Paid / Partial / Unpaid**
- Financial summary dashboard

### 📄 Audit & Backup
- Timestamped **activity.log** trail
- JSON, TXT, CSV backup & restore
- All actions logged automatically
- Foreign-key enforced data integrity

</td>
</tr>
</table>

---

<div align="center">

### 🎯 Feature Badges

![Students](https://img.shields.io/badge/📋_Students-CRUD_%2B_Search-4ecdc4?style=for-the-badge)
![Marks](https://img.shields.io/badge/📝_Marks-Auto_Grade-e8c547?style=for-the-badge)
![Attendance](https://img.shields.io/badge/📅_Attendance-Daily_Track-4caf78?style=for-the-badge)
![Fees](https://img.shields.io/badge/💰_Fees-Payment_Track-e05252?style=for-the-badge)
![CSV](https://img.shields.io/badge/📊_CSV-Import_%2F_Export-8a2be2?style=for-the-badge)
![Dark GUI](https://img.shields.io/badge/🌙_GUI-Dark_Theme-1a1d27?style=for-the-badge)

</div>

---

## 🗂️ Project Structure

```
Student-Data-Management-System/
│
├── 🖥️  main.py           # Multi-screen tkinter GUI (Login, Dashboard, 4 modules)
├── 🗄️  database.py       # Database class — all SQLite CRUD operations
├── 🧩  models.py         # OOP models: Student, Marks, Attendance, Fee, FileHandler
│                         # + custom exceptions
├── 💾  students.db       # SQLite database (auto-created on first run)
├── 📄  activity.log      # Timestamped audit log
└── 📖  README.md
```

---

## ⚙️ System Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| **Python** | 3.8 | 3.10+ |
| **OS** | Windows 7 / macOS 10.12 / Ubuntu 18.04 | Windows 10+ / macOS 12+ / Ubuntu 22.04 |
| **RAM** | 256 MB | 512 MB |
| **Disk** | 10 MB | 50 MB |
| **Display** | 1000 × 660 px | 1280 × 800 px or larger |
| **External packages** | None | None |

> ✅ Uses only Python standard library: `tkinter`, `sqlite3`, `csv`, `json`, `os`, `datetime`

---

## 🚀 Installation & Setup

### Step 1 — Clone the Repository

```bash
git clone https://github.com/dharani25007-code/Student-Data-Management-System.git
cd Student-Data-Management-System
```

### Step 2 — Verify Python Version

```bash
python --version
# Should output: Python 3.8.x or higher
```

### Step 3 — (Optional) Verify tkinter is Available

```bash
python -m tkinter
# A small test window should open — close it to continue
```

### Step 4 — Launch the Application

```bash
python main.py
```

> 🗄️ On first launch, `students.db` is auto-created with all required tables.

### Step 5 — Log In

Use the default credentials below to get started:

| Role | Username | Password | Access Level |
|---|---|---|---|
| 👑 Admin | `admin` | `admin123` | Full access — all modules + settings |
| 👩‍🏫 Teacher | `teacher` | `teach456` | Marks, Attendance, view Students |

> ⚠️ Change default passwords after your first login in a production environment.

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    main.py  (GUI Layer)                   │
│                                                           │
│  ┌──────────┐  ┌───────────┐  ┌──────────────────────┐  │
│  │LoginPage │  │ Dashboard │  │  StudentsPage        │  │
│  └──────────┘  └───────────┘  │  (CSV Import/Export) │  │
│                                └──────────────────────┘  │
│  ┌──────────────┐  ┌─────────────┐  ┌───────────────┐   │
│  │  MarksPage   │  │AttendancePage│  │   FeesPage   │   │
│  └──────────────┘  └─────────────┘  └───────────────┘   │
└──────────────────────────┬───────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│               database.py  (Data Access Layer)            │
│         Parameterised CRUD · Foreign Key Enforced        │
└──────────────────────────┬───────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
┌─────────────────────┐   ┌────────────────────────────────┐
│   students.db        │   │     models.py  (Domain Layer)  │
│   (SQLite)           │   │  Student · Marks · Attendance  │
│                      │   │  Fee · FileHandler · Exceptions│
└─────────────────────┘   └────────────────────────────────┘
```

---

## 🧩 Module Details

### `models.py` — Domain Models

| Class | Description |
|---|---|
| `Student` | Core student record — validation, `to_dict()`, `to_json()`, `to_txt()`, `to_csv_row()` |
| `Marks` | Subject marks with auto-computed `percentage` and `grade` properties |
| `Attendance` | Daily attendance record with Present / Absent / Late statuses |
| `Fee` | Semester fee record with computed `balance` property |
| `FileHandler` | Static I/O methods for `.json`, `.txt`, `.csv` and `activity.log` |
| `DuplicateStudentError` | Raised when a Student ID already exists |
| `StudentNotFoundError` | Raised when querying a non-existent student |
| `ValidationError` | Raised when model field validation fails |
| `FileHandlingError` | Raised on file I/O errors |

### `database.py` — Data Access Layer

| Method Group | Operations |
|---|---|
| **Student CRUD** | `add_student`, `get_all_students`, `get_student_by_id`, `update_student`, `delete_student` |
| **Marks** | `add_marks`, `get_marks`, `get_marks_summary`, `delete_marks` |
| **Attendance** | `add_attendance`, `get_attendance`, `get_attendance_summary`, `delete_attendance` |
| **Fees** | `add_fee`, `get_fees`, `update_fee_payment`, `get_fee_summary` |
| **Import / Export** | `export_csv`, `import_csv` |

---

## 🗄️ Database Schema

```sql
-- Student master table
CREATE TABLE students (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id  TEXT    UNIQUE NOT NULL,   -- e.g. "STU001"
    name        TEXT    NOT NULL,
    department  TEXT,
    year        INTEGER,
    email       TEXT,
    phone       TEXT,
    gpa         REAL
);

-- Academic marks
CREATE TABLE marks (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id      TEXT REFERENCES students(student_id) ON DELETE CASCADE,
    subject         TEXT,
    marks_obtained  REAL,
    max_marks       REAL,
    exam_type       TEXT    -- "Mid" | "Final" | "Internal"
);

-- Daily attendance
CREATE TABLE attendance (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id  TEXT REFERENCES students(student_id) ON DELETE CASCADE,
    date        TEXT,       -- ISO format: YYYY-MM-DD
    subject     TEXT,
    status      TEXT        -- "Present" | "Absent" | "Late"
);

-- Fee records
CREATE TABLE fees (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id   TEXT REFERENCES students(student_id) ON DELETE CASCADE,
    semester     INTEGER,
    amount_due   REAL,
    amount_paid  REAL,
    status       TEXT,      -- "Paid" | "Partial" | "Unpaid"
    due_date     TEXT
);
```

> 🔗 All child tables enforce `ON DELETE CASCADE` — deleting a student removes all related records automatically.

---

## 📖 Usage Guide

### Adding a Student

1. Log in as **Admin** or **Teacher**
2. Click **Students** in the left sidebar
3. Fill in the form fields: Student ID, Name, Department, Year, Email, Phone, GPA
4. Click **Add Student** — the record appears in the table immediately

### Importing Students via CSV

```csv
student_id,name,department,year,email,phone,gpa
STU001,Alice Johnson,Computer Science,2,alice@example.com,9876543210,8.5
STU002,Bob Smith,Electronics,3,bob@example.com,9876543211,7.2
```

1. Go to **Students** module
2. Click **Import CSV**
3. Select your `.csv` file
4. The system validates and inserts all rows — duplicates are skipped with a warning

### Recording Marks

1. Navigate to **Marks**
2. Select a student from the dropdown
3. Enter Subject, Marks Obtained, Max Marks, Exam Type
4. Click **Add Marks** — grade and percentage are computed automatically

### Marking Attendance

1. Navigate to **Attendance**
2. Select a student, date, and subject
3. Choose status: **Present**, **Absent**, or **Late**
4. Click **Save** — the record is logged with a timestamp in `activity.log`

### Processing a Fee Payment

1. Navigate to **Fees**
2. Select a student record
3. Click **Update Payment** and enter the payment amount
4. The system recalculates balance and updates the status automatically

---

## 📊 Grading Scale

| Grade | Percentage | Remark |
|---|---|---|
| **O** | ≥ 90% | Outstanding |
| **A+** | ≥ 80% | Excellent |
| **A** | ≥ 70% | Very Good |
| **B+** | ≥ 60% | Good |
| **B** | ≥ 50% | Average |
| **C** | ≥ 40% | Pass |
| **F** | < 40% | Fail |

---

## 📁 File Handling & Configuration

### Supported Formats

| Format | Purpose | Notes |
|---|---|---|
| `.db` (SQLite) | Primary live storage | Auto-created at startup |
| `.csv` | Bulk import/export | Student records only |
| `.json` | Full data backup/restore | All student fields |
| `.txt` | Pipe-delimited backup | Human-readable format |
| `activity.log` | Append-only audit trail | Every action timestamped |

### Changing Default Credentials

Default credentials are hardcoded in `main.py`. To change them, locate the `LoginPage` class and update the `USERS` dictionary:

```python
# main.py → LoginPage
USERS = {
    "admin":   {"password": "your_new_password", "role": "admin"},
    "teacher": {"password": "your_new_password", "role": "teacher"},
}
```

### Adjusting Window Size

The default window size is `1200 × 760 px` (minimum `1000 × 660 px`). Update in `main.py`:

```python
# main.py → App.__init__
self.geometry("1400x900")   # wider layout
self.minsize(1100, 700)
```

### Theme Colours

All colour tokens are defined at the top of `main.py`:

```python
BG      = "#0f1117"   # main background
PANEL   = "#1a1d27"   # card/panel background
SIDEBAR = "#141720"   # navigation sidebar
ACCENT  = "#e8c547"   # gold accent / highlights
TEAL    = "#4ecdc4"   # secondary accent
GREEN   = "#4caf78"   # success indicators
RED     = "#e05252"   # error / danger
TEXT    = "#e8e6e0"   # primary text
DIM     = "#6b6e7a"   # muted / placeholder text
```

---

## 🎨 UI Theme Overview

| Token | Hex Value | Usage |
|---|---|---|
| Background | `#0f1117` | Main window background |
| Panel | `#1a1d27` | Cards and form panels |
| Sidebar | `#141720` | Navigation sidebar |
| Accent | `#e8c547` | Gold highlights, active state |
| Teal | `#4ecdc4` | Secondary accent, icons |
| Success | `#4caf78` | Positive statuses, "Present" |
| Danger | `#e05252` | Errors, "Absent", delete actions |
| Text | `#e8e6e0` | Primary readable text |
| Dim | `#6b6e7a` | Placeholder / muted labels |

---

## 🔧 Troubleshooting

### `ModuleNotFoundError: No module named 'tkinter'`

tkinter is bundled with most Python distributions but may need to be installed on Linux:

```bash
# Debian / Ubuntu
sudo apt-get install python3-tk

# Fedora / RHEL
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

### Application Window Doesn't Open

```bash
# Check your Python version (3.8+ required)
python --version

# Run with verbose output to see any errors
python -v main.py
```

### Database Errors on Startup

If `students.db` becomes corrupted, delete it and let the app recreate it:

```bash
rm students.db      # Linux / macOS
del students.db     # Windows
python main.py      # Fresh database is created automatically
```

> ⚠️ Deleting `students.db` removes all data. Export a CSV backup first via the Students module.

### CSV Import Fails

- Ensure your CSV has the exact header row: `student_id,name,department,year,email,phone,gpa`
- Check for duplicate `student_id` values in the file
- Make sure the file is saved with **UTF-8** encoding
- Verify there are no empty required fields (`student_id` and `name` are mandatory)

### Login Fails

- Default Admin: `admin` / `admin123`
- Default Teacher: `teacher` / `teach456`
- Credentials are case-sensitive

---

## 📚 Academic Scope (Micro Project-01)

| Course Outcome | Skill Area | Implementation |
|---|---|---|
| **CO1** | Data structures & control | `Student.to_dict()`, lists, tuples, `validate()`, loops, `try/except` |
| **CO2** | File handling | `FileHandler`: `.json`, `.txt`, `.csv`, `activity.log` |
| **CO4** | Database operations | `Database` class: schema creation, parameterised CRUD, foreign keys |

---

## 🤝 Contributing

Contributions are welcome and appreciated! 🎉

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make** your changes and test them
4. **Commit** with a clear message:
   ```bash
   git commit -m "feat: add your feature description"
   ```
5. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request** on GitHub

### Contribution Ideas

- 📊 **Reports module** — PDF/Excel export of marks and attendance summaries
- 📧 **Email notifications** — fee due reminders via SMTP
- 🔒 **Password hashing** — bcrypt or hashlib integration for credentials
- 📱 **Responsive layout** — better scaling for different screen sizes
- 🌐 **Multi-language support** — i18n framework integration
- 🧪 **Unit tests** — pytest coverage for `models.py` and `database.py`

### Code Style

- Follow **PEP 8** conventions
- Add docstrings to all new classes and public methods
- Keep GUI logic in `main.py` and data logic in `database.py` / `models.py`

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```
MIT License — free to use, modify, and distribute with attribution.
```

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer&animation=twinkling" width="100%"/>

<p>
  <img src="https://img.shields.io/badge/Built%20with-Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/GUI-tkinter-0d7377?style=flat-square" alt="tkinter"/>
  <img src="https://img.shields.io/badge/DB-SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite"/>
  <img src="https://img.shields.io/badge/License-MIT-4caf78?style=flat-square" alt="MIT"/>
</p>

<p>
  <strong>🎓 Student Data Management System</strong><br/>
  <em>Empowering educational institutions with efficient data management</em>
</p>

⭐ **Star this repository** if you found it helpful!

</div>
