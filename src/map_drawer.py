import math

class MapDrawer:
    def __init__(self, canvas):
        self.canvas = canvas
        self.base_hex_size = 25  # Increased base size
        self.zoom_level = 1.0
        self.hex_size = self.base_hex_size * self.zoom_level
        self.current_map = None
        
        # Define terrain types directly
        self.terrain_types = {
            "plains": {
                "color": "#90EE90",
                "icon": "🌿",
                "movement_cost": 1
            },
            "forest": {
                "color": "#228B22",
                "icon": "🌳",
                "movement_cost": 2
            },
            "mountain": {
                "color": "#808080",
                "icon": "⛰️",
                "movement_cost": 3
            },
            "deep_water": {
                "color": "#0066CC",
                "icon": "",
                "movement_cost": 3
            },
            "shallow_water": {
                "color": "#66B2FF",
                "icon": "",
                "movement_cost": 2
            },
            "desert": {
                "color": "#F4A460",
                "icon": "🏜️",
                "movement_cost": 2
            },
            "swamp": {
                "color": "#4A5D23",
                "icon": "🌱",
                "movement_cost": 3
            },
            "hills": {
                "color": "#8B4513",
                "icon": "⛰️",
                "movement_cost": 2
            },
            "volcano": {
                "color": "#8B0000",
                "icon": "🌋",
                "movement_cost": 4
            },
            "ice": {
                "color": "#E0FFFF",
                "icon": "❄️",
                "movement_cost": 2
            },
            "jungle": {
                "color": "#006400",
                "icon": "🌴",
                "movement_cost": 3
            },
            "grassland": {
                "color": "#98FB98",
                "icon": "🌾",
                "movement_cost": 1
            },
            "rocky": {
                "color": "#A0522D",
                "icon": "🪨",
                "movement_cost": 2
            },
            "S": {
                "color": "#000000",
                "text_color": "#FFFFFF",
                "icon": "S",
                "movement_cost": 1
            },
            "E": {
                "color": "#000000",
                "text_color": "#FFFFFF",
                "icon": "E",
                "movement_cost": 1
            }
        }

    def zoom(self, factor, x=None, y=None):
        old_zoom = self.zoom_level
        self.zoom_level *= factor
        # Limit zoom level between 0.5 and 3.0
        self.zoom_level = max(0.5, min(3.0, self.zoom_level))
        
        if self.current_map:
            self.hex_size = self.base_hex_size * self.zoom_level
            self.draw_map(self.current_map)

    def reset_zoom(self):
        """Reset zoom level to default"""
        self.zoom_level = 1.0
        if self.current_map:
            self.hex_size = self.base_hex_size * self.zoom_level
            self.draw_map(self.current_map)

    def draw_map(self, map_data):
        if not map_data or not map_data[0]:
            print("Invalid map data")
            return
            
        self.current_map = map_data
        self.canvas.delete("all")
        rows = len(map_data)
        cols = len(map_data[0])
        
        # Calculate base hex size based on canvas size with padding
        canvas_width = self.canvas.winfo_width() - 40
        canvas_height = self.canvas.winfo_height() - 40
        width_size = canvas_width / (cols * 1.5 + 0.5)
        height_size = canvas_height / ((rows + 0.5) * math.sqrt(3))
        self.base_hex_size = min(width_size, height_size)
        self.hex_size = self.base_hex_size * self.zoom_level

        # Calculate total map width and height
        total_width = cols * 1.5 * self.hex_size + self.hex_size/2
        total_height = (rows + 0.5) * self.hex_size * math.sqrt(3)

        # Calculate offsets to center the map
        x_offset = (canvas_width - total_width) / 2 + 20
        y_offset = (canvas_height - total_height) / 2 + 20

        # Draw main hexagons
        for row in range(rows):
            for col in range(cols):
                terrain_type = map_data[row][col]
                if terrain_type not in self.terrain_types:
                    print(f"Warning: Unknown terrain type {terrain_type}")
                    continue
                    
                terrain_info = self.terrain_types[terrain_type]
                self.draw_hex(row, col, terrain_info, x_offset, y_offset)

    def draw_hex(self, row, col, terrain_info, x_offset, y_offset):
        # Calculate center of hexagon with offset
        x = x_offset + (col * 1.5 + 1) * self.hex_size
        y = y_offset + (row * math.sqrt(3) + 1) * self.hex_size
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