
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
from datetime import datetime

DB_NAME = "bloodcare.db"

# ============================================================
# BLOODCARE - BLOOD DONOR MANAGEMENT SYSTEM
# Tkinter + Python + SQLite
# ============================================================

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# -------------------- DATABASE --------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    full_name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS donors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    blood_group TEXT NOT NULL,
    contact TEXT NOT NULL,
    address TEXT NOT NULL,
    last_donation TEXT,
    available TEXT NOT NULL DEFAULT 'Yes',
    registered_by TEXT,
    created_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    blood_group TEXT NOT NULL,
    hospital TEXT NOT NULL,
    city TEXT NOT NULL,
    contact TEXT NOT NULL,
    units INTEGER NOT NULL,
    urgency TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pending',
    requested_by TEXT,
    created_at TEXT
)
""")
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -------------------- APPLICATION --------------------

class BloodCareApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BloodCare - Blood Donor Management System")
        self.root.geometry("1250x760")
        self.root.minsize(1050, 680)
        self.root.configure(bg="#f5f6fa")

        self.current_user = None
        self.current_role = None
        self.current_name = None

        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except:
            pass

        self.setup_styles()
        self.show_login()
        self.root.mainloop()

    def setup_styles(self):
        self.style.configure("Treeview", rowheight=32, font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), padding=8)
        self.style.configure("TCombobox", padding=6, font=("Segoe UI", 10))

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # -------------------- LOGIN / CREATE ACCOUNT --------------------

    def show_login(self):
        self.clear_root()
        self.root.configure(bg="#f5f6fa")

        outer = tk.Frame(self.root, bg="#f5f6fa")
        outer.pack(fill="both", expand=True)

        left = tk.Frame(outer, bg="#b5121b", width=470)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Label(left, text="BLOODCARE", font=("Segoe UI", 34, "bold"),
                 fg="white", bg="#b5121b").pack(pady=(145, 10))

        tk.Label(left, text="Blood Donor Management System",
                 font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#b5121b").pack()

        tk.Label(left,
                 text="Connect donors with people who need blood.\nFast. Organized. Reliable.",
                 font=("Segoe UI", 12), fg="#ffe5e5", bg="#b5121b",
                 justify="center").pack(pady=25)

        tk.Label(left, text="Tkinter  •  Python  •  SQLite",
                 font=("Segoe UI", 10), fg="#ffd7d7", bg="#b5121b").pack(
                     side="bottom", pady=35)

        right = tk.Frame(outer, bg="#f5f6fa")
        right.pack(side="right", fill="both", expand=True)

        card = tk.Frame(right, bg="white", highlightthickness=1,
                        highlightbackground="#dddddd")
        card.place(relx=0.5, rely=0.5, anchor="center", width=440, height=510)

        tk.Label(card, text="Welcome Back",
                 font=("Segoe UI", 24, "bold"),
                 fg="#222222", bg="white").pack(pady=(38, 5))

        tk.Label(card, text="Login to your BloodCare account",
                 font=("Segoe UI", 11), fg="#777777", bg="white").pack(
                     pady=(0, 25))

        tk.Label(card, text="Username", font=("Segoe UI", 10, "bold"),
                 fg="#444444", bg="white", anchor="w").pack(fill="x", padx=55)

        username = tk.Entry(card, font=("Segoe UI", 12), bd=1,
                            relief="solid", bg="#fafafa")
        username.pack(fill="x", padx=55, ipady=9, pady=(6, 16))

        tk.Label(card, text="Password", font=("Segoe UI", 10, "bold"),
                 fg="#444444", bg="white", anchor="w").pack(fill="x", padx=55)

        password = tk.Entry(card, font=("Segoe UI", 12), bd=1,
                            relief="solid", show="*", bg="#fafafa")
        password.pack(fill="x", padx=55, ipady=9, pady=(6, 20))

        def login():
            u = username.get().strip()
            p = password.get()

            if not u or not p:
                messagebox.showwarning("Missing Information",
                                       "Please enter username and password.")
                return

            cursor.execute(
                "SELECT username, role, full_name FROM users WHERE username=? AND password=?",
                (u, hash_password(p))
            )
            row = cursor.fetchone()

            if row:
                self.current_user, self.current_role, self.current_name = row
                self.show_dashboard()
            else:
                messagebox.showerror("Login Failed",
                                     "Invalid username or password.\nPlease create an account if you are a new user.")

        tk.Button(card, text="LOGIN", command=login,
                  bg="#b5121b", fg="white",
                  activebackground="#8f0e15", activeforeground="white",
                  font=("Segoe UI", 11, "bold"), bd=0, cursor="hand2").pack(
                      fill="x", padx=55, ipady=11)

        tk.Button(card, text="CREATE NEW ACCOUNT", command=self.show_signup,
                  bg="white", fg="#b5121b",
                  activebackground="#fff0f0", activeforeground="#8f0e15",
                  font=("Segoe UI", 10, "bold"),
                  bd=1, relief="solid", cursor="hand2").pack(
                      fill="x", padx=55, ipady=9, pady=(12, 5))

        tk.Label(card, text="New user? Create your own account first.",
                 font=("Segoe UI", 9), fg="#777777", bg="white").pack(pady=5)

        password.bind("<Return>", lambda e: login())
        username.focus()

    def show_signup(self):
        self.clear_root()
        self.root.configure(bg="#f5f6fa")

        card = tk.Frame(self.root, bg="white", highlightthickness=1,
                        highlightbackground="#dddddd")
        card.place(relx=0.5, rely=0.5, anchor="center", width=500, height=610)

        tk.Label(card, text="Create Your Account",
                 font=("Segoe UI", 25, "bold"),
                 fg="#222222", bg="white").pack(pady=(35, 5))

        tk.Label(card, text="Register once and use your own login details",
                 font=("Segoe UI", 11), fg="#777777", bg="white").pack(
                     pady=(0, 25))

        fields = {}
        field_names = [
            ("Full Name", False),
            ("Username", False),
            ("Password", True),
            ("Confirm Password", True)
        ]

        for label, secret in field_names:
            tk.Label(card, text=label, font=("Segoe UI", 10, "bold"),
                     fg="#444444", bg="white", anchor="w").pack(
                         fill="x", padx=65)
            entry = tk.Entry(card, font=("Segoe UI", 11), bd=1,
                             relief="solid", bg="#fafafa",
                             show="*" if secret else "")
            entry.pack(fill="x", padx=65, ipady=8, pady=(5, 13))
            fields[label] = entry

        note = tk.Label(
            card,
            text="The first account created on a fresh database becomes Admin.\n"
                 "All later accounts are regular Users.",
            font=("Segoe UI", 9), fg="#777777", bg="white",
            justify="center"
        )
        note.pack(pady=(0, 10))

        def create_account():
            full_name = fields["Full Name"].get().strip()
            username = fields["Username"].get().strip()
            pw = fields["Password"].get()
            confirm = fields["Confirm Password"].get()

            if not full_name or not username or not pw or not confirm:
                messagebox.showwarning("Missing Information",
                                       "Please fill all fields.")
                return

            if len(username) < 3:
                messagebox.showwarning("Invalid Username",
                                       "Username must contain at least 3 characters.")
                return

            if len(pw) < 6:
                messagebox.showwarning("Weak Password",
                                       "Password must contain at least 6 characters.")
                return

            if pw != confirm:
                messagebox.showerror("Password Error",
                                     "Passwords do not match.")
                return

            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            role = "admin" if count == 0 else "user"

            try:
                cursor.execute(
                    "INSERT INTO users(username,password,role,full_name) VALUES(?,?,?,?)",
                    (username, hash_password(pw), role, full_name)
                )
                conn.commit()

                if role == "admin":
                    messagebox.showinfo(
                        "Account Created",
                        "Account created successfully!\n\n"
                        "Because this is the first account in the system, "
                        "it has been given Admin access."
                    )
                else:
                    messagebox.showinfo(
                        "Account Created",
                        "Account created successfully!\n\n"
                        "You can now login using your own username and password."
                    )

                self.show_login()

            except sqlite3.IntegrityError:
                messagebox.showerror(
                    "Username Already Exists",
                    "This username is already registered.\nPlease choose another username."
                )

        tk.Button(card, text="CREATE ACCOUNT", command=create_account,
                  bg="#b5121b", fg="white", bd=0,
                  font=("Segoe UI", 11, "bold"), cursor="hand2").pack(
                      fill="x", padx=65, ipady=11)

        tk.Button(card, text="← BACK TO LOGIN", command=self.show_login,
                  bg="white", fg="#555555", bd=0,
                  font=("Segoe UI", 10, "bold"), cursor="hand2").pack(pady=14)

    # -------------------- DASHBOARD --------------------

    def show_dashboard(self):
        self.clear_root()

        top = tk.Frame(self.root, bg="#b5121b", height=72)
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(top, text="BLOODCARE", font=("Segoe UI", 22, "bold"),
                 fg="white", bg="#b5121b").pack(side="left", padx=25)

        tk.Label(top, text=f"Welcome, {self.current_name}  •  {self.current_role.title()}",
                 font=("Segoe UI", 10), fg="white", bg="#b5121b").pack(
                     side="right", padx=20)

        tk.Button(top, text="Logout", command=self.show_login,
                  bg="#8f0e15", fg="white", bd=0,
                  font=("Segoe UI", 10, "bold"), padx=15, pady=7,
                  cursor="hand2").pack(side="right", padx=5)

        side = tk.Frame(self.root, bg="#252a34", width=225)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)

        tk.Label(side, text="MAIN MENU", font=("Segoe UI", 10, "bold"),
                 fg="#9fa6b2", bg="#252a34").pack(anchor="w", padx=22, pady=(25, 12))

        menu = [
            ("Dashboard", self.show_dashboard_content),
            ("Find Donor", self.show_search_page),
            ("Add Donor", self.show_add_page),
            ("Blood Requests", self.show_requests_page),
        ]

        if self.current_role == "admin":
            menu += [
                ("Donor Records", self.show_records_page),
                ("Admin Panel", self.show_admin_page),
                ("Reports", self.show_reports_page),
            ]

        self.content = tk.Frame(self.root, bg="#f5f6fa")
        self.content.pack(side="right", fill="both", expand=True)

        for text, command in menu:
            tk.Button(side, text=text, command=command,
                      bg="#252a34", fg="white",
                      activebackground="#b5121b",
                      activeforeground="white",
                      anchor="w", bd=0,
                      font=("Segoe UI", 10, "bold"),
                      padx=22, pady=12,
                      cursor="hand2").pack(fill="x")

        self.show_dashboard_content()

    def page_title(self, title, subtitle=""):
        for w in self.content.winfo_children():
            w.destroy()

        tk.Label(self.content, text=title, font=("Segoe UI", 24, "bold"),
                 fg="#222222", bg="#f5f6fa").pack(anchor="w", padx=28, pady=(25, 2))

        if subtitle:
            tk.Label(self.content, text=subtitle, font=("Segoe UI", 10),
                     fg="#777777", bg="#f5f6fa").pack(anchor="w", padx=30, pady=(0, 20))

    def stat_card(self, parent, title, value, x):
        card = tk.Frame(parent, bg="white", highlightthickness=1,
                        highlightbackground="#e2e2e2")
        card.grid(row=0, column=x, padx=8, sticky="nsew", ipadx=10, ipady=14)
        tk.Label(card, text=title, font=("Segoe UI", 10, "bold"),
                 fg="#777777", bg="white").pack(anchor="w", padx=18, pady=(8, 3))
        tk.Label(card, text=value, font=("Segoe UI", 24, "bold"),
                 fg="#b5121b", bg="white").pack(anchor="w", padx=18)

    def show_dashboard_content(self):
        self.page_title("Dashboard", "Quick overview of your BloodCare system")

        stats = tk.Frame(self.content, bg="#f5f6fa")
        stats.pack(fill="x", padx=20)
        for i in range(4):
            stats.grid_columnconfigure(i, weight=1)

        cursor.execute("SELECT COUNT(*) FROM donors")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM donors WHERE available='Yes'")
        available = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(DISTINCT blood_group) FROM donors")
        groups = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM requests WHERE status='Pending'")
        pending = cursor.fetchone()[0]

        self.stat_card(stats, "TOTAL DONORS", str(total), 0)
        self.stat_card(stats, "AVAILABLE", str(available), 1)
        self.stat_card(stats, "BLOOD GROUPS", str(groups), 2)
        self.stat_card(stats, "PENDING REQUESTS", str(pending), 3)

        quick = tk.Frame(self.content, bg="white",
                         highlightthickness=1, highlightbackground="#e2e2e2")
        quick.pack(fill="x", padx=28, pady=25)

        tk.Label(quick, text="Quick Actions", font=("Segoe UI", 15, "bold"),
                 bg="white", fg="#222222").pack(anchor="w", padx=20, pady=(18, 12))

        row = tk.Frame(quick, bg="white")
        row.pack(fill="x", padx=20, pady=(0, 20))

        for title, command in [
            ("Find a Donor", self.show_search_page),
            ("Register Donor", self.show_add_page),
            ("Create Blood Request", self.show_requests_page)
        ]:
            tk.Button(row, text=title, command=command,
                      bg="#b5121b", fg="white", bd=0,
                      font=("Segoe UI", 10, "bold"),
                      padx=18, pady=12, cursor="hand2").pack(
                          side="left", padx=(0, 12))

    # -------------------- ADD DONOR --------------------

    def show_add_page(self):
        self.page_title("Register New Donor",
                        "Enter donor details and add them to the database.")

        form = tk.Frame(self.content, bg="white",
                        highlightthickness=1, highlightbackground="#e2e2e2")
        form.pack(fill="x", padx=28, pady=5)

        fields = {}
        labels = [
            ("Name", 0), ("Age", 1), ("Gender", 2), ("Blood Group", 3),
            ("Contact", 4), ("Address / City", 5), ("Last Donation", 6),
            ("Available", 7)
        ]

        for col in range(4):
            form.grid_columnconfigure(col, weight=1)

        for text, idx in labels:
            r = idx // 2
            c = (idx % 2) * 2
            tk.Label(form, text=text, font=("Segoe UI", 10, "bold"),
                     bg="white", fg="#444444").grid(
                         row=r, column=c, padx=(22, 8), pady=12, sticky="w")

            if text == "Gender":
                widget = ttk.Combobox(form, values=["Male", "Female", "Other"],
                                      state="readonly", width=25)
                widget.set("Male")
            elif text == "Blood Group":
                widget = ttk.Combobox(
                    form, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                    state="readonly", width=25)
                widget.set("A+")
            elif text == "Available":
                widget = ttk.Combobox(form, values=["Yes", "No"],
                                      state="readonly", width=25)
                widget.set("Yes")
            else:
                widget = tk.Entry(form, font=("Segoe UI", 10), bd=1,
                                  relief="solid", width=28)

            widget.grid(row=r, column=c+1, padx=(0, 22), pady=12, sticky="ew")
            fields[text] = widget

        def save():
            name = fields["Name"].get().strip()
            age = fields["Age"].get().strip()
            contact = fields["Contact"].get().strip()
            address = fields["Address / City"].get().strip()

            if not all([name, age, contact, address]):
                messagebox.showwarning("Missing Information",
                                       "Please fill all required fields.")
                return

            if not age.isdigit() or not (18 <= int(age) <= 65):
                messagebox.showwarning("Invalid Age",
                                       "Donor age must be between 18 and 65.")
                return

            if not contact.isdigit() or len(contact) != 10:
                messagebox.showwarning("Invalid Contact",
                                       "Enter a valid 10-digit contact number.")
                return

            cursor.execute("""
                INSERT INTO donors
                (name,age,gender,blood_group,contact,address,last_donation,
                 available,registered_by,created_at)
                VALUES(?,?,?,?,?,?,?,?,?,?)
            """, (
                name, int(age), fields["Gender"].get(), fields["Blood Group"].get(),
                contact, address, fields["Last Donation"].get().strip(),
                fields["Available"].get(), self.current_user,
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ))
            conn.commit()

            messagebox.showinfo("Success", "Donor registered successfully!")
            self.show_dashboard_content()

        tk.Button(form, text="ADD DONOR", command=save,
                  bg="#b5121b", fg="white", bd=0,
                  font=("Segoe UI", 10, "bold"),
                  padx=25, pady=11, cursor="hand2").grid(
                      row=4, column=1, pady=22, sticky="w")

    # -------------------- SEARCH DONOR --------------------

    def show_search_page(self):
        self.page_title("Find Suitable Donor",
                        "Search available donors by blood group and location.")

        controls = tk.Frame(self.content, bg="white",
                            highlightthickness=1, highlightbackground="#e2e2e2")
        controls.pack(fill="x", padx=28)

        tk.Label(controls, text="Blood Group", font=("Segoe UI", 10, "bold"),
                 bg="white").pack(side="left", padx=(18, 7), pady=15)

        bg_var = tk.StringVar(value="All")
        bg_box = ttk.Combobox(
            controls, textvariable=bg_var,
            values=["All", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
            state="readonly", width=10)
        bg_box.pack(side="left", padx=5)

        tk.Label(controls, text="City / Area", font=("Segoe UI", 10, "bold"),
                 bg="white").pack(side="left", padx=(20, 7))

        loc = tk.Entry(controls, font=("Segoe UI", 10), width=25,
                       relief="solid", bd=1)
        loc.pack(side="left", padx=5, ipady=5)

        columns = ("ID", "Name", "Age", "Gender", "Blood Group",
                   "Contact", "Address", "Last Donation", "Available")

        tree_frame = tk.Frame(self.content, bg="#f5f6fa")
        tree_frame.pack(fill="both", expand=True, padx=28, pady=18)

        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        widths = [50, 150, 55, 75, 95, 120, 130, 110, 80]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="center")

        tree.pack(side="top", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        def load_data(show_message=False):
            for item in tree.get_children():
                tree.delete(item)

            query = """
                SELECT id,name,age,gender,blood_group,contact,address,
                       last_donation,available
                FROM donors
                WHERE available='Yes'
            """
            params = []

            if bg_var.get() != "All":
                query += " AND blood_group=?"
                params.append(bg_var.get())

            if loc.get().strip():
                query += " AND LOWER(address) LIKE LOWER(?)"
                params.append("%" + loc.get().strip() + "%")

            query += " ORDER BY id DESC"

            cursor.execute(query, params)
            rows = cursor.fetchall()

            for row in rows:
                tree.insert("", "end", values=row)

            if show_message and not rows:
                messagebox.showinfo("No Donor Found",
                                    "No available donor matches your search.")

        tk.Button(controls, text="SEARCH", command=lambda: load_data(True),
                  bg="#b5121b", fg="white", bd=0,
                  font=("Segoe UI", 10, "bold"),
                  padx=18, pady=7, cursor="hand2").pack(side="left", padx=10)

        tk.Button(controls, text="VIEW ALL", command=load_data,
                  bg="#3f444d", fg="white", bd=0,
                  font=("Segoe UI", 10, "bold"),
                  padx=18, pady=7, cursor="hand2").pack(side="left", padx=2)

        load_data()

    # -------------------- RECORDS --------------------

    def show_records_page(self):
        self.page_title("Donor Records", "Admin-only donor database management.")

        frame = tk.Frame(self.content, bg="white")
        frame.pack(fill="both", expand=True, padx=28, pady=5)

        columns = ("ID", "Name", "Age", "Gender", "Blood", "Contact",
                   "Address", "Available", "Registered By")

        tree = ttk.Treeview(frame, columns=columns, show="headings")
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=110, anchor="center")

        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        def refresh():
            for item in tree.get_children():
                tree.delete(item)
            cursor.execute("""
                SELECT id,name,age,gender,blood_group,contact,address,
                       available,registered_by
                FROM donors ORDER BY id DESC
            """)
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)

        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Select Donor",
                                       "Please select a donor first.")
                return
            donor_id = tree.item(selected[0])["values"][0]
            if messagebox.askyesno("Confirm Delete", "Delete this donor record?"):
                cursor.execute("DELETE FROM donors WHERE id=?", (donor_id,))
                conn.commit()
                refresh()

        bottom = tk.Frame(self.content, bg="#f5f6fa")
        bottom.pack(fill="x", padx=28, pady=10)

        tk.Button(bottom, text="Refresh", command=refresh,
                  bg="#3f444d", fg="white", bd=0,
                  font=("Segoe UI", 10, "bold"), padx=18, pady=8).pack(
                      side="left", padx=(0, 8))
        tk.Button(bottom, text="Delete Selected", command=delete_selected,
                  bg="#b5121b", fg="white", bd=0,
                  font=("Segoe UI", 10, "bold"), padx=18, pady=8).pack(
                      side="left")

        refresh()

    # -------------------- BLOOD REQUESTS --------------------

    def show_requests_page(self):
        self.page_title("Emergency Blood Requests",
                        "Create and track blood requirements.")

        form = tk.Frame(self.content, bg="white",
                        highlightthickness=1, highlightbackground="#e2e2e2")
        form.pack(fill="x", padx=28, pady=5)

        entries = {}
        fields = [("Patient Name", 0), ("Hospital", 1), ("City", 2),
                  ("Contact", 3), ("Units", 4)]

        for text, r in fields:
            tk.Label(form, text=text, font=("Segoe UI", 10, "bold"),
                     bg="white").grid(row=r, column=0, padx=20, pady=8, sticky="w")
            e = tk.Entry(form, font=("Segoe UI", 10), width=28,
                         relief="solid", bd=1)
            e.grid(row=r, column=1, padx=10, pady=8, ipady=5)
            entries[text] = e

        tk.Label(form, text="Blood Group", font=("Segoe UI", 10, "bold"),
                 bg="white").grid(row=0, column=2, padx=20, pady=8, sticky="w")
        bg = ttk.Combobox(form, values=["A+","A-","B+","B-","AB+","AB-","O+","O-"],
                          state="readonly", width=25)
        bg.set("A+")
        bg.grid(row=0, column=3, padx=10, pady=8)

        tk.Label(form, text="Urgency", font=("Segoe UI", 10, "bold"),
                 bg="white").grid(row=1, column=2, padx=20, pady=8, sticky="w")
        urgency = ttk.Combobox(form, values=["Normal", "Urgent", "Critical"],
                               state="readonly", width=25)
        urgency.set("Urgent")
        urgency.grid(row=1, column=3, padx=10, pady=8)

        def create_request():
            vals = [entries[x].get().strip() for x, _ in fields]
            if not all(vals):
                messagebox.showwarning("Missing Information",
                                       "Please complete all request fields.")
                return
            if not vals[4].isdigit() or int(vals[4]) <= 0:
                messagebox.showwarning("Invalid Units",
                                       "Units must be a positive number.")
                return

            cursor.execute("""
                INSERT INTO requests
                (patient_name,blood_group,hospital,city,contact,units,urgency,
                 status,requested_by,created_at)
                VALUES(?,?,?,?,?,?,?,?,?,?)
            """, (vals[0], bg.get(), vals[1], vals[2], vals[3], int(vals[4]),
                  urgency.get(), "Pending", self.current_user,
                  datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            messagebox.showinfo("Request Created",
                                "Blood request submitted successfully.")
            load_requests()

        tk.Button(form, text="CREATE REQUEST", command=create_request,
                  bg="#b5121b", fg="white", bd=0,
                  font=("Segoe UI", 10, "bold"),
                  padx=20, pady=9).grid(row=4, column=3, padx=10, pady=15, sticky="w")

        table = tk.Frame(self.content, bg="#f5f6fa")
        table.pack(fill="both", expand=True, padx=28, pady=15)

        columns = ("ID","Patient","Blood","Hospital","City","Contact",
                   "Units","Urgency","Status","Date")
        tree = ttk.Treeview(table, columns=columns, show="headings")
        for c in columns:
            tree.heading(c, text=c)
            tree.column(c, width=105, anchor="center")
        tree.pack(fill="both", expand=True)

        def load_requests():
            for item in tree.get_children():
                tree.delete(item)
            cursor.execute("""
                SELECT id,patient_name,blood_group,hospital,city,contact,
                       units,urgency,status,created_at
                FROM requests ORDER BY id DESC
            """)
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)

        if self.current_role == "admin":
            def mark_completed():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Select Request",
                                           "Please select a request.")
                    return
                rid = tree.item(selected[0])["values"][0]
                cursor.execute("UPDATE requests SET status='Completed' WHERE id=?",
                               (rid,))
                conn.commit()
                load_requests()

            tk.Button(self.content, text="Mark Selected as Completed",
                      command=mark_completed, bg="#3f444d", fg="white", bd=0,
                      font=("Segoe UI", 10, "bold"), padx=18, pady=8).pack(
                          anchor="w", padx=28)

        load_requests()

    # -------------------- ADMIN PANEL --------------------

    def show_admin_page(self):
        self.page_title("Admin Panel", "Manage registered accounts and monitor the system.")

        panel = tk.Frame(self.content, bg="white",
                         highlightthickness=1, highlightbackground="#e2e2e2")
        panel.pack(fill="both", expand=True, padx=28, pady=5)

        tk.Label(panel, text="Registered Accounts",
                 font=("Segoe UI", 15, "bold"), bg="white").pack(
                     anchor="w", padx=20, pady=18)

        columns = ("ID", "Username", "Full Name", "Role")
        tree = ttk.Treeview(panel, columns=columns, show="headings", height=12)
        for c in columns:
            tree.heading(c, text=c)
            tree.column(c, width=200, anchor="center")
        tree.pack(fill="x", padx=20)

        def refresh_users():
            for item in tree.get_children():
                tree.delete(item)
            cursor.execute("SELECT id,username,full_name,role FROM users ORDER BY id")
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)

        def delete_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Select User", "Please select a user.")
                return

            values = tree.item(selected[0])["values"]
            uid, username, full_name, role = values

            if username == self.current_user:
                messagebox.showwarning("Not Allowed",
                                       "You cannot delete your own account.")
                return

            if messagebox.askyesno("Confirm Delete",
                                   f"Delete account '{username}'?"):
                cursor.execute("DELETE FROM users WHERE id=?", (uid,))
                conn.commit()
                refresh_users()

        tk.Button(panel, text="Refresh Accounts", command=refresh_users,
                  bg="#3f444d", fg="white", bd=0,
                  font=("Segoe UI", 10, "bold"), padx=18, pady=8).pack(
                      side="left", padx=20, pady=15)

        tk.Button(panel, text="Delete Selected Account", command=delete_user,
                  bg="#b5121b", fg="white", bd=0,
                  font=("Segoe UI", 10, "bold"), padx=18, pady=8).pack(
                      side="left", padx=5, pady=15)

        refresh_users()

    # -------------------- REPORTS --------------------

    def show_reports_page(self):
        self.page_title("Reports & Statistics",
                        "Quick system statistics for the administrator.")

        report = tk.Frame(self.content, bg="white",
                          highlightthickness=1, highlightbackground="#e2e2e2")
        report.pack(fill="both", expand=True, padx=28, pady=5)

        cursor.execute("SELECT blood_group, COUNT(*) FROM donors GROUP BY blood_group")
        blood_stats = cursor.fetchall()

        cursor.execute("SELECT available, COUNT(*) FROM donors GROUP BY available")
        availability = cursor.fetchall()

        tk.Label(report, text="Donor Statistics",
                 font=("Segoe UI", 16, "bold"), bg="white").pack(
                     anchor="w", padx=25, pady=(22, 15))

        frame1 = tk.Frame(report, bg="white")
        frame1.pack(side="left", fill="both", expand=True, padx=20)

        tk.Label(frame1, text="Blood Group Distribution",
                 font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w")

        for bg, count in blood_stats:
            row = tk.Frame(frame1, bg="#fff5f5")
            row.pack(fill="x", pady=3)
            tk.Label(row, text=bg, bg="#fff5f5",
                     font=("Segoe UI", 10, "bold"), width=10).pack(
                         side="left", padx=8, pady=6)
            tk.Label(row, text=str(count), bg="#fff5f5",
                     font=("Segoe UI", 10), width=8).pack(
                         side="right", padx=8)

        frame2 = tk.Frame(report, bg="white")
        frame2.pack(side="right", fill="both", expand=True, padx=20)

        tk.Label(frame2, text="Availability",
                 font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w")

        for status, count in availability:
            row = tk.Frame(frame2, bg="#f4f4f4")
            row.pack(fill="x", pady=3)
            tk.Label(row, text=status, bg="#f4f4f4",
                     font=("Segoe UI", 10, "bold"), width=10).pack(
                         side="left", padx=8, pady=6)
            tk.Label(row, text=str(count), bg="#f4f4f4",
                     font=("Segoe UI", 10), width=8).pack(
                         side="right", padx=8)

        tk.Label(report,
                 text="Statistics are generated directly from the SQLite database.",
                 font=("Segoe UI", 9), fg="#777777", bg="white").pack(
                     side="bottom", pady=20)


# -------------------- START --------------------
app = BloodCareApp()
