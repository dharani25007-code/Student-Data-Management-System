"""
models.py — OOP Data Models
Student Data Management System | Micro Project - 01
CO1: Data structures, CO2: File handling, CO4: Database operations
"""

import json
import os
from datetime import date


# ─────────────────────────────────────────────
#  CUSTOM EXCEPTIONS
# ─────────────────────────────────────────────

class StudentError(Exception):
    """Base exception for student management errors."""
    pass

class DuplicateStudentError(StudentError):
    """Raised when a student ID already exists."""
    pass

class StudentNotFoundError(StudentError):
    """Raised when a student record cannot be found."""
    pass

class ValidationError(StudentError):
    """Raised when input data fails validation."""
    pass

class FileHandlingError(StudentError):
    """Raised when file read/write operations fail."""
    pass


# ─────────────────────────────────────────────
#  STUDENT MODEL
# ─────────────────────────────────────────────

class Student:
    """Represents a single student record."""

    VALID_YEARS = [1, 2, 3, 4]
    DEPARTMENTS = [
        "Computer Science", "Information Technology",
        "Electronics", "Mechanical", "Civil",
        "Electrical", "Chemical", "Biotechnology"
    ]

    def __init__(self, student_id, name, department, year,
                 email="", phone="", gpa=0.0, db_id=None):
        self.db_id      = db_id
        self.student_id = student_id
        self.name       = name
        self.department = department
        self.year       = year
        self.email      = email
        self.phone      = phone
        self.gpa        = gpa

    # ── Validation ───────────────────────────

    @classmethod
    def validate(cls, student_id, name, department, year, gpa=""):
        errors = []
        if not str(student_id).strip():
            errors.append("Student ID is required.")
        if not str(name).strip():
            errors.append("Name is required.")
        if department not in cls.DEPARTMENTS:
            errors.append(f"Department must be one of: {', '.join(cls.DEPARTMENTS)}")
        try:
            y = int(year)
            if y not in cls.VALID_YEARS:
                errors.append("Year must be 1, 2, 3, or 4.")
        except (ValueError, TypeError):
            errors.append("Year must be a number.")
        if gpa not in ("", None):
            try:
                g = float(gpa)
                if not (0.0 <= g <= 10.0):
                    errors.append("GPA must be between 0.0 and 10.0.")
            except (ValueError, TypeError):
                errors.append("GPA must be a numeric value.")
        if errors:
            raise ValidationError("\n".join(errors))

    # ── Serialisation ────────────────────────

    def to_dict(self):
        return {
            "student_id":  self.student_id,
            "name":        self.name,
            "department":  self.department,
            "year":        self.year,
            "email":       self.email,
            "phone":       self.phone,
            "gpa":         self.gpa,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            student_id  = d["student_id"],
            name        = d["name"],
            department  = d["department"],
            year        = int(d["year"]),
            email       = d.get("email", ""),
            phone       = d.get("phone", ""),
            gpa         = float(d.get("gpa", 0)),
        )

    def to_text_line(self):
        """Single-line text representation for .txt file storage."""
        return (f"{self.student_id}|{self.name}|{self.department}|"
                f"{self.year}|{self.email}|{self.phone}|{self.gpa}\n")

    @classmethod
    def from_text_line(cls, line):
        """Parse a student from a text file line."""
        parts = line.strip().split("|")
        if len(parts) < 7:
            raise ValidationError(f"Malformed record line: {line!r}")
        return cls(
            student_id  = parts[0],
            name        = parts[1],
            department  = parts[2],
            year        = int(parts[3]),
            email       = parts[4],
            phone       = parts[5],
            gpa         = float(parts[6]),
        )

    def __repr__(self):
        return f"<Student {self.student_id} — {self.name}>"


# ─────────────────────────────────────────────
#  MARKS MODEL
# ─────────────────────────────────────────────

class Marks:
    """Stores subject-wise marks for a student."""

    MAX_MARK = 100

    def __init__(self, student_id, subject, marks_obtained,
                 max_marks=100, exam_type="Internal", db_id=None):
        self.db_id          = db_id
        self.student_id     = student_id
        self.subject        = subject
        self.marks_obtained = float(marks_obtained)
        self.max_marks      = float(max_marks)
        self.exam_type      = exam_type

    @property
    def percentage(self):
        if self.max_marks == 0:
            return 0.0
        return round((self.marks_obtained / self.max_marks) * 100, 2)

    @property
    def grade(self):
        p = self.percentage
        if p >= 90: return "O"
        if p >= 80: return "A+"
        if p >= 70: return "A"
        if p >= 60: return "B+"
        if p >= 50: return "B"
        if p >= 40: return "C"
        return "F"

    @classmethod
    def validate(cls, marks_obtained, max_marks=100):
        errors = []
        try:
            m = float(marks_obtained)
            mx = float(max_marks)
            if m < 0 or m > mx:
                errors.append(f"Marks must be between 0 and {mx}.")
        except (ValueError, TypeError):
            errors.append("Marks must be numeric.")
        if errors:
            raise ValidationError("\n".join(errors))

    def to_dict(self):
        return {
            "student_id":     self.student_id,
            "subject":        self.subject,
            "marks_obtained": self.marks_obtained,
            "max_marks":      self.max_marks,
            "exam_type":      self.exam_type,
            "percentage":     self.percentage,
            "grade":          self.grade,
        }

    def __repr__(self):
        return f"<Marks {self.student_id} | {self.subject}: {self.marks_obtained}/{self.max_marks}>"


# ─────────────────────────────────────────────
#  ATTENDANCE MODEL
# ─────────────────────────────────────────────

class Attendance:
    """Tracks daily attendance for a student."""

    STATUS_PRESENT = "Present"
    STATUS_ABSENT  = "Absent"
    STATUS_LATE    = "Late"
    VALID_STATUSES = [STATUS_PRESENT, STATUS_ABSENT, STATUS_LATE]

    def __init__(self, student_id, date_str, subject,
                 status=STATUS_PRESENT, db_id=None):
        self.db_id      = db_id
        self.student_id = student_id
        self.date_str   = date_str      # YYYY-MM-DD string
        self.subject    = subject
        self.status     = status

    @classmethod
    def today(cls, student_id, subject, status=STATUS_PRESENT):
        return cls(student_id, str(date.today()), subject, status)

    @classmethod
    def validate(cls, status):
        if status not in cls.VALID_STATUSES:
            raise ValidationError(
                f"Status must be one of: {', '.join(cls.VALID_STATUSES)}"
            )

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "date":       self.date_str,
            "subject":    self.subject,
            "status":     self.status,
        }

    def __repr__(self):
        return f"<Attendance {self.student_id} | {self.date_str} | {self.status}>"


# ─────────────────────────────────────────────
#  FEE MODEL
# ─────────────────────────────────────────────

class Fee:
    """Tracks fee payment records for a student."""

    STATUS_PAID    = "Paid"
    STATUS_PENDING = "Pending"
    STATUS_PARTIAL = "Partial"
    VALID_STATUSES = [STATUS_PAID, STATUS_PENDING, STATUS_PARTIAL]

    def __init__(self, student_id, semester, amount_due,
                 amount_paid=0.0, status=STATUS_PENDING,
                 due_date="", db_id=None):
        self.db_id       = db_id
        self.student_id  = student_id
        self.semester    = semester
        self.amount_due  = float(amount_due)
        self.amount_paid = float(amount_paid)
        self.status      = status
        self.due_date    = due_date

    @property
    def balance(self):
        return round(self.amount_due - self.amount_paid, 2)

    @classmethod
    def validate(cls, amount_due, amount_paid):
        errors = []
        try:
            d = float(amount_due)
            p = float(amount_paid)
            if d < 0:
                errors.append("Amount due cannot be negative.")
            if p < 0:
                errors.append("Amount paid cannot be negative.")
            if p > d:
                errors.append("Amount paid cannot exceed amount due.")
        except (ValueError, TypeError):
            errors.append("Amounts must be numeric.")
        if errors:
            raise ValidationError("\n".join(errors))

    def to_dict(self):
        return {
            "student_id":  self.student_id,
            "semester":    self.semester,
            "amount_due":  self.amount_due,
            "amount_paid": self.amount_paid,
            "balance":     self.balance,
            "status":      self.status,
            "due_date":    self.due_date,
        }

    def __repr__(self):
        return f"<Fee {self.student_id} | Sem {self.semester} | {self.status}>"


# ─────────────────────────────────────────────
#  FILE HANDLING UTILITIES  (CO2)
# ─────────────────────────────────────────────

class FileHandler:
    """
    Handles flat-file persistence (CO2 — File Handling).
    Supports .json and .txt formats for student backup/export.
    """

    @staticmethod
    def save_json(students: list, filepath: str):
        """Save a list of Student objects to a JSON file."""
        try:
            data = [s.to_dict() for s in students]
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except OSError as e:
            raise FileHandlingError(f"Cannot write JSON file: {e}")

    @staticmethod
    def load_json(filepath: str) -> list:
        """Load Student objects from a JSON file."""
        if not os.path.exists(filepath):
            raise FileHandlingError(f"File not found: {filepath}")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Student.from_dict(d) for d in data]
        except (json.JSONDecodeError, KeyError) as e:
            raise FileHandlingError(f"Invalid JSON file: {e}")

    @staticmethod
    def save_txt(students: list, filepath: str):
        """Save students to a pipe-delimited .txt file."""
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("# Student Data Management System — Text Backup\n")
                f.write("# Format: student_id|name|department|year|email|phone|gpa\n")
                for s in students:
                    f.write(s.to_text_line())
        except OSError as e:
            raise FileHandlingError(f"Cannot write text file: {e}")

    @staticmethod
    def load_txt(filepath: str) -> list:
        """Load students from a pipe-delimited .txt file."""
        if not os.path.exists(filepath):
            raise FileHandlingError(f"File not found: {filepath}")
        students = []
        errors   = []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for lineno, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    try:
                        students.append(Student.from_text_line(line))
                    except (ValidationError, ValueError) as e:
                        errors.append(f"Line {lineno}: {e}")
        except OSError as e:
            raise FileHandlingError(f"Cannot read text file: {e}")
        if errors:
            print(f"[FileHandler] Skipped {len(errors)} bad lines: {errors}")
        return students

    @staticmethod
    def append_log(message: str, logfile: str = "activity.log"):
        """Append a timestamped entry to the activity log."""
        from datetime import datetime
        try:
            with open(logfile, "a", encoding="utf-8") as f:
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{ts}] {message}\n")
        except OSError:
            pass  # Logging failure should never crash the app