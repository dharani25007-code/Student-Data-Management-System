"""
database.py — Database Access Layer
Student Data Management System | Micro Project - 01
CO4: Database operations — schema creation, CRUD, parameterised queries
"""

import sqlite3
import csv
from models import (Student, Marks, Attendance, Fee,
                    DuplicateStudentError, StudentNotFoundError,
                    ValidationError, FileHandlingError)


DB_FILE = "students.db"


class Database:
    """
    Manages all SQLite database operations (CO4).
    Uses context managers for safe connection handling.
    """

    def __init__(self, db_path: str = DB_FILE):
        self.db_path = db_path
        self._init_schema()

    # ── Connection helper ────────────────────

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    # ── Schema creation ──────────────────────

    def _init_schema(self):
        with self._conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS students (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id  TEXT    UNIQUE NOT NULL,
                    name        TEXT    NOT NULL,
                    department  TEXT    NOT NULL,
                    year        INTEGER NOT NULL,
                    email       TEXT    DEFAULT '',
                    phone       TEXT    DEFAULT '',
                    gpa         REAL    DEFAULT 0.0,
                    created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS marks (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id      TEXT    NOT NULL,
                    subject         TEXT    NOT NULL,
                    marks_obtained  REAL    NOT NULL,
                    max_marks       REAL    DEFAULT 100,
                    exam_type       TEXT    DEFAULT 'Internal',
                    FOREIGN KEY (student_id) REFERENCES students(student_id)
                        ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS attendance (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id  TEXT    NOT NULL,
                    date        TEXT    NOT NULL,
                    subject     TEXT    NOT NULL,
                    status      TEXT    DEFAULT 'Present',
                    FOREIGN KEY (student_id) REFERENCES students(student_id)
                        ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS fees (
                    id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id   TEXT    NOT NULL,
                    semester     INTEGER NOT NULL,
                    amount_due   REAL    NOT NULL,
                    amount_paid  REAL    DEFAULT 0.0,
                    status       TEXT    DEFAULT 'Pending',
                    due_date     TEXT    DEFAULT '',
                    FOREIGN KEY (student_id) REFERENCES students(student_id)
                        ON DELETE CASCADE
                );
            """)

    # ══════════════════════════════════════════
    #  STUDENT CRUD
    # ══════════════════════════════════════════

    def add_student(self, student: Student) -> Student:
        try:
            with self._conn() as conn:
                cur = conn.execute("""
                    INSERT INTO students
                        (student_id, name, department, year, email, phone, gpa)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (student.student_id, student.name, student.department,
                      student.year, student.email, student.phone, student.gpa))
                student.db_id = cur.lastrowid
                return student
        except sqlite3.IntegrityError:
            raise DuplicateStudentError(
                f"Student ID '{student.student_id}' already exists."
            )

    def get_all_students(self, search: str = "") -> list:
        with self._conn() as conn:
            if search:
                like = f"%{search}%"
                rows = conn.execute("""
                    SELECT * FROM students
                    WHERE student_id LIKE ? OR name LIKE ? OR department LIKE ?
                    ORDER BY name
                """, (like, like, like)).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM students ORDER BY name"
                ).fetchall()
        return [self._row_to_student(r) for r in rows]

    def get_student_by_id(self, student_id: str) -> Student:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM students WHERE student_id = ?", (student_id,)
            ).fetchone()
        if not row:
            raise StudentNotFoundError(
                f"No student found with ID '{student_id}'."
            )
        return self._row_to_student(row)

    def update_student(self, student: Student):
        with self._conn() as conn:
            conn.execute("""
                UPDATE students
                SET student_id=?, name=?, department=?, year=?,
                    email=?, phone=?, gpa=?
                WHERE id=?
            """, (student.student_id, student.name, student.department,
                  student.year, student.email, student.phone,
                  student.gpa, student.db_id))

    def delete_student(self, db_id: int):
        with self._conn() as conn:
            conn.execute("DELETE FROM students WHERE id=?", (db_id,))

    def student_count(self) -> int:
        with self._conn() as conn:
            return conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]

    @staticmethod
    def _row_to_student(row) -> Student:
        return Student(
            db_id      = row["id"],
            student_id = row["student_id"],
            name       = row["name"],
            department = row["department"],
            year       = row["year"],
            email      = row["email"],
            phone      = row["phone"],
            gpa        = row["gpa"],
        )

    # ══════════════════════════════════════════
    #  MARKS CRUD
    # ══════════════════════════════════════════

    def add_marks(self, m: Marks) -> Marks:
        with self._conn() as conn:
            cur = conn.execute("""
                INSERT INTO marks (student_id, subject, marks_obtained, max_marks, exam_type)
                VALUES (?, ?, ?, ?, ?)
            """, (m.student_id, m.subject, m.marks_obtained, m.max_marks, m.exam_type))
            m.db_id = cur.lastrowid
            return m

    def get_marks(self, student_id: str) -> list:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM marks WHERE student_id=? ORDER BY subject",
                (student_id,)
            ).fetchall()
        return [Marks(r["student_id"], r["subject"], r["marks_obtained"],
                      r["max_marks"], r["exam_type"], r["id"]) for r in rows]

    def delete_marks(self, mark_id: int):
        with self._conn() as conn:
            conn.execute("DELETE FROM marks WHERE id=?", (mark_id,))

    def get_marks_summary(self, student_id: str) -> dict:
        marks = self.get_marks(student_id)
        if not marks:
            return {"total": 0, "obtained": 0, "percentage": 0, "grades": []}
        total    = sum(m.max_marks for m in marks)
        obtained = sum(m.marks_obtained for m in marks)
        pct      = round((obtained / total) * 100, 2) if total else 0
        return {
            "total":      total,
            "obtained":   obtained,
            "percentage": pct,
            "grades":     [(m.subject, m.grade, m.percentage) for m in marks],
        }

    # ══════════════════════════════════════════
    #  ATTENDANCE CRUD
    # ══════════════════════════════════════════

    def add_attendance(self, a: Attendance) -> Attendance:
        with self._conn() as conn:
            cur = conn.execute("""
                INSERT INTO attendance (student_id, date, subject, status)
                VALUES (?, ?, ?, ?)
            """, (a.student_id, a.date_str, a.subject, a.status))
            a.db_id = cur.lastrowid
            return a

    def get_attendance(self, student_id: str) -> list:
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT * FROM attendance WHERE student_id=?
                ORDER BY date DESC
            """, (student_id,)).fetchall()
        return [Attendance(r["student_id"], r["date"], r["subject"],
                           r["status"], r["id"]) for r in rows]

    def get_attendance_summary(self, student_id: str) -> dict:
        records = self.get_attendance(student_id)
        if not records:
            return {"total": 0, "present": 0, "absent": 0, "late": 0, "percentage": 0}
        total   = len(records)
        present = sum(1 for r in records if r.status == Attendance.STATUS_PRESENT)
        absent  = sum(1 for r in records if r.status == Attendance.STATUS_ABSENT)
        late    = sum(1 for r in records if r.status == Attendance.STATUS_LATE)
        pct     = round(((present + late * 0.5) / total) * 100, 2)
        return {"total": total, "present": present,
                "absent": absent, "late": late, "percentage": pct}

    def delete_attendance(self, att_id: int):
        with self._conn() as conn:
            conn.execute("DELETE FROM attendance WHERE id=?", (att_id,))

    # ══════════════════════════════════════════
    #  FEE CRUD
    # ══════════════════════════════════════════

    def add_fee(self, fee: Fee) -> Fee:
        with self._conn() as conn:
            cur = conn.execute("""
                INSERT INTO fees (student_id, semester, amount_due, amount_paid, status, due_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (fee.student_id, fee.semester, fee.amount_due,
                  fee.amount_paid, fee.status, fee.due_date))
            fee.db_id = cur.lastrowid
            return fee

    def get_fees(self, student_id: str) -> list:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM fees WHERE student_id=? ORDER BY semester",
                (student_id,)
            ).fetchall()
        return [Fee(r["student_id"], r["semester"], r["amount_due"],
                    r["amount_paid"], r["status"], r["due_date"], r["id"])
                for r in rows]

    def update_fee_payment(self, fee_id: int, amount_paid: float, status: str):
        with self._conn() as conn:
            conn.execute("""
                UPDATE fees SET amount_paid=?, status=? WHERE id=?
            """, (amount_paid, status, fee_id))

    def get_fee_summary(self, student_id: str) -> dict:
        fees = self.get_fees(student_id)
        if not fees:
            return {"total_due": 0, "total_paid": 0, "balance": 0, "pending_sems": 0}
        return {
            "total_due":   sum(f.amount_due  for f in fees),
            "total_paid":  sum(f.amount_paid for f in fees),
            "balance":     sum(f.balance     for f in fees),
            "pending_sems": sum(1 for f in fees if f.status != Fee.STATUS_PAID),
        }

    # ══════════════════════════════════════════
    #  CSV IMPORT / EXPORT
    # ══════════════════════════════════════════

    def export_csv(self, filepath: str, search: str = ""):
        students = self.get_all_students(search)
        headers  = ["Student ID", "Name", "Department", "Year",
                    "Email", "Phone", "GPA"]
        try:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                for s in students:
                    writer.writerow([s.student_id, s.name, s.department,
                                     s.year, s.email, s.phone, s.gpa])
        except OSError as e:
            raise FileHandlingError(f"Cannot write CSV: {e}")
        return len(students)

    def import_csv(self, filepath: str) -> tuple:
        inserted = skipped = errors = 0
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        s = Student(
                            student_id = row["Student ID"].strip(),
                            name       = row["Name"].strip(),
                            department = row["Department"].strip(),
                            year       = int(row["Year"]),
                            email      = row.get("Email", "").strip(),
                            phone      = row.get("Phone", "").strip(),
                            gpa        = float(row.get("GPA", 0) or 0),
                        )
                        self.add_student(s)
                        inserted += 1
                    except DuplicateStudentError:
                        skipped += 1
                    except Exception:
                        errors += 1
        except OSError as e:
            raise FileHandlingError(f"Cannot read CSV: {e}")
        return inserted, skipped, errors