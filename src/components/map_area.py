import tkinter as tk
from ..styles.color_schemes import ColorScheme
from ..map_drawer import MapDrawer
from ..map_generator import MapGenerator

class MapArea:
    def __init__(self, parent, topbar):
        self.parent = parent
        self.topbar = topbar
        self.create_map_area()

    def create_map_area(self):
        # Configure parent grid
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(1, weight=1)  # Row 0 is for topbar

        # Main map frame
        self.map_frame = tk.Frame(
            self.parent,
            bg=ColorScheme.PRIMARY_DARK
        )
        self.map_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=30)
        
        # Configure map frame grid
        self.map_frame.grid_columnconfigure(0, weight=1)
        self.map_frame.grid_rowconfigure(0, weight=1)

        # Create canvas
        self.canvas = tk.Canvas(
            self.map_frame,
            bg="#121725",
            highlightthickness=0,
            width=800,
            height=600
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Initialize map drawer and generator
        self.map_drawer = MapDrawer(self.canvas)
        self.map_generator = MapGenerator()

        # Bind zoom events
        self.canvas.bind("<Button-4>", lambda e: self.map_drawer.zoom(1.1))
        self.canvas.bind("<Button-5>", lambda e: self.map_drawer.zoom(0.9))
        self.canvas.bind("<MouseWheel>", self.handle_mousewheel)

        # Zoom controls frame (using place for overlay)
        zoom_frame = tk.Frame(
            self.map_frame,
            bg=ColorScheme.PRIMARY_DARK
        )
        zoom_frame.place(relx=0.98, rely=0.02, anchor="ne")

        # Zoom buttons
        self.zoom_in_btn = tk.Button(
            zoom_frame,
            text="➕",
            bg=ColorScheme.ACCENT_ORANGE,
            fg=ColorScheme.TEXT_LIGHT,
            relief="flat",
            width=2,
            command=lambda: self.map_drawer.zoom(1.2)
        )
        self.zoom_in_btn.grid(row=0, column=0, pady=(0, 5))
        self.zoom_in_btn.bind("<Enter>", lambda e: e.widget.configure(bg=ColorScheme.HOVER))
        self.zoom_in_btn.bind("<Leave>", lambda e: e.widget.configure(bg=ColorScheme.ACCENT_ORANGE))

        self.zoom_out_btn = tk.Button(
            zoom_frame,
            text="➖",
            bg=ColorScheme.ACCENT_ORANGE,
            fg=ColorScheme.TEXT_LIGHT,
            relief="flat",
            width=2,
            command=lambda: self.map_drawer.zoom(0.8)
        )
        self.zoom_out_btn.grid(row=1, column=0)
        self.zoom_out_btn.bind("<Enter>", lambda e: e.widget.configure(bg=ColorScheme.HOVER))
        self.zoom_out_btn.bind("<Leave>", lambda e: e.widget.configure(bg=ColorScheme.ACCENT_ORANGE))

        self.reset_zoom_btn = tk.Button(
            zoom_frame,
            text="↺",
            bg=ColorScheme.ACCENT_ORANGE,
            fg=ColorScheme.TEXT_LIGHT,
            relief="flat",
            width=2,
            command=self.reset_zoom
        )
        self.reset_zoom_btn.grid(row=2, column=0, pady=(5, 0))
        self.reset_zoom_btn.bind("<Enter>", lambda e: e.widget.configure(bg=ColorScheme.HOVER))
        self.reset_zoom_btn.bind("<Leave>", lambda e: e.widget.configure(bg=ColorScheme.ACCENT_ORANGE))

        # Generate button container
        generate_container = tk.Frame(
            self.parent,
            bg=ColorScheme.PRIMARY_DARK
        )
        generate_container.grid(row=2, column=0, pady=(0, 20))

        self.generate_btn = tk.Button(
            generate_container,
            text="Generate Map",
            bg=ColorScheme.ACCENT_ORANGE,
            fg=ColorScheme.TEXT_LIGHT,
            relief="flat",
            padx=15,
            pady=5,
            font=('TkDefaultFont', 10),
            command=self.generate_map
        )
        self.generate_btn.grid(row=0, column=0)
        self.generate_btn.bind("<Enter>", lambda e: e.widget.configure(bg=ColorScheme.HOVER))
        self.generate_btn.bind("<Leave>", lambda e: e.widget.configure(bg=ColorScheme.ACCENT_ORANGE))

    def handle_mousewheel(self, event):
        if event.delta > 0:
            self.map_drawer.zoom(1.1)
        else:
            self.map_drawer.zoom(0.9)

    def reset_zoom(self):
        self.map_drawer.reset_zoom()

    def generate_map(self):
        width, height, map_type = self.topbar.get_map_settings()
        try:
            map_data = self.map_generator.create_map(height, width, map_type)
            self.map_drawer.draw_map(map_data)
        except Exception as e:
            print(f"Error generating map: {e}")