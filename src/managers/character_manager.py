# src/managers/character_manager.py
import json
import os
import shutil
from datetime import datetime
from ..models.character import Character
from ..utils.logger import Logger

class CharacterManager:
    def __init__(self):
        self.logger = Logger()
        self.characters = {}
        self.data_dir = "data"
        self.data_file = os.path.join(self.data_dir, "characters.json")
        self.backup_dir = os.path.join(self.data_dir, "backups")
        
        # Create necessary directories
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        
        self.load_characters()

    def load_characters(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    if data:
                        self.characters = {
                            name: Character.from_dict(char_data) 
                            for name, char_data in data.items()
                        }
                        self.logger.info(f"Loaded {len(self.characters)} characters")
            else:
                self.logger.info("No existing character data found")
                self.save_characters()  # Create empty file
                
        except json.JSONDecodeError:
            self.logger.error("Corrupted character data file detected")
            self.backup_corrupted_file()
            self.characters = {}
            self.save_characters()
            
        except Exception as e:
            self.logger.error(f"Error loading characters: {str(e)}")
            self.characters = {}
            self.save_characters()

    def save_characters(self):
        try:
            # Create backup before saving
            self.create_backup()
            
            # Save current data
            with open(self.data_file, 'w') as f:
                character_data = {
                    name: char.to_dict() 
                    for name, char in self.characters.items()
                }
                json.dump(character_data, f, indent=4)
                
            self.logger.info("Characters saved successfully")
            
        except Exception as e:
            self.logger.error(f"Error saving characters: {str(e)}")
            raise

    def create_backup(self):
        if os.path.exists(self.data_file):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"characters_backup_{timestamp}.json")
            shutil.copy2(self.data_file, backup_file)
            self.logger.info(f"Created backup: {backup_file}")
            
            # Clean old backups (keep last 5)
            self.clean_old_backups()

    def clean_old_backups(self):
        backups = sorted([
            os.path.join(self.backup_dir, f) 
            for f in os.listdir(self.backup_dir)
        ])
        while len(backups) > 5:
            os.remove(backups[0])
            self.logger.info(f"Removed old backup: {backups[0]}")
            backups.pop(0)

    def backup_corrupted_file(self):
        if os.path.exists(self.data_file):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            corrupted_file = os.path.join(
                self.backup_dir, 
                f"characters_corrupted_{timestamp}.json"
            )
            shutil.move(self.data_file, corrupted_file)
            self.logger.warning(f"Moved corrupted file to: {corrupted_file}")

    def add_character(self, character):
        try:
            character.validate()  # Validate character data
            self.characters[character.name] = character
            self.save_characters()
            self.logger.info(f"Added character: {character.name}")
        except Exception as e:
            self.logger.error(f"Error adding character: {str(e)}")
            raise

    def delete_character(self, character_name):
        try:
            if character_name in self.characters:
                del self.characters[character_name]
                self.save_characters()
                self.logger.info(f"Deleted character: {character_name}")
            else:
                self.logger.warning(f"Character not found: {character_name}")
        except Exception as e:
            self.logger.error(f"Error deleting character: {str(e)}")
            raise

    def get_all_characters(self):
        return {
            name: {
                "class": char.character_class,
                "level": char.level,
                "stats": char.stats
            }
            for name, char in self.characters.items()
        }

    def get_character(self, name):
        return self.characters.get(name)

    def add_experience(self, character_name, amount):
        try:
            if character_name in self.characters:
                self.characters[character_name].add_experience(amount)
                self.save_characters()
                self.logger.info(f"Added {amount} experience to {character_name}")
            else:
                self.logger.warning(f"Character not found: {character_name}")
        except Exception as e:
            self.logger.error(f"Error adding experience: {str(e)}")
            raise

    def get_character_stats(self, character_name):
        try:
            if character_name in self.characters:
                char = self.characters[character_name]
                return {
                    "level": char.level,
                    "experience": char.experience,
                    "next_level": char.get_experience_required(),
                    "stats": char.stats,
                    "skills": char.skills,
                    "history": char.history
                }
            return None
        except Exception as e:
            self.logger.error(f"Error getting character stats: {str(e)}")
            return None