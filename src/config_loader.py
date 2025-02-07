import json
import os

class ConfigLoader:
    @staticmethod
    def load_all_configs(base_path):
        config_dir = os.path.join(base_path, 'config')
        configs = {}
        
        print(f"Looking for configs in: {config_dir}")
        
        if not os.path.exists(config_dir):
            raise FileNotFoundError(f"Config directory not found at: {config_dir}")
            
        for filename in os.listdir(config_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(config_dir, filename)
                print(f"Loading config file: {file_path}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        try:
                            configs[filename.replace('.json', '')] = json.loads(content)
                        except json.JSONDecodeError as e:
                            print(f"Error in {filename}:")
                            print(f"Error message: {str(e)}")
                            print(f"Content near error:")
                            start = max(0, e.pos - 20)
                            end = min(len(content), e.pos + 20)
                            print(content[start:end])
                            raise
                except Exception as e:
                    print(f"Error loading {filename}: {str(e)}")
                    raise
        return configs