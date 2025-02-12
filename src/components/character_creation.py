import tkinter as tk
from tkinter import ttk
from src.styles.color_schemes import ColorScheme  # Changed from relative import

class CharacterCreation:
    def __init__(self, parent):
        self.parent = parent
        self.create_character_screen()

    def create_character_screen(self):
        # Title
        title_frame = tk.Frame(
            self.parent,
            bg=ColorScheme.PRIMARY_DARK
        )
        title_frame.grid(row=0, column=0, sticky="ew", pady=(20,0))
        title_frame.grid_columnconfigure(0, weight=1)

        title = tk.Label(
            title_frame,
            text="Characters",
            font=('TkDefaultFont', 20),
            fg=ColorScheme.TEXT_LIGHT,
            bg=ColorScheme.PRIMARY_DARK
        )
        title.grid(row=0, column=0)

        # Main content container
        self.container = tk.Frame(
            self.parent,
            bg=ColorScheme.PRIMARY_DARK
        )
        self.container.grid(row=1, column=0, sticky="nsew", padx=40, pady=20)
        self.container.grid_columnconfigure(0, weight=1)

        # Create New Character button
        new_char_btn = tk.Button(
            self.container,
            text="Create New Character",
            bg=ColorScheme.ACCENT_ORANGE,
            fg=ColorScheme.TEXT_LIGHT,
            relief="flat",
            command=self.show_character_creation
        )
        new_char_btn.grid(row=0, column=0, sticky="w", pady=10)

        # Characters list (placeholder)
        self.characters_frame = tk.Frame(
            self.container,
            bg=ColorScheme.PRIMARY_DARK
        )
        self.characters_frame.grid(row=1, column=0, sticky="nsew")
        
        # Add some placeholder text for now
        placeholder = tk.Label(
            self.characters_frame,
            text="No characters created yet",
            fg=ColorScheme.TEXT_MUTED,
            bg=ColorScheme.PRIMARY_DARK
        )
        placeholder.pack(pady=20)

    def show_character_creation(self):
        # This method will be implemented later to show the character creation form
        print("Show character creation form")