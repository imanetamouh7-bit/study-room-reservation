import json
import tkinter as tk
import sys
from pathlib import Path
from tkinter import messagebox, ttk
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / filename
    return Path(__file__).resolve().parent / filename

class StudyRoomApp:
    # =========================================================
    # COLORS
    # =========================================================

    BG = "#F4F7FB"
    CARD = "#FFFFFF"
    PRIMARY = "#1E3A5F"
    PRIMARY_LIGHT = "#2F5D8A"
    ACCENT = "#3B82C4"
    SUCCESS = "#2E8B57"
    SUCCESS_BG = "#E8F5EE"
    TEXT = "#1F2937"
    TEXT_LIGHT = "#6B7280"
    BORDER = "#D9E1EA"
    DANGER = "#C0392B"
    WHITE = "#FFFFFF"

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self, root):
        self.root = root

        self.root.title("Study Room Reservation System")
        self.root.iconbitmap(
             resource_path("study_room_icon.ico")
        )
        self.root.geometry("800x650")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG)

        self.api_url = tk.StringVar(
            value="http://127.0.0.1:8000"
        )

        self.api_key = tk.StringVar()

        self.rooms = []

        self.setup_styles()
        self.create_login_screen()

    # =========================================================
    # STYLES
    # =========================================================

    def setup_styles(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # Main table
        style.configure(
            "Treeview",
            background=self.WHITE,
            foreground=self.TEXT,
            rowheight=32,
            fieldbackground=self.WHITE,
            font=("Arial", 10),
            borderwidth=0,
        )

        style.configure(
            "Treeview.Heading",
            background=self.PRIMARY,
            foreground=self.WHITE,
            font=("Arial", 10, "bold"),
            padding=8,
        )

        style.map(
            "Treeview",
            background=[
                ("selected", "#DCEAF7")
            ],
            foreground=[
                ("selected", self.TEXT)
            ],
        )

        # Combobox
        style.configure(
            "TCombobox",
            padding=6,
            font=("Arial", 10),
        )

    # =========================================================
    # HELPER FUNCTIONS
    # =========================================================

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_header(self, title, subtitle=None):
        header = tk.Frame(
            self.root,
            bg=self.PRIMARY,
            height=95,
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        title_label = tk.Label(
            header,
            text=title,
            bg=self.PRIMARY,
            fg=self.WHITE,
            font=("Arial", 22, "bold"),
        )
        title_label.pack(
            anchor="w",
            padx=35,
            pady=(20, 0),
        )

        if subtitle:
            subtitle_label = tk.Label(
                header,
                text=subtitle,
                bg=self.PRIMARY,
                fg="#DCE7F2",
                font=("Arial", 10),
            )
            subtitle_label.pack(
                anchor="w",
                padx=37,
                pady=(3, 10),
            )

    def create_button(
        self,
        parent,
        text,
        command,
        width=22,
        color=None,
    ):
        if color is None:
            color = self.ACCENT

        button = tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            bg=color,
            fg=self.WHITE,
            activebackground=self.PRIMARY_LIGHT,
            activeforeground=self.WHITE,
            font=("Arial", 11, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=10,
            pady=9,
        )

        return button

    def create_back_button(self, command):
        return tk.Button(
            self.root,
            text="←  Back",
            command=command,
            width=16,
            bg="#E8EDF3",
            fg=self.TEXT,
            activebackground="#D8E0E9",
            activeforeground=self.TEXT,
            font=("Arial", 10, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=8,
        )

    # =========================================================
    # LOGIN SCREEN
    # =========================================================

    def create_login_screen(self):
        self.clear_screen()

        # Header
        header = tk.Frame(
            self.root,
            bg=self.PRIMARY,
            height=150,
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        logo = tk.Label(
            header,
            text="📚",
            bg=self.PRIMARY,
            fg=self.WHITE,
            font=("Arial", 30),
        )
        logo.pack(pady=(18, 0))

        title = tk.Label(
            header,
            text="Study Room Reservation System",
            bg=self.PRIMARY,
            fg=self.WHITE,
            font=("Arial", 22, "bold"),
        )
        title.pack()

        subtitle = tk.Label(
            header,
            text="Connect to the reservation database",
            bg=self.PRIMARY,
            fg="#DCE7F2",
            font=("Arial", 10),
        )
        subtitle.pack(pady=(2, 8))

        # Main card
        card = tk.Frame(
            self.root,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        card.pack(
            padx=100,
            pady=35,
            fill="x",
        )

        tk.Label(
            card,
            text="API Connection",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Arial", 16, "bold"),
        ).pack(
            anchor="w",
            padx=35,
            pady=(25, 20),
        )

        # API URL
        url_frame = tk.Frame(
            card,
            bg=self.CARD,
        )
        url_frame.pack(
            fill="x",
            padx=35,
        )

        tk.Label(
            url_frame,
            text="API URL",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Arial", 10, "bold"),
        ).pack(
            anchor="w"
        )

        api_entry = tk.Entry(
            url_frame,
            textvariable=self.api_url,
            font=("Arial", 11),
            bg="#F8FAFC",
            fg=self.TEXT,
            relief="solid",
            bd=1,
        )
        api_entry.pack(
            fill="x",
            pady=(5, 15),
            ipady=7,
        )

        # API Key
        key_frame = tk.Frame(
            card,
            bg=self.CARD,
        )
        key_frame.pack(
            fill="x",
            padx=35,
        )

        tk.Label(
            key_frame,
            text="API Key",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Arial", 10, "bold"),
        ).pack(
            anchor="w"
        )

        key_entry = tk.Entry(
            key_frame,
            textvariable=self.api_key,
            show="•",
            font=("Arial", 11),
            bg="#F8FAFC",
            fg=self.TEXT,
            relief="solid",
            bd=1,
        )
        key_entry.pack(
            fill="x",
            pady=(5, 20),
            ipady=7,
        )

        # Connect
        connect_button = self.create_button(
            card,
            "🔗  Connect to API",
            self.connect_to_api,
            width=25,
            color=self.ACCENT,
        )

        connect_button.pack(
            pady=(0, 10),
        )

        self.status_label = tk.Label(
            card,
            text="●  Not connected",
            bg=self.CARD,
            fg=self.TEXT_LIGHT,
            font=("Arial", 10),
        )
        self.status_label.pack(
            pady=(5, 25)
        )

    # =========================================================
    # CONNECT TO API
    # =========================================================

    def connect_to_api(self):
        url = self.api_url.get().strip()
        api_key = self.api_key.get().strip()

        if not url:
            messagebox.showerror(
                "Error",
                "Please enter the API URL.",
            )
            return

        if not api_key:
            messagebox.showerror(
                "Error",
                "Please enter the API key.",
            )
            return

        try:
            request = Request(
                f"{url}/rooms",
                headers={
                    "X-API-Key": api_key,
                    "Accept": "application/json",
                },
            )

            with urlopen(
                request,
                timeout=5
            ) as response:

                data = json.loads(
                    response.read().decode("utf-8")
                )

            self.rooms = data

            self.status_label.config(
                text=f"●  Connected successfully  •  "
                f"{len(data)} rooms found",
                fg=self.SUCCESS,
            )

            messagebox.showinfo(
                "Connection successful",
                f"Connection to the API was successful.\n\n"
                f"{len(data)} rooms found.",
            )

            self.show_main_screen(data)

        except HTTPError as error:
            messagebox.showerror(
                "Connection error",
                f"HTTP error {error.code}.\n\n"
                "Please check your API key.",
            )

        except URLError:
            messagebox.showerror(
                "Connection error",
                "Could not connect to the API.\n\n"
                "Make sure the backend is running.",
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"An unexpected error occurred:\n\n{error}",
            )

    # =========================================================
    # MAIN SCREEN
    # =========================================================

    def show_main_screen(self, rooms):
        self.clear_screen()

        self.rooms = rooms

        self.create_header(
            "📚  Study Room Reservation",
            "Manage study rooms and reservations",
        )

        # Connection status
        status_frame = tk.Frame(
            self.root,
            bg=self.SUCCESS_BG,
        )
        status_frame.pack(
            fill="x",
            padx=45,
            pady=(25, 10),
        )

        tk.Label(
            status_frame,
            text="●  Connected to API",
            bg=self.SUCCESS_BG,
            fg=self.SUCCESS,
            font=("Arial", 10, "bold"),
        ).pack(
            anchor="w",
            padx=15,
            pady=10,
        )

        # Room section
        tk.Label(
            self.root,
            text="Available Study Rooms",
            bg=self.BG,
            fg=self.TEXT,
            font=("Arial", 17, "bold"),
        ).pack(
            anchor="w",
            padx=45,
            pady=(15, 10),
        )

        # Room table card
        table_frame = tk.Frame(
            self.root,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        table_frame.pack(
            padx=45,
            fill="x",
        )

        tree = ttk.Treeview(
            table_frame,
            columns=(
                "room",
                "capacity",
            ),
            show="headings",
            height=5,
        )

        tree.heading(
            "room",
            text="🏫  Room",
        )

        tree.heading(
            "capacity",
            text="👥  Capacity",
        )

        tree.column(
            "room",
            width=300,
            anchor="center",
        )

        tree.column(
            "capacity",
            width=250,
            anchor="center",
        )

        for room in rooms:
            tree.insert(
                "",
                "end",
                values=(
                    room["room_number"],
                    room["capacity"],
                ),
            )

        tree.pack(
            padx=10,
            pady=10,
            fill="x",
        )

        # Buttons
        button_frame = tk.Frame(
            self.root,
            bg=self.BG,
        )
        button_frame.pack(
            pady=22,
        )

        new_button = self.create_button(
            button_frame,
            "📅  New Reservation",
            self.create_reservation_screen,
            width=23,
            color=self.ACCENT,
        )
        new_button.grid(
            row=0,
            column=0,
            padx=8,
            pady=6,
        )

        reservations_button = self.create_button(
            button_frame,
            "📋  View Reservations",
            self.show_reservations,
            width=23,
            color=self.PRIMARY_LIGHT,
        )
        reservations_button.grid(
            row=0,
            column=1,
            padx=8,
            pady=6,
        )

        usage_button = self.create_button(
            button_frame,
            "📊  Room Usage",
            self.show_room_usage,
            width=23,
            color=self.SUCCESS,
        )
        usage_button.grid(
            row=1,
            column=0,
            padx=8,
            pady=6,
        )

        back_button = tk.Button(
            button_frame,
            text="←  Disconnect",
            command=self.create_login_screen,
            width=23,
            bg="#E8EDF3",
            fg=self.TEXT,
            activebackground="#D8E0E9",
            font=("Arial", 10, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=9,
        )
        back_button.grid(
            row=1,
            column=1,
            padx=8,
            pady=6,
        )

    # =========================================================
    # VIEW RESERVATIONS
    # =========================================================

    def show_reservations(self):
        self.clear_screen()

        self.create_header(
            "📋  Reservations",
            "All current study room reservations",
        )

        try:
            request = Request(
                f"{self.api_url.get().strip()}/reservations",
                headers={
                    "X-API-Key": self.api_key.get().strip(),
                    "Accept": "application/json",
                },
            )

            with urlopen(
                request,
                timeout=5
            ) as response:

                reservations = json.loads(
                    response.read().decode("utf-8")
                )

        except HTTPError as error:
            messagebox.showerror(
                "Error",
                f"HTTP error {error.code}.",
            )
            self.show_main_screen(self.rooms)
            return

        except URLError:
            messagebox.showerror(
                "Connection error",
                "Could not connect to the API.",
            )
            self.show_main_screen(self.rooms)
            return

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"An unexpected error occurred:\n\n{error}",
            )
            self.show_main_screen(self.rooms)
            return

        # Count
        count_label = tk.Label(
            self.root,
            text=f"{len(reservations)} reservation(s)",
            bg=self.BG,
            fg=self.TEXT_LIGHT,
            font=("Arial", 10),
        )
        count_label.pack(
            anchor="w",
            padx=45,
            pady=(20, 8),
        )

        # Table
        table_frame = tk.Frame(
            self.root,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        table_frame.pack(
            padx=35,
            fill="x",
        )

        tree = ttk.Treeview(
            table_frame,
            columns=(
                "id",
                "date",
                "start",
                "end",
                "student",
                "room",
            ),
            show="headings",
            height=10,
        )

        tree.heading("id", text="ID")
        tree.heading("date", text="Date")
        tree.heading("start", text="Start")
        tree.heading("end", text="End")
        tree.heading("student", text="Student")
        tree.heading("room", text="Room")

        tree.column("id", width=45, anchor="center")
        tree.column("date", width=100, anchor="center")
        tree.column("start", width=80, anchor="center")
        tree.column("end", width=80, anchor="center")
        tree.column("student", width=150, anchor="center")
        tree.column("room", width=80, anchor="center")

        for reservation in reservations:
            tree.insert(
                "",
                "end",
                values=(
                    reservation["reservation_id"],
                    reservation["date"],
                    reservation["start_time"],
                    reservation["end_time"],
                    reservation["student_name"],
                    reservation["room_number"],
                ),
            )

        tree.pack(
            padx=10,
            pady=10,
        )

        back_button = self.create_back_button(
            lambda: self.show_main_screen(self.rooms)
        )

        back_button.pack(
            pady=25,
        )

    # =========================================================
    # ROOM USAGE
    # =========================================================

    def show_room_usage(self):
        self.clear_screen()

        self.create_header(
            "📊  Room Usage",
            "Overview of reservation activity by room",
        )

        try:
            request = Request(
                f"{self.api_url.get().strip()}/rooms/usage",
                headers={
                    "X-API-Key": self.api_key.get().strip(),
                    "Accept": "application/json",
                },
            )

            with urlopen(
                request,
                timeout=5
            ) as response:

                usage = json.loads(
                    response.read().decode("utf-8")
                )

        except HTTPError as error:
            try:
                error_body = error.read().decode(
                    "utf-8"
                )
            except Exception:
                error_body = ""

            messagebox.showerror(
                "Error",
                f"HTTP error {error.code}.\n\n"
                f"{error_body}",
            )

            self.show_main_screen(self.rooms)
            return

        except URLError:
            messagebox.showerror(
                "Connection error",
                "Could not connect to the API.",
            )

            self.show_main_screen(self.rooms)
            return

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"An unexpected error occurred:\n\n{error}",
            )

            self.show_main_screen(self.rooms)
            return

        # Table
        table_frame = tk.Frame(
            self.root,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        table_frame.pack(
            padx=70,
            pady=30,
            fill="x",
        )

        tree = ttk.Treeview(
            table_frame,
            columns=(
                "room_id",
                "room",
                "capacity",
                "reservations",
            ),
            show="headings",
            height=7,
        )

        tree.heading(
            "room_id",
            text="ID",
        )

        tree.heading(
            "room",
            text="🏫  Room",
        )

        tree.heading(
            "capacity",
            text="👥  Capacity",
        )

        tree.heading(
            "reservations",
            text="📋  Reservations",
        )

        tree.column(
            "room_id",
            width=80,
            anchor="center",
        )

        tree.column(
            "room",
            width=160,
            anchor="center",
        )

        tree.column(
            "capacity",
            width=150,
            anchor="center",
        )

        tree.column(
            "reservations",
            width=180,
            anchor="center",
        )

        for room in usage:
            tree.insert(
                "",
                "end",
                values=(
                    room["room_id"],
                    room["room_number"],
                    room["capacity"],
                    room["reservation_count"],
                ),
            )

        tree.pack(
            padx=10,
            pady=10,
        )

        back_button = self.create_back_button(
            lambda: self.show_main_screen(self.rooms)
        )

        back_button.pack(
            pady=20,
        )

    # =========================================================
    # NEW RESERVATION
    # =========================================================

    def create_reservation_screen(self):
        self.clear_screen()

        self.create_header(
            "📅  New Reservation",
            "Create a new study room reservation",
        )

        card = tk.Frame(
            self.root,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        card.pack(
            padx=120,
            pady=25,
            fill="x",
        )

        form = tk.Frame(
            card,
            bg=self.CARD,
        )
        form.pack(
            padx=35,
            pady=25,
        )

        # Date
        tk.Label(
            form,
            text="Date",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Arial", 10, "bold"),
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=8,
        )

        date_entry = tk.Entry(
            form,
            width=30,
            font=("Arial", 10),
            relief="solid",
            bd=1,
        )
        date_entry.insert(
            0,
            "2026-08-25",
        )
        date_entry.grid(
            row=0,
            column=1,
            padx=20,
            pady=8,
            ipady=5,
        )

        # Start time
        tk.Label(
            form,
            text="Start time",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Arial", 10, "bold"),
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=8,
        )

        start_entry = tk.Entry(
            form,
            width=30,
            font=("Arial", 10),
            relief="solid",
            bd=1,
        )
        start_entry.insert(
            0,
            "10:00:00",
        )
        start_entry.grid(
            row=1,
            column=1,
            padx=20,
            pady=8,
            ipady=5,
        )

        # End time
        tk.Label(
            form,
            text="End time",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Arial", 10, "bold"),
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=8,
        )

        end_entry = tk.Entry(
            form,
            width=30,
            font=("Arial", 10),
            relief="solid",
            bd=1,
        )
        end_entry.insert(
            0,
            "12:00:00",
        )
        end_entry.grid(
            row=2,
            column=1,
            padx=20,
            pady=8,
            ipady=5,
        )

        # Student ID
        tk.Label(
            form,
            text="Student ID",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Arial", 10, "bold"),
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=8,
        )

        student_entry = tk.Entry(
            form,
            width=30,
            font=("Arial", 10),
            relief="solid",
            bd=1,
        )
        student_entry.insert(
            0,
            "1",
        )
        student_entry.grid(
            row=3,
            column=1,
            padx=20,
            pady=8,
            ipady=5,
        )

        # Room
        tk.Label(
            form,
            text="Study room",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Arial", 10, "bold"),
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=8,
        )

        room_values = [
            f'{room["room_id"]} - {room["room_number"]}'
            for room in self.rooms
        ]

        room_combo = ttk.Combobox(
            form,
            values=room_values,
            width=28,
            state="readonly",
        )

        if room_values:
            room_combo.current(0)

        room_combo.grid(
            row=4,
            column=1,
            padx=20,
            pady=8,
        )

        # Buttons
        button_frame = tk.Frame(
            self.root,
            bg=self.BG,
        )
        button_frame.pack(
            pady=10,
        )

        reserve_button = self.create_button(
            button_frame,
            "✓  Reserve Room",
            lambda: self.create_reservation(
                date_entry.get(),
                start_entry.get(),
                end_entry.get(),
                student_entry.get(),
                room_combo.get(),
            ),
            width=20,
            color=self.SUCCESS,
        )

        reserve_button.grid(
            row=0,
            column=0,
            padx=8,
        )

        back_button = self.create_back_button(
            lambda: self.show_main_screen(self.rooms)
        )

        back_button.grid(
            row=0,
            column=1,
            padx=8,
        )

    # =========================================================
    # CREATE RESERVATION
    # =========================================================

    def create_reservation(
        self,
        date_value,
        start_time,
        end_time,
        student_id,
        room_value,
    ):
        if not room_value:
            messagebox.showerror(
                "Error",
                "Please select a room.",
            )
            return

        try:
            student_id = int(student_id)
            room_id = int(
                room_value.split(" - ")[0]
            )

        except ValueError:
            messagebox.showerror(
                "Error",
                "Student ID must be a number.",
            )
            return

        data = {
            "date": date_value,
            "start_time": start_time,
            "end_time": end_time,
            "student_id": student_id,
            "room_id": room_id,
        }

        try:
            request = Request(
                f"{self.api_url.get().strip()}/reservations",
                data=json.dumps(data).encode("utf-8"),
                headers={
                    "X-API-Key": self.api_key.get().strip(),
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                method="POST",
            )

            with urlopen(
                request,
                timeout=5
            ) as response:

                result = json.loads(
                    response.read().decode("utf-8")
                )

            messagebox.showinfo(
                "Reservation successful",
                "✓ Reservation created successfully!\n\n"
                f"Reservation ID: "
                f"{result['reservation_id']}",
            )

            self.show_main_screen(self.rooms)

        except HTTPError as error:
            try:
                error_body = error.read().decode(
                    "utf-8"
                )
            except Exception:
                error_body = ""

            # Special handling for conflict
            if error.code == 409:
                messagebox.showwarning(
                    "Room unavailable",
                    "⚠ This room is already reserved "
                    "for this time period.\n\n"
                    "Please choose another room or "
                    "another time.",
                )
            else:
                messagebox.showerror(
                    "Reservation error",
                    f"HTTP error {error.code}.\n\n"
                    f"{error_body}",
                )

        except URLError:
            messagebox.showerror(
                "Connection error",
                "Could not connect to the API.\n\n"
                "Make sure the backend is running.",
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"An unexpected error occurred:\n\n{error}",
            )


# =============================================================
# START APPLICATION
# =============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = StudyRoomApp(root)
    root.mainloop()