import json
import pygame

# Клас який зберігає налаштування гри під час робити програми
class GameConfig():
    _instance = None # зберігає єдиний створений екземпляр цього класу

    # Створює новий екземпляр класу.
    # Працює так: якщо ще не було створено екземпляра то створити та 
    # встановити розмір екрану (0, 0) і вкінці повертає сам екземпляр.
    def __new__(cls):
        # сls - стандартний параметр для функції __new__
        # що є самим класом.
        # Повертає створений екземпляр класу
        if cls._instance == None:
            cls._instance = super().__new__(cls)
            cls._instance.set_window_size(0, 0)
            cls._instance.controls_type = "A, D, SPACE"
            cls._instance.controls = {
                "Left": pygame.K_a,
                "Right": pygame.K_d,
                "Jump": pygame.K_SPACE
            }
            cls._instance.game_data = {}

        return cls._instance
        
    # Встановлює розмір вікна
    def set_window_size(self, width, height):
        # width - ширина вікна
        # height - висота вікна
        # Нічого не повертає
        self.window_width = width
        self.window_height = height

    # Повератає розмір вікна
    def get_window_size(self):
        return self.window_width, self.window_height
    
    # Завантаження прогесу гри
    def load_progress(self, file):
        with open(file, "r") as file:
            self.game_data = json.load(file)

    # Завантаження конфігу гри
    def load_config(self, file):
        self.load_progress(file)

        self.controls_type = self.game_data["controls"]
        if self.game_data["controls"] == "Arrows":
            self.controls = {
                "Left": pygame.K_LEFT,
                "Right": pygame.K_RIGHT,
                "Jump": pygame.K_UP
            }

    # Збереження конфігу гри
    def save_config(self, file, game_screen):
        data = {}

        player = game_screen.player
        data["player_max_health"] = player.max_health
        data["player_health"] = player.health
        data["player_damage_bonus"] = player.damage_bonus
        data["controls"] = self.controls_type

        level_manager = game_screen.level_manager
        data["level_name"] = [name for name, level in level_manager.levels.items() if level == level_manager.current_level][0]

        with open(file, "w") as file:
            json.dump(data, file)