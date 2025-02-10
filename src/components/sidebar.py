import tkinter as tk
from ..styles.color_schemes import ColorScheme

class Sidebar:
    def __init__(self, root, width=200, collapsed_width=50):
        self.root = root
        self.expanded = True
        self.width = width
        self.collapsed_width = collapsed_width
        self.create_sidebar()

    def create_sidebar(self):
        # Sidebar container
        self.sidebar = tk.Frame(
            self.root,
            bg=ColorScheme.PRIMARY_BLUE,
            width=self.width
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # Create toggle button
        self._create_toggle_button()
        
        # Create navigation buttons
        self.create_sidebar_button("Map Generator", 1)
        self.create_sidebar_button("Characters", 2)
        self.create_sidebar_button("Scenarios", 3)
        self.create_sidebar_button("Settings", 4)

    def _create_toggle_button(self):
        toggle_container = tk.Frame(
            self.sidebar,
            bg=ColorScheme.PRIMARY_BLUE
        )
        toggle_container.pack(fill="x", pady=(10,5))
        
        toggle_inner = tk.Frame(
            toggle_container,
            bg=ColorScheme.PRIMARY_BLUE,
            width=50
        )
        toggle_inner.pack(side="left")
        
        self.toggle_btn = tk.Label(
            toggle_inner,
            text="≡",
            bg=ColorScheme.PRIMARY_BLUE,
            fg=ColorScheme.TEXT_LIGHT,
            font=('TkDefaultFont', 14),
            anchor="center"
        )
        self.toggle_btn.pack(side="left", padx=15)
        self.toggle_btn.bind("<Button-1>", lambda e: self.toggle_sidebar())

    def create_sidebar_button(self, text, row):
        container = tk.Frame(
            self.sidebar,
            bg=ColorScheme.PRIMARY_BLUE
        )
        container.pack(fill="x", pady=2)
        
        icon_map = {
            "Map Generator": "🗺",
            "Characters": "👤",
            "Scenarios": "📚",
            "Settings": "⚙"
        }
        
        icon_label = tk.Label(
            container,
            text=icon_map.get(text, ""),
            bg=ColorScheme.PRIMARY_BLUE,
            fg=ColorScheme.TEXT_LIGHT,
            font=('TkDefaultFont', 14)
        )
        icon_label.pack(side="left", padx=15)
        
        text_label = tk.Label(
            container,
            text=text,
            bg=ColorScheme.PRIMARY_BLUE,
            fg=ColorScheme.TEXT_LIGHT,
            pady=8,
            anchor="w"
        )
        text_label.pack(side="left", fill="x", expand=True, padx=(0, 20))

        # Hover effects
        def on_hover_enter(event):
            container.configure(bg=ColorScheme.HOVER)
            icon_label.configure(bg=ColorScheme.HOVER)
            text_label.configure(bg=ColorScheme.HOVER)

        def on_hover_leave(event):
            container.configure(bg=ColorScheme.PRIMARY_BLUE)
            icon_label.configure(bg=ColorScheme.PRIMARY_BLUE)
            text_label.configure(bg=ColorScheme.PRIMARY_BLUE)

        for widget in (container, icon_label, text_label):
            widget.bind("<Enter>", on_hover_enter)
            widget.bind("<Leave>", on_hover_leave)
            widget.bind("<Button-1>", lambda e, t=text: self.on_page_select(t))

    def toggle_sidebar(self):
        if self.expanded:
            new_width = self.collapsed_width
            self.expanded = False
            for widget in self.sidebar.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label) and child.cget("text") not in "≡🗺👤📚⚙":
                            child.pack_forget()
        else:
            new_width = self.width
            self.expanded = True
            for widget in self.sidebar.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label):
                            if child.cget("text") in "≡🗺👤📚⚙":
                                child.pack(side="left", padx=15)
                            else:
                                child.pack(side="left", fill="x", expand=True, padx=(0, 20))
        
        self.sidebar.config(width=new_width)

    def set_page_callback(self, callback):
        self.on_page_select = callback