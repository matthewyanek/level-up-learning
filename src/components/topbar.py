import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
from datetime import datetime
from ..styles.color_schemes import ColorScheme

class Topbar:
    def __init__(self, parent):
        self.parent = parent
        self.map_area = None  # Will be set by UI Manager
        self.create_topbar()

    def create_topbar(self):
        # Top bar container
        self.top_bar = tk.Frame(
            self.parent,
            bg=ColorScheme.PRIMARY_DARK,
            height=50
        )
        self.top_bar.pack(fill="x", pady=(20, 0))
        
        # Controls container
        self.controls = tk.Frame(
            self.top_bar,
            bg=ColorScheme.PRIMARY_DARK
        )
        self.controls.pack(side="right", padx=20)
        
        self._create_controls()

    def _create_controls(self):
        # Size inputs
        size_frame = tk.Frame(
            self.controls, 
            bg=ColorScheme.PRIMARY_DARK,
            padx=0,
            pady=0
        )
        size_frame.pack(side="left", padx=5)
        
        # Width entry with default value
        self.width_entry = ttk.Entry(
            size_frame,
            style="Modern.TEntry",
            width=8
        )
        self.width_entry.insert(0, "25")
        self.width_entry.pack(side="left", padx=1, pady=1)
        
        # Height entry with default value
        self.height_entry = ttk.Entry(
            size_frame,
            style="Modern.TEntry",
            width=8
        )
        self.height_entry.insert(0, "25")
        self.height_entry.pack(side="left", padx=2, pady=1)
        
        # Map type dropdown using custom button and menu
        self.map_type_var = tk.StringVar(value="Random")
        options = ["Random", "Island", "Coast", "River Vertical", "River Horizontal"]
        
        # Create dropdown button
        self.map_type = tk.Button(
            self.controls,
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
            pady=5.5,
            cursor="hand2",
            font=('TkDefaultFont', 9),
            compound="left",
            anchor="w"
        )
        
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
        for option in options:
            self.dropdown_menu.add_command(
                label=option,
                command=lambda x=option: self._select_option(x)
            )
        
        # Bind click event to show menu
        self.map_type.bind('<Button-1>', self._show_menu)
        
        self.map_type.pack(side="left", padx=2, pady=0)
        
        # Action buttons
        self._create_action_buttons()

    def _show_menu(self, event):
        # Show the dropdown menu below the button
        self.dropdown_menu.post(
            event.widget.winfo_rootx(),
            event.widget.winfo_rooty() + event.widget.winfo_height()
        )

    def _select_option(self, option):
        # Update the button text and variable
        self.map_type_var.set(option)

    def _create_action_buttons(self):
        buttons = [
            ("Save", "💾", self.save_map),
            ("Load", "📂", self.load_map)
        ]
        
        for text, icon, command in buttons:
            btn_container = tk.Frame(
                self.controls,
                bg=ColorScheme.PRIMARY_DARK
            )
            btn_container.pack(side="left", padx=2)
            
            btn = tk.Button(
                btn_container,
                text=f"{icon}",
                bg=ColorScheme.ACCENT_PINK,
                fg=ColorScheme.TEXT_LIGHT,
                relief="flat",
                width=2,
                height=1,
                font=('TkDefaultFont', 11),
                command=command
            )
            btn.pack(expand=True, pady=0)
            btn.bind("<Enter>", lambda e: e.widget.configure(bg=ColorScheme.HOVER))
            btn.bind("<Leave>", lambda e: e.widget.configure(bg=ColorScheme.ACCENT_PINK))

    def save_map(self):
        if not self.map_area.map_drawer.current_map:
            messagebox.showwarning("No Map", "Generate a map before saving!")
            return
            
        # Create default maps directory
        save_dir = os.path.join(os.path.expanduser("~"), "LevelUpLearning", "maps")
        os.makedirs(save_dir, exist_ok=True)
        
        # Default filename with timestamp
        default_filename = f"map_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        default_path = os.path.join(save_dir, default_filename)
        
        file_path = filedialog.asksaveasfilename(
            initialdir=save_dir,
            initialfile=default_filename,
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Map"
        )
        
        if file_path:
            map_data = {
                "map": self.map_area.map_drawer.current_map,
                "width": int(self.width_entry.get()),
                "height": int(self.height_entry.get()),
                "map_type": self.map_type_var.get()
            }
            
            try:
                with open(file_path, 'w') as f:
                    json.dump(map_data, f)
                messagebox.showinfo("Success", f"Map saved successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving map: {e}")

    def load_map(self):
        # Use the same default directory for loading
        save_dir = os.path.join(os.path.expanduser("~"), "LevelUpLearning", "maps")
        os.makedirs(save_dir, exist_ok=True)
        
        file_path = filedialog.askopenfilename(
            initialdir=save_dir,
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Load Map"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    map_data = json.load(f)
                
                # Update UI elements
                self.width_entry.delete(0, tk.END)
                self.width_entry.insert(0, str(map_data["width"]))
                
                self.height_entry.delete(0, tk.END)
                self.height_entry.insert(0, str(map_data["height"]))
                
                self.map_type_var.set(map_data["map_type"])
                
                # Draw the loaded map
                self.map_area.map_drawer.draw_map(map_data["map"])
                messagebox.showinfo("Success", "Map loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading map: {e}")

    def toggle_fullscreen(self):
        # This will be connected to the UIManager's fullscreen toggle
        pass

    def get_map_settings(self):
        """Get the current values from the input fields"""
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            map_type = self.map_type_var.get()
            # Ensure minimum size and maximum size
            width = max(5, min(50, width))
            height = max(5, min(50, height))
            return width, height, map_type
        except ValueError:
            # Return default values if conversion fails
            return 25, 25, "Random"