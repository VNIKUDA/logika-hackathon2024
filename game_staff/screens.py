# Імпорт необхідних матеріалів з бібліотек/скриптів
from .game_config import GameConfig # Конфіг гри (для легшої роботи з розмірами вікна по всьому проекту)
from .user_interface import Image, Button # Клас картинки та кнопки
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

        # Створення фону та кнопки
        self.background = Image(path_to_image="game_assets\\images\\dead cells.jpg", size=config.get_window_size())
        self.button = Button(path_to_image="game_assets\\images\\button.png", size=(600, 100), position=(500, 300), rotation=50)

    # Відмальовування екрану
    def draw(self):
        self.background.draw(self.window_surface)
        self.button.draw(self.window_surface)

    # Обробник подій екрану
    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.button.check_if_pressed(event)


# Тестовий екран для перевірки роботи кнопок та зміни екранів
class TestScreen(Screen):
    def draw(self):
        self.window_surface.fill((0,0,0,0))

    def events(self, event):
        pass