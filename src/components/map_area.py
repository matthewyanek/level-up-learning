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
        # Main map frame with larger size and padding
        self.map_frame = tk.Frame(
            self.parent,
            bg=ColorScheme.PRIMARY_DARK
        )
        self.map_frame.pack(fill="both", expand=True, padx=40, pady=30)

        # Create canvas with dark background
        self.canvas = tk.Canvas(
            self.map_frame,
            bg="#121725",  # Dark blue background
            highlightthickness=0,
            width=800,
            height=600
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Initialize map drawer and generator
        self.map_drawer = MapDrawer(self.canvas)
        self.map_generator = MapGenerator()

        # Add zoom bindings for both Linux and Windows
        self.canvas.bind("<Button-4>", lambda e: self.map_drawer.zoom(1.1))  # Mouse wheel up (Linux)
        self.canvas.bind("<Button-5>", lambda e: self.map_drawer.zoom(0.9))  # Mouse wheel down (Linux)
        self.canvas.bind("<MouseWheel>", self.handle_mousewheel)  # Mouse wheel (Windows)

        # Create zoom controls frame
        zoom_frame = tk.Frame(
            self.map_frame,
            bg=ColorScheme.PRIMARY_DARK
        )
        zoom_frame.place(relx=0.98, rely=0.02, anchor="ne")

        # Zoom in button
        self.zoom_in_btn = tk.Button(
            zoom_frame,
            text="➕",
            bg=ColorScheme.ACCENT_ORANGE,
            fg=ColorScheme.TEXT_LIGHT,
            relief="flat",
            width=2,
            command=lambda: self.map_drawer.zoom(1.2)
        )
        self.zoom_in_btn.pack(pady=(0, 5))
        self.zoom_in_btn.bind("<Enter>", lambda e: e.widget.configure(bg=ColorScheme.HOVER))
        self.zoom_in_btn.bind("<Leave>", lambda e: e.widget.configure(bg=ColorScheme.ACCENT_ORANGE))

        # Zoom out button
        self.zoom_out_btn = tk.Button(
            zoom_frame,
            text="➖",
            bg=ColorScheme.ACCENT_ORANGE,
            fg=ColorScheme.TEXT_LIGHT,
            relief="flat",
            width=2,
            command=lambda: self.map_drawer.zoom(0.8)
        )
        self.zoom_out_btn.pack()
        self.zoom_out_btn.bind("<Enter>", lambda e: e.widget.configure(bg=ColorScheme.HOVER))
        self.zoom_out_btn.bind("<Leave>", lambda e: e.widget.configure(bg=ColorScheme.ACCENT_ORANGE))

        # Reset zoom button
        self.reset_zoom_btn = tk.Button(
            zoom_frame,
            text="↺",
            bg=ColorScheme.ACCENT_ORANGE,
            fg=ColorScheme.TEXT_LIGHT,
            relief="flat",
            width=2,
            command=self.reset_zoom
        )
        self.reset_zoom_btn.pack(pady=(5, 0))
        self.reset_zoom_btn.bind("<Enter>", lambda e: e.widget.configure(bg=ColorScheme.HOVER))
        self.reset_zoom_btn.bind("<Leave>", lambda e: e.widget.configure(bg=ColorScheme.ACCENT_ORANGE))

        # Generate Button Container
        generate_container = tk.Frame(
            self.parent,
            bg=ColorScheme.PRIMARY_DARK
        )
        generate_container.pack(side="bottom", pady=(0, 20))

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
        self.generate_btn.pack(side="bottom")
        self.generate_btn.bind("<Enter>", lambda e: e.widget.configure(bg=ColorScheme.HOVER))
        self.generate_btn.bind("<Leave>", lambda e: e.widget.configure(bg=ColorScheme.ACCENT_ORANGE))

    def handle_mousewheel(self, event):
        # Windows mousewheel events use event.delta
        # Delta is positive for wheel up, negative for wheel down
        if event.delta > 0:
            self.map_drawer.zoom(1.1)
        else:
            self.map_drawer.zoom(0.9)

    def reset_zoom(self):
        """Reset zoom level to default"""
        self.map_drawer.reset_zoom()

    def generate_map(self):
        # Get values from topbar
        width, height, map_type = self.topbar.get_map_settings()
        
        try:
            # Generate the map data
            map_data = self.map_generator.create_map(height, width, map_type)
            # Draw the map
            self.map_drawer.draw_map(map_data)
        except Exception as e:
            print(f"Error generating map: {e}")