# Імпорт необхідних матеріалів з бібліотек/скриптів
from .game_config import GameConfig # Конфіг гри (для легшої роботи з розмірами вікна по всьому проекту)
from .user_interface import Image, Button # Клас картинки та кнопки
from .player import Player
from .level import LevelManager, Level
from abc import abstractmethod # декоратор для абстрактного метода
import pygame
pygame.init()

# Конфіг гри
config = GameConfig()

# Клас екрану (абстрактний/батьківський)
class Screen():
    # Конструктор класу. Приймає параметр window(вікно гри)
    def __init__(self, window):
        self.window = window # вікно гри
        self.window_surface = self.window.window_surface # pygame.Surface цього вікна 

    # Встановлює себе як поточний екран вікна
    def set_screen(self):
        self.window.current_screen = self

    # Абстрактні методи класу
    # Відмальовка всіх об'єктів екрану
    @abstractmethod
    def draw(self):
        pass

    # Обробник подій об'єктів екрану
    @abstractmethod
    def events(self, event):
        # event - об'єкт типу pygame.event.Event, потрібен для обробки подій
        pass


# Клас екрану головного меню. Є спадкоємцем класу Screen
class MenuScreen(Screen):
    # Конструктор класу. Приймає параметер window()
    def __init__(self, window):
        # Конструктор супер-класу
        super().__init__(window)

        # Створення фону
        self.background = Image(path_to_image="game_assets\\images\\dead cells.jpg", size=config.get_window_size())

        # Кнопки для старту гри та виходу з програми
        w, h = config.get_window_size()
        self.start_button = Button(path_to_image="game_assets\\images\\button.png", size=(600, 100), position=(w/2-300, h/2), rotation=0)
        self.exit_button = Button(path_to_image="game_assets\\images\\button.png", size=(600, 100), position=(w/2-300, h/2+200), rotation=0)

        # Призначення подій на кожну з кнопок 
        self.start_button.add_action(self.window.game_screen.set_screen)
        self.exit_button.add_action(self.window.close)

    # Оновлення екрана
    def update_screen(self):
        pass

    # Відмальовування екрану
    def draw(self):
        self.background.draw(self.window_surface)
        self.start_button.draw(self.window_surface)
        self.exit_button.draw(self.window_surface)

    # Обробник подій екрану
    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.start_button.check_if_pressed(event)
            self.exit_button.check_if_pressed(event)

# Клас ігрового еркану
class GameScreen(Screen):
    def __init__(self, window):
        super().__init__(window)

        # Об'єкт для менеджменту рівнів + додання рівня
        self.level_manager = LevelManager()
        self.level_manager.add_level("first", Level("level.txt", (100, 100), {"B": "game_assets\\images\\block.png"}))

        # Гравець
        self.player = Player(position=(0, -1), size=(100, 200), animation_time=10, animation_sprite_size=16, level_manager=self.level_manager, temp="game_assets\\images\\player.png")

    # Оновлення екрана
    def update_screen(self):
        self.player.update(self.window.delta)

    # Відмальовування екрана
    def draw(self):
        self.window_surface.fill((0,0,0,0))
        self.player.draw(self.window_surface)
        self.level_manager.current_level.draw(self.window_surface)

    # Обробник подій екрана
    def events(self, event):
        pass