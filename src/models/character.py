# src/models/character.py
import random
from ..utils.logger import Logger

class Character:
    def __init__(self, name, character_class):
        self.logger = Logger()
        self.name = name
        self.character_class = character_class
        self.level = 1
        self.experience = 0
        self.stats = self.get_base_stats(character_class)
        self.skills = self.get_class_skills(character_class)
        self.history = []  # Track character development
        self.logger.info(f"Created new character: {name} ({character_class})")
        
    def get_base_stats(self, character_class):
        base_stats = {
            "explorer": {
                "Health": 100,
                "Energy": 120,
                "Intelligence": 8,
                "Wisdom": 10,
                "Speed": 12,
                "Luck": 10,
                "Learning Rate": 1.2,
                "Problem Solving": 8,
                "Memory": 7,
                "Focus": 9
            },
            "scholar": {
                "Health": 90,
                "Energy": 100,
                "Intelligence": 15,
                "Wisdom": 12,
                "Speed": 8,
                "Luck": 8,
                "Learning Rate": 1.5,
                "Problem Solving": 12,
                "Memory": 12,
                "Focus": 11
            },
            "collector": {
                "Health": 110,
                "Energy": 110,
                "Intelligence": 10,
                "Wisdom": 8,
                "Speed": 10,
                "Luck": 12,
                "Learning Rate": 1.1,
                "Problem Solving": 9,
                "Memory": 10,
                "Focus": 8
            },
            "strategist": {
                "Health": 95,
                "Energy": 105,
                "Intelligence": 12,
                "Wisdom": 15,
                "Speed": 9,
                "Luck": 9,
                "Learning Rate": 1.3,
                "Problem Solving": 14,
                "Memory": 9,
                "Focus": 12
            }
        }
        return base_stats[character_class.lower()]

    def get_class_skills(self, character_class):
        class_skills = {
            "explorer": {
                "Adaptive Learning": 1,
                "Quick Thinking": 1,
                "Pattern Recognition": 1
            },
            "scholar": {
                "Deep Analysis": 1,
                "Information Retention": 1,
                "Critical Thinking": 1
            },
            "collector": {
                "Resource Management": 1,
                "Knowledge Organization": 1,
                "Data Collection": 1
            },
            "strategist": {
                "Strategic Planning": 1,
                "Problem Decomposition": 1,
                "Logical Reasoning": 1
            }
        }
        return class_skills[character_class.lower()]

    def add_experience(self, amount):
        self.experience += amount
        self.logger.info(f"Character {self.name} gained {amount} experience")
        
        while self.experience >= self.get_experience_required():
            self.level_up()

    def get_experience_required(self):
        return 100 * (self.level ** 1.5)

    def level_up(self):
        old_level = self.level
        self.level += 1
        self.experience -= self.get_experience_required()
        
        # Improve stats based on class
        stat_improvements = self.get_level_up_stats()
        for stat, value in stat_improvements.items():
            self.stats[stat] += value

        # Improve skills
        skill_improvement = self.improve_skills()
        
        # Record history
        self.history.append({
            "event": "level_up",
            "from_level": old_level,
            "to_level": self.level,
            "stat_improvements": stat_improvements,
            "skill_improvements": skill_improvement
        })
        
        self.logger.info(f"Character {self.name} leveled up to {self.level}")

    def get_level_up_stats(self):
        improvements = {}
        class_bonuses = {
            "explorer": ["Speed", "Luck", "Learning Rate"],
            "scholar": ["Intelligence", "Memory", "Problem Solving"],
            "collector": ["Energy", "Memory", "Luck"],
            "strategist": ["Wisdom", "Problem Solving", "Focus"]
        }
        
        # Base improvements
        for stat in self.stats:
            improvements[stat] = round(random.uniform(0.5, 1.0), 2)
        
        # Class bonuses
        for stat in class_bonuses[self.character_class.lower()]:
            improvements[stat] += round(random.uniform(0.5, 1.0), 2)
            
        return improvements

    def improve_skills(self):
        skill = random.choice(list(self.skills.keys()))
        old_value = self.skills[skill]
        self.skills[skill] += 1
        return {"skill": skill, "from": old_value, "to": self.skills[skill]}

    def to_dict(self):
        return {
            "name": self.name,
            "class": self.character_class,
            "level": self.level,
            "experience": self.experience,
            "stats": self.stats,
            "skills": self.skills,
            "history": self.history
        }

    @classmethod
    def from_dict(cls, data):
        character = cls(data["name"], data["class"])
        character.level = data["level"]
        character.experience = data["experience"]
        character.stats = data["stats"]
        character.skills = data["skills"]
        character.history = data.get("history", [])
        return character

    def validate(self):
        """Validate character data integrity"""
        required_fields = ["name", "character_class", "level", "experience", "stats", "skills"]
        for field in required_fields:
            if not hasattr(self, field):
                raise ValueError(f"Missing required field: {field}")
        
        if self.level < 1:
            raise ValueError("Level cannot be less than 1")
        
        if self.experience < 0:
            raise ValueError("Experience cannot be negative")