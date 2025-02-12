import tkinter as tk
from src.ui_manager import UIManager

if __name__ == "__main__":
    root = tk.Tk()
    app = UIManager(root)
    app.run()