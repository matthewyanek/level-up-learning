import tkinter as tk
from tkinter import ttk
from .components.sidebar import Sidebar
from .components.topbar import Topbar
from .components.map_area import MapArea
from .styles.color_schemes import ColorScheme

class UIManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Level Up Learning")
        self.root.geometry("1400x900")  # Increased window size
        
        # Configure root grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Initialize variables
        self.pages = {}
        self.is_fullscreen = False
        
        # Setup styles
        self.setup_styles()
        
        # Create main UI elements
        self.sidebar = Sidebar(self.root)
        self.sidebar.set_page_callback(self.show_page)
        self._create_pages()
        
        # Show default page
        self.show_page("Map Generator")

        # Bind fullscreen toggle
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

    def setup_styles(self):
        style = ttk.Style()
        
        # Entry style
        style.configure(
            "Modern.TEntry",
            fieldbackground="white",
            foreground=ColorScheme.TEXT_MUTED,
            borderwidth=0,
            relief="flat",
            padding=(8, 5.5)
        )
        
        # Combobox style
        style.configure(
            "Modern.TCombobox",
            background="white",
            fieldbackground="white",
            foreground=ColorScheme.TEXT_MUTED,
            borderwidth=0,
            relief="flat",
            padding=(8, 7),
            arrowsize=12
        )
        
        style.map('Modern.TCombobox',
            fieldbackground=[('readonly', 'white')],
            selectbackground=[('readonly', 'white')],
            foreground=[('readonly', ColorScheme.TEXT_MUTED)]
        )

        # Override system colors
        self.root.option_add('*TCombobox*Listbox.background', 'white')
        self.root.option_add('*TCombobox*Listbox.foreground', ColorScheme.TEXT_MUTED)
        self.root.option_add('*TCombobox*Listbox.selectBackground', 'white')
        self.root.option_add('*TCombobox*Listbox.selectForeground', ColorScheme.TEXT_MUTED)
        self.root.option_add('*TCombobox*Listbox.highlightThickness', '0')
        self.root.option_add('*TCombobox*Listbox.relief', 'flat')

    def _create_pages(self):
        # Map Generator page
        map_page = tk.Frame(self.root, bg=ColorScheme.PRIMARY_DARK)
        self.topbar = Topbar(map_page)  # Create topbar first
        self.map_area = MapArea(map_page, self.topbar)  # Create map_area second
        self.topbar.map_area = self.map_area  # Set map_area reference in topbar
        self.pages["Map Generator"] = map_page
        
        # Characters page
        char_page = tk.Frame(self.root, bg=ColorScheme.PRIMARY_DARK)
        self._create_characters_page(char_page)
        self.pages["Characters"] = char_page
        
        # Hide all pages initially
        for page in self.pages.values():
            page.grid_remove()

    def _create_characters_page(self, container):
        title = tk.Label(
            container,
            text="Characters",
            font=('TkDefaultFont', 20),
            fg=ColorScheme.TEXT_LIGHT,
            bg=ColorScheme.PRIMARY_DARK
        )
        title.pack(pady=20)

    def show_page(self, page_name):
        # Hide all pages
        for page in self.pages.values():
            page.grid_remove()
        
        # Show selected page
        if page_name in self.pages:
            self.pages[page_name].grid(row=0, column=1, sticky="nsew")

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)

    def exit_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.root.attributes("-fullscreen", False)

    def run(self):
        """Start the application main loop"""
        self.root.mainloop()