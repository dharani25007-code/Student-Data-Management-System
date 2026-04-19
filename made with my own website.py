import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from pathlib import Path

# ----------------------------------------------------------------------
#                         MODEL (Database layer)
# ----------------------------------------------------------------------
class StudentModel:
    """SQLite operations for student records."""

    def __init__(self, db_path="students.db"):
        self.db_path = db_path
        self._initialize_database()

    # --------------------------------------------------------------
    def _initialize_database(self):
        """Create table if missing and migrate old schema if required."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # Create the target schema
        cur.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                age INTEGER,
                grade TEXT,
                email TEXT,
                phone TEXT,
                address TEXT,
                admission_date TEXT
            )
        ''')

        # Detect missing column (old DB without student_id)
        cur.execute("PRAGMA table_info(students)")
        cols = {info[1] for info in cur.fetchall()}
        if "student_id" not in cols:
            self._migrate_schema(cur)

        conn.commit()
        conn.close()

    # --------------------------------------------------------------
    def _migrate_schema(self, cur):
        """Re‑create table preserving existing rows (adds student_id column)."""
        cur.execute("CREATE TEMPORARY TABLE tmp_students AS SELECT * FROM students")
        cur.execute("DROP TABLE students")
        cur.execute('''
            CREATE TABLE students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                age INTEGER,
                grade TEXT,
                email TEXT,
                phone TEXT,
                address TEXT,
                admission_date TEXT
            )
        ''')
        # Old table may not have student_id → insert NULL for it
        try:
            cur.execute('''
                INSERT INTO students (
                    student_id, name, age, grade, email, phone, address, admission_date
                )
                SELECT student_id, name, age, grade, email, phone, address, admission_date
                FROM tmp_students
            ''')
        except sqlite3.OperationalError:
            cur.execute('''
                INSERT INTO students (
                    student_id, name, age, grade, email, phone, address, admission_date
                )
                SELECT NULL, name, age, grade, email, phone, address, admission_date
                FROM tmp_students
            ''')
        cur.execute("DROP TABLE tmp_students")

    # --------------------------------------------------------------
    def add_student(self, data: dict) -> bool:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        try:
            cur.execute('''
                INSERT INTO students (
                    student_id, name, age, grade, email,
                    phone, address, admission_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data["student_id"], data["name"], data["age"], data["grade"],
                data["email"], data["phone"], data["address"], data["admission_date"]
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Student ID already exists!")
            return False
        finally:
            conn.close()

    def get_all(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM students ORDER BY name")
        rows = cur.fetchall()
        conn.close()
        return rows

    def update_student(self, student_id: str, data: dict):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute('''
            UPDATE students SET
                name = ?, age = ?, grade = ?, email = ?, phone = ?, 
                address = ?, admission_date = ?
            WHERE student_id = ?
        ''', (
            data["name"], data["age"], data["grade"], data["email"],
            data["phone"], data["address"], data["admission_date"], student_id
        ))
        conn.commit()
        conn.close()

    def delete_student(self, student_id: str):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        conn.commit()
        conn.close()

    def search(self, term: str):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        like = f"%{term}%"
        cur.execute('''
            SELECT * FROM students
            WHERE student_id LIKE ? OR name LIKE ?
        ''', (like, like))
        rows = cur.fetchall()
        conn.close()
        return rows

    # ------------------------------------------------------------------
    # CSV import / export – handy for an ERP‑like system
    # ------------------------------------------------------------------
    def export_csv(self, file_path):
        rows = self.get_all()
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["id", "student_id", "name", "age", "grade",
                 "email", "phone", "address", "admission_date"]
            )
            writer.writerows(rows)

    def import_csv(self, file_path):
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert age to int, ignore empty strings
                row["age"] = int(row["age"]) if row["age"].isdigit() else 0
                # Try to insert – ignore duplicates silently
                try:
                    self.add_student(row)
                except Exception:
                    pass


# ----------------------------------------------------------------------
#                         VIEW (Tkinter GUI)
# ----------------------------------------------------------------------
class StudentView:
    def __init__(self, master):
        self.master = master
        master.title("Student Record Management System")
        master.geometry("1150x720")
        master.minsize(900, 600)

        # ---------------------------------------------------------- Style
        self.style = ttk.Style()
        self.style.theme_use("clam")                      # modern look
        self.style.configure("TLabel", font=("Segoe UI", 10))
        self.style.configure("TEntry", font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading",
                             font=("Segoe UI", 10, "bold"))
        self.style.map("TButton",
                       foreground=[("active", "#ffffff")],
                       background=[("active", "#0066cc")])

        # Alternate row colors
        self.style.configure("Treeview",
                             background="#f9f9f9",
                             fieldbackground="#f9f9f9")
        self.style.map("Treeview",
                       background=[("selected", "#3399ff")])

        # ---------------------------------------------------------- Model
        self.model = StudentModel()

        # ---------------------------------------------------------- Menu
        self._create_menu()

        # ---------------------------------------------------------- Notebook (tabs)
        notebook = ttk.Notebook(master)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_form = ttk.Frame(notebook)
        self.tab_report = ttk.Frame(notebook)

        notebook.add(self.tab_form, text="Data Entry")
        notebook.add(self.tab_report, text="Student List")

        # ---------------------------------------------------------- Form Tab
        self._build_form_tab(self.tab_form)

        # ---------------------------------------------------------- Report Tab
        self._build_report_tab(self.tab_report)

        # ---------------------------------------------------------- Status bar
        self.status = tk.StringVar()
        self.status_bar = ttk.Label(master, textvariable=self.status,
                                    relief="sunken", anchor="w")
        self.status_bar.pack(fill="x", side="bottom")
        self._set_status("Ready")

    # ------------------------------------------------------------------
    # Helper UI methods
    # ------------------------------------------------------------------
    def _set_status(self, msg):
        self.status.set(msg)
        self.master.after(5000, lambda: self.status.set(""))   # clear after 5 s

    def _create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import CSV…", command=self.import_csv)
        file_menu.add_command(label="Export CSV…", command=self.export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

        help_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    # ------------------------------------------------------------------
    # Form tab
    # ------------------------------------------------------------------
    def _build_form_tab(self, parent):
        # ---- Form fields -------------------------------------------------
        form = ttk.LabelFrame(parent, text="Student Details")
        form.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        labels = [
            ("Student ID*", "student_id"),
            ("Name*", "name"),
            ("Age", "age"),
            ("Grade", "grade"),
            ("Email", "email"),
            ("Phone", "phone"),
            ("Address", "address"),
            ("Admission Date", "admission_date")
        ]

        self.entries = {}
        for r, (lbl, key) in enumerate(labels):
            ttk.Label(form, text=lbl).grid(row=r, column=0, sticky="e", padx=5, pady=4)
            ent = ttk.Entry(form, width=30)
            ent.grid(row=r, column=1, padx=5, pady=4)
            self.entries[key] = ent

        # ---- Buttons ----------------------------------------------------
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=1, column=0, pady=5, sticky="e")

        ttk.Button(btn_frame, text="Add", command=self.add_student,
                   style="Accent.TButton").grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_student).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_student).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form).grid(row=0, column=3, padx=5)

        # Make the form expand nicely
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

    # ------------------------------------------------------------------
    # Report tab (treeview + search)
    # ------------------------------------------------------------------
    def _build_report_tab(self, parent):
        # ---- Search bar -------------------------------------------------
        search_frame = ttk.LabelFrame(parent, text="Search")
        search_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(search_frame, text="Keyword:").grid(row=0, column=0, padx=5, pady=4)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.grid(row=0, column=1, padx=5, pady=4)
        search_entry.bind("<KeyRelease>", lambda e: self.search_students())

        ttk.Button(search_frame, text="Clear", command=self.clear_search).grid(row=0, column=2, padx=5)

        # ---- Treeview ---------------------------------------------------
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("id", "student_id", "name", "age", "grade",
                "email", "phone", "address", "admission_date")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        # Column headings + sortable headers
        headings = [
            ("DB ID", 60), ("Student ID", 100), ("Name", 150), ("Age", 50),
            ("Grade", 60), ("Email", 150), ("Phone", 100), ("Address", 180),
            ("Admission Date", 100)
        ]
        for col, (txt, width) in zip(cols, headings):
            self.tree.heading(col, text=txt,
                              command=lambda _c=col: self._sort_by(_c, False))
            self.tree.column(col, width=width, anchor="center")

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)

        # Right‑click context menu
        self._create_tree_context_menu()

        # Bind selection → populate form on the *Data Entry* tab
        self.tree.bind("<<TreeviewSelect>>", self._populate_form_from_tree)

    # ------------------------------------------------------------------
    # Treeview utilities
    # ------------------------------------------------------------------
    def _sort_by(self, col, descending):
        """Sort tree contents when a column header is clicked."""
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        # Try to convert to numeric for proper sorting
        try:
            data = [(int(v), k) for v, k in data]
        except ValueError:
            pass
        data.sort(reverse=descending)
        for idx, (val, k) in enumerate(data):
            self.tree.move(k, '', idx)
        # Reverse sort next time
        self.tree.heading(col,
                         command=lambda: self._sort_by(col, not descending))

    def _create_tree_context_menu(self):
        self.tree_menu = tk.Menu(self.master, tearoff=False)
        self.tree_menu.add_command(label="Edit", command=self._edit_from_tree)
        self.tree_menu.add_command(label="Delete", command=self._delete_from_tree)
        self.tree.bind("<Button-3>", self._show_tree_menu)

    def _show_tree_menu(self, event):
        if self.tree.identify_region(event.x, event.y) == "cell":
            self.tree_menu.tk_popup(event.x_root, event.y_root)

    def _edit_from_tree(self):
        selected = self.tree.selection()
        if selected:
            self._populate_form_from_tree()
            # Switch to Data Entry tab automatically
            self.master.nametowidget(self.master.winfo_children()[0]).select(self.tab_form)

    def _delete_from_tree(self):
        selected = self.tree.selection()
        if selected:
            sid = self.tree.item(selected[0])["values"][1]
            if messagebox.askyesno("Confirm", "Delete this student?"):
                self.model.delete_student(sid)
                self.refresh_tree()
                self._set_status("Record deleted")

    # ------------------------------------------------------------------
    # CRUD operations (called from buttons)
    # ------------------------------------------------------------------
    def _collect_form(self):
        data = {}
        for key, entry in self.entries.items():
            val = entry.get().strip()
            if key == "age":
                data[key] = int(val) if val.isdigit() else 0
            else:
                data[key] = val
        return data

    def _validate_form(self, data):
        """Return (True, '') if ok, otherwise (False, error_msg)."""
        if not data["student_id"]:
            return False, "Student ID is required."
        if not data["name"]:
            return False, "Name is required."
        return True, ""

    def add_student(self):
        data = self._collect_form()
        ok, msg = self._validate_form(data)
        if not ok:
            messagebox.showwarning("Input error", msg)
            return
        if self.model.add_student(data):
            self.refresh_tree()
            self.clear_form()
            self._set_status("Student added")

    def update_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Select a row to update.")
            return
        data = self._collect_form()
        sid = self.tree.item(selected[0])["values"][1]   # student_id
        self.model.update_student(sid, data)
        self.refresh_tree()
        self.clear_form()
        self._set_status("Student updated")

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Select a row to delete.")
            return
        sid = self.tree.item(selected[0])["values"][1]
        if messagebox.askyesno("Confirm", "Delete this student?"):
            self.model.delete_student(sid)
            self.refresh_tree()
            self.clear_form()
            self._set_status("Student deleted")

    # ------------------------------------------------------------------
    # Search / refresh helpers
    # ------------------------------------------------------------------
    def search_students(self):
        term = self.search_var.get().strip()
        rows = self.model.search(term) if term else self.model.get_all()
        self._populate_tree(rows)

    def clear_search(self):
        self.search_var.set("")
        self.refresh_tree()

    def refresh_tree(self):
        rows = self.model.get_all()
        self._populate_tree(rows)
        self._set_status(f"{len(rows)} record(s) loaded")

    def _populate_tree(self, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    # ------------------------------------------------------------------
    # Form ↔ tree synchronization
    # ------------------------------------------------------------------
    def _populate_form_from_tree(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0])["values"]
        keys = list(self.entries.keys())
        for i, key in enumerate(keys, start=1):   # skip DB id (index 0)
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, values[i])

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    # ------------------------------------------------------------------
    # CSV import / export (menu actions)
    # ------------------------------------------------------------------
    def export_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Export to CSV"
        )
        if file_path:
            self.model.export_csv(file_path)
            self._set_status("Exported to CSV")

    def import_csv(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")],
            title="Import from CSV"
        )
        if file_path:
            self.model.import_csv(file_path)
            self.refresh_tree()
            self._set_status("CSV data imported")

    # ------------------------------------------------------------------
    # About dialog
    # ------------------------------------------------------------------
    def show_about(self):
        messagebox.showinfo(
            "About",
            "Student Record Management System\n"
            "Demo version – built with Tkinter & SQLite.\n"
            "Author: Your Name"
        )


# ----------------------------------------------------------------------
#                         APPLICATION ENTRY POINT
# ----------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentView(root)
    root.mainloop()
