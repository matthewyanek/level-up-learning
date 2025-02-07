import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
from src.config_loader import ConfigLoader
from src.map_generator import MapGenerator
from src.map_drawer import MapDrawer
from src.ui_manager import UIManager

class MapCreator:
    def __init__(self, root):
        self.root = root
        
        # Get the directory where level_up_learning.py is located
        base_path = os.path.dirname(os.path.abspath(__file__))
        print(f"Base path: {base_path}")
        
        # Load configurations
        self.configs = ConfigLoader.load_all_configs(base_path)
        
        # Create UI manager and set up UI
        self.ui_manager = UIManager(root, self.configs)
        self.ui_manager.on_load_callback = self.load_map
        self.ui_manager.on_save_callback = self.save_map
        self.ui_manager.setup_ui()
        
        # Create other components
        self.map_generator = MapGenerator(self.configs)
        self.map_drawer = MapDrawer(self.ui_manager.canvas, self.configs)
        self.ui_manager.set_map_drawer(self.map_drawer)
        self.current_map = None

        # Add generate button with command
        generate_btn = ttk.Button(
            self.root,
            text="Generate Map",
            command=self.generate_map,
            style='Custom.TButton'
        )
        generate_btn.pack(pady=5)

    def generate_map(self):
        settings = self.ui_manager.get_map_settings()
        if settings:
            rows, cols, map_type = settings
            self.current_map = self.map_generator.create_map(rows, cols, map_type)
            self.map_drawer.draw_map(self.current_map)

    def save_map(self, file_path):
        try:
            if self.current_map:
                with open(file_path, 'w') as f:
                    json.dump(self.current_map, f)
            else:
                messagebox.showerror("Error", "No map to save! Generate a map first.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save map: {str(e)}")

    def load_map(self, file_path):
        try:
            with open(file_path, 'r') as f:
                self.current_map = json.load(f)
            self.map_drawer.draw_map(self.current_map)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load map: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MapCreator(root)
    root.mainloop()