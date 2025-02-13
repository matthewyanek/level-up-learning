import tkinter as tk
from tkinter import ttk, messagebox
from src.styles.color_schemes import ColorScheme
from src.models.character import Character
from src.managers.character_manager import CharacterManager

class CharacterCreation:
    def __init__(self, parent):
        self.parent = parent
        self.character_manager = CharacterManager()
        self.create_character_screen()

    def create_character_screen(self):
        # Main content container
        self.container = tk.Frame(
            self.parent,
            bg=ColorScheme.PRIMARY_DARK
        )
        self.container.grid(row=0, column=0, sticky="nsew", padx=40, pady=20)
        self.container.grid_columnconfigure(0, weight=1)

        # Create New Character button
        new_char_btn = tk.Button(
            self.container,
            text="Create New Character",
            bg=ColorScheme.ACCENT_ORANGE,
            fg=ColorScheme.TEXT_LIGHT,
            relief="flat",
            padx=20,
            pady=10,
            font=('TkDefaultFont', 10),
            command=self.show_character_creation
        )
        new_char_btn.grid(row=0, column=0, sticky="w", pady=10)

        # Characters list frame
        self.characters_frame = tk.Frame(
            self.container,
            bg=ColorScheme.PRIMARY_DARK,
            relief="solid",
            bd=1
        )
        self.characters_frame.grid(row=1, column=0, sticky="nsew", pady=(20,0))
        self.characters_frame.grid_columnconfigure(0, weight=1)

        # Initialize character list
        self.update_character_list()

    def show_character_creation(self):
        # Create character creation window
        creation_window = tk.Toplevel(self.parent)
        creation_window.title("Create New Character")
        creation_window.configure(bg=ColorScheme.PRIMARY_DARK)
        
        # Center the window
        window_width = 600
        window_height = 700
        screen_width = creation_window.winfo_screenwidth()
        screen_height = creation_window.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        creation_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Create form container
        form_frame = tk.Frame(
            creation_window,
            bg=ColorScheme.PRIMARY_DARK
        )
        form_frame.pack(fill="both", expand=True, padx=40, pady=30)

        # Title
        title = tk.Label(
            form_frame,
            text="Create New Character",
            font=('TkDefaultFont', 24, 'bold'),
            bg=ColorScheme.PRIMARY_DARK,
            fg=ColorScheme.TEXT_LIGHT
        )
        title.pack(pady=(0, 20))

        # Name Entry
        name_frame = tk.Frame(form_frame, bg=ColorScheme.PRIMARY_DARK)
        name_frame.pack(fill="x", pady=10)
        
        tk.Label(
            name_frame,
            text="Character Name:",
            bg=ColorScheme.PRIMARY_DARK,
            fg=ColorScheme.TEXT_LIGHT
        ).pack(side="left")
        
        name_entry = ttk.Entry(
            name_frame,
            style="Modern.TEntry",
            width=30
        )
        name_entry.pack(side="left", padx=10)

        # Class Selection
        class_frame = tk.LabelFrame(
            form_frame,
            text="Choose Your Class",
            bg=ColorScheme.PRIMARY_DARK,
            fg=ColorScheme.TEXT_LIGHT,
            relief="solid",
            bd=1
        )
        class_frame.pack(fill="x", pady=20, padx=5)

        selected_class = tk.StringVar(value="Explorer")
        classes = ["Explorer", "Scholar", "Collector", "Strategist"]
        
        for class_name in classes:
            tk.Radiobutton(
                class_frame,
                text=class_name,
                variable=selected_class,
                value=class_name,
                bg=ColorScheme.PRIMARY_DARK,
                fg=ColorScheme.TEXT_LIGHT,
                selectcolor=ColorScheme.PRIMARY_DARK,
                activebackground=ColorScheme.PRIMARY_DARK,
                activeforeground=ColorScheme.TEXT_LIGHT
            ).pack(anchor="w", padx=10, pady=5)

        # Buttons
        button_frame = tk.Frame(form_frame, bg=ColorScheme.PRIMARY_DARK)
        button_frame.pack(fill="x", pady=20)

        tk.Button(
            button_frame,
            text="Create",
            bg=ColorScheme.ACCENT_ORANGE,
            fg=ColorScheme.TEXT_LIGHT,
            relief="flat",
            padx=20,
            pady=5,
            command=lambda: self.create_character(creation_window, name_entry.get(), selected_class.get())
        ).pack(side="right", padx=5)

        tk.Button(
            button_frame,
            text="Cancel",
            bg=ColorScheme.ACCENT_ORANGE,
            fg=ColorScheme.TEXT_LIGHT,
            relief="flat",
            padx=20,
            pady=5,
            command=creation_window.destroy
        ).pack(side="right", padx=5)

    def create_character(self, window, name, character_class):
        if not name:
            messagebox.showerror("Error", "Please enter a character name")
            return
        
        if name in self.character_manager.characters:
            messagebox.showerror("Error", "A character with this name already exists")
            return

        # Create new character
        character = Character(name, character_class)
        self.character_manager.add_character(character)
        
        # Close the creation window
        window.destroy()
        
        # Update the character list
        self.update_character_list()

    def update_character_list(self):
        # Clear existing items
        for widget in self.characters_frame.winfo_children():
            widget.destroy()

        characters = self.character_manager.get_all_characters()
        
        if not characters:
            # Show placeholder if no characters
            placeholder = tk.Label(
                self.characters_frame,
                text="No characters created yet",
                fg=ColorScheme.TEXT_MUTED,
                bg=ColorScheme.PRIMARY_DARK,
                pady=20
            )
            placeholder.grid(row=0, column=0)
            return

        # Create character cards
        for idx, (name, data) in enumerate(characters.items()):
            self.create_character_card(idx, name, data)

    def create_character_card(self, idx, name, data):
        card = tk.Frame(
            self.characters_frame,
            bg=ColorScheme.PRIMARY_DARK,
            relief="solid",
            bd=1
        )
        card.grid(row=idx, column=0, sticky="ew", pady=5, padx=10)
        card.grid_columnconfigure(1, weight=1)

        # Character name and class
        tk.Label(
            card,
            text=name,
            font=('TkDefaultFont', 12, 'bold'),
            bg=ColorScheme.PRIMARY_DARK,
            fg=ColorScheme.TEXT_LIGHT
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")

        tk.Label(
            card,
            text=data['class'],
            bg=ColorScheme.PRIMARY_DARK,
            fg=ColorScheme.TEXT_MUTED
        ).grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Action buttons
        button_frame = tk.Frame(card, bg=ColorScheme.PRIMARY_DARK)
        button_frame.grid(row=0, column=2, padx=10, pady=5)

        # Edit button
        tk.Button(
            button_frame,
            text="✏️",
            bg=ColorScheme.ACCENT_ORANGE,
            fg=ColorScheme.TEXT_LIGHT,
            relief="flat",
            command=lambda: self.edit_character(name)
        ).pack(side="left", padx=2)

        # Delete button
        tk.Button(
            button_frame,
            text="🗑️",
            bg=ColorScheme.ACCENT_ORANGE,
            fg=ColorScheme.TEXT_LIGHT,
            relief="flat",
            command=lambda: self.delete_character(name)
        ).pack(side="left", padx=2)

    def edit_character(self, name):
        character = self.character_manager.get_character(name)
        if not character:
            return

        # Create edit window
        edit_window = tk.Toplevel(self.parent)
        edit_window.title(f"Edit Character: {name}")
        edit_window.configure(bg=ColorScheme.PRIMARY_DARK)
        
        # Center the window
        window_width = 600
        window_height = 700
        screen_width = edit_window.winfo_screenwidth()
        screen_height = edit_window.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        edit_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Create form container
        form_frame = tk.Frame(
            edit_window,
            bg=ColorScheme.PRIMARY_DARK
        )
        form_frame.pack(fill="both", expand=True, padx=40, pady=30)

        # Title
        title = tk.Label(
            form_frame,
            text=f"Edit Character: {name}",
            font=('TkDefaultFont', 24, 'bold'),
            bg=ColorScheme.PRIMARY_DARK,
            fg=ColorScheme.TEXT_LIGHT
        )
        title.pack(pady=(0, 20))

        # Name Entry
        name_frame = tk.Frame(form_frame, bg=ColorScheme.PRIMARY_DARK)
        name_frame.pack(fill="x", pady=10)
        
        tk.Label(
            name_frame,
            text="Character Name:",
            bg=ColorScheme.PRIMARY_DARK,
            fg=ColorScheme.TEXT_LIGHT
        ).pack(side="left")
        
        name_entry = ttk.Entry(
            name_frame,
            style="Modern.TEntry",
            width=30
        )
        name_entry.insert(0, character.name)
        name_entry.pack(side="left", padx=10)

        # Class Selection
        class_frame = tk.LabelFrame(
            form_frame,
            text="Character Class",
            bg=ColorScheme.PRIMARY_DARK,
            fg=ColorScheme.TEXT_LIGHT,
            relief="solid",
            bd=1
        )
        class_frame.pack(fill="x", pady=20, padx=5)

        selected_class = tk.StringVar(value=character.character_class)
        classes = ["Explorer", "Scholar", "Collector", "Strategist"]
        
        for class_name in classes:
            tk.Radiobutton(
                class_frame,
                text=class_name,
                variable=selected_class,
                value=class_name,
                bg=ColorScheme.PRIMARY_DARK,
                fg=ColorScheme.TEXT_LIGHT,
                selectcolor=ColorScheme.PRIMARY_DARK,
                activebackground=ColorScheme.PRIMARY_DARK,
                activeforeground=ColorScheme.TEXT_LIGHT
            ).pack(anchor="w", padx=10, pady=5)

        # Stats Display
        stats_frame = tk.LabelFrame(
            form_frame,
            text="Character Stats",
            bg=ColorScheme.PRIMARY_DARK,
            fg=ColorScheme.TEXT_LIGHT,
            relief="solid",
            bd=1
        )
        stats_frame.pack(fill="x", pady=20, padx=5)

        # Display current stats
        for stat, value in character.stats.items():
            stat_row = tk.Frame(stats_frame, bg=ColorScheme.PRIMARY_DARK)
            stat_row.pack(fill="x", padx=10, pady=2)
            
            tk.Label(
                stat_row,
                text=f"{stat}:",
                bg=ColorScheme.PRIMARY_DARK,
                fg=ColorScheme.TEXT_LIGHT,
                width=15,
                anchor="w"
            ).pack(side="left")
            
            tk.Label(
                stat_row,
                text=str(value),
                bg=ColorScheme.PRIMARY_DARK,
                fg=ColorScheme.TEXT_MUTED
            ).pack(side="left")

        # Experience and Level
        exp_frame = tk.Frame(form_frame, bg=ColorScheme.PRIMARY_DARK)
        exp_frame.pack(fill="x", pady=10)
        
        tk.Label(
            exp_frame,
            text=f"Level: {character.level}",
            bg=ColorScheme.PRIMARY_DARK,
            fg=ColorScheme.TEXT_LIGHT
        ).pack(side="left", padx=10)
        
        tk.Label(
            exp_frame,
            text=f"Experience: {character.experience}",
            bg=ColorScheme.PRIMARY_DARK,
            fg=ColorScheme.TEXT_LIGHT
        ).pack(side="left", padx=10)

        # Buttons
        button_frame = tk.Frame(form_frame, bg=ColorScheme.PRIMARY_DARK)
        button_frame.pack(fill="x", pady=20)

        tk.Button(
            button_frame,
            text="Save Changes",
            bg=ColorScheme.ACCENT_ORANGE,
            fg=ColorScheme.TEXT_LIGHT,
            relief="flat",
            padx=20,
            pady=5,
            command=lambda: self.save_character_changes(
                edit_window,
                character,
                name_entry.get(),
                selected_class.get()
            )
        ).pack(side="right", padx=5)

        tk.Button(
            button_frame,
            text="Cancel",
            bg=ColorScheme.ACCENT_ORANGE,
            fg=ColorScheme.TEXT_LIGHT,
            relief="flat",
            padx=20,
            pady=5,
            command=edit_window.destroy
        ).pack(side="right", padx=5)

    def save_character_changes(self, window, character, new_name, new_class):
        if not new_name:
            messagebox.showerror("Error", "Please enter a character name")
            return
        
        if new_name != character.name and new_name in self.character_manager.characters:
            messagebox.showerror("Error", "A character with this name already exists")
            return

        # If name changed, delete old character entry
        if new_name != character.name:
            self.character_manager.delete_character(character.name)
            character.name = new_name

        # Update class if changed
        if new_class != character.character_class:
            character.character_class = new_class
            # Optionally reset or adjust stats based on new class
            new_base_stats = character.get_base_stats(new_class)
            character.stats = new_base_stats
            character.skills = character.get_class_skills(new_class)

        # Save changes
        self.character_manager.add_character(character)
        
        # Close the edit window
        window.destroy()
        # Stats Display
        stats_frame = tk.LabelFrame(
            form_frame,
            text="Character Stats",
            bg=ColorScheme.PRIMARY_DARK,
            fg=ColorScheme.TEXT_LIGHT,
            relief="solid",
            bd=1
        )
        stats_frame.pack(fill="x", pady=20, padx=5)

        # Display current stats
        for stat, value in character.stats.items():
            stat_row = tk.Frame(stats_frame, bg=ColorScheme.PRIMARY_DARK)
            stat_row.pack(fill="x", padx=10, pady=2)
            
            tk.Label(
                stat_row,
                text=f"{stat}:",
                bg=ColorScheme.PRIMARY_DARK,
                fg=ColorScheme.TEXT_LIGHT,
                width=15,
                anchor="w"
            ).pack(side="left")
            
            tk.Label(
                stat_row,
                text=str(value),
                bg=ColorScheme.PRIMARY_DARK,
                fg=ColorScheme.TEXT_MUTED
            ).pack(side="left")

        # Experience and Level
        exp_frame = tk.Frame(form_frame, bg=ColorScheme.PRIMARY_DARK)
        exp_frame.pack(fill="x", pady=10)
        
        tk.Label(
            exp_frame,
            text=f"Level: {character.level}",
            bg=ColorScheme.PRIMARY_DARK,
            fg=ColorScheme.TEXT_LIGHT
        ).pack(side="left", padx=10)
        
        tk.Label(
            exp_frame,
            text=f"Experience: {character.experience}",
            bg=ColorScheme.PRIMARY_DARK,
            fg=ColorScheme.TEXT_LIGHT
        ).pack(side="left", padx=10)

        # Buttons
        button_frame = tk.Frame(form_frame, bg=ColorScheme.PRIMARY_DARK)
        button_frame.pack(fill="x", pady=20)

        tk.Button(
            button_frame,
            text="Save Changes",
            bg=ColorScheme.ACCENT_ORANGE,
            fg=ColorScheme.TEXT_LIGHT,
            relief="flat",
            padx=20,
            pady=5,
            command=lambda: self.save_character_changes(
                edit_window,
                character,
                name_entry.get(),
                selected_class.get()
            )
        ).pack(side="right", padx=5)

        tk.Button(
            button_frame,
            text="Cancel",
            bg=ColorScheme.ACCENT_ORANGE,
            fg=ColorScheme.TEXT_LIGHT,
            relief="flat",
            padx=20,
            pady=5,
            command=edit_window.destroy
        ).pack(side="right", padx=5)

    def save_character_changes(self, window, character, new_name, new_class):
        if not new_name:
            messagebox.showerror("Error", "Please enter a character name")
            return
        
        if new_name != character.name and new_name in self.character_manager.characters:
            messagebox.showerror("Error", "A character with this name already exists")
            return

        # If name changed, delete old character entry
        if new_name != character.name:
            self.character_manager.delete_character(character.name)
            character.name = new_name

        # Update class if changed
        if new_class != character.character_class:
            character.character_class = new_class
            # Optionally reset or adjust stats based on new class
            new_base_stats = character.get_base_stats(new_class)
            character.stats = new_base_stats
            character.skills = character.get_class_skills(new_class)

        # Save changes
        self.character_manager.add_character(character)
        
        # Close the edit window
        window.destroy()
        
        # Update the character list
        self.update_character_list()

    def delete_character(self, name):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {name}?"):
            self.character_manager.delete_character(name)
            self.update_character_list()        
