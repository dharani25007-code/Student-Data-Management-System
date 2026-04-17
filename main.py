"""
main.py — GUI Application (Multi-Screen tkinter)
Student Data Management System | Micro Project - 01
CO1: Data structures + control  CO2: File handling  CO4: Database ops
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

from models import (Student, Marks, Attendance, Fee,
                    FileHandler, ValidationError,
                    DuplicateStudentError, StudentNotFoundError,
                    FileHandlingError)
from database import Database


# ─────────────────────────────────────────────
#  THEME
# ─────────────────────────────────────────────

BG      = "#0f1117"
PANEL   = "#1a1d27"
SIDEBAR = "#141720"
ACCENT  = "#e8c547"
TEAL    = "#4ecdc4"
RED     = "#e05252"
GREEN   = "#4caf78"
TEXT    = "#e8e6e0"
DIM     = "#6b6e7a"
BORDER  = "#2d3143"
ROW_ODD  = "#151823"
ROW_EVEN = "#1a1d27"

FH = ("Georgia", 20, "bold")
FB = ("Courier New", 10, "bold")
FN = ("Courier New", 10)
FS = ("Courier New",  9)

DEPTS = Student.DEPARTMENTS


# ─────────────────────────────────────────────
#  HELPER WIDGETS
# ─────────────────────────────────────────────

def label(parent, text, font=FN, fg=TEXT, bg=None, **kw):
    return tk.Label(parent, text=text, font=font, fg=fg,
                    bg=bg or parent["bg"], **kw)

def entry(parent, var, **kw):
    return tk.Entry(parent, textvariable=var, font=FN,
                    bg=BG, fg=TEXT, insertbackground=ACCENT,
                    relief="flat", highlightthickness=1,
                    highlightbackground=BORDER,
                    highlightcolor=ACCENT, **kw)

def btn(parent, text, cmd, color=ACCENT, fg=BG, **kw):
    return tk.Button(parent, text=text, font=FB,
                     bg=color, fg=fg,
                     activebackground=TEXT, activeforeground=BG,
                     relief="flat", cursor="hand2",
                     command=cmd, **kw)

def combo(parent, var, values, **kw):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox",
                    fieldbackground=BG, background=BG,
                    foreground=TEXT, selectbackground=PANEL,
                    selectforeground=TEXT, arrowcolor=ACCENT)
    return ttk.Combobox(parent, textvariable=var, values=values,
                        font=FN, state="readonly", **kw)

def sep(parent, color=BORDER):
    return tk.Frame(parent, bg=color, height=1)

def card(parent, **kw):
    return tk.Frame(parent, bg=PANEL, **kw)


# ─────────────────────────────────────────────
#  TREEVIEW FACTORY
# ─────────────────────────────────────────────

def make_tree(parent, columns, headings, widths):
    style = ttk.Style()
    style.configure("T.Treeview",
                    background=ROW_ODD, foreground=TEXT,
                    fieldbackground=ROW_ODD, rowheight=26,
                    font=FS)
    style.configure("T.Treeview.Heading",
                    background=BORDER, foreground=ACCENT,
                    font=("Courier New", 9, "bold"), relief="flat")
    style.map("T.Treeview",
              background=[("selected", ACCENT)],
              foreground=[("selected", BG)])

    frame = tk.Frame(parent, bg=PANEL)
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    tree = ttk.Treeview(frame, columns=columns,
                        show="headings", style="T.Treeview")
    for col, head, w in zip(columns, headings, widths):
        tree.heading(col, text=head)
        tree.column(col, width=w, minwidth=40, anchor="w")

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    tree.tag_configure("odd",  background=ROW_ODD)
    tree.tag_configure("even", background=ROW_EVEN)
    return tree, frame


# ─────────────────────────────────────────────
#  BASE PAGE
# ─────────────────────────────────────────────

class Page(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self.db  = app.db
        self.build()

    def build(self):
        pass

    def on_show(self):
        pass

    def page_header(self, title, subtitle=""):
        hdr = tk.Frame(self, bg=PANEL, pady=10)
        hdr.pack(fill="x", padx=0, pady=(0, 14))
        tk.Frame(hdr, bg=ACCENT, width=5).pack(side="left", fill="y", padx=(16,0))
        tk.Label(hdr, text=title, font=FH,
                 bg=PANEL, fg=ACCENT).pack(side="left", padx=12)
        if subtitle:
            tk.Label(hdr, text=subtitle, font=("Courier New", 9),
                     bg=PANEL, fg=DIM).pack(side="left", padx=4)

    def stat_badge(self, parent, label_text, value_var, color=TEAL):
        f = tk.Frame(parent, bg=PANEL, padx=14, pady=8)
        tk.Label(f, text=label_text, font=FS, bg=PANEL, fg=DIM).pack(anchor="w")
        tk.Label(f, textvariable=value_var, font=("Courier New", 18, "bold"),
                 bg=PANEL, fg=color).pack(anchor="w")
        return f


# ─────────────────────────────────────────────
#  LOGIN PAGE
# ─────────────────────────────────────────────

class LoginPage(Page):
    CREDENTIALS = {"admin": "admin123", "teacher": "teach456"}

    def build(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        box = card(self, padx=40, pady=40)
        box.place(relx=0.5, rely=0.5, anchor="center", width=360)

        tk.Label(box, text="STUDENT ERP", font=("Georgia", 22, "bold"),
                 bg=PANEL, fg=ACCENT).pack(pady=(0, 4))
        tk.Label(box, text="Management System", font=("Courier New", 10),
                 bg=PANEL, fg=DIM).pack(pady=(0, 24))

        sep(box).pack(fill="x", pady=(0, 20))

        for txt, attr, show in [("Username", "_u", ""), ("Password", "_p", "*")]:
            tk.Label(box, text=txt, font=FB, bg=PANEL, fg=DIM).pack(anchor="w")
            var = tk.StringVar()
            setattr(self, attr + "_var", var)
            e = entry(box, var, show=show)
            e.pack(fill="x", ipady=5, pady=(2, 10))

        self._msg = tk.StringVar()
        tk.Label(box, textvariable=self._msg, font=FS,
                 bg=PANEL, fg=RED).pack()

        btn(box, "LOGIN", self._login, pady=10).pack(fill="x", pady=(12, 0))
        tk.Label(box, text="Default: admin / admin123",
                 font=FS, bg=PANEL, fg=DIM).pack(pady=(8, 0))

        self._u_var.set("admin")
        self._p_var.set("admin123")

    def _login(self):
        u = self._u_var.get().strip()
        p = self._p_var.get().strip()
        if self.CREDENTIALS.get(u) == p:
            FileHandler.append_log(f"Login: {u}")
            self.app.show_page("dashboard")
        else:
            self._msg.set("Invalid credentials. Try again.")


# ─────────────────────────────────────────────
#  DASHBOARD PAGE
# ─────────────────────────────────────────────

class DashboardPage(Page):
    def build(self):
        self.page_header("DASHBOARD", "Overview of the institution")

        self._sv = tk.StringVar(value="0")
        self._mv = tk.StringVar(value="0")
        self._av = tk.StringVar(value="0")
        self._fv = tk.StringVar(value="₹0")

        # Stat badges
        badges = tk.Frame(self, bg=BG)
        badges.pack(fill="x", padx=20, pady=(0, 16))
        for i, (lbl, var, col) in enumerate([
            ("Total Students",  self._sv, TEAL),
            ("Marks Entered",   self._mv, GREEN),
            ("Attendance Rows", self._av, ACCENT),
            ("Fees Pending",    self._fv, RED),
        ]):
            b = self.stat_badge(badges, lbl, var, col)
            b.grid(row=0, column=i, sticky="ew", padx=(0, 12))
            badges.columnconfigure(i, weight=1)

        # Quick nav buttons
        nav = tk.Frame(self, bg=BG)
        nav.pack(fill="x", padx=20, pady=(0, 20))
        pages = [
            ("👤  Students",   "students", "#2d6a4f"),
            ("📊  Marks",      "marks",    "#1d4e89"),
            ("📅  Attendance", "attendance","#4a3d6e"),
            ("💰  Fees",       "fees",     "#6e3d3d"),
        ]
        for i, (txt, pg, c) in enumerate(pages):
            btn(nav, txt, lambda p=pg: self.app.show_page(p),
                color=c, fg=TEXT, pady=16).grid(
                row=0, column=i, sticky="ew", padx=(0, 10))
            nav.columnconfigure(i, weight=1)

        # Recent log
        tk.Label(self, text="Recent Activity",
                 font=FB, bg=BG, fg=DIM).pack(anchor="w", padx=20)
        self._log_box = tk.Text(self, height=10, bg=PANEL, fg=TEXT,
                                font=FS, relief="flat",
                                highlightthickness=1,
                                highlightbackground=BORDER,
                                state="disabled")
        self._log_box.pack(fill="both", padx=20, pady=(4, 16), expand=True)

    def on_show(self):
        with self.db._conn() as conn:
            s = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
            m = conn.execute("SELECT COUNT(*) FROM marks").fetchone()[0]
            a = conn.execute("SELECT COUNT(*) FROM attendance").fetchone()[0]
            f = conn.execute(
                "SELECT COALESCE(SUM(amount_due-amount_paid),0) FROM fees WHERE status!='Paid'"
            ).fetchone()[0]
        self._sv.set(str(s))
        self._mv.set(str(m))
        self._av.set(str(a))
        self._fv.set(f"₹{f:,.0f}")
        self._load_log()

    def _load_log(self):
        self._log_box.configure(state="normal")
        self._log_box.delete("1.0", "end")
        try:
            with open("activity.log", "r", encoding="utf-8") as f:
                lines = f.readlines()[-20:]
            for line in reversed(lines):
                self._log_box.insert("end", line)
        except FileNotFoundError:
            self._log_box.insert("end", "No activity yet.\n")
        self._log_box.configure(state="disabled")


# ─────────────────────────────────────────────
#  STUDENTS PAGE
# ─────────────────────────────────────────────

class StudentsPage(Page):
    def build(self):
        self.page_header("STUDENTS", "Add · Edit · Delete · Search · Import/Export")
        self._sel_id = None
        self._vars   = {}

        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True, padx=20, pady=(0, 16))
        outer.columnconfigure(1, weight=1)
        outer.rowconfigure(0, weight=1)

        self._build_form(outer)
        self._build_table(outer)

    def _build_form(self, parent):
        frm = card(parent, pady=12)
        frm.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        frm.configure(width=240)
        frm.grid_propagate(False)

        label(frm, "STUDENT FORM", font=FB, fg=ACCENT).pack(pady=(8,2), padx=12, anchor="w")
        sep(frm).pack(fill="x", padx=12, pady=(0,10))

        fields = [
            ("Student ID",  "sid",  None),
            ("Full Name",   "name", None),
            ("Department",  "dept", DEPTS),
            ("Year",        "year", ["1","2","3","4"]),
            ("Email",       "email",None),
            ("Phone",       "phone",None),
            ("GPA (0–10)",  "gpa",  None),
        ]
        for lbl, key, choices in fields:
            label(frm, lbl, font=FB, fg=DIM).pack(anchor="w", padx=12, pady=(5,1))
            var = tk.StringVar()
            if choices:
                w = combo(frm, var, choices)
            else:
                w = entry(frm, var)
            w.pack(fill="x", padx=12, ipady=4)
            self._vars[key] = var

        sep(frm).pack(fill="x", padx=12, pady=12)
        for txt, col, cmd in [
            ("＋ ADD",    "#2d6a4f", self._add),
            ("✎ UPDATE",  "#1d4e89", self._update),
            ("✕ DELETE",  "#7b2d2d", self._delete),
            ("↺ CLEAR",   "#3a3d4d", self._clear),
        ]:
            btn(frm, txt, cmd, color=col, fg=TEXT, pady=7).pack(
                fill="x", padx=12, pady=2)

        sep(frm).pack(fill="x", padx=12, pady=8)
        btn(frm, "⬆ EXPORT CSV",  self._export, color="#3d3568", fg=TEXT, pady=6).pack(fill="x", padx=12, pady=2)
        btn(frm, "⬇ IMPORT CSV",  self._import, color="#2d4a6a", fg=TEXT, pady=6).pack(fill="x", padx=12, pady=2)
        btn(frm, "💾 SAVE JSON",   self._save_json, color="#2d4a3a", fg=TEXT, pady=6).pack(fill="x", padx=12, pady=2)
        btn(frm, "📂 LOAD JSON",   self._load_json, color="#2a3a4a", fg=TEXT, pady=6).pack(fill="x", padx=12, pady=2)
        btn(frm, "📝 SAVE TXT",    self._save_txt,  color="#3a3020", fg=TEXT, pady=6).pack(fill="x", padx=12, pady=2)
        btn(frm, "📖 LOAD TXT",    self._load_txt,  color="#2a2830", fg=TEXT, pady=6).pack(fill="x", padx=12, pady=2)

    def _build_table(self, parent):
        panel = card(parent)
        panel.grid(row=0, column=1, sticky="nsew")
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(1, weight=1)

        # Search
        srow = tk.Frame(panel, bg=PANEL, pady=8)
        srow.grid(row=0, column=0, sticky="ew", padx=10)
        label(srow, "🔍", bg=PANEL, fg=TEAL).pack(side="left")
        self._sv = tk.StringVar()
        self._sv.trace_add("write", lambda *_: self._refresh())
        entry(srow, self._sv).pack(side="left", fill="x", expand=True, ipady=4, padx=6)
        label(srow, "Search by ID / Name / Dept", font=FS, fg=DIM, bg=PANEL).pack(side="left")

        # Tree
        cols = ("sid","name","dept","year","email","phone","gpa")
        heads = ("Student ID","Name","Department","Year","Email","Phone","GPA")
        widths = (90,160,150,50,160,110,60)
        self._tree, tf = make_tree(panel, cols, heads, widths)
        tf.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,8))

        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        self._status = tk.StringVar(value="")
        label(panel, "", font=FS, fg=DIM, bg=PANEL,
              textvariable=self._status).grid(row=2, column=0, sticky="w", padx=10)

    # ── CRUD ─────────────────────────────────

    def _get_data(self):
        return Student(
            student_id = self._vars["sid"].get().strip(),
            name       = self._vars["name"].get().strip(),
            department = self._vars["dept"].get(),
            year       = self._vars["year"].get() or 0,
            email      = self._vars["email"].get().strip(),
            phone      = self._vars["phone"].get().strip(),
            gpa        = self._vars["gpa"].get().strip() or 0,
            db_id      = self._sel_id,
        )

    def _add(self):
        try:
            s = self._get_data()
            Student.validate(s.student_id, s.name, s.department, s.year, s.gpa)
            self.db.add_student(s)
            FileHandler.append_log(f"ADD student {s.student_id} — {s.name}")
            self._clear(); self._refresh()
            self._status.set(f"✔  Added: {s.name}")
        except (ValidationError, DuplicateStudentError) as e:
            messagebox.showerror("Error", str(e))

    def _update(self):
        if not self._sel_id:
            messagebox.showwarning("No selection", "Select a student to update.")
            return
        try:
            s = self._get_data()
            Student.validate(s.student_id, s.name, s.department, s.year, s.gpa)
            self.db.update_student(s)
            FileHandler.append_log(f"UPDATE student {s.student_id}")
            self._refresh()
            self._status.set(f"✔  Updated: {s.name}")
        except ValidationError as e:
            messagebox.showerror("Validation Error", str(e))

    def _delete(self):
        if not self._sel_id:
            messagebox.showwarning("No selection", "Select a student to delete.")
            return
        name = self._vars["name"].get()
        if messagebox.askyesno("Confirm", f"Delete '{name}'? This cannot be undone."):
            self.db.delete_student(self._sel_id)
            FileHandler.append_log(f"DELETE student id={self._sel_id} ({name})")
            self._clear(); self._refresh()
            self._status.set(f"✔  Deleted: {name}")

    def _on_select(self, _=None):
        sel = self._tree.selection()
        if not sel: return
        self._sel_id = int(sel[0])
        vals = self._tree.item(sel[0], "values")
        for key, val in zip(["sid","name","dept","year","email","phone","gpa"], vals):
            self._vars[key].set(val)

    def _clear(self):
        for v in self._vars.values(): v.set("")
        self._sel_id = None

    def _refresh(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
        rows = self.db.get_all_students(self._sv.get())
        for i, s in enumerate(rows):
            tag = "odd" if i % 2 else "even"
            self._tree.insert("", "end", iid=str(s.db_id),
                values=(s.student_id, s.name, s.department,
                        s.year, s.email, s.phone, s.gpa), tags=(tag,))
        self._status.set(f"{len(rows)} records")

    def on_show(self):
        self._refresh()

    # ── File ops ─────────────────────────────

    def _export(self):
        p = filedialog.asksaveasfilename(defaultextension=".csv",
                filetypes=[("CSV","*.csv")])
        if not p: return
        try:
            n = self.db.export_csv(p, self._sv.get())
            FileHandler.append_log(f"EXPORT CSV {n} records → {p}")
            messagebox.showinfo("Exported", f"{n} records saved to {p}")
        except FileHandlingError as e:
            messagebox.showerror("Export Error", str(e))

    def _import(self):
        p = filedialog.askopenfilename(filetypes=[("CSV","*.csv")])
        if not p: return
        try:
            ins, skip, err = self.db.import_csv(p)
            FileHandler.append_log(f"IMPORT CSV inserted={ins} skipped={skip}")
            messagebox.showinfo("Imported",
                f"Inserted: {ins}\nSkipped duplicates: {skip}\nErrors: {err}")
            self._refresh()
        except FileHandlingError as e:
            messagebox.showerror("Import Error", str(e))

    def _save_json(self):
        p = filedialog.asksaveasfilename(defaultextension=".json",
                filetypes=[("JSON","*.json")])
        if not p: return
        try:
            students = self.db.get_all_students()
            FileHandler.save_json(students, p)
            FileHandler.append_log(f"SAVE JSON {len(students)} records → {p}")
            messagebox.showinfo("Saved", f"{len(students)} records saved as JSON.")
        except FileHandlingError as e:
            messagebox.showerror("Save Error", str(e))

    def _load_json(self):
        p = filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if not p: return
        try:
            students = FileHandler.load_json(p)
            ins = skip = 0
            for s in students:
                try:
                    self.db.add_student(s); ins += 1
                except DuplicateStudentError:
                    skip += 1
            FileHandler.append_log(f"LOAD JSON inserted={ins} skipped={skip}")
            messagebox.showinfo("Loaded", f"Inserted: {ins}, Skipped: {skip}")
            self._refresh()
        except FileHandlingError as e:
            messagebox.showerror("Load Error", str(e))

    def _save_txt(self):
        p = filedialog.asksaveasfilename(defaultextension=".txt",
                filetypes=[("Text","*.txt")])
        if not p: return
        try:
            students = self.db.get_all_students()
            FileHandler.save_txt(students, p)
            FileHandler.append_log(f"SAVE TXT {len(students)} records → {p}")
            messagebox.showinfo("Saved", f"{len(students)} records saved as TXT.")
        except FileHandlingError as e:
            messagebox.showerror("Save Error", str(e))

    def _load_txt(self):
        p = filedialog.askopenfilename(filetypes=[("Text","*.txt")])
        if not p: return
        try:
            students = FileHandler.load_txt(p)
            ins = skip = 0
            for s in students:
                try:
                    self.db.add_student(s); ins += 1
                except DuplicateStudentError:
                    skip += 1
            FileHandler.append_log(f"LOAD TXT inserted={ins} skipped={skip}")
            messagebox.showinfo("Loaded", f"Inserted: {ins}, Skipped: {skip}")
            self._refresh()
        except FileHandlingError as e:
            messagebox.showerror("Load Error", str(e))


# ─────────────────────────────────────────────
#  MARKS PAGE
# ─────────────────────────────────────────────

class MarksPage(Page):
    def build(self):
        self.page_header("MARKS", "Enter and review subject-wise marks")
        self._sel_mark_id = None

        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True, padx=20, pady=(0,16))
        outer.columnconfigure(1, weight=1)
        outer.rowconfigure(0, weight=1)

        # Form
        frm = card(outer, pady=12, width=240)
        frm.grid(row=0, column=0, sticky="nsew", padx=(0,14))
        frm.grid_propagate(False)

        label(frm, "MARKS ENTRY", font=FB, fg=ACCENT).pack(pady=(8,2), padx=12, anchor="w")
        sep(frm).pack(fill="x", padx=12, pady=(0,10))

        self._mv = {}
        for lbl, key, choices in [
            ("Student ID",    "sid",       None),
            ("Subject",       "subject",   None),
            ("Marks Obtained","marks",     None),
            ("Max Marks",     "max_marks", None),
            ("Exam Type",     "exam_type", ["Internal","External","Lab","Assignment"]),
        ]:
            label(frm, lbl, font=FB, fg=DIM).pack(anchor="w", padx=12, pady=(5,1))
            var = tk.StringVar()
            w = combo(frm, var, choices) if choices else entry(frm, var)
            w.pack(fill="x", padx=12, ipady=4)
            self._mv[key] = var

        self._mv["max_marks"].set("100")
        self._mv["exam_type"].set("Internal")

        sep(frm).pack(fill="x", padx=12, pady=10)
        btn(frm, "＋ ADD MARKS",   self._add,    "#2d6a4f", TEXT, pady=7).pack(fill="x", padx=12, pady=2)
        btn(frm, "✕ DELETE",       self._delete, "#7b2d2d", TEXT, pady=7).pack(fill="x", padx=12, pady=2)
        btn(frm, "↺ CLEAR",        self._clear,  "#3a3d4d", TEXT, pady=7).pack(fill="x", padx=12, pady=2)

        self._summary = tk.StringVar(value="")
        label(frm, "", font=FS, fg=TEAL, bg=PANEL,
              textvariable=self._summary, wraplength=210).pack(padx=12, pady=8, anchor="w")

        # Table
        panel = card(outer)
        panel.grid(row=0, column=1, sticky="nsew")
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(1, weight=1)

        srow = tk.Frame(panel, bg=PANEL, pady=8)
        srow.grid(row=0, column=0, sticky="ew", padx=10)
        label(srow, "Student ID:", font=FB, bg=PANEL, fg=DIM).pack(side="left")
        self._filter_v = tk.StringVar()
        entry(srow, self._filter_v).pack(side="left", fill="x", expand=True, ipady=4, padx=6)
        btn(srow, "LOAD", self._load_marks, pady=4).pack(side="left", padx=4)

        cols = ("subject","marks_obtained","max_marks","percentage","grade","exam_type")
        heads = ("Subject","Obtained","Max","Percentage","Grade","Exam Type")
        widths = (160,80,80,90,60,100)
        self._tree, tf = make_tree(panel, cols, heads, widths)
        tf.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,8))
        self._tree.bind("<<TreeviewSelect>>", self._on_select)

    def _add(self):
        try:
            sid = self._mv["sid"].get().strip()
            sub = self._mv["subject"].get().strip()
            mo  = self._mv["marks"].get().strip()
            mx  = self._mv["max_marks"].get().strip() or "100"
            et  = self._mv["exam_type"].get()
            if not sid or not sub:
                raise ValidationError("Student ID and Subject are required.")
            Marks.validate(mo, mx)
            m = Marks(sid, sub, float(mo), float(mx), et)
            self.db.add_marks(m)
            FileHandler.append_log(f"ADD marks {sid} {sub} {mo}/{mx}")
            self._load_marks()
        except (ValidationError, Exception) as e:
            messagebox.showerror("Error", str(e))

    def _delete(self):
        if not self._sel_mark_id:
            messagebox.showwarning("No selection", "Select a marks row to delete.")
            return
        self.db.delete_marks(self._sel_mark_id)
        self._sel_mark_id = None
        self._load_marks()

    def _on_select(self, _=None):
        sel = self._tree.selection()
        if sel:
            self._sel_mark_id = int(sel[0])

    def _clear(self):
        for v in self._mv.values(): v.set("")
        self._mv["max_marks"].set("100")
        self._mv["exam_type"].set("Internal")
        self._sel_mark_id = None
        self._summary.set("")

    def _load_marks(self):
        sid = self._filter_v.get().strip() or self._mv["sid"].get().strip()
        if not sid:
            messagebox.showinfo("Tip", "Enter a Student ID and click LOAD.")
            return
        for item in self._tree.get_children():
            self._tree.delete(item)
        marks = self.db.get_marks(sid)
        for i, m in enumerate(marks):
            tag = "odd" if i % 2 else "even"
            self._tree.insert("", "end", iid=str(m.db_id),
                values=(m.subject, m.marks_obtained, m.max_marks,
                        f"{m.percentage}%", m.grade, m.exam_type), tags=(tag,))
        sm = self.db.get_marks_summary(sid)
        if sm["total"]:
            self._summary.set(
                f"Total: {sm['obtained']}/{sm['total']}\n"
                f"Percentage: {sm['percentage']}%"
            )


# ─────────────────────────────────────────────
#  ATTENDANCE PAGE
# ─────────────────────────────────────────────

class AttendancePage(Page):
    def build(self):
        self.page_header("ATTENDANCE", "Track daily subject-wise attendance")
        self._sel_att_id = None

        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True, padx=20, pady=(0,16))
        outer.columnconfigure(1, weight=1)
        outer.rowconfigure(0, weight=1)

        # Form
        frm = card(outer, pady=12, width=240)
        frm.grid(row=0, column=0, sticky="nsew", padx=(0,14))
        frm.grid_propagate(False)

        label(frm, "ATTENDANCE ENTRY", font=FB, fg=ACCENT).pack(pady=(8,2), padx=12, anchor="w")
        sep(frm).pack(fill="x", padx=12, pady=(0,10))

        self._av = {}
        from datetime import date
        for lbl, key, choices in [
            ("Student ID", "sid",     None),
            ("Date",       "date",    None),
            ("Subject",    "subject", None),
            ("Status",     "status",  Attendance.VALID_STATUSES),
        ]:
            label(frm, lbl, font=FB, fg=DIM).pack(anchor="w", padx=12, pady=(5,1))
            var = tk.StringVar()
            w = combo(frm, var, choices) if choices else entry(frm, var)
            w.pack(fill="x", padx=12, ipady=4)
            self._av[key] = var

        self._av["date"].set(str(date.today()))
        self._av["status"].set("Present")

        sep(frm).pack(fill="x", padx=12, pady=10)
        btn(frm, "＋ MARK ATTENDANCE", self._add,    "#2d6a4f", TEXT, pady=7).pack(fill="x", padx=12, pady=2)
        btn(frm, "✕ DELETE",           self._delete, "#7b2d2d", TEXT, pady=7).pack(fill="x", padx=12, pady=2)

        self._summary = tk.StringVar()
        label(frm, "", font=FS, fg=TEAL, bg=PANEL,
              textvariable=self._summary, wraplength=210).pack(padx=12, pady=8, anchor="w")

        # Table
        panel = card(outer)
        panel.grid(row=0, column=1, sticky="nsew")
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(1, weight=1)

        srow = tk.Frame(panel, bg=PANEL, pady=8)
        srow.grid(row=0, column=0, sticky="ew", padx=10)
        label(srow, "Student ID:", font=FB, bg=PANEL, fg=DIM).pack(side="left")
        self._filter_v = tk.StringVar()
        entry(srow, self._filter_v).pack(side="left", fill="x", expand=True, ipady=4, padx=6)
        btn(srow, "LOAD", self._load_att, pady=4).pack(side="left", padx=4)

        cols = ("date","subject","status")
        heads = ("Date","Subject","Status")
        widths = (110,200,100)
        self._tree, tf = make_tree(panel, cols, heads, widths)
        tf.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,8))
        self._tree.bind("<<TreeviewSelect>>", lambda _: self._on_select())

    def _add(self):
        try:
            sid  = self._av["sid"].get().strip()
            dt   = self._av["date"].get().strip()
            subj = self._av["subject"].get().strip()
            stat = self._av["status"].get()
            if not sid or not dt or not subj:
                raise ValidationError("Student ID, Date and Subject are required.")
            Attendance.validate(stat)
            a = Attendance(sid, dt, subj, stat)
            self.db.add_attendance(a)
            FileHandler.append_log(f"ATTENDANCE {sid} {dt} {subj} {stat}")
            self._load_att()
        except ValidationError as e:
            messagebox.showerror("Error", str(e))

    def _delete(self):
        if not self._sel_att_id:
            messagebox.showwarning("No selection", "Select a row to delete.")
            return
        self.db.delete_attendance(self._sel_att_id)
        self._sel_att_id = None
        self._load_att()

    def _on_select(self):
        sel = self._tree.selection()
        if sel:
            self._sel_att_id = int(sel[0])

    def _load_att(self):
        sid = self._filter_v.get().strip()
        if not sid:
            messagebox.showinfo("Tip", "Enter a Student ID and click LOAD.")
            return
        for item in self._tree.get_children():
            self._tree.delete(item)
        records = self.db.get_attendance(sid)
        for i, a in enumerate(records):
            color_tag = "odd" if i % 2 else "even"
            self._tree.insert("", "end", iid=str(a.db_id),
                values=(a.date_str, a.subject, a.status), tags=(color_tag,))
        sm = self.db.get_attendance_summary(sid)
        if sm["total"]:
            self._summary.set(
                f"Total: {sm['total']}  Present: {sm['present']}\n"
                f"Absent: {sm['absent']}  Late: {sm['late']}\n"
                f"Attendance: {sm['percentage']}%"
            )


# ─────────────────────────────────────────────
#  FEES PAGE
# ─────────────────────────────────────────────

class FeesPage(Page):
    def build(self):
        self.page_header("FEES", "Track semester fee payments and balances")
        self._sel_fee_id = None

        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True, padx=20, pady=(0,16))
        outer.columnconfigure(1, weight=1)
        outer.rowconfigure(0, weight=1)

        # Form
        frm = card(outer, pady=12, width=240)
        frm.grid(row=0, column=0, sticky="nsew", padx=(0,14))
        frm.grid_propagate(False)

        label(frm, "FEE ENTRY", font=FB, fg=ACCENT).pack(pady=(8,2), padx=12, anchor="w")
        sep(frm).pack(fill="x", padx=12, pady=(0,10))

        self._fv = {}
        for lbl, key, choices in [
            ("Student ID",   "sid",         None),
            ("Semester",     "semester",    [str(i) for i in range(1,9)]),
            ("Amount Due",   "amount_due",  None),
            ("Amount Paid",  "amount_paid", None),
            ("Status",       "status",      Fee.VALID_STATUSES),
            ("Due Date",     "due_date",    None),
        ]:
            label(frm, lbl, font=FB, fg=DIM).pack(anchor="w", padx=12, pady=(5,1))
            var = tk.StringVar()
            w = combo(frm, var, choices) if choices else entry(frm, var)
            w.pack(fill="x", padx=12, ipady=4)
            self._fv[key] = var

        self._fv["status"].set("Pending")
        self._fv["amount_paid"].set("0")

        sep(frm).pack(fill="x", padx=12, pady=10)
        btn(frm, "＋ ADD FEE",       self._add,    "#2d6a4f", TEXT, pady=7).pack(fill="x", padx=12, pady=2)
        btn(frm, "💳 UPDATE PAYMENT", self._pay,   "#1d4e89", TEXT, pady=7).pack(fill="x", padx=12, pady=2)

        self._summary = tk.StringVar()
        label(frm, "", font=FS, fg=TEAL, bg=PANEL,
              textvariable=self._summary, wraplength=210).pack(padx=12, pady=8, anchor="w")

        # Table
        panel = card(outer)
        panel.grid(row=0, column=1, sticky="nsew")
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(1, weight=1)

        srow = tk.Frame(panel, bg=PANEL, pady=8)
        srow.grid(row=0, column=0, sticky="ew", padx=10)
        label(srow, "Student ID:", font=FB, bg=PANEL, fg=DIM).pack(side="left")
        self._filter_v = tk.StringVar()
        entry(srow, self._filter_v).pack(side="left", fill="x", expand=True, ipady=4, padx=6)
        btn(srow, "LOAD", self._load_fees, pady=4).pack(side="left", padx=4)

        cols = ("semester","amount_due","amount_paid","balance","status","due_date")
        heads = ("Semester","Amount Due","Amount Paid","Balance","Status","Due Date")
        widths = (70,100,100,90,90,110)
        self._tree, tf = make_tree(panel, cols, heads, widths)
        tf.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,8))
        self._tree.bind("<<TreeviewSelect>>", lambda _: self._on_select())

    def _add(self):
        try:
            sid = self._fv["sid"].get().strip()
            sem = self._fv["semester"].get()
            ad  = self._fv["amount_due"].get().strip()
            ap  = self._fv["amount_paid"].get().strip() or "0"
            st  = self._fv["status"].get()
            dd  = self._fv["due_date"].get().strip()
            if not sid or not sem or not ad:
                raise ValidationError("Student ID, Semester, and Amount Due are required.")
            Fee.validate(ad, ap)
            f = Fee(sid, int(sem), float(ad), float(ap), st, dd)
            self.db.add_fee(f)
            FileHandler.append_log(f"ADD fee {sid} sem={sem} due={ad}")
            self._load_fees()
        except ValidationError as e:
            messagebox.showerror("Error", str(e))

    def _pay(self):
        if not self._sel_fee_id:
            messagebox.showwarning("No selection", "Select a fee row first.")
            return
        ap  = self._fv["amount_paid"].get().strip()
        st  = self._fv["status"].get()
        try:
            Fee.validate(self._fv["amount_due"].get() or 0, ap)
            self.db.update_fee_payment(self._sel_fee_id, float(ap), st)
            FileHandler.append_log(f"UPDATE fee id={self._sel_fee_id} paid={ap}")
            self._load_fees()
        except ValidationError as e:
            messagebox.showerror("Error", str(e))

    def _on_select(self):
        sel = self._tree.selection()
        if not sel: return
        self._sel_fee_id = int(sel[0])
        vals = self._tree.item(sel[0], "values")
        self._fv["semester"].set(vals[0])
        self._fv["amount_due"].set(vals[1])
        self._fv["amount_paid"].set(vals[2])
        self._fv["status"].set(vals[4])
        self._fv["due_date"].set(vals[5])

    def _load_fees(self):
        sid = self._filter_v.get().strip()
        if not sid:
            messagebox.showinfo("Tip", "Enter a Student ID and click LOAD.")
            return
        for item in self._tree.get_children():
            self._tree.delete(item)
        fees = self.db.get_fees(sid)
        for i, f in enumerate(fees):
            tag = "odd" if i % 2 else "even"
            self._tree.insert("", "end", iid=str(f.db_id),
                values=(f.semester, f"₹{f.amount_due:,.0f}",
                        f"₹{f.amount_paid:,.0f}", f"₹{f.balance:,.0f}",
                        f.status, f.due_date), tags=(tag,))
        sm = self.db.get_fee_summary(sid)
        if sm["total_due"]:
            self._summary.set(
                f"Total Due:  ₹{sm['total_due']:,.0f}\n"
                f"Total Paid: ₹{sm['total_paid']:,.0f}\n"
                f"Balance:    ₹{sm['balance']:,.0f}"
            )


# ─────────────────────────────────────────────
#  MAIN APPLICATION — MULTI-SCREEN
# ─────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Data Management System")
        self.geometry("1200x760")
        self.minsize(1000, 660)
        self.configure(bg=BG)

        self.db = Database()
        self._pages = {}
        self._build_shell()
        self._init_pages()
        self.show_page("login")

    def _build_shell(self):
        # Top nav bar (shown after login)
        self._nav = tk.Frame(self, bg=SIDEBAR, pady=0)
        self._nav.pack(fill="x", side="top")
        self._nav.pack_forget()

        tk.Frame(self._nav, bg=ACCENT, width=5).pack(side="left", fill="y")
        tk.Label(self._nav, text="STUDENT ERP",
                 font=("Georgia", 13, "bold"), bg=SIDEBAR,
                 fg=ACCENT, padx=14, pady=8).pack(side="left")

        self._nav_btns = {}
        for name, label_text in [
            ("dashboard",  "Dashboard"),
            ("students",   "Students"),
            ("marks",      "Marks"),
            ("attendance", "Attendance"),
            ("fees",       "Fees"),
        ]:
            b = tk.Button(self._nav, text=label_text, font=FB,
                          bg=SIDEBAR, fg=DIM,
                          activebackground=PANEL, activeforeground=ACCENT,
                          relief="flat", cursor="hand2", padx=16, pady=8,
                          command=lambda n=name: self.show_page(n))
            b.pack(side="left")
            self._nav_btns[name] = b

        tk.Button(self._nav, text="Logout", font=FB,
                  bg=SIDEBAR, fg=DIM,
                  relief="flat", cursor="hand2", padx=16, pady=8,
                  command=self._logout).pack(side="right")

        self._content = tk.Frame(self, bg=BG)
        self._content.pack(fill="both", expand=True)

    def _init_pages(self):
        classes = {
            "login":      LoginPage,
            "dashboard":  DashboardPage,
            "students":   StudentsPage,
            "marks":      MarksPage,
            "attendance": AttendancePage,
            "fees":       FeesPage,
        }
        for name, cls in classes.items():
            page = cls(self._content, self)
            page.place(relx=0, rely=0, relwidth=1, relheight=1)
            self._pages[name] = page

    def show_page(self, name):
        for page in self._pages.values():
            page.place_forget()
        page = self._pages[name]
        page.place(relx=0, rely=0, relwidth=1, relheight=1)
        page.on_show()

        if name == "login":
            self._nav.pack_forget()
        else:
            self._nav.pack(fill="x", side="top", before=self._content)
            for n, b in self._nav_btns.items():
                b.configure(bg=PANEL if n == name else SIDEBAR,
                            fg=ACCENT if n == name else DIM)

    def _logout(self):
        FileHandler.append_log("Logout")
        self.show_page("login")


# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()