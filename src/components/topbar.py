import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ..styles.color_schemes import ColorScheme

class Topbar:
    def __init__(self, parent):
        self.parent = parent
        self.map_area = None
        self.create_topbar()

    def create_topbar(self):
        # Create topbar frame
        self.frame = tk.Frame(
            self.parent,
            bg=ColorScheme.PRIMARY_DARK,
            height=50
        )
        self.frame.grid(row=0, column=0, sticky="ew", pady=(20, 0))
        self.frame.grid_propagate(False)
        
        # Configure grid
        self.frame.grid_columnconfigure(0, weight=1)  # Left empty space
        self.frame.grid_columnconfigure(1, weight=0)  # Controls area
        self.frame.grid_rowconfigure(0, weight=1)

        # Controls container
        controls = tk.Frame(
            self.frame,
            bg=ColorScheme.PRIMARY_DARK
        )
        controls.grid(row=0, column=1, padx=20)

        # Width entry
        self.width_var = tk.StringVar()
        self.width_entry = ttk.Entry(
            controls,
            textvariable=self.width_var,
            width=8,
            style="Modern.TEntry"
        )
        self.width_entry.grid(row=0, column=0, padx=1, pady=6)
        self.width_entry.insert(0, "Width")
        self.width_entry.bind("<FocusIn>", lambda e: self._on_entry_click(self.width_entry, "Width"))
        self.width_entry.bind("<FocusOut>", lambda e: self._on_focus_out(self.width_entry, "Width"))

        # Height entry
        self.height_var = tk.StringVar()
        self.height_entry = ttk.Entry(
            controls,
            textvariable=self.height_var,
            width=8,
            style="Modern.TEntry"
        )
        self.height_entry.grid(row=0, column=1, padx=2, pady=6)
        self.height_entry.insert(0, "Height")
        self.height_entry.bind("<FocusIn>", lambda e: self._on_entry_click(self.height_entry, "Height"))
        self.height_entry.bind("<FocusOut>", lambda e: self._on_focus_out(self.height_entry, "Height"))

        # Map type button (custom dropdown)
        self.map_type_var = tk.StringVar(value="Random")
        self.map_type = tk.Button(
            controls,
            textvariable=self.map_type_var,
            bg="white",
            fg=ColorScheme.TEXT_MUTED,
            activebackground="white",
            activeforeground=ColorScheme.TEXT_MUTED,
            highlightthickness=0,
            bd=1,
            width=20,
            height=1,
            relief="solid",
            pady=6,
            cursor="hand2",
            font=('TkDefaultFont', 9),
            compound="left",
            anchor="w"
        )
        self.map_type.grid(row=0, column=2, padx=2)

        # Create dropdown menu
        self.dropdown_menu = tk.Menu(
            self.map_type,
            tearoff=0,
            bg="white",
            fg=ColorScheme.TEXT_MUTED,
            activebackground="white",
            activeforeground=ColorScheme.TEXT_MUTED,
            relief="solid",
            bd=0
        )
        
        # Add menu items
        for option in ["Random", "Island", "Coast", "River Vertical", "River Horizontal"]:
            self.dropdown_menu.add_command(
                label=option,
                command=lambda x=option: self._select_option(x)
            )
        
        # Bind click event
        self.map_type.bind('<Button-1>', self._show_menu)

        # Buttons container
        buttons_frame = tk.Frame(
            controls,
            bg=ColorScheme.PRIMARY_DARK
        )
        buttons_frame.grid(row=0, column=3, padx=(2, 0))

        # Save Button
        self.save_button = tk.Button(
            buttons_frame,
            text="💾",
            bg=ColorScheme.ACCENT_PINK,
            fg=ColorScheme.TEXT_LIGHT,
            relief="flat",
            width=2,
            height=1,
            pady=3,
            padx=3,
            font=('TkDefaultFont', 9),
            command=self.save_map
        )
        self.save_button.grid(row=0, column=0, padx=1)
        self.save_button.bind("<Enter>", lambda e: e.widget.configure(bg=ColorScheme.HOVER))
        self.save_button.bind("<Leave>", lambda e: e.widget.configure(bg=ColorScheme.ACCENT_PINK))

        # Load Button
        self.load_button = tk.Button(
            buttons_frame,
            text="📂",
            bg=ColorScheme.ACCENT_PINK,
            fg=ColorScheme.TEXT_LIGHT,
            relief="flat",
            width=2,
            height=1,
            pady=3,
            padx=3,
            font=('TkDefaultFont', 9),
            command=self.load_map
        )
        self.load_button.grid(row=0, column=1, padx=1)
        self.load_button.bind("<Enter>", lambda e: e.widget.configure(bg=ColorScheme.HOVER))
        self.load_button.bind("<Leave>", lambda e: e.widget.configure(bg=ColorScheme.ACCENT_PINK))

    def _on_entry_click(self, entry, placeholder):
        """Handle entry field click"""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(foreground=ColorScheme.TEXT_DARK)

    def _on_focus_out(self, entry, placeholder):
        """Handle entry field focus out"""
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.config(foreground=ColorScheme.TEXT_MUTED)

    def _show_menu(self, event):
        self.dropdown_menu.post(
            event.widget.winfo_rootx(),
            event.widget.winfo_rooty() + event.widget.winfo_height()
        )

    def _select_option(self, option):
        self.map_type_var.set(option)

    def get_map_settings(self):
        try:
            # Get width, accounting for placeholder
            width_text = self.width_entry.get()
            width = int(width_text) if width_text != "Width" else 25

            # Get height, accounting for placeholder
            height_text = self.height_entry.get()
            height = int(height_text) if height_text != "Height" else 25

            map_type = self.map_type_var.get().lower()
            return width, height, map_type
        except ValueError:
            return 25, 25, "random"

    def save_map(self):
        if self.map_area:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".map",
                filetypes=[("Map files", "*.map"), ("All files", "*.*")]
            )
            if file_path:
                self.map_area.save_map(file_path)

    def load_map(self):
        if self.map_area:
            file_path = filedialog.askopenfilename(
                filetypes=[("Map files", "*.map"), ("All files", "*.*")]
            )
            if file_path:
                self.map_area.load_map(file_path)