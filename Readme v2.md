# Student Data Management System — v2 (100% Scope)
### Micro Project-01 | Software Development & Education Technology

## Run the app
```
python main.py
```
Default login: **admin / admin123**

## File structure
| File | Purpose |
|---|---|
| `main.py` | Multi-screen GUI — Login, Dashboard, Students, Marks, Attendance, Fees |
| `database.py` | `Database` class — all SQLite CRUD operations (CO4) |
| `models.py` | `Student`, `Marks`, `Attendance`, `Fee` classes + `FileHandler` + custom exceptions (CO1, CO2) |

## Scope coverage
| Requirement | Where |
|---|---|
| Data structures | `models.py` — dicts, lists, tuples throughout |
| Control statements | Validation loops, if/else, try/except in every class |
| File handling | `FileHandler`: JSON save/load, TXT save/load, CSV import/export, activity.log |
| GUI programming | `main.py` — Login, Dashboard, 4 module screens, sidebar nav |
| Database operations | `database.py` — schema creation, INSERT, SELECT, UPDATE, DELETE |
| CRUD on student records | Full add/update/delete/search on Students page |
| ERP simulation | Marks module, Attendance module, Fees module |
| OOP design | Classes: Student, Marks, Attendance, Fee, FileHandler, Database, App, each Page |
| Custom exceptions | DuplicateStudentError, StudentNotFoundError, ValidationError, FileHandlingError |
| Entry-level career readiness | Modular structure, docstrings, parameterised SQL, separation of concerns |

## COs Addressed
- **CO1** — Data structures (Student.to_dict, lists, tuples), control statements (validate methods, loops, try/except)
- **CO2** — File handling (FileHandler: .json, .txt, .csv, activity.log)
- **CO4** — Database (Database class: schema creation, all CRUD, foreign keys, parameterised queries)