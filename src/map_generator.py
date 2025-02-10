import random
import math

class MapGenerator:
    def __init__(self):
        # Define patterns
        self.patterns = {
            'random': {
                'terrain_weights': {
                    'plains': 0.15,
                    'forest': 0.15,
                    'hills': 0.1,
                    'mountain': 0.1,
                    'shallow_water': 0.1,
                    'desert': 0.1,
                    'swamp': 0.05,
                    'grassland': 0.1,
                    'jungle': 0.05,
                    'rocky': 0.05,
                    'ice': 0.05
                }
            }
        }

    def create_map(self, rows, cols, map_type):
        map_type = map_type.lower()
        # Generate the base map
        if map_type == "random":
            terrains = self.generate_random_pattern(rows, cols)
        elif map_type == "island":
            terrains = self.generate_island_pattern(rows, cols)
        elif map_type == "coast":
            terrains = self.generate_coast_pattern(rows, cols)
        elif map_type == "river vertical":
            terrains = self.generate_river_pattern(rows, cols, "vertical")
        elif map_type == "river horizontal":
            terrains = self.generate_river_pattern(rows, cols, "horizontal")
        else:
            terrains = self.generate_random_pattern(rows, cols)
        
        # Add special points to the map
        terrains = self.add_special_points(terrains)
        return terrains

    def generate_random_pattern(self, rows, cols):
        terrains = [[None for _ in range(cols)] for _ in range(rows)]
        weights = self.patterns['random']['terrain_weights']
        
        valid_terrains = list(weights.keys())
        valid_weights = list(weights.values())
        
        total_weight = sum(valid_weights)
        valid_weights = [w/total_weight for w in valid_weights]

        for row in range(rows):
            for col in range(cols):
                terrains[row][col] = random.choices(
                    valid_terrains, 
                    weights=valid_weights, 
                    k=1)[0]
        
        return terrains

    def generate_island_pattern(self, rows, cols):
        terrains = [["deep_water" for _ in range(cols)] for _ in range(rows)]
        center_row = rows // 2
        center_col = cols // 2
        max_distance = math.sqrt((rows/2)**2 + (cols/2)**2)
        
        for row in range(rows):
            for col in range(cols):
                distance = math.sqrt((row - center_row)**2 + (col - center_col)**2)
                normalized_distance = distance / max_distance
                
                if normalized_distance < 0.25:
                    terrains[row][col] = random.choice(["plains", "forest", "hills", "grassland"])
                elif normalized_distance < 0.35:
                    terrains[row][col] = random.choice(["plains", "forest", "hills", "mountain"])
                elif normalized_distance < 0.45:
                    terrains[row][col] = random.choice(["plains", "hills", "shallow_water"])
                elif normalized_distance < 0.55:
                    terrains[row][col] = "shallow_water"
        
        return terrains

    def generate_coast_pattern(self, rows, cols):
        terrains = [["plains" for _ in range(cols)] for _ in range(rows)]
        coast_position = int(cols * 0.75)
        variation = 3
        
        for row in range(rows):
            local_coast = coast_position + random.randint(-variation, variation)
            local_coast = max(int(cols * 0.7), min(int(cols * 0.8), local_coast))
            
            for col in range(cols):
                if col > local_coast + 1:
                    terrains[row][col] = "deep_water"
                elif col > local_coast:
                    terrains[row][col] = "shallow_water"
                else:
                    terrains[row][col] = random.choice(["plains", "forest", "hills", "mountain", "grassland"])
        
        return terrains

    def generate_river_pattern(self, rows, cols, direction):
        terrains = [[random.choice(["plains", "forest", "hills", "mountain", "grassland"]) 
                    for _ in range(cols)] for _ in range(rows)]
        
        if direction == "vertical":
            river_col = cols // 2
            current_col = river_col
            
            for row in range(rows):
                current_col += random.randint(-1, 1)
                current_col = max(1, min(cols-2, current_col))
                
                terrains[row][current_col] = "deep_water"
                terrains[row][current_col-1] = "shallow_water"
                terrains[row][current_col+1] = "shallow_water"
                
        else:  # horizontal
            river_row = rows // 2
            current_row = river_row
            
            for col in range(cols):
                current_row += random.randint(-1, 1)
                current_row = max(1, min(rows-2, current_row))
                
                terrains[current_row][col] = "deep_water"
                terrains[current_row-1][col] = "shallow_water"
                terrains[current_row+1][col] = "shallow_water"
        
        return terrains

    def add_special_points(self, terrains):
        rows = len(terrains)
        cols = len(terrains[0])
        
        # Find the outermost non-water positions
        possible_positions = []
        
        # Check each row and column from the outside in
        for layer in range(min(rows, cols) // 4):  # Check up to 1/4 of the map depth
            positions_this_layer = []
            
            # Check top and bottom rows of this layer
            for col in range(layer, cols - layer):
                # Top row
                if terrains[layer][col] not in ["deep_water", "shallow_water"]:
                    positions_this_layer.append((layer, col))
                # Bottom row
                if terrains[rows-1-layer][col] not in ["deep_water", "shallow_water"]:
                    positions_this_layer.append((rows-1-layer, col))
            
            # Check left and right columns of this layer
            for row in range(layer, rows - layer):
                # Left column
                if terrains[row][layer] not in ["deep_water", "shallow_water"]:
                    positions_this_layer.append((row, layer))
                # Right column
                if terrains[row][cols-1-layer] not in ["deep_water", "shallow_water"]:
                    positions_this_layer.append((row, cols-1-layer))
            
            # If we found positions in this layer, add them and stop looking deeper
            if positions_this_layer:
                possible_positions.extend(positions_this_layer)
                break
        
        # Place single exit (E) first
        if possible_positions:
            exit_pos = random.choice(possible_positions)
            terrains[exit_pos[0]][exit_pos[1]] = "E"
            possible_positions.remove(exit_pos)
        
            # Place spawn point (S) on remaining positions, trying to place it far from exit
            if possible_positions:
                # Try to find the position furthest from the exit
                max_distance = 0
                spawn_pos = None
                for pos in possible_positions:
                    distance = abs(pos[0] - exit_pos[0]) + abs(pos[1] - exit_pos[1])  # Manhattan distance
                    if distance > max_distance:
                        max_distance = distance
                        spawn_pos = pos
                
                if spawn_pos:
                    terrains[spawn_pos[0]][spawn_pos[1]] = "S"
        
        return terrains