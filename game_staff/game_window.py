# Імпорт зі скрипту screens.py екрани Меню та для тестів
from .screens import MenuScreen, GameScreen, PauseScreen
import pygame
pygame.init()


# Вікно гри
class GameWindow():
    # Конструктор класу
    def __init__(self, window_size, title="game", framerate=60, flags=0):
        # Створення вікна та встановлення назви заголовка програми 
        self.window_surface = pygame.display.set_mode(window_size, flags)
        pygame.display.set_caption(title)

        # Таймер, який буде оновлювати гру та FPS
        self.clock = pygame.time.Clock()
        self.FPS = framerate
        self.delta = 0

        # Створення екранів меню та тестового
        self.pause_screen = PauseScreen(self)
        self.game_screen = GameScreen(self)
        self.menu_screen = MenuScreen(self)

        # # Додання події до кнопки в екрані меню для переходу на тестовий екран
        # self.menu_screen.button.add_action(self.test_screen.set_screen)

        # Поточний екран
        self.current_screen = self.menu_screen

        # Змінна, яка відображає стан вікна
        self.open = True

    # Закриття вікна
    def close(self):
        self.open = False

    # Оновлення вікна
    def update_window(self):
        pygame.display.update()
        self.delta = self.clock.tick(self.FPS)/10