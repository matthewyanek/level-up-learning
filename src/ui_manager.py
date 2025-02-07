import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

class UIManager:
    def __init__(self, root, configs):
        self.root = root
        self.configs = configs
        self.canvas = None
        self.rows_entry = None
        self.cols_entry = None
        self.map_type_var = None
        self.on_load_callback = None
        self.on_save_callback = None
        self.current_map = None
        self.map_drawer = None

    def setup_ui(self):
        # Create main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create control panel
        control_panel = self.create_control_panel(main_frame)
        control_panel.pack(fill=tk.X, pady=(0, 10))

        # Create canvas
        self.canvas = tk.Canvas(
            main_frame,
            bg="#23272A",
            width=600,
            height=400
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind mouse wheel and key events for zoom
        self.canvas.bind('<MouseWheel>', self.on_mousewheel)  # Windows
        self.canvas.bind('<Button-4>', self.on_mousewheel)    # Linux up
        self.canvas.bind('<Button-5>', self.on_mousewheel)    # Linux down
        self.root.bind('<Key>', self.on_key)

    def create_control_panel(self, parent):
        control_frame = ttk.Frame(parent)

        # Left side controls (dimensions and map type)
        left_frame = ttk.Frame(control_frame)
        left_frame.pack(side=tk.LEFT, padx=5)

        # Dimensions controls
        dims_frame = ttk.Frame(left_frame)
        dims_frame.pack(side=tk.LEFT, padx=5)

        ttk.Label(dims_frame, text="Rows:").pack(side=tk.LEFT)
        self.rows_entry = ttk.Entry(dims_frame, width=5)
        self.rows_entry.insert(0, "25")
        self.rows_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(dims_frame, text="Cols:").pack(side=tk.LEFT)
        self.cols_entry = ttk.Entry(dims_frame, width=5)
        self.cols_entry.insert(0, "25")
        self.cols_entry.pack(side=tk.LEFT, padx=5)

        # Map type selection
        type_frame = ttk.Frame(left_frame)
        type_frame.pack(side=tk.LEFT, padx=5)

        ttk.Label(type_frame, text="Map Type:").pack(side=tk.LEFT)
        self.map_type_var = tk.StringVar(value="Random")
        map_type_menu = ttk.OptionMenu(
            type_frame,
            self.map_type_var,
            "Random",
            "Random",
            "Island",
            "Coast",
            "River Vertical",
            "River Horizontal"
        )
        map_type_menu.pack(side=tk.LEFT, padx=5)

        # Right side controls
        right_frame = ttk.Frame(control_frame)
        right_frame.pack(side=tk.RIGHT, padx=5)

        # Add zoom buttons
        zoom_frame = ttk.Frame(right_frame)
        zoom_frame.pack(side=tk.LEFT, padx=5)

        zoom_in_btn = ttk.Button(
            zoom_frame,
            text="Zoom In (+)",
            command=lambda: self.zoom(1.1)
        )
        zoom_in_btn.pack(side=tk.LEFT, padx=2)

        zoom_out_btn = ttk.Button(
            zoom_frame,
            text="Zoom Out (-)",
            command=lambda: self.zoom(0.9)
        )
        zoom_out_btn.pack(side=tk.LEFT, padx=2)

        # Add save/load buttons
        save_btn = ttk.Button(
            right_frame,
            text="Save Map",
            command=self.save_map
        )
        save_btn.pack(side=tk.RIGHT, padx=5)

        load_btn = ttk.Button(
            right_frame,
            text="Load Map",
            command=self.load_map
        )
        load_btn.pack(side=tk.RIGHT, padx=5)

        return control_frame

    def get_map_settings(self):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            map_type = self.map_type_var.get()
            
            if not (5 <= rows <= 50 and 5 <= cols <= 50):
                raise ValueError("Dimensions must be between 5 and 50")
                
            return rows, cols, map_type
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return None

    def save_map(self):
        if self.on_save_callback:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialdir=os.path.join(os.path.dirname(os.path.dirname(__file__)), "maps")
            )
            if file_path:
                self.on_save_callback(file_path)

    def load_map(self):
        if self.on_load_callback:
            file_path = filedialog.askopenfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialdir=os.path.join(os.path.dirname(os.path.dirname(__file__)), "maps")
            )
            if file_path:
                self.on_load_callback(file_path)

    def on_mousewheel(self, event):
        # Handle different systems' mousewheel events
        if event.num == 5 or event.delta < 0:
            self.zoom(0.9)
        if event.num == 4 or event.delta > 0:
            self.zoom(1.1)

    def on_key(self, event):
        if event.char == '+' or event.char == '=':
            self.zoom(1.1)
        elif event.char == '-' or event.char == '_':
            self.zoom(0.9)

    def zoom(self, factor):
        if self.map_drawer:
            self.map_drawer.zoom(factor)

    def set_map_drawer(self, map_drawer):
        self.map_drawer = map_drawer