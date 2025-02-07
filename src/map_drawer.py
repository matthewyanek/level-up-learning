import math

class MapDrawer:
    def __init__(self, canvas, configs):
        self.canvas = canvas
        self.configs = configs
        self.base_hex_size = 20  # Base size
        self.zoom_level = 1.0    # Current zoom level
        self.hex_size = self.base_hex_size * self.zoom_level
        self.current_map = None  # Store current map data

    def zoom(self, factor, x=None, y=None):
        old_zoom = self.zoom_level
        self.zoom_level *= factor
        # Limit zoom level between 0.5 and 3.0
        self.zoom_level = max(0.5, min(3.0, self.zoom_level))
        
        if self.current_map:
            self.hex_size = self.base_hex_size * self.zoom_level
            self.draw_map(self.current_map)

    def draw_map(self, map_data):
        if not map_data or not map_data[0]:
            print("Invalid map data")
            return
            
        self.current_map = map_data  # Store the current map
        self.canvas.delete("all")
        rows = len(map_data)
        cols = len(map_data[0])
        
        # Calculate base hex size based on canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        width_size = canvas_width / (cols * 1.5 + 0.5)
        height_size = canvas_height / ((rows + 0.5) * math.sqrt(3))
        self.base_hex_size = min(width_size, height_size)
        self.hex_size = self.base_hex_size * self.zoom_level

        # Draw hexagons
        for row in range(rows):
            for col in range(cols):
                terrain_type = map_data[row][col]
                if terrain_type not in self.configs['terrain_types']:
                    print(f"Warning: Unknown terrain type {terrain_type}")
                    continue
                    
                terrain_info = self.configs['terrain_types'][terrain_type]
                self.draw_hex(row, col, terrain_info)

    def draw_hex(self, row, col, terrain_info):
        # Calculate center of hexagon
        x = (col * 1.5 + 1) * self.hex_size
        y = (row * math.sqrt(3) + 1) * self.hex_size
        if col % 2:
            y += self.hex_size * math.sqrt(3) / 2

        # Calculate vertices
        vertices = []
        for i in range(6):
            angle = i * math.pi / 3
            vx = x + self.hex_size * math.cos(angle)
            vy = y + self.hex_size * math.sin(angle)
            vertices.extend([vx, vy])

        # Draw hexagon
        self.canvas.create_polygon(vertices, fill=terrain_info['color'], outline="black")
        
        # Draw the icon/text
        font_size = int(self.hex_size * 0.6)
        if 'text_color' in terrain_info:  # Special handling for S and E
            self.canvas.create_text(x, y, 
                                  text=terrain_info['icon'], 
                                  fill=terrain_info['text_color'],
                                  font=("TkDefaultFont", font_size, "bold"))
        else:  # Normal terrain icons
            self.canvas.create_text(x, y, 
                                  text=terrain_info['icon'], 
                                  font=("TkDefaultFont", font_size))